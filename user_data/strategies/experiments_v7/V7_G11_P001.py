"""V7 G11 dynamic timeout loss=32 win=96 th=-0.02"""
from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
import numpy as np
import talib.abstract as ta
import logging
logger = logging.getLogger(__name__)
class V7_G11_P001(IStrategy):
    INTERFACE_VERSION = 3
    timeframe = '15m'
    can_short = True
    startup_candle_count = 400
    stoploss = -0.1
    use_custom_stoploss = False
    trailing_stop = True
    trailing_stop_positive = 0.03
    trailing_stop_positive_offset = 0.3
    trailing_only_offset_is_reached = True
    minimal_roi = {"0": 0.99}
    order_types = {"entry": "limit", "exit": "limit", "stoploss": "market", "stoploss_on_exchange": True}

    def leverage(self, pair, current_time, current_rate, proposed_leverage, max_leverage, entry_tag, side, **kwargs):
        return 5.0

    ADX_MIN = 28
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
            (dataframe['macdhist'] > 0) & (dataframe['macdhist'] > dataframe['macdhist'].shift(1))
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
        if bars_held >= 40 and current_profit < -0.04:
            return "stair_late"
        if bars_held >= 20 and current_profit < -0.06:
            return "stair_mid"
        if bars_held >= 32 and current_profit < -0.02:
            return "timeout_loss_dyn"
        if bars_held >= 96 and current_profit < 0.01:
            return "timeout_neutral"
        if bars_held >= 96 * 2:
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
