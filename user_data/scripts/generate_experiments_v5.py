# -*- coding: utf-8 -*-
"""
V5 Experiment Generator — CryptoV11 基线（动态 G6 DC + G2 MACD 共振 + 阶梯 S5）
生成约 200 个独立策略文件 + experiment_manifest_v5.json。

Group notes:
- A4: 24 = 4×3×2（第二维为 bars2 = 2*bars1 或 2*bars1+4，loss2 = loss1+0.02）。
- A5: 10×2 MAX_BARS × timeout 阈值 + 1 个 (64, -0.025) 中点校准，共 21 条。
- B1: 在 fast < slow-4 下枚举全部 MACD 三元组（当前为 51 组，多于文案中的 40，以覆盖完整有效网格）。
- C: 基础 5×4 笛卡尔积去约束后 18 组，外加 (20,40)/(20,45) 共 20 组。
"""
from __future__ import annotations

import json
import os
from itertools import product
from typing import Any, Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA = os.path.dirname(SCRIPT_DIR)
STRATEGY_DIR = os.path.join(USER_DATA, "strategies")
EXPERIMENT_DIR = os.path.join(STRATEGY_DIR, "experiments_v5")
MANIFEST_PATH = os.path.join(USER_DATA, "experiment_manifest_v5.json")

os.makedirs(EXPERIMENT_DIR, exist_ok=True)

experiments: List[Dict[str, Any]] = []
_existing_classnames: set = set()


def save_strategy(classname: str, code: str, name: str, group: str, params: dict, config: str | None = None):
    if classname in _existing_classnames:
        raise RuntimeError(f"Duplicate classname: {classname}")
    path = os.path.join(EXPERIMENT_DIR, f"{classname}.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    entry: Dict[str, Any] = {"name": name, "strategy": classname, "group": group, "params": params}
    if config:
        entry["config"] = config
    experiments.append(entry)
    _existing_classnames.add(classname)


# ---------------------------------------------------------------------------
# Core template fragments (CryptoV11-style)
# ---------------------------------------------------------------------------
HEADER = '''"""{doc}"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import numpy as np
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)
'''

FOOTER_CONFIRM = '''
    def confirm_trade_entry(self, pair, order_type, amount, rate, time_in_force, current_time, entry_tag, side, **kwargs):
        closed_trades = Trade.get_trades_proxy(pair=pair, is_open=False)
        if closed_trades:
            last_trade = closed_trades[-1]
            if last_trade.exit_reason == 'stop_loss':
                if (current_time - last_trade.close_date_utc).total_seconds() < self.COOLDOWN_BARS * 15 * 60:
                    return False
        today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        today_losses = [t for t in Trade.get_trades_proxy(is_open=False) if t.close_date_utc and t.close_date_utc >= today_start and t.exit_reason == 'stop_loss']
        if len(today_losses) >= self.DAILY_MAX_LOSSES:
            return False
        return True
'''


def build_class_open(
    classname: str,
    trailing_stop: bool,
    stoploss: float = -0.10,
    trailing_stop_positive: float = 0.03,
    trailing_stop_positive_offset: float = 0.30,
    extra_class_attrs: str = "",
    informative_4h: bool = True,
) -> str:
    ts = "True" if trailing_stop else "False"
    lines = [
        f"class {classname}(IStrategy):",
        "    INTERFACE_VERSION = 3",
        "    timeframe = '15m'",
        "    can_short = True",
        "    startup_candle_count = 400",
        f"    stoploss = {stoploss}",
        "    use_custom_stoploss = False",
        f"    trailing_stop = {ts}",
        f"    trailing_stop_positive = {trailing_stop_positive}",
        f"    trailing_stop_positive_offset = {trailing_stop_positive_offset}",
        "    trailing_only_offset_is_reached = True",
        '    minimal_roi = {"0": 0.99}',
        '    order_types = {"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}',
        "",
        "    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):",
        "        return 5.0",
        "",
    ]
    if extra_class_attrs:
        lines.append(extra_class_attrs.rstrip() + "\n")
    if informative_4h:
        lines.extend(
            [
                "    @informative('4h')",
                "    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:",
                "        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)",
                "        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)",
                "        return dataframe",
                "",
            ]
        )
    return "\n".join(lines)


V11_BASE_ATTRS = """    ADX_MIN = 28
    ATR_MULT = 0.6
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    TIMEOUT_LOSS_THRESHOLD = -0.02
    ATR_LOOKBACK = 100
    DC_SHORT = 14
    DC_LONG = 40
    ATR_PCT_THRESHOLD = 0.7
    MACD_FAST = 8
    MACD_SLOW = 17
    MACD_SIGNAL = 9
"""


def indicators_v11_g6_macd_tail() -> str:
    """G6 dynamic DC + MACD block (after ema/adx/atr)."""
    return """
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        atr_pct = dataframe['atr'].rolling(self.ATR_LOOKBACK).apply(
            lambda x: float(DataFrame(x).rank(pct=True).iloc[-1].item()) if len(x) == self.ATR_LOOKBACK else np.nan,
            raw=False,
        )
        use_short = atr_pct < self.ATR_PCT_THRESHOLD
        dc_s = dataframe['high'].rolling(self.DC_SHORT).max().shift(1)
        dc_l = dataframe['high'].rolling(self.DC_LONG).max().shift(1)
        dataframe['dc_upper'] = np.where(use_short, dc_s, dc_l)
        _macd = ta.MACD(dataframe, fastperiod=self.MACD_FAST, slowperiod=self.MACD_SLOW, signalperiod=self.MACD_SIGNAL)
        dataframe['macd'] = _macd['macd']
        dataframe['macdsignal'] = _macd['macdsignal']
        dataframe['macdhist'] = _macd['macdhist']
        return dataframe
"""


def populate_indicators_v11_standard(prefix_extra: str = "") -> str:
    """Standard V11 populate_indicators: base + G6 + MACD + optional extra lines before return."""
    body = """
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
"""
    tail = indicators_v11_g6_macd_tail()
    if prefix_extra:
        # Insert extra calculations before `return dataframe` inside tail
        tail = tail.replace("        return dataframe", prefix_extra.rstrip() + "\n        return dataframe")
    return body + tail


def populate_indicators_v10_fixed_dc() -> str:
    """CryptoV10-style: fixed DC 20, no MACD."""
    return '''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['dc_upper'] = dataframe['high'].rolling(self.DC_PERIOD).max().shift(1)
        return dataframe
'''


def populate_indicators_fixed_dc_with_macd() -> str:
    """Fixed DC_PERIOD + MACD (ablation: no G6)."""
    return '''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['dc_upper'] = dataframe['high'].rolling(self.DC_PERIOD).max().shift(1)
        _macd = ta.MACD(dataframe, fastperiod=self.MACD_FAST, slowperiod=self.MACD_SLOW, signalperiod=self.MACD_SIGNAL)
        dataframe['macd'] = _macd['macd']
        dataframe['macdsignal'] = _macd['macdsignal']
        dataframe['macdhist'] = _macd['macdhist']
        return dataframe
'''


def populate_entry_trend_long(
    extra_macd_or_momentum: str,
    use_adx_rising: bool = True,
    use_4h_ema: bool = True,
    atr_mult_expr: str = "self.ATR_MULT",
) -> str:
    adx_r = "(dataframe['adx_rising'])" if use_adx_rising else "(True)"
    ema4h = "(dataframe['ema21_4h'] > dataframe['ema55_4h'])" if use_4h_ema else "(True)"
    return f'''
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * {atr_mult_expr})) &
            (dataframe['adx'] > self.ADX_MIN) & {adx_r} &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            {ema4h} &
            ({extra_macd_or_momentum})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
'''


def populate_exit_trend_empty() -> str:
    return '''
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe
'''


def custom_exit_block(
    use_stair: bool,
    use_dc_exit: bool = False,
    dc_min_bars: int = 0,
    profit_giveback: bool = False,
    stair_b1: int = 20,
    stair_l1: float = -0.06,
    stair_b2: int = 40,
    stair_l2: float = -0.04,
) -> str:
    stair_lines = ""
    if use_stair:
        stair_lines = f"""
        if bars_held >= {stair_b2} and current_profit < {stair_l2}:
            return "stair_late"
        if bars_held >= {stair_b1} and current_profit < {stair_l1}:
            return "stair_mid"
"""
    dc_block = ""
    if use_dc_exit:
        dc_block = f"""
        if bars_held >= {dc_min_bars}:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) > 0 and 'dc_lower_exit' in dataframe.columns:
                row = dataframe.iloc[-1]
                v = row.get('dc_lower_exit')
                if v is not None and not (isinstance(v, float) and np.isnan(v)):
                    if row['close'] < v:
                        return "dc_exit"
"""
    giveback = ""
    if profit_giveback:
        giveback = """
        if bars_held > 8:
            lo = self.MIN_PROFIT * self.KEEP_RATIO
            hi = self.MIN_PROFIT
            if lo < current_profit < hi:
                return "profit_giveback"
"""
    return f'''
    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
{dc_block}{stair_lines}{giveback}
        if bars_held >= self.MAX_BARS and current_profit < self.TIMEOUT_LOSS_THRESHOLD:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
'''


MACD_ENTRY_MODES: Dict[str, str] = {
    "hist_rise": "(dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))",
    "hist_pos": "(dataframe['macdhist'] > 0)",
    "macd_above_sig": "(dataframe['macd'] > dataframe['macdsignal'])",
    "macd_above_rise": "(dataframe['macd'] > dataframe['macdsignal']) & (dataframe['macd'] > dataframe['macd'].shift(1))",
    "hist_rise2": "(dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(2))",
    "no_macd": "(True)",
}

ENTRY_MACD_V11_BASE = MACD_ENTRY_MODES["hist_rise"]


def _v11_attrs_merge(base_tail: str = "") -> str:
    return V11_BASE_ATTRS.rstrip() + ("\n" + base_tail if base_tail else "")


def _emit_v11_strategy(
    classname: str,
    doc: str,
    group: str,
    name: str,
    params: dict,
    extra_attrs: str,
    indicators_code: str,
    entry_code: str,
    use_stair: bool = True,
    stair_b1: int = 20,
    stair_l1: float = -0.06,
    stair_b2: int = 40,
    stair_l2: float = -0.04,
    stoploss: float = -0.10,
    trail_pos: float = 0.03,
    trail_off: float = 0.30,
    trailing_on: bool = True,
):
    code = (
        HEADER.format(doc=doc)
        + build_class_open(
            classname,
            trailing_stop=trailing_on,
            stoploss=stoploss,
            trailing_stop_positive=trail_pos,
            trailing_stop_positive_offset=trail_off,
            extra_class_attrs=extra_attrs,
        )
        + indicators_code
        + entry_code
        + populate_exit_trend_empty()
        + custom_exit_block(
            use_stair=use_stair,
            use_dc_exit=False,
            stair_b1=stair_b1,
            stair_l1=stair_l1,
            stair_b2=stair_b2,
            stair_l2=stair_l2,
        )
        + FOOTER_CONFIRM
    )
    save_strategy(classname, code, name, group, params)


# =============================================================================
# Group A — Exit system grid
# =============================================================================
def gen_ga1_trailing_grid():
    """A1: 6 x 5 = 30 trailing grid."""
    tps = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]
    offs = [0.20, 0.25, 0.30, 0.35, 0.40]
    idx = 0
    for tp, off in product(tps, offs):
        idx += 1
        cn = f"V5_GA1_P{idx:03d}"
        attrs = _v11_attrs_merge()
        _emit_v11_strategy(
            cn,
            doc=f"V5 GA1 trail_pos={tp} offset={off}",
            group="group_a1_trailing",
            name=f"GA1 trail {tp}/{off}",
            params={"trailing_stop_positive": tp, "trailing_stop_positive_offset": off},
            extra_attrs=attrs,
            indicators_code=populate_indicators_v11_standard(),
            entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            trail_pos=tp,
            trail_off=off,
        )


def gen_ga2_stoploss_stair():
    """A2: 7 stoploss x 2 stair = 14."""
    stops = [-0.06, -0.07, -0.08, -0.09, -0.10, -0.12, -0.15]
    idx = 0
    for sl, stair in product(stops, [True, False]):
        idx += 1
        cn = f"V5_GA2_P{idx:03d}"
        attrs = _v11_attrs_merge()
        _emit_v11_strategy(
            cn,
            doc=f"V5 GA2 stoploss={sl} stair={stair}",
            group="group_a2_stoploss",
            name=f"GA2 sl={sl} stair={stair}",
            params={"stoploss": sl, "stair": stair},
            extra_attrs=attrs,
            indicators_code=populate_indicators_v11_standard(),
            entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            stoploss=sl,
            use_stair=stair,
        )


def gen_ga3_tp_big():
    """A3: TP_BIG scan x10."""
    tps = [0.20, 0.25, 0.30, 0.35, 0.40, 0.50, 0.60, 0.80, 1.00, 99.0]
    for i, tp in enumerate(tps, start=1):
        cn = f"V5_GA3_P{i:03d}"
        base = V11_BASE_ATTRS.replace("TP_BIG = 0.40", f"TP_BIG = {tp}")
        _emit_v11_strategy(
            cn,
            doc=f"V5 GA3 TP_BIG={tp}",
            group="group_a3_tp_big",
            name=f"GA3 TP_BIG={tp}",
            params={"TP_BIG": tp},
            extra_attrs=base.rstrip(),
            indicators_code=populate_indicators_v11_standard(),
            entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
        )


def gen_ga4_stair_fine():
    """
    A4: 24 variants — bars1 in [16,18,20,22], loss1 in [-0.04,-0.05,-0.06],
    loss2 = loss1 + 0.02, and bars2 = 2*bars1 OR 2*bars1+4 (second late tier spacing).
    """
    bars1_list = [16, 18, 20, 22]
    loss1_list = [-0.04, -0.05, -0.06]
    idx = 0
    for b1, l1, b2_extra in product(bars1_list, loss1_list, [0, 4]):
        idx += 1
        cn = f"V5_GA4_P{idx:03d}"
        b2 = b1 * 2 + b2_extra
        l2 = round(l1 + 0.02, 4)
        attrs = _v11_attrs_merge()
        _emit_v11_strategy(
            cn,
            doc=f"V5 GA4 stair b1={b1} l1={l1} b2={b2} l2={l2}",
            group="group_a4_stair_fine",
            name=f"GA4 stair {b1}/{l1} {b2}/{l2}",
            params={"bars1": b1, "loss1": l1, "bars2": b2, "loss2": l2, "bars2_extra": b2_extra},
            extra_attrs=attrs,
            indicators_code=populate_indicators_v11_standard(),
            entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            stair_b1=b1,
            stair_l1=l1,
            stair_b2=b2,
            stair_l2=l2,
        )


def gen_ga5_max_bars_timeout():
    """A5: 10×2 网格 + (64,-0.025) 中点，共 21 条。"""
    max_bars_opts = [32, 40, 48, 56, 64, 80, 96, 128, 144, 160]
    thr_opts = [-0.02, -0.03]
    idx = 0
    for mb, th in product(max_bars_opts, thr_opts):
        idx += 1
        cn = f"V5_GA5_P{idx:03d}"
        attrs = V11_BASE_ATTRS.replace("MAX_BARS = 64", f"MAX_BARS = {mb}")
        attrs = attrs.replace("TIMEOUT_LOSS_THRESHOLD = -0.02", f"TIMEOUT_LOSS_THRESHOLD = {th}")
        _emit_v11_strategy(
            cn,
            doc=f"V5 GA5 MAX_BARS={mb} timeout_thr={th}",
            group="group_a5_max_bars",
            name=f"GA5 MAX_BARS={mb} timeout={th}",
            params={"MAX_BARS": mb, "TIMEOUT_LOSS_THRESHOLD": th},
            extra_attrs=attrs.rstrip(),
            indicators_code=populate_indicators_v11_standard(),
            entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
        )
    # Midpoint between -0.02 / -0.03 at baseline MAX_BARS (extra ~200th experiment slot).
    idx += 1
    cn = f"V5_GA5_P{idx:03d}"
    mb, th = 64, -0.025
    attrs = V11_BASE_ATTRS.replace("MAX_BARS = 64", f"MAX_BARS = {mb}")
    attrs = attrs.replace("TIMEOUT_LOSS_THRESHOLD = -0.02", f"TIMEOUT_LOSS_THRESHOLD = {th}")
    _emit_v11_strategy(
        cn,
        doc=f"V5 GA5 MAX_BARS={mb} timeout_thr={th} (mid)",
        group="group_a5_max_bars",
        name=f"GA5 MAX_BARS={mb} timeout={th}",
        params={"MAX_BARS": mb, "TIMEOUT_LOSS_THRESHOLD": th, "note": "timeout_mid"},
        extra_attrs=attrs.rstrip(),
        indicators_code=populate_indicators_v11_standard(),
        entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
    )


# =============================================================================
# Group B — MACD robustness
# =============================================================================
def _macd_combos_for_b1() -> List[Tuple[int, int, int]]:
    """All (fast, slow, signal) with fast < slow - 4; typically 51 combos."""
    fasts = [6, 8, 10, 12, 14]
    slows = [15, 17, 21, 26]
    sigs = [5, 7, 9]
    combos: List[Tuple[int, int, int]] = []
    for s in slows:
        for f in fasts:
            if f >= s - 4:
                continue
            for sig in sigs:
                combos.append((s, f, sig))
    combos.sort(key=lambda x: (x[1], x[0], x[2]))
    return [(f, s, sig) for s, f, sig in combos]


def gen_gb1_macd_grid():
    for i, (mf, ms, msig) in enumerate(_macd_combos_for_b1(), start=1):
        cn = f"V5_GB1_P{i:03d}"
        attrs = V11_BASE_ATTRS.replace("MACD_FAST = 8", f"MACD_FAST = {mf}")
        attrs = attrs.replace("MACD_SLOW = 17", f"MACD_SLOW = {ms}")
        attrs = attrs.replace("MACD_SIGNAL = 9", f"MACD_SIGNAL = {msig}")
        _emit_v11_strategy(
            cn,
            doc=f"V5 GB1 MACD {mf},{ms},{msig}",
            group="group_b1_macd_grid",
            name=f"GB1 MACD {mf}/{ms}/{msig}",
            params={"MACD_FAST": mf, "MACD_SLOW": ms, "MACD_SIGNAL": msig},
            extra_attrs=attrs.rstrip(),
            indicators_code=populate_indicators_v11_standard(),
            entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
        )


def gen_gb2_macd_modes():
    """B2: (8,17,9) and (12,26,9) x 6 modes = 12."""
    macd_sets = [(8, 17, 9), (12, 26, 9)]
    idx = 0
    for mf, ms, msig in macd_sets:
        for mode_name, expr in MACD_ENTRY_MODES.items():
            idx += 1
            cn = f"V5_GB2_P{idx:03d}"
            attrs = V11_BASE_ATTRS.replace("MACD_FAST = 8", f"MACD_FAST = {mf}")
            attrs = attrs.replace("MACD_SLOW = 17", f"MACD_SLOW = {ms}")
            attrs = attrs.replace("MACD_SIGNAL = 9", f"MACD_SIGNAL = {msig}")
            _emit_v11_strategy(
                cn,
                doc=f"V5 GB2 MACD {mf},{ms},{msig} mode={mode_name}",
                group="group_b2_macd_modes",
                name=f"GB2 {mf}/{ms}/{msig} {mode_name}",
                params={"MACD": [mf, ms, msig], "mode": mode_name},
                extra_attrs=attrs.rstrip(),
                indicators_code=populate_indicators_v11_standard(),
                entry_code=populate_entry_trend_long(expr),
            )


def gen_gb3_alternatives():
    """B3: EMA slope x4, Stoch x2, dual x2 = 8."""
    idx = 0
    for period, th in product([5, 8], [0.001, 0.002]):
        idx += 1
        cn = f"V5_GB3_P{idx:03d}"
        extra = f"""
        prev = dataframe['ema21'].shift({period})
        dataframe['ema21_slope'] = (dataframe['ema21'] - prev) / prev.replace(0, np.nan)
"""
        ind = populate_indicators_v11_standard(prefix_extra=extra)
        attrs_extra = f"    EMA_SLOPE_PERIOD = {period}\n    EMA_SLOPE_THRESHOLD = {th}\n"
        # Re-build with attrs on class — need threshold as self
        full_attrs = _v11_attrs_merge(attrs_extra)
        code = (
            HEADER.format(doc=f"V5 GB3 EMA slope p={period} th={th}")
            + build_class_open(cn, True, extra_class_attrs=full_attrs)
            + ind
            + populate_entry_trend_long("(dataframe['ema21_slope'] > self.EMA_SLOPE_THRESHOLD)")
            + populate_exit_trend_empty()
            + custom_exit_block(True, False)
            + FOOTER_CONFIRM
        )
        save_strategy(
            cn,
            code,
            f"GB3 EMA slope p={period} th={th}",
            "group_b3_alternatives",
            {"type": "ema_slope", "period": period, "threshold": th},
        )

    for k in (14, 21):
        idx += 1
        cn = f"V5_GB3_P{idx:03d}"
        attrs = _v11_attrs_merge(f"    STOCH_K = {k}\n    STOCH_D = 3\n    STOCH_TH = 60\n")
        extra = f"""
        st = ta.STOCH(dataframe, fastk_period=self.STOCH_K, slowk_period=3, slowd_period=self.STOCH_D)
        dataframe['slowk'] = st['slowk']
        dataframe['slowd'] = st['slowd']
"""
        ind = populate_indicators_v11_standard(prefix_extra=extra)
        code = (
            HEADER.format(doc=f"V5 GB3 Stoch K={k}")
            + build_class_open(cn, True, extra_class_attrs=attrs)
            + ind
            + populate_entry_trend_long("(dataframe['slowk'] > self.STOCH_TH)")
            + populate_exit_trend_empty()
            + custom_exit_block(True, False)
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"GB3 Stoch K={k}", "group_b3_alternatives", {"type": "stoch", "K": k, "D": 3, "th": 60})

    dual_expr = (
        "(dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1)) "
        "& (dataframe['slowk'] > 60)"
    )
    for k in (14, 21):
        idx += 1
        cn = f"V5_GB3_P{idx:03d}"
        attrs = _v11_attrs_merge(f"    STOCH_K = {k}\n    STOCH_D = 3\n")
        extra = f"""
        st = ta.STOCH(dataframe, fastk_period=self.STOCH_K, slowk_period=3, slowd_period=self.STOCH_D)
        dataframe['slowk'] = st['slowk']
        dataframe['slowd'] = st['slowd']
"""
        ind = populate_indicators_v11_standard(prefix_extra=extra)
        code = (
            HEADER.format(doc=f"V5 GB3 dual MACD+Stoch K={k}")
            + build_class_open(cn, True, extra_class_attrs=attrs)
            + ind
            + populate_entry_trend_long(dual_expr)
            + populate_exit_trend_empty()
            + custom_exit_block(True, False)
            + FOOTER_CONFIRM
        )
        save_strategy(
            cn,
            code,
            f"GB3 dual MACD+Stoch K={k}",
            "group_b3_alternatives",
            {"type": "dual_macd_stoch", "K": k},
        )


# =============================================================================
# Group C — DC period fine search
# =============================================================================
def gen_gc_dc_grid():
    shorts = [10, 12, 14, 16, 18]
    longs = [30, 35, 40, 45]
    idx = 0
    # Extend base 18-tuple grid to exactly 20: DC_SHORT=20 with longer legs (>=35).
    extra_pairs = [(20, 40), (20, 45)]
    seen: set[Tuple[int, int]] = set()
    pairs: List[Tuple[int, int]] = []
    for ds, dl in product(shorts, longs):
        if dl - ds < 15:
            continue
        pairs.append((ds, dl))
        seen.add((ds, dl))
    for ep in extra_pairs:
        if ep not in seen:
            pairs.append(ep)
            seen.add(ep)
    for ds, dl in pairs:
        idx += 1
        cn = f"V5_GC_P{idx:03d}"
        attrs = V11_BASE_ATTRS.replace("DC_SHORT = 14", f"DC_SHORT = {ds}")
        attrs = attrs.replace("DC_LONG = 40", f"DC_LONG = {dl}")
        _emit_v11_strategy(
            cn,
            doc=f"V5 GC DC short={ds} long={dl}",
            group="group_c_dc_grid",
            name=f"GC DC {ds}/{dl}",
            params={"DC_SHORT": ds, "DC_LONG": dl},
            extra_attrs=attrs.rstrip(),
            indicators_code=populate_indicators_v11_standard(),
            entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
        )


# =============================================================================
# Group D — Controls & ablations
# =============================================================================
def gen_gd_controls():
    # D1: CryptoV11 baseline
    cn = "V5_GD1_P001"
    _emit_v11_strategy(
        cn,
        doc="V5 GD1 CryptoV11 baseline",
        group="group_d1_baseline_v11",
        name="GD1 CryptoV11 baseline",
        params={"variant": "v11_baseline"},
        extra_attrs=_v11_attrs_merge(),
        indicators_code=populate_indicators_v11_standard(),
        entry_code=populate_entry_trend_long(ENTRY_MACD_V11_BASE),
    )

    # D2: CryptoV10 baseline — fixed DC 20, no MACD
    cn = "V5_GD2_P001"
    attrs = """    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    TIMEOUT_LOSS_THRESHOLD = -0.02
"""
    code = (
        HEADER.format(doc="V5 GD2 CryptoV10 baseline (fixed DC20, no MACD)")
        + build_class_open(cn, True, extra_class_attrs=attrs)
        + populate_indicators_v10_fixed_dc()
        + populate_entry_trend_long("(True)")
        + populate_exit_trend_empty()
        + custom_exit_block(True, False)
        + FOOTER_CONFIRM
    )
    save_strategy(cn, code, "GD2 CryptoV10 baseline", "group_d2_baseline_v10", {"variant": "v10_baseline"})

    # D3 ablations (8)
    ablations = [
        (
            "no_g6",
            "No G6 fixed DC20 + MACD",
            populate_indicators_fixed_dc_with_macd(),
            populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            """    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    TIMEOUT_LOSS_THRESHOLD = -0.02
    MACD_FAST = 8
    MACD_SLOW = 17
    MACD_SIGNAL = 9
""",
        ),
        (
            "no_g2",
            "No G2 MACD filter",
            populate_indicators_v11_standard(),
            populate_entry_trend_long("(True)"),
            _v11_attrs_merge(),
        ),
        (
            "no_stair",
            "No stair S5",
            populate_indicators_v11_standard(),
            populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            _v11_attrs_merge(),
        ),
        (
            "no_cooldown",
            "COOLDOWN_BARS=0",
            populate_indicators_v11_standard(),
            populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            _v11_attrs_merge("    COOLDOWN_BARS = 0\n"),
        ),
        (
            "no_daily_max",
            "DAILY_MAX_LOSSES=999",
            populate_indicators_v11_standard(),
            populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            _v11_attrs_merge("    DAILY_MAX_LOSSES = 999\n"),
        ),
        (
            "no_atr_filter",
            "ATR_MULT=0",
            populate_indicators_v11_standard(),
            populate_entry_trend_long(ENTRY_MACD_V11_BASE),
            _v11_attrs_merge("    ATR_MULT = 0.0\n"),
        ),
        (
            "no_4h_ema",
            "No 4H EMA confirm",
            populate_indicators_v11_standard(),
            populate_entry_trend_long(ENTRY_MACD_V11_BASE, use_4h_ema=False),
            _v11_attrs_merge(),
        ),
        (
            "no_adx_rising",
            "No ADX rising",
            populate_indicators_v11_standard(),
            populate_entry_trend_long(ENTRY_MACD_V11_BASE, use_adx_rising=False),
            _v11_attrs_merge(),
        ),
    ]

    for i, (key, title, ind, ent, ats) in enumerate(ablations, start=1):
        cn = f"V5_GD3_P{i:03d}"
        use_stair = key != "no_stair"
        code = (
            HEADER.format(doc=f"V5 GD3 ablation {key}")
            + build_class_open(cn, True, extra_class_attrs=ats.rstrip() + "\n")
            + ind
            + ent
            + populate_exit_trend_empty()
            + custom_exit_block(use_stair, False)
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"GD3 {title}", "group_d3_ablation", {"ablation": key})


def main():
    global experiments, _existing_classnames
    experiments = []
    _existing_classnames = set()

    gen_ga1_trailing_grid()
    gen_ga2_stoploss_stair()
    gen_ga3_tp_big()
    gen_ga4_stair_fine()
    gen_ga5_max_bars_timeout()
    gen_gb1_macd_grid()
    gen_gb2_macd_modes()
    gen_gb3_alternatives()
    gen_gc_dc_grid()
    gen_gd_controls()

    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(experiments, f, indent=2, ensure_ascii=False)
        f.write("\n")

    total = len(experiments)
    print(f"Total experiments: {total}")
    groups = sorted({e["group"] for e in experiments})
    for g in groups:
        c = len([e for e in experiments if e["group"] == g])
        print(f"  {g}: {c}")
    print(f"Manifest: {MANIFEST_PATH}")
    print(f"Strategies: {EXPERIMENT_DIR}")


if __name__ == "__main__":
    main()
