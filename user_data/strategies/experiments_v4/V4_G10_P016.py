"""V4 G10 Stoch K=14 D=5 th=80 stair=False"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import numpy as np
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)
class V4_G10_P016(IStrategy):
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
    minimal_roi = {"0": 0.99}
    order_types = {"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    ADX_MIN = 28
    ATR_MULT = 0.6
    DC_PERIOD = 20
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4
    TP_BIG = 0.40
    STOCH_K = 14
    STOCH_D = 5
    STOCH_TH = 80

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
        st = ta.STOCH(dataframe, fastk_period=self.STOCH_K, slowk_period=3, slowd_period=self.STOCH_D)
        dataframe['slowk'] = st['slowk']
        dataframe['slowd'] = st['slowd']
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
            (dataframe['ema21_4h'] > dataframe['ema55_4h']) &
            ((dataframe['slowk'] > self.STOCH_TH))
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
