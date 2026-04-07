# V7 三阶段回测分析报告

- 生成路径: `/Users/lin/crypto-quant-trading/user_data/experiment_results/v7_analysis.md`
- 数据根目录: `/Users/lin/crypto-quant-trading`

## 1. 全样本排名（Top 20，按 Sharpe 降序）

基线参考: Sharpe **1.21**, PF **1.5**, 最大回撤 **11.24%**, 总利润 **1398%**, 交易数 **1098**。

| 排名 | strategy | group | name | Sharpe | PF | 利润% | 回撤% | 交易数 | 超越基线(分项) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | V7_G1_P007 | group_g1_volume | G1 vol vp=50 vm=1.0 macd=True | 1.23 | 1.52 | 1482.7 | 11.0 | 1092 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 2 | V7_G1_P001 | group_g1_volume | G1 vol vp=20 vm=1.0 macd=True | 1.22 | 1.51 | 1442.4 | 10.9 | 1095 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 3 | V7_G1_P009 | group_g1_volume | G1 vol vp=50 vm=1.5 macd=True | 1.22 | 1.54 | 1553.9 | 9.4 | 1057 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 4 | V7_G1_P008 | group_g1_volume | G1 vol vp=50 vm=1.0 macd=False | 1.21 | 1.50 | 1492.3 | 11.9 | 1112 | Sharpe:✓ PF:✓ 回撤:× 利润%:✓ 交易数:✓ |
| 5 | V7_G1_P010 | group_g1_volume | G1 vol vp=50 vm=1.5 macd=False | 1.21 | 1.52 | 1568.3 | 9.3 | 1076 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:× |
| 6 | V7_H1_P001 | group_h1_baseline | H1 CryptoV11 baseline | 1.21 | 1.50 | 1406.7 | 11.0 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:✓ 交易数:✓ |
| 7 | V7_G1_P002 | group_g1_volume | G1 vol vp=20 vm=1.0 macd=False | 1.20 | 1.49 | 1471.7 | 11.9 | 1114 | Sharpe:× PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 8 | V7_G1_P004 | group_g1_volume | G1 vol vp=20 vm=1.5 macd=False | 1.19 | 1.51 | 1388.2 | 9.5 | 1073 | Sharpe:× PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 9 | V7_G1_P003 | group_g1_volume | G1 vol vp=20 vm=1.5 macd=True | 1.18 | 1.51 | 1340.8 | 9.6 | 1058 | Sharpe:× PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 10 | V7_G4_P003 | group_g4_keltner | G4 KC p=20 m=2.0 macd=True | 1.17 | 1.27 | 1264.7 | 32.4 | 1713 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 11 | V7_G13_P007 | group_g13_compound_exit | G13 di=False ema=True adx=True bars=8 | 1.16 | 1.47 | 1194.2 | 14.1 | 1102 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 12 | V7_G13_P008 | group_g13_compound_exit | G13 di=False ema=True adx=True bars=16 | 1.16 | 1.47 | 1195.1 | 14.0 | 1102 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 13 | V7_G1_P011 | group_g1_volume | G1 vol vp=50 vm=2.0 macd=True | 1.14 | 1.51 | 1333.4 | 7.6 | 992 | Sharpe:× PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 14 | V7_G1_P012 | group_g1_volume | G1 vol vp=50 vm=2.0 macd=False | 1.12 | 1.50 | 1332.6 | 7.6 | 1006 | Sharpe:× PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 15 | V7_G1_P005 | group_g1_volume | G1 vol vp=20 vm=2.0 macd=True | 1.11 | 1.53 | 1190.0 | 8.7 | 949 | Sharpe:× PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 16 | V7_G1_P006 | group_g1_volume | G1 vol vp=20 vm=2.0 macd=False | 1.11 | 1.53 | 1216.0 | 8.6 | 957 | Sharpe:× PF:✓ 回撤:✓ 利润%:× 交易数:× |
| 17 | V7_G13_P004 | group_g13_compound_exit | G13 di=True ema=True adx=False bars=16 | 1.11 | 1.44 | 1075.2 | 14.7 | 1104 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 18 | V7_G2_P011 | group_g2_rsi | G2 RSI p=21 max=80 macd=True | 1.10 | 1.47 | 1029.6 | 10.5 | 1009 | Sharpe:× PF:× 回撤:✓ 利润%:× 交易数:× |
| 19 | V7_G4_P001 | group_g4_keltner | G4 KC p=20 m=1.5 macd=True | 1.08 | 1.21 | 1106.3 | 32.3 | 1909 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 20 | V7_G4_P002 | group_g4_keltner | G4 KC p=20 m=1.5 macd=False | 1.07 | 1.18 | 1223.7 | 37.6 | 2224 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |

<details><summary>Top20 的 params 摘要（展开）</summary>

| 排名 | params |
| --- | --- |
| 1 | `{"vol_period": 50, "vol_mult": 1.0, "with_macd": true}` |
| 2 | `{"vol_period": 20, "vol_mult": 1.0, "with_macd": true}` |
| 3 | `{"vol_period": 50, "vol_mult": 1.5, "with_macd": true}` |
| 4 | `{"vol_period": 50, "vol_mult": 1.0, "with_macd": false}` |
| 5 | `{"vol_period": 50, "vol_mult": 1.5, "with_macd": false}` |
| 6 | `{"variant": "v11_baseline"}` |
| 7 | `{"vol_period": 20, "vol_mult": 1.0, "with_macd": false}` |
| 8 | `{"vol_period": 20, "vol_mult": 1.5, "with_macd": false}` |
| 9 | `{"vol_period": 20, "vol_mult": 1.5, "with_macd": true}` |
| 10 | `{"kc_period": 20, "kc_mult": 2.0, "with_macd": true}` |
| 11 | `{"need_di": false, "need_ema": true, "need_adx": true, "min_bars": 8}` |
| 12 | `{"need_di": false, "need_ema": true, "need_adx": true, "min_bars": 16}` |
| 13 | `{"vol_period": 50, "vol_mult": 2.0, "with_macd": true}` |
| 14 | `{"vol_period": 50, "vol_mult": 2.0, "with_macd": false}` |
| 15 | `{"vol_period": 20, "vol_mult": 2.0, "with_macd": true}` |
| 16 | `{"vol_period": 20, "vol_mult": 2.0, "with_macd": false}` |
| 17 | `{"need_di": true, "need_ema": true, "need_adx": false, "min_bars": 16}` |
| 18 | `{"rsi_period": 21, "rsi_max": 80, "with_macd": true}` |
| 19 | `{"kc_period": 20, "kc_mult": 1.5, "with_macd": true}` |
| 20 | `{"kc_period": 20, "kc_mult": 1.5, "with_macd": false}` |

</details>

## 2. 分组汇总

| group | 策略数 | 阶段1通过率 | 组均Sharpe | 最优 name | 最优Sharpe | 分年度验证 | Walk-Forward | 邻域std标签 | 结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| group_g10_consecutive | 12 | 0% | 0.00 | G10 consec=2 macd=True | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g11_dyn_timeout | 12 | 0% | 0.00 | G11 loss_bars=32 win_bars=96 th=-0.02 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g12_stoploss | 10 | 0% | 0.00 | G12 SL=-0.06 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g13_compound_exit | 8 | 38% | 0.61 | G13 di=False ema=True adx=True bars=8 | 1.16 | 稳定 (CV=0.42, 6/6年盈利) | 无过拟合 (OOS=2.06) | 平滑 (0.00) | 推荐 |
| group_g14_regime | 8 | 25% | 0.73 | G14 half_lev adx=45 | 0.97 | 可接受 (CV=0.77, 6/6年盈利) | 无过拟合 (OOS=1.78) | 平滑 (0.00) | 有潜力 |
| group_g1_volume | 12 | 100% | 1.18 | G1 vol vp=50 vm=1.0 macd=True | 1.23 | 稳定 (CV=0.40, 6/6年盈利) | 无过拟合 (OOS=1.90) | 平滑 (0.00) | 推荐 |
| group_g2_rsi | 12 | 8% | 0.34 | G2 RSI p=21 max=80 macd=True | 1.10 | 稳定 (CV=0.34, 6/6年盈利) | 无过拟合 (OOS=2.36) | 平滑 (0.00) | 推荐 |
| group_g3_timeframe | 9 | 0% | 0.00 | G3 tf=5m atr=0.4 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g4_keltner | 16 | 0% | 0.47 | G4 KC p=20 m=2.0 macd=True | 1.17 | — | — | 平滑 (0.00) | 放弃 |
| group_g5_dc_fixed | 12 | 0% | 0.00 | G5 DC=10 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g6_pair_weight | 8 | 0% | 0.00 | G6 btc=3 eth=7 sol=5 ada=7 | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g7_ablation | 10 | 0% | 0.00 | G7 no_atr_filter | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g8_macd_th | 12 | 0% | 0.00 | G8 hist_th=0.0 rising=True | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_g9_session | 12 | 0% | 0.00 | G9 sess=asia macd=True | 0.00 | — | — | 平滑 (0.00) | 放弃 |
| group_h1_baseline | 1 | 100% | 1.21 | H1 CryptoV11 baseline | 1.21 | 不稳定 (CV=inf, 4/6年盈利) | — | 平滑 (0.00) | 有潜力 |

> 分年度参考：参考：2020:+85% Sharpe1.72 / 2021:+115% Sharpe1.91 / 2022:+6.94% Sharpe0.21 / 2023:+74% Sharpe1.33 / 2024:+36% Sharpe1.14 / 2025Q1:+46% Sharpe1.07

## 3. 参数邻域稳定性（阶段1，按 group × strategy）

在同一 `strategy`+`group` 内，对所有变体的 Sharpe 计算总体标准差；并按 `name` 字典序相邻检测尖峰（高于邻居最大值超过 0.3）。

| strategy | group | 变体数 | Sharpe std | 稳定性 | 尖峰标记(若有) |
| --- | --- | --- | --- | --- | --- |
| V7_G10_P001 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P002 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P003 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P004 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P005 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P006 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P007 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P008 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P009 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P010 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P011 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G10_P012 | group_g10_consecutive | 1 | 0.00 | 平滑 | — |
| V7_G11_P001 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P002 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P003 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P004 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P005 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P006 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P007 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P008 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P009 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P010 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P011 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G11_P012 | group_g11_dyn_timeout | 1 | 0.00 | 平滑 | — |
| V7_G12_P001 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P002 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P003 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P004 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P005 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P006 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P007 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P008 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P009 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G12_P010 | group_g12_stoploss | 1 | 0.00 | 平滑 | — |
| V7_G13_P001 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G13_P002 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G13_P003 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G13_P004 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G13_P005 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G13_P006 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G13_P007 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G13_P008 | group_g13_compound_exit | 1 | 0.00 | 平滑 | — |
| V7_G14_P001 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G14_P002 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G14_P003 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G14_P004 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G14_P005 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G14_P006 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G14_P007 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G14_P008 | group_g14_regime | 1 | 0.00 | 平滑 | — |
| V7_G1_P001 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P002 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P003 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P004 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P005 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P006 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P007 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P008 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P009 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P010 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P011 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G1_P012 | group_g1_volume | 1 | 0.00 | 平滑 | — |
| V7_G2_P001 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P002 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P003 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P004 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P005 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P006 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P007 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P008 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P009 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P010 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P011 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G2_P012 | group_g2_rsi | 1 | 0.00 | 平滑 | — |
| V7_G3_P001 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P002 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P003 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P004 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P005 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P006 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P007 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P008 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G3_P009 | group_g3_timeframe | 1 | 0.00 | 平滑 | — |
| V7_G4_P001 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P002 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P003 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P004 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P005 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P006 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P007 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P008 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P009 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P010 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P011 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P012 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P013 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P014 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P015 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G4_P016 | group_g4_keltner | 1 | 0.00 | 平滑 | — |
| V7_G5_P001 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P002 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P003 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P004 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P005 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P006 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P007 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P008 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P009 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P010 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P011 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G5_P012 | group_g5_dc_fixed | 1 | 0.00 | 平滑 | — |
| V7_G6_P001 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G6_P002 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G6_P003 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G6_P004 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G6_P005 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G6_P006 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G6_P007 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G6_P008 | group_g6_pair_weight | 1 | 0.00 | 平滑 | — |
| V7_G7_P001 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P002 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P003 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P004 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P005 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P006 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P007 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P008 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P009 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G7_P010 | group_g7_ablation | 1 | 0.00 | 平滑 | — |
| V7_G8_P001 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P002 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P003 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P004 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P005 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P006 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P007 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P008 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P009 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P010 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P011 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G8_P012 | group_g8_macd_th | 1 | 0.00 | 平滑 | — |
| V7_G9_P001 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P002 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P003 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P004 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P005 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P006 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P007 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P008 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P009 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P010 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P011 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_G9_P012 | group_g9_session | 1 | 0.00 | 平滑 | — |
| V7_H1_P001 | group_h1_baseline | 1 | 0.00 | 平滑 | — |

## 4. 分年度一致性（仅阶段1已通过门控的候选）

规则：**稳定** = CV < 0.5 且全年份盈利；**可接受** = CV < 0.8 且盈利年份≥ max(1, 总年数-1)；否则 **不稳定**。

| strategy | group | name | 全样本Sharpe | 年份数 | 盈利年数 | CV | 2022 Sharpe | 标签 | 阶段2通过 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V7_G1_P007 | group_g1_volume | G1 vol vp=50 vm=1.0 macd=True | 1.23 | 6 | 6 | 0.40 | 0.21 | 稳定 | 是 |
| V7_G1_P001 | group_g1_volume | G1 vol vp=20 vm=1.0 macd=True | 1.22 | 6 | 6 | 0.39 | 0.24 | 稳定 | 是 |
| V7_G1_P009 | group_g1_volume | G1 vol vp=50 vm=1.5 macd=True | 1.22 | 6 | 6 | 0.06 | 1.42 | 稳定 | 是 |
| V7_G1_P008 | group_g1_volume | G1 vol vp=50 vm=1.0 macd=False | 1.21 | 6 | 6 | 0.41 | 0.21 | 稳定 | 是 |
| V7_G1_P010 | group_g1_volume | G1 vol vp=50 vm=1.5 macd=False | 1.21 | 6 | 6 | 0.43 | 0.17 | 稳定 | 是 |
| V7_H1_P001 | group_h1_baseline | H1 CryptoV11 baseline | 1.21 | 6 | 4 | inf | 0.21 | 不稳定 | 否 |
| V7_G1_P002 | group_g1_volume | G1 vol vp=20 vm=1.0 macd=False | 1.20 | 6 | 6 | 0.40 | 0.24 | 稳定 | 是 |
| V7_G1_P004 | group_g1_volume | G1 vol vp=20 vm=1.5 macd=False | 1.19 | 6 | 6 | 0.08 | 1.38 | 稳定 | 是 |
| V7_G1_P003 | group_g1_volume | G1 vol vp=20 vm=1.5 macd=True | 1.18 | 6 | 6 | 0.43 | 0.08 | 稳定 | 是 |
| V7_G13_P008 | group_g13_compound_exit | G13 di=False ema=True adx=True bars=16 | 1.16 | 6 | 6 | 0.43 | 0.14 | 稳定 | 是 |
| V7_G13_P007 | group_g13_compound_exit | G13 di=False ema=True adx=True bars=8 | 1.16 | 6 | 6 | 0.42 | 0.14 | 稳定 | 是 |
| V7_G1_P011 | group_g1_volume | G1 vol vp=50 vm=2.0 macd=True | 1.14 | 6 | 6 | 0.48 | 0.12 | 稳定 | 是 |
| V7_G1_P012 | group_g1_volume | G1 vol vp=50 vm=2.0 macd=False | 1.12 | 6 | 6 | 0.53 | 0.10 | 可接受 | 是 |
| V7_G13_P004 | group_g13_compound_exit | G13 di=True ema=True adx=False bars=16 | 1.11 | 6 | 6 | 0.41 | 0.16 | 稳定 | 是 |
| V7_G1_P006 | group_g1_volume | G1 vol vp=20 vm=2.0 macd=False | 1.11 | 6 | 5 | 0.52 | -0.03 | 可接受 | 是 |
| V7_G1_P005 | group_g1_volume | G1 vol vp=20 vm=2.0 macd=True | 1.11 | 6 | 6 | 0.18 | 1.47 | 稳定 | 是 |
| V7_G2_P011 | group_g2_rsi | G2 RSI p=21 max=80 macd=True | 1.10 | 6 | 6 | 0.34 | 0.33 | 稳定 | 是 |
| V7_G14_P006 | group_g14_regime | G14 half_lev adx=45 | 0.97 | 6 | 6 | 0.77 | 0.26 | 可接受 | 是 |
| V7_G14_P004 | group_g14_regime | G14 half_lev adx=40 | 0.94 | 6 | 6 | 0.48 | 0.17 | 稳定 | 是 |

## 5. Walk-Forward 过拟合检测（对阶段2已通过门控的候选）

OOS Ratio = 平均(测试期 Sharpe) / 平均(训练期 Sharpe)；PF Decay = 平均(测试期 PF) / 平均(训练期 PF)。

| strategy | group | name | 均训练Sharpe | 均测试Sharpe | OOS | PF Decay | 过拟合标签 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V7_G1_P001 | group_g1_volume | G1 vol vp=20 vm=1.0 macd=True | 1.12 | 1.49 | 1.33 | 1.12 | 无过拟合 |
| V7_G1_P002 | group_g1_volume | G1 vol vp=20 vm=1.0 macd=False | 1.14 | 1.45 | 1.27 | 1.09 | 无过拟合 |
| V7_G1_P003 | group_g1_volume | G1 vol vp=20 vm=1.5 macd=True | 0.71 | 0.95 | 1.33 | 1.15 | 无过拟合 |
| V7_G1_P004 | group_g1_volume | G1 vol vp=20 vm=1.5 macd=False | 1.11 | 1.48 | 1.34 | 1.13 | 无过拟合 |
| V7_G1_P005 | group_g1_volume | G1 vol vp=20 vm=2.0 macd=True | 0.29 | 1.44 | 5.02 | 3.70 | 无过拟合 |
| V7_G1_P006 | group_g1_volume | G1 vol vp=20 vm=2.0 macd=False | 0.69 | 1.47 | 2.12 | 1.73 | 无过拟合 |
| V7_G1_P007 | group_g1_volume | G1 vol vp=50 vm=1.0 macd=True | 0.80 | 1.52 | 1.90 | 1.63 | 无过拟合 |
| V7_G1_P008 | group_g1_volume | G1 vol vp=50 vm=1.0 macd=False | 1.15 | 1.48 | 1.28 | 1.10 | 无过拟合 |
| V7_G1_P009 | group_g1_volume | G1 vol vp=50 vm=1.5 macd=True | 0.75 | 0.93 | 1.25 | 1.12 | 无过拟合 |
| V7_G1_P010 | group_g1_volume | G1 vol vp=50 vm=1.5 macd=False | 1.16 | 1.45 | 1.25 | 1.09 | 无过拟合 |
| V7_G1_P011 | group_g1_volume | G1 vol vp=50 vm=2.0 macd=True | 1.09 | 0.88 | 0.81 | 0.69 | 无过拟合 |
| V7_G1_P012 | group_g1_volume | G1 vol vp=50 vm=2.0 macd=False | 0.66 | 0.24 | 0.36 | 0.46 | 严重 |
| V7_G2_P011 | group_g2_rsi | G2 RSI p=21 max=80 macd=True | 0.38 | 0.90 | 2.36 | 2.15 | 无过拟合 |
| V7_G13_P004 | group_g13_compound_exit | G13 di=True ema=True adx=False bars=16 | 1.06 | 1.36 | 1.28 | 1.09 | 无过拟合 |
| V7_G13_P007 | group_g13_compound_exit | G13 di=False ema=True adx=True bars=8 | 0.69 | 1.43 | 2.06 | 1.71 | 无过拟合 |
| V7_G13_P008 | group_g13_compound_exit | G13 di=False ema=True adx=True bars=16 | 1.08 | 1.43 | 1.33 | 1.11 | 无过拟合 |
| V7_G14_P004 | group_g14_regime | G14 half_lev adx=40 | 0.76 | 0.35 | 0.46 | 0.34 | 严重 |
| V7_G14_P006 | group_g14_regime | G14 half_lev adx=45 | 0.54 | 0.96 | 1.78 | 1.59 | 无过拟合 |

## 6. 最终推荐（综合三阶段）

判定摘要：
- **阶段1**：Sharpe≥0.9、PF≥1.3、交易≥800、回撤≤25.0%。
- **阶段2**：分年度标签为「稳定」或「可接受」（见第4节）。
- **阶段3**：存在 WF 行且 OOS≥0.5 且平均测试 Sharpe>0；**强烈推荐** 另要求 OOS>0.8 且组内邻域 Sharpe 标准差 < 0.1（平滑）。

### 强烈推荐

- **强烈推荐** `V7_G1_P001` / `group_g1_volume` / `G1 vol vp=20 vm=1.0 macd=True`：三阶段通过，Sharpe>1.21，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V7_G1_P007` / `group_g1_volume` / `G1 vol vp=50 vm=1.0 macd=True`：三阶段通过，Sharpe>1.21，OOS>0.8，邻域平滑(std=0.00)
- **强烈推荐** `V7_G1_P009` / `group_g1_volume` / `G1 vol vp=50 vm=1.5 macd=True`：三阶段通过，Sharpe>1.21，OOS>0.8，邻域平滑(std=0.00)

### 推荐

- **推荐** `V7_G1_P002` / `group_g1_volume` / `G1 vol vp=20 vm=1.0 macd=False`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V7_G1_P003` / `group_g1_volume` / `G1 vol vp=20 vm=1.5 macd=True`：三阶段通过且 Sharpe>1.0（OOS=1.33）
- **推荐** `V7_G1_P004` / `group_g1_volume` / `G1 vol vp=20 vm=1.5 macd=False`：三阶段通过且 Sharpe>1.0（OOS=1.34）
- **推荐** `V7_G1_P005` / `group_g1_volume` / `G1 vol vp=20 vm=2.0 macd=True`：三阶段通过且 Sharpe>1.0（OOS=5.02）
- **推荐** `V7_G1_P006` / `group_g1_volume` / `G1 vol vp=20 vm=2.0 macd=False`：三阶段通过且 Sharpe>1.0（OOS=2.12）
- **推荐** `V7_G1_P008` / `group_g1_volume` / `G1 vol vp=50 vm=1.0 macd=False`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V7_G1_P010` / `group_g1_volume` / `G1 vol vp=50 vm=1.5 macd=False`：三阶段通过且 Sharpe>1.0（OOS=1.25）
- **推荐** `V7_G1_P011` / `group_g1_volume` / `G1 vol vp=50 vm=2.0 macd=True`：三阶段通过且 Sharpe>1.0（OOS=0.81）
- **推荐** `V7_G2_P011` / `group_g2_rsi` / `G2 RSI p=21 max=80 macd=True`：三阶段通过且 Sharpe>1.0（OOS=2.36）
- **推荐** `V7_G13_P004` / `group_g13_compound_exit` / `G13 di=True ema=True adx=False bars=16`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V7_G13_P007` / `group_g13_compound_exit` / `G13 di=False ema=True adx=True bars=8`：三阶段通过且 Sharpe>1.0（OOS=2.06）
- **推荐** `V7_G13_P008` / `group_g13_compound_exit` / `G13 di=False ema=True adx=True bars=16`：三阶段通过且 Sharpe>1.0（OOS=1.33）

### 观察名单

- **观察** `V7_G1_P012` / `group_g1_volume` / `G1 vol vp=50 vm=2.0 macd=False`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=0.36）
- **观察** `V7_G14_P004` / `group_g14_regime` / `G14 half_lev adx=40`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=0.46）
- **观察** `V7_G14_P006` / `group_g14_regime` / `G14 half_lev adx=45`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛

### 放弃/未过关

- **放弃** `V7_G2_P001` / `group_g2_rsi` / `G2 RSI p=14 max=70 macd=True`：未通过阶段1
- **放弃** `V7_G2_P002` / `group_g2_rsi` / `G2 RSI p=14 max=70 macd=False`：未通过阶段1
- **放弃** `V7_G2_P003` / `group_g2_rsi` / `G2 RSI p=14 max=75 macd=True`：未通过阶段1
- **放弃** `V7_G2_P004` / `group_g2_rsi` / `G2 RSI p=14 max=75 macd=False`：未通过阶段1
- **放弃** `V7_G2_P005` / `group_g2_rsi` / `G2 RSI p=14 max=80 macd=True`：未通过阶段1
- **放弃** `V7_G2_P006` / `group_g2_rsi` / `G2 RSI p=14 max=80 macd=False`：未通过阶段1
- **放弃** `V7_G2_P007` / `group_g2_rsi` / `G2 RSI p=21 max=70 macd=True`：未通过阶段1
- **放弃** `V7_G2_P008` / `group_g2_rsi` / `G2 RSI p=21 max=70 macd=False`：未通过阶段1
- **放弃** `V7_G2_P009` / `group_g2_rsi` / `G2 RSI p=21 max=75 macd=True`：未通过阶段1
- **放弃** `V7_G2_P010` / `group_g2_rsi` / `G2 RSI p=21 max=75 macd=False`：未通过阶段1
- **放弃** `V7_G2_P012` / `group_g2_rsi` / `G2 RSI p=21 max=80 macd=False`：未通过阶段1
- **放弃** `V7_G3_P001` / `group_g3_timeframe` / `G3 tf=5m atr=0.4`：未通过阶段1
- **放弃** `V7_G3_P002` / `group_g3_timeframe` / `G3 tf=5m atr=0.6`：未通过阶段1
- **放弃** `V7_G3_P003` / `group_g3_timeframe` / `G3 tf=5m atr=0.8`：未通过阶段1
- **放弃** `V7_G3_P004` / `group_g3_timeframe` / `G3 tf=30m atr=0.4`：未通过阶段1
- **放弃** `V7_G3_P005` / `group_g3_timeframe` / `G3 tf=30m atr=0.6`：未通过阶段1
- **放弃** `V7_G3_P006` / `group_g3_timeframe` / `G3 tf=30m atr=0.8`：未通过阶段1
- **放弃** `V7_G3_P007` / `group_g3_timeframe` / `G3 tf=1h atr=0.4`：未通过阶段1
- **放弃** `V7_G3_P008` / `group_g3_timeframe` / `G3 tf=1h atr=0.6`：未通过阶段1
- **放弃** `V7_G3_P009` / `group_g3_timeframe` / `G3 tf=1h atr=0.8`：未通过阶段1
- **放弃** `V7_G4_P001` / `group_g4_keltner` / `G4 KC p=20 m=1.5 macd=True`：未通过阶段1
- **放弃** `V7_G4_P002` / `group_g4_keltner` / `G4 KC p=20 m=1.5 macd=False`：未通过阶段1
- **放弃** `V7_G4_P003` / `group_g4_keltner` / `G4 KC p=20 m=2.0 macd=True`：未通过阶段1
- **放弃** `V7_G4_P004` / `group_g4_keltner` / `G4 KC p=20 m=2.0 macd=False`：未通过阶段1
- **放弃** `V7_G4_P005` / `group_g4_keltner` / `G4 KC p=20 m=2.5 macd=True`：未通过阶段1
- **放弃** `V7_G4_P006` / `group_g4_keltner` / `G4 KC p=20 m=2.5 macd=False`：未通过阶段1
- **放弃** `V7_G4_P007` / `group_g4_keltner` / `G4 KC p=30 m=1.5 macd=True`：未通过阶段1
- **放弃** `V7_G4_P008` / `group_g4_keltner` / `G4 KC p=30 m=1.5 macd=False`：未通过阶段1
- **放弃** `V7_G4_P009` / `group_g4_keltner` / `G4 KC p=30 m=2.0 macd=True`：未通过阶段1
- **放弃** `V7_G4_P010` / `group_g4_keltner` / `G4 KC p=30 m=2.0 macd=False`：未通过阶段1
- **放弃** `V7_G4_P011` / `group_g4_keltner` / `G4 KC p=30 m=2.5 macd=True`：未通过阶段1
- **放弃** `V7_G4_P012` / `group_g4_keltner` / `G4 KC p=30 m=2.5 macd=False`：未通过阶段1
- **放弃** `V7_G4_P013` / `group_g4_keltner` / `G4 KC p=40 m=1.5 macd=True`：未通过阶段1
- **放弃** `V7_G4_P014` / `group_g4_keltner` / `G4 KC p=40 m=1.5 macd=False`：未通过阶段1
- **放弃** `V7_G4_P015` / `group_g4_keltner` / `G4 KC p=40 m=2.0 macd=True`：未通过阶段1
- **放弃** `V7_G4_P016` / `group_g4_keltner` / `G4 KC p=40 m=2.0 macd=False`：未通过阶段1
- **放弃** `V7_G5_P001` / `group_g5_dc_fixed` / `G5 DC=10`：未通过阶段1
- **放弃** `V7_G5_P002` / `group_g5_dc_fixed` / `G5 DC=12`：未通过阶段1
- **放弃** `V7_G5_P003` / `group_g5_dc_fixed` / `G5 DC=14`：未通过阶段1
- **放弃** `V7_G5_P004` / `group_g5_dc_fixed` / `G5 DC=18`：未通过阶段1
- **放弃** `V7_G5_P005` / `group_g5_dc_fixed` / `G5 DC=20`：未通过阶段1
- **放弃** `V7_G5_P006` / `group_g5_dc_fixed` / `G5 DC=25`：未通过阶段1
- **放弃** `V7_G5_P007` / `group_g5_dc_fixed` / `G5 DC=30`：未通过阶段1
- **放弃** `V7_G5_P008` / `group_g5_dc_fixed` / `G5 DC=35`：未通过阶段1
- **放弃** `V7_G5_P009` / `group_g5_dc_fixed` / `G5 DC=40`：未通过阶段1
- **放弃** `V7_G5_P010` / `group_g5_dc_fixed` / `G5 DC=50`：未通过阶段1
- **放弃** `V7_G5_P011` / `group_g5_dc_fixed` / `G5 DC=60`：未通过阶段1
- **放弃** `V7_G5_P012` / `group_g5_dc_fixed` / `G5 DC=80`：未通过阶段1
- **放弃** `V7_G6_P001` / `group_g6_pair_weight` / `G6 btc=3 eth=7 sol=5 ada=7`：未通过阶段1
- **放弃** `V7_G6_P002` / `group_g6_pair_weight` / `G6 btc=5 eth=7 sol=3 ada=7`：未通过阶段1
- **放弃** `V7_G6_P003` / `group_g6_pair_weight` / `G6 btc=3 eth=5 sol=5 ada=5`：未通过阶段1
- **放弃** `V7_G6_P004` / `group_g6_pair_weight` / `G6 btc=7 eth=7 sol=3 ada=5`：未通过阶段1
- **放弃** `V7_G6_P005` / `group_g6_pair_weight` / `G6 btc=5 eth=5 sol=7 ada=7`：未通过阶段1
- **放弃** `V7_G6_P006` / `group_g6_pair_weight` / `G6 btc=3 eth=7 sol=7 ada=5`：未通过阶段1
- **放弃** `V7_G6_P007` / `group_g6_pair_weight` / `G6 btc=5 eth=3 sol=7 ada=7`：未通过阶段1
- **放弃** `V7_G6_P008` / `group_g6_pair_weight` / `G6 btc=7 eth=5 sol=5 ada=3`：未通过阶段1
- **放弃** `V7_G7_P001` / `group_g7_ablation` / `G7 no_atr_filter`：未通过阶段1
- **放弃** `V7_G7_P002` / `group_g7_ablation` / `G7 no_adx_rising`：未通过阶段1
- **放弃** `V7_G7_P003` / `group_g7_ablation` / `G7 no_di_cross`：未通过阶段1
- **放弃** `V7_G7_P004` / `group_g7_ablation` / `G7 no_ema_align`：未通过阶段1
- **放弃** `V7_G7_P005` / `group_g7_ablation` / `G7 no_ema200`：未通过阶段1
- **放弃** `V7_G7_P006` / `group_g7_ablation` / `G7 no_4h_ema`：未通过阶段1
- **放弃** `V7_G7_P007` / `group_g7_ablation` / `G7 no_macd`：未通过阶段1
- **放弃** `V7_G7_P008` / `group_g7_ablation` / `G7 no_macd_rising`：未通过阶段1
- **放弃** `V7_G7_P009` / `group_g7_ablation` / `G7 minimal_dc_adx`：未通过阶段1
- **放弃** `V7_G7_P010` / `group_g7_ablation` / `G7 minimal_dc_only`：未通过阶段1
- **放弃** `V7_G8_P001` / `group_g8_macd_th` / `G8 hist_th=0.0 rising=True`：未通过阶段1
- **放弃** `V7_G8_P002` / `group_g8_macd_th` / `G8 hist_th=0.0 rising=False`：未通过阶段1
- **放弃** `V7_G8_P003` / `group_g8_macd_th` / `G8 hist_th=0.001 rising=True`：未通过阶段1
- **放弃** `V7_G8_P004` / `group_g8_macd_th` / `G8 hist_th=0.001 rising=False`：未通过阶段1
- **放弃** `V7_G8_P005` / `group_g8_macd_th` / `G8 hist_th=0.005 rising=True`：未通过阶段1
- **放弃** `V7_G8_P006` / `group_g8_macd_th` / `G8 hist_th=0.005 rising=False`：未通过阶段1
- **放弃** `V7_G8_P007` / `group_g8_macd_th` / `G8 hist_th=0.01 rising=True`：未通过阶段1
- **放弃** `V7_G8_P008` / `group_g8_macd_th` / `G8 hist_th=0.01 rising=False`：未通过阶段1
- **放弃** `V7_G8_P009` / `group_g8_macd_th` / `G8 hist_th=0.02 rising=True`：未通过阶段1
- **放弃** `V7_G8_P010` / `group_g8_macd_th` / `G8 hist_th=0.02 rising=False`：未通过阶段1
- **放弃** `V7_G8_P011` / `group_g8_macd_th` / `G8 hist_th=0.05 rising=True`：未通过阶段1
- **放弃** `V7_G8_P012` / `group_g8_macd_th` / `G8 hist_th=0.05 rising=False`：未通过阶段1
- **放弃** `V7_G9_P001` / `group_g9_session` / `G9 sess=asia macd=True`：未通过阶段1
- **放弃** `V7_G9_P002` / `group_g9_session` / `G9 sess=asia macd=False`：未通过阶段1
- **放弃** `V7_G9_P003` / `group_g9_session` / `G9 sess=europe macd=True`：未通过阶段1
- **放弃** `V7_G9_P004` / `group_g9_session` / `G9 sess=europe macd=False`：未通过阶段1
- **放弃** `V7_G9_P005` / `group_g9_session` / `G9 sess=us macd=True`：未通过阶段1
- **放弃** `V7_G9_P006` / `group_g9_session` / `G9 sess=us macd=False`：未通过阶段1
- **放弃** `V7_G9_P007` / `group_g9_session` / `G9 sess=no_asia macd=True`：未通过阶段1
- **放弃** `V7_G9_P008` / `group_g9_session` / `G9 sess=no_asia macd=False`：未通过阶段1
- **放弃** `V7_G9_P009` / `group_g9_session` / `G9 sess=no_low macd=True`：未通过阶段1
- **放弃** `V7_G9_P010` / `group_g9_session` / `G9 sess=no_low macd=False`：未通过阶段1
- **放弃** `V7_G9_P011` / `group_g9_session` / `G9 sess=overlap macd=True`：未通过阶段1
- **放弃** `V7_G9_P012` / `group_g9_session` / `G9 sess=overlap macd=False`：未通过阶段1
- **放弃** `V7_G10_P001` / `group_g10_consecutive` / `G10 consec=2 macd=True`：未通过阶段1
- **放弃** `V7_G10_P002` / `group_g10_consecutive` / `G10 consec=2 macd=False`：未通过阶段1
- **放弃** `V7_G10_P003` / `group_g10_consecutive` / `G10 consec=3 macd=True`：未通过阶段1
- **放弃** `V7_G10_P004` / `group_g10_consecutive` / `G10 consec=3 macd=False`：未通过阶段1
- **放弃** `V7_G10_P005` / `group_g10_consecutive` / `G10 consec=4 macd=True`：未通过阶段1
- **放弃** `V7_G10_P006` / `group_g10_consecutive` / `G10 consec=4 macd=False`：未通过阶段1
- **放弃** `V7_G10_P007` / `group_g10_consecutive` / `G10 consec=5 macd=True`：未通过阶段1
- **放弃** `V7_G10_P008` / `group_g10_consecutive` / `G10 consec=5 macd=False`：未通过阶段1
- **放弃** `V7_G10_P009` / `group_g10_consecutive` / `G10 consec=6 macd=True`：未通过阶段1
- **放弃** `V7_G10_P010` / `group_g10_consecutive` / `G10 consec=6 macd=False`：未通过阶段1
- **放弃** `V7_G10_P011` / `group_g10_consecutive` / `G10 consec=8 macd=True`：未通过阶段1
- **放弃** `V7_G10_P012` / `group_g10_consecutive` / `G10 consec=8 macd=False`：未通过阶段1
- **放弃** `V7_G11_P001` / `group_g11_dyn_timeout` / `G11 loss_bars=32 win_bars=96 th=-0.02`：未通过阶段1
- **放弃** `V7_G11_P002` / `group_g11_dyn_timeout` / `G11 loss_bars=32 win_bars=96 th=-0.03`：未通过阶段1
- **放弃** `V7_G11_P003` / `group_g11_dyn_timeout` / `G11 loss_bars=40 win_bars=80 th=-0.02`：未通过阶段1
- **放弃** `V7_G11_P004` / `group_g11_dyn_timeout` / `G11 loss_bars=40 win_bars=80 th=-0.03`：未通过阶段1
- **放弃** `V7_G11_P005` / `group_g11_dyn_timeout` / `G11 loss_bars=48 win_bars=128 th=-0.02`：未通过阶段1
- **放弃** `V7_G11_P006` / `group_g11_dyn_timeout` / `G11 loss_bars=48 win_bars=128 th=-0.03`：未通过阶段1
- **放弃** `V7_G11_P007` / `group_g11_dyn_timeout` / `G11 loss_bars=24 win_bars=64 th=-0.02`：未通过阶段1
- **放弃** `V7_G11_P008` / `group_g11_dyn_timeout` / `G11 loss_bars=24 win_bars=64 th=-0.03`：未通过阶段1
- **放弃** `V7_G11_P009` / `group_g11_dyn_timeout` / `G11 loss_bars=32 win_bars=128 th=-0.02`：未通过阶段1
- **放弃** `V7_G11_P010` / `group_g11_dyn_timeout` / `G11 loss_bars=32 win_bars=128 th=-0.03`：未通过阶段1
- **放弃** `V7_G11_P011` / `group_g11_dyn_timeout` / `G11 loss_bars=48 win_bars=96 th=-0.02`：未通过阶段1
- **放弃** `V7_G11_P012` / `group_g11_dyn_timeout` / `G11 loss_bars=48 win_bars=96 th=-0.03`：未通过阶段1
- **放弃** `V7_G12_P001` / `group_g12_stoploss` / `G12 SL=-0.06`：未通过阶段1
- **放弃** `V7_G12_P002` / `group_g12_stoploss` / `G12 SL=-0.07`：未通过阶段1
- **放弃** `V7_G12_P003` / `group_g12_stoploss` / `G12 SL=-0.08`：未通过阶段1
- **放弃** `V7_G12_P004` / `group_g12_stoploss` / `G12 SL=-0.09`：未通过阶段1
- **放弃** `V7_G12_P005` / `group_g12_stoploss` / `G12 SL=-0.1`：未通过阶段1
- **放弃** `V7_G12_P006` / `group_g12_stoploss` / `G12 SL=-0.11`：未通过阶段1
- **放弃** `V7_G12_P007` / `group_g12_stoploss` / `G12 SL=-0.12`：未通过阶段1
- **放弃** `V7_G12_P008` / `group_g12_stoploss` / `G12 SL=-0.13`：未通过阶段1
- **放弃** `V7_G12_P009` / `group_g12_stoploss` / `G12 SL=-0.14`：未通过阶段1
- **放弃** `V7_G12_P010` / `group_g12_stoploss` / `G12 SL=-0.15`：未通过阶段1
- **放弃** `V7_G13_P001` / `group_g13_compound_exit` / `G13 di=True ema=True adx=True bars=8`：未通过阶段1
- **放弃** `V7_G13_P002` / `group_g13_compound_exit` / `G13 di=True ema=True adx=True bars=16`：未通过阶段1
- **放弃** `V7_G13_P003` / `group_g13_compound_exit` / `G13 di=True ema=True adx=False bars=8`：未通过阶段1
- **放弃** `V7_G13_P005` / `group_g13_compound_exit` / `G13 di=True ema=False adx=True bars=8`：未通过阶段1
- **放弃** `V7_G13_P006` / `group_g13_compound_exit` / `G13 di=True ema=False adx=True bars=16`：未通过阶段1
- **放弃** `V7_G14_P001` / `group_g14_regime` / `G14 strong_only adx>35`：未通过阶段1
- **放弃** `V7_G14_P002` / `group_g14_regime` / `G14 half_lev adx=35`：未通过阶段1
- **放弃** `V7_G14_P003` / `group_g14_regime` / `G14 strong_only adx>40`：未通过阶段1
- **放弃** `V7_G14_P005` / `group_g14_regime` / `G14 strong_only adx>45`：未通过阶段1
- **放弃** `V7_G14_P007` / `group_g14_regime` / `G14 adx_slope bars=5`：未通过阶段1
- **放弃** `V7_G14_P008` / `group_g14_regime` / `G14 adx_slope bars=10`：未通过阶段1
- **放弃** `V7_H1_P001` / `group_h1_baseline` / `H1 CryptoV11 baseline`：阶段2「不稳定」

## 7. 失败方向总结（按 group，避免重复踩坑）

### group `group_g10_consecutive`

- **失败** `V7_G10_P002` / `G10 consec=2 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P001` / `G10 consec=2 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P004` / `G10 consec=3 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P003` / `G10 consec=3 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P006` / `G10 consec=4 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P005` / `G10 consec=4 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P008` / `G10 consec=5 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P007` / `G10 consec=5 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P010` / `G10 consec=6 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P009` / `G10 consec=6 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P012` / `G10 consec=8 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G10_P011` / `G10 consec=8 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g11_dyn_timeout`

- **失败** `V7_G11_P007` / `G11 loss_bars=24 win_bars=64 th=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P008` / `G11 loss_bars=24 win_bars=64 th=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P009` / `G11 loss_bars=32 win_bars=128 th=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P010` / `G11 loss_bars=32 win_bars=128 th=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P001` / `G11 loss_bars=32 win_bars=96 th=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P002` / `G11 loss_bars=32 win_bars=96 th=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P003` / `G11 loss_bars=40 win_bars=80 th=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P004` / `G11 loss_bars=40 win_bars=80 th=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P005` / `G11 loss_bars=48 win_bars=128 th=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P006` / `G11 loss_bars=48 win_bars=128 th=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P011` / `G11 loss_bars=48 win_bars=96 th=-0.02`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G11_P012` / `G11 loss_bars=48 win_bars=96 th=-0.03`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g12_stoploss`

- **失败** `V7_G12_P001` / `G12 SL=-0.06`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P002` / `G12 SL=-0.07`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P003` / `G12 SL=-0.08`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P004` / `G12 SL=-0.09`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P005` / `G12 SL=-0.1`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P006` / `G12 SL=-0.11`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P007` / `G12 SL=-0.12`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P008` / `G12 SL=-0.13`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P009` / `G12 SL=-0.14`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G12_P010` / `G12 SL=-0.15`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g13_compound_exit`

- **失败** `V7_G13_P006` / `G13 di=True ema=False adx=True bars=16`：Sharpe<0.9；PF<1.3 (Sharpe=0.74, PF=1.25, 交易=1155, 回撤%=14.71)
- **失败** `V7_G13_P005` / `G13 di=True ema=False adx=True bars=8`：Sharpe<0.9；PF<1.3 (Sharpe=0.75, PF=1.26, 交易=1157, 回撤%=14.28)
- **失败** `V7_G13_P003` / `G13 di=True ema=True adx=False bars=8`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G13_P002` / `G13 di=True ema=True adx=True bars=16`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G13_P001` / `G13 di=True ema=True adx=True bars=8`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g14_regime`

- **失败** `V7_G14_P008` / `G14 adx_slope bars=10`：Sharpe<0.9 (Sharpe=0.84, PF=1.41, 交易=821, 回撤%=14.02)
- **失败** `V7_G14_P007` / `G14 adx_slope bars=5`：Sharpe<0.9 (Sharpe=0.82, PF=1.34, 交易=923, 回撤%=16.77)
- **失败** `V7_G14_P002` / `G14 half_lev adx=35`：Sharpe<0.9 (Sharpe=0.83, PF=1.30, 交易=1066, 回撤%=13.74)
- **失败** `V7_G14_P001` / `G14 strong_only adx>35`：Sharpe<0.9；交易数<800 (Sharpe=0.64, PF=1.35, 交易=710, 回撤%=13.73)
- **失败** `V7_G14_P003` / `G14 strong_only adx>40`：Sharpe<0.9；交易数<800 (Sharpe=0.45, PF=1.34, 交易=482, 回撤%=14.69)
- **失败** `V7_G14_P005` / `G14 strong_only adx>45`：Sharpe<0.9；交易数<800 (Sharpe=0.35, PF=1.44, 交易=291, 回撤%=11.57)

### group `group_g2_rsi`

- **失败** `V7_G2_P002` / `G2 RSI p=14 max=70 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.02, PF=1.04, 交易=154, 回撤%=13.54)
- **失败** `V7_G2_P001` / `G2 RSI p=14 max=70 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.04, PF=1.09, 交易=148, 回撤%=11.09)
- **失败** `V7_G2_P004` / `G2 RSI p=14 max=75 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G2_P003` / `G2 RSI p=14 max=75 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.27, PF=1.18, 交易=510, 回撤%=16.85)
- **失败** `V7_G2_P006` / `G2 RSI p=14 max=80 macd=False`：Sharpe<0.9 (Sharpe=0.84, PF=1.37, 交易=881, 回撤%=17.36)
- **失败** `V7_G2_P005` / `G2 RSI p=14 max=80 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G2_P008` / `G2 RSI p=21 max=70 macd=False`：Sharpe<0.9；PF<1.3；交易数<800；回撤>25.0% (Sharpe=0.07, PF=1.05, 交易=471, 回撤%=27.01)
- **失败** `V7_G2_P007` / `G2 RSI p=21 max=70 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.11, PF=1.07, 交易=461, 回撤%=22.66)
- **失败** `V7_G2_P010` / `G2 RSI p=21 max=75 macd=False`：Sharpe<0.9 (Sharpe=0.79, PF=1.35, 交易=860, 回撤%=12.16)
- **失败** `V7_G2_P009` / `G2 RSI p=21 max=75 macd=True`：Sharpe<0.9 (Sharpe=0.78, PF=1.36, 交易=839, 回撤%=11.24)
- **失败** `V7_G2_P012` / `G2 RSI p=21 max=80 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g3_timeframe`

- **失败** `V7_G3_P007` / `G3 tf=1h atr=0.4`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P008` / `G3 tf=1h atr=0.6`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P009` / `G3 tf=1h atr=0.8`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P004` / `G3 tf=30m atr=0.4`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P005` / `G3 tf=30m atr=0.6`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P006` / `G3 tf=30m atr=0.8`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P001` / `G3 tf=5m atr=0.4`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P002` / `G3 tf=5m atr=0.6`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G3_P003` / `G3 tf=5m atr=0.8`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g4_keltner`

- **失败** `V7_G4_P002` / `G4 KC p=20 m=1.5 macd=False`：PF<1.3；回撤>25.0% (Sharpe=1.07, PF=1.18, 交易=2224, 回撤%=37.63)
- **失败** `V7_G4_P001` / `G4 KC p=20 m=1.5 macd=True`：PF<1.3；回撤>25.0% (Sharpe=1.08, PF=1.21, 交易=1909, 回撤%=32.31)
- **失败** `V7_G4_P004` / `G4 KC p=20 m=2.0 macd=False`：PF<1.3；回撤>25.0% (Sharpe=1.04, PF=1.21, 交易=1930, 回撤%=37.99)
- **失败** `V7_G4_P003` / `G4 KC p=20 m=2.0 macd=True`：PF<1.3；回撤>25.0% (Sharpe=1.17, PF=1.27, 交易=1713, 回撤%=32.40)
- **失败** `V7_G4_P006` / `G4 KC p=20 m=2.5 macd=False`：PF<1.3；回撤>25.0% (Sharpe=1.02, PF=1.24, 交易=1597, 回撤%=29.20)
- **失败** `V7_G4_P005` / `G4 KC p=20 m=2.5 macd=True`：PF<1.3；回撤>25.0% (Sharpe=1.03, PF=1.27, 交易=1471, 回撤%=28.35)
- **失败** `V7_G4_P008` / `G4 KC p=30 m=1.5 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P007` / `G4 KC p=30 m=1.5 macd=True`：PF<1.3；回撤>25.0% (Sharpe=1.03, PF=1.20, 交易=1967, 回撤%=27.20)
- **失败** `V7_G4_P010` / `G4 KC p=30 m=2.0 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P009` / `G4 KC p=30 m=2.0 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P012` / `G4 KC p=30 m=2.5 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P011` / `G4 KC p=30 m=2.5 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P014` / `G4 KC p=40 m=1.5 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P013` / `G4 KC p=40 m=1.5 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P016` / `G4 KC p=40 m=2.0 macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G4_P015` / `G4 KC p=40 m=2.0 macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g5_dc_fixed`

- **失败** `V7_G5_P001` / `G5 DC=10`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P002` / `G5 DC=12`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P003` / `G5 DC=14`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P004` / `G5 DC=18`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P005` / `G5 DC=20`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P006` / `G5 DC=25`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P007` / `G5 DC=30`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P008` / `G5 DC=35`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P009` / `G5 DC=40`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P010` / `G5 DC=50`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P011` / `G5 DC=60`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G5_P012` / `G5 DC=80`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g6_pair_weight`

- **失败** `V7_G6_P003` / `G6 btc=3 eth=5 sol=5 ada=5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G6_P001` / `G6 btc=3 eth=7 sol=5 ada=7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G6_P006` / `G6 btc=3 eth=7 sol=7 ada=5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G6_P007` / `G6 btc=5 eth=3 sol=7 ada=7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G6_P005` / `G6 btc=5 eth=5 sol=7 ada=7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G6_P002` / `G6 btc=5 eth=7 sol=3 ada=7`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G6_P008` / `G6 btc=7 eth=5 sol=5 ada=3`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G6_P004` / `G6 btc=7 eth=7 sol=3 ada=5`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g7_ablation`

- **失败** `V7_G7_P009` / `G7 minimal_dc_adx`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P010` / `G7 minimal_dc_only`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P006` / `G7 no_4h_ema`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P002` / `G7 no_adx_rising`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P001` / `G7 no_atr_filter`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P003` / `G7 no_di_cross`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P005` / `G7 no_ema200`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P004` / `G7 no_ema_align`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P007` / `G7 no_macd`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G7_P008` / `G7 no_macd_rising`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g8_macd_th`

- **失败** `V7_G8_P002` / `G8 hist_th=0.0 rising=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P001` / `G8 hist_th=0.0 rising=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P004` / `G8 hist_th=0.001 rising=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P003` / `G8 hist_th=0.001 rising=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P006` / `G8 hist_th=0.005 rising=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P005` / `G8 hist_th=0.005 rising=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P008` / `G8 hist_th=0.01 rising=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P007` / `G8 hist_th=0.01 rising=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P010` / `G8 hist_th=0.02 rising=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P009` / `G8 hist_th=0.02 rising=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P012` / `G8 hist_th=0.05 rising=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G8_P011` / `G8 hist_th=0.05 rising=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

### group `group_g9_session`

- **失败** `V7_G9_P002` / `G9 sess=asia macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P001` / `G9 sess=asia macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P004` / `G9 sess=europe macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P003` / `G9 sess=europe macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P008` / `G9 sess=no_asia macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P007` / `G9 sess=no_asia macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P010` / `G9 sess=no_low macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P009` / `G9 sess=no_low macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P012` / `G9 sess=overlap macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P011` / `G9 sess=overlap macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P006` / `G9 sess=us macd=False`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)
- **失败** `V7_G9_P005` / `G9 sess=us macd=True`：Sharpe<0.9；PF<1.3；交易数<800 (Sharpe=0.00, PF=0.00, 交易=0, 回撤%=0.00)

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
