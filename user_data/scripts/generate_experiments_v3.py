"""
V3 Experiment Generator — 全新方向，不与 V1/V2 重复
目标：~140 个实验，约 2 小时运行时间

新增方向：
  1. TrailPos=0.03 分年度验证（6 个年度段）
  2. 多时间框架变体（4H ADX/RSI 确认）
  3. Ichimoku Cloud 策略
  4. ATR 自适应止损（custom_exit 实现）
  5. 品种级别单独回测（4 品种 × 参数扫描）
  6. Donchian + RSI 入场过滤
  7. Donchian + Volume 放大确认
  8. 动态止盈（ATR-based TP）
  9. TrailPos=0.03 基线上再优化组合
"""
import os
import json

STRATEGY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "strategies")
EXPERIMENT_DIR = os.path.join(STRATEGY_DIR, "experiments")
os.makedirs(EXPERIMENT_DIR, exist_ok=True)

manifest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "experiment_manifest_v3.json")
experiments = []
existing = set()


def save_strategy(classname, code, name, group, params):
    if classname in existing:
        return
    filepath = os.path.join(EXPERIMENT_DIR, f"{classname}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": name, "strategy": classname, "group": group, "params": params})
    existing.add(classname)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 1: 多时间框架变体 — 4H 用 ADX/RSI 代替 EMA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MTF_TEMPLATE = '''"""Multi-Timeframe Variant - {name}"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = -0.10
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.10
    trailing_stop_positive_offset = 0.30
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    CONFIRM_4H = "{confirm_4h}"
    ADX_4H_MIN = {adx_4h_min}
    RSI_4H_MIN = {rsi_4h_min}
    RSI_4H_MAX = {rsi_4h_max}
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        base = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * 0.5)) &
            (dataframe['adx'] > 28) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200'])
        )

        if self.CONFIRM_4H == "ema":
            confirm = (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        elif self.CONFIRM_4H == "adx":
            confirm = (dataframe['adx_4h'] > self.ADX_4H_MIN) & (dataframe['plus_di_4h'] > dataframe['minus_di_4h'])
        elif self.CONFIRM_4H == "rsi":
            confirm = (dataframe['rsi_4h'] > self.RSI_4H_MIN) & (dataframe['rsi_4h'] < self.RSI_4H_MAX)
        elif self.CONFIRM_4H == "ema_adx":
            confirm = ((dataframe['ema21_4h'] > dataframe['ema55_4h']) & (dataframe['adx_4h'] > self.ADX_4H_MIN))
        elif self.CONFIRM_4H == "ema_rsi":
            confirm = ((dataframe['ema21_4h'] > dataframe['ema55_4h']) & (dataframe['rsi_4h'] > self.RSI_4H_MIN) & (dataframe['rsi_4h'] < self.RSI_4H_MAX))
        elif self.CONFIRM_4H == "all":
            confirm = ((dataframe['ema21_4h'] > dataframe['ema55_4h']) & (dataframe['adx_4h'] > self.ADX_4H_MIN) & (dataframe['rsi_4h'] > self.RSI_4H_MIN))
        elif self.CONFIRM_4H == "none":
            confirm = True
        else:
            confirm = (dataframe['ema21_4h'] > dataframe['ema55_4h'])

        dataframe.loc[base & confirm, 'enter_long'] = 1
        dataframe.loc[base & confirm, 'enter_tag'] = 'dc_long'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.40:
            return "tp_big"
        if bars_held >= 64 and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= 128:
            return "timeout_extended"
        return None

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

for confirm, adx_4h, rsi_min, rsi_max in [
    ("adx", 20, 0, 100), ("adx", 25, 0, 100), ("adx", 30, 0, 100),
    ("rsi", 0, 40, 70), ("rsi", 0, 45, 75), ("rsi", 0, 50, 80), ("rsi", 0, 35, 65),
    ("ema_adx", 20, 0, 100), ("ema_adx", 25, 0, 100),
    ("ema_rsi", 0, 40, 75), ("ema_rsi", 0, 50, 80),
    ("all", 20, 40, 100), ("all", 25, 45, 100),
    ("none", 0, 0, 100),
]:
    cn = f"V3_MTF_{confirm}_{adx_4h}_{rsi_min}_{rsi_max}"
    nm = f"4H={confirm} ADX4H>{adx_4h} RSI4H({rsi_min}-{rsi_max})"
    code = MTF_TEMPLATE.format(name=nm, classname=cn, confirm_4h=confirm, adx_4h_min=adx_4h, rsi_4h_min=rsi_min, rsi_4h_max=rsi_max)
    save_strategy(cn, code, nm, "mtf_variant", {"confirm_4h": confirm, "adx_4h_min": adx_4h, "rsi_4h_min": rsi_min, "rsi_4h_max": rsi_max})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 2: Donchian + RSI 入场过滤
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DC_RSI_TEMPLATE = '''"""Donchian + RSI Filter - {name}"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = -0.10
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.10
    trailing_stop_positive_offset = 0.30
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    RSI_MIN = {rsi_min}
    RSI_MAX = {rsi_max}
    RSI_PERIOD = {rsi_period}
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.RSI_PERIOD)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * 0.5)) &
            (dataframe['adx'] > 28) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['rsi'] > self.RSI_MIN) & (dataframe['rsi'] < self.RSI_MAX)
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_rsi_long'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.40:
            return "tp_big"
        if bars_held >= 64 and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= 128:
            return "timeout_extended"
        return None

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

for rsi_p, rsi_min, rsi_max in [
    (14, 40, 100), (14, 45, 100), (14, 50, 100), (14, 55, 100), (14, 60, 100),
    (14, 40, 75), (14, 40, 80), (14, 50, 80), (14, 50, 75),
    (7, 40, 100), (7, 50, 100), (7, 50, 80),
    (21, 40, 100), (21, 50, 100),
]:
    cn = f"V3_DCRSI_{rsi_p}_{rsi_min}_{rsi_max}"
    nm = f"DC+RSI({rsi_p}) {rsi_min}<RSI<{rsi_max}"
    code = DC_RSI_TEMPLATE.format(name=nm, classname=cn, rsi_min=rsi_min, rsi_max=rsi_max, rsi_period=rsi_p)
    save_strategy(cn, code, nm, "dc_rsi_filter", {"rsi_period": rsi_p, "rsi_min": rsi_min, "rsi_max": rsi_max})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 3: ATR 自适应止损/止盈（用 custom_exit 实现，绕开杠杆 bug）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ATR_SL_TEMPLATE = '''"""ATR Adaptive Exit - {name}"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = -0.25
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.10
    trailing_stop_positive_offset = 0.30
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    ATR_SL_MULT = {atr_sl_mult}
    ATR_TP_MULT = {atr_tp_mult}
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * 0.5)) &
            (dataframe['adx'] > 28) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return None
        current_atr = float(dataframe.iloc[-1]['atr'])
        entry_rate = trade.open_rate
        atr_pct = current_atr / entry_rate

        if current_profit <= -(atr_pct * self.ATR_SL_MULT):
            return "atr_stop"
        if current_profit >= (atr_pct * self.ATR_TP_MULT):
            return "atr_tp"
        if bars_held >= 64 and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= 128:
            return "timeout_extended"
        return None

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

for atr_sl, atr_tp in [
    (1.5, 3.0), (1.5, 4.0), (1.5, 5.0), (1.5, 6.0),
    (2.0, 3.0), (2.0, 4.0), (2.0, 5.0), (2.0, 6.0), (2.0, 8.0),
    (2.5, 4.0), (2.5, 5.0), (2.5, 6.0), (2.5, 8.0),
    (3.0, 5.0), (3.0, 6.0), (3.0, 8.0), (3.0, 10.0),
]:
    sl_str = str(atr_sl).replace(".", "")
    tp_str = str(atr_tp).replace(".", "")
    cn = f"V3_ATRSL_{sl_str}_{tp_str}"
    nm = f"ATR_SL={atr_sl}x ATR_TP={atr_tp}x"
    code = ATR_SL_TEMPLATE.format(name=nm, classname=cn, atr_sl_mult=atr_sl, atr_tp_mult=atr_tp)
    save_strategy(cn, code, nm, "atr_adaptive_exit", {"atr_sl_mult": atr_sl, "atr_tp_mult": atr_tp})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 4: Donchian + Volume 确认
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VOL_TEMPLATE = '''"""Donchian + Volume Confirmation - {name}"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = -0.10
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.10
    trailing_stop_positive_offset = 0.30
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    VOL_MULT = {vol_mult}
    VOL_PERIOD = {vol_period}
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['vol_ma'] = dataframe['volume'].rolling(self.VOL_PERIOD).mean()
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * 0.5)) &
            (dataframe['adx'] > 28) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['volume'] > dataframe['vol_ma'] * self.VOL_MULT)
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_vol_long'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.40:
            return "tp_big"
        if bars_held >= 64 and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= 128:
            return "timeout_extended"
        return None

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

for vol_p, vol_m in [
    (20, 1.2), (20, 1.5), (20, 2.0), (20, 2.5), (20, 3.0),
    (10, 1.5), (10, 2.0), (10, 2.5),
    (50, 1.5), (50, 2.0), (50, 2.5),
]:
    vm_str = str(vol_m).replace(".", "")
    cn = f"V3_Vol_{vol_p}_{vm_str}"
    nm = f"DC+Vol(p={vol_p}) >{vol_m}x avg"
    code = VOL_TEMPLATE.format(name=nm, classname=cn, vol_mult=vol_m, vol_period=vol_p)
    save_strategy(cn, code, nm, "dc_volume", {"vol_period": vol_p, "vol_mult": vol_m})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 5: Ichimoku Cloud 策略
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ICHI_TEMPLATE = '''"""Ichimoku Cloud Breakout - {name}"""
from freqtrade.strategy import IStrategy, informative
from pandas import DataFrame
import talib.abstract as ta
import numpy as np
import logging
logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = -0.10
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.10
    trailing_stop_positive_offset = 0.30
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    TENKAN = {tenkan}
    KIJUN = {kijun}
    SENKOU_B = {senkou_b}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        hi_t = dataframe['high'].rolling(self.TENKAN).max()
        lo_t = dataframe['low'].rolling(self.TENKAN).min()
        dataframe['tenkan'] = (hi_t + lo_t) / 2

        hi_k = dataframe['high'].rolling(self.KIJUN).max()
        lo_k = dataframe['low'].rolling(self.KIJUN).min()
        dataframe['kijun'] = (hi_k + lo_k) / 2

        dataframe['senkou_a'] = ((dataframe['tenkan'] + dataframe['kijun']) / 2).shift(self.KIJUN)

        hi_s = dataframe['high'].rolling(self.SENKOU_B).max()
        lo_s = dataframe['low'].rolling(self.SENKOU_B).min()
        dataframe['senkou_b'] = ((hi_s + lo_s) / 2).shift(self.KIJUN)

        dataframe['cloud_top'] = np.maximum(dataframe['senkou_a'], dataframe['senkou_b'])

        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['cloud_top']) &
            (dataframe['tenkan'] > dataframe['kijun']) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'ichi_break'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (dataframe['tenkan'] < dataframe['kijun'])
        dataframe.loc[exit_cond, 'exit_long'] = 1
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.40:
            return "tp_big"
        if bars_held >= 96 and current_profit < -0.02:
            return "timeout_loss"
        return None
'''

for t, k, s in [
    (9, 26, 52), (7, 22, 44), (13, 34, 68), (9, 26, 78),
    (20, 60, 120), (9, 26, 104), (5, 13, 26),
]:
    cn = f"V3_Ichi_{t}_{k}_{s}"
    nm = f"Ichimoku({t}/{k}/{s})"
    code = ICHI_TEMPLATE.format(name=nm, classname=cn, tenkan=t, kijun=k, senkou_b=s)
    save_strategy(cn, code, nm, "ichimoku", {"tenkan": t, "kijun": k, "senkou_b": s})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 6: TrailPos=0.03 基线上再优化（最优发现 + 其他参数调整）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
NEWBASE_TEMPLATE = '''"""New Baseline (TrailPos=0.03) + Optimization - {name}"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = {stoploss}
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = {trail_offset}
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return {leverage}

    ADX_MIN = {adx_min}
    DC_PERIOD = {dc_period}
    ATR_MULT = {atr_mult}
    MAX_BARS = {max_bars}
    COOLDOWN_BARS = {cooldown_bars}
    DAILY_MAX_LOSSES = 4
    TP_BIG = {tp_big}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

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
        return dataframe

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
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_long'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= self.TP_BIG:
            return "tp_big"
        if bars_held >= self.MAX_BARS and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"
        return None

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

NB_DEFAULTS = dict(stoploss=-0.10, trail_offset=0.30, leverage=5.0, adx_min=28,
                    dc_period=20, atr_mult=0.5, max_bars=64, cooldown_bars=24, tp_big=0.40)

def make_nb(name, classname, overrides):
    params = {**NB_DEFAULTS, **overrides}
    code = NEWBASE_TEMPLATE.format(name=name, classname=classname, **params)
    save_strategy(classname, code, name, "newbase_opt", overrides)

# ADX on new base
for adx in [24, 26, 30, 32]:
    make_nb(f"NB+ADX={adx}", f"V3_NB_ADX{adx}", {"adx_min": adx})

# ATR mult on new base
for am in [0.3, 0.4, 0.6, 0.7]:
    am_str = str(am).replace(".", "")
    make_nb(f"NB+ATR={am}", f"V3_NB_ATR{am_str}", {"atr_mult": am})

# Trail offset on new base
for off in [0.25, 0.35, 0.40, 0.50]:
    off_str = str(off).replace(".", "")
    make_nb(f"NB+Offset={off}", f"V3_NB_Off{off_str}", {"trail_offset": off})

# SL on new base
for sl in [-0.06, -0.08, -0.12, -0.15]:
    sl_str = str(sl).replace("-","").replace(".","")
    make_nb(f"NB+SL={sl}", f"V3_NB_SL{sl_str}", {"stoploss": sl})

# Leverage on new base
for lev in [3.0, 4.0, 7.0]:
    make_nb(f"NB+Lev={int(lev)}", f"V3_NB_Lev{int(lev)}", {"leverage": lev})

# TP on new base
for tp in [0.25, 0.30, 0.50, 0.60]:
    tp_str = str(tp).replace(".","")
    make_nb(f"NB+TP={tp}", f"V3_NB_TP{tp_str}", {"tp_big": tp})

# DC period on new base
for dc in [14, 16, 25, 30]:
    make_nb(f"NB+DC={dc}", f"V3_NB_DC{dc}", {"dc_period": dc})

# Cooldown on new base
for cd in [12, 36, 48]:
    make_nb(f"NB+CD={cd}", f"V3_NB_CD{cd}", {"cooldown_bars": cd})

# Best combos on new base
for adx, am, off in [(26, 0.5, 0.35), (28, 0.6, 0.35), (30, 0.5, 0.35), (28, 0.5, 0.40), (28, 0.5, 0.50), (26, 0.6, 0.40), (30, 0.6, 0.40)]:
    am_str = str(am).replace(".","")
    off_str = str(off).replace(".","")
    make_nb(f"NB+A{adx}_R{am}_O{off}", f"V3_NB_Combo_A{adx}R{am_str}O{off_str}", {"adx_min": adx, "atr_mult": am, "trail_offset": off})

# Best combos with lower SL
for sl, off, tp in [(-0.08, 0.35, 0.30), (-0.08, 0.40, 0.30), (-0.10, 0.35, 0.25), (-0.10, 0.40, 0.25), (-0.12, 0.35, 0.30)]:
    sl_str = str(sl).replace("-","").replace(".","")
    off_str = str(off).replace(".","")
    tp_str = str(tp).replace(".","")
    make_nb(f"NB+S{sl}_O{off}_T{tp}", f"V3_NB_SOT_{sl_str}{off_str}{tp_str}", {"stoploss": sl, "trail_offset": off, "tp_big": tp})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 7: Donchian + MFI (Money Flow Index — volume-weighted RSI)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MFI_TEMPLATE = '''"""Donchian + MFI Filter - {name}"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = -0.10
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.10
    trailing_stop_positive_offset = 0.30
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    MFI_MIN = {mfi_min}
    MFI_PERIOD = {mfi_period}
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['mfi'] = ta.MFI(dataframe, timeperiod=self.MFI_PERIOD)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''
        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * 0.5)) &
            (dataframe['adx'] > 28) & (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            (dataframe['mfi'] > self.MFI_MIN)
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'dc_mfi_long'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.40:
            return "tp_big"
        if bars_held >= 64 and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= 128:
            return "timeout_extended"
        return None

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

for mfi_p, mfi_min in [(14, 40), (14, 50), (14, 60), (14, 30), (7, 50), (7, 60), (21, 40), (21, 50)]:
    cn = f"V3_MFI_{mfi_p}_{mfi_min}"
    nm = f"DC+MFI({mfi_p})>{mfi_min}"
    code = MFI_TEMPLATE.format(name=nm, classname=cn, mfi_min=mfi_min, mfi_period=mfi_p)
    save_strategy(cn, code, nm, "dc_mfi", {"mfi_period": mfi_p, "mfi_min": mfi_min})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Save V3 manifest
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(experiments, f, indent=2, ensure_ascii=False)

print(f"Generated {len(experiments)} V3 experiments")
for group in sorted(set(e['group'] for e in experiments)):
    count = len([e for e in experiments if e['group'] == group])
    print(f"  - {group}: {count}")
print(f"Estimated runtime: {len(experiments) * 50 / 60:.0f} min ({len(experiments) * 50 / 3600:.1f} hours)")
print(f"Manifest: {manifest_path}")
