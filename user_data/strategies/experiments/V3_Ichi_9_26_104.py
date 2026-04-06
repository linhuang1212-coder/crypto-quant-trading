"""Ichimoku Cloud Breakout - Ichimoku(9/26/104)"""
from freqtrade.strategy import IStrategy, informative
from pandas import DataFrame
import talib.abstract as ta
import numpy as np
import logging
logger = logging.getLogger(__name__)

class V3_Ichi_9_26_104(IStrategy):
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

    TENKAN = 9
    KIJUN = 26
    SENKOU_B = 104

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
