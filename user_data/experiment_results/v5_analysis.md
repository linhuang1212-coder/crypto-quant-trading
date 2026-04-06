# V5 三阶段回测分析报告

- 生成路径: `C:\Users\hlin2\freqtrade\user_data\experiment_results\v5_analysis.md`
- 数据根目录: `C:\Users\hlin2\freqtrade`

## 数据文件状态
- 未找到 `C:\Users\hlin2\freqtrade\user_data\experiment_results\v5_walkforward.csv`，已跳过 Walk-Forward 与部分综合结论。

## 1. 全样本排名（Top 20，按 Sharpe 降序）

基线参考: Sharpe **1.21**, PF **1.5**, 最大回撤 **11.24%**, 总利润 **1398%**, 交易数 **1098**。

| 排名 | strategy | group | name | Sharpe | PF | 利润% | 回撤% | 交易数 | 超越基线(分项) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | V5_GA1_P002 | group_a1_trailing | GA1 trail 0.01/0.25 | 1.31 | 1.54 | 2086.3 | 12.3 | 1140 | Sharpe:✓ PF:✓ 回撤:× 利润%:✓ 交易数:✓ |
| 2 | V5_GA1_P001 | group_a1_trailing | GA1 trail 0.01/0.2 | 1.28 | 1.43 | 1260.2 | 12.0 | 1198 | Sharpe:✓ PF:× 回撤:× 利润%:× 交易数:✓ |
| 3 | V5_GA1_P003 | group_a1_trailing | GA1 trail 0.01/0.3 | 1.28 | 1.58 | 2217.4 | 10.9 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 4 | V5_GA1_P007 | group_a1_trailing | GA1 trail 0.02/0.25 | 1.26 | 1.49 | 1559.4 | 12.6 | 1140 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 5 | V5_GA1_P008 | group_a1_trailing | GA1 trail 0.02/0.3 | 1.24 | 1.54 | 1781.0 | 11.1 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 6 | V5_GA1_P013 | group_a1_trailing | GA1 trail 0.03/0.3 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 7 | V5_GA2_P009 | group_a2_stoploss | GA2 sl=-0.1 stair=True | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 8 | V5_GA3_P002 | group_a3_tp_big | GA3 TP_BIG=0.25 | 1.21 | 1.49 | 1332.3 | 11.9 | 1098 | Sharpe:✓ PF:× 回撤:× 利润%:× 交易数:✓ |
| 9 | V5_GA3_P003 | group_a3_tp_big | GA3 TP_BIG=0.3 | 1.21 | 1.50 | 1402.1 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 10 | V5_GA3_P004 | group_a3_tp_big | GA3 TP_BIG=0.35 | 1.21 | 1.50 | 1402.1 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 11 | V5_GA3_P005 | group_a3_tp_big | GA3 TP_BIG=0.4 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 12 | V5_GA3_P006 | group_a3_tp_big | GA3 TP_BIG=0.5 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 13 | V5_GA3_P007 | group_a3_tp_big | GA3 TP_BIG=0.6 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 14 | V5_GA3_P008 | group_a3_tp_big | GA3 TP_BIG=0.8 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 15 | V5_GA3_P009 | group_a3_tp_big | GA3 TP_BIG=1.0 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 16 | V5_GA3_P010 | group_a3_tp_big | GA3 TP_BIG=99.0 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 17 | V5_GA4_P012 | group_a4_stair_fine | GA4 stair 18/-0.06 40/-0.04 | 1.21 | 1.50 | 1361.4 | 10.6 | 1101 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 18 | V5_GA4_P017 | group_a4_stair_fine | GA4 stair 20/-0.06 40/-0.04 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 19 | V5_GA5_P009 | group_a5_max_bars | GA5 MAX_BARS=64 timeout=-0.02 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 20 | V5_GA1_P004 | group_a1_trailing | GA1 trail 0.01/0.35 | 1.20 | 1.55 | 1829.6 | 12.3 | 1069 | Sharpe:× PF:✓ 回撤:× 利润%:✓ 交易数:× |

<details><summary>Top20 的 params 摘要（展开）</summary>

| 排名 | params |
| --- | --- |
| 1 | `{"trailing_stop_positive":0.01,"trailing_stop_positive_offset":0.25}` |
| 2 | `{"trailing_stop_positive":0.01,"trailing_stop_positive_offset":0.2}` |
| 3 | `{"trailing_stop_positive":0.01,"trailing_stop_positive_offset":0.3}` |
| 4 | `{"trailing_stop_positive":0.02,"trailing_stop_positive_offset":0.25}` |
| 5 | `{"trailing_stop_positive":0.02,"trailing_stop_positive_offset":0.3}` |
| 6 | `{"trailing_stop_positive":0.03,"trailing_stop_positive_offset":0.3}` |
| 7 | `{"stoploss":-0.1,"stair":true}` |
| 8 | `{"TP_BIG":0.25}` |
| 9 | `{"TP_BIG":0.3}` |
| 10 | `{"TP_BIG":0.35}` |
| 11 | `{"TP_BIG":0.4}` |
| 12 | `{"TP_BIG":0.5}` |
| 13 | `{"TP_BIG":0.6}` |
| 14 | `{"TP_BIG":0.8}` |
| 15 | `{"TP_BIG":1.0}` |
| 16 | `{"TP_BIG":99.0}` |
| 17 | `{"bars1":18,"loss1":-0.06,"bars2":40,"loss2":-0.04,"bars2_extra":4}` |
| 18 | `{"bars1":20,"loss1":-0.06,"bars2":40,"loss2":-0.04,"bars2_extra":0}` |
| 19 | `{"MAX_BARS":64,"TIMEOUT_LOSS_THRESHOLD":-0.02}` |
| 20 | `{"trailing_stop_positive":0.01,"trailing_stop_positive_offset":0.35}` |

</details>

## 2. 分组汇总

| group | 策略数 | 阶段1通过率 | 组均Sharpe | 最优 name | 最优Sharpe | 分年度验证 | Walk-Forward | 邻域std标签 | 结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| group_a1_trailing | 30 | 90% | 1.10 | GA1 trail 0.01/0.25 | 1.31 | 不稳定 (CV=inf, 0/6年盈利) | — | 平滑 (0.00) | 有潜力 |
| group_a2_stoploss | 14 | 71% | 0.96 | GA2 sl=-0.1 stair=True | 1.21 | 不稳定 (CV=inf, 0/6年盈利) | — | 平滑 (0.00) | 有潜力 |
| group_a3_tp_big | 10 | 100% | 1.20 | GA3 TP_BIG=0.25 | 1.21 | 不稳定 (CV=inf, 0/6年盈利) | — | 平滑 (0.00) | 有潜力 |
| group_a4_stair_fine | 24 | 100% | 1.11 | GA4 stair 18/-0.06 40/-0.04 | 1.21 | 不稳定 (CV=inf, 0/6年盈利) | — | 平滑 (0.00) | 有潜力 |
| group_a5_max_bars | 21 | 62% | 0.74 | GA5 MAX_BARS=64 timeout=-0.02 | 1.21 | 不稳定 (CV=inf, 0/6年盈利) | — | 平滑 (0.00) | 有潜力 |
| group_b1_macd_grid | 51 | 0% | 0.00 | GB1 MACD 6/15/5 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_b2_macd_modes | 12 | 0% | 0.00 | GB2 8/17/9 hist_rise | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_b3_alternatives | 8 | 0% | 0.00 | GB3 EMA slope p=5 th=0.001 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_c_dc_grid | 20 | 0% | 0.00 | GC DC 10/30 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_d1_baseline_v11 | 1 | 0% | 0.00 | GD1 CryptoV11 baseline | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_d2_baseline_v10 | 1 | 0% | 0.00 | GD2 CryptoV10 baseline | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_d3_ablation | 8 | 0% | 0.00 | GD3 No G6 fixed DC20 + MACD | 0.00 | — | — | 平滑 (0.00) | 放弃 |

> 分年度参考：参考：2020:+85% Sharpe1.72 / 2021:+115% Sharpe1.91 / 2022:+6.94% Sharpe0.21 / 2023:+74% Sharpe1.33 / 2024:+36% Sharpe1.14 / 2025Q1:+46% Sharpe1.07

## 3. 参数邻域稳定性（阶段1，按 group × strategy）

在同一 `strategy`+`group` 内，对所有变体的 Sharpe 计算总体标准差；并按 `name` 字典序相邻检测尖峰（高于邻居最大值超过 0.3）。

| strategy | group | 变体数 | Sharpe std | 稳定性 | 尖峰标记(若有) |
| --- | --- | --- | --- | --- | --- |
| V5_GA1_P001 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P002 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P003 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P004 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P005 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P006 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P007 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P008 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P009 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P010 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P011 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P012 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P013 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P014 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P015 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P016 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P017 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P018 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P019 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P020 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P021 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P022 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P023 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P024 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P025 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P026 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P027 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P028 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P029 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA1_P030 | group_a1_trailing | 1 | 0.00 | 平滑 | — |
| V5_GA2_P001 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P002 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P003 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P004 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P005 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P006 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P007 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P008 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P009 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P010 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P011 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P012 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P013 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA2_P014 | group_a2_stoploss | 1 | 0.00 | 平滑 | — |
| V5_GA3_P001 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P002 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P003 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P004 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P005 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P006 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P007 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P008 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P009 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA3_P010 | group_a3_tp_big | 1 | 0.00 | 平滑 | — |
| V5_GA4_P001 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P002 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P003 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P004 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P005 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P006 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P007 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P008 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P009 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P010 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P011 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P012 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P013 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P014 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P015 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P016 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P017 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P018 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P019 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P020 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P021 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P022 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P023 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA4_P024 | group_a4_stair_fine | 1 | 0.00 | 平滑 | — |
| V5_GA5_P001 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P002 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P003 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P004 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P005 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P006 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P007 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P008 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P009 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P010 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P011 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P012 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P013 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P014 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P015 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P016 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P017 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P018 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P019 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P020 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GA5_P021 | group_a5_max_bars | 1 | 0.00 | 平滑 | — |
| V5_GB1_P001 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P002 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P003 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P004 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P005 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P006 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P007 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P008 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P009 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P010 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P011 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P012 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P013 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P014 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P015 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P016 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P017 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P018 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P019 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P020 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P021 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P022 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P023 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P024 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P025 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P026 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P027 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P028 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P029 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P030 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P031 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P032 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P033 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P034 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P035 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P036 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P037 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P038 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P039 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P040 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P041 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P042 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P043 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P044 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P045 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P046 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P047 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P048 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P049 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P050 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB1_P051 | group_b1_macd_grid | 1 | 0.00 | 平滑 | — |
| V5_GB2_P001 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P002 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P003 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P004 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P005 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P006 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P007 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P008 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P009 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P010 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P011 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB2_P012 | group_b2_macd_modes | 1 | 0.00 | 平滑 | — |
| V5_GB3_P001 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GB3_P002 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GB3_P003 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GB3_P004 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GB3_P005 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GB3_P006 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GB3_P007 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GB3_P008 | group_b3_alternatives | 1 | 0.00 | 平滑 | — |
| V5_GC_P001 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P002 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P003 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P004 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P005 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P006 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P007 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P008 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P009 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P010 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P011 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P012 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P013 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P014 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P015 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P016 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P017 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P018 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P019 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GC_P020 | group_c_dc_grid | 1 | 0.00 | 平滑 | — |
| V5_GD1_P001 | group_d1_baseline_v11 | 1 | 0.00 | 平滑 | — |
| V5_GD2_P001 | group_d2_baseline_v10 | 1 | 0.00 | 平滑 | — |
| V5_GD3_P001 | group_d3_ablation | 1 | 0.00 | 平滑 | — |
| V5_GD3_P002 | group_d3_ablation | 1 | 0.00 | 平滑 | — |
| V5_GD3_P003 | group_d3_ablation | 1 | 0.00 | 平滑 | — |
| V5_GD3_P004 | group_d3_ablation | 1 | 0.00 | 平滑 | — |
| V5_GD3_P005 | group_d3_ablation | 1 | 0.00 | 平滑 | — |
| V5_GD3_P006 | group_d3_ablation | 1 | 0.00 | 平滑 | — |
| V5_GD3_P007 | group_d3_ablation | 1 | 0.00 | 平滑 | — |
| V5_GD3_P008 | group_d3_ablation | 1 | 0.00 | 平滑 | — |

## 4. 分年度一致性（仅阶段1已通过门控的候选）

规则：**稳定** = CV < 0.5 且全年份盈利；**可接受** = CV < 0.8 且盈利年份≥ max(1, 总年数-1)；否则 **不稳定**。

| strategy | group | name | 全样本Sharpe | 年份数 | 盈利年数 | CV | 2022 Sharpe | 标签 | 阶段2通过 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V5_GA1_P002 | group_a1_trailing | GA1 trail 0.01/0.25 | 1.31 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P001 | group_a1_trailing | GA1 trail 0.01/0.2 | 1.28 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P003 | group_a1_trailing | GA1 trail 0.01/0.3 | 1.28 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P007 | group_a1_trailing | GA1 trail 0.02/0.25 | 1.26 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P008 | group_a1_trailing | GA1 trail 0.02/0.3 | 1.24 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P013 | group_a1_trailing | GA1 trail 0.03/0.3 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P009 | group_a2_stoploss | GA2 sl=-0.1 stair=True | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P002 | group_a3_tp_big | GA3 TP_BIG=0.25 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P003 | group_a3_tp_big | GA3 TP_BIG=0.3 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P004 | group_a3_tp_big | GA3 TP_BIG=0.35 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P005 | group_a3_tp_big | GA3 TP_BIG=0.4 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P006 | group_a3_tp_big | GA3 TP_BIG=0.5 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P007 | group_a3_tp_big | GA3 TP_BIG=0.6 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P008 | group_a3_tp_big | GA3 TP_BIG=0.8 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P009 | group_a3_tp_big | GA3 TP_BIG=1.0 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P010 | group_a3_tp_big | GA3 TP_BIG=99.0 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P012 | group_a4_stair_fine | GA4 stair 18/-0.06 40/-0.04 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P017 | group_a4_stair_fine | GA4 stair 20/-0.06 40/-0.04 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P009 | group_a5_max_bars | GA5 MAX_BARS=64 timeout=-0.02 | 1.21 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P004 | group_a1_trailing | GA1 trail 0.01/0.35 | 1.20 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P012 | group_a1_trailing | GA1 trail 0.03/0.25 | 1.20 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P018 | group_a4_stair_fine | GA4 stair 20/-0.06 44/-0.04 | 1.20 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P006 | group_a4_stair_fine | GA4 stair 16/-0.06 36/-0.04 | 1.19 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P010 | group_a5_max_bars | GA5 MAX_BARS=64 timeout=-0.03 | 1.19 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P006 | group_a1_trailing | GA1 trail 0.02/0.2 | 1.18 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P009 | group_a1_trailing | GA1 trail 0.02/0.35 | 1.18 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P011 | group_a4_stair_fine | GA4 stair 18/-0.06 36/-0.04 | 1.18 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P023 | group_a4_stair_fine | GA4 stair 22/-0.06 44/-0.04 | 1.18 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P024 | group_a4_stair_fine | GA4 stair 22/-0.06 48/-0.04 | 1.17 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P007 | group_a5_max_bars | GA5 MAX_BARS=56 timeout=-0.02 | 1.17 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P012 | group_a5_max_bars | GA5 MAX_BARS=80 timeout=-0.03 | 1.17 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P018 | group_a1_trailing | GA1 trail 0.04/0.3 | 1.16 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P008 | group_a5_max_bars | GA5 MAX_BARS=56 timeout=-0.03 | 1.16 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P014 | group_a1_trailing | GA1 trail 0.03/0.35 | 1.15 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA3_P001 | group_a3_tp_big | GA3 TP_BIG=0.2 | 1.15 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P013 | group_a5_max_bars | GA5 MAX_BARS=96 timeout=-0.02 | 1.15 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P014 | group_a5_max_bars | GA5 MAX_BARS=96 timeout=-0.03 | 1.15 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P011 | group_a5_max_bars | GA5 MAX_BARS=80 timeout=-0.02 | 1.14 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P017 | group_a1_trailing | GA1 trail 0.04/0.25 | 1.13 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P005 | group_a4_stair_fine | GA4 stair 16/-0.06 32/-0.04 | 1.13 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P023 | group_a1_trailing | GA1 trail 0.05/0.3 | 1.12 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P011 | group_a2_stoploss | GA2 sl=-0.12 stair=True | 1.12 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P001 | group_a4_stair_fine | GA4 stair 16/-0.04 32/-0.02 | 1.12 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P005 | group_a5_max_bars | GA5 MAX_BARS=48 timeout=-0.02 | 1.12 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P019 | group_a1_trailing | GA1 trail 0.04/0.35 | 1.11 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P007 | group_a2_stoploss | GA2 sl=-0.09 stair=True | 1.11 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P013 | group_a2_stoploss | GA2 sl=-0.15 stair=True | 1.10 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P002 | group_a4_stair_fine | GA4 stair 16/-0.04 36/-0.02 | 1.10 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P015 | group_a4_stair_fine | GA4 stair 20/-0.05 40/-0.03 | 1.10 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P006 | group_a5_max_bars | GA5 MAX_BARS=48 timeout=-0.03 | 1.10 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P005 | group_a1_trailing | GA1 trail 0.01/0.4 | 1.09 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P010 | group_a2_stoploss | GA2 sl=-0.1 stair=False | 1.09 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P008 | group_a4_stair_fine | GA4 stair 18/-0.04 40/-0.02 | 1.09 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P013 | group_a4_stair_fine | GA4 stair 20/-0.04 40/-0.02 | 1.09 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P024 | group_a1_trailing | GA1 trail 0.05/0.35 | 1.08 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P007 | group_a4_stair_fine | GA4 stair 18/-0.04 36/-0.02 | 1.08 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P010 | group_a4_stair_fine | GA4 stair 18/-0.05 40/-0.03 | 1.08 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P016 | group_a4_stair_fine | GA4 stair 20/-0.05 44/-0.03 | 1.08 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P020 | group_a4_stair_fine | GA4 stair 22/-0.04 48/-0.02 | 1.08 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P004 | group_a5_max_bars | GA5 MAX_BARS=40 timeout=-0.03 | 1.08 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P010 | group_a1_trailing | GA1 trail 0.02/0.4 | 1.07 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P028 | group_a1_trailing | GA1 trail 0.06/0.3 | 1.07 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P004 | group_a4_stair_fine | GA4 stair 16/-0.05 36/-0.03 | 1.07 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P009 | group_a4_stair_fine | GA4 stair 18/-0.05 36/-0.03 | 1.07 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P014 | group_a4_stair_fine | GA4 stair 20/-0.04 44/-0.02 | 1.07 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P021 | group_a4_stair_fine | GA4 stair 22/-0.05 44/-0.03 | 1.07 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P008 | group_a2_stoploss | GA2 sl=-0.09 stair=False | 1.06 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P019 | group_a4_stair_fine | GA4 stair 22/-0.04 44/-0.02 | 1.06 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P003 | group_a5_max_bars | GA5 MAX_BARS=40 timeout=-0.02 | 1.06 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P011 | group_a1_trailing | GA1 trail 0.03/0.2 | 1.05 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P022 | group_a1_trailing | GA1 trail 0.05/0.25 | 1.05 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P022 | group_a4_stair_fine | GA4 stair 22/-0.05 48/-0.03 | 1.05 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P015 | group_a1_trailing | GA1 trail 0.03/0.4 | 1.04 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA4_P003 | group_a4_stair_fine | GA4 stair 16/-0.05 32/-0.03 | 1.04 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P029 | group_a1_trailing | GA1 trail 0.06/0.35 | 1.03 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P020 | group_a1_trailing | GA1 trail 0.04/0.4 | 1.02 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P005 | group_a2_stoploss | GA2 sl=-0.08 stair=True | 1.01 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P027 | group_a1_trailing | GA1 trail 0.06/0.25 | 1.00 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P025 | group_a1_trailing | GA1 trail 0.05/0.4 | 0.99 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA1_P030 | group_a1_trailing | GA1 trail 0.06/0.4 | 0.98 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P006 | group_a2_stoploss | GA2 sl=-0.08 stair=False | 0.98 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P012 | group_a2_stoploss | GA2 sl=-0.12 stair=False | 0.97 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA2_P014 | group_a2_stoploss | GA2 sl=-0.15 stair=False | 0.92 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |
| V5_GA5_P001 | group_a5_max_bars | GA5 MAX_BARS=32 timeout=-0.02 | 0.92 | 6 | 0 | inf | 0.00 | 不稳定 | 否 |

## 5. Walk-Forward 过拟合检测（对阶段2已通过门控的候选）

（无 Walk-Forward CSV）

## 6. 最终推荐（综合三阶段）

判定摘要：
- **阶段1**：Sharpe≥0.9、PF≥1.3、交易≥800、回撤≤25.0%。
- **阶段2**：分年度标签为「稳定」或「可接受」（见第4节）。
- **阶段3**：存在 WF 行且 OOS≥0.5 且平均测试 Sharpe>0；**强烈推荐** 另要求 OOS>0.8 且组内邻域 Sharpe 标准差 < 0.1（平滑）。

### 强烈推荐

（当前无候选满足全部强化条件）

### 推荐

（当前无候选满足三阶段+Sharpe 条件）

### 观察名单

（无）

### 放弃/未过关

- **放弃** `V5_GA1_P001` / `group_a1_trailing` / `GA1 trail 0.01/0.2`：阶段2「不稳定」
- **放弃** `V5_GA1_P002` / `group_a1_trailing` / `GA1 trail 0.01/0.25`：阶段2「不稳定」
- **放弃** `V5_GA1_P003` / `group_a1_trailing` / `GA1 trail 0.01/0.3`：阶段2「不稳定」
- **放弃** `V5_GA1_P004` / `group_a1_trailing` / `GA1 trail 0.01/0.35`：阶段2「不稳定」
- **放弃** `V5_GA1_P005` / `group_a1_trailing` / `GA1 trail 0.01/0.4`：阶段2「不稳定」
- **放弃** `V5_GA1_P006` / `group_a1_trailing` / `GA1 trail 0.02/0.2`：阶段2「不稳定」
- **放弃** `V5_GA1_P007` / `group_a1_trailing` / `GA1 trail 0.02/0.25`：阶段2「不稳定」
- **放弃** `V5_GA1_P008` / `group_a1_trailing` / `GA1 trail 0.02/0.3`：阶段2「不稳定」
- **放弃** `V5_GA1_P009` / `group_a1_trailing` / `GA1 trail 0.02/0.35`：阶段2「不稳定」
- **放弃** `V5_GA1_P010` / `group_a1_trailing` / `GA1 trail 0.02/0.4`：阶段2「不稳定」
- **放弃** `V5_GA1_P011` / `group_a1_trailing` / `GA1 trail 0.03/0.2`：阶段2「不稳定」
- **放弃** `V5_GA1_P012` / `group_a1_trailing` / `GA1 trail 0.03/0.25`：阶段2「不稳定」
- **放弃** `V5_GA1_P013` / `group_a1_trailing` / `GA1 trail 0.03/0.3`：阶段2「不稳定」
- **放弃** `V5_GA1_P014` / `group_a1_trailing` / `GA1 trail 0.03/0.35`：阶段2「不稳定」
- **放弃** `V5_GA1_P015` / `group_a1_trailing` / `GA1 trail 0.03/0.4`：阶段2「不稳定」
- **放弃** `V5_GA1_P016` / `group_a1_trailing` / `GA1 trail 0.04/0.2`：未通过阶段1
- **放弃** `V5_GA1_P017` / `group_a1_trailing` / `GA1 trail 0.04/0.25`：阶段2「不稳定」
- **放弃** `V5_GA1_P018` / `group_a1_trailing` / `GA1 trail 0.04/0.3`：阶段2「不稳定」
- **放弃** `V5_GA1_P019` / `group_a1_trailing` / `GA1 trail 0.04/0.35`：阶段2「不稳定」
- **放弃** `V5_GA1_P020` / `group_a1_trailing` / `GA1 trail 0.04/0.4`：阶段2「不稳定」
- **放弃** `V5_GA1_P021` / `group_a1_trailing` / `GA1 trail 0.05/0.2`：未通过阶段1
- **放弃** `V5_GA1_P022` / `group_a1_trailing` / `GA1 trail 0.05/0.25`：阶段2「不稳定」
- **放弃** `V5_GA1_P023` / `group_a1_trailing` / `GA1 trail 0.05/0.3`：阶段2「不稳定」
- **放弃** `V5_GA1_P024` / `group_a1_trailing` / `GA1 trail 0.05/0.35`：阶段2「不稳定」
- **放弃** `V5_GA1_P025` / `group_a1_trailing` / `GA1 trail 0.05/0.4`：阶段2「不稳定」
- **放弃** `V5_GA1_P026` / `group_a1_trailing` / `GA1 trail 0.06/0.2`：未通过阶段1
- **放弃** `V5_GA1_P027` / `group_a1_trailing` / `GA1 trail 0.06/0.25`：阶段2「不稳定」
- **放弃** `V5_GA1_P028` / `group_a1_trailing` / `GA1 trail 0.06/0.3`：阶段2「不稳定」
- **放弃** `V5_GA1_P029` / `group_a1_trailing` / `GA1 trail 0.06/0.35`：阶段2「不稳定」
- **放弃** `V5_GA1_P030` / `group_a1_trailing` / `GA1 trail 0.06/0.4`：阶段2「不稳定」
- **放弃** `V5_GA2_P001` / `group_a2_stoploss` / `GA2 sl=-0.06 stair=True`：未通过阶段1
- **放弃** `V5_GA2_P002` / `group_a2_stoploss` / `GA2 sl=-0.06 stair=False`：未通过阶段1
- **放弃** `V5_GA2_P003` / `group_a2_stoploss` / `GA2 sl=-0.07 stair=True`：未通过阶段1
- **放弃** `V5_GA2_P004` / `group_a2_stoploss` / `GA2 sl=-0.07 stair=False`：未通过阶段1
- **放弃** `V5_GA2_P005` / `group_a2_stoploss` / `GA2 sl=-0.08 stair=True`：阶段2「不稳定」
- **放弃** `V5_GA2_P006` / `group_a2_stoploss` / `GA2 sl=-0.08 stair=False`：阶段2「不稳定」
- **放弃** `V5_GA2_P007` / `group_a2_stoploss` / `GA2 sl=-0.09 stair=True`：阶段2「不稳定」
- **放弃** `V5_GA2_P008` / `group_a2_stoploss` / `GA2 sl=-0.09 stair=False`：阶段2「不稳定」
- **放弃** `V5_GA2_P009` / `group_a2_stoploss` / `GA2 sl=-0.1 stair=True`：阶段2「不稳定」
- **放弃** `V5_GA2_P010` / `group_a2_stoploss` / `GA2 sl=-0.1 stair=False`：阶段2「不稳定」
- **放弃** `V5_GA2_P011` / `group_a2_stoploss` / `GA2 sl=-0.12 stair=True`：阶段2「不稳定」
- **放弃** `V5_GA2_P012` / `group_a2_stoploss` / `GA2 sl=-0.12 stair=False`：阶段2「不稳定」
- **放弃** `V5_GA2_P013` / `group_a2_stoploss` / `GA2 sl=-0.15 stair=True`：阶段2「不稳定」
- **放弃** `V5_GA2_P014` / `group_a2_stoploss` / `GA2 sl=-0.15 stair=False`：阶段2「不稳定」
- **放弃** `V5_GA3_P001` / `group_a3_tp_big` / `GA3 TP_BIG=0.2`：阶段2「不稳定」
- **放弃** `V5_GA3_P002` / `group_a3_tp_big` / `GA3 TP_BIG=0.25`：阶段2「不稳定」
- **放弃** `V5_GA3_P003` / `group_a3_tp_big` / `GA3 TP_BIG=0.3`：阶段2「不稳定」
- **放弃** `V5_GA3_P004` / `group_a3_tp_big` / `GA3 TP_BIG=0.35`：阶段2「不稳定」
- **放弃** `V5_GA3_P005` / `group_a3_tp_big` / `GA3 TP_BIG=0.4`：阶段2「不稳定」
- **放弃** `V5_GA3_P006` / `group_a3_tp_big` / `GA3 TP_BIG=0.5`：阶段2「不稳定」
- **放弃** `V5_GA3_P007` / `group_a3_tp_big` / `GA3 TP_BIG=0.6`：阶段2「不稳定」
- **放弃** `V5_GA3_P008` / `group_a3_tp_big` / `GA3 TP_BIG=0.8`：阶段2「不稳定」
- **放弃** `V5_GA3_P009` / `group_a3_tp_big` / `GA3 TP_BIG=1.0`：阶段2「不稳定」
- **放弃** `V5_GA3_P010` / `group_a3_tp_big` / `GA3 TP_BIG=99.0`：阶段2「不稳定」
- **放弃** `V5_GA4_P001` / `group_a4_stair_fine` / `GA4 stair 16/-0.04 32/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P002` / `group_a4_stair_fine` / `GA4 stair 16/-0.04 36/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P003` / `group_a4_stair_fine` / `GA4 stair 16/-0.05 32/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P004` / `group_a4_stair_fine` / `GA4 stair 16/-0.05 36/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P005` / `group_a4_stair_fine` / `GA4 stair 16/-0.06 32/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA4_P006` / `group_a4_stair_fine` / `GA4 stair 16/-0.06 36/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA4_P007` / `group_a4_stair_fine` / `GA4 stair 18/-0.04 36/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P008` / `group_a4_stair_fine` / `GA4 stair 18/-0.04 40/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P009` / `group_a4_stair_fine` / `GA4 stair 18/-0.05 36/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P010` / `group_a4_stair_fine` / `GA4 stair 18/-0.05 40/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P011` / `group_a4_stair_fine` / `GA4 stair 18/-0.06 36/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA4_P012` / `group_a4_stair_fine` / `GA4 stair 18/-0.06 40/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA4_P013` / `group_a4_stair_fine` / `GA4 stair 20/-0.04 40/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P014` / `group_a4_stair_fine` / `GA4 stair 20/-0.04 44/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P015` / `group_a4_stair_fine` / `GA4 stair 20/-0.05 40/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P016` / `group_a4_stair_fine` / `GA4 stair 20/-0.05 44/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P017` / `group_a4_stair_fine` / `GA4 stair 20/-0.06 40/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA4_P018` / `group_a4_stair_fine` / `GA4 stair 20/-0.06 44/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA4_P019` / `group_a4_stair_fine` / `GA4 stair 22/-0.04 44/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P020` / `group_a4_stair_fine` / `GA4 stair 22/-0.04 48/-0.02`：阶段2「不稳定」
- **放弃** `V5_GA4_P021` / `group_a4_stair_fine` / `GA4 stair 22/-0.05 44/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P022` / `group_a4_stair_fine` / `GA4 stair 22/-0.05 48/-0.03`：阶段2「不稳定」
- **放弃** `V5_GA4_P023` / `group_a4_stair_fine` / `GA4 stair 22/-0.06 44/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA4_P024` / `group_a4_stair_fine` / `GA4 stair 22/-0.06 48/-0.04`：阶段2「不稳定」
- **放弃** `V5_GA5_P001` / `group_a5_max_bars` / `GA5 MAX_BARS=32 timeout=-0.02`：阶段2「不稳定」
- **放弃** `V5_GA5_P002` / `group_a5_max_bars` / `GA5 MAX_BARS=32 timeout=-0.03`：未通过阶段1
- **放弃** `V5_GA5_P003` / `group_a5_max_bars` / `GA5 MAX_BARS=40 timeout=-0.02`：阶段2「不稳定」
- **放弃** `V5_GA5_P004` / `group_a5_max_bars` / `GA5 MAX_BARS=40 timeout=-0.03`：阶段2「不稳定」
- **放弃** `V5_GA5_P005` / `group_a5_max_bars` / `GA5 MAX_BARS=48 timeout=-0.02`：阶段2「不稳定」
- **放弃** `V5_GA5_P006` / `group_a5_max_bars` / `GA5 MAX_BARS=48 timeout=-0.03`：阶段2「不稳定」
- **放弃** `V5_GA5_P007` / `group_a5_max_bars` / `GA5 MAX_BARS=56 timeout=-0.02`：阶段2「不稳定」
- **放弃** `V5_GA5_P008` / `group_a5_max_bars` / `GA5 MAX_BARS=56 timeout=-0.03`：阶段2「不稳定」
- **放弃** `V5_GA5_P009` / `group_a5_max_bars` / `GA5 MAX_BARS=64 timeout=-0.02`：阶段2「不稳定」
- **放弃** `V5_GA5_P010` / `group_a5_max_bars` / `GA5 MAX_BARS=64 timeout=-0.03`：阶段2「不稳定」
- **放弃** `V5_GA5_P011` / `group_a5_max_bars` / `GA5 MAX_BARS=80 timeout=-0.02`：阶段2「不稳定」
- **放弃** `V5_GA5_P012` / `group_a5_max_bars` / `GA5 MAX_BARS=80 timeout=-0.03`：阶段2「不稳定」
- **放弃** `V5_GA5_P013` / `group_a5_max_bars` / `GA5 MAX_BARS=96 timeout=-0.02`：阶段2「不稳定」
- **放弃** `V5_GA5_P014` / `group_a5_max_bars` / `GA5 MAX_BARS=96 timeout=-0.03`：阶段2「不稳定」
- **放弃** `V5_GA5_P015` / `group_a5_max_bars` / `GA5 MAX_BARS=128 timeout=-0.02`：未通过阶段1
- **放弃** `V5_GA5_P016` / `group_a5_max_bars` / `GA5 MAX_BARS=128 timeout=-0.03`：未通过阶段1
- **放弃** `V5_GA5_P017` / `group_a5_max_bars` / `GA5 MAX_BARS=144 timeout=-0.02`：未通过阶段1
- **放弃** `V5_GA5_P018` / `group_a5_max_bars` / `GA5 MAX_BARS=144 timeout=-0.03`：未通过阶段1
- **放弃** `V5_GA5_P019` / `group_a5_max_bars` / `GA5 MAX_BARS=160 timeout=-0.02`：未通过阶段1
- **放弃** `V5_GA5_P020` / `group_a5_max_bars` / `GA5 MAX_BARS=160 timeout=-0.03`：未通过阶段1
- **放弃** `V5_GA5_P021` / `group_a5_max_bars` / `GA5 MAX_BARS=64 timeout=-0.025`：未通过阶段1
- **放弃** `V5_GB1_P001` / `group_b1_macd_grid` / `GB1 MACD 6/15/5`：未通过阶段1
- **放弃** `V5_GB1_P002` / `group_b1_macd_grid` / `GB1 MACD 6/15/7`：未通过阶段1
- **放弃** `V5_GB1_P003` / `group_b1_macd_grid` / `GB1 MACD 6/15/9`：未通过阶段1
- **放弃** `V5_GB1_P004` / `group_b1_macd_grid` / `GB1 MACD 6/17/5`：未通过阶段1
- **放弃** `V5_GB1_P005` / `group_b1_macd_grid` / `GB1 MACD 6/17/7`：未通过阶段1
- **放弃** `V5_GB1_P006` / `group_b1_macd_grid` / `GB1 MACD 6/17/9`：未通过阶段1
- **放弃** `V5_GB1_P007` / `group_b1_macd_grid` / `GB1 MACD 6/21/5`：未通过阶段1
- **放弃** `V5_GB1_P008` / `group_b1_macd_grid` / `GB1 MACD 6/21/7`：未通过阶段1
- **放弃** `V5_GB1_P009` / `group_b1_macd_grid` / `GB1 MACD 6/21/9`：未通过阶段1
- **放弃** `V5_GB1_P010` / `group_b1_macd_grid` / `GB1 MACD 6/26/5`：未通过阶段1
- **放弃** `V5_GB1_P011` / `group_b1_macd_grid` / `GB1 MACD 6/26/7`：未通过阶段1
- **放弃** `V5_GB1_P012` / `group_b1_macd_grid` / `GB1 MACD 6/26/9`：未通过阶段1
- **放弃** `V5_GB1_P013` / `group_b1_macd_grid` / `GB1 MACD 8/15/5`：未通过阶段1
- **放弃** `V5_GB1_P014` / `group_b1_macd_grid` / `GB1 MACD 8/15/7`：未通过阶段1
- **放弃** `V5_GB1_P015` / `group_b1_macd_grid` / `GB1 MACD 8/15/9`：未通过阶段1
- **放弃** `V5_GB1_P016` / `group_b1_macd_grid` / `GB1 MACD 8/17/5`：未通过阶段1
- **放弃** `V5_GB1_P017` / `group_b1_macd_grid` / `GB1 MACD 8/17/7`：未通过阶段1
- **放弃** `V5_GB1_P018` / `group_b1_macd_grid` / `GB1 MACD 8/17/9`：未通过阶段1
- **放弃** `V5_GB1_P019` / `group_b1_macd_grid` / `GB1 MACD 8/21/5`：未通过阶段1
- **放弃** `V5_GB1_P020` / `group_b1_macd_grid` / `GB1 MACD 8/21/7`：未通过阶段1
- **放弃** `V5_GB1_P021` / `group_b1_macd_grid` / `GB1 MACD 8/21/9`：未通过阶段1
- **放弃** `V5_GB1_P022` / `group_b1_macd_grid` / `GB1 MACD 8/26/5`：未通过阶段1
- **放弃** `V5_GB1_P023` / `group_b1_macd_grid` / `GB1 MACD 8/26/7`：未通过阶段1
- **放弃** `V5_GB1_P024` / `group_b1_macd_grid` / `GB1 MACD 8/26/9`：未通过阶段1
- **放弃** `V5_GB1_P025` / `group_b1_macd_grid` / `GB1 MACD 10/15/5`：未通过阶段1
- **放弃** `V5_GB1_P026` / `group_b1_macd_grid` / `GB1 MACD 10/15/7`：未通过阶段1
- **放弃** `V5_GB1_P027` / `group_b1_macd_grid` / `GB1 MACD 10/15/9`：未通过阶段1
- **放弃** `V5_GB1_P028` / `group_b1_macd_grid` / `GB1 MACD 10/17/5`：未通过阶段1
- **放弃** `V5_GB1_P029` / `group_b1_macd_grid` / `GB1 MACD 10/17/7`：未通过阶段1
- **放弃** `V5_GB1_P030` / `group_b1_macd_grid` / `GB1 MACD 10/17/9`：未通过阶段1
- **放弃** `V5_GB1_P031` / `group_b1_macd_grid` / `GB1 MACD 10/21/5`：未通过阶段1
- **放弃** `V5_GB1_P032` / `group_b1_macd_grid` / `GB1 MACD 10/21/7`：未通过阶段1
- **放弃** `V5_GB1_P033` / `group_b1_macd_grid` / `GB1 MACD 10/21/9`：未通过阶段1
- **放弃** `V5_GB1_P034` / `group_b1_macd_grid` / `GB1 MACD 10/26/5`：未通过阶段1
- **放弃** `V5_GB1_P035` / `group_b1_macd_grid` / `GB1 MACD 10/26/7`：未通过阶段1
- **放弃** `V5_GB1_P036` / `group_b1_macd_grid` / `GB1 MACD 10/26/9`：未通过阶段1
- **放弃** `V5_GB1_P037` / `group_b1_macd_grid` / `GB1 MACD 12/17/5`：未通过阶段1
- **放弃** `V5_GB1_P038` / `group_b1_macd_grid` / `GB1 MACD 12/17/7`：未通过阶段1
- **放弃** `V5_GB1_P039` / `group_b1_macd_grid` / `GB1 MACD 12/17/9`：未通过阶段1
- **放弃** `V5_GB1_P040` / `group_b1_macd_grid` / `GB1 MACD 12/21/5`：未通过阶段1
- **放弃** `V5_GB1_P041` / `group_b1_macd_grid` / `GB1 MACD 12/21/7`：未通过阶段1
- **放弃** `V5_GB1_P042` / `group_b1_macd_grid` / `GB1 MACD 12/21/9`：未通过阶段1
- **放弃** `V5_GB1_P043` / `group_b1_macd_grid` / `GB1 MACD 12/26/5`：未通过阶段1
- **放弃** `V5_GB1_P044` / `group_b1_macd_grid` / `GB1 MACD 12/26/7`：未通过阶段1
- **放弃** `V5_GB1_P045` / `group_b1_macd_grid` / `GB1 MACD 12/26/9`：未通过阶段1
- **放弃** `V5_GB1_P046` / `group_b1_macd_grid` / `GB1 MACD 14/21/5`：未通过阶段1
- **放弃** `V5_GB1_P047` / `group_b1_macd_grid` / `GB1 MACD 14/21/7`：未通过阶段1
- **放弃** `V5_GB1_P048` / `group_b1_macd_grid` / `GB1 MACD 14/21/9`：未通过阶段1
- **放弃** `V5_GB1_P049` / `group_b1_macd_grid` / `GB1 MACD 14/26/5`：未通过阶段1
- **放弃** `V5_GB1_P050` / `group_b1_macd_grid` / `GB1 MACD 14/26/7`：未通过阶段1
- **放弃** `V5_GB1_P051` / `group_b1_macd_grid` / `GB1 MACD 14/26/9`：未通过阶段1
- **放弃** `V5_GB2_P001` / `group_b2_macd_modes` / `GB2 8/17/9 hist_rise`：未通过阶段1
- **放弃** `V5_GB2_P002` / `group_b2_macd_modes` / `GB2 8/17/9 hist_pos`：未通过阶段1
- **放弃** `V5_GB2_P003` / `group_b2_macd_modes` / `GB2 8/17/9 macd_above_sig`：未通过阶段1
- **放弃** `V5_GB2_P004` / `group_b2_macd_modes` / `GB2 8/17/9 macd_above_rise`：未通过阶段1
- **放弃** `V5_GB2_P005` / `group_b2_macd_modes` / `GB2 8/17/9 hist_rise2`：未通过阶段1
- **放弃** `V5_GB2_P006` / `group_b2_macd_modes` / `GB2 8/17/9 no_macd`：未通过阶段1
- **放弃** `V5_GB2_P007` / `group_b2_macd_modes` / `GB2 12/26/9 hist_rise`：未通过阶段1
- **放弃** `V5_GB2_P008` / `group_b2_macd_modes` / `GB2 12/26/9 hist_pos`：未通过阶段1
- **放弃** `V5_GB2_P009` / `group_b2_macd_modes` / `GB2 12/26/9 macd_above_sig`：未通过阶段1
- **放弃** `V5_GB2_P010` / `group_b2_macd_modes` / `GB2 12/26/9 macd_above_rise`：未通过阶段1
- **放弃** `V5_GB2_P011` / `group_b2_macd_modes` / `GB2 12/26/9 hist_rise2`：未通过阶段1
- **放弃** `V5_GB2_P012` / `group_b2_macd_modes` / `GB2 12/26/9 no_macd`：未通过阶段1
- **放弃** `V5_GB3_P001` / `group_b3_alternatives` / `GB3 EMA slope p=5 th=0.001`：未通过阶段1
- **放弃** `V5_GB3_P002` / `group_b3_alternatives` / `GB3 EMA slope p=5 th=0.002`：未通过阶段1
- **放弃** `V5_GB3_P003` / `group_b3_alternatives` / `GB3 EMA slope p=8 th=0.001`：未通过阶段1
- **放弃** `V5_GB3_P004` / `group_b3_alternatives` / `GB3 EMA slope p=8 th=0.002`：未通过阶段1
- **放弃** `V5_GB3_P005` / `group_b3_alternatives` / `GB3 Stoch K=14`：未通过阶段1
- **放弃** `V5_GB3_P006` / `group_b3_alternatives` / `GB3 Stoch K=21`：未通过阶段1
- **放弃** `V5_GB3_P007` / `group_b3_alternatives` / `GB3 dual MACD+Stoch K=14`：未通过阶段1
- **放弃** `V5_GB3_P008` / `group_b3_alternatives` / `GB3 dual MACD+Stoch K=21`：未通过阶段1
- **放弃** `V5_GC_P001` / `group_c_dc_grid` / `GC DC 10/30`：未通过阶段1
- **放弃** `V5_GC_P002` / `group_c_dc_grid` / `GC DC 10/35`：未通过阶段1
- **放弃** `V5_GC_P003` / `group_c_dc_grid` / `GC DC 10/40`：未通过阶段1
- **放弃** `V5_GC_P004` / `group_c_dc_grid` / `GC DC 10/45`：未通过阶段1
- **放弃** `V5_GC_P005` / `group_c_dc_grid` / `GC DC 12/30`：未通过阶段1
- **放弃** `V5_GC_P006` / `group_c_dc_grid` / `GC DC 12/35`：未通过阶段1
- **放弃** `V5_GC_P007` / `group_c_dc_grid` / `GC DC 12/40`：未通过阶段1
- **放弃** `V5_GC_P008` / `group_c_dc_grid` / `GC DC 12/45`：未通过阶段1
- **放弃** `V5_GC_P009` / `group_c_dc_grid` / `GC DC 14/30`：未通过阶段1
- **放弃** `V5_GC_P010` / `group_c_dc_grid` / `GC DC 14/35`：未通过阶段1
- **放弃** `V5_GC_P011` / `group_c_dc_grid` / `GC DC 14/40`：未通过阶段1
- **放弃** `V5_GC_P012` / `group_c_dc_grid` / `GC DC 14/45`：未通过阶段1
- **放弃** `V5_GC_P013` / `group_c_dc_grid` / `GC DC 16/35`：未通过阶段1
- **放弃** `V5_GC_P014` / `group_c_dc_grid` / `GC DC 16/40`：未通过阶段1
- **放弃** `V5_GC_P015` / `group_c_dc_grid` / `GC DC 16/45`：未通过阶段1
- **放弃** `V5_GC_P016` / `group_c_dc_grid` / `GC DC 18/35`：未通过阶段1
- **放弃** `V5_GC_P017` / `group_c_dc_grid` / `GC DC 18/40`：未通过阶段1
- **放弃** `V5_GC_P018` / `group_c_dc_grid` / `GC DC 18/45`：未通过阶段1
- **放弃** `V5_GC_P019` / `group_c_dc_grid` / `GC DC 20/40`：未通过阶段1
- **放弃** `V5_GC_P020` / `group_c_dc_grid` / `GC DC 20/45`：未通过阶段1
- **放弃** `V5_GD1_P001` / `group_d1_baseline_v11` / `GD1 CryptoV11 baseline`：未通过阶段1
- **放弃** `V5_GD2_P001` / `group_d2_baseline_v10` / `GD2 CryptoV10 baseline`：未通过阶段1
- **放弃** `V5_GD3_P001` / `group_d3_ablation` / `GD3 No G6 fixed DC20 + MACD`：未通过阶段1
- **放弃** `V5_GD3_P002` / `group_d3_ablation` / `GD3 No G2 MACD filter`：未通过阶段1
- **放弃** `V5_GD3_P003` / `group_d3_ablation` / `GD3 No stair S5`：未通过阶段1
- **放弃** `V5_GD3_P004` / `group_d3_ablation` / `GD3 COOLDOWN_BARS=0`：未通过阶段1
- **放弃** `V5_GD3_P005` / `group_d3_ablation` / `GD3 DAILY_MAX_LOSSES=999`：未通过阶段1
- **放弃** `V5_GD3_P006` / `group_d3_ablation` / `GD3 ATR_MULT=0`：未通过阶段1
- **放弃** `V5_GD3_P007` / `group_d3_ablation` / `GD3 No 4H EMA confirm`：未通过阶段1
- **放弃** `V5_GD3_P008` / `group_d3_ablation` / `GD3 No ADX rising`：未通过阶段1

## 7. 失败方向总结（按 group，避免重复踩坑）

### group `group_a1_trailing`

- **失败** `V5_GA1_P016` / `GA1 trail 0.04/0.2`：PF<1.3 (Sharpe=0.95, PF=1.27, 交易=1195, 回撤%=13.22)
- **失败** `V5_GA1_P021` / `GA1 trail 0.05/0.2`：Sharpe<0.9；PF<1.3 (Sharpe=0.86, PF=1.24, 交易=1190, 回撤%=13.66)
- **失败** `V5_GA1_P026` / `GA1 trail 0.06/0.2`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.22, 交易=1182, 回撤%=14.23)

### group `group_a2_stoploss`

- **失败** `V5_GA2_P002` / `GA2 sl=-0.06 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.64, PF=1.22, 交易=1103, 回撤%=27.39)
- **失败** `V5_GA2_P001` / `GA2 sl=-0.06 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.66, PF=1.23, 交易=1105, 回撤%=27.02)
- **失败** `V5_GA2_P004` / `GA2 sl=-0.07 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.79, PF=1.27, 交易=1091, 回撤%=24.64)
- **失败** `V5_GA2_P003` / `GA2 sl=-0.07 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.29, 交易=1096, 回撤%=23.50)

### group `group_a5_max_bars`

- **失败** `V5_GA5_P015` / `GA5 MAX_BARS=128 timeout=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GA5_P016` / `GA5 MAX_BARS=128 timeout=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GA5_P017` / `GA5 MAX_BARS=144 timeout=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GA5_P018` / `GA5 MAX_BARS=144 timeout=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GA5_P019` / `GA5 MAX_BARS=160 timeout=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GA5_P020` / `GA5 MAX_BARS=160 timeout=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GA5_P002` / `GA5 MAX_BARS=32 timeout=-0.03`：Sharpe<0.9 (Sharpe=0.89, PF=1.30, 交易=1139, 回撤%=15.22)
- **失败** `V5_GA5_P021` / `GA5 MAX_BARS=64 timeout=-0.025`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_b1_macd_grid`

- **失败** `V5_GB1_P025` / `GB1 MACD 10/15/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P026` / `GB1 MACD 10/15/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P027` / `GB1 MACD 10/15/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P028` / `GB1 MACD 10/17/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P029` / `GB1 MACD 10/17/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P030` / `GB1 MACD 10/17/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P031` / `GB1 MACD 10/21/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P032` / `GB1 MACD 10/21/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P033` / `GB1 MACD 10/21/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P034` / `GB1 MACD 10/26/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P035` / `GB1 MACD 10/26/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P036` / `GB1 MACD 10/26/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P037` / `GB1 MACD 12/17/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P038` / `GB1 MACD 12/17/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P039` / `GB1 MACD 12/17/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P040` / `GB1 MACD 12/21/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P041` / `GB1 MACD 12/21/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P042` / `GB1 MACD 12/21/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P043` / `GB1 MACD 12/26/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P044` / `GB1 MACD 12/26/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P045` / `GB1 MACD 12/26/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P046` / `GB1 MACD 14/21/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P047` / `GB1 MACD 14/21/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P048` / `GB1 MACD 14/21/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P049` / `GB1 MACD 14/26/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P050` / `GB1 MACD 14/26/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P051` / `GB1 MACD 14/26/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P001` / `GB1 MACD 6/15/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P002` / `GB1 MACD 6/15/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P003` / `GB1 MACD 6/15/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P004` / `GB1 MACD 6/17/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P005` / `GB1 MACD 6/17/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P006` / `GB1 MACD 6/17/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P007` / `GB1 MACD 6/21/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P008` / `GB1 MACD 6/21/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P009` / `GB1 MACD 6/21/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P010` / `GB1 MACD 6/26/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P011` / `GB1 MACD 6/26/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P012` / `GB1 MACD 6/26/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P013` / `GB1 MACD 8/15/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P014` / `GB1 MACD 8/15/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P015` / `GB1 MACD 8/15/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P016` / `GB1 MACD 8/17/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P017` / `GB1 MACD 8/17/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P018` / `GB1 MACD 8/17/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P019` / `GB1 MACD 8/21/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P020` / `GB1 MACD 8/21/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P021` / `GB1 MACD 8/21/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P022` / `GB1 MACD 8/26/5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P023` / `GB1 MACD 8/26/7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB1_P024` / `GB1 MACD 8/26/9`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_b2_macd_modes`

- **失败** `V5_GB2_P008` / `GB2 12/26/9 hist_pos`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P007` / `GB2 12/26/9 hist_rise`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P011` / `GB2 12/26/9 hist_rise2`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P010` / `GB2 12/26/9 macd_above_rise`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P009` / `GB2 12/26/9 macd_above_sig`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P012` / `GB2 12/26/9 no_macd`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P002` / `GB2 8/17/9 hist_pos`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P001` / `GB2 8/17/9 hist_rise`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P005` / `GB2 8/17/9 hist_rise2`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P004` / `GB2 8/17/9 macd_above_rise`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P003` / `GB2 8/17/9 macd_above_sig`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB2_P006` / `GB2 8/17/9 no_macd`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_b3_alternatives`

- **失败** `V5_GB3_P001` / `GB3 EMA slope p=5 th=0.001`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB3_P002` / `GB3 EMA slope p=5 th=0.002`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB3_P003` / `GB3 EMA slope p=8 th=0.001`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB3_P004` / `GB3 EMA slope p=8 th=0.002`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB3_P005` / `GB3 Stoch K=14`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB3_P006` / `GB3 Stoch K=21`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB3_P007` / `GB3 dual MACD+Stoch K=14`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GB3_P008` / `GB3 dual MACD+Stoch K=21`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_c_dc_grid`

- **失败** `V5_GC_P001` / `GC DC 10/30`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P002` / `GC DC 10/35`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P003` / `GC DC 10/40`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P004` / `GC DC 10/45`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P005` / `GC DC 12/30`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P006` / `GC DC 12/35`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P007` / `GC DC 12/40`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P008` / `GC DC 12/45`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P009` / `GC DC 14/30`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P010` / `GC DC 14/35`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P011` / `GC DC 14/40`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P012` / `GC DC 14/45`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P013` / `GC DC 16/35`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P014` / `GC DC 16/40`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P015` / `GC DC 16/45`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P016` / `GC DC 18/35`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P017` / `GC DC 18/40`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P018` / `GC DC 18/45`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P019` / `GC DC 20/40`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GC_P020` / `GC DC 20/45`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_d1_baseline_v11`

- **失败** `V5_GD1_P001` / `GD1 CryptoV11 baseline`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_d2_baseline_v10`

- **失败** `V5_GD2_P001` / `GD2 CryptoV10 baseline`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_d3_ablation`

- **失败** `V5_GD3_P006` / `GD3 ATR_MULT=0`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GD3_P004` / `GD3 COOLDOWN_BARS=0`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GD3_P005` / `GD3 DAILY_MAX_LOSSES=999`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GD3_P007` / `GD3 No 4H EMA confirm`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GD3_P008` / `GD3 No ADX rising`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GD3_P002` / `GD3 No G2 MACD filter`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GD3_P001` / `GD3 No G6 fixed DC20 + MACD`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V5_GD3_P003` / `GD3 No stair S5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

## 附录：脚本门控参数（可复制到流水线配置）

```json
{
  "STAGE1_MIN_SHARPE": 0.9,
  "STAGE1_MIN_PF": 1.3,
  "STAGE1_MIN_TRADES": 800,
  "STAGE1_MAX_DD": 25.0,
  "STAGE2_MAX_CV_STABLE": 0.5,
  "STAGE2_MAX_CV_ACCEPTABLE": 0.8,
  "STAGE3_PASS_MIN_OOS": 0.5,
  "STRONG_REC_MIN_OOS": 0.8,
  "NEIGHBOR_SMOOTH_STD": 0.1,
  "BASELINE_FULL": {
    "sharpe": 1.21,
    "profit_factor": 1.5,
    "max_drawdown_pct": 11.24,
    "tot_profit_pct": 1398,
    "trades": 1098
  }
}
```
