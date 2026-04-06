# -*- coding: utf-8 -*-
"""
V6 Experiment Generator — 全新探索方向（不重复V1-V5已验证的领域）
基线：CryptoV11（动态G6 DC + G2 MACD共振 + 阶梯S5）

探索方向（约300个变体）：
- E1: 做空逻辑（CryptoV11 only-long，从未测试做空）— 20组
- E2: ADX阈值精搜（22-34） + 品种自适应ADX — 20组
- E3: 入场回踩确认（突破后回踩再入 vs 突破即入）— 18组
- E4: 退出信号增强（趋势反转退出、DI交叉退出、ADX衰退退出）— 24组
- E5: 波动率自适应杠杆（低波动高杠杆，高波动低杠杆）— 15组
- E6: 4H DC共振（15m+4H双重DC突破确认）— 16组
- E7: 动态ATR_MULT（根据波动率百分位调整入场门槛）— 16组
- E8: 持仓时间自适应止盈（持仓越久trailing越紧）— 20组
- E9: 入场动量强度分级（弱/中/强突破不同仓位管理）— 16组
- E10: DC周期自适应扩展（用ADX而非ATR选DC周期）— 16组
- E11: 多级阶梯止盈（不只止损，还分级止盈）— 18组
- F1: CryptoV11 基线对照 — 1组
- F2: 做空+做多组合最优 — 按E1结果
"""
from __future__ import annotations

import json
import os
from itertools import product
from typing import Any, Dict, List

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA = os.path.dirname(SCRIPT_DIR)
STRATEGY_DIR = os.path.join(USER_DATA, "strategies")
EXPERIMENT_DIR = os.path.join(STRATEGY_DIR, "experiments_v6")
MANIFEST_PATH = os.path.join(USER_DATA, "experiment_manifest_v6.json")

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
# Template fragments
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
        "    timeframe = '15m'",
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


# =============================================================================
# E1: 做空逻辑（全新 — CryptoV11从未测试做空）
# =============================================================================
def gen_e1_short():
    """E1: 做空策略 — DC下破 + 反向条件，20组"""
    short_modes = {
        "mirror": {
            "desc": "完全镜像做多逻辑",
            "short_cond": """(dataframe['close'] < dataframe['dc_lower']) &
            ((dataframe['dc_lower'] - dataframe['close']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['minus_di'] > dataframe['plus_di']) &
            (dataframe['ema21'] < dataframe['ema55']) &
            (dataframe['ema55'] < dataframe['ema200']) &
            (dataframe['ema21_4h'] < dataframe['ema55_4h']) &
            (dataframe['macdhist'] < 0) & (dataframe['macdhist'] < dataframe['macdhist'].shift(1))""",
        },
        "relaxed_ema": {
            "desc": "做空不要求EMA200排列(熊市EMA200很慢)",
            "short_cond": """(dataframe['close'] < dataframe['dc_lower']) &
            ((dataframe['dc_lower'] - dataframe['close']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['minus_di'] > dataframe['plus_di']) &
            (dataframe['ema21'] < dataframe['ema55']) &
            (dataframe['ema21_4h'] < dataframe['ema55_4h']) &
            (dataframe['macdhist'] < 0) & (dataframe['macdhist'] < dataframe['macdhist'].shift(1))""",
        },
        "no_macd": {
            "desc": "做空不要MACD(熊市做空MACD可能不适用)",
            "short_cond": """(dataframe['close'] < dataframe['dc_lower']) &
            ((dataframe['dc_lower'] - dataframe['close']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['minus_di'] > dataframe['plus_di']) &
            (dataframe['ema21'] < dataframe['ema55']) &
            (dataframe['ema21_4h'] < dataframe['ema55_4h'])""",
        },
        "adx_only": {
            "desc": "做空只看ADX+DI(最简化)",
            "short_cond": """(dataframe['close'] < dataframe['dc_lower']) &
            ((dataframe['dc_lower'] - dataframe['close']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) &
            (dataframe['minus_di'] > dataframe['plus_di'])""",
        },
    }

    adx_shorts = [24, 28, 32]
    idx = 0
    for mode_name, mode_info in short_modes.items():
        for adx in adx_shorts:
            idx += 1
            cn = f"V6_E1_P{idx:03d}"
            attrs = V11_BASE_ATTRS.replace("ADX_MIN = 28", f"ADX_MIN = {adx}")
            short_cond_adj = mode_info["short_cond"]
            if adx != 28:
                short_cond_adj = short_cond_adj.replace("self.ADX_MIN", f"{adx}")

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
            ({ENTRY_LONG_V11})
        )
        short_conditions = (
            {short_cond_adj}
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        dataframe.loc[short_conditions, 'enter_short'] = 1
        dataframe.loc[short_conditions, 'enter_tag'] = 'dc_short'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V6 E1 short mode={mode_name} ADX={adx}")
                + build_class_open(cn, extra_class_attrs=attrs, can_short=True)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"E1 {mode_name} ADX={adx}", "group_e1_short", {"mode": mode_name, "adx": adx})

    # Short-only variants (no long)
    for mode_name in ["mirror", "relaxed_ema"]:
        for adx in [24, 28]:
            idx += 1
            cn = f"V6_E1_P{idx:03d}"
            attrs = V11_BASE_ATTRS.replace("ADX_MIN = 28", f"ADX_MIN = {adx}")
            short_cond_adj = short_modes[mode_name]["short_cond"]

            entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        short_conditions = (
            {short_cond_adj}
        )
        dataframe.loc[short_conditions, 'enter_short'] = 1
        dataframe.loc[short_conditions, 'enter_tag'] = 'dc_short'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V6 E1 short-only mode={mode_name} ADX={adx}")
                + build_class_open(cn, extra_class_attrs=attrs, can_short=True)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"E1 short-only {mode_name} ADX={adx}", "group_e1_short",
                          {"mode": f"short_only_{mode_name}", "adx": adx})


# =============================================================================
# E2: ADX阈值精搜 + 品种自适应
# =============================================================================
def gen_e2_adx_scan():
    """E2: ADX精搜 22-34 步长2，共7组"""
    adx_values = [22, 24, 26, 28, 30, 32, 34]
    idx = 0
    for adx in adx_values:
        idx += 1
        cn = f"V6_E2_P{idx:03d}"
        attrs = V11_BASE_ATTRS.replace("ADX_MIN = 28", f"ADX_MIN = {adx}")
        entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > {adx}) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
        code = (
            HEADER.format(doc=f"V6 E2 ADX_MIN={adx}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + indicators_v11_standard()
            + entry_code
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"E2 ADX={adx}", "group_e2_adx", {"ADX_MIN": adx})


# =============================================================================
# E3: 入场回踩确认（突破后回踩DC再入）
# =============================================================================
def gen_e3_pullback():
    """E3: 回踩确认入场 — 先突破DC，回踩DC附近再入，18组"""
    pullback_configs = []
    for lookback in [3, 5, 8]:
        for proximity in [0.3, 0.5, 0.8]:
            for require_macd in [True, False]:
                pullback_configs.append((lookback, proximity, require_macd))

    idx = 0
    for lookback, proximity, req_macd in pullback_configs:
        idx += 1
        cn = f"V6_E3_P{idx:03d}"
        attrs = V11_BASE_ATTRS + f"""    PULLBACK_LOOKBACK = {lookback}
    PULLBACK_PROXIMITY = {proximity}
"""
        macd_cond = f"({ENTRY_LONG_V11})" if req_macd else "(True)"
        extra_indicators = f"""
        dataframe['broke_above'] = (dataframe['high'].rolling({lookback}).max() > dataframe['dc_upper']).astype(int)
        dataframe['near_dc'] = ((dataframe['close'] - dataframe['dc_upper']).abs() < dataframe['atr'] * {proximity}).astype(int)
"""
        ind_code = indicators_v11_standard().replace(
            "        return dataframe",
            extra_indicators + "        return dataframe"
        )
        entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['broke_above'] == 1) &
            (dataframe['near_dc'] == 1) &
            (dataframe['close'] > dataframe['dc_upper']) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            {macd_cond}
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_pullback'
        return dataframe
"""
        code = (
            HEADER.format(doc=f"V6 E3 pullback lb={lookback} prox={proximity} macd={req_macd}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + ind_code
            + entry_code
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"E3 pull lb={lookback} prox={proximity} macd={req_macd}",
                       "group_e3_pullback", {"lookback": lookback, "proximity": proximity, "require_macd": req_macd})


# =============================================================================
# E4: 退出信号增强（趋势反转退出）
# =============================================================================
def gen_e4_exit_signals():
    """E4: 智能退出信号 — DI交叉/ADX衰退/EMA交叉退出，24组"""
    idx = 0

    # E4a: DI交叉退出（持仓中 -DI 超过 +DI 时退出）
    for min_bars in [8, 12, 16, 20]:
        for min_profit in [-0.02, 0.0, 0.02]:
            idx += 1
            cn = f"V6_E4_P{idx:03d}"
            attrs = V11_BASE_ATTRS + f"""    EXIT_DI_MIN_BARS = {min_bars}
    EXIT_DI_MIN_PROFIT = {min_profit}
"""
            exit_code = f"""
    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
        if bars_held >= 40 and current_profit < -0.04:
            return "stair_late"
        if bars_held >= 20 and current_profit < -0.06:
            return "stair_mid"
        if bars_held >= {min_bars} and current_profit > {min_profit}:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) > 0:
                last = dataframe.iloc[-1]
                if last['minus_di'] > last['plus_di']:
                    return "di_cross_exit"
        if bars_held >= self.MAX_BARS and current_profit < self.TIMEOUT_LOSS_THRESHOLD:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
"""
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
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V6 E4a DI cross exit bars={min_bars} profit={min_profit}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + exit_code
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"E4a DI exit bars={min_bars} profit={min_profit}",
                          "group_e4_exit", {"type": "di_cross", "min_bars": min_bars, "min_profit": min_profit})

    # E4b: ADX衰退退出（ADX连续下降N根K线时退出盈利单）
    for adx_drop_bars in [3, 5, 8]:
        for min_profit_adx in [0.01, 0.03]:
            idx += 1
            cn = f"V6_E4_P{idx:03d}"
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
        if bars_held >= 8 and current_profit > {min_profit_adx}:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) >= {adx_drop_bars + 1}:
                adx_vals = dataframe['adx'].iloc[-{adx_drop_bars + 1}:].values
                if all(adx_vals[i] > adx_vals[i+1] for i in range({adx_drop_bars})):
                    return "adx_decay_exit"
        if bars_held >= self.MAX_BARS and current_profit < self.TIMEOUT_LOSS_THRESHOLD:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
"""
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
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V6 E4b ADX decay exit drop={adx_drop_bars} profit={min_profit_adx}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + exit_code
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"E4b ADX decay drop={adx_drop_bars} profit={min_profit_adx}",
                          "group_e4_exit", {"type": "adx_decay", "drop_bars": adx_drop_bars, "min_profit": min_profit_adx})


# =============================================================================
# E5: 波动率自适应杠杆
# =============================================================================
def gen_e5_adaptive_leverage():
    """E5: 根据ATR百分位动态调整杠杆 — 15组"""
    configs = []
    for low_lev, high_lev in [(7, 3), (6, 3), (5, 3), (7, 4), (6, 4)]:
        for threshold in [0.5, 0.7, 0.8]:
            configs.append((low_lev, high_lev, threshold))

    idx = 0
    for low_lev, high_lev, threshold in configs:
        idx += 1
        cn = f"V6_E5_P{idx:03d}"
        attrs = V11_BASE_ATTRS + f"""    LEV_LOW_VOL = {low_lev}
    LEV_HIGH_VOL = {high_lev}
    LEV_ATR_THRESHOLD = {threshold}
"""
        leverage_code = f"""
    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) > 0:
            atr_pct_val = dataframe.iloc[-1].get('atr_pct', 0.5)
            if not np.isnan(atr_pct_val) and atr_pct_val >= {threshold}:
                return float({high_lev})
        return float({low_lev})
"""
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
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
        # Remove default leverage from class_open and add custom
        code_raw = (
            HEADER.format(doc=f"V6 E5 adaptive leverage low={low_lev} high={high_lev} th={threshold}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + indicators_v11_standard()
            + entry_code
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        code = code_raw.replace(
            "    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):\n        return 5.0\n",
            leverage_code.lstrip('\n')
        )
        save_strategy(cn, code, f"E5 lev low={low_lev} high={high_lev} th={threshold}",
                       "group_e5_leverage", {"low_vol_lev": low_lev, "high_vol_lev": high_lev, "threshold": threshold})


# =============================================================================
# E6: 4H DC共振（多时间框架DC突破确认）
# =============================================================================
def gen_e6_mtf_dc():
    """E6: 4H DC突破确认 + 15m DC突破，16组"""
    dc_4h_periods = [10, 14, 20, 30]
    require_4h_breakout = [True, False]  # True=4H也要突破DC, False=4H价格在DC上方即可
    idx = 0
    for dc4h, req_breakout in product(dc_4h_periods, require_4h_breakout):
        for atr_mult_4h in [0.0, 0.3]:
            idx += 1
            cn = f"V6_E6_P{idx:03d}"
            attrs = V11_BASE_ATTRS + f"    DC_4H_PERIOD = {dc4h}\n"

            informative_code = f"""
    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['dc_upper_4h'] = dataframe['high'].rolling({dc4h}).max().shift(1)
        dataframe['atr_4h'] = ta.ATR(dataframe, timeperiod=14)
        return dataframe
"""
            if req_breakout:
                if atr_mult_4h > 0:
                    cond_4h = f"(dataframe['close'] > dataframe['dc_upper_4h_4h']) & ((dataframe['close'] - dataframe['dc_upper_4h_4h']) > dataframe['atr_4h_4h'] * {atr_mult_4h})"
                else:
                    cond_4h = "(dataframe['close'] > dataframe['dc_upper_4h_4h'])"
            else:
                cond_4h = "(dataframe['close'] > dataframe['dc_upper_4h_4h'])"

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
            {cond_4h} &
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_mtf'
        return dataframe
"""
            ind_code = indicators_v11_standard()
            code_raw = (
                HEADER.format(doc=f"V6 E6 MTF DC 4H dc={dc4h} breakout={req_breakout} atr={atr_mult_4h}")
                + build_class_open(cn, extra_class_attrs=attrs, informative_4h=False)
                + informative_code
                + ind_code
                + entry_code
                + exit_trend_empty()
                + custom_exit_v11()
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code_raw, f"E6 4H-DC={dc4h} brk={req_breakout} atr={atr_mult_4h}",
                          "group_e6_mtf_dc", {"dc_4h": dc4h, "require_breakout": req_breakout, "atr_mult_4h": atr_mult_4h})


# =============================================================================
# E7: 动态ATR_MULT
# =============================================================================
def gen_e7_dynamic_atr_mult():
    """E7: 根据波动率百分位动态调整入场ATR门槛，16组"""
    configs = []
    for low_mult, high_mult in [(0.3, 0.8), (0.4, 0.8), (0.3, 1.0), (0.5, 1.0)]:
        for threshold in [0.5, 0.6, 0.7, 0.8]:
            configs.append((low_mult, high_mult, threshold))

    idx = 0
    for low_m, high_m, th in configs:
        idx += 1
        cn = f"V6_E7_P{idx:03d}"
        attrs = V11_BASE_ATTRS + f"""    ATR_MULT_LOW = {low_m}
    ATR_MULT_HIGH = {high_m}
    ATR_MULT_THRESHOLD = {th}
"""
        ind_extra = f"""
        dataframe['dyn_atr_mult'] = np.where(dataframe['atr_pct'] < {th}, {low_m}, {high_m})
"""
        ind_code = indicators_v11_standard().replace(
            "        return dataframe",
            ind_extra + "        return dataframe"
        )
        entry_code = f"""
    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * dataframe['dyn_atr_mult'])) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_dyn_atr'
        return dataframe
"""
        code = (
            HEADER.format(doc=f"V6 E7 dynamic ATR_MULT low={low_m} high={high_m} th={th}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + ind_code
            + entry_code
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"E7 dynATR low={low_m} high={high_m} th={th}",
                       "group_e7_dyn_atr", {"low_mult": low_m, "high_mult": high_m, "threshold": th})


# =============================================================================
# E8: 持仓时间自适应trailing
# =============================================================================
def gen_e8_time_adaptive_exit():
    """E8: 持仓越久trailing越紧 — 通过custom_stoploss实现，20组"""
    configs = []
    for base_trail in [0.03, 0.04]:
        for tight_trail in [0.01, 0.015, 0.02]:
            for transition_bars in [24, 40, 56]:
                configs.append((base_trail, tight_trail, transition_bars))
            configs.append((base_trail, tight_trail, 80))
    # Deduplicate
    configs = list(dict.fromkeys(configs))[:20]

    idx = 0
    for base_t, tight_t, trans_bars in configs:
        idx += 1
        cn = f"V6_E8_P{idx:03d}"
        attrs = V11_BASE_ATTRS + f"""    BASE_TRAIL = {base_t}
    TIGHT_TRAIL = {tight_t}
    TRANSITION_BARS = {trans_bars}
"""
        # Use custom_stoploss for time-adaptive trailing
        custom_sl_code = f"""
    use_custom_stoploss = True
    trailing_stop = False

    def custom_stoploss(self, pair, trade, current_time, current_rate, current_profit, after_fill, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.30:
            ratio = min(1.0, bars_held / {trans_bars})
            trail = self.BASE_TRAIL - ratio * (self.BASE_TRAIL - self.TIGHT_TRAIL)
            return -(current_profit - trail) / 5.0
        return -0.10 / 5.0
"""
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
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
        code_raw = (
            HEADER.format(doc=f"V6 E8 time-adaptive trail base={base_t} tight={tight_t} bars={trans_bars}")
            + build_class_open(cn, trailing_stop=False, extra_class_attrs=attrs)
            + custom_sl_code
            + indicators_v11_standard()
            + entry_code
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        # Fix: remove duplicate use_custom_stoploss from class_open
        code = code_raw.replace("    use_custom_stoploss = False\n", "", 1)
        save_strategy(cn, code, f"E8 trail base={base_t} tight={tight_t} bars={trans_bars}",
                       "group_e8_adaptive_trail", {"base_trail": base_t, "tight_trail": tight_t, "transition_bars": trans_bars})


# =============================================================================
# E9: DC周期自适应（用ADX选DC而非ATR）
# =============================================================================
def gen_e9_adx_dc():
    """E9: 用ADX强度选DC周期 — ADX高用短DC(趋势强),ADX低用长DC(等更大突破)，16组"""
    configs = []
    for dc_strong, dc_weak in [(10, 30), (12, 35), (14, 40), (10, 40)]:
        for adx_threshold in [25, 30, 35, 40]:
            configs.append((dc_strong, dc_weak, adx_threshold))

    idx = 0
    for dc_s, dc_w, adx_th in configs:
        idx += 1
        cn = f"V6_E9_P{idx:03d}"
        attrs = V11_BASE_ATTRS + f"""    DC_STRONG = {dc_s}
    DC_WEAK = {dc_w}
    ADX_DC_THRESHOLD = {adx_th}
"""
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
        use_strong = dataframe['adx'] > {adx_th}
        dc_s = dataframe['high'].rolling({dc_s}).max().shift(1)
        dc_w = dataframe['high'].rolling({dc_w}).max().shift(1)
        dataframe['dc_upper'] = np.where(use_strong, dc_s, dc_w)
        dc_low_s = dataframe['low'].rolling({dc_s}).min().shift(1)
        dc_low_w = dataframe['low'].rolling({dc_w}).min().shift(1)
        dataframe['dc_lower'] = np.where(use_strong, dc_low_s, dc_low_w)
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
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * self.ATR_MULT)) &
            (dataframe['adx'] > self.ADX_MIN) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_adx_adaptive'
        return dataframe
"""
        code = (
            HEADER.format(doc=f"V6 E9 ADX-DC dc_strong={dc_s} dc_weak={dc_w} adx_th={adx_th}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + ind_code
            + entry_code
            + exit_trend_empty()
            + custom_exit_v11()
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"E9 ADX-DC s={dc_s} w={dc_w} adx={adx_th}",
                       "group_e9_adx_dc", {"dc_strong": dc_s, "dc_weak": dc_w, "adx_threshold": adx_th})


# =============================================================================
# E10: 多级阶梯止盈（分级锁利润）
# =============================================================================
def gen_e10_stair_tp():
    """E10: 阶梯止盈 — 达到不同利润水平后锁住部分利润，18组"""
    configs = []
    for tp1_level, tp1_lock in [(0.05, 0.02), (0.08, 0.03), (0.10, 0.04)]:
        for tp2_level, tp2_lock in [(0.15, 0.08), (0.20, 0.10), (0.20, 0.12)]:
            for tp3_level in [0.30, 0.40]:
                configs.append((tp1_level, tp1_lock, tp2_level, tp2_lock, tp3_level))
    configs = configs[:18]

    idx = 0
    for tp1_lv, tp1_lk, tp2_lv, tp2_lk, tp3_lv in configs:
        idx += 1
        cn = f"V6_E10_P{idx:03d}"
        attrs = V11_BASE_ATTRS + f"""    TP1_LEVEL = {tp1_lv}
    TP1_LOCK = {tp1_lk}
    TP2_LEVEL = {tp2_lv}
    TP2_LOCK = {tp2_lk}
    TP3_LEVEL = {tp3_lv}
"""
        exit_code = f"""
    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
        max_profit = trade.calc_profit_ratio(trade.max_rate)
        if max_profit >= {tp3_lv} and current_profit < max_profit * 0.5:
            return "stair_tp3"
        if max_profit >= {tp2_lv} and current_profit < {tp2_lk}:
            return "stair_tp2"
        if max_profit >= {tp1_lv} and current_profit < {tp1_lk}:
            return "stair_tp1"
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
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
        code = (
            HEADER.format(doc=f"V6 E10 stair TP tp1={tp1_lv}/{tp1_lk} tp2={tp2_lv}/{tp2_lk} tp3={tp3_lv}")
            + build_class_open(cn, extra_class_attrs=attrs)
            + indicators_v11_standard()
            + entry_code
            + exit_trend_empty()
            + exit_code
            + FOOTER_CONFIRM
        )
        save_strategy(cn, code, f"E10 TP1={tp1_lv}/{tp1_lk} TP2={tp2_lv}/{tp2_lk} TP3={tp3_lv}",
                       "group_e10_stair_tp", {"tp1": [tp1_lv, tp1_lk], "tp2": [tp2_lv, tp2_lk], "tp3": tp3_lv})


# =============================================================================
# E11: EMA交叉退出（趋势反转时退出）
# =============================================================================
def gen_e11_ema_exit():
    """E11: EMA交叉退出 — 持仓中EMA21<EMA55时退出，12组"""
    idx = 0
    for min_bars in [8, 16, 24]:
        for min_profit in [-0.03, -0.01, 0.01, 0.03]:
            idx += 1
            cn = f"V6_E11_P{idx:03d}"
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
        if bars_held >= {min_bars} and current_profit > {min_profit}:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) > 0:
                last = dataframe.iloc[-1]
                if last['ema21'] < last['ema55']:
                    return "ema_cross_exit"
        if bars_held >= self.MAX_BARS and current_profit < self.TIMEOUT_LOSS_THRESHOLD:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None
"""
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
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
            code = (
                HEADER.format(doc=f"V6 E11 EMA exit bars={min_bars} profit={min_profit}")
                + build_class_open(cn, extra_class_attrs=attrs)
                + indicators_v11_standard()
                + entry_code
                + exit_trend_empty()
                + exit_code
                + FOOTER_CONFIRM
            )
            save_strategy(cn, code, f"E11 EMA exit bars={min_bars} profit={min_profit}",
                          "group_e11_ema_exit", {"type": "ema_cross", "min_bars": min_bars, "min_profit": min_profit})


# =============================================================================
# F1: 基线对照
# =============================================================================
def gen_f1_baseline():
    """F1: CryptoV11 基线对照"""
    cn = "V6_F1_P001"
    attrs = V11_BASE_ATTRS
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
            ({ENTRY_LONG_V11})
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe
"""
    code = (
        HEADER.format(doc="V6 F1 CryptoV11 baseline")
        + build_class_open(cn, extra_class_attrs=attrs)
        + indicators_v11_standard()
        + entry_code
        + exit_trend_empty()
        + custom_exit_v11()
        + FOOTER_CONFIRM
    )
    save_strategy(cn, code, "F1 CryptoV11 baseline", "group_f1_baseline", {"variant": "v11_baseline"})


# =============================================================================
# Main
# =============================================================================
def main():
    global experiments, _existing_classnames
    experiments = []
    _existing_classnames = set()

    gen_e1_short()
    gen_e2_adx_scan()
    gen_e3_pullback()
    gen_e4_exit_signals()
    gen_e5_adaptive_leverage()
    gen_e6_mtf_dc()
    gen_e7_dynamic_atr_mult()
    gen_e8_time_adaptive_exit()
    gen_e9_adx_dc()
    gen_e10_stair_tp()
    gen_e11_ema_exit()
    gen_f1_baseline()

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
