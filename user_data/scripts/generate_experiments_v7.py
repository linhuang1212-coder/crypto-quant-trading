# -*- coding: utf-8 -*-
"""
V7 Experiment Generator — V1-V6未覆盖的全新领域
基线：CryptoV11（动态G6 DC + G2 MACD共振 + 阶梯S5）

基于V6中间结果的学习：
  - 做空(E1)是最大突破，Sharpe 1.48 vs 基线1.21
  - 4H-DC共振(E6)显著降低DD到8.43%
  - 阶梯止盈(E10)/时间自适应trailing(E8)灾难性失败，趋势策略不能过早锁利
  - 回踩入场(E3)大幅降低表现，突破即入是最优的

V7全新探索方向（不重复V1-V6）：
  - G1: 成交量确认入场（Volume > MA_Vol 表示有效突破）— 18组
  - G2: RSI过滤（RSI区间条件过滤假突破）— 12组
  - G3: 不同时间框架（5m/30m/1h 对比15m）— 9组
  - G4: Keltner Channel 替代 Donchian（KC基于ATR，带中线）— 16组
  - G5: DC周期单参数扫描（固定DC，不用动态DC）— 12组
  - G6: 多币种权重（不同品种不同杠杆/仓位）— 8组
  - G7: 入场条件消融（逐个移除条件看贡献度）— 10组
  - G8: MACD直方图阈值（hist > threshold 而非 > 0）— 12组
  - G9: 日内时段过滤（亚洲/欧洲/美洲盘过滤）— 12组
  - G10: 连续突破过滤（要求N根K线连续在DC上方）— 12组
  - G11: 动态MAX_BARS（根据盈亏动态调整持仓时限）— 12组
  - G12: Stoploss精搜（-0.06 ~ -0.14 细粒度）— 10组
  - G13: 复合退出（DI+EMA+ADX联合退出信号）— 15组
  - G14: 市场状态感知（用ADX区分趋势/震荡，仅趋势市入场）— 10组
  - H1: V11基线对照 — 1组
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA = os.path.dirname(SCRIPT_DIR)
STRATEGY_DIR = os.path.join(USER_DATA, "strategies")
EXPERIMENT_DIR = os.path.join(STRATEGY_DIR, "experiments_v7")
MANIFEST_PATH = os.path.join(USER_DATA, "experiment_manifest_v7.json")

os.makedirs(EXPERIMENT_DIR, exist_ok=True)

experiments: List[Dict[str, Any]] = []
_existing_classnames: set = set()


def save_strategy(classname: str, code: str, name: str, group: str, params: dict):
    if classname in _existing_classnames:
        raise RuntimeError(f"Duplicate classname: {classname}")
    path = os.path.join(EXPERIMENT_DIR, f"{classname}.py")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    entry: Dict[str, Any] = {"name": name, "strategy": classname, "group": group, "params": params}
    experiments.append(entry)
    _existing_classnames.add(classname)


# ---------------------------------------------------------------------------
# Template fragments (reuse V6 proven templates)
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
    timeframe: str = "15m",
    trailing_stop: bool = True,
    stoploss: float = -0.10,
    trailing_stop_positive: float = 0.03,
    trailing_stop_positive_offset: float = 0.30,
    extra_class_attrs: str = "",
    informative_4h: bool = True,
    can_short: bool = True,
) -> str:
    ts = "True" if trailing_stop else "False"
    lines = [
        f"class {classname}(IStrategy):",
        "    INTERFACE_VERSION = 3",
        f"    timeframe = '{timeframe}'",
        f"    can_short = {can_short}",
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
        lines.extend([
            "    @informative('4h')",
            "    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:",
            "        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)",
            "        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)",
            "        return dataframe",
            "",
        ])
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


def indicators_v11_standard():
    return """
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
            lambda x: float(DataFrame(x).rank(pct=True).iloc[-1].item()) if len(x) == self.ATR_LOOKBACK else np.nan,
            raw=False,
        )
        use_short = atr_pct < self.ATR_PCT_THRESHOLD
        dc_s = dataframe['high'].rolling(self.DC_SHORT).max().shift(1)
        dc_l = dataframe['high'].rolling(self.DC_LONG).max().shift(1)
        dataframe['dc_upper'] = np.where(use_short, dc_s, dc_l)
        dc_low_s = dataframe['low'].rolling(self.DC_SHORT).min().shift(1)
        dc_low_l = dataframe['low'].rolling(self.DC_LONG).min().shift(1)
        dataframe['dc_lower'] = np.where(use_short, dc_low_s, dc_low_l)
        _macd = ta.MACD(dataframe, fastperiod=self.MACD_FAST, slowperiod=self.MACD_SLOW, signalperiod=self.MACD_SIGNAL)
        dataframe['macd'] = _macd['macd']
        dataframe['macdsignal'] = _macd['macdsignal']
        dataframe['macdhist'] = _macd['macdhist']
        dataframe['atr_pct'] = atr_pct
        return dataframe
"""


def exit_trend_empty():
    return """
    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe
"""


def custom_exit_v11():
    return """
    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
        if bars_held >= 40 and current_profit < -0.04:
            return "stair_late"
        if bars_held >= 20 and current_profit < -0.06:
            return "stair_mid"
        if bars_held >= self.MAX_BARS and current_profit < self.TIMEOUT_LOSS_THRESHOLD:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
"""

ENTRY_LONG_V11 = """(dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))"""

ENTRY_LONG_V11_FULL = """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))"""


def entry_trend_v11():
    return f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            {ENTRY_LONG_V11_FULL}
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""


# =============================================================================
# G1: 成交量确认入场（Volume > N * MA_Vol）
# =============================================================================
def gen_g1_volume():
    """G1: 要求突破时成交量高于均量，过滤低量假突破"""
    vol_periods = [20, 50]
    vol_multiples = [1.0, 1.5, 2.0]
    with_macd = [True, False]
    idx = 0
    for vp in vol_periods:
        for vm in vol_multiples:
            for macd in with_macd:
                idx += 1
                cn = f"V7_G1_P{idx:03d}"
                attrs = V11_BASE_ATTRS + f"    VOL_PERIOD = {vp}\n    VOL_MULT = {vm}\n"
                macd_cond = f"({ENTRY_LONG_V11}) &" if macd else ""
                extra_ind = f"""
        dataframe['vol_ma'] = dataframe['volume'].rolling({vp}).mean()
"""
                ind_code = indicators_v11_standard().replace(
                    "        return dataframe",
                    extra_ind + "        return dataframe"
                )
                entry_code = f"""
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
            {macd_cond}
            (dataframe['volume'] > dataframe['vol_ma'] * {vm})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_vol'
        return dataframe
"""
                code = (
                    HEADER.format(doc=f"V7 G1 volume confirm vp={vp} vm={vm} macd={macd}")
                    + build_class_open(cn, extra_class_attrs=attrs)
                    + ind_code
                    + entry_code
                    + exit_trend_empty()
                    + custom_exit_v11()
                    + FOOTER_CONFIRM
                )
                save_strategy(cn, code, f"G1 vol vp={vp} vm={vm} macd={macd}",
                              "group_g1_volume", {"vol_period": vp, "vol_mult": vm, "with_macd": macd})


# =============================================================================
# G2: RSI过滤（避免超买区入场）
# =============================================================================
def gen_g2_rsi_filter():
    """G2: RSI过滤 — 避免RSI过高时入场（趋势末端），12组"""
    rsi_periods = [14, 21]
    rsi_max_vals = [70, 75, 80]
    idx = 0
    for rp in rsi_periods:
        for rsi_max in rsi_max_vals:
            for with_macd in [True, False]:
                idx += 1
                cn = f"V7_G2_P{idx:03d}"
                attrs = V11_BASE_ATTRS + f"    RSI_PERIOD = {rp}\n    RSI_MAX = {rsi_max}\n"
                macd_cond = f"({ENTRY_LONG_V11}) &" if with_macd else ""
                extra_ind = f"""
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod={rp})
"""
                ind_code = indicators_v11_standard().replace(
                    "        return dataframe",
                    extra_ind + "        return dataframe"
                )
                entry_code = f"""
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
            {macd_cond}
            (dataframe['rsi'] < {rsi_max})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_rsi'
        return dataframe
"""
                code = (
                    HEADER.format(doc=f"V7 G2 RSI filter period={rp} max={rsi_max} macd={with_macd}")
                    + build_class_open(cn, extra_class_attrs=attrs)
                    + ind_code
                    + entry_code
                    + exit_trend_empty()
                    + custom_exit_v11()
                    + FOOTER_CONFIRM
                )
                save_strategy(cn, code, f"G2 RSI p={rp} max={rsi_max} macd={with_macd}",
                              "group_g2_rsi", {"rsi_period": rp, "rsi_max": rsi_max, "with_macd": with_macd})


# =============================================================================
# G3: 不同时间框架（5m/30m/1h）
# =============================================================================
def gen_g3_timeframes():
    """G3: 非15m时间框架测试，9组"""
    timeframes = ["5m", "30m", "1h"]
    # 不同时间框架需要调整bars参数
    tf_configs = {
        "5m":  {"max_bars": 192, "cooldown": 72, "stair_mid_bars": 60, "stair_late_bars": 120, "candles": 800},
        "30m": {"max_bars": 32, "cooldown": 12, "stair_mid_bars": 10, "stair_late_bars": 20, "candles": 400},
        "1h":  {"max_bars": 16, "cooldown": 6,  "stair_mid_bars": 5,  "stair_late_bars": 10, "candles": 400},
    }
    idx = 0
    for tf in timeframes:
        cfg = tf_configs[tf]
        for atr_mult in [0.4, 0.6, 0.8]:
            idx += 1
            cn = f"V7_G3_P{idx:03d}"
            attrs = V11_BASE_ATTRS.replace("MAX_BARS = 64", f"MAX_BARS = {cfg['max_bars']}")
            attrs = attrs.replace("COOLDOWN_BARS = 24", f"COOLDOWN_BARS = {cfg['cooldown']}")
            attrs = attrs.replace("ATR_MULT = 0.6", f"ATR_MULT = {atr_mult}")
            exit_code = f"""
    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        tf_minutes = {{'5m': 5, '15m': 15, '30m': 30, '1h': 60}}
        mins = tf_minutes.get(self.timeframe, 15)
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (mins * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
        if bars_held >= {cfg['stair_late_bars']} and current_profit < -0.04:
            return "stair_late"
        if bars_held >= {cfg['stair_mid_bars']} and current_profit < -0.06:
            return "stair_mid"
        if bars_held >= self.MAX_BARS and current_profit < self.TIMEOUT_LOSS_THRESHOLD:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
"""
            # 4h informative needs adjustment for 1h timeframe
            use_4h = tf != "1h"
            if use_4h:
                ema_4h_cond = "(dataframe['ema21_4h'] > dataframe['ema55_4h']) &"
            else:
                ema_4h_cond = ""

            entry_code = f"""
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
            {ema_4h_cond}
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V7 G3 timeframe={tf} atr_mult={atr_mult}")
                + build_class_open(cn, timeframe=tf, extra_class_attrs=attrs, informative_4h=use_4h)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + exit_code
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"G3 tf={tf} atr={atr_mult}",
                          "group_g3_timeframe", {"timeframe": tf, "atr_mult": atr_mult})


# =============================================================================
# G4: Keltner Channel 替代 Donchian
# =============================================================================
def gen_g4_keltner():
    """G4: Keltner Channel突破 — 基于EMA+ATR的通道，16组"""
    kc_periods = [20, 30, 40]
    kc_mults = [1.5, 2.0, 2.5]
    idx = 0
    for kp in kc_periods:
        for km in kc_mults:
            for with_macd in [True, False]:
                if idx >= 16:
                    break
                idx += 1
                cn = f"V7_G4_P{idx:03d}"
                attrs = V11_BASE_ATTRS + f"    KC_PERIOD = {kp}\n    KC_MULT = {km}\n"
                macd_cond = f"({ENTRY_LONG_V11}) &" if with_macd else ""
                ind_code = f"""
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        kc_mid = ta.EMA(dataframe, timeperiod={kp})
        kc_atr = ta.ATR(dataframe, timeperiod={kp})
        dataframe['kc_upper'] = kc_mid + {km} * kc_atr
        dataframe['kc_lower'] = kc_mid - {km} * kc_atr
        _macd = ta.MACD(dataframe, fastperiod=self.MACD_FAST, slowperiod=self.MACD_SLOW, signalperiod=self.MACD_SIGNAL)
        dataframe['macd'] = _macd['macd']
        dataframe['macdsignal'] = _macd['macdsignal']
        dataframe['macdhist'] = _macd['macdhist']
        return dataframe
"""
                entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['kc_upper']) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            {macd_cond}
            (dataframe['close'] > dataframe['ema21'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'kc_long'
        return dataframe
"""
                code = (
                    HEADER.format(doc=f"V7 G4 Keltner kp={kp} km={km} macd={with_macd}")
                    + build_class_open(cn, extra_class_attrs=attrs)
                    + ind_code
                    + entry_code
                    + exit_trend_empty()
                    + custom_exit_v11()
                    + FOOTER_CONFIRM
                )
                save_strategy(cn, code, f"G4 KC p={kp} m={km} macd={with_macd}",
                              "group_g4_keltner", {"kc_period": kp, "kc_mult": km, "with_macd": with_macd})


# =============================================================================
# G5: DC周期单参数扫描（固定DC，不用动态DC）
# =============================================================================
def gen_g5_dc_fixed():
    """G5: 固定DC周期扫描 — 对比动态DC(G6)是否真的必要，12组"""
    dc_periods = [10, 12, 14, 18, 20, 25, 30, 35, 40, 50, 60, 80]
    idx = 0
    for dc in dc_periods:
        idx += 1
        cn = f"V7_G5_P{idx:03d}"
        attrs = V11_BASE_ATTRS
        ind_code = f"""
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['dc_upper'] = dataframe['high'].rolling({dc}).max().shift(1)
        dataframe['dc_lower'] = dataframe['low'].rolling({dc}).min().shift(1)
        _macd = ta.MACD(dataframe, fastperiod=self.MACD_FAST, slowperiod=self.MACD_SLOW, signalperiod=self.MACD_SIGNAL)
        dataframe['macd'] = _macd['macd']
        dataframe['macdsignal'] = _macd['macdsignal']
        dataframe['macdhist'] = _macd['macdhist']
        return dataframe
"""
        code = (
            HEADER.format(doc=f"V7 G5 fixed DC={dc}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + ind_code
            + entry_trend_v11()
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"G5 DC={dc}", "group_g5_dc_fixed", {"dc_period": dc})


# =============================================================================
# G6: 多币种权重（不同品种不同杠杆）
# =============================================================================
def gen_g6_pair_weights():
    """G6: 品种自适应杠杆 — 高表现品种高杠杆，8组"""
    configs = [
        {"btc": 3, "eth": 7, "sol": 5, "ada": 7},
        {"btc": 5, "eth": 7, "sol": 3, "ada": 7},
        {"btc": 3, "eth": 5, "sol": 5, "ada": 5},
        {"btc": 7, "eth": 7, "sol": 3, "ada": 5},
        {"btc": 5, "eth": 5, "sol": 7, "ada": 7},
        {"btc": 3, "eth": 7, "sol": 7, "ada": 5},
        {"btc": 5, "eth": 3, "sol": 7, "ada": 7},
        {"btc": 7, "eth": 5, "sol": 5, "ada": 3},
    ]
    idx = 0
    for cfg in configs:
        idx += 1
        cn = f"V7_G6_P{idx:03d}"
        attrs = V11_BASE_ATTRS
        lev_code = f"""
    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        pair_levs = {{'BTC/USDT:USDT': {cfg['btc']}, 'ETH/USDT:USDT': {cfg['eth']}, 'SOL/USDT:USDT': {cfg['sol']}, 'ADA/USDT:USDT': {cfg['ada']}}}
        return float(pair_levs.get(pair, 5))
"""
        code_raw = (
            HEADER.format(doc=f"V7 G6 pair weights btc={cfg['btc']} eth={cfg['eth']} sol={cfg['sol']} ada={cfg['ada']}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + indicators_v11_standard()
            + entry_trend_v11()
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        code = code_raw.replace(
            "    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):\n        return 5.0\n",
            lev_code.lstrip('\n')
        )
        save_strategy(cn, code, f"G6 btc={cfg['btc']} eth={cfg['eth']} sol={cfg['sol']} ada={cfg['ada']}",
                      "group_g6_pair_weight", cfg)


# =============================================================================
# G7: 入场条件消融（逐个移除条件看贡献度）
# =============================================================================
def gen_g7_ablation():
    """G7: 消融实验 — 逐个移除V11的入场条件，10组"""
    ablations = {
        "no_atr_filter": "移除ATR突破力度过滤",
        "no_adx_rising": "移除ADX上升要求",
        "no_di_cross": "移除DI方向要求",
        "no_ema_align": "移除15m EMA三线排列",
        "no_ema200": "移除EMA200条件(只保留21>55)",
        "no_4h_ema": "移除4H EMA确认",
        "no_macd": "移除MACD共振",
        "no_macd_rising": "MACD只要>0不要求上升",
        "minimal_dc_adx": "最简:只DC突破+ADX>28",
        "minimal_dc_only": "极简:只DC突破",
    }
    conditions_map = {
        "no_atr_filter": """(dataframe['close'] > dataframe['dc_upper']) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))""",
        "no_adx_rising": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))""",
        "no_di_cross": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))""",
        "no_ema_align": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))""",
        "no_ema200": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))""",
        "no_4h_ema": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))""",
        "no_macd": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])""",
        "no_macd_rising": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['macdhist'] > 0)""",
        "minimal_dc_adx": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN)""",
        "minimal_dc_only": """(dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT))""",
    }
    idx = 0
    for abl_name, desc in ablations.items():
        idx += 1
        cn = f"V7_G7_P{idx:03d}"
        attrs = V11_BASE_ATTRS
        cond = conditions_map[abl_name]
        entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            {cond}
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_{abl_name}'
        return dataframe
"""
        code = (
            HEADER.format(doc=f"V7 G7 ablation: {abl_name} — {desc}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + indicators_v11_standard()
            + entry_code
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"G7 {abl_name}", "group_g7_ablation", {"ablation": abl_name, "desc": desc})


# =============================================================================
# G8: MACD直方图阈值（hist > threshold）
# =============================================================================
def gen_g8_macd_threshold():
    """G8: MACD histogram要求绝对值大于阈值，过滤弱动量，12组"""
    # 使用归一化阈值：hist / atr 比值
    thresholds = [0.0, 0.001, 0.005, 0.01, 0.02, 0.05]
    idx = 0
    for th in thresholds:
        for rising_req in [True, False]:
            idx += 1
            cn = f"V7_G8_P{idx:03d}"
            attrs = V11_BASE_ATTRS + f"    MACD_HIST_THRESHOLD = {th}\n"
            if th == 0.0:
                macd_cond = "(dataframe['macdhist'] > 0)"
            else:
                macd_cond = f"(dataframe['macdhist'] > {th})"
            if rising_req:
                macd_cond += " & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))"

            entry_code = f"""
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
            {macd_cond}
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_macd_th'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V7 G8 MACD threshold={th} rising={rising_req}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"G8 hist_th={th} rising={rising_req}",
                          "group_g8_macd_th", {"threshold": th, "rising_required": rising_req})


# =============================================================================
# G9: 日内时段过滤
# =============================================================================
def gen_g9_session_filter():
    """G9: 按UTC时段过滤入场 — 测试不同时段的趋势质量，12组"""
    sessions = {
        "asia":     (0, 8),     # UTC 0-8 (亚洲)
        "europe":   (8, 16),    # UTC 8-16 (欧洲)
        "us":       (14, 22),   # UTC 14-22 (美洲)
        "no_asia":  (-1, -1),   # 排除亚洲盘
        "no_low":   (-2, -2),   # 排除低流动性时段 (22-6 UTC)
        "overlap":  (13, 17),   # 欧美重叠
    }
    idx = 0
    for sess_name, (start_h, end_h) in sessions.items():
        for with_macd in [True, False]:
            idx += 1
            cn = f"V7_G9_P{idx:03d}"
            attrs = V11_BASE_ATTRS
            macd_cond = f"({ENTRY_LONG_V11}) &" if with_macd else ""
            if start_h == -1:  # no_asia
                time_cond = "((dataframe['date'].dt.hour >= 8) | (dataframe['date'].dt.hour < 0))"
                time_cond = "((dataframe['date'].dt.hour >= 8))"
            elif start_h == -2:  # no_low
                time_cond = "((dataframe['date'].dt.hour >= 6) & (dataframe['date'].dt.hour < 22))"
            else:
                if start_h < end_h:
                    time_cond = f"((dataframe['date'].dt.hour >= {start_h}) & (dataframe['date'].dt.hour < {end_h}))"
                else:
                    time_cond = f"((dataframe['date'].dt.hour >= {start_h}) | (dataframe['date'].dt.hour < {end_h}))"

            entry_code = f"""
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
            {macd_cond}
            {time_cond}
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_{sess_name}'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V7 G9 session={sess_name} macd={with_macd}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"G9 sess={sess_name} macd={with_macd}",
                          "group_g9_session", {"session": sess_name, "with_macd": with_macd})


# =============================================================================
# G10: 连续突破过滤（要求N根K线连续在DC上方）
# =============================================================================
def gen_g10_consecutive():
    """G10: 连续N根K线在DC上方才入场，过滤瞬时假突破，12组"""
    n_bars_list = [2, 3, 4, 5, 6, 8]
    idx = 0
    for n in n_bars_list:
        for with_macd in [True, False]:
            idx += 1
            cn = f"V7_G10_P{idx:03d}"
            attrs = V11_BASE_ATTRS + f"    CONSEC_BARS = {n}\n"
            macd_cond = f"({ENTRY_LONG_V11}) &" if with_macd else ""
            extra_ind = f"""
        above_dc = (dataframe['close'] > dataframe['dc_upper']).astype(int)
        dataframe['consec_above'] = above_dc.rolling({n}).sum()
"""
            ind_code = indicators_v11_standard().replace(
                "        return dataframe",
                extra_ind + "        return dataframe"
            )
            entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['consec_above'] >= {n}) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            {macd_cond}
            (dataframe['close'] > dataframe['dc_upper'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_consec'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V7 G10 consecutive bars={n} macd={with_macd}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + ind_code
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"G10 consec={n} macd={with_macd}",
                          "group_g10_consecutive", {"consecutive_bars": n, "with_macd": with_macd})


# =============================================================================
# G11: 动态MAX_BARS（盈利时加长，亏损时缩短）
# =============================================================================
def gen_g11_dynamic_timeout():
    """G11: 动态持仓时限 — 盈利持仓不设限，亏损提前止，12组"""
    configs = [
        (32, 96), (40, 80), (48, 128), (24, 64), (32, 128), (48, 96),
    ]
    idx = 0
    for loss_bars, win_bars in configs:
        for loss_th in [-0.02, -0.03]:
            idx += 1
            cn = f"V7_G11_P{idx:03d}"
            attrs = V11_BASE_ATTRS
            exit_code = f"""
    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
        if bars_held >= 40 and current_profit < -0.04:
            return "stair_late"
        if bars_held >= 20 and current_profit < -0.06:
            return "stair_mid"
        if bars_held >= {loss_bars} and current_profit < {loss_th}:
            return "timeout_loss_dyn"
        if bars_held >= {win_bars} and current_profit < 0.01:
            return "timeout_neutral"
        if bars_held >= {win_bars} * 2:
            return "timeout_extended"
        return None
"""
            code = (
                HEADER.format(doc=f"V7 G11 dynamic timeout loss={loss_bars} win={win_bars} th={loss_th}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_trend_v11()
                + exit_trend_empty()
                + exit_code
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"G11 loss_bars={loss_bars} win_bars={win_bars} th={loss_th}",
                          "group_g11_dyn_timeout", {"loss_bars": loss_bars, "win_bars": win_bars, "loss_threshold": loss_th})


# =============================================================================
# G12: Stoploss精搜
# =============================================================================
def gen_g12_stoploss_scan():
    """G12: 硬止损精搜 -0.06 ~ -0.14，10组"""
    stoploss_vals = [-0.06, -0.07, -0.08, -0.09, -0.10, -0.11, -0.12, -0.13, -0.14, -0.15]
    idx = 0
    for sl in stoploss_vals:
        idx += 1
        cn = f"V7_G12_P{idx:03d}"
        attrs = V11_BASE_ATTRS
        code = (
            HEADER.format(doc=f"V7 G12 stoploss={sl}")
            + build_class_open(cn, stoploss=sl, extra_class_attrs=attrs)
            + indicators_v11_standard()
            + entry_trend_v11()
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"G12 SL={sl}", "group_g12_stoploss", {"stoploss": sl})


# =============================================================================
# G13: 复合退出（多信号联合退出）
# =============================================================================
def gen_g13_compound_exit():
    """G13: 复合退出 — 多个弱信号联合触发退出，15组"""
    configs = []
    for need_di in [True, False]:
        for need_ema in [True, False]:
            for need_adx_drop in [True, False]:
                for min_bars in [8, 16]:
                    if not (need_di or need_ema or need_adx_drop):
                        continue
                    signals = sum([need_di, need_ema, need_adx_drop])
                    if signals < 2:
                        continue
                    configs.append((need_di, need_ema, need_adx_drop, min_bars))
    configs = configs[:15]

    idx = 0
    for need_di, need_ema, need_adx, min_bars in configs:
        idx += 1
        cn = f"V7_G13_P{idx:03d}"
        attrs = V11_BASE_ATTRS

        checks = []
        if need_di:
            checks.append("last['minus_di'] > last['plus_di']")
        if need_ema:
            checks.append("last['ema21'] < last['ema55']")
        if need_adx:
            checks.append("last['adx'] < dataframe['adx'].iloc[-3]")
        check_str = " and ".join(checks)

        exit_code = f"""
    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
        if bars_held >= 40 and current_profit < -0.04:
            return "stair_late"
        if bars_held >= 20 and current_profit < -0.06:
            return "stair_mid"
        if bars_held >= {min_bars}:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) >= 3:
                last = dataframe.iloc[-1]
                if {check_str}:
                    return "compound_exit"
        if bars_held >= self.MAX_BARS and current_profit < self.TIMEOUT_LOSS_THRESHOLD:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
"""
        label = f"di={need_di} ema={need_ema} adx={need_adx} bars={min_bars}"
        code = (
            HEADER.format(doc=f"V7 G13 compound exit {label}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + indicators_v11_standard()
            + entry_trend_v11()
            + exit_trend_empty()
            + exit_code
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"G13 {label}",
                      "group_g13_compound_exit",
                      {"need_di": need_di, "need_ema": need_ema, "need_adx": need_adx, "min_bars": min_bars})


# =============================================================================
# G14: 市场状态感知（ADX级别区分趋势强度）
# =============================================================================
def gen_g14_market_regime():
    """G14: 根据ADX水平区分市场状态 — 仅强趋势入场，10组"""
    configs = []
    for adx_strong in [35, 40, 45]:
        for adx_weak_action in ["skip", "half_leverage"]:
            configs.append((adx_strong, adx_weak_action))
    # 也测试用ADX斜率而非绝对值
    for slope_bars in [5, 10]:
        configs.append((0, f"slope_{slope_bars}"))
    configs = configs[:10]

    idx = 0
    for adx_th, action in configs:
        idx += 1
        cn = f"V7_G14_P{idx:03d}"
        attrs = V11_BASE_ATTRS

        if isinstance(action, str) and action.startswith("slope_"):
            slope_bars = int(action.split("_")[1])
            extra_ind = f"""
        dataframe['adx_slope'] = (dataframe['adx'] - dataframe['adx'].shift({slope_bars})) / {slope_bars}
"""
            ind_code = indicators_v11_standard().replace(
                "        return dataframe",
                extra_ind + "        return dataframe"
            )
            entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['adx_slope'] > 0.5) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_regime'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V7 G14 market regime adx_slope bars={slope_bars}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + ind_code
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"G14 adx_slope bars={slope_bars}",
                          "group_g14_regime", {"type": "slope", "slope_bars": slope_bars})

        elif action == "half_leverage":
            lev_code = f"""
    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) > 0:
            adx_val = dataframe.iloc[-1]['adx']
            if adx_val >= {adx_th}:
                return 7.0
            return 3.0
        return 5.0
"""
            code_raw = (
                HEADER.format(doc=f"V7 G14 regime half_lev adx_th={adx_th}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_trend_v11()
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            code = code_raw.replace(
                "    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):\n        return 5.0\n",
                lev_code.lstrip('\n')
            )
            save_strategy(cn, code, f"G14 half_lev adx={adx_th}",
                          "group_g14_regime", {"type": "half_leverage", "adx_threshold": adx_th})

        else:  # skip
            entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > {adx_th}) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_strong_trend'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V7 G14 regime strong_only adx>{adx_th}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"G14 strong_only adx>{adx_th}",
                          "group_g14_regime", {"type": "strong_only", "adx_threshold": adx_th})


# =============================================================================
# H1: 基线对照
# =============================================================================
def gen_h1_baseline():
    """H1: CryptoV11 基线对照"""
    cn = "V7_H1_P001"
    attrs = V11_BASE_ATTRS
    code = (
        HEADER.format(doc="V7 H1 CryptoV11 baseline")
        + build_class_open(cn, extra_class_attrs=attrs)
        + indicators_v11_standard()
        + entry_trend_v11()
        + exit_trend_empty()
        + custom_exit_v11()
        + FOOTER_CONFIRM
    )
    save_strategy(cn, code, "H1 CryptoV11 baseline", "group_h1_baseline", {"variant": "v11_baseline"})


# =============================================================================
# Main
# =============================================================================
def main():
    global experiments, _existing_classnames
    experiments = []
    _existing_classnames = set()

    gen_g1_volume()
    gen_g2_rsi_filter()
    gen_g3_timeframes()
    gen_g4_keltner()
    gen_g5_dc_fixed()
    gen_g6_pair_weights()
    gen_g7_ablation()
    gen_g8_macd_threshold()
    gen_g9_session_filter()
    gen_g10_consecutive()
    gen_g11_dynamic_timeout()
    gen_g12_stoploss_scan()
    gen_g13_compound_exit()
    gen_g14_market_regime()
    gen_h1_baseline()

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
