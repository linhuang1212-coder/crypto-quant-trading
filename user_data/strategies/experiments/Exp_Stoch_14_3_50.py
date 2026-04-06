"""Stochastic + Donchian Hybrid - Stoch(14,3) Entry>50"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import talib.abstract as ta
import logging

logger = logging.getLogger(__name__)

class Exp_Stoch_14_3_50(IStrategy):
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
    order_types = {
        "entry": "limit", "exit": "limit",
        "stoploss": "market", "stoploss_on_exchange": True,
    }

    def leverage(self, pair, current_time, current_rate, proposed_leverage,
                 max_leverage, entry_tag, side, **kwargs):
        return 5.0

    STOCH_K = 14
    STOCH_D = 3
    STOCH_ENTRY = 50

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
