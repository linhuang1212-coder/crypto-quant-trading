"""
8-Hour Experiment Matrix Generator
自动生成 120+ 策略变体文件，覆盖：
  1. CryptoV10 参数网格扫描（核心参数 one-at-a-time）
  2. 退出策略变体
  3. 全新策略原型（均值回归、RSI、MACD、Keltner、双均线）
  4. 品种扩展扫描
"""
import os
import json
import itertools

STRATEGY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "strategies")
EXPERIMENT_DIR = os.path.join(STRATEGY_DIR, "experiments")
os.makedirs(EXPERIMENT_DIR, exist_ok=True)

INIT_FILE = os.path.join(EXPERIMENT_DIR, "__init__.py")
if not os.path.exists(INIT_FILE):
    with open(INIT_FILE, "w") as f:
        f.write("")

experiments = []

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 1: CryptoV10 参数 one-at-a-time 扫描
# 基线：ADX=28, DC=20, ATR_MULT=0.5, TRAIL_OFFSET=0.30, COOLDOWN=24
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CRYPTOV10_TEMPLATE = '''"""Auto-generated experiment: {name}"""
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
    trailing_stop_positive = {trail_positive}
    trailing_stop_positive_offset = {trail_offset}
    trailing_only_offset_is_reached = True

    minimal_roi = {{"0": 0.99}}
    order_types = {{
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
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
        dataframe['ema21']  = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55']  = ta.EMA(dataframe, timeperiod=55)
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
            (dataframe['adx'] > self.ADX_MIN) &
            (dataframe['adx_rising']) &
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

    def confirm_trade_entry(self, pair, order_type, amount, rate,
                            time_in_force, current_time, entry_tag, side, **kwargs):
        closed_trades = Trade.get_trades_proxy(pair=pair, is_open=False)
        if closed_trades:
            last_trade = closed_trades[-1]
            if last_trade.exit_reason == 'stop_loss':
                cooldown_secs = self.COOLDOWN_BARS * 15 * 60
                if (current_time - last_trade.close_date_utc).total_seconds() < cooldown_secs:
                    return False
        today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        today_losses = [
            t for t in Trade.get_trades_proxy(is_open=False)
            if t.close_date_utc and t.close_date_utc >= today_start
            and t.exit_reason == 'stop_loss'
        ]
        if len(today_losses) >= self.DAILY_MAX_LOSSES:
            return False
        return True
'''

DEFAULTS = dict(
    stoploss=-0.10, trail_positive=0.10, trail_offset=0.30,
    leverage=5.0, adx_min=28, dc_period=20, atr_mult=0.5,
    max_bars=64, cooldown_bars=24, tp_big=0.40,
)

def make_cryptov10_variant(name, classname, overrides):
    params = {**DEFAULTS, **overrides}
    code = CRYPTOV10_TEMPLATE.format(name=name, classname=classname, **params)
    filepath = os.path.join(EXPERIMENT_DIR, f"{classname}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": name, "strategy": classname, "group": "param_scan", "params": overrides})

# --- ADX threshold scan ---
for adx in [20, 22, 24, 26, 30, 32, 36]:
    make_cryptov10_variant(f"ADX={adx}", f"Exp_ADX_{adx}", {"adx_min": adx})

# --- Donchian period scan ---
for dc in [10, 14, 16, 18, 25, 30, 40]:
    make_cryptov10_variant(f"DC={dc}", f"Exp_DC_{dc}", {"dc_period": dc})

# --- ATR multiplier scan ---
for atr_m in [0.0, 0.2, 0.3, 0.4, 0.6, 0.7, 0.8, 1.0, 1.2, 1.5]:
    atr_str = str(atr_m).replace(".", "")
    make_cryptov10_variant(f"ATR_MULT={atr_m}", f"Exp_ATR_{atr_str}", {"atr_mult": atr_m})

# --- Trailing offset scan ---
for offset in [0.15, 0.20, 0.25, 0.35, 0.40, 0.45, 0.50]:
    off_str = str(offset).replace(".", "")
    make_cryptov10_variant(f"TRAIL_OFF={offset}", f"Exp_Trail_{off_str}", {"trail_offset": offset})

# --- Trailing positive scan ---
for tp in [0.03, 0.05, 0.08, 0.12, 0.15]:
    tp_str = str(tp).replace(".", "")
    make_cryptov10_variant(f"TRAIL_POS={tp}", f"Exp_TrailPos_{tp_str}", {"trail_positive": tp})

# --- Stoploss scan ---
for sl in [-0.06, -0.08, -0.12, -0.15, -0.20]:
    sl_str = str(sl).replace("-", "").replace(".", "")
    make_cryptov10_variant(f"SL={sl}", f"Exp_SL_{sl_str}", {"stoploss": sl})

# --- Cooldown scan ---
for cd in [0, 8, 12, 16, 36, 48]:
    make_cryptov10_variant(f"COOLDOWN={cd}", f"Exp_CD_{cd}", {"cooldown_bars": cd})

# --- Max bars (timeout) scan ---
for mb in [32, 48, 80, 96, 128]:
    make_cryptov10_variant(f"MAX_BARS={mb}", f"Exp_MB_{mb}", {"max_bars": mb})

# --- Take profit scan ---
for tp in [0.25, 0.30, 0.35, 0.50, 0.60, 0.80]:
    tp_str = str(tp).replace(".", "")
    make_cryptov10_variant(f"TP_BIG={tp}", f"Exp_TP_{tp_str}", {"tp_big": tp})

# --- Leverage scan ---
for lev in [2.0, 3.0, 4.0, 6.0, 7.0, 8.0, 10.0]:
    lev_str = str(int(lev))
    make_cryptov10_variant(f"LEV={lev}", f"Exp_Lev_{lev_str}", {"leverage": lev})

# --- 2D combos: best candidates (small grid) ---
for adx, atr_m in [(24, 0.3), (24, 0.7), (26, 0.3), (26, 0.5), (30, 0.3), (30, 0.7), (32, 0.5)]:
    atr_str = str(atr_m).replace(".", "")
    make_cryptov10_variant(f"ADX={adx}_ATR={atr_m}", f"Exp_2D_ADX{adx}_ATR{atr_str}",
                           {"adx_min": adx, "atr_mult": atr_m})

for offset, sl in [(0.25, -0.08), (0.25, -0.12), (0.35, -0.08), (0.35, -0.12), (0.40, -0.08)]:
    off_str = str(offset).replace(".", "")
    sl_str = str(sl).replace("-", "").replace(".", "")
    make_cryptov10_variant(f"TRAIL={offset}_SL={sl}", f"Exp_2D_Trail{off_str}_SL{sl_str}",
                           {"trail_offset": offset, "stoploss": sl})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP 2: 全新策略原型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# --- Bollinger Band Mean Reversion ---
BB_TEMPLATE = '''"""Bollinger Band Mean Reversion - {name}"""
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
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.15
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    BB_PERIOD = {bb_period}
    BB_STD = {bb_std}
    RSI_PERIOD = {rsi_period}
    RSI_OVERSOLD = {rsi_oversold}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        bb = ta.BBANDS(dataframe, timeperiod=self.BB_PERIOD, nbdevup=self.BB_STD, nbdevdn=self.BB_STD)
        dataframe['bb_lower'] = bb['lowerband']
        dataframe['bb_middle'] = bb['middleband']
        dataframe['bb_upper'] = bb['upperband']
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.RSI_PERIOD)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        long_conditions = (
            (dataframe['close'] < dataframe['bb_lower']) &
            (dataframe['rsi'] < self.RSI_OVERSOLD) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'bb_bounce'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        long_exit = (dataframe['close'] > dataframe['bb_middle'])
        dataframe.loc[long_exit, 'exit_long'] = 1
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.20:
            return "tp_big"
        if bars_held >= 64 and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= 128:
            return "timeout_extended"
        return None
'''

for bb_p, bb_s, rsi_p, rsi_os, sl in [
    (20, 2.0, 14, 30, -0.10),
    (20, 2.0, 14, 25, -0.10),
    (20, 2.5, 14, 30, -0.10),
    (20, 2.0, 14, 35, -0.08),
    (30, 2.0, 14, 30, -0.10),
    (20, 1.5, 14, 35, -0.10),
    (20, 2.0, 21, 30, -0.10),
    (20, 2.0, 14, 30, -0.06),
    (40, 2.0, 14, 25, -0.10),
]:
    bb_s_str = str(bb_s).replace(".", "")
    sl_str = str(sl).replace("-", "").replace(".", "")
    cn = f"Exp_BB_{bb_p}_{bb_s_str}_RSI{rsi_os}_SL{sl_str}"
    nm = f"BB(p={bb_p},std={bb_s}) RSI<{rsi_os} SL={sl}"
    code = BB_TEMPLATE.format(name=nm, classname=cn, bb_period=bb_p, bb_std=bb_s,
                              rsi_period=rsi_p, rsi_oversold=rsi_os, stoploss=sl)
    filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": nm, "strategy": cn, "group": "bollinger_band", "params": {
        "bb_period": bb_p, "bb_std": bb_s, "rsi_oversold": rsi_os, "stoploss": sl}})


# --- MACD Crossover ---
MACD_TEMPLATE = '''"""MACD Crossover Strategy - {name}"""
from freqtrade.strategy import IStrategy, informative
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
    trailing_stop_positive = 0.08
    trailing_stop_positive_offset = 0.25
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    MACD_FAST = {macd_fast}
    MACD_SLOW = {macd_slow}
    MACD_SIGNAL = {macd_signal}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        macd = ta.MACD(dataframe, fastperiod=self.MACD_FAST, slowperiod=self.MACD_SLOW,
                       signalperiod=self.MACD_SIGNAL)
        dataframe['macd'] = macd['macd']
        dataframe['macdsignal'] = macd['macdsignal']
        dataframe['macdhist'] = macd['macdhist']
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        long_conditions = (
            (dataframe['macd'] > dataframe['macdsignal']) &
            (dataframe['macd'].shift(1) <= dataframe['macdsignal'].shift(1)) &
            (dataframe['macd'] > 0) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'macd_cross'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (
            (dataframe['macd'] < dataframe['macdsignal']) &
            (dataframe['macd'].shift(1) >= dataframe['macdsignal'].shift(1))
        )
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

for fast, slow, sig in [(8, 21, 5), (12, 26, 9), (8, 17, 9), (5, 13, 5), (12, 26, 5), (8, 26, 9)]:
    cn = f"Exp_MACD_{fast}_{slow}_{sig}"
    nm = f"MACD({fast},{slow},{sig})"
    code = MACD_TEMPLATE.format(name=nm, classname=cn, macd_fast=fast, macd_slow=slow, macd_signal=sig)
    filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": nm, "strategy": cn, "group": "macd", "params": {
        "fast": fast, "slow": slow, "signal": sig}})


# --- Keltner Channel Breakout ---
KELTNER_TEMPLATE = '''"""Keltner Channel Breakout - {name}"""
from freqtrade.strategy import IStrategy, informative
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
    order_types = {{
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    KC_PERIOD = {kc_period}
    KC_MULT = {kc_mult}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema_kc'] = ta.EMA(dataframe, timeperiod=self.KC_PERIOD)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=self.KC_PERIOD)
        dataframe['kc_upper'] = dataframe['ema_kc'] + self.KC_MULT * dataframe['atr']
        dataframe['kc_lower'] = dataframe['ema_kc'] - self.KC_MULT * dataframe['atr']
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        long_conditions = (
            (dataframe['close'] > dataframe['kc_upper']) &
            (dataframe['close'].shift(1) <= dataframe['kc_upper'].shift(1)) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'kc_break'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (dataframe['close'] < dataframe['ema_kc'])
        dataframe.loc[exit_cond, 'exit_long'] = 1
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
'''

for kc_p, kc_m in [(20, 1.5), (20, 2.0), (20, 2.5), (14, 1.5), (14, 2.0), (30, 2.0), (20, 3.0)]:
    kc_m_str = str(kc_m).replace(".", "")
    cn = f"Exp_KC_{kc_p}_{kc_m_str}"
    nm = f"Keltner({kc_p}, {kc_m}x ATR)"
    code = KELTNER_TEMPLATE.format(name=nm, classname=cn, kc_period=kc_p, kc_mult=kc_m)
    filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": nm, "strategy": cn, "group": "keltner", "params": {
        "kc_period": kc_p, "kc_mult": kc_m}})


# --- Dual EMA Crossover ---
EMA_CROSS_TEMPLATE = '''"""Dual EMA Crossover - {name}"""
from freqtrade.strategy import IStrategy, informative
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
    order_types = {{
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    EMA_FAST = {ema_fast}
    EMA_SLOW = {ema_slow}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema_fast'] = ta.EMA(dataframe, timeperiod=self.EMA_FAST)
        dataframe['ema_slow'] = ta.EMA(dataframe, timeperiod=self.EMA_SLOW)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        long_conditions = (
            (dataframe['ema_fast'] > dataframe['ema_slow']) &
            (dataframe['ema_fast'].shift(1) <= dataframe['ema_slow'].shift(1)) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'ema_cross'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (
            (dataframe['ema_fast'] < dataframe['ema_slow']) &
            (dataframe['ema_fast'].shift(1) >= dataframe['ema_slow'].shift(1))
        )
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

for fast, slow in [(8, 21), (10, 30), (13, 34), (21, 55), (5, 13), (8, 34), (13, 55)]:
    cn = f"Exp_EMA_{fast}_{slow}"
    nm = f"EMA Cross({fast}/{slow})"
    code = EMA_CROSS_TEMPLATE.format(name=nm, classname=cn, ema_fast=fast, ema_slow=slow)
    filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": nm, "strategy": cn, "group": "ema_cross", "params": {
        "ema_fast": fast, "ema_slow": slow}})


# --- RSI + EMA Trend ---
RSI_TEMPLATE = '''"""RSI Oversold + Trend - {name}"""
from freqtrade.strategy import IStrategy, informative
from pandas import DataFrame
import talib.abstract as ta
import logging

logger = logging.getLogger(__name__)

class {classname}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400

    stoploss = -0.08
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.05
    trailing_stop_positive_offset = 0.15
    trailing_only_offset_is_reached = True
    minimal_roi = {{"0": 0.99}}
    order_types = {{
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    RSI_PERIOD = {rsi_period}
    RSI_ENTRY = {rsi_entry}
    RSI_EXIT = {rsi_exit}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['rsi'] = ta.RSI(dataframe, timeperiod=self.RSI_PERIOD)
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        long_conditions = (
            (dataframe['rsi'] < self.RSI_ENTRY) &
            (dataframe['rsi'].shift(1) >= self.RSI_ENTRY) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['adx'] > 20) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'rsi_dip'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (dataframe['rsi'] > self.RSI_EXIT)
        dataframe.loc[exit_cond, 'exit_long'] = 1
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))
        if current_profit >= 0.30:
            return "tp_big"
        if bars_held >= 64 and current_profit < -0.02:
            return "timeout_loss"
        if bars_held >= 128:
            return "timeout_extended"
        return None
'''

for rsi_p, rsi_e, rsi_x in [(14, 30, 70), (14, 25, 75), (14, 35, 65), (21, 30, 70), (7, 25, 75), (14, 30, 60)]:
    cn = f"Exp_RSI_{rsi_p}_{rsi_e}_{rsi_x}"
    nm = f"RSI({rsi_p}) Entry<{rsi_e} Exit>{rsi_x}"
    code = RSI_TEMPLATE.format(name=nm, classname=cn, rsi_period=rsi_p, rsi_entry=rsi_e, rsi_exit=rsi_x)
    filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": nm, "strategy": cn, "group": "rsi_trend", "params": {
        "rsi_period": rsi_p, "rsi_entry": rsi_e, "rsi_exit": rsi_x}})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Save experiment manifest
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
manifest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "experiment_manifest.json")
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(experiments, f, indent=2, ensure_ascii=False)

print(f"Generated {len(experiments)} experiment strategy files in {EXPERIMENT_DIR}")
for group in set(e['group'] for e in experiments):
    count = len([e for e in experiments if e['group'] == group])
    print(f"  - {group}: {count} variants")
print(f"Manifest saved to {manifest_path}")
