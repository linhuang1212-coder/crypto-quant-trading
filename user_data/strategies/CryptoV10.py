"""
CryptoV10 Strategy - 15m Donchian 趋势突破 Long-Only
=============================================
核心配置：
  - 品种：BTC/USDT + ETH/USDT + SOL/USDT + ADA/USDT
  - 15m 时间框架 + 4H 多时间框架确认
  - Donchian 20 突破入场 + 8 个过滤条件（消融实验精简后）
  - trailing stop 0.03/0.30（利润跑到 30% 才开始追踪，3% 追踪距离）
  - 硬止损 -10% + 阶梯止损（20bars后亏>-6%离场，40bars后亏>-4%离场）
  - 5x 杠杆
  - 复利模式：40% tradable_balance_ratio

入场条件（精简后 8 个）：
  1. 价格突破 Donchian 20 上轨
  2. ATR 突破强度：(close - dc_upper) > atr * 0.6
  3. ADX > 28 且 ADX 上升
  4. +DI > -DI
  5. EMA21 > EMA55 > EMA200（多头排列）
  6. 4H EMA21 > 4H EMA55（多时间框架确认）

消融实验移除的冗余条件（2026-04-02 验证）：
  - DI 差值 > 5：与 +DI > -DI 完全重叠，移除后结果不变
  - EMA200 斜率 > 0：与三线排列完全重叠，移除后结果不变
  - OBV > OBV_EMA：完全冗余，移除后结果不变

回测（$1,000 本金，2020-2026）：
  $1,000 → $14,024（+1302%），CAGR ~53%，PF 1.46，Sortino 3.66
  最大回撤：13.1%  |  Walk-Forward 3窗口全部优于无阶梯基线

优化历史（2026-04-03 验证，530+ 实验）：
  - trailing_stop_positive: 0.10 → 0.03（Sharpe +0.23，影响最大的单一参数）
  - ATR 突破倍数: 0.5 → 0.6（PF 1.33→1.37，回撤 17.4%→15.3%）
  - 阶梯止损 S5: 20bars/-0.06 + 40bars/-0.04（PF 1.37→1.46，回撤 15.3%→13.1%）
"""

from freqtrade.strategy import IStrategy, informative
from freqtrade.persistence import Trade
from pandas import DataFrame
from datetime import datetime, timedelta, timezone
import talib.abstract as ta
import numpy as np
import logging
import os
import json
import time
import tempfile
import urllib.request

logger = logging.getLogger(__name__)

STATE_FILE = "/freqtrade/user_data/market_state.json"
_funding_cache = {}
_fng_cache = {'value': None, 'ts': 0}
FUNDING_CACHE_SECS = 8 * 3600
FNG_CACHE_SECS = 24 * 3600


def read_market_state() -> str:
    try:
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE) as f:
                return json.load(f).get("state", "trend")
    except Exception:
        pass
    return "trend"


def get_funding_rate(pair: str) -> float | None:
    global _funding_cache
    now = time.time()
    bn_symbol = pair.split('/')[0] + 'USDT'
    if bn_symbol in _funding_cache:
        if now - _funding_cache[bn_symbol]['ts'] < FUNDING_CACHE_SECS:
            return _funding_cache[bn_symbol]['rate']
    try:
        url = f"https://fapi.binance.com/fapi/v1/premiumIndex?symbol={bn_symbol}"
        req = urllib.request.Request(url, headers={'User-Agent': 'FreqtradeBot/1.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
        rate = float(data['lastFundingRate'])
        _funding_cache[bn_symbol] = {'rate': rate, 'ts': now}
        return rate
    except Exception as e:
        logger.debug(f"[FundingRate] 获取失败 {bn_symbol}: {e}")
        return None


def get_fear_greed() -> int | None:
    global _fng_cache
    now = time.time()
    if _fng_cache['value'] is not None and now - _fng_cache['ts'] < FNG_CACHE_SECS:
        return _fng_cache['value']
    try:
        url = "https://api.alternative.me/fng/?limit=1"
        req = urllib.request.Request(url, headers={'User-Agent': 'FreqtradeBot/1.0'})
        with urllib.request.urlopen(req, timeout=5) as r:
            data = json.loads(r.read())
        value = int(data['data'][0]['value'])
        label = data['data'][0]['value_classification']
        _fng_cache = {'value': value, 'ts': now}
        logger.info(f"[FearGreed] 指数: {value} ({label})")
        return value
    except Exception as e:
        logger.debug(f"[FearGreed] 获取失败: {e}")
        return None


class CryptoV10(IStrategy):

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

    order_types = {
        "entry": "limit",
        "exit": "limit",
        "stoploss": "market",
        "stoploss_on_exchange": True,
    }

    def leverage(self, pair: str, current_time, current_rate: float,
                 proposed_leverage: float, max_leverage: float,
                 entry_tag, side: str, **kwargs) -> float:
        return 5.0

    ADX_MIN  = 28
    MAX_BARS = 64
    COOLDOWN_BARS = 24
    DAILY_MAX_LOSSES = 4

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

        dataframe['dc_upper'] = dataframe['high'].rolling(20).max().shift(1)

        dataframe['atr'] = ta.ATR(dataframe, timeperiod=14)

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        pair  = metadata['pair']
        state = read_market_state()

        dataframe['enter_long']  = 0
        dataframe['enter_short'] = 0
        dataframe['enter_tag']   = ''

        if state == 'pause' or state == 'range':
            return dataframe

        if self.dp and self.dp.runmode.value in ('live', 'dry_run'):
            fng = get_fear_greed()
            funding = get_funding_rate(pair)
            if fng is not None:
                fr_str = f"{funding*100:.4f}%" if funding else "N/A"
                logger.info(f"[{pair}] FearGreed={fng} | FundingRate={fr_str}")

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

        dataframe.loc[long_conditions,  'enter_long']  = 1
        dataframe.loc[long_conditions,  'enter_tag']   = 'dc_long'

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['exit_long']  = 0
        dataframe['exit_short'] = 0
        return dataframe

    def custom_exit(self, pair: str, trade, current_time,
                    current_rate: float, current_profit: float, **kwargs):
        bars_held = int((current_time - trade.open_date_utc).total_seconds() / (15 * 60))

        if current_profit >= 0.40:
            return "tp_big"

        if bars_held >= 40 and current_profit < -0.04:
            return "stair_late"
        if bars_held >= 20 and current_profit < -0.06:
            return "stair_mid"

        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        if len(dataframe) < 1:
            return None
        last = dataframe.iloc[-1]

        if bars_held >= self.MAX_BARS and current_profit < -0.02:
            return "timeout_loss"

        if bars_held >= self.MAX_BARS * 2:
            return "timeout_extended"

        return None

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float,
                            rate: float, time_in_force: str, current_time,
                            entry_tag, side: str, **kwargs) -> bool:
        if read_market_state() == 'pause':
            return False

        closed_trades = Trade.get_trades_proxy(pair=pair, is_open=False)

        if closed_trades:
            last_trade = closed_trades[-1]
            if last_trade.exit_reason == 'stop_loss':
                cooldown_secs = self.COOLDOWN_BARS * 15 * 60
                if (current_time - last_trade.close_date_utc).total_seconds() < cooldown_secs:
                    logger.info(f"[{pair}] 冷却期中，止损后等待 {self.COOLDOWN_BARS} 根 K 线")
                    return False

        today_start = current_time.replace(hour=0, minute=0, second=0, microsecond=0)
        today_losses = [
            t for t in Trade.get_trades_proxy(is_open=False)
            if t.close_date_utc and t.close_date_utc >= today_start
            and t.exit_reason == 'stop_loss'
        ]
        if len(today_losses) >= self.DAILY_MAX_LOSSES:
            logger.warning(f"日内止损已达 {len(today_losses)} 笔，暂停入场")
            return False

        self._record_factor_snapshot(pair, rate, current_time)

        return True

    def _record_factor_snapshot(self, pair: str, rate: float, current_time):
        try:
            dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
            if len(dataframe) < 1:
                return
            last = dataframe.iloc[-1]
            snapshot = {
                'time': str(current_time),
                'pair': pair,
                'price': rate,
                'adx': round(float(last['adx']), 2),
                'plus_di': round(float(last['plus_di']), 2),
                'minus_di': round(float(last['minus_di']), 2),
                'atr': round(float(last['atr']), 4),
            }
            snap_path = "/freqtrade/user_data/factor_snapshots.json"
            snapshots = []
            if os.path.exists(snap_path):
                with open(snap_path) as f:
                    snapshots = json.load(f)
            snapshots.append(snapshot)
            tmp_fd, tmp_path = tempfile.mkstemp(dir="/freqtrade/user_data", suffix='.tmp')
            with os.fdopen(tmp_fd, 'w') as f:
                json.dump(snapshots, f, indent=2)
            os.replace(tmp_path, snap_path)
        except Exception as e:
            logger.debug(f"[FactorSnapshot] 记录失败: {e}")
