"""Multi-Timeframe Variant - 4H=all ADX4H>25 RSI4H(45-100)"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)

class V3_MTF_all_25_45_100(IStrategy):
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
    minimal_roi = {"0": 0.99}
    order_types = {"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    CONFIRM_4H = "all"
    ADX_4H_MIN = 25
    RSI_4H_MIN = 45
    RSI_4H_MAX = 100
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
