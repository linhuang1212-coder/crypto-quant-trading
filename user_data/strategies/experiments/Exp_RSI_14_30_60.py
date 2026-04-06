"""RSI Oversold + Trend - RSI(14) Entry<30 Exit>60"""
from freqtrade.strategy import IStrategy, informative
from pandas import DataFrame
import talib.abstract as ta
import logging

logger = logging.getLogger(__name__)

class Exp_RSI_14_30_60(IStrategy):
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
    minimal_roi = {"0": 0.99}
    order_types = {
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    RSI_PERIOD = 14
    RSI_ENTRY = 30
    RSI_EXIT = 60

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
