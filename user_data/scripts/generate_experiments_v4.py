# -*- coding: utf-8 -*-
"""
V4 Experiment Generator — CryptoV10 基线（TrailPos=0.03, ATR_MULT=0.6, S5 阶梯止损）
生成约 280 个独立策略文件 + experiment_manifest_v4.json + GROUP7 单品种配置。
"""
from __future__ import annotations

import copy
import json
import os
from typing import Any, Dict, List, Tuple

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA = os.path.dirname(SCRIPT_DIR)
STRATEGY_DIR = os.path.join(USER_DATA, "strategies")
EXPERIMENT_DIR = os.path.join(STRATEGY_DIR, "experiments_v4")
CONFIG_DIR = os.path.join(USER_DATA, "configs_v4")
CONFIG_BACKTEST = os.path.join(USER_DATA, "config_backtest.json")
MANIFEST_PATH = os.path.join(USER_DATA, "experiment_manifest_v4.json")

os.makedirs(EXPERIMENT_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)

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
# Core template fragments (baseline CryptoV10-style)
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
    extra_class_attrs: str = "",
    informative_4h: bool = True,
    informative_1h: bool = False,
) -> str:
    ts = "True" if trailing_stop else "False"
    lines = [
        f"class {classname}(IStrategy):",
        "    INTERFACE_VERSION = 3",
        "    timeframe = '15m'",
        "    can_short = True",
        "    startup_candle_count = 400",
        "    stoploss = -0.10",
        "    use_custom_stoploss = False",
        f"    trailing_stop = {ts}",
        "    trailing_stop_positive = 0.03",
        "    trailing_stop_positive_offset = 0.30",
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
    if informative_1h:
        lines.extend(
            [
                "    @informative('1h')",
                "    def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:",
                "        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)",
                "        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)",
                "        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)",
                "        return dataframe",
                "",
            ]
        )
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


def baseline_populate_indicators(dc_expr: str = "self.DC_PERIOD") -> str:
    return f'''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling({dc_expr}).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        return dataframe
'''.replace("{dc_expr}", dc_expr)


def baseline_entry_long(extra_and_block: str) -> str:
    """extra_and_block: expression combined with & inside long_conditions."""
    return f'''
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            ({extra_and_block})
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
    use_dc_exit: bool,
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
        if bars_held >= self.MAX_BARS and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
'''


# =============================================================================
# GROUP 1: 双 Donchian 退出
# =============================================================================
def gen_group1():
    periods = [5, 7, 10, 12, 15]
    modes = [
        ("dc_only", False, True, False),
        ("dc_trail", True, True, False),
        ("dc_trail_stair", True, True, True),
    ]
    min_bars_opts = [0, 8]
    idx = 0
    for p in periods:
        for mode, trail, dc_on, stair in modes:
            for mb in min_bars_opts:
                idx += 1
                cn = f"V4_G1_P{idx:03d}"
                attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    DC_EXIT_PERIOD = {p}
    DC_EXIT_MIN_BARS = {mb}
"""
                ind = f'''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(self.DC_PERIOD).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['dc_lower_exit'] = dataframe['low'].rolling(self.DC_EXIT_PERIOD).min().shift(1)
        return dataframe
'''
                entry = baseline_entry_long("True")
                code = (
                    HEADER.format(doc=f"V4 G1 DC exit p={p} mode={mode} mb={mb}")
                    + build_class_open(cn, trailing_stop=trail, extra_class_attrs=attrs)
                    + ind
                    + entry
                    + populate_exit_trend_empty()
                    + custom_exit_block(
                        use_stair=stair,
                        use_dc_exit=dc_on,
                        dc_min_bars=mb,
                    )
                    + FOOTER_CONFIRM
                )
                save_strategy(
                    cn,
                    code,
                    f"G1 DCexit p={p} {mode} mb={mb}",
                    "group1_dc_exit",
                    {"dc_exit_period": p, "mode": mode, "dc_exit_min_bars": mb, "trailing": trail, "stair": stair},
                )


# =============================================================================
# GROUP 2: MACD 共振
# =============================================================================
MACD_MODES_CODE = {
    "hist_pos": "(_macd['macdhist'] > 0)",
    "hist_rise": "((_macd['macdhist'] > 0) & (_macd['macdhist'] > _macd['macdhist'].shift(1)))",
    "macd_pos": "(_macd['macd'] > 0)",
    "macd_sig_hist": "((_macd['macd'] > _macd['macdsignal']) & (_macd['macdhist'] > 0))",
}


def gen_group2():
    macds = [(8, 21, 5), (12, 26, 9), (8, 17, 9)]
    modes = list(MACD_MODES_CODE.keys())
    idx = 0
    for fast, slow, sig in macds:
        for mname in modes:
            for use_stair in (True, False):
                idx += 1
                cn = f"V4_G2_P{idx:03d}"
                expr = MACD_MODES_CODE[mname]
                entry_extra = "(" + expr.replace("_macd", "dataframe") + ")"
                attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    MACD_FAST = {fast}
    MACD_SLOW = {slow}
    MACD_SIGNAL = {sig}
"""
                ind = f'''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(self.DC_PERIOD).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        _macd = ta.MACD(dataframe, fastperiod=self.MACD_FAST, slowperiod=self.MACD_SLOW, signalperiod=self.MACD_SIGNAL)
        dataframe['macd'] = _macd['macd']
        dataframe['macdsignal'] = _macd['macdsignal']
        dataframe['macdhist'] = _macd['macdhist']
        return dataframe
'''
                entry = baseline_entry_long(entry_extra)
                code = (
                    HEADER.format(doc=f"V4 G2 MACD {fast},{slow},{sig} {mname} stair={use_stair}")
                    + build_class_open(cn, trailing_stop=True, extra_class_attrs=attrs)
                    + ind
                    + entry
                    + populate_exit_trend_empty()
                    + custom_exit_block(use_stair=use_stair, use_dc_exit=False)
                    + FOOTER_CONFIRM
                )
                save_strategy(
                    cn,
                    code,
                    f"G2 MACD f{fast}s{slow}sig{sig} {mname} stair={use_stair}",
                    "group2_macd",
                    {"macd": [fast, slow, sig], "mode": mname, "stair": use_stair},
                )


# =============================================================================
# GROUP 3: EMA21 斜率
# =============================================================================
def gen_group3():
    slopes = [3, 5, 8]
    th_all = [0.0005, 0.001, 0.002, 0.003]
    idx = 0
    for sp in slopes:
        for th in th_all:
            if th in (0.001, 0.002):
                stair_opts = (True, False)
            else:
                stair_opts = (True,)
            for use_stair in stair_opts:
                idx += 1
                cn = f"V4_G3_P{idx:03d}"
                attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    EMA_SLOPE_PERIOD = {sp}
    EMA_SLOPE_THRESHOLD = {th}
"""
                ind = f'''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(self.DC_PERIOD).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        prev = dataframe['ema21'].shift(self.EMA_SLOPE_PERIOD)
        dataframe['ema21_slope'] = (dataframe['ema21'] - prev) / prev.replace(0, np.nan)
        return dataframe
'''
                entry = baseline_entry_long("(dataframe['ema21_slope'] > self.EMA_SLOPE_THRESHOLD)")
                code = (
                    HEADER.format(doc=f"V4 G3 EMA slope sp={sp} th={th} stair={use_stair}")
                    + build_class_open(cn, True, attrs)
                    + ind
                    + entry
                    + populate_exit_trend_empty()
                    + custom_exit_block(use_stair=use_stair, use_dc_exit=False)
                    + FOOTER_CONFIRM
                )
                save_strategy(
                    cn,
                    code,
                    f"G3 EMA slope p={sp} th={th} stair={use_stair}",
                    "group3_ema_slope",
                    {"slope_period": sp, "threshold": th, "stair": use_stair},
                )


# =============================================================================
# GROUP 4: 1H 确认框架
# =============================================================================
def gen_group4():
    modes = [
        ("1h_only", "(dataframe['ema21_1h'] > dataframe['ema55_1h'])"),
        ("1h_and_4h", "((dataframe['ema21_1h'] > dataframe['ema55_1h']) & (dataframe['ema21_4h'] > dataframe['ema55_4h']))"),
        ("1h_or_4h", "((dataframe['ema21_1h'] > dataframe['ema55_1h']) | (dataframe['ema21_4h'] > dataframe['ema55_4h']))"),
    ]
    adxs = [0, 25, 30]
    idx = 0
    for mname, ema_expr in modes:
        for adx_min in adxs:
            for use_stair in (True, False):
                idx += 1
                cn = f"V4_G4_P{idx:03d}"
                attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    H1_ADX_MIN = {adx_min}
"""
                if adx_min > 0:
                    extra = f"({ema_expr} & (dataframe['adx_1h'] > self.H1_ADX_MIN))"
                else:
                    extra = f"({ema_expr})"
                ind = baseline_populate_indicators()
                entry2 = f'''
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            ({extra})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
'''
                code = (
                    HEADER.format(doc=f"V4 G4 1H {mname} adx>{adx_min} stair={use_stair}")
                    + build_class_open(cn, True, attrs, informative_1h=True)
                    + ind
                    + entry2
                    + populate_exit_trend_empty()
                    + custom_exit_block(use_stair=use_stair, use_dc_exit=False)
                    + FOOTER_CONFIRM
                )
                save_strategy(
                    cn,
                    code,
                    f"G4 1H {mname} adx1h>{adx_min} stair={use_stair}",
                    "group4_1h_confirm",
                    {"mode": mname, "h1_adx_min": adx_min, "stair": use_stair},
                )


# =============================================================================
# GROUP 5: 利润回吐（无状态近似）
# =============================================================================
def gen_group5():
    mins = [0.05, 0.08, 0.10, 0.15, 0.20]
    keeps = [0.3, 0.5, 0.7]
    idx = 0
    for mp in mins:
        for kr in keeps:
            idx += 1
            cn = f"V4_G5_P{idx:03d}"
            use_stair = True
            attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    MIN_PROFIT = {mp}
    KEEP_RATIO = {kr}
"""
            ind = baseline_populate_indicators()
            entry = baseline_entry_long("True")
            code = (
                HEADER.format(doc=f"V4 G5 giveback mp={mp} kr={kr} stair={use_stair}")
                + build_class_open(cn, True, attrs)
                + ind
                + entry
                + populate_exit_trend_empty()
                + custom_exit_block(use_stair=use_stair, use_dc_exit=False, profit_giveback=True)
                + FOOTER_CONFIRM
            )
            save_strategy(
                cn,
                code,
                f"G5 giveback mp={mp} kr={kr} stair={use_stair}",
                "group5_profit_giveback",
                {"min_profit": mp, "keep_ratio": kr, "stair": use_stair},
            )
    for mp in mins:
        for kr in (0.5, 0.7):
            idx += 1
            cn = f"V4_G5_P{idx:03d}"
            use_stair = False
            attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    MIN_PROFIT = {mp}
    KEEP_RATIO = {kr}
"""
            ind = baseline_populate_indicators()
            entry = baseline_entry_long("True")
            code = (
                HEADER.format(doc=f"V4 G5 giveback mp={mp} kr={kr} stair={use_stair}")
                + build_class_open(cn, True, attrs)
                + ind
                + entry
                + populate_exit_trend_empty()
                + custom_exit_block(use_stair=use_stair, use_dc_exit=False, profit_giveback=True)
                + FOOTER_CONFIRM
            )
            save_strategy(
                cn,
                code,
                f"G5 giveback mp={mp} kr={kr} stair={use_stair}",
                "group5_profit_giveback",
                {"min_profit": mp, "keep_ratio": kr, "stair": use_stair},
            )


# =============================================================================
# GROUP 6: 动态 Donchian（约 20 组）
# =============================================================================
G6_COMBOS: List[Tuple[int, int, int, float]] = [
    (50, 14, 25, 0.3),
    (50, 14, 40, 0.5),
    (50, 16, 40, 0.7),
    (100, 14, 30, 0.3),
    (100, 16, 35, 0.5),
    (100, 14, 30, 0.5),
    (50, 16, 25, 0.7),
    (100, 16, 40, 0.3),
    (50, 14, 25, 0.3),
    (100, 14, 40, 0.7),
    (50, 14, 40, 0.3),
    (100, 16, 30, 0.5),
    (50, 14, 30, 0.5),
    (100, 14, 40, 0.3),
    (50, 16, 35, 0.5),
    (100, 14, 30, 0.5),
    (50, 16, 40, 0.7),
    (100, 16, 30, 0.7),
    (50, 16, 35, 0.3),
    (100, 14, 25, 0.7),
]


def gen_group6():
    for i, (lb, ds, dlong, th) in enumerate(G6_COMBOS, start=1):
        cn = f"V4_G6_P{i:03d}"
        attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    ATR_LOOKBACK = {lb}
    DC_SHORT = {ds}
    DC_LONG = {dlong}
    ATR_PCT_THRESHOLD = {th}
"""
        ind = f'''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        atr_pct = dataframe['atr'].rolling(self.ATR_LOOKBACK).apply(
            lambda x: float(DataFrame(x).rank(pct=True).iloc[-1]) if len(x) == self.ATR_LOOKBACK else np.nan,
            raw=False,
        )
        use_short = atr_pct < self.ATR_PCT_THRESHOLD
        dc_s = dataframe['high'].rolling(self.DC_SHORT).max().shift(1)
        dc_l = dataframe['high'].rolling(self.DC_LONG).max().shift(1)
        dataframe['dc_upper'] = np.where(use_short, dc_s, dc_l)
        return dataframe
'''
        entry = baseline_entry_long("True")
        code = (
            HEADER.format(doc=f"V4 G6 dynamic DC lb={lb} short={ds} long={dlong} th={th}")
            + build_class_open(cn, True, attrs)
            + ind
            + entry
            + populate_exit_trend_empty()
            + custom_exit_block(use_stair=True, use_dc_exit=False)
            + FOOTER_CONFIRM
        )
        save_strategy(
            cn,
            code,
            f"G6 dynDC lb={lb} s={ds} L={dlong} th={th}",
            "group6_dynamic_dc",
            {"lookback": lb, "dc_short": ds, "dc_long": dlong, "atr_pct_threshold": th},
        )


# =============================================================================
# GROUP 7: 品种差异化 + 配置文件
# =============================================================================
PAIRS_FUT = [
    "BTC/USDT:USDT",
    "ETH/USDT:USDT",
    "SOL/USDT:USDT",
    "ADA/USDT:USDT",
]
PARAM_GROUPS = [
    (26, 0.5, 20),
    (28, 0.6, 20),
    (30, 0.7, 20),
    (28, 0.5, 14),
    (28, 0.6, 14),
    (28, 0.8, 20),
    (26, 0.6, 25),
    (30, 0.6, 25),
]


def gen_group7():
    with open(CONFIG_BACKTEST, "r", encoding="utf-8") as f:
        base_cfg = json.load(f)
    idx = 0
    for pair in PAIRS_FUT:
        sym = pair.split("/")[0].lower()
        for gi, (adx, atrm, dc) in enumerate(PARAM_GROUPS, start=1):
            idx += 1
            cn = f"V4_G7_{sym.upper()}_PG{gi:02d}"
            cfg_name = f"v4_g7_{sym}_pg{gi:02d}.json"
            cfg_path = os.path.join(CONFIG_DIR, cfg_name)
            cfg = copy.deepcopy(base_cfg)
            cfg["exchange"]["pair_whitelist"] = [pair]
            with open(cfg_path, "w", encoding="utf-8") as f:
                json.dump(cfg, f, indent=4, ensure_ascii=False)
                f.write("\n")
            rel_config = os.path.join("user_data", "configs_v4", cfg_name).replace("\\", "/")
            attrs = f"""    ADX_MIN = {adx}
    ATR_MULT = {atrm}
    DC_PERIOD = {dc}
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
"""
            ind = baseline_populate_indicators()
            entry = baseline_entry_long("True")
            code = (
                HEADER.format(doc=f"V4 G7 {pair} ADX={adx} ATR={atrm} DC={dc}")
                + build_class_open(cn, True, attrs)
                + ind
                + entry
                + populate_exit_trend_empty()
                + custom_exit_block(use_stair=True, use_dc_exit=False)
                + FOOTER_CONFIRM
            )
            save_strategy(
                cn,
                code,
                f"G7 {pair} ADX={adx} ATR={atrm} DC={dc}",
                "group7_per_pair_params",
                {"pair": pair, "adx": adx, "atr_mult": atrm, "dc_period": dc, "param_group": gi},
                config=rel_config,
            )


# =============================================================================
# GROUP 8: 阶梯止损精细搜索（约 36）
# =============================================================================
G8_COMBOS: List[Tuple[int, float, int, float]] = [
    (16, -0.05, 36, -0.03),
    (16, -0.05, 40, -0.04),
    (16, -0.05, 44, -0.05),
    (16, -0.06, 36, -0.03),
    (16, -0.06, 40, -0.04),
    (16, -0.06, 48, -0.05),
    (16, -0.07, 40, -0.03),
    (16, -0.07, 44, -0.04),
    (18, -0.05, 36, -0.03),
    (18, -0.05, 40, -0.05),
    (18, -0.06, 36, -0.04),
    (18, -0.06, 44, -0.03),
    (18, -0.07, 40, -0.04),
    (18, -0.07, 48, -0.05),
    (20, -0.05, 36, -0.03),
    (20, -0.05, 40, -0.04),
    (20, -0.05, 48, -0.05),
    (20, -0.06, 36, -0.03),
    (20, -0.06, 40, -0.04),
    (20, -0.06, 44, -0.05),
    (20, -0.07, 36, -0.04),
    (20, -0.07, 40, -0.05),
    (20, -0.07, 48, -0.03),
    (22, -0.05, 40, -0.03),
    (22, -0.05, 44, -0.04),
    (22, -0.06, 36, -0.05),
    (22, -0.06, 40, -0.03),
    (22, -0.06, 48, -0.04),
    (22, -0.07, 36, -0.03),
    (22, -0.07, 40, -0.05),
    (24, -0.05, 36, -0.04),
    (24, -0.05, 44, -0.03),
    (24, -0.06, 40, -0.05),
    (24, -0.06, 48, -0.03),
    (24, -0.07, 36, -0.04),
    (24, -0.07, 40, -0.03),
]


def gen_group8():
    for i, (b1, l1, b2, l2) in enumerate(G8_COMBOS, start=1):
        cn = f"V4_G8_P{i:03d}"
        attrs = """    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
"""
        ind = baseline_populate_indicators()
        entry = baseline_entry_long("True")
        code = (
            HEADER.format(doc=f"V4 G8 stair b1={b1} l1={l1} b2={b2} l2={l2}")
            + build_class_open(cn, True, attrs)
            + ind
            + entry
            + populate_exit_trend_empty()
            + custom_exit_block(True, False, stair_b1=b1, stair_l1=l1, stair_b2=b2, stair_l2=l2)
            + FOOTER_CONFIRM
        )
        save_strategy(
            cn,
            code,
            f"G8 stair {b1}b/{l1} {b2}b/{l2}",
            "group8_stair_grid",
            {"bars1": b1, "loss1": l1, "bars2": b2, "loss2": l2},
        )


# =============================================================================
# GROUP 9: 入场时间过滤（UTC）
# =============================================================================
def gen_group9():
    excludes = [(0, 4), (4, 8), (8, 12), (12, 16), (16, 20), (20, 24)]
    allows = [("allow_8_20", 8, 20), ("allow_12_24", 12, 24), ("allow_0_12", 0, 12)]
    hybrids = [
        ("ex0_4_allow8_20", [(0, 4)], (8, 20)),
        ("ex20_24_allow12_24", [(20, 24)], (12, 24)),
        ("ex8_12_allow0_12", [(8, 12)], (0, 12)),
    ]
    idx = 0

    def hour_filter_code(mode: str, ex: list, alo: tuple | None) -> str:
        if mode == "exclude":
            lo, hi = ex[0]
            return f"(~dataframe['hour'].between({lo}, {hi - 1}, inclusive='both'))"
        if mode == "allow":
            _, lo, hi = alo  # type: ignore
            if hi == 24:
                return f"(dataframe['hour'] >= {lo})"
            return f"(dataframe['hour'].between({lo}, {hi - 1}, inclusive='both'))"
        if mode == "hybrid":
            parts = []
            for lo, hi in ex:
                parts.append(f"(~dataframe['hour'].between({lo}, {hi - 1}, inclusive='both'))")
            al, ah = alo  # type: ignore
            if ah == 24:
                parts.append(f"(dataframe['hour'] >= {al})")
            else:
                parts.append(f"(dataframe['hour'].between({al}, {ah - 1}, inclusive='both'))")
            return "(" + " & ".join(parts) + ")"
        raise ValueError(mode)

    for lo, hi in excludes:
        for use_stair in (True, False):
            idx += 1
            cn = f"V4_G9_P{idx:03d}"
            hf = hour_filter_code("exclude", [(lo, hi)], None)
            attrs = """    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
"""
            ind = (
                baseline_populate_indicators().rstrip()
                + """
        dataframe['hour'] = dataframe['date'].dt.hour
        return dataframe
"""
            )
            entry = baseline_entry_long(hf)
            code = (
                HEADER.format(doc=f"V4 G9 exclude UTC [{lo},{hi}) stair={use_stair}")
                + build_class_open(cn, True, attrs)
                + ind
                + entry
                + populate_exit_trend_empty()
                + custom_exit_block(use_stair, False)
                + FOOTER_CONFIRM
            )
            save_strategy(
                cn,
                code,
                f"G9 exclude [{lo},{hi}) UTC stair={use_stair}",
                "group9_hour_filter",
                {"exclude": [lo, hi], "stair": use_stair},
            )

    for aname, alo, ahi in allows:
        for use_stair in (True, False):
            idx += 1
            cn = f"V4_G9_P{idx:03d}"
            hf = hour_filter_code("allow", [], (aname, alo, ahi))
            ind = (
                baseline_populate_indicators().rstrip()
                + """
        dataframe['hour'] = dataframe['date'].dt.hour
        return dataframe
"""
            )
            entry = baseline_entry_long(hf)
            attrs = """    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
"""
            code = (
                HEADER.format(doc=f"V4 G9 {aname} stair={use_stair}")
                + build_class_open(cn, True, attrs)
                + ind
                + entry
                + populate_exit_trend_empty()
                + custom_exit_block(use_stair, False)
                + FOOTER_CONFIRM
            )
            save_strategy(
                cn,
                code,
                f"G9 {aname} stair={use_stair}",
                "group9_hour_filter",
                {"allow": [alo, ahi], "stair": use_stair},
            )

    for hname, exlist, al in hybrids:
        for use_stair in (True, False):
            idx += 1
            cn = f"V4_G9_P{idx:03d}"
            hf = hour_filter_code("hybrid", exlist, al)
            ind = (
                baseline_populate_indicators().rstrip()
                + """
        dataframe['hour'] = dataframe['date'].dt.hour
        return dataframe
"""
            )
            entry = baseline_entry_long(hf)
            attrs = """    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
"""
            code = (
                HEADER.format(doc=f"V4 G9 hybrid {hname} stair={use_stair}")
                + build_class_open(cn, True, attrs)
                + ind
                + entry
                + populate_exit_trend_empty()
                + custom_exit_block(use_stair, False)
                + FOOTER_CONFIRM
            )
            save_strategy(
                cn,
                code,
                f"G9 hybrid {hname} stair={use_stair}",
                "group9_hour_filter",
                {"hybrid": hname, "stair": use_stair},
            )


# =============================================================================
# GROUP 10: Stochastic
# =============================================================================
def gen_group10():
    ks = [9, 14, 21]
    ds = [3, 5]
    ths = [60, 80]
    idx = 0
    for k in ks:
        for d in ds:
            for th in ths:
                for use_stair in (True, False):
                    idx += 1
                    cn = f"V4_G10_P{idx:03d}"
                    attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    STOCH_K = {k}
    STOCH_D = {d}
    STOCH_TH = {th}
"""
                    ind = f'''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(self.DC_PERIOD).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        st = ta.STOCH(dataframe, fastk_period=self.STOCH_K, slowk_period=3, slowd_period=self.STOCH_D)
        dataframe['slowk'] = st['slowk']
        dataframe['slowd'] = st['slowd']
        return dataframe
'''
                    entry = baseline_entry_long("(dataframe['slowk'] > self.STOCH_TH)")
                    code = (
                        HEADER.format(doc=f"V4 G10 Stoch K={k} D={d} th={th} stair={use_stair}")
                        + build_class_open(cn, True, attrs)
                        + ind
                        + entry
                        + populate_exit_trend_empty()
                        + custom_exit_block(use_stair, False)
                        + FOOTER_CONFIRM
                    )
                    save_strategy(
                        cn,
                        code,
                        f"G10 Stoch K={k} D={d} th>{th} stair={use_stair}",
                        "group10_stoch",
                        {"stoch_k": k, "stoch_d": d, "threshold": th, "stair": use_stair},
                    )


# =============================================================================
# GROUP 11: 趋势强度复合评分
# =============================================================================
WEIGHT_SCHEMES = {
    "equal": (1, 1, 1, 1),
    "w_adx2": (2, 1, 1, 1),
    "w_atr2": (1, 1, 2, 1),
    "w_di2": (1, 2, 1, 1),
    "w_slope2": (1, 1, 1, 2),
}


def gen_group11():
    thresholds = [0.6, 0.8, 1.0]
    idx = 0
    for th in thresholds:
        for wname, ws in WEIGHT_SCHEMES.items():
            for use_stair in (True, False):
                idx += 1
                wa, wd, wt, wsl = ws
                cn = f"V4_G11_P{idx:03d}"
                attrs = f"""    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    SCORE_THRESHOLD = {th}
    W_ADX = {wa}
    W_DI = {wd}
    W_ATR = {wt}
    W_SLOPE = {wsl}
    EMA_SLOPE_BARS = 5
"""
                ind = f'''
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['dc_upper'] = dataframe['high'].rolling(self.DC_PERIOD).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        di_diff = dataframe['plus_di'] - dataframe['minus_di']
        atr_break = (dataframe['close'] - dataframe['dc_upper'])
        prev = dataframe['ema21'].shift(self.EMA_SLOPE_BARS)
        ema_slope = (dataframe['ema21'] - prev) / prev.replace(0, np.nan)
        dataframe['trend_score'] = (
            self.W_ADX * (dataframe['adx'] / 50.0)
            + self.W_DI * (di_diff / 30.0)
            + self.W_ATR * (atr_break / dataframe['atr'].replace(0, np.nan))
            + self.W_SLOPE * (ema_slope * 1000.0)
        )
        return dataframe
'''
                entry = f'''
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['trend_score'] > self.SCORE_THRESHOLD)
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long_score'
        return dataframe
'''
                code = (
                    HEADER.format(doc=f"V4 G11 score th={th} {wname} stair={use_stair}")
                    + build_class_open(cn, True, attrs)
                    + ind
                    + entry
                    + populate_exit_trend_empty()
                    + custom_exit_block(use_stair, False)
                    + FOOTER_CONFIRM
                )
                save_strategy(
                    cn,
                    code,
                    f"G11 score>{th} {wname} stair={use_stair}",
                    "group11_trend_score",
                    {"threshold": th, "weights": wname, "stair": use_stair},
                )


def main():
    global experiments, _existing_classnames
    experiments = []
    _existing_classnames = set()

    gen_group1()
    gen_group2()
    gen_group3()
    gen_group4()
    gen_group5()
    gen_group6()
    gen_group7()
    gen_group8()
    gen_group9()
    gen_group10()
    gen_group11()

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
    print(f"Configs (G7): {CONFIG_DIR}")


if __name__ == "__main__":
    main()
