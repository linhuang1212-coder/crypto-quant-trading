# V4 三阶段回测分析报告

- 生成路径: `C:\Users\hlin2\freqtrade\user_data\experiment_results\v4_analysis.md`
- 数据根目录: `C:\Users\hlin2\freqtrade`

## 1. 全样本排名（Top 20，按 Sharpe 降序）

基线参考: Sharpe **1.15**, PF **1.46**, 最大回撤 **13.05%**, 总利润 **1302.0%**, 交易数 **1115**。

| 排名 | strategy | group | name | Sharpe | PF | 利润% | 回撤% | 交易数 | 超越基线(分项) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | V4_G6_P010 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.7 | 1.18 | 1.48 | 1390.1 | 6.0 | 1119 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 2 | V4_G6_P010 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.7 | 1.18 | 1.48 | 1390.1 | 12.2 | 1119 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 3 | V4_G6_P008 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=40 th=0.3 | 1.17 | 1.48 | 1378.0 | 7.0 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 4 | V4_G6_P008 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=40 th=0.3 | 1.17 | 1.48 | 1378.0 | 12.9 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 5 | V4_G8_P005 | group8_stair_grid | G8 stair 16b/-0.06 40b/-0.04 | 1.17 | 1.46 | 1275.3 | 2.0 | 1118 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 6 | V4_G8_P005 | group8_stair_grid | G8 stair 16b/-0.06 40b/-0.04 | 1.17 | 1.46 | 1275.3 | 12.1 | 1118 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 7 | V4_G2_P017 | group2_macd | G2 MACD f8s17sig9 hist_pos stair=True | 1.16 | 1.47 | 1277.3 | 12.1 | 1097 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 8 | V4_G2_P019 | group2_macd | G2 MACD f8s17sig9 hist_rise stair=True | 1.16 | 1.47 | 1226.2 | 12.1 | 1093 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 9 | V4_G2_P023 | group2_macd | G2 MACD f8s17sig9 macd_sig_hist stair=True | 1.16 | 1.47 | 1277.3 | 12.1 | 1097 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 10 | V4_G3_P014 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=True | 1.16 | 1.46 | 1324.0 | 6.0 | 1110 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 11 | V4_G3_P014 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=True | 1.16 | 1.46 | 1324.0 | 13.1 | 1110 | Sharpe:✓ PF:✓ 回撤:× 利润%:✓ 交易数:× |
| 12 | V4_G6_P003 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.16 | 1.46 | 1355.9 | 7.0 | 1117 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 13 | V4_G6_P005 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=35 th=0.5 | 1.16 | 1.48 | 1409.6 | 4.0 | 1103 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 14 | V4_G6_P003 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.16 | 1.46 | 1355.9 | 12.2 | 1117 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 15 | V4_G6_P005 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=35 th=0.5 | 1.16 | 1.48 | 1409.6 | 13.4 | 1103 | Sharpe:✓ PF:✓ 回撤:× 利润%:✓ 交易数:× |
| 16 | V4_G6_P011 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.3 | 1.16 | 1.47 | 1319.0 | 7.0 | 1101 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 17 | V4_G6_P014 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.3 | 1.16 | 1.48 | 1362.7 | 6.0 | 1100 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 18 | V4_G6_P011 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.3 | 1.16 | 1.47 | 1319.0 | 12.2 | 1101 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 19 | V4_G6_P014 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.3 | 1.16 | 1.48 | 1362.7 | 12.9 | 1100 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 20 | V4_G6_P017 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.16 | 1.46 | 1355.9 | 7.0 | 1117 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |

<details><summary>Top20 的 params 摘要（展开）</summary>

| 排名 | params |
| --- | --- |
| 1 | `{"lookback":100,"dc_short":14,"dc_long":40,"atr_pct_threshold":0.7}` |
| 2 | `{"lookback":100,"dc_short":14,"dc_long":40,"atr_pct_threshold":0.7}` |
| 3 | `{"lookback":100,"dc_short":16,"dc_long":40,"atr_pct_threshold":0.3}` |
| 4 | `{"lookback":100,"dc_short":16,"dc_long":40,"atr_pct_threshold":0.3}` |
| 5 | `{"bars1":16,"loss1":-0.06,"bars2":40,"loss2":-0.04}` |
| 6 | `{"bars1":16,"loss1":-0.06,"bars2":40,"loss2":-0.04}` |
| 7 | `{"macd":[8,17,9],"mode":"hist_pos","stair":true}` |
| 8 | `{"macd":[8,17,9],"mode":"hist_rise","stair":true}` |
| 9 | `{"macd":[8,17,9],"mode":"macd_sig_hist","stair":true}` |
| 10 | `{"slope_period":8,"threshold":0.001,"stair":true}` |
| 11 | `{"slope_period":8,"threshold":0.001,"stair":true}` |
| 12 | `{"lookback":50,"dc_short":16,"dc_long":40,"atr_pct_threshold":0.7}` |
| 13 | `{"lookback":100,"dc_short":16,"dc_long":35,"atr_pct_threshold":0.5}` |
| 14 | `{"lookback":50,"dc_short":16,"dc_long":40,"atr_pct_threshold":0.7}` |
| 15 | `{"lookback":100,"dc_short":16,"dc_long":35,"atr_pct_threshold":0.5}` |
| 16 | `{"lookback":50,"dc_short":14,"dc_long":40,"atr_pct_threshold":0.3}` |
| 17 | `{"lookback":100,"dc_short":14,"dc_long":40,"atr_pct_threshold":0.3}` |
| 18 | `{"lookback":50,"dc_short":14,"dc_long":40,"atr_pct_threshold":0.3}` |
| 19 | `{"lookback":100,"dc_short":14,"dc_long":40,"atr_pct_threshold":0.3}` |
| 20 | `{"lookback":50,"dc_short":16,"dc_long":40,"atr_pct_threshold":0.7}` |

</details>

## 2. 分组汇总

| group | 策略数 | 阶段1通过率 | 组均Sharpe | 最优 name | 最优Sharpe | 分年度验证 | Walk-Forward | 邻域std标签 | 结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| group10_stoch | 48 | 58% | 0.88 | G10 Stoch K=21 D=3 th>60 stair=True | 1.14 | 稳定 (CV=0.43, 12/12年盈利) | 无过拟合 (OOS=1.25) | 平滑 (0.00) | 推荐 |
| group11_trend_score | 60 | 0% | 0.85 | G11 score>0.8 w_slope2 stair=True | 0.91 | — | — | 平滑 (0.00) | 放弃 |
| group1_dc_exit | 53 | 0% | 0.48 | G1 DCexit p=15 dc_trail_stair mb=8 | 0.71 | — | — | 平滑 (0.00) | 放弃 |
| group2_macd | 48 | 77% | 0.83 | G2 MACD f8s17sig9 hist_pos stair=True | 1.16 | 稳定 (CV=0.44, 12/12年盈利) | 无过拟合 (OOS=1.31) | 敏感 (0.58) | 推荐 |
| group3_ema_slope | 36 | 83% | 0.90 | G3 EMA slope p=8 th=0.001 stair=True | 1.16 | 稳定 (CV=0.45, 12/12年盈利) | 无过拟合 (OOS=1.25) | 平滑 (0.00) | 推荐 |
| group4_1h_confirm | 36 | 0% | 0.00 | G4 1H 1h_only adx1h>0 stair=True | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group5_profit_giveback | 50 | 0% | 0.68 | G5 giveback mp=0.08 kr=0.7 stair=True | 0.86 | — | — | 平滑 (0.00) | 放弃 |
| group6_dynamic_dc | 40 | 98% | 1.12 | G6 dynDC lb=100 s=14 L=40 th=0.7 | 1.18 | 稳定 (CV=0.41, 12/12年盈利) | 无过拟合 (OOS=1.28) | 平滑 (0.00) | 推荐 |
| group7_per_pair_params | 64 | 0% | 0.32 | G7 SOL/USDT:USDT ADX=28 ATR=0.6 DC=20 | 0.44 | — | — | 平滑 (0.00) | 放弃 |
| group8_stair_grid | 72 | 99% | 1.07 | G8 stair 16b/-0.06 40b/-0.04 | 1.17 | 稳定 (CV=0.43, 12/12年盈利) | 无过拟合 (OOS=1.27) | 平滑 (0.00) | 推荐 |
| group9_hour_filter | 48 | 0% | 0.00 | G9 exclude [0,4) UTC stair=True | 0.00 | — | — | 平滑 (0.00) | 放弃 |

> 分年度参考：参考：2020:+78% Sharpe1.62 / 2021:+110% Sharpe1.82 / 2022:+8.7% Sharpe0.27 / 2023:+70% Sharpe1.26 / 2024:+34% Sharpe1.09 / 2025Q1:+44% Sharpe1.01

## 3. 参数邻域稳定性（阶段1，按 group × strategy）

在同一 `strategy`+`group` 内，对所有变体的 Sharpe 计算总体标准差；并按 `name` 字典序相邻检测尖峰（高于邻居最大值超过 0.3）。

| strategy | group | 变体数 | Sharpe std | 稳定性 | 尖峰标记(若有) |
| --- | --- | --- | --- | --- | --- |
| V4_G10_P001 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P002 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P003 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P004 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P005 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P006 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P007 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P008 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P009 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P010 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P011 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P012 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P013 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P014 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P015 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P016 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P017 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P018 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P019 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P020 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P021 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P022 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P023 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G10_P024 | group10_stoch | 2 | 0.00 | 平滑 | — |
| V4_G11_P001 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P002 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P003 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P004 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P005 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P006 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P007 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P008 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P009 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P010 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P011 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P012 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P013 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P014 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P015 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P016 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P017 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P018 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P019 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P020 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P021 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P022 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P023 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P024 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P025 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P026 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P027 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P028 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P029 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G11_P030 | group11_trend_score | 2 | 0.00 | 平滑 | — |
| V4_G1_P001 | group1_dc_exit | 1 | 0.00 | 平滑 | — |
| V4_G1_P002 | group1_dc_exit | 1 | 0.00 | 平滑 | — |
| V4_G1_P003 | group1_dc_exit | 1 | 0.00 | 平滑 | — |
| V4_G1_P004 | group1_dc_exit | 1 | 0.00 | 平滑 | — |
| V4_G1_P005 | group1_dc_exit | 1 | 0.00 | 平滑 | — |
| V4_G1_P006 | group1_dc_exit | 1 | 0.00 | 平滑 | — |
| V4_G1_P007 | group1_dc_exit | 1 | 0.00 | 平滑 | — |
| V4_G1_P008 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P009 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P010 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P011 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P012 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P013 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P014 | group1_dc_exit | 2 | 0.14 | 正常 | — |
| V4_G1_P015 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P016 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P017 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P018 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P019 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P020 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P021 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P022 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P023 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P024 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P025 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P026 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P027 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P028 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P029 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G1_P030 | group1_dc_exit | 2 | 0.00 | 平滑 | — |
| V4_G2_P001 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P002 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P003 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P004 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P005 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P006 | group2_macd | 2 | 0.51 | 敏感 | G2 MACD f8s21sig5 macd_pos stair=False: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f8s21sig5 macd_pos stair=False: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P007 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P008 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P009 | group2_macd | 2 | 0.57 | 敏感 | G2 MACD f12s26sig9 hist_pos stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f12s26sig9 hist_pos stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P010 | group2_macd | 2 | 0.50 | 敏感 | G2 MACD f12s26sig9 hist_pos stair=False: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f12s26sig9 hist_pos stair=False: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P011 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P012 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P013 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P014 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P015 | group2_macd | 2 | 0.57 | 敏感 | G2 MACD f12s26sig9 macd_sig_hist stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f12s26sig9 macd_sig_hist stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P016 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P017 | group2_macd | 2 | 0.58 | 敏感 | G2 MACD f8s17sig9 hist_pos stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f8s17sig9 hist_pos stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P018 | group2_macd | 2 | 0.52 | 敏感 | G2 MACD f8s17sig9 hist_pos stair=False: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f8s17sig9 hist_pos stair=False: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P019 | group2_macd | 2 | 0.58 | 敏感 | G2 MACD f8s17sig9 hist_rise stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f8s17sig9 hist_rise stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P020 | group2_macd | 2 | 0.51 | 敏感 | G2 MACD f8s17sig9 hist_rise stair=False: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f8s17sig9 hist_rise stair=False: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P021 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P022 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G2_P023 | group2_macd | 2 | 0.58 | 敏感 | G2 MACD f8s17sig9 macd_sig_hist stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G2 MACD f8s17sig9 macd_sig_hist stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G2_P024 | group2_macd | 2 | 0.00 | 平滑 | — |
| V4_G3_P001 | group3_ema_slope | 2 | 0.57 | 敏感 | G3 EMA slope p=3 th=0.0005 stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G3 EMA slope p=3 th=0.0005 stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G3_P002 | group3_ema_slope | 2 | 0.56 | 敏感 | G3 EMA slope p=3 th=0.001 stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G3 EMA slope p=3 th=0.001 stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G3_P003 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P004 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P005 | group3_ema_slope | 2 | 0.46 | 敏感 | G3 EMA slope p=3 th=0.002 stair=False: 可能过拟合（Sharpe 显著高于相邻变体）; G3 EMA slope p=3 th=0.002 stair=False: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G3_P006 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P007 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P008 | group3_ema_slope | 2 | 0.57 | 敏感 | G3 EMA slope p=5 th=0.001 stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G3 EMA slope p=5 th=0.001 stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G3_P009 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P010 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P011 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P012 | group3_ema_slope | 2 | 0.43 | 敏感 | G3 EMA slope p=5 th=0.003 stair=True: 可能过拟合（Sharpe 显著高于相邻变体）; G3 EMA slope p=5 th=0.003 stair=True: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G3_P013 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P014 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P015 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P016 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P017 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G3_P018 | group3_ema_slope | 2 | 0.00 | 平滑 | — |
| V4_G4_P001 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P002 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P003 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P004 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P005 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P006 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P007 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P008 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P009 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P010 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P011 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P012 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P013 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P014 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P015 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P016 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P017 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G4_P018 | group4_1h_confirm | 2 | 0.00 | 平滑 | — |
| V4_G5_P001 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P002 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P003 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P004 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P005 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P006 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P007 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P008 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P009 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P010 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P011 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P012 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P013 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P014 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P015 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P016 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P017 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P018 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P019 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P020 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P021 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P022 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P023 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P024 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G5_P025 | group5_profit_giveback | 2 | 0.00 | 平滑 | — |
| V4_G6_P001 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P002 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P003 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P004 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P005 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P006 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P007 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P008 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P009 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P010 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P011 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P012 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P013 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P014 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P015 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P016 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P017 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P018 | group6_dynamic_dc | 2 | 0.58 | 敏感 | G6 dynDC lb=100 s=16 L=30 th=0.7: 可能过拟合（Sharpe 显著高于相邻变体）; G6 dynDC lb=100 s=16 L=30 th=0.7: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G6_P019 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G6_P020 | group6_dynamic_dc | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG01 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG02 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG03 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG04 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG05 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG06 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG07 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ADA_PG08 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG01 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG02 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG03 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG04 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG05 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG06 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG07 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_BTC_PG08 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG01 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG02 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG03 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG04 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG05 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG06 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG07 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_ETH_PG08 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG01 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG02 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG03 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG04 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG05 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG06 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG07 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G7_SOL_PG08 | group7_per_pair_params | 2 | 0.00 | 平滑 | — |
| V4_G8_P001 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P002 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P003 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P004 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P005 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P006 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P007 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P008 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P009 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P010 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P011 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P012 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P013 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P014 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P015 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P016 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P017 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P018 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P019 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P020 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P021 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P022 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P023 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P024 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P025 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P026 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P027 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P028 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P029 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P030 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P031 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P032 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P033 | group8_stair_grid | 2 | 0.54 | 敏感 | G8 stair 24b/-0.06 40b/-0.05: 可能过拟合（Sharpe 显著高于相邻变体）; G8 stair 24b/-0.06 40b/-0.05: 可能过拟合（Sharpe 显著高于相邻变体） |
| V4_G8_P034 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P035 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G8_P036 | group8_stair_grid | 2 | 0.00 | 平滑 | — |
| V4_G9_P001 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P002 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P003 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P004 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P005 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P006 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P007 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P008 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P009 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P010 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P011 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P012 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P013 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P014 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P015 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P016 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P017 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P018 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P019 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P020 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P021 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P022 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P023 | group9_hour_filter | 2 | 0.00 | 平滑 | — |
| V4_G9_P024 | group9_hour_filter | 2 | 0.00 | 平滑 | — |

## 4. 分年度一致性（仅阶段1已通过门控的候选）

规则：**稳定** = CV < 0.5 且全年份盈利；**可接受** = CV < 0.8 且盈利年份≥ max(1, 总年数-1)；否则 **不稳定**。

| strategy | group | name | 全样本Sharpe | 年份数 | 盈利年数 | CV | 2022 Sharpe | 标签 | 阶段2通过 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V4_G6_P010 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.7 | 1.18 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G6_P010 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.7 | 1.18 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G6_P008 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=40 th=0.3 | 1.17 | 12 | 12 | 0.44 | 0.16 | 稳定 | 是 |
| V4_G6_P008 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=40 th=0.3 | 1.17 | 12 | 12 | 0.44 | 0.16 | 稳定 | 是 |
| V4_G8_P005 | group8_stair_grid | G8 stair 16b/-0.06 40b/-0.04 | 1.17 | 12 | 12 | 0.43 | 0.13 | 稳定 | 是 |
| V4_G8_P005 | group8_stair_grid | G8 stair 16b/-0.06 40b/-0.04 | 1.17 | 12 | 12 | 0.43 | 0.13 | 稳定 | 是 |
| V4_G2_P017 | group2_macd | G2 MACD f8s17sig9 hist_pos stair=True | 1.16 | 12 | 12 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G2_P019 | group2_macd | G2 MACD f8s17sig9 hist_rise stair=True | 1.16 | 12 | 12 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G2_P023 | group2_macd | G2 MACD f8s17sig9 macd_sig_hist stair=True | 1.16 | 12 | 12 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G3_P014 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=True | 1.16 | 12 | 12 | 0.45 | 0.12 | 稳定 | 是 |
| V4_G3_P014 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=True | 1.16 | 12 | 12 | 0.45 | 0.12 | 稳定 | 是 |
| V4_G6_P020 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=25 th=0.7 | 1.16 | 12 | 12 | 0.42 | 0.18 | 稳定 | 是 |
| V4_G6_P020 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=25 th=0.7 | 1.16 | 12 | 12 | 0.42 | 0.18 | 稳定 | 是 |
| V4_G6_P014 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.3 | 1.16 | 12 | 12 | 0.45 | 0.12 | 稳定 | 是 |
| V4_G6_P014 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.3 | 1.16 | 12 | 12 | 0.45 | 0.12 | 稳定 | 是 |
| V4_G6_P018 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=30 th=0.7 | 1.16 | 12 | 12 | 0.43 | 0.15 | 稳定 | 是 |
| V4_G6_P005 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=35 th=0.5 | 1.16 | 12 | 12 | 0.42 | 0.24 | 稳定 | 是 |
| V4_G6_P005 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=35 th=0.5 | 1.16 | 12 | 12 | 0.42 | 0.24 | 稳定 | 是 |
| V4_G6_P011 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.3 | 1.16 | 12 | 12 | 0.39 | 0.23 | 稳定 | 是 |
| V4_G6_P011 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.3 | 1.16 | 12 | 12 | 0.39 | 0.23 | 稳定 | 是 |
| V4_G6_P019 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.3 | 1.16 | 12 | 12 | 0.40 | 0.23 | 稳定 | 是 |
| V4_G6_P019 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.3 | 1.16 | 12 | 12 | 0.40 | 0.23 | 稳定 | 是 |
| V4_G6_P003 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.16 | 12 | 12 | 0.39 | 0.28 | 稳定 | 是 |
| V4_G6_P003 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.16 | 12 | 12 | 0.39 | 0.28 | 稳定 | 是 |
| V4_G6_P017 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.16 | 12 | 12 | 0.39 | 0.28 | 稳定 | 是 |
| V4_G6_P017 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.16 | 12 | 12 | 0.39 | 0.28 | 稳定 | 是 |
| V4_G2_P013 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G2_P013 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G2_P021 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G2_P021 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G2_P001 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=True | 1.15 | 6 | 6 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G2_P001 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=True | 1.15 | 6 | 6 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G2_P003 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=True | 1.15 | 6 | 6 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G2_P003 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=True | 1.15 | 6 | 6 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G2_P005 | group2_macd | G2 MACD f8s21sig5 macd_pos stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G2_P005 | group2_macd | G2 MACD f8s21sig5 macd_pos stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G2_P007 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=True | 1.15 | 12 | 12 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G2_P007 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=True | 1.15 | 12 | 12 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G3_P001 | group3_ema_slope | G3 EMA slope p=3 th=0.0005 stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G3_P007 | group3_ema_slope | G3 EMA slope p=5 th=0.0005 stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G3_P007 | group3_ema_slope | G3 EMA slope p=5 th=0.0005 stair=True | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G3_P013 | group3_ema_slope | G3 EMA slope p=8 th=0.0005 stair=True | 1.15 | 12 | 12 | 0.45 | 0.12 | 稳定 | 是 |
| V4_G3_P013 | group3_ema_slope | G3 EMA slope p=8 th=0.0005 stair=True | 1.15 | 12 | 12 | 0.45 | 0.12 | 稳定 | 是 |
| V4_G6_P012 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=30 th=0.5 | 1.15 | 12 | 12 | 0.44 | 0.15 | 稳定 | 是 |
| V4_G6_P012 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=30 th=0.5 | 1.15 | 12 | 12 | 0.44 | 0.15 | 稳定 | 是 |
| V4_G8_P008 | group8_stair_grid | G8 stair 16b/-0.07 44b/-0.04 | 1.15 | 12 | 12 | 0.42 | 0.22 | 稳定 | 是 |
| V4_G8_P008 | group8_stair_grid | G8 stair 16b/-0.07 44b/-0.04 | 1.15 | 12 | 12 | 0.42 | 0.22 | 稳定 | 是 |
| V4_G8_P019 | group8_stair_grid | G8 stair 20b/-0.06 40b/-0.04 | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G8_P019 | group8_stair_grid | G8 stair 20b/-0.06 40b/-0.04 | 1.15 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G10_P017 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=True | 1.14 | 12 | 12 | 0.43 | 0.16 | 稳定 | 是 |
| V4_G10_P017 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=True | 1.14 | 12 | 12 | 0.43 | 0.16 | 稳定 | 是 |
| V4_G10_P021 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=True | 1.14 | 12 | 12 | 0.43 | 0.16 | 稳定 | 是 |
| V4_G10_P021 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=True | 1.14 | 12 | 12 | 0.43 | 0.16 | 稳定 | 是 |
| V4_G2_P009 | group2_macd | G2 MACD f12s26sig9 hist_pos stair=True | 1.14 | 12 | 12 | 0.47 | 0.10 | 稳定 | 是 |
| V4_G2_P011 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=True | 1.14 | 12 | 12 | 0.47 | 0.10 | 稳定 | 是 |
| V4_G2_P011 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=True | 1.14 | 12 | 12 | 0.47 | 0.10 | 稳定 | 是 |
| V4_G2_P015 | group2_macd | G2 MACD f12s26sig9 macd_sig_hist stair=True | 1.14 | 12 | 12 | 0.47 | 0.10 | 稳定 | 是 |
| V4_G3_P008 | group3_ema_slope | G3 EMA slope p=5 th=0.001 stair=True | 1.14 | 12 | 12 | 0.46 | 0.08 | 稳定 | 是 |
| V4_G6_P004 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.3 | 1.14 | 12 | 12 | 0.49 | 0.03 | 稳定 | 是 |
| V4_G6_P004 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.3 | 1.14 | 12 | 12 | 0.49 | 0.03 | 稳定 | 是 |
| V4_G6_P013 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=30 th=0.5 | 1.14 | 12 | 12 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G6_P013 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=30 th=0.5 | 1.14 | 12 | 12 | 0.44 | 0.10 | 稳定 | 是 |
| V4_G6_P002 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.5 | 1.14 | 12 | 12 | 0.41 | 0.17 | 稳定 | 是 |
| V4_G6_P002 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.5 | 1.14 | 12 | 12 | 0.41 | 0.17 | 稳定 | 是 |
| V4_G6_P007 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=25 th=0.7 | 1.14 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G6_P007 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=25 th=0.7 | 1.14 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G6_P015 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.5 | 1.14 | 12 | 12 | 0.41 | 0.20 | 稳定 | 是 |
| V4_G6_P015 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.5 | 1.14 | 12 | 12 | 0.41 | 0.20 | 稳定 | 是 |
| V4_G6_P006 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G6_P006 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G6_P016 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G6_P016 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G6_P001 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.13 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G6_P001 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.13 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G6_P009 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.13 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G6_P009 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.13 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G8_P006 | group8_stair_grid | G8 stair 16b/-0.06 48b/-0.05 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G8_P006 | group8_stair_grid | G8 stair 16b/-0.06 48b/-0.05 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G8_P011 | group8_stair_grid | G8 stair 18b/-0.06 36b/-0.04 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G8_P011 | group8_stair_grid | G8 stair 18b/-0.06 36b/-0.04 | 1.13 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G8_P013 | group8_stair_grid | G8 stair 18b/-0.07 40b/-0.04 | 1.13 | 12 | 12 | 0.42 | 0.21 | 稳定 | 是 |
| V4_G8_P013 | group8_stair_grid | G8 stair 18b/-0.07 40b/-0.04 | 1.13 | 12 | 12 | 0.42 | 0.21 | 稳定 | 是 |
| V4_G8_P020 | group8_stair_grid | G8 stair 20b/-0.06 44b/-0.05 | 1.12 | 12 | 12 | 0.47 | 0.07 | 稳定 | 是 |
| V4_G8_P020 | group8_stair_grid | G8 stair 20b/-0.06 44b/-0.05 | 1.12 | 12 | 12 | 0.47 | 0.07 | 稳定 | 是 |
| V4_G8_P028 | group8_stair_grid | G8 stair 22b/-0.06 48b/-0.04 | 1.12 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G8_P028 | group8_stair_grid | G8 stair 22b/-0.06 48b/-0.04 | 1.12 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G10_P009 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=True | 1.11 | 12 | 12 | 0.45 | 0.13 | 稳定 | 是 |
| V4_G10_P009 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=True | 1.11 | 12 | 12 | 0.45 | 0.13 | 稳定 | 是 |
| V4_G10_P013 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=True | 1.11 | 12 | 12 | 0.45 | 0.13 | 稳定 | 是 |
| V4_G10_P013 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=True | 1.11 | 12 | 12 | 0.45 | 0.13 | 稳定 | 是 |
| V4_G10_P001 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=True | 1.11 | 12 | 12 | 0.48 | 0.09 | 稳定 | 是 |
| V4_G10_P001 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=True | 1.11 | 12 | 12 | 0.48 | 0.09 | 稳定 | 是 |
| V4_G10_P005 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=True | 1.11 | 12 | 12 | 0.48 | 0.09 | 稳定 | 是 |
| V4_G10_P005 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=True | 1.11 | 12 | 12 | 0.48 | 0.09 | 稳定 | 是 |
| V4_G3_P002 | group3_ema_slope | G3 EMA slope p=3 th=0.001 stair=True | 1.11 | 12 | 12 | 0.47 | 0.08 | 稳定 | 是 |
| V4_G8_P014 | group8_stair_grid | G8 stair 18b/-0.07 48b/-0.05 | 1.11 | 12 | 12 | 0.42 | 0.21 | 稳定 | 是 |
| V4_G8_P014 | group8_stair_grid | G8 stair 18b/-0.07 48b/-0.05 | 1.11 | 12 | 12 | 0.42 | 0.21 | 稳定 | 是 |
| V4_G8_P021 | group8_stair_grid | G8 stair 20b/-0.07 36b/-0.04 | 1.11 | 12 | 12 | 0.42 | 0.22 | 稳定 | 是 |
| V4_G8_P021 | group8_stair_grid | G8 stair 20b/-0.07 36b/-0.04 | 1.11 | 12 | 12 | 0.42 | 0.22 | 稳定 | 是 |
| V4_G8_P023 | group8_stair_grid | G8 stair 20b/-0.07 48b/-0.03 | 1.11 | 12 | 12 | 0.46 | 0.12 | 稳定 | 是 |
| V4_G8_P023 | group8_stair_grid | G8 stair 20b/-0.07 48b/-0.03 | 1.11 | 12 | 12 | 0.46 | 0.12 | 稳定 | 是 |
| V4_G3_P016 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=True | 1.10 | 12 | 12 | 0.45 | 0.14 | 稳定 | 是 |
| V4_G3_P016 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=True | 1.10 | 12 | 12 | 0.45 | 0.14 | 稳定 | 是 |
| V4_G8_P004 | group8_stair_grid | G8 stair 16b/-0.06 36b/-0.03 | 1.10 | 12 | 12 | 0.47 | 0.03 | 稳定 | 是 |
| V4_G8_P004 | group8_stair_grid | G8 stair 16b/-0.06 36b/-0.03 | 1.10 | 12 | 12 | 0.47 | 0.03 | 稳定 | 是 |
| V4_G8_P007 | group8_stair_grid | G8 stair 16b/-0.07 40b/-0.03 | 1.10 | 12 | 12 | 0.44 | 0.13 | 稳定 | 是 |
| V4_G8_P007 | group8_stair_grid | G8 stair 16b/-0.07 40b/-0.03 | 1.10 | 12 | 12 | 0.44 | 0.13 | 稳定 | 是 |
| V4_G8_P012 | group8_stair_grid | G8 stair 18b/-0.06 44b/-0.03 | 1.10 | 12 | 12 | 0.48 | 0.00 | 稳定 | 是 |
| V4_G8_P012 | group8_stair_grid | G8 stair 18b/-0.06 44b/-0.03 | 1.10 | 12 | 12 | 0.48 | 0.00 | 稳定 | 是 |
| V4_G8_P018 | group8_stair_grid | G8 stair 20b/-0.06 36b/-0.03 | 1.09 | 12 | 10 | 0.50 | -0.01 | 可接受 | 是 |
| V4_G8_P018 | group8_stair_grid | G8 stair 20b/-0.06 36b/-0.03 | 1.09 | 12 | 10 | 0.50 | -0.01 | 可接受 | 是 |
| V4_G8_P022 | group8_stair_grid | G8 stair 20b/-0.07 40b/-0.05 | 1.09 | 12 | 12 | 0.43 | 0.18 | 稳定 | 是 |
| V4_G8_P022 | group8_stair_grid | G8 stair 20b/-0.07 40b/-0.05 | 1.09 | 12 | 12 | 0.43 | 0.18 | 稳定 | 是 |
| V4_G8_P027 | group8_stair_grid | G8 stair 22b/-0.06 40b/-0.03 | 1.09 | 12 | 12 | 0.42 | 0.13 | 稳定 | 是 |
| V4_G8_P027 | group8_stair_grid | G8 stair 22b/-0.06 40b/-0.03 | 1.09 | 12 | 12 | 0.42 | 0.13 | 稳定 | 是 |
| V4_G8_P026 | group8_stair_grid | G8 stair 22b/-0.06 36b/-0.05 | 1.08 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G8_P026 | group8_stair_grid | G8 stair 22b/-0.06 36b/-0.05 | 1.08 | 12 | 12 | 0.41 | 0.21 | 稳定 | 是 |
| V4_G8_P030 | group8_stair_grid | G8 stair 22b/-0.07 40b/-0.05 | 1.08 | 12 | 12 | 0.43 | 0.17 | 稳定 | 是 |
| V4_G8_P030 | group8_stair_grid | G8 stair 22b/-0.07 40b/-0.05 | 1.08 | 12 | 12 | 0.43 | 0.17 | 稳定 | 是 |
| V4_G8_P033 | group8_stair_grid | G8 stair 24b/-0.06 40b/-0.05 | 1.08 | 12 | 12 | 0.42 | 0.18 | 稳定 | 是 |
| V4_G8_P034 | group8_stair_grid | G8 stair 24b/-0.06 48b/-0.03 | 1.08 | 12 | 12 | 0.46 | 0.10 | 稳定 | 是 |
| V4_G8_P034 | group8_stair_grid | G8 stair 24b/-0.06 48b/-0.03 | 1.08 | 12 | 12 | 0.46 | 0.10 | 稳定 | 是 |
| V4_G8_P035 | group8_stair_grid | G8 stair 24b/-0.07 36b/-0.04 | 1.08 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G8_P035 | group8_stair_grid | G8 stair 24b/-0.07 36b/-0.04 | 1.08 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G3_P010 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=True | 1.07 | 12 | 12 | 0.49 | 0.06 | 稳定 | 是 |
| V4_G3_P010 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=True | 1.07 | 12 | 12 | 0.49 | 0.06 | 稳定 | 是 |
| V4_G8_P015 | group8_stair_grid | G8 stair 20b/-0.05 36b/-0.03 | 1.07 | 12 | 12 | 0.50 | 0.00 | 可接受 | 是 |
| V4_G8_P015 | group8_stair_grid | G8 stair 20b/-0.05 36b/-0.03 | 1.07 | 12 | 12 | 0.50 | 0.00 | 可接受 | 是 |
| V4_G8_P001 | group8_stair_grid | G8 stair 16b/-0.05 36b/-0.03 | 1.06 | 12 | 12 | 0.48 | 0.06 | 稳定 | 是 |
| V4_G8_P001 | group8_stair_grid | G8 stair 16b/-0.05 36b/-0.03 | 1.06 | 12 | 12 | 0.48 | 0.06 | 稳定 | 是 |
| V4_G8_P036 | group8_stair_grid | G8 stair 24b/-0.07 40b/-0.03 | 1.06 | 12 | 12 | 0.45 | 0.09 | 稳定 | 是 |
| V4_G8_P036 | group8_stair_grid | G8 stair 24b/-0.07 40b/-0.03 | 1.06 | 12 | 12 | 0.45 | 0.09 | 稳定 | 是 |
| V4_G8_P002 | group8_stair_grid | G8 stair 16b/-0.05 40b/-0.04 | 1.05 | 12 | 12 | 0.43 | 0.18 | 稳定 | 是 |
| V4_G8_P002 | group8_stair_grid | G8 stair 16b/-0.05 40b/-0.04 | 1.05 | 12 | 12 | 0.43 | 0.18 | 稳定 | 是 |
| V4_G8_P009 | group8_stair_grid | G8 stair 18b/-0.05 36b/-0.03 | 1.05 | 12 | 12 | 0.50 | 0.01 | 稳定 | 是 |
| V4_G8_P009 | group8_stair_grid | G8 stair 18b/-0.05 36b/-0.03 | 1.05 | 12 | 12 | 0.50 | 0.01 | 稳定 | 是 |
| V4_G8_P016 | group8_stair_grid | G8 stair 20b/-0.05 40b/-0.04 | 1.05 | 12 | 12 | 0.46 | 0.11 | 稳定 | 是 |
| V4_G8_P016 | group8_stair_grid | G8 stair 20b/-0.05 40b/-0.04 | 1.05 | 12 | 12 | 0.46 | 0.11 | 稳定 | 是 |
| V4_G8_P029 | group8_stair_grid | G8 stair 22b/-0.07 36b/-0.03 | 1.05 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G8_P029 | group8_stair_grid | G8 stair 22b/-0.07 36b/-0.03 | 1.05 | 12 | 12 | 0.45 | 0.11 | 稳定 | 是 |
| V4_G3_P018 | group3_ema_slope | G3 EMA slope p=8 th=0.003 stair=True | 1.04 | 12 | 12 | 0.51 | 0.06 | 可接受 | 是 |
| V4_G3_P018 | group3_ema_slope | G3 EMA slope p=8 th=0.003 stair=True | 1.04 | 12 | 12 | 0.51 | 0.06 | 可接受 | 是 |
| V4_G8_P024 | group8_stair_grid | G8 stair 22b/-0.05 40b/-0.03 | 1.04 | 12 | 12 | 0.43 | 0.16 | 稳定 | 是 |
| V4_G8_P024 | group8_stair_grid | G8 stair 22b/-0.05 40b/-0.03 | 1.04 | 12 | 12 | 0.43 | 0.16 | 稳定 | 是 |
| V4_G8_P025 | group8_stair_grid | G8 stair 22b/-0.05 44b/-0.04 | 1.04 | 12 | 12 | 0.40 | 0.25 | 稳定 | 是 |
| V4_G8_P025 | group8_stair_grid | G8 stair 22b/-0.05 44b/-0.04 | 1.04 | 12 | 12 | 0.40 | 0.25 | 稳定 | 是 |
| V4_G2_P018 | group2_macd | G2 MACD f8s17sig9 hist_pos stair=False | 1.03 | 12 | 12 | 0.40 | 0.27 | 稳定 | 是 |
| V4_G2_P024 | group2_macd | G2 MACD f8s17sig9 macd_sig_hist stair=False | 1.03 | 12 | 12 | 0.40 | 0.27 | 稳定 | 是 |
| V4_G2_P024 | group2_macd | G2 MACD f8s17sig9 macd_sig_hist stair=False | 1.03 | 12 | 12 | 0.40 | 0.27 | 稳定 | 是 |
| V4_G3_P015 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=False | 1.03 | 12 | 12 | 0.41 | 0.30 | 稳定 | 是 |
| V4_G3_P015 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=False | 1.03 | 12 | 12 | 0.41 | 0.30 | 稳定 | 是 |
| V4_G8_P003 | group8_stair_grid | G8 stair 16b/-0.05 44b/-0.05 | 1.03 | 12 | 12 | 0.44 | 0.16 | 稳定 | 是 |
| V4_G8_P003 | group8_stair_grid | G8 stair 16b/-0.05 44b/-0.05 | 1.03 | 12 | 12 | 0.44 | 0.16 | 稳定 | 是 |
| V4_G8_P017 | group8_stair_grid | G8 stair 20b/-0.05 48b/-0.05 | 1.03 | 12 | 12 | 0.46 | 0.10 | 稳定 | 是 |
| V4_G8_P017 | group8_stair_grid | G8 stair 20b/-0.05 48b/-0.05 | 1.03 | 12 | 12 | 0.46 | 0.10 | 稳定 | 是 |
| V4_G2_P020 | group2_macd | G2 MACD f8s17sig9 hist_rise stair=False | 1.02 | 12 | 12 | 0.41 | 0.27 | 稳定 | 是 |
| V4_G2_P014 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=False | 1.01 | 12 | 12 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G2_P014 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=False | 1.01 | 12 | 12 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G2_P022 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=False | 1.01 | 12 | 12 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G2_P022 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=False | 1.01 | 12 | 12 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G2_P002 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=False | 1.01 | 6 | 6 | 0.41 | 0.27 | 稳定 | 是 |
| V4_G2_P002 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=False | 1.01 | 6 | 6 | 0.41 | 0.27 | 稳定 | 是 |
| V4_G2_P004 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=False | 1.01 | 11 | 11 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G2_P004 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=False | 1.01 | 11 | 11 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G2_P006 | group2_macd | G2 MACD f8s21sig5 macd_pos stair=False | 1.01 | 12 | 12 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G2_P008 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=False | 1.01 | 12 | 12 | 0.41 | 0.27 | 稳定 | 是 |
| V4_G2_P008 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=False | 1.01 | 12 | 12 | 0.41 | 0.27 | 稳定 | 是 |
| V4_G8_P010 | group8_stair_grid | G8 stair 18b/-0.05 40b/-0.05 | 1.01 | 12 | 12 | 0.46 | 0.10 | 稳定 | 是 |
| V4_G8_P010 | group8_stair_grid | G8 stair 18b/-0.05 40b/-0.05 | 1.01 | 12 | 12 | 0.46 | 0.10 | 稳定 | 是 |
| V4_G8_P031 | group8_stair_grid | G8 stair 24b/-0.05 36b/-0.04 | 1.01 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G8_P031 | group8_stair_grid | G8 stair 24b/-0.05 36b/-0.04 | 1.01 | 12 | 12 | 0.42 | 0.20 | 稳定 | 是 |
| V4_G10_P018 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=False | 1.00 | 12 | 12 | 0.41 | 0.33 | 稳定 | 是 |
| V4_G10_P018 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=False | 1.00 | 12 | 12 | 0.41 | 0.33 | 稳定 | 是 |
| V4_G10_P022 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=False | 1.00 | 12 | 12 | 0.41 | 0.33 | 稳定 | 是 |
| V4_G10_P022 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=False | 1.00 | 12 | 12 | 0.41 | 0.33 | 稳定 | 是 |
| V4_G2_P010 | group2_macd | G2 MACD f12s26sig9 hist_pos stair=False | 1.00 | 12 | 12 | 0.44 | 0.28 | 稳定 | 是 |
| V4_G2_P012 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=False | 1.00 | 12 | 12 | 0.44 | 0.28 | 稳定 | 是 |
| V4_G2_P012 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=False | 1.00 | 12 | 12 | 0.44 | 0.28 | 稳定 | 是 |
| V4_G3_P009 | group3_ema_slope | G3 EMA slope p=5 th=0.001 stair=False | 1.00 | 12 | 12 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G3_P009 | group3_ema_slope | G3 EMA slope p=5 th=0.001 stair=False | 1.00 | 12 | 12 | 0.42 | 0.27 | 稳定 | 是 |
| V4_G3_P011 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=False | 0.99 | 12 | 12 | 0.47 | 0.19 | 稳定 | 是 |
| V4_G3_P011 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=False | 0.99 | 12 | 12 | 0.47 | 0.19 | 稳定 | 是 |
| V4_G3_P017 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=False | 0.99 | 12 | 12 | 0.42 | 0.32 | 稳定 | 是 |
| V4_G3_P017 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=False | 0.99 | 12 | 12 | 0.42 | 0.32 | 稳定 | 是 |
| V4_G8_P032 | group8_stair_grid | G8 stair 24b/-0.05 44b/-0.03 | 0.99 | 12 | 12 | 0.46 | 0.11 | 稳定 | 是 |
| V4_G8_P032 | group8_stair_grid | G8 stair 24b/-0.05 44b/-0.03 | 0.99 | 12 | 12 | 0.46 | 0.11 | 稳定 | 是 |
| V4_G10_P002 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=False | 0.98 | 12 | 12 | 0.43 | 0.29 | 稳定 | 是 |
| V4_G10_P002 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=False | 0.98 | 12 | 12 | 0.43 | 0.29 | 稳定 | 是 |
| V4_G10_P006 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=False | 0.98 | 12 | 12 | 0.43 | 0.29 | 稳定 | 是 |
| V4_G10_P006 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=False | 0.98 | 12 | 12 | 0.43 | 0.29 | 稳定 | 是 |
| V4_G3_P003 | group3_ema_slope | G3 EMA slope p=3 th=0.001 stair=False | 0.98 | 12 | 12 | 0.44 | 0.26 | 稳定 | 是 |
| V4_G3_P003 | group3_ema_slope | G3 EMA slope p=3 th=0.001 stair=False | 0.98 | 12 | 12 | 0.44 | 0.26 | 稳定 | 是 |
| V4_G10_P010 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=False | 0.97 | 12 | 12 | 0.43 | 0.33 | 稳定 | 是 |
| V4_G10_P010 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=False | 0.97 | 12 | 12 | 0.43 | 0.33 | 稳定 | 是 |
| V4_G10_P014 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=False | 0.97 | 12 | 12 | 0.43 | 0.33 | 稳定 | 是 |
| V4_G10_P014 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=False | 0.97 | 12 | 12 | 0.43 | 0.33 | 稳定 | 是 |
| V4_G3_P004 | group3_ema_slope | G3 EMA slope p=3 th=0.002 stair=True | 0.96 | 12 | 12 | 0.53 | 0.16 | 可接受 | 是 |
| V4_G3_P004 | group3_ema_slope | G3 EMA slope p=3 th=0.002 stair=True | 0.96 | 12 | 12 | 0.53 | 0.16 | 可接受 | 是 |
| V4_G3_P006 | group3_ema_slope | G3 EMA slope p=3 th=0.003 stair=True | 0.94 | 12 | 10 | 0.63 | -0.09 | 可接受 | 是 |
| V4_G3_P006 | group3_ema_slope | G3 EMA slope p=3 th=0.003 stair=True | 0.94 | 12 | 10 | 0.63 | -0.09 | 可接受 | 是 |
| V4_G10_P019 | group10_stoch | G10 Stoch K=21 D=3 th>80 stair=True | 0.91 | 12 | 12 | 0.46 | 0.26 | 稳定 | 是 |
| V4_G10_P019 | group10_stoch | G10 Stoch K=21 D=3 th>80 stair=True | 0.91 | 12 | 12 | 0.46 | 0.26 | 稳定 | 是 |
| V4_G10_P023 | group10_stoch | G10 Stoch K=21 D=5 th>80 stair=True | 0.91 | 12 | 12 | 0.46 | 0.26 | 稳定 | 是 |
| V4_G10_P023 | group10_stoch | G10 Stoch K=21 D=5 th>80 stair=True | 0.91 | 12 | 12 | 0.46 | 0.26 | 稳定 | 是 |
| V4_G3_P005 | group3_ema_slope | G3 EMA slope p=3 th=0.002 stair=False | 0.91 | 12 | 12 | 0.49 | 0.28 | 稳定 | 是 |

## 5. Walk-Forward 过拟合检测（对阶段2已通过门控的候选）

OOS Ratio = 平均(测试期 Sharpe) / 平均(训练期 Sharpe)；PF Decay = 平均(测试期 PF) / 平均(训练期 PF)。

| strategy | group | name | 均训练Sharpe | 均测试Sharpe | OOS | PF Decay | 过拟合标签 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V4_G2_P001 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=True | 1.08 | 1.38 | 1.28 | 1.10 | 无过拟合 |
| V4_G2_P002 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=False | 1.00 | 1.13 | 1.13 | 1.04 | 无过拟合 |
| V4_G2_P003 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=True | 1.05 | 1.36 | 1.30 | 1.11 | 无过拟合 |
| V4_G2_P004 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=False | 0.98 | 1.12 | 1.14 | 1.05 | 无过拟合 |
| V4_G2_P005 | group2_macd | G2 MACD f8s21sig5 macd_pos stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G2_P006 | group2_macd | G2 MACD f8s21sig5 macd_pos stair=False | 1.01 | 1.12 | 1.11 | 1.04 | 无过拟合 |
| V4_G2_P007 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=True | 1.08 | 1.38 | 1.28 | 1.10 | 无过拟合 |
| V4_G2_P008 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=False | 1.00 | 1.13 | 1.13 | 1.04 | 无过拟合 |
| V4_G2_P001 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=True | 1.08 | 1.38 | 1.28 | 1.10 | 无过拟合 |
| V4_G2_P002 | group2_macd | G2 MACD f8s21sig5 hist_pos stair=False | 1.00 | 1.13 | 1.13 | 1.04 | 无过拟合 |
| V4_G2_P011 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=True | 1.07 | 1.33 | 1.24 | 1.08 | 无过拟合 |
| V4_G2_P003 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=True | 1.05 | 1.36 | 1.30 | 1.11 | 无过拟合 |
| V4_G2_P004 | group2_macd | G2 MACD f8s21sig5 hist_rise stair=False | 0.98 | 1.12 | 1.14 | 1.05 | 无过拟合 |
| V4_G2_P012 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=False | 1.00 | 1.08 | 1.08 | 1.02 | 无过拟合 |
| V4_G2_P013 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G2_P005 | group2_macd | G2 MACD f8s21sig5 macd_pos stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G2_P014 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=False | 1.01 | 1.12 | 1.11 | 1.04 | 无过拟合 |
| V4_G2_P007 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=True | 1.08 | 1.38 | 1.28 | 1.10 | 无过拟合 |
| V4_G2_P008 | group2_macd | G2 MACD f8s21sig5 macd_sig_hist stair=False | 1.00 | 1.13 | 1.13 | 1.04 | 无过拟合 |
| V4_G2_P009 | group2_macd | G2 MACD f12s26sig9 hist_pos stair=True | 1.07 | 1.33 | 1.24 | 1.08 | 无过拟合 |
| V4_G2_P010 | group2_macd | G2 MACD f12s26sig9 hist_pos stair=False | 1.00 | 1.08 | 1.08 | 1.02 | 无过拟合 |
| V4_G2_P011 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=True | 1.07 | 1.33 | 1.24 | 1.08 | 无过拟合 |
| V4_G2_P012 | group2_macd | G2 MACD f12s26sig9 hist_rise stair=False | 1.00 | 1.08 | 1.08 | 1.02 | 无过拟合 |
| V4_G2_P021 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G2_P013 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G2_P014 | group2_macd | G2 MACD f12s26sig9 macd_pos stair=False | 1.01 | 1.12 | 1.11 | 1.04 | 无过拟合 |
| V4_G2_P022 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=False | 1.01 | 1.12 | 1.11 | 1.04 | 无过拟合 |
| V4_G2_P015 | group2_macd | G2 MACD f12s26sig9 macd_sig_hist stair=True | 1.07 | 1.33 | 1.24 | 1.08 | 无过拟合 |
| V4_G2_P024 | group2_macd | G2 MACD f8s17sig9 macd_sig_hist stair=False | 1.00 | 1.16 | 1.16 | 1.05 | 无过拟合 |
| V4_G2_P017 | group2_macd | G2 MACD f8s17sig9 hist_pos stair=True | 1.07 | 1.41 | 1.31 | 1.11 | 无过拟合 |
| V4_G2_P018 | group2_macd | G2 MACD f8s17sig9 hist_pos stair=False | 1.00 | 1.16 | 1.16 | 1.05 | 无过拟合 |
| V4_G2_P019 | group2_macd | G2 MACD f8s17sig9 hist_rise stair=True | 1.04 | 1.38 | 1.32 | 1.12 | 无过拟合 |
| V4_G3_P003 | group3_ema_slope | G3 EMA slope p=3 th=0.001 stair=False | 1.01 | 1.08 | 1.07 | 1.02 | 无过拟合 |
| V4_G3_P004 | group3_ema_slope | G3 EMA slope p=3 th=0.002 stair=True | 1.00 | 1.04 | 1.03 | 1.03 | 无过拟合 |
| V4_G2_P020 | group2_macd | G2 MACD f8s17sig9 hist_rise stair=False | 0.97 | 1.13 | 1.16 | 1.05 | 无过拟合 |
| V4_G2_P021 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G3_P006 | group3_ema_slope | G3 EMA slope p=3 th=0.003 stair=True | 0.85 | 0.97 | 1.14 | 1.11 | 无过拟合 |
| V4_G2_P022 | group2_macd | G2 MACD f8s17sig9 macd_pos stair=False | 1.01 | 1.12 | 1.11 | 1.04 | 无过拟合 |
| V4_G3_P007 | group3_ema_slope | G3 EMA slope p=5 th=0.0005 stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G2_P023 | group2_macd | G2 MACD f8s17sig9 macd_sig_hist stair=True | 1.07 | 1.41 | 1.31 | 1.11 | 无过拟合 |
| V4_G2_P024 | group2_macd | G2 MACD f8s17sig9 macd_sig_hist stair=False | 1.00 | 1.16 | 1.16 | 1.05 | 无过拟合 |
| V4_G3_P001 | group3_ema_slope | G3 EMA slope p=3 th=0.0005 stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G3_P009 | group3_ema_slope | G3 EMA slope p=5 th=0.001 stair=False | 1.02 | 1.12 | 1.09 | 1.03 | 无过拟合 |
| V4_G3_P010 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=True | 1.03 | 1.22 | 1.19 | 1.08 | 无过拟合 |
| V4_G3_P002 | group3_ema_slope | G3 EMA slope p=3 th=0.001 stair=True | 1.08 | 1.32 | 1.23 | 1.08 | 无过拟合 |
| V4_G3_P011 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=False | 0.97 | 1.05 | 1.08 | 1.04 | 无过拟合 |
| V4_G3_P003 | group3_ema_slope | G3 EMA slope p=3 th=0.001 stair=False | 1.01 | 1.08 | 1.07 | 1.02 | 无过拟合 |
| V4_G3_P004 | group3_ema_slope | G3 EMA slope p=3 th=0.002 stair=True | 1.00 | 1.04 | 1.03 | 1.03 | 无过拟合 |
| V4_G3_P005 | group3_ema_slope | G3 EMA slope p=3 th=0.002 stair=False | 0.97 | 0.93 | 0.96 | 1.00 | 无过拟合 |
| V4_G3_P013 | group3_ema_slope | G3 EMA slope p=8 th=0.0005 stair=True | 1.09 | 1.37 | 1.25 | 1.09 | 无过拟合 |
| V4_G3_P006 | group3_ema_slope | G3 EMA slope p=3 th=0.003 stair=True | 0.85 | 0.97 | 1.14 | 1.11 | 无过拟合 |
| V4_G3_P014 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=True | 1.10 | 1.37 | 1.25 | 1.09 | 无过拟合 |
| V4_G3_P015 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=False | 1.02 | 1.14 | 1.11 | 1.04 | 无过拟合 |
| V4_G3_P007 | group3_ema_slope | G3 EMA slope p=5 th=0.0005 stair=True | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G3_P008 | group3_ema_slope | G3 EMA slope p=5 th=0.001 stair=True | 1.09 | 1.36 | 1.25 | 1.09 | 无过拟合 |
| V4_G3_P016 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=True | 1.08 | 1.30 | 1.20 | 1.07 | 无过拟合 |
| V4_G3_P017 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=False | 1.01 | 1.08 | 1.06 | 1.02 | 无过拟合 |
| V4_G3_P009 | group3_ema_slope | G3 EMA slope p=5 th=0.001 stair=False | 1.02 | 1.12 | 1.09 | 1.03 | 无过拟合 |
| V4_G3_P018 | group3_ema_slope | G3 EMA slope p=8 th=0.003 stair=True | 1.02 | 1.19 | 1.16 | 1.07 | 无过拟合 |
| V4_G3_P010 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=True | 1.03 | 1.22 | 1.19 | 1.08 | 无过拟合 |
| V4_G3_P011 | group3_ema_slope | G3 EMA slope p=5 th=0.002 stair=False | 0.97 | 1.05 | 1.08 | 1.04 | 无过拟合 |
| V4_G3_P013 | group3_ema_slope | G3 EMA slope p=8 th=0.0005 stair=True | 1.09 | 1.37 | 1.25 | 1.09 | 无过拟合 |
| V4_G3_P014 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=True | 1.10 | 1.37 | 1.25 | 1.09 | 无过拟合 |
| V4_G3_P015 | group3_ema_slope | G3 EMA slope p=8 th=0.001 stair=False | 1.02 | 1.14 | 1.11 | 1.04 | 无过拟合 |
| V4_G3_P016 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=True | 1.08 | 1.30 | 1.20 | 1.07 | 无过拟合 |
| V4_G3_P017 | group3_ema_slope | G3 EMA slope p=8 th=0.002 stair=False | 1.01 | 1.08 | 1.06 | 1.02 | 无过拟合 |
| V4_G3_P018 | group3_ema_slope | G3 EMA slope p=8 th=0.003 stair=True | 1.02 | 1.19 | 1.16 | 1.07 | 无过拟合 |
| V4_G6_P001 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.08 | 1.35 | 1.25 | 1.08 | 无过拟合 |
| V4_G6_P002 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.5 | 1.09 | 1.40 | 1.29 | 1.10 | 无过拟合 |
| V4_G6_P003 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.13 | 1.37 | 1.22 | 1.08 | 无过拟合 |
| V4_G6_P001 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.08 | 1.35 | 1.25 | 1.08 | 无过拟合 |
| V4_G6_P004 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.3 | 1.07 | 1.37 | 1.28 | 1.10 | 无过拟合 |
| V4_G6_P002 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.5 | 1.09 | 1.40 | 1.29 | 1.10 | 无过拟合 |
| V4_G6_P005 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=35 th=0.5 | 1.16 | 1.42 | 1.22 | 1.08 | 无过拟合 |
| V4_G6_P003 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.13 | 1.37 | 1.22 | 1.08 | 无过拟合 |
| V4_G6_P006 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.09 | 1.38 | 1.27 | 1.09 | 无过拟合 |
| V4_G6_P004 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.3 | 1.07 | 1.37 | 1.28 | 1.10 | 无过拟合 |
| V4_G6_P007 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=25 th=0.7 | 1.11 | 1.37 | 1.23 | 1.08 | 无过拟合 |
| V4_G6_P005 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=35 th=0.5 | 1.16 | 1.42 | 1.22 | 1.08 | 无过拟合 |
| V4_G6_P008 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=40 th=0.3 | 1.13 | 1.41 | 1.25 | 1.09 | 无过拟合 |
| V4_G6_P009 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.08 | 1.35 | 1.25 | 1.08 | 无过拟合 |
| V4_G6_P006 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.09 | 1.38 | 1.27 | 1.09 | 无过拟合 |
| V4_G6_P007 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=25 th=0.7 | 1.11 | 1.37 | 1.23 | 1.08 | 无过拟合 |
| V4_G6_P010 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.7 | 1.13 | 1.44 | 1.28 | 1.10 | 无过拟合 |
| V4_G6_P011 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.3 | 1.11 | 1.41 | 1.27 | 1.10 | 无过拟合 |
| V4_G6_P008 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=40 th=0.3 | 1.13 | 1.41 | 1.25 | 1.09 | 无过拟合 |
| V4_G6_P012 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=30 th=0.5 | 1.11 | 1.39 | 1.26 | 1.09 | 无过拟合 |
| V4_G6_P009 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=25 th=0.3 | 1.08 | 1.35 | 1.25 | 1.08 | 无过拟合 |
| V4_G6_P013 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=30 th=0.5 | 1.08 | 1.40 | 1.30 | 1.10 | 无过拟合 |
| V4_G6_P010 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.7 | 1.13 | 1.44 | 1.28 | 1.10 | 无过拟合 |
| V4_G6_P014 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.3 | 1.12 | 1.41 | 1.26 | 1.10 | 无过拟合 |
| V4_G6_P011 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=40 th=0.3 | 1.11 | 1.41 | 1.27 | 1.10 | 无过拟合 |
| V4_G6_P015 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.5 | 1.09 | 1.38 | 1.26 | 1.09 | 无过拟合 |
| V4_G6_P012 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=30 th=0.5 | 1.11 | 1.39 | 1.26 | 1.09 | 无过拟合 |
| V4_G6_P013 | group6_dynamic_dc | G6 dynDC lb=50 s=14 L=30 th=0.5 | 1.08 | 1.40 | 1.30 | 1.10 | 无过拟合 |
| V4_G6_P016 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.09 | 1.38 | 1.27 | 1.09 | 无过拟合 |
| V4_G6_P014 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=40 th=0.3 | 1.12 | 1.41 | 1.26 | 1.10 | 无过拟合 |
| V4_G6_P017 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.13 | 1.37 | 1.22 | 1.08 | 无过拟合 |
| V4_G6_P015 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.5 | 1.09 | 1.38 | 1.26 | 1.09 | 无过拟合 |
| V4_G6_P019 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.3 | 1.11 | 1.39 | 1.26 | 1.09 | 无过拟合 |
| V4_G6_P016 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=30 th=0.5 | 1.09 | 1.38 | 1.27 | 1.09 | 无过拟合 |
| V4_G6_P017 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=40 th=0.7 | 1.13 | 1.37 | 1.22 | 1.08 | 无过拟合 |
| V4_G6_P020 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=25 th=0.7 | 1.10 | 1.40 | 1.28 | 1.09 | 无过拟合 |
| V4_G6_P018 | group6_dynamic_dc | G6 dynDC lb=100 s=16 L=30 th=0.7 | 1.09 | 1.40 | 1.28 | 1.10 | 无过拟合 |
| V4_G6_P019 | group6_dynamic_dc | G6 dynDC lb=50 s=16 L=35 th=0.3 | 1.11 | 1.39 | 1.26 | 1.09 | 无过拟合 |
| V4_G6_P020 | group6_dynamic_dc | G6 dynDC lb=100 s=14 L=25 th=0.7 | 1.10 | 1.40 | 1.28 | 1.09 | 无过拟合 |
| V4_G8_P001 | group8_stair_grid | G8 stair 16b/-0.05 36b/-0.03 | 0.99 | 1.20 | 1.21 | 1.07 | 无过拟合 |
| V4_G8_P002 | group8_stair_grid | G8 stair 16b/-0.05 40b/-0.04 | 1.00 | 1.18 | 1.18 | 1.06 | 无过拟合 |
| V4_G8_P003 | group8_stair_grid | G8 stair 16b/-0.05 44b/-0.05 | 0.99 | 1.15 | 1.17 | 1.06 | 无过拟合 |
| V4_G8_P004 | group8_stair_grid | G8 stair 16b/-0.06 36b/-0.03 | 1.00 | 1.28 | 1.28 | 1.10 | 无过拟合 |
| V4_G8_P005 | group8_stair_grid | G8 stair 16b/-0.06 40b/-0.04 | 1.07 | 1.37 | 1.27 | 1.10 | 无过拟合 |
| V4_G8_P006 | group8_stair_grid | G8 stair 16b/-0.06 48b/-0.05 | 1.05 | 1.30 | 1.24 | 1.08 | 无过拟合 |
| V4_G8_P007 | group8_stair_grid | G8 stair 16b/-0.07 40b/-0.03 | 1.04 | 1.26 | 1.22 | 1.08 | 无过拟合 |
| V4_G8_P008 | group8_stair_grid | G8 stair 16b/-0.07 44b/-0.04 | 1.11 | 1.32 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P009 | group8_stair_grid | G8 stair 18b/-0.05 36b/-0.03 | 0.99 | 1.21 | 1.22 | 1.07 | 无过拟合 |
| V4_G8_P001 | group8_stair_grid | G8 stair 16b/-0.05 36b/-0.03 | 0.99 | 1.20 | 1.21 | 1.07 | 无过拟合 |
| V4_G8_P010 | group8_stair_grid | G8 stair 18b/-0.05 40b/-0.05 | 0.98 | 1.15 | 1.18 | 1.06 | 无过拟合 |
| V4_G8_P002 | group8_stair_grid | G8 stair 16b/-0.05 40b/-0.04 | 1.00 | 1.18 | 1.18 | 1.06 | 无过拟合 |
| V4_G8_P011 | group8_stair_grid | G8 stair 18b/-0.06 36b/-0.04 | 1.05 | 1.32 | 1.25 | 1.09 | 无过拟合 |
| V4_G8_P003 | group8_stair_grid | G8 stair 16b/-0.05 44b/-0.05 | 0.99 | 1.15 | 1.17 | 1.06 | 无过拟合 |
| V4_G8_P012 | group8_stair_grid | G8 stair 18b/-0.06 44b/-0.03 | 1.02 | 1.31 | 1.29 | 1.10 | 无过拟合 |
| V4_G8_P004 | group8_stair_grid | G8 stair 16b/-0.06 36b/-0.03 | 1.00 | 1.28 | 1.28 | 1.10 | 无过拟合 |
| V4_G8_P013 | group8_stair_grid | G8 stair 18b/-0.07 40b/-0.04 | 1.10 | 1.30 | 1.18 | 1.07 | 无过拟合 |
| V4_G8_P005 | group8_stair_grid | G8 stair 16b/-0.06 40b/-0.04 | 1.07 | 1.37 | 1.27 | 1.10 | 无过拟合 |
| V4_G8_P014 | group8_stair_grid | G8 stair 18b/-0.07 48b/-0.05 | 1.08 | 1.28 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P006 | group8_stair_grid | G8 stair 16b/-0.06 48b/-0.05 | 1.05 | 1.30 | 1.24 | 1.08 | 无过拟合 |
| V4_G8_P015 | group8_stair_grid | G8 stair 20b/-0.05 36b/-0.03 | 1.00 | 1.24 | 1.24 | 1.08 | 无过拟合 |
| V4_G8_P007 | group8_stair_grid | G8 stair 16b/-0.07 40b/-0.03 | 1.04 | 1.26 | 1.22 | 1.08 | 无过拟合 |
| V4_G8_P016 | group8_stair_grid | G8 stair 20b/-0.05 40b/-0.04 | 1.01 | 1.21 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P008 | group8_stair_grid | G8 stair 16b/-0.07 44b/-0.04 | 1.11 | 1.32 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P017 | group8_stair_grid | G8 stair 20b/-0.05 48b/-0.05 | 0.99 | 1.18 | 1.19 | 1.06 | 无过拟合 |
| V4_G8_P009 | group8_stair_grid | G8 stair 18b/-0.05 36b/-0.03 | 0.99 | 1.21 | 1.22 | 1.07 | 无过拟合 |
| V4_G8_P018 | group8_stair_grid | G8 stair 20b/-0.06 36b/-0.03 | 1.01 | 1.30 | 1.28 | 1.10 | 无过拟合 |
| V4_G8_P010 | group8_stair_grid | G8 stair 18b/-0.05 40b/-0.05 | 0.98 | 1.15 | 1.18 | 1.06 | 无过拟合 |
| V4_G8_P019 | group8_stair_grid | G8 stair 20b/-0.06 40b/-0.04 | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G8_P011 | group8_stair_grid | G8 stair 18b/-0.06 36b/-0.04 | 1.05 | 1.32 | 1.25 | 1.09 | 无过拟合 |
| V4_G8_P020 | group8_stair_grid | G8 stair 20b/-0.06 44b/-0.05 | 1.07 | 1.31 | 1.23 | 1.08 | 无过拟合 |
| V4_G8_P012 | group8_stair_grid | G8 stair 18b/-0.06 44b/-0.03 | 1.02 | 1.31 | 1.29 | 1.10 | 无过拟合 |
| V4_G8_P021 | group8_stair_grid | G8 stair 20b/-0.07 36b/-0.04 | 1.09 | 1.28 | 1.17 | 1.07 | 无过拟合 |
| V4_G8_P013 | group8_stair_grid | G8 stair 18b/-0.07 40b/-0.04 | 1.10 | 1.30 | 1.18 | 1.07 | 无过拟合 |
| V4_G8_P022 | group8_stair_grid | G8 stair 20b/-0.07 40b/-0.05 | 1.06 | 1.25 | 1.18 | 1.06 | 无过拟合 |
| V4_G8_P023 | group8_stair_grid | G8 stair 20b/-0.07 48b/-0.03 | 1.08 | 1.30 | 1.20 | 1.08 | 无过拟合 |
| V4_G8_P014 | group8_stair_grid | G8 stair 18b/-0.07 48b/-0.05 | 1.08 | 1.28 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P024 | group8_stair_grid | G8 stair 22b/-0.05 40b/-0.03 | 1.00 | 1.20 | 1.20 | 1.07 | 无过拟合 |
| V4_G8_P015 | group8_stair_grid | G8 stair 20b/-0.05 36b/-0.03 | 1.00 | 1.24 | 1.24 | 1.08 | 无过拟合 |
| V4_G8_P016 | group8_stair_grid | G8 stair 20b/-0.05 40b/-0.04 | 1.01 | 1.21 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P025 | group8_stair_grid | G8 stair 22b/-0.05 44b/-0.04 | 1.02 | 1.18 | 1.16 | 1.05 | 无过拟合 |
| V4_G8_P017 | group8_stair_grid | G8 stair 20b/-0.05 48b/-0.05 | 0.99 | 1.18 | 1.19 | 1.06 | 无过拟合 |
| V4_G8_P026 | group8_stair_grid | G8 stair 22b/-0.06 36b/-0.05 | 1.03 | 1.25 | 1.21 | 1.07 | 无过拟合 |
| V4_G8_P018 | group8_stair_grid | G8 stair 20b/-0.06 36b/-0.03 | 1.01 | 1.30 | 1.28 | 1.10 | 无过拟合 |
| V4_G8_P027 | group8_stair_grid | G8 stair 22b/-0.06 40b/-0.03 | 1.03 | 1.31 | 1.27 | 1.10 | 无过拟合 |
| V4_G8_P028 | group8_stair_grid | G8 stair 22b/-0.06 48b/-0.04 | 1.09 | 1.31 | 1.20 | 1.08 | 无过拟合 |
| V4_G8_P019 | group8_stair_grid | G8 stair 20b/-0.06 40b/-0.04 | 1.09 | 1.37 | 1.26 | 1.10 | 无过拟合 |
| V4_G8_P029 | group8_stair_grid | G8 stair 22b/-0.07 36b/-0.03 | 1.00 | 1.22 | 1.22 | 1.07 | 无过拟合 |
| V4_G8_P020 | group8_stair_grid | G8 stair 20b/-0.06 44b/-0.05 | 1.07 | 1.31 | 1.23 | 1.08 | 无过拟合 |
| V4_G8_P030 | group8_stair_grid | G8 stair 22b/-0.07 40b/-0.05 | 1.03 | 1.24 | 1.20 | 1.07 | 无过拟合 |
| V4_G8_P021 | group8_stair_grid | G8 stair 20b/-0.07 36b/-0.04 | 1.09 | 1.28 | 1.17 | 1.07 | 无过拟合 |
| V4_G8_P031 | group8_stair_grid | G8 stair 24b/-0.05 36b/-0.04 | 0.99 | 1.15 | 1.16 | 1.05 | 无过拟合 |
| V4_G8_P022 | group8_stair_grid | G8 stair 20b/-0.07 40b/-0.05 | 1.06 | 1.25 | 1.18 | 1.06 | 无过拟合 |
| V4_G8_P032 | group8_stair_grid | G8 stair 24b/-0.05 44b/-0.03 | 0.96 | 1.11 | 1.16 | 1.06 | 无过拟合 |
| V4_G8_P023 | group8_stair_grid | G8 stair 20b/-0.07 48b/-0.03 | 1.08 | 1.30 | 1.20 | 1.08 | 无过拟合 |
| V4_G8_P024 | group8_stair_grid | G8 stair 22b/-0.05 40b/-0.03 | 1.00 | 1.20 | 1.20 | 1.07 | 无过拟合 |
| V4_G8_P025 | group8_stair_grid | G8 stair 22b/-0.05 44b/-0.04 | 1.02 | 1.18 | 1.16 | 1.05 | 无过拟合 |
| V4_G8_P034 | group8_stair_grid | G8 stair 24b/-0.06 48b/-0.03 | 1.04 | 1.24 | 1.20 | 1.07 | 无过拟合 |
| V4_G8_P035 | group8_stair_grid | G8 stair 24b/-0.07 36b/-0.04 | 1.05 | 1.24 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P026 | group8_stair_grid | G8 stair 22b/-0.06 36b/-0.05 | 1.03 | 1.25 | 1.21 | 1.07 | 无过拟合 |
| V4_G8_P027 | group8_stair_grid | G8 stair 22b/-0.06 40b/-0.03 | 1.03 | 1.31 | 1.27 | 1.10 | 无过拟合 |
| V4_G8_P036 | group8_stair_grid | G8 stair 24b/-0.07 40b/-0.03 | 1.00 | 1.23 | 1.23 | 1.08 | 无过拟合 |
| V4_G8_P028 | group8_stair_grid | G8 stair 22b/-0.06 48b/-0.04 | 1.09 | 1.31 | 1.20 | 1.08 | 无过拟合 |
| V4_G8_P029 | group8_stair_grid | G8 stair 22b/-0.07 36b/-0.03 | 1.00 | 1.22 | 1.22 | 1.07 | 无过拟合 |
| V4_G8_P030 | group8_stair_grid | G8 stair 22b/-0.07 40b/-0.05 | 1.03 | 1.24 | 1.20 | 1.07 | 无过拟合 |
| V4_G8_P031 | group8_stair_grid | G8 stair 24b/-0.05 36b/-0.04 | 0.99 | 1.15 | 1.16 | 1.05 | 无过拟合 |
| V4_G8_P032 | group8_stair_grid | G8 stair 24b/-0.05 44b/-0.03 | 0.96 | 1.11 | 1.16 | 1.06 | 无过拟合 |
| V4_G8_P033 | group8_stair_grid | G8 stair 24b/-0.06 40b/-0.05 | 1.04 | 1.25 | 1.21 | 1.07 | 无过拟合 |
| V4_G8_P034 | group8_stair_grid | G8 stair 24b/-0.06 48b/-0.03 | 1.04 | 1.24 | 1.20 | 1.07 | 无过拟合 |
| V4_G8_P035 | group8_stair_grid | G8 stair 24b/-0.07 36b/-0.04 | 1.05 | 1.24 | 1.19 | 1.07 | 无过拟合 |
| V4_G8_P036 | group8_stair_grid | G8 stair 24b/-0.07 40b/-0.03 | 1.00 | 1.23 | 1.23 | 1.08 | 无过拟合 |
| V4_G10_P001 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=True | 0.99 | 1.26 | 1.28 | 1.11 | 无过拟合 |
| V4_G10_P002 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=False | 0.93 | 1.02 | 1.10 | 1.05 | 无过拟合 |
| V4_G10_P005 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=True | 0.99 | 1.26 | 1.28 | 1.11 | 无过拟合 |
| V4_G10_P006 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=False | 0.93 | 1.02 | 1.10 | 1.05 | 无过拟合 |
| V4_G10_P009 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=True | 0.99 | 1.24 | 1.25 | 1.10 | 无过拟合 |
| V4_G10_P010 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=False | 0.93 | 0.99 | 1.06 | 1.03 | 无过拟合 |
| V4_G10_P001 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=True | 0.99 | 1.26 | 1.28 | 1.11 | 无过拟合 |
| V4_G10_P002 | group10_stoch | G10 Stoch K=9 D=3 th>60 stair=False | 0.93 | 1.02 | 1.10 | 1.05 | 无过拟合 |
| V4_G10_P013 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=True | 0.99 | 1.24 | 1.25 | 1.10 | 无过拟合 |
| V4_G10_P014 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=False | 0.93 | 0.99 | 1.06 | 1.03 | 无过拟合 |
| V4_G10_P005 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=True | 0.99 | 1.26 | 1.28 | 1.11 | 无过拟合 |
| V4_G10_P006 | group10_stoch | G10 Stoch K=9 D=5 th>60 stair=False | 0.93 | 1.02 | 1.10 | 1.05 | 无过拟合 |
| V4_G10_P017 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=True | 1.06 | 1.32 | 1.25 | 1.09 | 无过拟合 |
| V4_G10_P018 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=False | 0.99 | 1.06 | 1.08 | 1.04 | 无过拟合 |
| V4_G10_P009 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=True | 0.99 | 1.24 | 1.25 | 1.10 | 无过拟合 |
| V4_G10_P019 | group10_stoch | G10 Stoch K=21 D=3 th>80 stair=True | 0.83 | 0.91 | 1.10 | 1.05 | 无过拟合 |
| V4_G10_P010 | group10_stoch | G10 Stoch K=14 D=3 th>60 stair=False | 0.93 | 0.99 | 1.06 | 1.03 | 无过拟合 |
| V4_G10_P021 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=True | 1.06 | 1.32 | 1.25 | 1.09 | 无过拟合 |
| V4_G10_P022 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=False | 0.99 | 1.06 | 1.08 | 1.04 | 无过拟合 |
| V4_G10_P023 | group10_stoch | G10 Stoch K=21 D=5 th>80 stair=True | 0.83 | 0.91 | 1.10 | 1.05 | 无过拟合 |
| V4_G10_P013 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=True | 0.99 | 1.24 | 1.25 | 1.10 | 无过拟合 |
| V4_G10_P014 | group10_stoch | G10 Stoch K=14 D=5 th>60 stair=False | 0.93 | 0.99 | 1.06 | 1.03 | 无过拟合 |
| V4_G10_P017 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=True | 1.06 | 1.32 | 1.25 | 1.09 | 无过拟合 |
| V4_G10_P018 | group10_stoch | G10 Stoch K=21 D=3 th>60 stair=False | 0.99 | 1.06 | 1.08 | 1.04 | 无过拟合 |
| V4_G10_P019 | group10_stoch | G10 Stoch K=21 D=3 th>80 stair=True | 0.83 | 0.91 | 1.10 | 1.05 | 无过拟合 |
| V4_G10_P021 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=True | 1.06 | 1.32 | 1.25 | 1.09 | 无过拟合 |
| V4_G10_P022 | group10_stoch | G10 Stoch K=21 D=5 th>60 stair=False | 0.99 | 1.06 | 1.08 | 1.04 | 无过拟合 |
| V4_G10_P023 | group10_stoch | G10 Stoch K=21 D=5 th>80 stair=True | 0.83 | 0.91 | 1.10 | 1.05 | 无过拟合 |

## 6. 最终推荐（综合三阶段）

判定摘要：
- **阶段1**：Sharpe≥0.9、PF≥1.3、交易≥800、回撤≤25.0%。
- **阶段2**：分年度标签为「稳定」或「可接受」（见第4节）。
- **阶段3**：存在 WF 行且 OOS≥0.5 且平均测试 Sharpe>0；**强烈推荐** 另要求 OOS>0.8 且组内邻域 Sharpe 标准差 < 0.1（平滑）。

### 强烈推荐

- **强烈推荐** `V4_G3_P014` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.001 stair=True`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G3_P014` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.001 stair=True`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P003` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=40 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P005` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=35 th=0.5`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P003` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=40 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P005` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=35 th=0.5`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P008` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=40 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P010` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=40 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P011` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=40 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P008` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=40 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P010` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=40 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P014` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=40 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P011` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=40 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P014` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=40 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P017` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=40 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P019` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=35 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P017` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=40 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P020` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=25 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P019` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=35 th=0.3`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G6_P020` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=25 th=0.7`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G8_P005` / `group8_stair_grid` / `G8 stair 16b/-0.06 40b/-0.04`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V4_G8_P005` / `group8_stair_grid` / `G8 stair 16b/-0.06 40b/-0.04`：三阶段通过，Sharpe>1.15，OOS>0.8，邻域平滑(std=0.00)

### 推荐

- **推荐** `V4_G2_P001` / `group2_macd` / `G2 MACD f8s21sig5 hist_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G2_P002` / `group2_macd` / `G2 MACD f8s21sig5 hist_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.13）
- **推荐** `V4_G2_P003` / `group2_macd` / `G2 MACD f8s21sig5 hist_rise stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.30）
- **推荐** `V4_G2_P004` / `group2_macd` / `G2 MACD f8s21sig5 hist_rise stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.14）
- **推荐** `V4_G2_P005` / `group2_macd` / `G2 MACD f8s21sig5 macd_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G2_P006` / `group2_macd` / `G2 MACD f8s21sig5 macd_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.11）
- **推荐** `V4_G2_P007` / `group2_macd` / `G2 MACD f8s21sig5 macd_sig_hist stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G2_P008` / `group2_macd` / `G2 MACD f8s21sig5 macd_sig_hist stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.13）
- **推荐** `V4_G2_P001` / `group2_macd` / `G2 MACD f8s21sig5 hist_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G2_P002` / `group2_macd` / `G2 MACD f8s21sig5 hist_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.13）
- **推荐** `V4_G2_P011` / `group2_macd` / `G2 MACD f12s26sig9 hist_rise stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G2_P003` / `group2_macd` / `G2 MACD f8s21sig5 hist_rise stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.30）
- **推荐** `V4_G2_P004` / `group2_macd` / `G2 MACD f8s21sig5 hist_rise stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.14）
- **推荐** `V4_G2_P013` / `group2_macd` / `G2 MACD f12s26sig9 macd_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G2_P005` / `group2_macd` / `G2 MACD f8s21sig5 macd_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G2_P014` / `group2_macd` / `G2 MACD f12s26sig9 macd_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.11）
- **推荐** `V4_G2_P007` / `group2_macd` / `G2 MACD f8s21sig5 macd_sig_hist stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G2_P008` / `group2_macd` / `G2 MACD f8s21sig5 macd_sig_hist stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.13）
- **推荐** `V4_G2_P009` / `group2_macd` / `G2 MACD f12s26sig9 hist_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G2_P011` / `group2_macd` / `G2 MACD f12s26sig9 hist_rise stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G2_P021` / `group2_macd` / `G2 MACD f8s17sig9 macd_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G2_P013` / `group2_macd` / `G2 MACD f12s26sig9 macd_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G2_P014` / `group2_macd` / `G2 MACD f12s26sig9 macd_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.11）
- **推荐** `V4_G2_P022` / `group2_macd` / `G2 MACD f8s17sig9 macd_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.11）
- **推荐** `V4_G2_P015` / `group2_macd` / `G2 MACD f12s26sig9 macd_sig_hist stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G2_P024` / `group2_macd` / `G2 MACD f8s17sig9 macd_sig_hist stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G2_P017` / `group2_macd` / `G2 MACD f8s17sig9 hist_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.31）
- **推荐** `V4_G2_P018` / `group2_macd` / `G2 MACD f8s17sig9 hist_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G2_P019` / `group2_macd` / `G2 MACD f8s17sig9 hist_rise stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.32）
- **推荐** `V4_G2_P020` / `group2_macd` / `G2 MACD f8s17sig9 hist_rise stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G2_P021` / `group2_macd` / `G2 MACD f8s17sig9 macd_pos stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G2_P022` / `group2_macd` / `G2 MACD f8s17sig9 macd_pos stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.11）
- **推荐** `V4_G3_P007` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.0005 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G2_P023` / `group2_macd` / `G2 MACD f8s17sig9 macd_sig_hist stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.31）
- **推荐** `V4_G2_P024` / `group2_macd` / `G2 MACD f8s17sig9 macd_sig_hist stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G3_P001` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.0005 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G3_P010` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.002 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G3_P002` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.001 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.23）
- **推荐** `V4_G3_P013` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.0005 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G3_P015` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.001 stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.11）
- **推荐** `V4_G3_P007` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.0005 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G3_P008` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.001 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G3_P016` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.002 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G3_P018` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.003 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G3_P010` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.002 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G3_P013` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.0005 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G3_P015` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.001 stair=False`：三阶段通过且 Sharpe>1.0（OOS=1.11）
- **推荐** `V4_G3_P016` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.002 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G3_P018` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.003 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G6_P001` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=25 th=0.3`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G6_P002` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=40 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.29）
- **推荐** `V4_G6_P001` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=25 th=0.3`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G6_P004` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=30 th=0.3`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G6_P002` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=40 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.29）
- **推荐** `V4_G6_P006` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V4_G6_P004` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=30 th=0.3`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G6_P007` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=25 th=0.7`：三阶段通过且 Sharpe>1.0（OOS=1.23）
- **推荐** `V4_G6_P009` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=25 th=0.3`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G6_P006` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V4_G6_P007` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=25 th=0.7`：三阶段通过且 Sharpe>1.0（OOS=1.23）
- **推荐** `V4_G6_P012` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G6_P009` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=25 th=0.3`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G6_P013` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.30）
- **推荐** `V4_G6_P015` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=35 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G6_P012` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G6_P013` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=14 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.30）
- **推荐** `V4_G6_P016` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V4_G6_P015` / `group6_dynamic_dc` / `G6 dynDC lb=50 s=16 L=35 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G6_P016` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=14 L=30 th=0.5`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V4_G6_P018` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=30 th=0.7`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G8_P001` / `group8_stair_grid` / `G8 stair 16b/-0.05 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.21）
- **推荐** `V4_G8_P002` / `group8_stair_grid` / `G8 stair 16b/-0.05 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P003` / `group8_stair_grid` / `G8 stair 16b/-0.05 44b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.17）
- **推荐** `V4_G8_P004` / `group8_stair_grid` / `G8 stair 16b/-0.06 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G8_P006` / `group8_stair_grid` / `G8 stair 16b/-0.06 48b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G8_P007` / `group8_stair_grid` / `G8 stair 16b/-0.07 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.22）
- **推荐** `V4_G8_P008` / `group8_stair_grid` / `G8 stair 16b/-0.07 44b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P009` / `group8_stair_grid` / `G8 stair 18b/-0.05 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.22）
- **推荐** `V4_G8_P001` / `group8_stair_grid` / `G8 stair 16b/-0.05 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.21）
- **推荐** `V4_G8_P010` / `group8_stair_grid` / `G8 stair 18b/-0.05 40b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P002` / `group8_stair_grid` / `G8 stair 16b/-0.05 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P011` / `group8_stair_grid` / `G8 stair 18b/-0.06 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G8_P003` / `group8_stair_grid` / `G8 stair 16b/-0.05 44b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.17）
- **推荐** `V4_G8_P012` / `group8_stair_grid` / `G8 stair 18b/-0.06 44b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.29）
- **推荐** `V4_G8_P004` / `group8_stair_grid` / `G8 stair 16b/-0.06 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G8_P013` / `group8_stair_grid` / `G8 stair 18b/-0.07 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P014` / `group8_stair_grid` / `G8 stair 18b/-0.07 48b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P006` / `group8_stair_grid` / `G8 stair 16b/-0.06 48b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G8_P015` / `group8_stair_grid` / `G8 stair 20b/-0.05 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G8_P007` / `group8_stair_grid` / `G8 stair 16b/-0.07 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.22）
- **推荐** `V4_G8_P016` / `group8_stair_grid` / `G8 stair 20b/-0.05 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P008` / `group8_stair_grid` / `G8 stair 16b/-0.07 44b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P017` / `group8_stair_grid` / `G8 stair 20b/-0.05 48b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P009` / `group8_stair_grid` / `G8 stair 18b/-0.05 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.22）
- **推荐** `V4_G8_P018` / `group8_stair_grid` / `G8 stair 20b/-0.06 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G8_P010` / `group8_stair_grid` / `G8 stair 18b/-0.05 40b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P019` / `group8_stair_grid` / `G8 stair 20b/-0.06 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G8_P011` / `group8_stair_grid` / `G8 stair 18b/-0.06 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G8_P020` / `group8_stair_grid` / `G8 stair 20b/-0.06 44b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.23）
- **推荐** `V4_G8_P012` / `group8_stair_grid` / `G8 stair 18b/-0.06 44b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.29）
- **推荐** `V4_G8_P021` / `group8_stair_grid` / `G8 stair 20b/-0.07 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.17）
- **推荐** `V4_G8_P013` / `group8_stair_grid` / `G8 stair 18b/-0.07 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P022` / `group8_stair_grid` / `G8 stair 20b/-0.07 40b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P023` / `group8_stair_grid` / `G8 stair 20b/-0.07 48b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P014` / `group8_stair_grid` / `G8 stair 18b/-0.07 48b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P024` / `group8_stair_grid` / `G8 stair 22b/-0.05 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P015` / `group8_stair_grid` / `G8 stair 20b/-0.05 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.24）
- **推荐** `V4_G8_P016` / `group8_stair_grid` / `G8 stair 20b/-0.05 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P025` / `group8_stair_grid` / `G8 stair 22b/-0.05 44b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G8_P017` / `group8_stair_grid` / `G8 stair 20b/-0.05 48b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P026` / `group8_stair_grid` / `G8 stair 22b/-0.06 36b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.21）
- **推荐** `V4_G8_P018` / `group8_stair_grid` / `G8 stair 20b/-0.06 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G8_P027` / `group8_stair_grid` / `G8 stair 22b/-0.06 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V4_G8_P028` / `group8_stair_grid` / `G8 stair 22b/-0.06 48b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P019` / `group8_stair_grid` / `G8 stair 20b/-0.06 40b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.26）
- **推荐** `V4_G8_P029` / `group8_stair_grid` / `G8 stair 22b/-0.07 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.22）
- **推荐** `V4_G8_P020` / `group8_stair_grid` / `G8 stair 20b/-0.06 44b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.23）
- **推荐** `V4_G8_P030` / `group8_stair_grid` / `G8 stair 22b/-0.07 40b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P021` / `group8_stair_grid` / `G8 stair 20b/-0.07 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.17）
- **推荐** `V4_G8_P031` / `group8_stair_grid` / `G8 stair 24b/-0.05 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G8_P022` / `group8_stair_grid` / `G8 stair 20b/-0.07 40b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.18）
- **推荐** `V4_G8_P023` / `group8_stair_grid` / `G8 stair 20b/-0.07 48b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P024` / `group8_stair_grid` / `G8 stair 22b/-0.05 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P025` / `group8_stair_grid` / `G8 stair 22b/-0.05 44b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G8_P034` / `group8_stair_grid` / `G8 stair 24b/-0.06 48b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P035` / `group8_stair_grid` / `G8 stair 24b/-0.07 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P026` / `group8_stair_grid` / `G8 stair 22b/-0.06 36b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.21）
- **推荐** `V4_G8_P027` / `group8_stair_grid` / `G8 stair 22b/-0.06 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V4_G8_P036` / `group8_stair_grid` / `G8 stair 24b/-0.07 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.23）
- **推荐** `V4_G8_P028` / `group8_stair_grid` / `G8 stair 22b/-0.06 48b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P029` / `group8_stair_grid` / `G8 stair 22b/-0.07 36b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.22）
- **推荐** `V4_G8_P030` / `group8_stair_grid` / `G8 stair 22b/-0.07 40b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P031` / `group8_stair_grid` / `G8 stair 24b/-0.05 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.16）
- **推荐** `V4_G8_P033` / `group8_stair_grid` / `G8 stair 24b/-0.06 40b/-0.05`：三阶段通过且 Sharpe>1.0（OOS=1.21）
- **推荐** `V4_G8_P034` / `group8_stair_grid` / `G8 stair 24b/-0.06 48b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.20）
- **推荐** `V4_G8_P035` / `group8_stair_grid` / `G8 stair 24b/-0.07 36b/-0.04`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V4_G8_P036` / `group8_stair_grid` / `G8 stair 24b/-0.07 40b/-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.23）
- **推荐** `V4_G10_P001` / `group10_stoch` / `G10 Stoch K=9 D=3 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G10_P005` / `group10_stoch` / `G10 Stoch K=9 D=5 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G10_P009` / `group10_stoch` / `G10 Stoch K=14 D=3 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G10_P001` / `group10_stoch` / `G10 Stoch K=9 D=3 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G10_P013` / `group10_stoch` / `G10 Stoch K=14 D=5 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G10_P005` / `group10_stoch` / `G10 Stoch K=9 D=5 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V4_G10_P017` / `group10_stoch` / `G10 Stoch K=21 D=3 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G10_P009` / `group10_stoch` / `G10 Stoch K=14 D=3 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G10_P021` / `group10_stoch` / `G10 Stoch K=21 D=5 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G10_P013` / `group10_stoch` / `G10 Stoch K=14 D=5 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G10_P017` / `group10_stoch` / `G10 Stoch K=21 D=3 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V4_G10_P021` / `group10_stoch` / `G10 Stoch K=21 D=5 th>60 stair=True`：三阶段通过且 Sharpe>1.0（OOS=1.25）

### 观察名单

- **观察** `V4_G2_P012` / `group2_macd` / `G2 MACD f12s26sig9 hist_rise stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G2_P010` / `group2_macd` / `G2 MACD f12s26sig9 hist_pos stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G2_P012` / `group2_macd` / `G2 MACD f12s26sig9 hist_rise stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G3_P003` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.001 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.98），未达「推荐」门槛
- **观察** `V4_G3_P004` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.002 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.96），未达「推荐」门槛
- **观察** `V4_G3_P006` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.003 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.94），未达「推荐」门槛
- **观察** `V4_G3_P009` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.001 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G3_P011` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.002 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.99），未达「推荐」门槛
- **观察** `V4_G3_P003` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.001 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.98），未达「推荐」门槛
- **观察** `V4_G3_P004` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.002 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.96），未达「推荐」门槛
- **观察** `V4_G3_P005` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.002 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V4_G3_P006` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.003 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.94），未达「推荐」门槛
- **观察** `V4_G3_P017` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.002 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.99），未达「推荐」门槛
- **观察** `V4_G3_P009` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.001 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G3_P011` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.002 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.99），未达「推荐」门槛
- **观察** `V4_G3_P017` / `group3_ema_slope` / `G3 EMA slope p=8 th=0.002 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.99），未达「推荐」门槛
- **观察** `V4_G8_P032` / `group8_stair_grid` / `G8 stair 24b/-0.05 44b/-0.03`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.99），未达「推荐」门槛
- **观察** `V4_G8_P032` / `group8_stair_grid` / `G8 stair 24b/-0.05 44b/-0.03`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.99），未达「推荐」门槛
- **观察** `V4_G10_P002` / `group10_stoch` / `G10 Stoch K=9 D=3 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.98），未达「推荐」门槛
- **观察** `V4_G10_P006` / `group10_stoch` / `G10 Stoch K=9 D=5 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.98），未达「推荐」门槛
- **观察** `V4_G10_P010` / `group10_stoch` / `G10 Stoch K=14 D=3 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛
- **观察** `V4_G10_P002` / `group10_stoch` / `G10 Stoch K=9 D=3 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.98），未达「推荐」门槛
- **观察** `V4_G10_P014` / `group10_stoch` / `G10 Stoch K=14 D=5 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛
- **观察** `V4_G10_P006` / `group10_stoch` / `G10 Stoch K=9 D=5 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.98），未达「推荐」门槛
- **观察** `V4_G10_P018` / `group10_stoch` / `G10 Stoch K=21 D=3 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G10_P019` / `group10_stoch` / `G10 Stoch K=21 D=3 th>80 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V4_G10_P010` / `group10_stoch` / `G10 Stoch K=14 D=3 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛
- **观察** `V4_G10_P022` / `group10_stoch` / `G10 Stoch K=21 D=5 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G10_P023` / `group10_stoch` / `G10 Stoch K=21 D=5 th>80 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V4_G10_P014` / `group10_stoch` / `G10 Stoch K=14 D=5 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛
- **观察** `V4_G10_P018` / `group10_stoch` / `G10 Stoch K=21 D=3 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G10_P019` / `group10_stoch` / `G10 Stoch K=21 D=3 th>80 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V4_G10_P022` / `group10_stoch` / `G10 Stoch K=21 D=5 th>60 stair=False`：三阶段均通过，但全样本 Sharpe≤1.0（当前 1.00），未达「推荐」门槛
- **观察** `V4_G10_P023` / `group10_stoch` / `G10 Stoch K=21 D=5 th>80 stair=True`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛

### 放弃/未过关

- **放弃** `V4_G1_P008` / `group1_dc_exit` / `G1 DCexit p=7 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P001` / `group1_dc_exit` / `G1 DCexit p=5 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P009` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P002` / `group1_dc_exit` / `G1 DCexit p=5 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P010` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P003` / `group1_dc_exit` / `G1 DCexit p=5 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P011` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P004` / `group1_dc_exit` / `G1 DCexit p=5 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P012` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P005` / `group1_dc_exit` / `G1 DCexit p=5 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P013` / `group1_dc_exit` / `G1 DCexit p=10 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P006` / `group1_dc_exit` / `G1 DCexit p=5 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P014` / `group1_dc_exit` / `G1 DCexit p=10 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P007` / `group1_dc_exit` / `G1 DCexit p=7 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P015` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P008` / `group1_dc_exit` / `G1 DCexit p=7 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P016` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P009` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P017` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P010` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P018` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P011` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P019` / `group1_dc_exit` / `G1 DCexit p=12 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P012` / `group1_dc_exit` / `G1 DCexit p=7 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P020` / `group1_dc_exit` / `G1 DCexit p=12 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P013` / `group1_dc_exit` / `G1 DCexit p=10 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P021` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P014` / `group1_dc_exit` / `G1 DCexit p=10 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P022` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P015` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P023` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P016` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P024` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P017` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P025` / `group1_dc_exit` / `G1 DCexit p=15 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P018` / `group1_dc_exit` / `G1 DCexit p=10 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P026` / `group1_dc_exit` / `G1 DCexit p=15 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P019` / `group1_dc_exit` / `G1 DCexit p=12 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P027` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P020` / `group1_dc_exit` / `G1 DCexit p=12 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P028` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P021` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P029` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P022` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P030` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P023` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P024` / `group1_dc_exit` / `G1 DCexit p=12 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G1_P025` / `group1_dc_exit` / `G1 DCexit p=15 dc_only mb=0`：未通过阶段1
- **放弃** `V4_G1_P026` / `group1_dc_exit` / `G1 DCexit p=15 dc_only mb=8`：未通过阶段1
- **放弃** `V4_G1_P027` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail mb=0`：未通过阶段1
- **放弃** `V4_G1_P028` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail mb=8`：未通过阶段1
- **放弃** `V4_G1_P029` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail_stair mb=0`：未通过阶段1
- **放弃** `V4_G1_P030` / `group1_dc_exit` / `G1 DCexit p=15 dc_trail_stair mb=8`：未通过阶段1
- **放弃** `V4_G2_P009` / `group2_macd` / `G2 MACD f12s26sig9 hist_pos stair=True`：未通过阶段1
- **放弃** `V4_G2_P010` / `group2_macd` / `G2 MACD f12s26sig9 hist_pos stair=False`：未通过阶段1
- **放弃** `V4_G2_P006` / `group2_macd` / `G2 MACD f8s21sig5 macd_pos stair=False`：未通过阶段1
- **放弃** `V4_G2_P015` / `group2_macd` / `G2 MACD f12s26sig9 macd_sig_hist stair=True`：未通过阶段1
- **放弃** `V4_G2_P016` / `group2_macd` / `G2 MACD f12s26sig9 macd_sig_hist stair=False`：未通过阶段1
- **放弃** `V4_G2_P017` / `group2_macd` / `G2 MACD f8s17sig9 hist_pos stair=True`：未通过阶段1
- **放弃** `V4_G2_P018` / `group2_macd` / `G2 MACD f8s17sig9 hist_pos stair=False`：未通过阶段1
- **放弃** `V4_G2_P019` / `group2_macd` / `G2 MACD f8s17sig9 hist_rise stair=True`：未通过阶段1
- **放弃** `V4_G2_P020` / `group2_macd` / `G2 MACD f8s17sig9 hist_rise stair=False`：未通过阶段1
- **放弃** `V4_G2_P023` / `group2_macd` / `G2 MACD f8s17sig9 macd_sig_hist stair=True`：未通过阶段1
- **放弃** `V4_G2_P016` / `group2_macd` / `G2 MACD f12s26sig9 macd_sig_hist stair=False`：未通过阶段1
- **放弃** `V4_G3_P001` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.0005 stair=True`：未通过阶段1
- **放弃** `V4_G3_P002` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.001 stair=True`：未通过阶段1
- **放弃** `V4_G3_P005` / `group3_ema_slope` / `G3 EMA slope p=3 th=0.002 stair=False`：未通过阶段1
- **放弃** `V4_G3_P008` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.001 stair=True`：未通过阶段1
- **放弃** `V4_G3_P012` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.003 stair=True`：未通过阶段1
- **放弃** `V4_G4_P001` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>0 stair=True`：未通过阶段1
- **放弃** `V4_G4_P002` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>0 stair=False`：未通过阶段1
- **放弃** `V4_G4_P003` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>25 stair=True`：未通过阶段1
- **放弃** `V4_G4_P004` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>25 stair=False`：未通过阶段1
- **放弃** `V4_G3_P012` / `group3_ema_slope` / `G3 EMA slope p=5 th=0.003 stair=True`：未通过阶段1
- **放弃** `V4_G4_P005` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>30 stair=True`：未通过阶段1
- **放弃** `V4_G4_P006` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>30 stair=False`：未通过阶段1
- **放弃** `V4_G4_P007` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>0 stair=True`：未通过阶段1
- **放弃** `V4_G4_P008` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>0 stair=False`：未通过阶段1
- **放弃** `V4_G4_P009` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>25 stair=True`：未通过阶段1
- **放弃** `V4_G4_P010` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>25 stair=False`：未通过阶段1
- **放弃** `V4_G4_P011` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>30 stair=True`：未通过阶段1
- **放弃** `V4_G4_P012` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>30 stair=False`：未通过阶段1
- **放弃** `V4_G4_P013` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>0 stair=True`：未通过阶段1
- **放弃** `V4_G4_P014` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>0 stair=False`：未通过阶段1
- **放弃** `V4_G4_P015` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>25 stair=True`：未通过阶段1
- **放弃** `V4_G4_P016` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>25 stair=False`：未通过阶段1
- **放弃** `V4_G4_P017` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>30 stair=True`：未通过阶段1
- **放弃** `V4_G4_P018` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>30 stair=False`：未通过阶段1
- **放弃** `V4_G4_P001` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>0 stair=True`：未通过阶段1
- **放弃** `V4_G4_P002` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>0 stair=False`：未通过阶段1
- **放弃** `V4_G5_P001` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G4_P003` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>25 stair=True`：未通过阶段1
- **放弃** `V4_G4_P004` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>25 stair=False`：未通过阶段1
- **放弃** `V4_G5_P002` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G4_P005` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>30 stair=True`：未通过阶段1
- **放弃** `V4_G4_P006` / `group4_1h_confirm` / `G4 1H 1h_only adx1h>30 stair=False`：未通过阶段1
- **放弃** `V4_G5_P003` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G4_P007` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>0 stair=True`：未通过阶段1
- **放弃** `V4_G4_P008` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>0 stair=False`：未通过阶段1
- **放弃** `V4_G5_P004` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G4_P009` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>25 stair=True`：未通过阶段1
- **放弃** `V4_G4_P010` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>25 stair=False`：未通过阶段1
- **放弃** `V4_G5_P005` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G4_P011` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>30 stair=True`：未通过阶段1
- **放弃** `V4_G4_P012` / `group4_1h_confirm` / `G4 1H 1h_and_4h adx1h>30 stair=False`：未通过阶段1
- **放弃** `V4_G5_P006` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G4_P013` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>0 stair=True`：未通过阶段1
- **放弃** `V4_G4_P014` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>0 stair=False`：未通过阶段1
- **放弃** `V4_G5_P007` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G4_P015` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>25 stair=True`：未通过阶段1
- **放弃** `V4_G5_P008` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G4_P016` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>25 stair=False`：未通过阶段1
- **放弃** `V4_G4_P017` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>30 stair=True`：未通过阶段1
- **放弃** `V4_G5_P009` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G4_P018` / `group4_1h_confirm` / `G4 1H 1h_or_4h adx1h>30 stair=False`：未通过阶段1
- **放弃** `V4_G5_P010` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G5_P001` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G5_P002` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G5_P011` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G5_P003` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G5_P012` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G5_P004` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G5_P013` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G5_P005` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G5_P014` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G5_P006` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G5_P015` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G5_P007` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G5_P016` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P008` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G5_P017` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P009` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G5_P018` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P010` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G5_P019` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P011` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G5_P020` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P012` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G5_P021` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P013` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.3 stair=True`：未通过阶段1
- **放弃** `V4_G5_P022` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P014` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.5 stair=True`：未通过阶段1
- **放弃** `V4_G5_P023` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P015` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.7 stair=True`：未通过阶段1
- **放弃** `V4_G5_P024` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P016` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P025` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P017` / `group5_profit_giveback` / `G5 giveback mp=0.05 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P018` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P019` / `group5_profit_giveback` / `G5 giveback mp=0.08 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P020` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P021` / `group5_profit_giveback` / `G5 giveback mp=0.1 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P022` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P023` / `group5_profit_giveback` / `G5 giveback mp=0.15 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G5_P024` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.5 stair=False`：未通过阶段1
- **放弃** `V4_G5_P025` / `group5_profit_giveback` / `G5 giveback mp=0.2 kr=0.7 stair=False`：未通过阶段1
- **放弃** `V4_G6_P018` / `group6_dynamic_dc` / `G6 dynDC lb=100 s=16 L=30 th=0.7`：未通过阶段1
- **放弃** `V4_G7_BTC_PG01` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=26 ATR=0.5 DC=20`：未通过阶段1
- **放弃** `V4_G7_BTC_PG02` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=20`：未通过阶段1
- **放弃** `V4_G7_BTC_PG03` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=30 ATR=0.7 DC=20`：未通过阶段1
- **放弃** `V4_G7_BTC_PG04` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.5 DC=14`：未通过阶段1
- **放弃** `V4_G7_BTC_PG05` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=14`：未通过阶段1
- **放弃** `V4_G7_BTC_PG06` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.8 DC=20`：未通过阶段1
- **放弃** `V4_G7_BTC_PG07` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=26 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_BTC_PG08` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=30 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_ETH_PG01` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=26 ATR=0.5 DC=20`：未通过阶段1
- **放弃** `V4_G7_ETH_PG02` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=20`：未通过阶段1
- **放弃** `V4_G7_ETH_PG03` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=30 ATR=0.7 DC=20`：未通过阶段1
- **放弃** `V4_G7_ETH_PG04` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=28 ATR=0.5 DC=14`：未通过阶段1
- **放弃** `V4_G7_ETH_PG05` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=14`：未通过阶段1
- **放弃** `V4_G7_ETH_PG06` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=28 ATR=0.8 DC=20`：未通过阶段1
- **放弃** `V4_G7_ETH_PG07` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=26 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_ETH_PG08` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=30 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_BTC_PG01` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=26 ATR=0.5 DC=20`：未通过阶段1
- **放弃** `V4_G7_SOL_PG01` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=26 ATR=0.5 DC=20`：未通过阶段1
- **放弃** `V4_G7_SOL_PG02` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=28 ATR=0.6 DC=20`：未通过阶段1
- **放弃** `V4_G7_BTC_PG02` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=20`：未通过阶段1
- **放弃** `V4_G7_SOL_PG03` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=30 ATR=0.7 DC=20`：未通过阶段1
- **放弃** `V4_G7_BTC_PG03` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=30 ATR=0.7 DC=20`：未通过阶段1
- **放弃** `V4_G7_SOL_PG04` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=28 ATR=0.5 DC=14`：未通过阶段1
- **放弃** `V4_G7_BTC_PG04` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.5 DC=14`：未通过阶段1
- **放弃** `V4_G7_SOL_PG05` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=28 ATR=0.6 DC=14`：未通过阶段1
- **放弃** `V4_G7_BTC_PG05` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=14`：未通过阶段1
- **放弃** `V4_G7_SOL_PG06` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=28 ATR=0.8 DC=20`：未通过阶段1
- **放弃** `V4_G7_BTC_PG06` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=28 ATR=0.8 DC=20`：未通过阶段1
- **放弃** `V4_G7_SOL_PG07` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=26 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_BTC_PG07` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=26 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_SOL_PG08` / `group7_per_pair_params` / `G7 SOL/USDT:USDT ADX=30 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_BTC_PG08` / `group7_per_pair_params` / `G7 BTC/USDT:USDT ADX=30 ATR=0.6 DC=25`：未通过阶段1
- **放弃** `V4_G7_ADA_PG01` / `group7_per_pair_params` / `G7 ADA/USDT:USDT ADX=26 ATR=0.5 DC=20`：未通过阶段1
- **放弃** `V4_G7_ADA_PG02` / `group7_per_pair_params` / `G7 ADA/USDT:USDT ADX=28 ATR=0.6 DC=20`：未通过阶段1
- **放弃** `V4_G7_ETH_PG01` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=26 ATR=0.5 DC=20`：未通过阶段1
- **放弃** `V4_G7_ADA_PG03` / `group7_per_pair_params` / `G7 ADA/USDT:USDT ADX=30 ATR=0.7 DC=20`：未通过阶段1
- **放弃** `V4_G7_ETH_PG02` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=20`：未通过阶段1
- **放弃** `V4_G7_ADA_PG04` / `group7_per_pair_params` / `G7 ADA/USDT:USDT ADX=28 ATR=0.5 DC=14`：未通过阶段1
- **放弃** `V4_G7_ETH_PG03` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=30 ATR=0.7 DC=20`：未通过阶段1
- **放弃** `V4_G7_ADA_PG05` / `group7_per_pair_params` / `G7 ADA/USDT:USDT ADX=28 ATR=0.6 DC=14`：未通过阶段1
- **放弃** `V4_G7_ETH_PG04` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=28 ATR=0.5 DC=14`：未通过阶段1
- **放弃** `V4_G7_ADA_PG06` / `group7_per_pair_params` / `G7 ADA/USDT:USDT ADX=28 ATR=0.8 DC=20`：未通过阶段1
- **放弃** `V4_G7_ETH_PG05` / `group7_per_pair_params` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=14`：未通过阶段1

> 放弃条目过多，仅显示前 200 条，共 350 条。

## 7. 失败方向总结（按 group，避免重复踩坑）

### group `group10_stoch`

- **失败** `V4_G10_P012` / `G10 Stoch K=14 D=3 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.68, PF=1.25, 交易=955, 回撤%=3.00)
- **失败** `V4_G10_P012` / `G10 Stoch K=14 D=3 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.68, PF=1.25, 交易=955, 回撤%=15.33)
- **失败** `V4_G10_P011` / `G10 Stoch K=14 D=3 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.73, PF=1.28, 交易=965, 回撤%=7.00)
- **失败** `V4_G10_P011` / `G10 Stoch K=14 D=3 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.73, PF=1.28, 交易=965, 回撤%=12.57)
- **失败** `V4_G10_P016` / `G10 Stoch K=14 D=5 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.68, PF=1.25, 交易=955, 回撤%=3.00)
- **失败** `V4_G10_P016` / `G10 Stoch K=14 D=5 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.68, PF=1.25, 交易=955, 回撤%=15.33)
- **失败** `V4_G10_P015` / `G10 Stoch K=14 D=5 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.73, PF=1.28, 交易=965, 回撤%=7.00)
- **失败** `V4_G10_P015` / `G10 Stoch K=14 D=5 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.73, PF=1.28, 交易=965, 回撤%=12.57)
- **失败** `V4_G10_P020` / `G10 Stoch K=21 D=3 th>80 stair=False`：Sharpe<0.9 (Sharpe=0.81, PF=1.30, 交易=1001, 回撤%=6.00)
- **失败** `V4_G10_P020` / `G10 Stoch K=21 D=3 th>80 stair=False`：Sharpe<0.9 (Sharpe=0.81, PF=1.30, 交易=1001, 回撤%=17.16)
- **失败** `V4_G10_P024` / `G10 Stoch K=21 D=5 th>80 stair=False`：Sharpe<0.9 (Sharpe=0.81, PF=1.30, 交易=1001, 回撤%=6.00)
- **失败** `V4_G10_P024` / `G10 Stoch K=21 D=5 th>80 stair=False`：Sharpe<0.9 (Sharpe=0.81, PF=1.30, 交易=1001, 回撤%=17.16)
- **失败** `V4_G10_P004` / `G10 Stoch K=9 D=3 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.22, 交易=886, 回撤%=9.00)
- **失败** `V4_G10_P004` / `G10 Stoch K=9 D=3 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.22, 交易=886, 回撤%=12.09)
- **失败** `V4_G10_P003` / `G10 Stoch K=9 D=3 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.21, 交易=894, 回撤%=1.00)
- **失败** `V4_G10_P003` / `G10 Stoch K=9 D=3 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.21, 交易=894, 回撤%=11.91)
- **失败** `V4_G10_P008` / `G10 Stoch K=9 D=5 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.22, 交易=886, 回撤%=9.00)
- **失败** `V4_G10_P008` / `G10 Stoch K=9 D=5 th>80 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.22, 交易=886, 回撤%=12.09)
- **失败** `V4_G10_P007` / `G10 Stoch K=9 D=5 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.21, 交易=894, 回撤%=1.00)
- **失败** `V4_G10_P007` / `G10 Stoch K=9 D=5 th>80 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.21, 交易=894, 回撤%=11.91)

### group `group11_trend_score`

- **失败** `V4_G11_P002` / `G11 score>0.6 equal stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.09, 交易=3039, 回撤%=6.00)
- **失败** `V4_G11_P002` / `G11 score>0.6 equal stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.80, PF=1.09, 交易=3039, 回撤%=42.86)
- **失败** `V4_G11_P001` / `G11 score>0.6 equal stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.88, PF=1.09, 交易=3222, 回撤%=8.00)
- **失败** `V4_G11_P001` / `G11 score>0.6 equal stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.88, PF=1.09, 交易=3222, 回撤%=27.38)
- **失败** `V4_G11_P004` / `G11 score>0.6 w_adx2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.09, 交易=3041, 回撤%=7.00)
- **失败** `V4_G11_P004` / `G11 score>0.6 w_adx2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.80, PF=1.09, 交易=3041, 回撤%=42.97)
- **失败** `V4_G11_P003` / `G11 score>0.6 w_adx2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.86, PF=1.09, 交易=3226, 回撤%=7.00)
- **失败** `V4_G11_P003` / `G11 score>0.6 w_adx2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.86, PF=1.09, 交易=3226, 回撤%=40.27)
- **失败** `V4_G11_P006` / `G11 score>0.6 w_atr2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.81, PF=1.09, 交易=3040, 回撤%=1.00)
- **失败** `V4_G11_P006` / `G11 score>0.6 w_atr2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.81, PF=1.09, 交易=3040, 回撤%=42.61)
- **失败** `V4_G11_P005` / `G11 score>0.6 w_atr2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.87, PF=1.09, 交易=3224, 回撤%=9.00)
- **失败** `V4_G11_P005` / `G11 score>0.6 w_atr2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.87, PF=1.09, 交易=3224, 回撤%=39.89)
- **失败** `V4_G11_P008` / `G11 score>0.6 w_di2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.09, 交易=3038, 回撤%=8.00)
- **失败** `V4_G11_P008` / `G11 score>0.6 w_di2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.80, PF=1.09, 交易=3038, 回撤%=42.38)
- **失败** `V4_G11_P007` / `G11 score>0.6 w_di2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.87, PF=1.09, 交易=3223, 回撤%=0.00)
- **失败** `V4_G11_P007` / `G11 score>0.6 w_di2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.87, PF=1.09, 交易=3223, 回撤%=27.30)
- **失败** `V4_G11_P010` / `G11 score>0.6 w_slope2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.82, PF=1.09, 交易=3038, 回撤%=0.00)
- **失败** `V4_G11_P010` / `G11 score>0.6 w_slope2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.82, PF=1.09, 交易=3038, 回撤%=43.20)
- **失败** `V4_G11_P009` / `G11 score>0.6 w_slope2 stair=True`：PF<1.3 (Sharpe=0.90, PF=1.10, 交易=3221, 回撤%=4.00)
- **失败** `V4_G11_P009` / `G11 score>0.6 w_slope2 stair=True`：PF<1.3；回撤>25.0% (Sharpe=0.90, PF=1.10, 交易=3221, 回撤%=40.24)
- **失败** `V4_G11_P012` / `G11 score>0.8 equal stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.81, PF=1.09, 交易=3036, 回撤%=2.00)
- **失败** `V4_G11_P012` / `G11 score>0.8 equal stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.81, PF=1.09, 交易=3036, 回撤%=42.62)
- **失败** `V4_G11_P011` / `G11 score>0.8 equal stair=True`：PF<1.3 (Sharpe=0.90, PF=1.10, 交易=3218, 回撤%=5.00)
- **失败** `V4_G11_P011` / `G11 score>0.8 equal stair=True`：PF<1.3；回撤>25.0% (Sharpe=0.90, PF=1.10, 交易=3218, 回撤%=27.45)
- **失败** `V4_G11_P014` / `G11 score>0.8 w_adx2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.09, 交易=3041, 回撤%=4.00)
- **失败** `V4_G11_P014` / `G11 score>0.8 w_adx2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.80, PF=1.09, 交易=3041, 回撤%=42.94)
- **失败** `V4_G11_P013` / `G11 score>0.8 w_adx2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.86, PF=1.09, 交易=3225, 回撤%=3.00)
- **失败** `V4_G11_P013` / `G11 score>0.8 w_adx2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.86, PF=1.09, 交易=3225, 回撤%=40.33)
- **失败** `V4_G11_P016` / `G11 score>0.8 w_atr2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.09, 交易=3039, 回撤%=7.00)
- **失败** `V4_G11_P016` / `G11 score>0.8 w_atr2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.80, PF=1.09, 交易=3039, 回撤%=42.87)
- **失败** `V4_G11_P015` / `G11 score>0.8 w_atr2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.87, PF=1.09, 交易=3222, 回撤%=7.00)
- **失败** `V4_G11_P015` / `G11 score>0.8 w_atr2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.87, PF=1.09, 交易=3222, 回撤%=27.57)
- **失败** `V4_G11_P018` / `G11 score>0.8 w_di2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.09, 交易=3039, 回撤%=0.00)
- **失败** `V4_G11_P018` / `G11 score>0.8 w_di2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.80, PF=1.09, 交易=3039, 回撤%=42.30)
- **失败** `V4_G11_P017` / `G11 score>0.8 w_di2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.88, PF=1.09, 交易=3222, 回撤%=7.00)
- **失败** `V4_G11_P017` / `G11 score>0.8 w_di2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.88, PF=1.09, 交易=3222, 回撤%=27.27)
- **失败** `V4_G11_P020` / `G11 score>0.8 w_slope2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.83, PF=1.09, 交易=3035, 回撤%=0.00)
- **失败** `V4_G11_P020` / `G11 score>0.8 w_slope2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.83, PF=1.09, 交易=3035, 回撤%=42.60)
- **失败** `V4_G11_P019` / `G11 score>0.8 w_slope2 stair=True`：PF<1.3 (Sharpe=0.91, PF=1.10, 交易=3218, 回撤%=1.00)
- **失败** `V4_G11_P019` / `G11 score>0.8 w_slope2 stair=True`：PF<1.3；回撤>25.0% (Sharpe=0.91, PF=1.10, 交易=3218, 回撤%=27.51)
- **失败** `V4_G11_P022` / `G11 score>1.0 equal stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.82, PF=1.09, 交易=3033, 回撤%=5.00)
- **失败** `V4_G11_P022` / `G11 score>1.0 equal stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.82, PF=1.09, 交易=3033, 回撤%=41.95)
- **失败** `V4_G11_P021` / `G11 score>1.0 equal stair=True`：PF<1.3 (Sharpe=0.91, PF=1.10, 交易=3215, 回撤%=3.00)
- **失败** `V4_G11_P021` / `G11 score>1.0 equal stair=True`：PF<1.3；回撤>25.0% (Sharpe=0.91, PF=1.10, 交易=3215, 回撤%=27.33)
- **失败** `V4_G11_P024` / `G11 score>1.0 w_adx2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.79, PF=1.09, 交易=3041, 回撤%=7.00)
- **失败** `V4_G11_P024` / `G11 score>1.0 w_adx2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.79, PF=1.09, 交易=3041, 回撤%=42.87)
- **失败** `V4_G11_P023` / `G11 score>1.0 w_adx2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.88, PF=1.09, 交易=3223, 回撤%=1.00)
- **失败** `V4_G11_P023` / `G11 score>1.0 w_adx2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.88, PF=1.09, 交易=3223, 回撤%=39.91)
- **失败** `V4_G11_P026` / `G11 score>1.0 w_atr2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.09, 交易=3036, 回撤%=7.00)
- **失败** `V4_G11_P026` / `G11 score>1.0 w_atr2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.80, PF=1.09, 交易=3036, 回撤%=41.97)
- **失败** `V4_G11_P025` / `G11 score>1.0 w_atr2 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.87, PF=1.09, 交易=3219, 回撤%=4.00)
- **失败** `V4_G11_P025` / `G11 score>1.0 w_atr2 stair=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.87, PF=1.09, 交易=3219, 回撤%=27.44)
- **失败** `V4_G11_P028` / `G11 score>1.0 w_di2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.81, PF=1.09, 交易=3035, 回撤%=2.00)
- **失败** `V4_G11_P028` / `G11 score>1.0 w_di2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.81, PF=1.09, 交易=3035, 回撤%=42.52)
- **失败** `V4_G11_P027` / `G11 score>1.0 w_di2 stair=True`：PF<1.3 (Sharpe=0.90, PF=1.10, 交易=3217, 回撤%=6.00)
- **失败** `V4_G11_P027` / `G11 score>1.0 w_di2 stair=True`：PF<1.3；回撤>25.0% (Sharpe=0.90, PF=1.10, 交易=3217, 回撤%=27.46)
- **失败** `V4_G11_P030` / `G11 score>1.0 w_slope2 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.09, 交易=3033, 回撤%=5.00)
- **失败** `V4_G11_P030` / `G11 score>1.0 w_slope2 stair=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.84, PF=1.09, 交易=3033, 回撤%=41.95)
- **失败** `V4_G11_P029` / `G11 score>1.0 w_slope2 stair=True`：PF<1.3 (Sharpe=0.91, PF=1.10, 交易=3214, 回撤%=9.00)
- **失败** `V4_G11_P029` / `G11 score>1.0 w_slope2 stair=True`：PF<1.3；回撤>25.0% (Sharpe=0.91, PF=1.10, 交易=3214, 回撤%=27.49)

### group `group1_dc_exit`

- **失败** `V4_G1_P013` / `G1 DCexit p=10 dc_only mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.24, PF=1.08, 交易=1132, 回撤%=9.00)
- **失败** `V4_G1_P013` / `G1 DCexit p=10 dc_only mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.24, PF=1.08, 交易=1132, 回撤%=16.39)
- **失败** `V4_G1_P014` / `G1 DCexit p=10 dc_only mb=8`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G1_P014` / `G1 DCexit p=10 dc_only mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.27, PF=1.09, 交易=1129, 回撤%=16.58)
- **失败** `V4_G1_P015` / `G1 DCexit p=10 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.52, PF=1.17, 交易=1195, 回撤%=3.00)
- **失败** `V4_G1_P015` / `G1 DCexit p=10 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.52, PF=1.17, 交易=1195, 回撤%=16.53)
- **失败** `V4_G1_P016` / `G1 DCexit p=10 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.18, 交易=1193, 回撤%=9.00)
- **失败** `V4_G1_P016` / `G1 DCexit p=10 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.18, 交易=1193, 回撤%=16.79)
- **失败** `V4_G1_P017` / `G1 DCexit p=10 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.54, PF=1.17, 交易=1198, 回撤%=7.00)
- **失败** `V4_G1_P017` / `G1 DCexit p=10 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.54, PF=1.17, 交易=1198, 回撤%=14.97)
- **失败** `V4_G1_P018` / `G1 DCexit p=10 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.18, 交易=1196, 回撤%=6.00)
- **失败** `V4_G1_P018` / `G1 DCexit p=10 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.18, 交易=1196, 回撤%=15.26)
- **失败** `V4_G1_P019` / `G1 DCexit p=12 dc_only mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.32, PF=1.11, 交易=1107, 回撤%=1.00)
- **失败** `V4_G1_P019` / `G1 DCexit p=12 dc_only mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.32, PF=1.11, 交易=1107, 回撤%=16.51)
- **失败** `V4_G1_P020` / `G1 DCexit p=12 dc_only mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.34, PF=1.12, 交易=1105, 回撤%=6.00)
- **失败** `V4_G1_P020` / `G1 DCexit p=12 dc_only mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.34, PF=1.12, 交易=1105, 回撤%=16.56)
- **失败** `V4_G1_P021` / `G1 DCexit p=12 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.62, PF=1.20, 交易=1176, 回撤%=2.00)
- **失败** `V4_G1_P021` / `G1 DCexit p=12 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.62, PF=1.20, 交易=1176, 回撤%=15.92)
- **失败** `V4_G1_P022` / `G1 DCexit p=12 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.65, PF=1.21, 交易=1175, 回撤%=3.00)
- **失败** `V4_G1_P022` / `G1 DCexit p=12 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.65, PF=1.21, 交易=1175, 回撤%=15.93)
- **失败** `V4_G1_P023` / `G1 DCexit p=12 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.66, PF=1.22, 交易=1179, 回撤%=5.00)
- **失败** `V4_G1_P023` / `G1 DCexit p=12 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.66, PF=1.22, 交易=1179, 回撤%=15.25)
- **失败** `V4_G1_P024` / `G1 DCexit p=12 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.67, PF=1.22, 交易=1178, 回撤%=1.00)
- **失败** `V4_G1_P024` / `G1 DCexit p=12 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.67, PF=1.22, 交易=1178, 回撤%=15.31)
- **失败** `V4_G1_P025` / `G1 DCexit p=15 dc_only mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.38, PF=1.13, 交易=1086, 回撤%=4.00)
- **失败** `V4_G1_P025` / `G1 DCexit p=15 dc_only mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.38, PF=1.13, 交易=1086, 回撤%=17.24)
- **失败** `V4_G1_P026` / `G1 DCexit p=15 dc_only mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.39, PF=1.13, 交易=1085, 回撤%=6.00)
- **失败** `V4_G1_P026` / `G1 DCexit p=15 dc_only mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.39, PF=1.13, 交易=1085, 回撤%=17.26)
- **失败** `V4_G1_P027` / `G1 DCexit p=15 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.64, PF=1.21, 交易=1157, 回撤%=0.00)
- **失败** `V4_G1_P027` / `G1 DCexit p=15 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.64, PF=1.21, 交易=1157, 回撤%=16.30)
- **失败** `V4_G1_P028` / `G1 DCexit p=15 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.66, PF=1.22, 交易=1156, 回撤%=9.00)
- **失败** `V4_G1_P028` / `G1 DCexit p=15 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.66, PF=1.22, 交易=1156, 回撤%=16.29)
- **失败** `V4_G1_P029` / `G1 DCexit p=15 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.69, PF=1.23, 交易=1160, 回撤%=9.00)
- **失败** `V4_G1_P029` / `G1 DCexit p=15 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.69, PF=1.23, 交易=1160, 回撤%=15.39)
- **失败** `V4_G1_P030` / `G1 DCexit p=15 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.71, PF=1.24, 交易=1159, 回撤%=8.00)
- **失败** `V4_G1_P030` / `G1 DCexit p=15 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.71, PF=1.24, 交易=1159, 回撤%=15.38)
- **失败** `V4_G1_P001` / `G1 DCexit p=5 dc_only mb=0`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-0.05, PF=0.99, 交易=1227, 回撤%=33.71)
- **失败** `V4_G1_P002` / `G1 DCexit p=5 dc_only mb=8`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.05, PF=1.02, 交易=1202, 回撤%=29.02)
- **失败** `V4_G1_P003` / `G1 DCexit p=5 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.40, PF=1.12, 交易=1277, 回撤%=18.51)
- **失败** `V4_G1_P004` / `G1 DCexit p=5 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.48, PF=1.15, 交易=1253, 回撤%=15.01)
- **失败** `V4_G1_P005` / `G1 DCexit p=5 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.41, PF=1.13, 交易=1277, 回撤%=19.23)
- **失败** `V4_G1_P006` / `G1 DCexit p=5 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.50, PF=1.16, 交易=1253, 回撤%=13.16)
- **失败** `V4_G1_P007` / `G1 DCexit p=7 dc_only mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.22, PF=1.07, 交易=1175, 回撤%=20.68)
- **失败** `V4_G1_P008` / `G1 DCexit p=7 dc_only mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.21, PF=1.07, 交易=1169, 回撤%=6.00)
- **失败** `V4_G1_P008` / `G1 DCexit p=7 dc_only mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.21, PF=1.07, 交易=1169, 回撤%=17.46)
- **失败** `V4_G1_P009` / `G1 DCexit p=7 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.18, 交易=1235, 回撤%=6.00)
- **失败** `V4_G1_P009` / `G1 DCexit p=7 dc_trail mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.18, 交易=1235, 回撤%=15.26)
- **失败** `V4_G1_P010` / `G1 DCexit p=7 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.54, PF=1.17, 交易=1229, 回撤%=4.00)
- **失败** `V4_G1_P010` / `G1 DCexit p=7 dc_trail mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.54, PF=1.17, 交易=1229, 回撤%=15.94)
- **失败** `V4_G1_P011` / `G1 DCexit p=7 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.53, PF=1.17, 交易=1236, 回撤%=3.00)
- **失败** `V4_G1_P011` / `G1 DCexit p=7 dc_trail_stair mb=0`：Sharpe<0.9；PF<1.3 (Sharpe=0.53, PF=1.17, 交易=1236, 回撤%=13.63)
- **失败** `V4_G1_P012` / `G1 DCexit p=7 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.53, PF=1.17, 交易=1230, 回撤%=2.00)
- **失败** `V4_G1_P012` / `G1 DCexit p=7 dc_trail_stair mb=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.53, PF=1.17, 交易=1230, 回撤%=14.12)

### group `group2_macd`

- **失败** `V4_G2_P010` / `G2 MACD f12s26sig9 hist_pos stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P009` / `G2 MACD f12s26sig9 hist_pos stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P016` / `G2 MACD f12s26sig9 macd_sig_hist stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P016` / `G2 MACD f12s26sig9 macd_sig_hist stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P015` / `G2 MACD f12s26sig9 macd_sig_hist stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P018` / `G2 MACD f8s17sig9 hist_pos stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P017` / `G2 MACD f8s17sig9 hist_pos stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P020` / `G2 MACD f8s17sig9 hist_rise stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P019` / `G2 MACD f8s17sig9 hist_rise stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P023` / `G2 MACD f8s17sig9 macd_sig_hist stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G2_P006` / `G2 MACD f8s21sig5 macd_pos stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group3_ema_slope`

- **失败** `V4_G3_P001` / `G3 EMA slope p=3 th=0.0005 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G3_P002` / `G3 EMA slope p=3 th=0.001 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G3_P005` / `G3 EMA slope p=3 th=0.002 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G3_P008` / `G3 EMA slope p=5 th=0.001 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G3_P012` / `G3 EMA slope p=5 th=0.003 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G3_P012` / `G3 EMA slope p=5 th=0.003 stair=True`：Sharpe<0.9 (Sharpe=0.87, PF=1.34, 交易=1009, 回撤%=14.16)

### group `group4_1h_confirm`

- **失败** `V4_G4_P008` / `G4 1H 1h_and_4h adx1h>0 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P008` / `G4 1H 1h_and_4h adx1h>0 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P007` / `G4 1H 1h_and_4h adx1h>0 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P007` / `G4 1H 1h_and_4h adx1h>0 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P010` / `G4 1H 1h_and_4h adx1h>25 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P010` / `G4 1H 1h_and_4h adx1h>25 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P009` / `G4 1H 1h_and_4h adx1h>25 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P009` / `G4 1H 1h_and_4h adx1h>25 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P012` / `G4 1H 1h_and_4h adx1h>30 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P012` / `G4 1H 1h_and_4h adx1h>30 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P011` / `G4 1H 1h_and_4h adx1h>30 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P011` / `G4 1H 1h_and_4h adx1h>30 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P002` / `G4 1H 1h_only adx1h>0 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P002` / `G4 1H 1h_only adx1h>0 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P001` / `G4 1H 1h_only adx1h>0 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P001` / `G4 1H 1h_only adx1h>0 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P004` / `G4 1H 1h_only adx1h>25 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P004` / `G4 1H 1h_only adx1h>25 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P003` / `G4 1H 1h_only adx1h>25 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P003` / `G4 1H 1h_only adx1h>25 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P006` / `G4 1H 1h_only adx1h>30 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P006` / `G4 1H 1h_only adx1h>30 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P005` / `G4 1H 1h_only adx1h>30 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P005` / `G4 1H 1h_only adx1h>30 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P014` / `G4 1H 1h_or_4h adx1h>0 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P014` / `G4 1H 1h_or_4h adx1h>0 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P013` / `G4 1H 1h_or_4h adx1h>0 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P013` / `G4 1H 1h_or_4h adx1h>0 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P016` / `G4 1H 1h_or_4h adx1h>25 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P016` / `G4 1H 1h_or_4h adx1h>25 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P015` / `G4 1H 1h_or_4h adx1h>25 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P015` / `G4 1H 1h_or_4h adx1h>25 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P018` / `G4 1H 1h_or_4h adx1h>30 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P018` / `G4 1H 1h_or_4h adx1h>30 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P017` / `G4 1H 1h_or_4h adx1h>30 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G4_P017` / `G4 1H 1h_or_4h adx1h>30 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group5_profit_giveback`

- **失败** `V4_G5_P001` / `G5 giveback mp=0.05 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.70, PF=1.22, 交易=1309, 回撤%=7.00)
- **失败** `V4_G5_P001` / `G5 giveback mp=0.05 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.70, PF=1.22, 交易=1309, 回撤%=15.07)
- **失败** `V4_G5_P016` / `G5 giveback mp=0.05 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.62, PF=1.18, 交易=1284, 回撤%=6.00)
- **失败** `V4_G5_P016` / `G5 giveback mp=0.05 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.62, PF=1.18, 交易=1284, 回撤%=18.26)
- **失败** `V4_G5_P002` / `G5 giveback mp=0.05 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.71, PF=1.22, 交易=1289, 回撤%=7.00)
- **失败** `V4_G5_P002` / `G5 giveback mp=0.05 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.71, PF=1.22, 交易=1289, 回撤%=14.87)
- **失败** `V4_G5_P017` / `G5 giveback mp=0.05 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.74, PF=1.22, 交易=1243, 回撤%=9.00)
- **失败** `V4_G5_P017` / `G5 giveback mp=0.05 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.74, PF=1.22, 交易=1243, 回撤%=16.29)
- **失败** `V4_G5_P003` / `G5 giveback mp=0.05 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.85, PF=1.26, 交易=1251, 回撤%=0.00)
- **失败** `V4_G5_P003` / `G5 giveback mp=0.05 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.85, PF=1.26, 交易=1251, 回撤%=13.10)
- **失败** `V4_G5_P004` / `G5 giveback mp=0.08 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.64, PF=1.18, 交易=1322, 回撤%=0.00)
- **失败** `V4_G5_P004` / `G5 giveback mp=0.08 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.64, PF=1.18, 交易=1322, 回撤%=12.20)
- **失败** `V4_G5_P018` / `G5 giveback mp=0.08 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.62, PF=1.17, 交易=1280, 回撤%=3.00)
- **失败** `V4_G5_P018` / `G5 giveback mp=0.08 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.62, PF=1.17, 交易=1280, 回撤%=16.03)
- **失败** `V4_G5_P005` / `G5 giveback mp=0.08 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.75, PF=1.21, 交易=1286, 回撤%=5.00)
- **失败** `V4_G5_P005` / `G5 giveback mp=0.08 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.75, PF=1.21, 交易=1286, 回撤%=12.35)
- **失败** `V4_G5_P019` / `G5 giveback mp=0.08 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.72, PF=1.20, 交易=1242, 回撤%=5.00)
- **失败** `V4_G5_P019` / `G5 giveback mp=0.08 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.72, PF=1.20, 交易=1242, 回撤%=17.55)
- **失败** `V4_G5_P006` / `G5 giveback mp=0.08 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.86, PF=1.25, 交易=1248, 回撤%=6.00)
- **失败** `V4_G5_P006` / `G5 giveback mp=0.08 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.86, PF=1.25, 交易=1248, 回撤%=13.46)
- **失败** `V4_G5_P007` / `G5 giveback mp=0.1 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.58, PF=1.16, 交易=1317, 回撤%=6.00)
- **失败** `V4_G5_P007` / `G5 giveback mp=0.1 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.58, PF=1.16, 交易=1317, 回撤%=15.06)
- **失败** `V4_G5_P020` / `G5 giveback mp=0.1 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.14, 交易=1275, 回撤%=8.00)
- **失败** `V4_G5_P020` / `G5 giveback mp=0.1 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.55, PF=1.14, 交易=1275, 回撤%=16.48)
- **失败** `V4_G5_P008` / `G5 giveback mp=0.1 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.69, PF=1.18, 交易=1281, 回撤%=6.00)
- **失败** `V4_G5_P008` / `G5 giveback mp=0.1 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.69, PF=1.18, 交易=1281, 回撤%=12.66)
- **失败** `V4_G5_P021` / `G5 giveback mp=0.1 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.68, PF=1.18, 交易=1235, 回撤%=3.00)
- **失败** `V4_G5_P021` / `G5 giveback mp=0.1 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.68, PF=1.18, 交易=1235, 回撤%=18.03)
- **失败** `V4_G5_P009` / `G5 giveback mp=0.1 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.23, 交易=1243, 回撤%=8.00)
- **失败** `V4_G5_P009` / `G5 giveback mp=0.1 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.23, 交易=1243, 回撤%=13.08)
- **失败** `V4_G5_P010` / `G5 giveback mp=0.15 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.14, 交易=1304, 回撤%=8.00)
- **失败** `V4_G5_P010` / `G5 giveback mp=0.15 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.56, PF=1.14, 交易=1304, 回撤%=19.68)
- **失败** `V4_G5_P022` / `G5 giveback mp=0.15 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.52, PF=1.13, 交易=1246, 回撤%=1.00)
- **失败** `V4_G5_P022` / `G5 giveback mp=0.15 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.52, PF=1.13, 交易=1246, 回撤%=19.11)
- **失败** `V4_G5_P011` / `G5 giveback mp=0.15 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.64, PF=1.16, 交易=1253, 回撤%=8.00)
- **失败** `V4_G5_P011` / `G5 giveback mp=0.15 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.64, PF=1.16, 交易=1253, 回撤%=15.48)
- **失败** `V4_G5_P023` / `G5 giveback mp=0.15 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.58, PF=1.15, 交易=1210, 回撤%=0.00)
- **失败** `V4_G5_P023` / `G5 giveback mp=0.15 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.58, PF=1.15, 交易=1210, 回撤%=17.50)
- **失败** `V4_G5_P012` / `G5 giveback mp=0.15 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.70, PF=1.19, 交易=1214, 回撤%=8.00)
- **失败** `V4_G5_P012` / `G5 giveback mp=0.15 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.70, PF=1.19, 交易=1214, 回撤%=15.18)
- **失败** `V4_G5_P013` / `G5 giveback mp=0.2 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.70, PF=1.18, 交易=1282, 回撤%=6.00)
- **失败** `V4_G5_P013` / `G5 giveback mp=0.2 kr=0.3 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.70, PF=1.18, 交易=1282, 回撤%=14.86)
- **失败** `V4_G5_P024` / `G5 giveback mp=0.2 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.57, PF=1.14, 交易=1221, 回撤%=4.00)
- **失败** `V4_G5_P024` / `G5 giveback mp=0.2 kr=0.5 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.57, PF=1.14, 交易=1221, 回撤%=19.34)
- **失败** `V4_G5_P014` / `G5 giveback mp=0.2 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.69, PF=1.18, 交易=1226, 回撤%=2.00)
- **失败** `V4_G5_P014` / `G5 giveback mp=0.2 kr=0.5 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.69, PF=1.18, 交易=1226, 回撤%=15.92)
- **失败** `V4_G5_P025` / `G5 giveback mp=0.2 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.73, PF=1.20, 交易=1176, 回撤%=0.00)
- **失败** `V4_G5_P025` / `G5 giveback mp=0.2 kr=0.7 stair=False`：Sharpe<0.9；PF<1.3 (Sharpe=0.73, PF=1.20, 交易=1176, 回撤%=18.90)
- **失败** `V4_G5_P015` / `G5 giveback mp=0.2 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.85, PF=1.25, 交易=1183, 回撤%=3.00)
- **失败** `V4_G5_P015` / `G5 giveback mp=0.2 kr=0.7 stair=True`：Sharpe<0.9；PF<1.3 (Sharpe=0.85, PF=1.25, 交易=1183, 回撤%=16.03)

### group `group6_dynamic_dc`

- **失败** `V4_G6_P018` / `G6 dynDC lb=100 s=16 L=30 th=0.7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group7_per_pair_params`

- **失败** `V4_G7_ADA_PG01` / `G7 ADA/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.33, PF=1.34, 交易=334, 回撤%=3.00)
- **失败** `V4_G7_ADA_PG01` / `G7 ADA/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.33, PF=1.34, 交易=334, 回撤%=15.43)
- **失败** `V4_G7_ADA_PG07` / `G7 ADA/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.29, PF=1.32, 交易=311, 回撤%=7.00)
- **失败** `V4_G7_ADA_PG07` / `G7 ADA/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.29, PF=1.32, 交易=311, 回撤%=12.27)
- **失败** `V4_G7_ADA_PG04` / `G7 ADA/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.33, PF=1.39, 交易=301, 回撤%=0.00)
- **失败** `V4_G7_ADA_PG04` / `G7 ADA/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.33, PF=1.39, 交易=301, 回撤%=15.20)
- **失败** `V4_G7_ADA_PG05` / `G7 ADA/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.33, PF=1.42, 交易=283, 回撤%=7.00)
- **失败** `V4_G7_ADA_PG05` / `G7 ADA/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.33, PF=1.42, 交易=283, 回撤%=10.77)
- **失败** `V4_G7_ADA_PG02` / `G7 ADA/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.34, PF=1.44, 交易=277, 回撤%=7.00)
- **失败** `V4_G7_ADA_PG02` / `G7 ADA/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.34, PF=1.44, 交易=277, 回撤%=10.77)
- **失败** `V4_G7_ADA_PG06` / `G7 ADA/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.29, PF=1.44, 交易=235, 回撤%=6.00)
- **失败** `V4_G7_ADA_PG06` / `G7 ADA/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.29, PF=1.44, 交易=235, 回撤%=13.86)
- **失败** `V4_G7_ADA_PG08` / `G7 ADA/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.32, 交易=256, 回撤%=4.00)
- **失败** `V4_G7_ADA_PG08` / `G7 ADA/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.32, 交易=256, 回撤%=13.24)
- **失败** `V4_G7_ADA_PG03` / `G7 ADA/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.36, 交易=234, 回撤%=5.00)
- **失败** `V4_G7_ADA_PG03` / `G7 ADA/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.36, 交易=234, 回撤%=10.75)
- **失败** `V4_G7_BTC_PG01` / `G7 BTC/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.37, PF=1.46, 交易=327, 回撤%=1.00)
- **失败** `V4_G7_BTC_PG01` / `G7 BTC/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.37, PF=1.46, 交易=327, 回撤%=13.81)
- **失败** `V4_G7_BTC_PG07` / `G7 BTC/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.35, PF=1.46, 交易=296, 回撤%=3.00)
- **失败** `V4_G7_BTC_PG07` / `G7 BTC/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.35, PF=1.46, 交易=296, 回撤%=13.83)
- **失败** `V4_G7_BTC_PG04` / `G7 BTC/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.49, 交易=299, 回撤%=9.00)
- **失败** `V4_G7_BTC_PG04` / `G7 BTC/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.49, 交易=299, 回撤%=15.29)
- **失败** `V4_G7_BTC_PG05` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.54, 交易=271, 回撤%=7.00)
- **失败** `V4_G7_BTC_PG05` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.54, 交易=271, 回撤%=13.07)
- **失败** `V4_G7_BTC_PG02` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.34, PF=1.51, 交易=265, 回撤%=0.00)
- **失败** `V4_G7_BTC_PG02` / `G7 BTC/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.34, PF=1.51, 交易=265, 回撤%=13.00)
- **失败** `V4_G7_BTC_PG06` / `G7 BTC/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.26, PF=1.46, 交易=227, 回撤%=2.00)
- **失败** `V4_G7_BTC_PG06` / `G7 BTC/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.26, PF=1.46, 交易=227, 回撤%=9.42)
- **失败** `V4_G7_BTC_PG08` / `G7 BTC/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.31, PF=1.53, 交易=240, 回撤%=4.00)
- **失败** `V4_G7_BTC_PG08` / `G7 BTC/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.31, PF=1.53, 交易=240, 回撤%=11.34)
- **失败** `V4_G7_BTC_PG03` / `G7 BTC/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.31, PF=1.57, 交易=228, 回撤%=2.00)
- **失败** `V4_G7_BTC_PG03` / `G7 BTC/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.31, PF=1.57, 交易=228, 回撤%=10.52)
- **失败** `V4_G7_ETH_PG01` / `G7 ETH/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.37, PF=1.39, 交易=359, 回撤%=1.00)
- **失败** `V4_G7_ETH_PG01` / `G7 ETH/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.37, PF=1.39, 交易=359, 回撤%=11.11)
- **失败** `V4_G7_ETH_PG07` / `G7 ETH/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.28, PF=1.31, 交易=328, 回撤%=7.00)
- **失败** `V4_G7_ETH_PG07` / `G7 ETH/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.28, PF=1.31, 交易=328, 回撤%=12.97)
- **失败** `V4_G7_ETH_PG04` / `G7 ETH/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.40, 交易=334, 回撤%=9.00)
- **失败** `V4_G7_ETH_PG04` / `G7 ETH/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.40, 交易=334, 回撤%=15.29)
- **失败** `V4_G7_ETH_PG05` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.23, PF=1.26, 交易=307, 回撤%=6.00)
- **失败** `V4_G7_ETH_PG05` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.23, PF=1.26, 交易=307, 回撤%=15.96)
- **失败** `V4_G7_ETH_PG02` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.21, PF=1.24, 交易=299, 回撤%=6.00)
- **失败** `V4_G7_ETH_PG02` / `G7 ETH/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.21, PF=1.24, 交易=299, 回撤%=15.26)
- **失败** `V4_G7_ETH_PG06` / `G7 ETH/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.16, PF=1.22, 交易=256, 回撤%=4.00)
- **失败** `V4_G7_ETH_PG06` / `G7 ETH/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.16, PF=1.22, 交易=256, 回撤%=17.14)
- **失败** `V4_G7_ETH_PG08` / `G7 ETH/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.33, 交易=259, 回撤%=9.00)
- **失败** `V4_G7_ETH_PG08` / `G7 ETH/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.33, 交易=259, 回撤%=17.19)
- **失败** `V4_G7_ETH_PG03` / `G7 ETH/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.22, PF=1.32, 交易=242, 回撤%=4.00)
- **失败** `V4_G7_ETH_PG03` / `G7 ETH/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.22, PF=1.32, 交易=242, 回撤%=15.54)
- **失败** `V4_G7_SOL_PG01` / `G7 SOL/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.35, PF=1.31, 交易=357, 回撤%=1.00)
- **失败** `V4_G7_SOL_PG01` / `G7 SOL/USDT:USDT ADX=26 ATR=0.5 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.35, PF=1.31, 交易=357, 回撤%=13.31)
- **失败** `V4_G7_SOL_PG07` / `G7 SOL/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.43, PF=1.47, 交易=313, 回撤%=8.00)
- **失败** `V4_G7_SOL_PG07` / `G7 SOL/USDT:USDT ADX=26 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.43, PF=1.47, 交易=313, 回撤%=13.88)
- **失败** `V4_G7_SOL_PG04` / `G7 SOL/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.37, PF=1.37, 交易=319, 回撤%=5.00)
- **失败** `V4_G7_SOL_PG04` / `G7 SOL/USDT:USDT ADX=28 ATR=0.5 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.37, PF=1.37, 交易=319, 回撤%=11.95)
- **失败** `V4_G7_SOL_PG05` / `G7 SOL/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.44, PF=1.54, 交易=281, 回撤%=2.00)
- **失败** `V4_G7_SOL_PG05` / `G7 SOL/USDT:USDT ADX=28 ATR=0.6 DC=14`：Sharpe<0.9；交易数<800 (Sharpe=0.44, PF=1.54, 交易=281, 回撤%=12.82)
- **失败** `V4_G7_SOL_PG02` / `G7 SOL/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.44, PF=1.57, 交易=275, 回撤%=2.00)
- **失败** `V4_G7_SOL_PG02` / `G7 SOL/USDT:USDT ADX=28 ATR=0.6 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.44, PF=1.57, 交易=275, 回撤%=12.82)
- **失败** `V4_G7_SOL_PG06` / `G7 SOL/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.37, 交易=220, 回撤%=6.00)
- **失败** `V4_G7_SOL_PG06` / `G7 SOL/USDT:USDT ADX=28 ATR=0.8 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.24, PF=1.37, 交易=220, 回撤%=23.66)
- **失败** `V4_G7_SOL_PG08` / `G7 SOL/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.44, PF=1.63, 交易=251, 回撤%=5.00)
- **失败** `V4_G7_SOL_PG08` / `G7 SOL/USDT:USDT ADX=30 ATR=0.6 DC=25`：Sharpe<0.9；交易数<800 (Sharpe=0.44, PF=1.63, 交易=251, 回撤%=10.55)
- **失败** `V4_G7_SOL_PG03` / `G7 SOL/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.58, 交易=221, 回撤%=7.00)
- **失败** `V4_G7_SOL_PG03` / `G7 SOL/USDT:USDT ADX=30 ATR=0.7 DC=20`：Sharpe<0.9；交易数<800 (Sharpe=0.36, PF=1.58, 交易=221, 回撤%=13.37)

### group `group8_stair_grid`

- **失败** `V4_G8_P033` / `G8 stair 24b/-0.06 40b/-0.05`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group9_hour_filter`

- **失败** `V4_G9_P018` / `G9 allow_0_12 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P018` / `G9 allow_0_12 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P017` / `G9 allow_0_12 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P017` / `G9 allow_0_12 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P016` / `G9 allow_12_24 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P016` / `G9 allow_12_24 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P015` / `G9 allow_12_24 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P015` / `G9 allow_12_24 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P014` / `G9 allow_8_20 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P014` / `G9 allow_8_20 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P013` / `G9 allow_8_20 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P013` / `G9 allow_8_20 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P002` / `G9 exclude [0,4) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P002` / `G9 exclude [0,4) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P001` / `G9 exclude [0,4) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P001` / `G9 exclude [0,4) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P008` / `G9 exclude [12,16) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P008` / `G9 exclude [12,16) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P007` / `G9 exclude [12,16) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P007` / `G9 exclude [12,16) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P010` / `G9 exclude [16,20) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P010` / `G9 exclude [16,20) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P009` / `G9 exclude [16,20) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P009` / `G9 exclude [16,20) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P012` / `G9 exclude [20,24) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P012` / `G9 exclude [20,24) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P011` / `G9 exclude [20,24) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P011` / `G9 exclude [20,24) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P004` / `G9 exclude [4,8) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P004` / `G9 exclude [4,8) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P003` / `G9 exclude [4,8) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P003` / `G9 exclude [4,8) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P006` / `G9 exclude [8,12) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P006` / `G9 exclude [8,12) UTC stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P005` / `G9 exclude [8,12) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P005` / `G9 exclude [8,12) UTC stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P020` / `G9 hybrid ex0_4_allow8_20 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P020` / `G9 hybrid ex0_4_allow8_20 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P019` / `G9 hybrid ex0_4_allow8_20 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P019` / `G9 hybrid ex0_4_allow8_20 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P022` / `G9 hybrid ex20_24_allow12_24 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P022` / `G9 hybrid ex20_24_allow12_24 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P021` / `G9 hybrid ex20_24_allow12_24 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P021` / `G9 hybrid ex20_24_allow12_24 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P024` / `G9 hybrid ex8_12_allow0_12 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P024` / `G9 hybrid ex8_12_allow0_12 stair=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P023` / `G9 hybrid ex8_12_allow0_12 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V4_G9_P023` / `G9 hybrid ex8_12_allow0_12 stair=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

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
    "sharpe": 1.15,
    "profit_factor": 1.46,
    "max_drawdown_pct": 13.05,
    "tot_profit_pct": 1302.0,
    "trades": 1115
  }
}
```
