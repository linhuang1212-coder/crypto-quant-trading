"""
生成降风险优化实验的策略变体：
  - 措施1: 杠杆 3x vs 5x（基线）
  - 措施2: DAILY_MAX_LOSSES 2/3/4（基线）
  - 措施3: 阶梯止损（多种参数组合）
  - 组合: 最优杠杆 + 最优限损 + 阶梯止损
"""
import os
import json

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'strategies', 'experiments')
os.makedirs(OUTPUT_DIR, exist_ok=True)

TEMPLATE = '''
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging

logger = logging.getLogger(__name__)

class {class_name}(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400

    stoploss = -0.10
    use_custom_stoploss = False

    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.30
    trailing_only_offset_is_reached = True

    minimal_roi = {{"0": 0.99}}

    order_types = {{
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": True,
    }}

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return {leverage}

    ADX_MIN  = 28
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = {daily_max_losses}

    @informative('4h')
    def populate_indicators_4h(self, dataframe, metadata):
        dataframe['ema21'] = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55'] = ta.EMA(dataframe, timeperiod=55)
        return dataframe

    def populate_indicators(self, dataframe, metadata):
        dataframe['ema21']  = ta.EMA(dataframe, timeperiod=21)
        dataframe['ema55']  = ta.EMA(dataframe, timeperiod=55)
        dataframe['ema200'] = ta.EMA(dataframe, timeperiod=200)
        dataframe['adx'] = ta.ADX(dataframe, timeperiod=14)
        dataframe['plus_di'] = ta.PLUS_DI(dataframe, timeperiod=14)
        dataframe['minus_di'] = ta.MINUS_DI(dataframe, timeperiod=14)
        dataframe['adx_rising'] = dataframe['adx'] > dataframe['adx'].shift(2)
        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)
        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)
        return dataframe

    def populate_entry_trend(self, dataframe, metadata):
        dataframe['enter_long']  = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag']   = ''

        long_conditions = (
            (dataframe['close'] > dataframe['dc_upper']) &
            ((dataframe['close'] - dataframe['dc_upper']) > (dataframe['atr'] * 0.6)) &
            (dataframe['adx'] > self.ADX_MIN) &
            (dataframe['adx_rising']) &
            (dataframe['plus_di'] > dataframe['minus_di']) &
            (dataframe['ema21'] > dataframe['ema55']) &
            (dataframe['ema55'] > dataframe['ema200']) &
            (dataframe['ema21_4h'] > dataframe['ema55_4h'])
        )
        dataframe.loc[long_conditions, 'enter_long'] = 1
        dataframe.loc[long_conditions, 'enter_tag']  = 'dc_long'
        return dataframe

    def populate_exit_trend(self, dataframe, metadata):
        dataframe['exit_long']  = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair, trade, current_time, current_rate, current_profit, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))

        if current_profit >= 0.40:
            return "tp_big"

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return None

{stair_exit}

        if bars_held >= self.MAX_BARS and current_profit < -0.02:
            return "timeout_loss"

        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"

        return None

    def confirm_trade_entry(self, pair, order_type, amount, rate, time_in_force,
                            current_time, entry_tag, side, **kwargs):
        closed_trades = Trade.get_trades_proxy(pair=pair, is_open=False)
        if closed_trades:
            last_trade = closed_trades[-1]
            if last_trade.exit_reason == 'stop_loss':
                cooldown_secs = self.COOLDOWN_BARS * 15 * 60
                if (current_time - last_trade.close_date_utc).total_seconds() < cooldown_secs:
                    return False

        from datetime import timezone
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

NO_STAIR = "        pass  # no stair exit"

strategies = []

# --- 措施1: 杠杆对比 ---
for lev in [3.0, 4.0]:
    name = f"Risk_Lev{int(lev)}"
    code = TEMPLATE.format(
        class_name=name, leverage=lev, daily_max_losses=4, stair_exit=NO_STAIR
    )
    path = os.path.join(OUTPUT_DIR, f"{name}.py")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    strategies.append({"name": name, "group": "leverage", "params": f"lev={int(lev)}"})

# --- 措施2: DAILY_MAX_LOSSES 对比 ---
for dml in [2, 3]:
    name = f"Risk_DML{dml}"
    code = TEMPLATE.format(
        class_name=name, leverage=5.0, daily_max_losses=dml, stair_exit=NO_STAIR
    )
    path = os.path.join(OUTPUT_DIR, f"{name}.py")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    strategies.append({"name": name, "group": "daily_max_losses", "params": f"dml={dml}"})

# --- 措施3: 阶梯止损 ---
stair_configs = [
    # (mid_bars, mid_sl, late_bars, late_sl, label)
    (16, -0.05, 32, -0.03, "S1"),  # 标准阶梯
    (16, -0.06, 32, -0.04, "S2"),  # 宽松一档
    (16, -0.04, 32, -0.02, "S3"),  # 激进收紧
    (12, -0.05, 24, -0.03, "S4"),  # 更早触发
    (20, -0.06, 40, -0.04, "S5"),  # 更晚触发
    (16, -0.07, 32, -0.05, "S6"),  # 最宽松
    (16, -0.05, 32, -0.03, "S7_lev3"),  # 标准阶梯 + 3x杠杆
]

for i, (mid_b, mid_sl, late_b, late_sl, label) in enumerate(stair_configs):
    lev = 3.0 if "lev3" in label else 5.0
    stair_code = f"""        # stair_exit: {mid_b}bars>{mid_sl}, {late_b}bars>{late_sl}
        if bars_held >= {late_b} and current_profit < {late_sl}:
            return "stair_late"
        if bars_held >= {mid_b} and current_profit < {mid_sl}:
            return "stair_mid"
"""
    name = f"Risk_Stair_{label}"
    code = TEMPLATE.format(
        class_name=name, leverage=lev, daily_max_losses=4, stair_exit=stair_code
    )
    path = os.path.join(OUTPUT_DIR, f"{name}.py")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(code)
    strategies.append({"name": name, "group": "stair_exit",
                       "params": f"mid={mid_b}b/{mid_sl},late={late_b}b/{late_sl},lev={lev}"})

# --- 组合: 3x杠杆 + DML2 ---
name = "Risk_Combo_Lev3_DML2"
code = TEMPLATE.format(
    class_name=name, leverage=3.0, daily_max_losses=2, stair_exit=NO_STAIR
)
path = os.path.join(OUTPUT_DIR, f"{name}.py")
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
strategies.append({"name": name, "group": "combo", "params": "lev=3,dml=2"})

# --- 组合: 3x杠杆 + DML2 + 阶梯止损S1 ---
stair_s1 = """        # stair_exit: 16bars>-0.05, 32bars>-0.03
        if bars_held >= 32 and current_profit < -0.03:
            return "stair_late"
        if bars_held >= 16 and current_profit < -0.05:
            return "stair_mid"
"""
name = "Risk_Combo_Full"
code = TEMPLATE.format(
    class_name=name, leverage=3.0, daily_max_losses=2, stair_exit=stair_s1
)
path = os.path.join(OUTPUT_DIR, f"{name}.py")
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
strategies.append({"name": name, "group": "combo", "params": "lev=3,dml=2,stair=S1"})

# --- 组合: 3x杠杆 + DML3 + 阶梯止损S1 ---
name = "Risk_Combo_Full_DML3"
code = TEMPLATE.format(
    class_name=name, leverage=3.0, daily_max_losses=3, stair_exit=stair_s1
)
path = os.path.join(OUTPUT_DIR, f"{name}.py")
with open(path, 'w', encoding='utf-8') as f:
    f.write(code)
strategies.append({"name": name, "group": "combo", "params": "lev=3,dml=3,stair=S1"})

manifest_path = os.path.join(os.path.dirname(__file__), 'risk_experiment_manifest.json')
with open(manifest_path, 'w') as f:
    json.dump(strategies, f, indent=2)

print(f"Generated {len(strategies)} strategies")
for s in strategies:
    print(f"  [{s['group']}] {s['name']} -> {s['params']}")
