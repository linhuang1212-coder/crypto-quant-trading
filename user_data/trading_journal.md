# CryptoV10 Trading Journal

## 系统变更记录

- 2026-04-02: 上线实盘，4 品种（BTC/ETH/SOL/ADA），40% 复利，$1,300 本金，CryptoV10 策略
- 2026-04-02: 新增冷却期机制（COOLDOWN_BARS=24，止损后 6 小时不入场），回测 Sharpe 0.70→0.77，止损减少 37 笔
- 2026-04-02: 新增日内最大亏损保护（DAILY_MAX_LOSSES=4），防止极端行情连续止损
- 2026-04-02: 新增因子快照记录（factor_snapshots.json），每次入场自动采集 ADX/DI/ATR/OBV 等因子

## 策略观察记录

（实盘后逐笔记录异常交易，格式：日期 | 品种 | 方向 | 盈亏 | 观察）

## 因子研究笔记

- 回测中 ADX_MIN=28 是入场门槛，但不同品种最佳 ADX 阈值可能不同（待验证）
- ATR 突破强度过滤 (close - dc_upper) > atr * 0.5 有效减少假突破，回撤从 17.4% 降到 9.3%（固定仓位下）
- OBV > OBV_EMA 作为成交量确认有效

## 踩过的坑

- custom_stoploss + stoploss_from_open 在杠杆下返回值被 Freqtrade 二次乘以 leverage，导致止损/止盈极端收紧
- trend_dead 早退出（EMA 交叉 + ADX/DI 翻转）会误杀恢复交易，负优化
- 1H 时间框架太慢，只有 +2.2% 利润和 29% 回撤，15m 是最优时间框架
- 过滤休市 bar 会导致指标时间窗口错位（黄金系统经验），加密货币 7×24 无此问题
- 9 币全做时 DOGE(-29%)、LINK(-14%)、XRP(-11%) 严重拖后腿，品种筛选至关重要
- BNB 在 Donchian 突破策略下接近零收益，不适合此策略

## 宏观环境记录

- 2026-04-02: Fear & Greed = 12（极度恐惧），ETH/SOL/ADA 资金费率为负（空头偏多）
- 加密货币 4 年减半周期：2024 年 BTC 减半，历史上减半后 12-18 个月为牛市高峰

## 待办与未来方向

- [ ] 积累 50+ 笔实盘交易后，基于 factor_snapshots.json 做 IC 因子分析
- [ ] 账户增长到 $3,000+ 后，考虑提高 tradable_balance_ratio 到 50%
- [ ] 研究均值回归策略（Bollinger Band）作为趋势策略的互补，改善熊市（2022）表现
- [ ] 研究 ATR 自适应止损替代固定 -10% 硬止损（需避开 custom_stoploss 杠杆 bug）
- [ ] 定期（每月）运行分年度回测检查策略是否衰减
