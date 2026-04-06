# CryptoV11 Trading Journal

> 本文件是 AI 的长期记忆。每次新对话必须先读取此文件，对话结束前必须将新发现追加到对应章节。
> 完整历史归档见 `trading_journal_archive.md`，仅在需要详细实验数据时按需查阅。

## 系统变更记录

- 2026-04-05: 新增 V7 实验框架（154个全新方向变体）：成交量确认(G1,12组)/RSI过滤(G2,12组)/多时间框架(G3,9组)/Keltner通道(G4,16组)/DC固定周期扫描(G5,12组)/品种权重(G6,8组)/入场消融(G7,10组)/MACD阈值(G8,12组)/日内时段(G9,12组)/连续突破(G10,12组)/动态超时(G11,12组)/止损精搜(G12,10组)/复合退出(G13,8组)/市场状态(G14,8组)/基线(H1,1组)。[已验证] 154文件语法全通过
- 2026-04-05: V6实验Stage1完成(173→57通过门控) → Stage2分年度(57→50通过,87.7%通过率) → Stage3 Walk-Forward进行中(50×3窗口)
- 2026-04-05: 新增 V6 实验框架（173个全新方向变体）：做空逻辑(E1,16组)/ADX精搜(E2,7组)/回踩确认(E3,18组)/退出信号增强(E4,18组)/自适应杠杆(E5,15组)/4H-DC共振(E6,16组)/动态ATR_MULT(E7,16组)/时间自适应trailing(E8,20组)/ADX-DC自适应(E9,16组)/阶梯止盈(E10,18组)/EMA退出(E11,12组)/基线(F1,1组)。三阶段防过拟合流水线。[已验证] 173文件语法全通过
- 2026-04-05: V5 实验结果分析：200策略8.5h完成。A组(参数微调)全样本最优Sharpe1.31但分年度全挂(疑似脚本bug)；B/C/D组(MACD网格/DC网格/基线/消融)全部0交易(策略加载问题)；12新币全部SKIPPED。**无可用改进** [已验证]
- 2026-04-04: 新增 `user_data/scripts/generate_experiments_v5.py`：以 CryptoV11 为模板批量生成 V5 实验策略（约 200 个）至 `strategies/experiments_v5/`，清单 `experiment_manifest_v5.json`；A4 用 bars2=2×bars1 与 2×bars1+4 两档补足 24 组，B1 枚举 fast<slow-4 下全部 MACD 三元组（51 组）。[已验证] 脚本可运行
- 2026-04-04: 新增 `user_data/scripts/run_experiments_v5.ps1`：Phase0 下载12新币15m/4h → Pipeline-1（v5 三阶段+analyze_v5）→ Pipeline-2（CryptoV11 单币筛选+`experiment_gates.json` 年度门控，`v5_pair_screening.csv`）[已交付脚本，全流程待跑]
- 2026-04-04: **CryptoV11 部署实盘**，替换CryptoV10。改进：动态DC周期(ATR百分位<70%用DC14,否则DC40) + MACD(8,17,9)共振过滤(hist>0且上升)。Docker确认RUNNING
- 2026-04-04: Harness 基础设施优化：journal compaction + rules 去重 + experiment_gates.json 统一门控
- 2026-04-03: 阶梯止损S5部署实盘（custom_exit: 20b/-0.06, 40b/-0.04）
- 2026-04-03: 实盘参数更新：trailing_stop_positive 0.10→0.03, ATR_MULT 0.5→0.6
- 2026-04-02: 上线实盘，4品种（BTC/ETH/SOL/ADA），40%复利，$1,300本金

## 策略观察记录

（实盘后逐笔记录异常交易，格式：日期 | 品种 | 方向 | 盈亏 | 观察）

- 2026-04-03: 上线第2天，0笔交易。FNG=9极度恐惧，策略8个入场条件均不满足，属正常表现

## 回测实验记录

> 完整 45+ 条实验记录见 `trading_journal_archive.md`。以下为摘要。

- **V1（04-02）**：消融实验8组 + trailing/冷却期/FNG等优化12组 → 精简入场条件11→8个，Sharpe 0.71→0.77
- **V2（04-03）**：392个大规模回测（参数扫描+3D网格+新策略原型35个）→ TrailPos=0.03最优，所有非Donchian策略类型均不可行
- **V3（04-03）**：113个新方向（MTF/RSI/ATR自适应/成交量/Ichimoku/MFI）→ ATR_MULT=0.6胜出，Walk-Forward验证通过；降风险14变体→阶梯止损S5最优
- **V4（04-04）**：281个全新变体，三阶段防过拟合流水线（全样本→分年度→Walk-Forward），耗时15h21m。5组有效（G2 MACD/G3 EMA斜率/G6 动态DC/G8 阶梯止损精搜/G10 Stoch），6组放弃。**所有通过策略OOS比率>1.0，零过拟合**
- **CryptoV11（04-04）**：G6动态DC + G2 MACD共振组合 → Sharpe 1.15→1.21, PF 1.46→1.50, DD 13.05%→11.24%, 分年度6年全盈利(2022:+6.94%), WF OOS比率1.31 [已验证] **已部署**
- **V5（04-04→04-05）**：200个变体(参数微调+MACD网格+DC网格+消融+12新币)，8h31m完成。A组全样本Sharpe 0.89-1.31但分年度验证全挂(脚本bug)。B/C/D组0交易(策略加载问题)。12新币(DOT/LTC/ATOM/NEAR/APT/ARB/OP/INJ/SUI/TRX/UNI/FIL)全部不可用。**无改进** [已验证]
- **V6（04-05，Stage3进行中）**：173个变体，S1:173→57, S2:57→50(87.7%), S3:50×3窗口进行中。E1做空Sharpe1.48最亮眼；E3回踩/E8时间trail/E10阶梯止盈全部失败。[待验证-WF阶段]
- **V7（04-05，已生成待跑）**：154个全新方向（成交量/RSI/多TF/Keltner/DC固定扫描/品种权重/消融/MACD阈值/时段/连续突破/动态超时/止损精搜/复合退出/市场状态），三阶段流水线 [待验证]

## 品种筛选记录

- BTC/USDT: +86% 胜率34.8% | [留] 最稳定
- ETH/USDT: +149% 胜率34.6% | [留] 收益最高
- SOL/USDT: +85% 胜率30.5% | [留] ATR过滤后显著改善
- ADA/USDT: +163% 胜率31.4% | [留] 复利效果最好
- BNB/AVAX/XRP/LINK/DOGE: [弃] 零或负收益，详见归档
- DOT/LTC/ATOM/NEAR/APT/ARB/OP/INJ/SUI/TRX/UNI/FIL: [弃] V5筛选全部0交易(CryptoV11不适用) [已验证]

## 因子研究笔记

### 核心结论（按重要性排序）

- **因子重要性**：ADX>28（最关键）> 4H EMA确认 > ATR过滤 > EMA三线排列 > ADX上升 [已验证]
- **CryptoV11 基线指标**：Sharpe 1.21, Sortino 3.75, PF 1.50, CAGR 54.32%, DD 11.24%, 1098笔交易, 胜率31.9% [已验证]
- **trailing_stop_positive** 是影响最大的单一参数：0.03最优 [已验证]
- **阶梯止损** 极其鲁棒，V4精搜36/36全部三阶段通过 [已验证]
- **动态DC(G6)** 与 **MACD共振(G2)** 正交可组合，G3与G2高度相关不值得叠加 [已验证]
- 所有非Donchian策略（BB/MACD/Keltner/RSI/EMA交叉/Stoch/CCI/WillR/SAR）均不可行 [已验证]
- ATR自适应止损（替换硬止损）完全不可行 [已验证]
- 冗余因子已移除：DI差值>5, EMA200斜率, OBV [已验证]

### 待验证

- ADX_MIN=28 不同品种最佳阈值可能不同
- Funding Rate 纳入决策的可行性
- G2 MACD参数邻域敏感(std=0.58)，需实盘监控

## 踩过的坑

- custom_stoploss + stoploss_from_open 在杠杆下返回值被二次乘以 leverage
- trend_dead 早退出会误杀恢复交易，负优化
- 1H 时间框架太慢，15m 是最优
- 9币全做时 DOGE/LINK/XRP 严重拖后腿，品种筛选至关重要
- PowerShell 不支持 heredoc 语法，git commit 需用单行 -m

## 宏观环境记录

- 2026-04-02: FNG=12（极度恐惧），ETH/SOL/ADA 资金费率为负
- 2026-04-03: FNG=9（极度恐惧，进一步下降）
- 加密货币4年减半周期：2024年BTC减半，历史上减半后12-18个月为牛市高峰

## 待办与未来方向

- [x] **V5 实验结果分析**：已完成(04-05)，200策略8.5h，无可用改进，12新币全部不可用
- [ ] **V6 Stage3 Walk-Forward 运行中**：50个策略×3窗口=300次回测
- [ ] **V7 实验待运行**：154个全新方向(成交量/RSI/多TF/KC/消融等)，V6完成后接上
- [ ] 积累 50+ 笔实盘交易后，基于 factor_snapshots.json 做 IC 因子分析
- [ ] 账户增长到 $3,000+ 后，考虑提高 tradable_balance_ratio 到 50%
- [ ] 定期（每月）运行分年度回测检查策略是否衰减
- [ ] Funding Rate 纳入决策的可行性研究
