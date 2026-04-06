"""
Extended Experiment Matrix Generator (V2)
在 V1 的 112 个实验基础上，追加更多实验到 manifest 中，目标 500+ 个实验。

新增内容：
  1. CryptoV10 多维网格（ADX × ATR × Trail）
  2. 品种级别扫描（每个品种单独回测）
  3. 更多新策略变体
  4. CryptoV10 + 不同 EMA 周期组合
  5. Donchian 突破变体（带 EMA 退出）
"""
import os
import json

STRATEGY_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "strategies")
EXPERIMENT_DIR = os.path.join(STRATEGY_DIR, "experiments")
os.makedirs(EXPERIMENT_DIR, exist_ok=True)

manifest_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "experiment_manifest.json")
experiments = json.load(open(manifest_path, encoding="utf-8"))
existing_strategies = {e["strategy"] for e in experiments}
new_count = 0

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
    EMA_FAST = {ema_fast}
    EMA_MID = {ema_mid}
    EMA_SLOW_P = {ema_slow}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema_f'] = ta.EMA(dataframe, timeperiod=self.EMA_FAST)
        dataframe['ema_m'] = ta.EMA(dataframe, timeperiod=self.EMA_MID)
        dataframe['ema_s'] = ta.EMA(dataframe, timeperiod=self.EMA_SLOW_P)
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
            (dataframe['ema_f'] > dataframe['ema_m']) &
            (dataframe['ema_m'] > dataframe['ema_s']) &
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
    ema_fast=21, ema_mid=55, ema_slow=200,
)

def make_variant(name, classname, overrides, group="param_scan_v2"):
    global new_count
    if classname in existing_strategies:
        return
    params = {**DEFAULTS, **overrides}
    code = CRYPTOV10_TEMPLATE.format(name=name, classname=classname, **params)
    filepath = os.path.join(EXPERIMENT_DIR, f"{classname}.py")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    experiments.append({"name": name, "strategy": classname, "group": group, "params": overrides})
    existing_strategies.add(classname)
    new_count += 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP A: 3D Grid (ADX × ATR × Trail Offset) — 60 combos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for adx in [24, 26, 28, 30, 32]:
    for atr_m in [0.3, 0.5, 0.7, 1.0]:
        for trail in [0.20, 0.25, 0.30]:
            atr_str = str(atr_m).replace(".", "")
            trail_str = str(trail).replace(".", "")
            cn = f"Exp_3D_A{adx}_T{atr_str}_O{trail_str}"
            nm = f"ADX={adx} ATR={atr_m} Trail={trail}"
            make_variant(nm, cn, {"adx_min": adx, "atr_mult": atr_m, "trail_offset": trail}, "grid_3d")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP B: EMA Periods scan
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for fast, mid, slow in [
    (10, 30, 100), (10, 30, 200), (13, 34, 200), (13, 55, 200),
    (21, 55, 100), (21, 55, 150), (21, 75, 200), (21, 100, 200),
    (8, 21, 100), (8, 21, 200), (34, 89, 200), (10, 55, 200),
    (15, 40, 150), (20, 50, 200), (25, 60, 200), (13, 34, 100),
]:
    cn = f"Exp_EMA_{fast}_{mid}_{slow}"
    nm = f"EMA({fast}/{mid}/{slow})"
    make_variant(nm, cn, {"ema_fast": fast, "ema_mid": mid, "ema_slow": slow}, "ema_periods")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP C: Stoploss × Leverage combos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for sl in [-0.06, -0.08, -0.10, -0.12, -0.15]:
    for lev in [3.0, 5.0, 7.0, 10.0]:
        sl_str = str(sl).replace("-", "").replace(".", "")
        lev_str = str(int(lev))
        cn = f"Exp_SL{sl_str}_Lev{lev_str}"
        nm = f"SL={sl} Lev={lev}"
        make_variant(nm, cn, {"stoploss": sl, "leverage": lev}, "sl_leverage")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP D: Donchian Period × ATR × DC combos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for dc in [14, 18, 20, 25, 30]:
    for atr_m in [0.0, 0.3, 0.5, 0.7]:
        atr_str = str(atr_m).replace(".", "")
        cn = f"Exp_DC{dc}_ATR{atr_str}"
        nm = f"DC={dc} ATR={atr_m}"
        make_variant(nm, cn, {"dc_period": dc, "atr_mult": atr_m}, "dc_atr")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP E: Trailing (positive × offset) combos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for tp in [0.03, 0.05, 0.08, 0.10, 0.12, 0.15]:
    for off in [0.15, 0.20, 0.25, 0.30, 0.35, 0.40]:
        if off > tp:
            tp_str = str(tp).replace(".", "")
            off_str = str(off).replace(".", "")
            cn = f"Exp_Tr{tp_str}_Off{off_str}"
            nm = f"TrailPos={tp} Offset={off}"
            make_variant(nm, cn, {"trail_positive": tp, "trail_offset": off}, "trailing_grid")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP F: Timeout × TP combos
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for mb in [32, 48, 64, 80, 96]:
    for tp in [0.30, 0.40, 0.50, 0.60]:
        tp_str = str(tp).replace(".", "")
        cn = f"Exp_MB{mb}_TP{tp_str}"
        nm = f"MaxBars={mb} TP={tp}"
        make_variant(nm, cn, {"max_bars": mb, "tp_big": tp}, "timeout_tp")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP G: "Best of" combos — combine best single-param values
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
for adx in [26, 28, 30]:
    for atr_m in [0.3, 0.5, 0.7]:
        for sl in [-0.08, -0.10, -0.12]:
            for trail in [0.25, 0.30, 0.35]:
                atr_str = str(atr_m).replace(".", "")
                sl_str = str(sl).replace("-", "").replace(".", "")
                trail_str = str(trail).replace(".", "")
                cn = f"Exp_Best_A{adx}_R{atr_str}_S{sl_str}_T{trail_str}"
                nm = f"ADX={adx} ATR={atr_m} SL={sl} Trail={trail}"
                make_variant(nm, cn, {
                    "adx_min": adx, "atr_mult": atr_m,
                    "stoploss": sl, "trail_offset": trail
                }, "best_combo")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP H: Stochastic + Donchian hybrid
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STOCH_TEMPLATE = '''"""Stochastic + Donchian Hybrid - {name}"""
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
    order_types = {{
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    STOCH_K = {stoch_k}
    STOCH_D = {stoch_d}
    STOCH_ENTRY = {stoch_entry}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        stoch = ta.STOCH(dataframe, fastk_period=self.STOCH_K, slowk_period=self.STOCH_D, slowd_period=3)
        dataframe['slowk'] = stoch['slowk']
        dataframe['slowd'] = stoch['slowd']
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['enter_long'] = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag'] = ''

        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            (dataframe['slowk'] > self.STOCH_ENTRY) &
            (dataframe['slowk'] > dataframe['slowd']) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'stoch_dc'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (dataframe['slowk'] < 80) & (dataframe['slowk'] < dataframe['slowd'])
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

for stoch_k, stoch_d, stoch_e in [
    (14, 3, 50), (14, 3, 60), (14, 3, 70), (14, 5, 50),
    (21, 3, 50), (21, 5, 60), (9, 3, 50), (9, 3, 60),
]:
    cn = f"Exp_Stoch_{stoch_k}_{stoch_d}_{stoch_e}"
    nm = f"Stoch({stoch_k},{stoch_d}) Entry>{stoch_e}"
    if cn not in existing_strategies:
        code = STOCH_TEMPLATE.format(name=nm, classname=cn, stoch_k=stoch_k, stoch_d=stoch_d, stoch_entry=stoch_e)
        filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        experiments.append({"name": nm, "strategy": cn, "group": "stoch_dc", "params": {
            "stoch_k": stoch_k, "stoch_d": stoch_d, "stoch_entry": stoch_e}})
        existing_strategies.add(cn)
        new_count += 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP I: CCI + Trend
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CCI_TEMPLATE = '''"""CCI Trend Strategy - {name}"""
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

    CCI_PERIOD = {cci_period}
    CCI_ENTRY = {cci_entry}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['cci'] = ta.CCI(dataframe, timeperiod=self.CCI_PERIOD)
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
            (dataframe['cci'] > self.CCI_ENTRY) &
            (dataframe['cci'].shift(1) <= self.CCI_ENTRY) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'cci_trend'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (dataframe['cci'] < 0)
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

for cci_p, cci_e in [(14, 100), (14, 50), (14, 150), (20, 100), (20, 50), (7, 100), (7, 50)]:
    cn = f"Exp_CCI_{cci_p}_{cci_e}"
    nm = f"CCI({cci_p}) Entry>{cci_e}"
    if cn not in existing_strategies:
        code = CCI_TEMPLATE.format(name=nm, classname=cn, cci_period=cci_p, cci_entry=cci_e)
        filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        experiments.append({"name": nm, "strategy": cn, "group": "cci_trend", "params": {
            "cci_period": cci_p, "cci_entry": cci_e}})
        existing_strategies.add(cn)
        new_count += 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP J: Williams %R
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WILLR_TEMPLATE = '''"""Williams %R Strategy - {name}"""
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

    WILLR_PERIOD = {willr_period}
    WILLR_ENTRY = {willr_entry}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['willr'] = ta.WILLR(dataframe, timeperiod=self.WILLR_PERIOD)
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
            (dataframe['willr'] > self.WILLR_ENTRY) &
            (dataframe['willr'].shift(1) <= self.WILLR_ENTRY) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'willr_trend'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (dataframe['willr'] < -80)
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

for wp, we in [(14, -20), (14, -30), (14, -40), (21, -20), (21, -30), (7, -20), (7, -30)]:
    we_str = str(abs(we))
    cn = f"Exp_WillR_{wp}_{we_str}"
    nm = f"WillR({wp}) Entry>{we}"
    if cn not in existing_strategies:
        code = WILLR_TEMPLATE.format(name=nm, classname=cn, willr_period=wp, willr_entry=we)
        filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        experiments.append({"name": nm, "strategy": cn, "group": "willr_trend", "params": {
            "willr_period": wp, "willr_entry": we}})
        existing_strategies.add(cn)
        new_count += 1


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GROUP K: SAR + Trend
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SAR_TEMPLATE = '''"""Parabolic SAR + Trend - {name}"""
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

    SAR_ACC = {sar_acc}
    SAR_MAX = {sar_max}

    @informative('4h')
    def populate_indicators_4h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['sar'] = ta.SAR(dataframe, acceleration=self.SAR_ACC, maximum=self.SAR_MAX)
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
            (dataframe['close'] > dataframe['sar']) &
            (dataframe['close'].shift(1) <= dataframe['sar'].shift(1)) &
            (dataframe['adx'] > 25) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['close'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag'] = 'sar_flip'
        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long'] = 0
        dataframe['exit_short'] = 0
        exit_cond = (dataframe['close'] < dataframe['sar'])
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

for sa, sm in [(0.02, 0.2), (0.01, 0.2), (0.02, 0.1), (0.01, 0.1), (0.03, 0.3), (0.02, 0.3)]:
    sa_str = str(sa).replace(".", "")
    sm_str = str(sm).replace(".", "")
    cn = f"Exp_SAR_{sa_str}_{sm_str}"
    nm = f"SAR(acc={sa}, max={sm})"
    if cn not in existing_strategies:
        code = SAR_TEMPLATE.format(name=nm, classname=cn, sar_acc=sa, sar_max=sm)
        filepath = os.path.join(EXPERIMENT_DIR, f"{cn}.py")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        experiments.append({"name": nm, "strategy": cn, "group": "sar_trend", "params": {
            "sar_acc": sa, "sar_max": sm}})
        existing_strategies.add(cn)
        new_count += 1


# Save updated manifest
with open(manifest_path, "w", encoding="utf-8") as f:
    json.dump(experiments, f, indent=2, ensure_ascii=False)

print(f"Added {new_count} new experiments (total now: {len(experiments)})")
for group in sorted(set(e['group'] for e in experiments)):
    count = len([e for e in experiments if e['group'] == group])
    print(f"  - {group}: {count}")
print(f"Estimated runtime: {len(experiments) * 50 / 60:.0f} minutes ({len(experiments) * 50 / 3600:.1f} hours)")
