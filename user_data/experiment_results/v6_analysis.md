# V5 三阶段回测分析报告

- 生成路径: `C:\Users\hlin2\freqtrade\user_data\experiment_results\v6_analysis.md`
- 数据根目录: `C:\Users\hlin2\freqtrade`

## 1. 全样本排名（Top 20，按 Sharpe 降序）

基线参考: Sharpe **1.21**, PF **1.5**, 最大回撤 **11.24%**, 总利润 **1398%**, 交易数 **1098**。

| 排名 | strategy | group | name | Sharpe | PF | 利润% | 回撤% | 交易数 | 超越基线(分项) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | V6_E1_P007 | group_e1_short | E1 no_macd ADX=24 | 1.49 | 1.23 | 3157.0 | 17.2 | 3056 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 2 | V6_E1_P001 | group_e1_short | E1 mirror ADX=24 | 1.48 | 1.24 | 2241.6 | 15.1 | 2801 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 3 | V6_E1_P004 | group_e1_short | E1 relaxed_ema ADX=24 | 1.44 | 1.21 | 3113.7 | 17.2 | 3047 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 4 | V6_E1_P008 | group_e1_short | E1 no_macd ADX=28 | 1.37 | 1.25 | 2698.3 | 18.8 | 2413 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 5 | V6_E1_P002 | group_e1_short | E1 mirror ADX=28 | 1.34 | 1.27 | 2203.4 | 18.8 | 2225 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 6 | V6_E1_P005 | group_e1_short | E1 relaxed_ema ADX=28 | 1.32 | 1.24 | 2550.4 | 18.8 | 2403 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 7 | V6_E2_P002 | group_e2_adx | E2 ADX=24 | 1.30 | 1.41 | 1639.3 | 26.9 | 1397 | Sharpe:✓ PF:× 回撤:× 利润%:✓ 交易数:✓ |
| 8 | V6_E2_P003 | group_e2_adx | E2 ADX=26 | 1.24 | 1.44 | 1468.6 | 9.7 | 1241 | Sharpe:✓ PF:× 回撤:✓ 利润%:✓ 交易数:✓ |
| 9 | V6_E2_P004 | group_e2_adx | E2 ADX=28 | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 10 | V6_F1_P001 | group_f1_baseline | F1 CryptoV11 baseline | 1.21 | 1.50 | 1397.8 | 11.2 | 1098 | Sharpe:✓ PF:✓ 回撤:✓ 利润%:× 交易数:✓ |
| 11 | V6_E9_P008 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=40 | 1.19 | 1.49 | 1227.0 | 12.5 | 1087 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:× |
| 12 | V6_E9_P012 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=40 | 1.19 | 1.50 | 1255.6 | 11.9 | 1081 | Sharpe:× PF:✓ 回撤:× 利润%:× 交易数:× |
| 13 | V6_E9_P016 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=40 | 1.19 | 1.50 | 1225.4 | 11.9 | 1086 | Sharpe:× PF:✓ 回撤:× 利润%:× 交易数:× |
| 14 | V6_E9_P009 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=25 | 1.17 | 1.46 | 1198.4 | 11.8 | 1115 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 15 | V6_E9_P011 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=35 | 1.17 | 1.47 | 1165.4 | 11.9 | 1091 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:× |
| 16 | V6_E9_P001 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=25 | 1.16 | 1.45 | 1199.6 | 12.3 | 1137 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 17 | V6_E9_P004 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=40 | 1.16 | 1.47 | 1127.8 | 12.5 | 1094 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:× |
| 18 | V6_E9_P007 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=35 | 1.16 | 1.47 | 1146.2 | 12.5 | 1098 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 19 | V6_E9_P013 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=25 | 1.16 | 1.45 | 1199.6 | 12.3 | 1137 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |
| 20 | V6_E9_P015 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=35 | 1.16 | 1.46 | 1170.8 | 12.9 | 1101 | Sharpe:× PF:× 回撤:× 利润%:× 交易数:✓ |

<details><summary>Top20 的 params 摘要（展开）</summary>

| 排名 | params |
| --- | --- |
| 1 | `{"mode":"no_macd","adx":24}` |
| 2 | `{"mode":"mirror","adx":24}` |
| 3 | `{"mode":"relaxed_ema","adx":24}` |
| 4 | `{"mode":"no_macd","adx":28}` |
| 5 | `{"mode":"mirror","adx":28}` |
| 6 | `{"mode":"relaxed_ema","adx":28}` |
| 7 | `{"ADX_MIN":24}` |
| 8 | `{"ADX_MIN":26}` |
| 9 | `{"ADX_MIN":28}` |
| 10 | `{"variant":"v11_baseline"}` |
| 11 | `{"dc_strong":12,"dc_weak":35,"adx_threshold":40}` |
| 12 | `{"dc_strong":14,"dc_weak":40,"adx_threshold":40}` |
| 13 | `{"dc_strong":10,"dc_weak":40,"adx_threshold":40}` |
| 14 | `{"dc_strong":14,"dc_weak":40,"adx_threshold":25}` |
| 15 | `{"dc_strong":14,"dc_weak":40,"adx_threshold":35}` |
| 16 | `{"dc_strong":10,"dc_weak":30,"adx_threshold":25}` |
| 17 | `{"dc_strong":10,"dc_weak":30,"adx_threshold":40}` |
| 18 | `{"dc_strong":12,"dc_weak":35,"adx_threshold":35}` |
| 19 | `{"dc_strong":10,"dc_weak":40,"adx_threshold":25}` |
| 20 | `{"dc_strong":10,"dc_weak":40,"adx_threshold":35}` |

</details>

## 2. 分组汇总

| group | 策略数 | 阶段1通过率 | 组均Sharpe | 最优 name | 最优Sharpe | 分年度验证 | Walk-Forward | 邻域std标签 | 结论 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| group_e10_stair_tp | 18 | 0% | -1.92 | E10 TP1=0.1/0.04 TP2=0.2/0.1 TP3=0.4 | -1.28 | — | — | 平滑 (0.00) | 放弃 |
| group_e11_ema_exit | 12 | 100% | 1.12 | E11 EMA exit bars=8 profit=0.03 | 1.14 | 稳定 (CV=0.42, 6/6年盈利) | 无过拟合 (OOS=1.30) | 平滑 (0.00) | 推荐 |
| group_e1_short | 16 | 0% | 0.97 | E1 no_macd ADX=24 | 1.49 | — | — | 平滑 (0.00) | 放弃 |
| group_e2_adx | 7 | 71% | 1.09 | E2 ADX=24 | 1.30 | — | — | 平滑 (0.00) | 有潜力 |
| group_e3_pullback | 18 | 0% | 0.48 | E3 pull lb=3 prox=0.8 macd=True | 0.71 | — | — | 平滑 (0.00) | 放弃 |
| group_e4_exit | 18 | 0% | 0.79 | E4b ADX decay drop=8 profit=0.03 | 0.86 | — | — | 平滑 (0.00) | 放弃 |
| group_e5_leverage | 15 | 60% | 0.90 | E5 lev low=6 high=4 th=0.8 | 0.98 | 可接受 (CV=0.71, 5/6年盈利) | — | 平滑 (0.00) | 有潜力 |
| group_e6_mtf_dc | 16 | 44% | 0.86 | E6 4H-DC=10 brk=True atr=0.0 | 1.06 | 可接受 (CV=0.67, 5/6年盈利) | — | 平滑 (0.00) | 有潜力 |
| group_e7_dyn_atr | 16 | 44% | 0.85 | E7 dynATR low=0.3 high=0.8 th=0.7 | 1.01 | 稳定 (CV=0.45, 6/6年盈利) | 无过拟合 (OOS=1.13) | 平滑 (0.00) | 推荐 |
| group_e8_adaptive_trail | 20 | 0% | -12.42 | E8 trail base=0.03 tight=0.01 bars=24 | -12.42 | — | — | 平滑 (0.00) | 放弃 |
| group_e9_adx_dc | 16 | 100% | 1.16 | E9 ADX-DC s=12 w=35 adx=40 | 1.19 | 稳定 (CV=0.41, 6/6年盈利) | 无过拟合 (OOS=1.37) | 平滑 (0.00) | 推荐 |
| group_f1_baseline | 1 | 100% | 1.21 | F1 CryptoV11 baseline | 1.21 | 稳定 (CV=0.39, 6/6年盈利) | 无过拟合 (OOS=1.33) | 平滑 (0.00) | 推荐 |

> 分年度参考：参考：2020:+85% Sharpe1.72 / 2021:+115% Sharpe1.91 / 2022:+6.94% Sharpe0.21 / 2023:+74% Sharpe1.33 / 2024:+36% Sharpe1.14 / 2025Q1:+46% Sharpe1.07

## 3. 参数邻域稳定性（阶段1，按 group × strategy）

在同一 `strategy`+`group` 内，对所有变体的 Sharpe 计算总体标准差；并按 `name` 字典序相邻检测尖峰（高于邻居最大值超过 0.3）。

| strategy | group | 变体数 | Sharpe std | 稳定性 | 尖峰标记(若有) |
| --- | --- | --- | --- | --- | --- |
| V6_E10_P001 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P002 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P003 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P004 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P005 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P006 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P007 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P008 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P009 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P010 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P011 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P012 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P013 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P014 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P015 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P016 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P017 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E10_P018 | group_e10_stair_tp | 1 | 0.00 | 平滑 | — |
| V6_E11_P001 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P002 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P003 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P004 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P005 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P006 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P007 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P008 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P009 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P010 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P011 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E11_P012 | group_e11_ema_exit | 1 | 0.00 | 平滑 | — |
| V6_E1_P001 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P002 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P003 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P004 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P005 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P006 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P007 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P008 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P009 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P010 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P011 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P012 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P013 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P014 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P015 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E1_P016 | group_e1_short | 1 | 0.00 | 平滑 | — |
| V6_E2_P001 | group_e2_adx | 1 | 0.00 | 平滑 | — |
| V6_E2_P002 | group_e2_adx | 1 | 0.00 | 平滑 | — |
| V6_E2_P003 | group_e2_adx | 1 | 0.00 | 平滑 | — |
| V6_E2_P004 | group_e2_adx | 1 | 0.00 | 平滑 | — |
| V6_E2_P005 | group_e2_adx | 1 | 0.00 | 平滑 | — |
| V6_E2_P006 | group_e2_adx | 1 | 0.00 | 平滑 | — |
| V6_E2_P007 | group_e2_adx | 1 | 0.00 | 平滑 | — |
| V6_E3_P001 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P002 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P003 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P004 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P005 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P006 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P007 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P008 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P009 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P010 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P011 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P012 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P013 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P014 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P015 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P016 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P017 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E3_P018 | group_e3_pullback | 1 | 0.00 | 平滑 | — |
| V6_E4_P001 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P002 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P003 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P004 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P005 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P006 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P007 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P008 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P009 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P010 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P011 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P012 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P013 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P014 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P015 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P016 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P017 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E4_P018 | group_e4_exit | 1 | 0.00 | 平滑 | — |
| V6_E5_P001 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P002 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P003 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P004 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P005 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P006 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P007 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P008 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P009 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P010 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P011 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P012 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P013 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P014 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E5_P015 | group_e5_leverage | 1 | 0.00 | 平滑 | — |
| V6_E6_P001 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P002 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P003 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P004 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P005 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P006 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P007 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P008 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P009 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P010 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P011 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P012 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P013 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P014 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P015 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E6_P016 | group_e6_mtf_dc | 1 | 0.00 | 平滑 | — |
| V6_E7_P001 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P002 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P003 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P004 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P005 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P006 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P007 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P008 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P009 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P010 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P011 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P012 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P013 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P014 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P015 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E7_P016 | group_e7_dyn_atr | 1 | 0.00 | 平滑 | — |
| V6_E8_P001 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P002 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P003 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P004 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P005 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P006 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P007 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P008 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P009 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P010 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P011 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P012 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P013 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P014 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P015 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P016 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P017 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P018 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P019 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E8_P020 | group_e8_adaptive_trail | 1 | 0.00 | 平滑 | — |
| V6_E9_P001 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P002 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P003 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P004 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P005 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P006 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P007 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P008 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P009 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P010 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P011 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P012 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P013 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P014 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P015 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_E9_P016 | group_e9_adx_dc | 1 | 0.00 | 平滑 | — |
| V6_F1_P001 | group_f1_baseline | 1 | 0.00 | 平滑 | — |

## 4. 分年度一致性（仅阶段1已通过门控的候选）

规则：**稳定** = CV < 0.5 且全年份盈利；**可接受** = CV < 0.8 且盈利年份≥ max(1, 总年数-1)；否则 **不稳定**。

| strategy | group | name | 全样本Sharpe | 年份数 | 盈利年数 | CV | 2022 Sharpe | 标签 | 阶段2通过 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| V6_E2_P003 | group_e2_adx | E2 ADX=26 | 1.24 | 6 | 6 | 0.34 | 0.38 | 稳定 | 是 |
| V6_E2_P004 | group_e2_adx | E2 ADX=28 | 1.21 | 6 | 6 | 0.39 | 0.21 | 稳定 | 是 |
| V6_F1_P001 | group_f1_baseline | F1 CryptoV11 baseline | 1.21 | 6 | 6 | 0.39 | 0.21 | 稳定 | 是 |
| V6_E9_P016 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=40 | 1.19 | 6 | 6 | 0.41 | 0.14 | 稳定 | 是 |
| V6_E9_P008 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=40 | 1.19 | 6 | 6 | 0.41 | 0.14 | 稳定 | 是 |
| V6_E9_P012 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=40 | 1.19 | 6 | 6 | 0.41 | 0.14 | 稳定 | 是 |
| V6_E9_P009 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=25 | 1.17 | 6 | 6 | 0.43 | 0.15 | 稳定 | 是 |
| V6_E9_P011 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=35 | 1.17 | 6 | 6 | 0.36 | 0.28 | 稳定 | 是 |
| V6_E9_P001 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=25 | 1.16 | 6 | 6 | 0.43 | 0.11 | 稳定 | 是 |
| V6_E9_P004 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=40 | 1.16 | 6 | 6 | 0.44 | 0.07 | 稳定 | 是 |
| V6_E9_P013 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=25 | 1.16 | 6 | 6 | 0.43 | 0.11 | 稳定 | 是 |
| V6_E9_P015 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=35 | 1.16 | 6 | 6 | 0.36 | 0.27 | 稳定 | 是 |
| V6_E9_P007 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=35 | 1.16 | 6 | 6 | 0.36 | 0.28 | 稳定 | 是 |
| V6_E2_P001 | group_e2_adx | E2 ADX=22 | 1.15 | 6 | 6 | 0.45 | 0.31 | 稳定 | 是 |
| V6_E9_P003 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=35 | 1.15 | 6 | 6 | 0.39 | 0.20 | 稳定 | 是 |
| V6_E9_P005 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=25 | 1.15 | 6 | 6 | 0.44 | 0.13 | 稳定 | 是 |
| V6_E9_P010 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=30 | 1.15 | 6 | 6 | 0.39 | 0.22 | 稳定 | 是 |
| V6_E11_P008 | group_e11_ema_exit | E11 EMA exit bars=16 profit=0.03 | 1.14 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E11_P012 | group_e11_ema_exit | E11 EMA exit bars=24 profit=0.03 | 1.14 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E11_P004 | group_e11_ema_exit | E11 EMA exit bars=8 profit=0.03 | 1.14 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E9_P002 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=30 | 1.14 | 6 | 6 | 0.42 | 0.15 | 稳定 | 是 |
| V6_E9_P014 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=30 | 1.14 | 6 | 6 | 0.40 | 0.19 | 稳定 | 是 |
| V6_E11_P007 | group_e11_ema_exit | E11 EMA exit bars=16 profit=0.01 | 1.13 | 6 | 6 | 0.41 | 0.17 | 稳定 | 是 |
| V6_E11_P011 | group_e11_ema_exit | E11 EMA exit bars=24 profit=0.01 | 1.13 | 6 | 6 | 0.41 | 0.17 | 稳定 | 是 |
| V6_E11_P003 | group_e11_ema_exit | E11 EMA exit bars=8 profit=0.01 | 1.13 | 6 | 6 | 0.41 | 0.17 | 稳定 | 是 |
| V6_E2_P005 | group_e2_adx | E2 ADX=30 | 1.13 | 6 | 6 | 0.33 | 0.38 | 稳定 | 是 |
| V6_E9_P006 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=30 | 1.13 | 6 | 6 | 0.41 | 0.19 | 稳定 | 是 |
| V6_E11_P006 | group_e11_ema_exit | E11 EMA exit bars=16 profit=-0.01 | 1.11 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E11_P010 | group_e11_ema_exit | E11 EMA exit bars=24 profit=-0.01 | 1.11 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E11_P002 | group_e11_ema_exit | E11 EMA exit bars=8 profit=-0.01 | 1.11 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E11_P005 | group_e11_ema_exit | E11 EMA exit bars=16 profit=-0.03 | 1.10 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E11_P009 | group_e11_ema_exit | E11 EMA exit bars=24 profit=-0.03 | 1.10 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E11_P001 | group_e11_ema_exit | E11 EMA exit bars=8 profit=-0.03 | 1.10 | 6 | 6 | 0.42 | 0.17 | 稳定 | 是 |
| V6_E6_P003 | group_e6_mtf_dc | E6 4H-DC=10 brk=False atr=0.0 | 1.06 | 6 | 5 | 0.67 | -0.44 | 可接受 | 是 |
| V6_E6_P004 | group_e6_mtf_dc | E6 4H-DC=10 brk=False atr=0.3 | 1.06 | 6 | 5 | 0.67 | -0.44 | 可接受 | 是 |
| V6_E6_P001 | group_e6_mtf_dc | E6 4H-DC=10 brk=True atr=0.0 | 1.06 | 6 | 5 | 0.67 | -0.44 | 可接受 | 是 |
| V6_E7_P003 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.7 | 1.01 | 6 | 6 | 0.45 | 0.23 | 稳定 | 是 |
| V6_E7_P004 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.8 | 1.01 | 6 | 6 | 0.38 | 0.27 | 稳定 | 是 |
| V6_E5_P015 | group_e5_leverage | E5 lev low=6 high=4 th=0.8 | 0.98 | 6 | 5 | 0.71 | -0.34 | 可接受 | 是 |
| V6_E2_P006 | group_e2_adx | E2 ADX=32 | 0.97 | 6 | 6 | 0.38 | 0.41 | 稳定 | 是 |
| V6_E5_P008 | group_e5_leverage | E5 lev low=5 high=3 th=0.7 | 0.97 | 6 | 5 | 0.49 | -0.00 | 可接受 | 是 |
| V6_E5_P014 | group_e5_leverage | E5 lev low=6 high=4 th=0.7 | 0.97 | 6 | 5 | 0.66 | -0.25 | 可接受 | 是 |
| V6_E5_P012 | group_e5_leverage | E5 lev low=7 high=4 th=0.8 | 0.96 | 6 | 5 | 0.68 | -0.28 | 可接受 | 是 |
| V6_E7_P007 | group_e7_dyn_atr | E7 dynATR low=0.4 high=0.8 th=0.7 | 0.96 | 6 | 6 | 0.42 | 0.33 | 稳定 | 是 |
| V6_E5_P013 | group_e5_leverage | E5 lev low=6 high=4 th=0.5 | 0.95 | 6 | 5 | 0.66 | -0.09 | 可接受 | 是 |
| V6_E5_P011 | group_e5_leverage | E5 lev low=7 high=4 th=0.7 | 0.95 | 6 | 5 | 0.65 | -0.19 | 可接受 | 是 |
| V6_E7_P002 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.6 | 0.95 | 6 | 6 | 0.48 | 0.17 | 稳定 | 是 |
| V6_E7_P008 | group_e7_dyn_atr | E7 dynATR low=0.4 high=0.8 th=0.8 | 0.95 | 6 | 6 | 0.36 | 0.35 | 稳定 | 是 |
| V6_E5_P010 | group_e5_leverage | E5 lev low=7 high=4 th=0.5 | 0.92 | 6 | 5 | 0.68 | -0.09 | 可接受 | 是 |
| V6_E6_P007 | group_e6_mtf_dc | E6 4H-DC=14 brk=False atr=0.0 | 0.92 | 6 | 5 | 0.70 | -0.43 | 可接受 | 是 |
| V6_E6_P008 | group_e6_mtf_dc | E6 4H-DC=14 brk=False atr=0.3 | 0.92 | 6 | 5 | 0.70 | -0.43 | 可接受 | 是 |
| V6_E6_P005 | group_e6_mtf_dc | E6 4H-DC=14 brk=True atr=0.0 | 0.92 | 6 | 5 | 0.70 | -0.43 | 可接受 | 是 |
| V6_E5_P007 | group_e5_leverage | E5 lev low=5 high=3 th=0.5 | 0.91 | 6 | 6 | 0.50 | 0.05 | 稳定 | 是 |
| V6_E5_P009 | group_e5_leverage | E5 lev low=5 high=3 th=0.8 | 0.91 | 6 | 5 | 0.56 | -0.15 | 可接受 | 是 |
| V6_E6_P002 | group_e6_mtf_dc | E6 4H-DC=10 brk=True atr=0.3 | 0.91 | 6 | 5 | 0.59 | -0.20 | 可接受 | 是 |
| V6_E7_P001 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.5 | 0.91 | 6 | 6 | 0.49 | 0.09 | 稳定 | 是 |
| V6_E7_P006 | group_e7_dyn_atr | E7 dynATR low=0.4 high=0.8 th=0.6 | 0.91 | 6 | 6 | 0.45 | 0.30 | 稳定 | 是 |

## 5. Walk-Forward 过拟合检测（对阶段2已通过门控的候选）

OOS Ratio = 平均(测试期 Sharpe) / 平均(训练期 Sharpe)；PF Decay = 平均(测试期 PF) / 平均(训练期 PF)。

| strategy | group | name | 均训练Sharpe | 均测试Sharpe | OOS | PF Decay | 过拟合标签 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| V6_E2_P001 | group_e2_adx | E2 ADX=22 | 1.25 | 1.44 | 1.15 | 1.03 | 无过拟合 |
| V6_E2_P003 | group_e2_adx | E2 ADX=26 | 1.11 | 1.47 | 1.33 | 1.10 | 无过拟合 |
| V6_E2_P004 | group_e2_adx | E2 ADX=28 | 1.11 | 1.48 | 1.33 | 1.11 | 无过拟合 |
| V6_E2_P005 | group_e2_adx | E2 ADX=30 | 0.97 | 1.24 | 1.27 | 1.12 | 无过拟合 |
| V6_E2_P006 | group_e2_adx | E2 ADX=32 | 0.93 | 1.03 | 1.12 | 1.07 | 无过拟合 |
| V6_E5_P007 | group_e5_leverage | E5 lev low=5 high=3 th=0.5 | 0.84 | 0.94 | 1.12 | 1.05 | 无过拟合 |
| V6_E5_P008 | group_e5_leverage | E5 lev low=5 high=3 th=0.7 | 0.84 | 1.06 | 1.27 | 1.09 | 无过拟合 |
| V6_E5_P009 | group_e5_leverage | E5 lev low=5 high=3 th=0.8 | 0.78 | 1.01 | 1.29 | 1.08 | 无过拟合 |
| V6_E5_P010 | group_e5_leverage | E5 lev low=7 high=4 th=0.5 | 0.72 | 0.95 | 1.32 | 1.10 | 无过拟合 |
| V6_E5_P011 | group_e5_leverage | E5 lev low=7 high=4 th=0.7 | 0.69 | 1.03 | 1.50 | 1.13 | 无过拟合 |
| V6_E5_P012 | group_e5_leverage | E5 lev low=7 high=4 th=0.8 | 0.65 | 1.08 | 1.68 | 1.15 | 无过拟合 |
| V6_E5_P013 | group_e5_leverage | E5 lev low=6 high=4 th=0.5 | 0.78 | 0.99 | 1.28 | 1.09 | 无过拟合 |
| V6_E5_P014 | group_e5_leverage | E5 lev low=6 high=4 th=0.7 | 0.71 | 1.07 | 1.51 | 1.14 | 无过拟合 |
| V6_E5_P015 | group_e5_leverage | E5 lev low=6 high=4 th=0.8 | — | — | — | — | 无WF行 |
| V6_E6_P001 | group_e6_mtf_dc | E6 4H-DC=10 brk=True atr=0.0 | — | — | — | — | 无WF行 |
| V6_E6_P002 | group_e6_mtf_dc | E6 4H-DC=10 brk=True atr=0.3 | 0.85 | 1.11 | 1.31 | 1.11 | 无过拟合 |
| V6_E6_P003 | group_e6_mtf_dc | E6 4H-DC=10 brk=False atr=0.0 | — | — | — | — | 无WF行 |
| V6_E6_P004 | group_e6_mtf_dc | E6 4H-DC=10 brk=False atr=0.3 | — | — | — | — | 无WF行 |
| V6_E6_P005 | group_e6_mtf_dc | E6 4H-DC=14 brk=True atr=0.0 | — | — | — | — | 无WF行 |
| V6_E6_P007 | group_e6_mtf_dc | E6 4H-DC=14 brk=False atr=0.0 | — | — | — | — | 无WF行 |
| V6_E6_P008 | group_e6_mtf_dc | E6 4H-DC=14 brk=False atr=0.3 | — | — | — | — | 无WF行 |
| V6_E7_P001 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.5 | 0.83 | 0.95 | 1.15 | 1.05 | 无过拟合 |
| V6_E7_P002 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.6 | 0.90 | 0.99 | 1.11 | 1.05 | 无过拟合 |
| V6_E7_P003 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.7 | 0.94 | 1.06 | 1.13 | 1.05 | 无过拟合 |
| V6_E7_P004 | group_e7_dyn_atr | E7 dynATR low=0.3 high=0.8 th=0.8 | 0.95 | 1.13 | 1.19 | 1.06 | 无过拟合 |
| V6_E7_P006 | group_e7_dyn_atr | E7 dynATR low=0.4 high=0.8 th=0.6 | 0.92 | 0.92 | 1.00 | 1.01 | 无过拟合 |
| V6_E7_P007 | group_e7_dyn_atr | E7 dynATR low=0.4 high=0.8 th=0.7 | 0.93 | 0.99 | 1.06 | 1.02 | 无过拟合 |
| V6_E7_P008 | group_e7_dyn_atr | E7 dynATR low=0.4 high=0.8 th=0.8 | 0.93 | 1.04 | 1.11 | 1.03 | 无过拟合 |
| V6_E9_P001 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=25 | 1.04 | 1.42 | 1.37 | 1.12 | 无过拟合 |
| V6_E9_P002 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=30 | 1.05 | 1.38 | 1.32 | 1.10 | 无过拟合 |
| V6_E9_P003 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=35 | 1.04 | 1.39 | 1.34 | 1.12 | 无过拟合 |
| V6_E9_P004 | group_e9_adx_dc | E9 ADX-DC s=10 w=30 adx=40 | 1.00 | 1.40 | 1.40 | 1.15 | 无过拟合 |
| V6_E9_P005 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=25 | 1.03 | 1.40 | 1.36 | 1.12 | 无过拟合 |
| V6_E9_P006 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=30 | 1.04 | 1.38 | 1.33 | 1.11 | 无过拟合 |
| V6_E9_P007 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=35 | 1.04 | 1.40 | 1.35 | 1.12 | 无过拟合 |
| V6_E9_P008 | group_e9_adx_dc | E9 ADX-DC s=12 w=35 adx=40 | 1.07 | 1.46 | 1.37 | 1.13 | 无过拟合 |
| V6_E9_P009 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=25 | 1.04 | 1.41 | 1.36 | 1.13 | 无过拟合 |
| V6_E9_P010 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=30 | 1.05 | 1.39 | 1.32 | 1.11 | 无过拟合 |
| V6_E9_P011 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=35 | 1.05 | 1.40 | 1.34 | 1.13 | 无过拟合 |
| V6_E9_P012 | group_e9_adx_dc | E9 ADX-DC s=14 w=40 adx=40 | 1.07 | 1.46 | 1.37 | 1.13 | 无过拟合 |
| V6_E9_P013 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=25 | 1.04 | 1.42 | 1.37 | 1.12 | 无过拟合 |
| V6_E9_P014 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=30 | 1.04 | 1.38 | 1.33 | 1.11 | 无过拟合 |
| V6_E9_P015 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=35 | 1.04 | 1.40 | 1.34 | 1.12 | 无过拟合 |
| V6_E9_P016 | group_e9_adx_dc | E9 ADX-DC s=10 w=40 adx=40 | 1.06 | 1.47 | 1.39 | 1.14 | 无过拟合 |
| V6_E11_P001 | group_e11_ema_exit | E11 EMA exit bars=8 profit=-0.03 | 1.05 | 1.34 | 1.28 | 1.09 | 无过拟合 |
| V6_E11_P002 | group_e11_ema_exit | E11 EMA exit bars=8 profit=-0.01 | 1.06 | 1.36 | 1.29 | 1.09 | 无过拟合 |
| V6_E11_P003 | group_e11_ema_exit | E11 EMA exit bars=8 profit=0.01 | 1.06 | 1.38 | 1.31 | 1.10 | 无过拟合 |
| V6_E11_P004 | group_e11_ema_exit | E11 EMA exit bars=8 profit=0.03 | 1.07 | 1.39 | 1.30 | 1.10 | 无过拟合 |
| V6_E11_P005 | group_e11_ema_exit | E11 EMA exit bars=16 profit=-0.03 | 1.05 | 1.34 | 1.28 | 1.09 | 无过拟合 |
| V6_E11_P006 | group_e11_ema_exit | E11 EMA exit bars=16 profit=-0.01 | 1.06 | 1.36 | 1.29 | 1.09 | 无过拟合 |
| V6_E11_P007 | group_e11_ema_exit | E11 EMA exit bars=16 profit=0.01 | 1.06 | 1.38 | 1.31 | 1.10 | 无过拟合 |
| V6_E11_P008 | group_e11_ema_exit | E11 EMA exit bars=16 profit=0.03 | 1.07 | 1.39 | 1.30 | 1.10 | 无过拟合 |
| V6_E11_P009 | group_e11_ema_exit | E11 EMA exit bars=24 profit=-0.03 | 1.05 | 1.34 | 1.28 | 1.09 | 无过拟合 |
| V6_E11_P010 | group_e11_ema_exit | E11 EMA exit bars=24 profit=-0.01 | 1.06 | 1.36 | 1.29 | 1.09 | 无过拟合 |
| V6_E11_P011 | group_e11_ema_exit | E11 EMA exit bars=24 profit=0.01 | 1.06 | 1.38 | 1.31 | 1.10 | 无过拟合 |
| V6_E11_P012 | group_e11_ema_exit | E11 EMA exit bars=24 profit=0.03 | 1.07 | 1.39 | 1.30 | 1.10 | 无过拟合 |
| V6_F1_P001 | group_f1_baseline | F1 CryptoV11 baseline | 1.11 | 1.48 | 1.33 | 1.11 | 无过拟合 |

## 6. 最终推荐（综合三阶段）

判定摘要：
- **阶段1**：Sharpe≥0.9、PF≥1.3、交易≥800、回撤≤25.0%。
- **阶段2**：分年度标签为「稳定」或「可接受」（见第4节）。
- **阶段3**：存在 WF 行且 OOS≥0.5 且平均测试 Sharpe>0；**强烈推荐** 另要求 OOS>0.8 且组内邻域 Sharpe 标准差 < 0.1（平滑）。

### 强烈推荐

- **强烈推荐** `V6_E2_P003` / `group_e2_adx` / `E2 ADX=26`：三阶段通过，Sharpe>1.21，OOS>0.8，邻域平滑(std=0.00)

### 推荐

- **推荐** `V6_E2_P001` / `group_e2_adx` / `E2 ADX=22`：三阶段通过且 Sharpe>1.0（OOS=1.15）
- **推荐** `V6_E2_P004` / `group_e2_adx` / `E2 ADX=28`：三阶段通过且 Sharpe>1.0（OOS=1.33）
- **推荐** `V6_E2_P005` / `group_e2_adx` / `E2 ADX=30`：三阶段通过且 Sharpe>1.0（OOS=1.27）
- **推荐** `V6_E7_P003` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=0.8 th=0.7`：三阶段通过且 Sharpe>1.0（OOS=1.13）
- **推荐** `V6_E7_P004` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=0.8 th=0.8`：三阶段通过且 Sharpe>1.0（OOS=1.19）
- **推荐** `V6_E9_P001` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=30 adx=25`：三阶段通过且 Sharpe>1.0（OOS=1.37）
- **推荐** `V6_E9_P002` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=30 adx=30`：三阶段通过且 Sharpe>1.0（OOS=1.32）
- **推荐** `V6_E9_P003` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=30 adx=35`：三阶段通过且 Sharpe>1.0（OOS=1.34）
- **推荐** `V6_E9_P004` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=30 adx=40`：三阶段通过且 Sharpe>1.0（OOS=1.40）
- **推荐** `V6_E9_P005` / `group_e9_adx_dc` / `E9 ADX-DC s=12 w=35 adx=25`：三阶段通过且 Sharpe>1.0（OOS=1.36）
- **推荐** `V6_E9_P006` / `group_e9_adx_dc` / `E9 ADX-DC s=12 w=35 adx=30`：三阶段通过且 Sharpe>1.0（OOS=1.33）
- **推荐** `V6_E9_P007` / `group_e9_adx_dc` / `E9 ADX-DC s=12 w=35 adx=35`：三阶段通过且 Sharpe>1.0（OOS=1.35）
- **推荐** `V6_E9_P008` / `group_e9_adx_dc` / `E9 ADX-DC s=12 w=35 adx=40`：三阶段通过且 Sharpe>1.0（OOS=1.37）
- **推荐** `V6_E9_P009` / `group_e9_adx_dc` / `E9 ADX-DC s=14 w=40 adx=25`：三阶段通过且 Sharpe>1.0（OOS=1.36）
- **推荐** `V6_E9_P010` / `group_e9_adx_dc` / `E9 ADX-DC s=14 w=40 adx=30`：三阶段通过且 Sharpe>1.0（OOS=1.32）
- **推荐** `V6_E9_P011` / `group_e9_adx_dc` / `E9 ADX-DC s=14 w=40 adx=35`：三阶段通过且 Sharpe>1.0（OOS=1.34）
- **推荐** `V6_E9_P012` / `group_e9_adx_dc` / `E9 ADX-DC s=14 w=40 adx=40`：三阶段通过且 Sharpe>1.0（OOS=1.37）
- **推荐** `V6_E9_P013` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=40 adx=25`：三阶段通过且 Sharpe>1.0（OOS=1.37）
- **推荐** `V6_E9_P014` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=40 adx=30`：三阶段通过且 Sharpe>1.0（OOS=1.33）
- **推荐** `V6_E9_P015` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=40 adx=35`：三阶段通过且 Sharpe>1.0（OOS=1.34）
- **推荐** `V6_E9_P016` / `group_e9_adx_dc` / `E9 ADX-DC s=10 w=40 adx=40`：三阶段通过且 Sharpe>1.0（OOS=1.39）
- **推荐** `V6_E11_P001` / `group_e11_ema_exit` / `E11 EMA exit bars=8 profit=-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V6_E11_P002` / `group_e11_ema_exit` / `E11 EMA exit bars=8 profit=-0.01`：三阶段通过且 Sharpe>1.0（OOS=1.29）
- **推荐** `V6_E11_P003` / `group_e11_ema_exit` / `E11 EMA exit bars=8 profit=0.01`：三阶段通过且 Sharpe>1.0（OOS=1.31）
- **推荐** `V6_E11_P004` / `group_e11_ema_exit` / `E11 EMA exit bars=8 profit=0.03`：三阶段通过且 Sharpe>1.0（OOS=1.30）
- **推荐** `V6_E11_P005` / `group_e11_ema_exit` / `E11 EMA exit bars=16 profit=-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V6_E11_P006` / `group_e11_ema_exit` / `E11 EMA exit bars=16 profit=-0.01`：三阶段通过且 Sharpe>1.0（OOS=1.29）
- **推荐** `V6_E11_P007` / `group_e11_ema_exit` / `E11 EMA exit bars=16 profit=0.01`：三阶段通过且 Sharpe>1.0（OOS=1.31）
- **推荐** `V6_E11_P008` / `group_e11_ema_exit` / `E11 EMA exit bars=16 profit=0.03`：三阶段通过且 Sharpe>1.0（OOS=1.30）
- **推荐** `V6_E11_P009` / `group_e11_ema_exit` / `E11 EMA exit bars=24 profit=-0.03`：三阶段通过且 Sharpe>1.0（OOS=1.28）
- **推荐** `V6_E11_P010` / `group_e11_ema_exit` / `E11 EMA exit bars=24 profit=-0.01`：三阶段通过且 Sharpe>1.0（OOS=1.29）
- **推荐** `V6_E11_P011` / `group_e11_ema_exit` / `E11 EMA exit bars=24 profit=0.01`：三阶段通过且 Sharpe>1.0（OOS=1.31）
- **推荐** `V6_E11_P012` / `group_e11_ema_exit` / `E11 EMA exit bars=24 profit=0.03`：三阶段通过且 Sharpe>1.0（OOS=1.30）
- **推荐** `V6_F1_P001` / `group_f1_baseline` / `F1 CryptoV11 baseline`：三阶段通过且 Sharpe>1.0（OOS=1.33）

### 观察名单

- **观察** `V6_E2_P006` / `group_e2_adx` / `E2 ADX=32`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛
- **观察** `V6_E5_P007` / `group_e5_leverage` / `E5 lev low=5 high=3 th=0.5`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V6_E5_P008` / `group_e5_leverage` / `E5 lev low=5 high=3 th=0.7`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛
- **观察** `V6_E5_P009` / `group_e5_leverage` / `E5 lev low=5 high=3 th=0.8`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V6_E5_P010` / `group_e5_leverage` / `E5 lev low=7 high=4 th=0.5`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.92），未达「推荐」门槛
- **观察** `V6_E5_P011` / `group_e5_leverage` / `E5 lev low=7 high=4 th=0.7`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.95），未达「推荐」门槛
- **观察** `V6_E5_P012` / `group_e5_leverage` / `E5 lev low=7 high=4 th=0.8`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.96），未达「推荐」门槛
- **观察** `V6_E5_P013` / `group_e5_leverage` / `E5 lev low=6 high=4 th=0.5`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.95），未达「推荐」门槛
- **观察** `V6_E5_P014` / `group_e5_leverage` / `E5 lev low=6 high=4 th=0.7`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.97），未达「推荐」门槛
- **观察** `V6_E5_P015` / `group_e5_leverage` / `E5 lev low=6 high=4 th=0.8`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=—）
- **观察** `V6_E6_P001` / `group_e6_mtf_dc` / `E6 4H-DC=10 brk=True atr=0.0`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=—）
- **观察** `V6_E6_P002` / `group_e6_mtf_dc` / `E6 4H-DC=10 brk=True atr=0.3`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V6_E6_P003` / `group_e6_mtf_dc` / `E6 4H-DC=10 brk=False atr=0.0`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=—）
- **观察** `V6_E6_P004` / `group_e6_mtf_dc` / `E6 4H-DC=10 brk=False atr=0.3`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=—）
- **观察** `V6_E6_P005` / `group_e6_mtf_dc` / `E6 4H-DC=14 brk=True atr=0.0`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=—）
- **观察** `V6_E6_P007` / `group_e6_mtf_dc` / `E6 4H-DC=14 brk=False atr=0.0`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=—）
- **观察** `V6_E6_P008` / `group_e6_mtf_dc` / `E6 4H-DC=14 brk=False atr=0.3`：阶段1+2 通过，但阶段3偏弱或无有效 WF（OOS=—）
- **观察** `V6_E7_P001` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=0.8 th=0.5`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V6_E7_P002` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=0.8 th=0.6`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.95），未达「推荐」门槛
- **观察** `V6_E7_P006` / `group_e7_dyn_atr` / `E7 dynATR low=0.4 high=0.8 th=0.6`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.91），未达「推荐」门槛
- **观察** `V6_E7_P007` / `group_e7_dyn_atr` / `E7 dynATR low=0.4 high=0.8 th=0.7`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.96），未达「推荐」门槛
- **观察** `V6_E7_P008` / `group_e7_dyn_atr` / `E7 dynATR low=0.4 high=0.8 th=0.8`：三阶段均通过，但全样本 Sharpe≤1.0（当前 0.95），未达「推荐」门槛

### 放弃/未过关

- **放弃** `V6_E1_P001` / `group_e1_short` / `E1 mirror ADX=24`：未通过阶段1
- **放弃** `V6_E1_P002` / `group_e1_short` / `E1 mirror ADX=28`：未通过阶段1
- **放弃** `V6_E1_P003` / `group_e1_short` / `E1 mirror ADX=32`：未通过阶段1
- **放弃** `V6_E1_P004` / `group_e1_short` / `E1 relaxed_ema ADX=24`：未通过阶段1
- **放弃** `V6_E1_P005` / `group_e1_short` / `E1 relaxed_ema ADX=28`：未通过阶段1
- **放弃** `V6_E1_P006` / `group_e1_short` / `E1 relaxed_ema ADX=32`：未通过阶段1
- **放弃** `V6_E1_P007` / `group_e1_short` / `E1 no_macd ADX=24`：未通过阶段1
- **放弃** `V6_E1_P008` / `group_e1_short` / `E1 no_macd ADX=28`：未通过阶段1
- **放弃** `V6_E1_P009` / `group_e1_short` / `E1 no_macd ADX=32`：未通过阶段1
- **放弃** `V6_E1_P010` / `group_e1_short` / `E1 adx_only ADX=24`：未通过阶段1
- **放弃** `V6_E1_P011` / `group_e1_short` / `E1 adx_only ADX=28`：未通过阶段1
- **放弃** `V6_E1_P012` / `group_e1_short` / `E1 adx_only ADX=32`：未通过阶段1
- **放弃** `V6_E1_P013` / `group_e1_short` / `E1 short-only mirror ADX=24`：未通过阶段1
- **放弃** `V6_E1_P014` / `group_e1_short` / `E1 short-only mirror ADX=28`：未通过阶段1
- **放弃** `V6_E1_P015` / `group_e1_short` / `E1 short-only relaxed_ema ADX=24`：未通过阶段1
- **放弃** `V6_E1_P016` / `group_e1_short` / `E1 short-only relaxed_ema ADX=28`：未通过阶段1
- **放弃** `V6_E2_P002` / `group_e2_adx` / `E2 ADX=24`：未通过阶段1
- **放弃** `V6_E2_P007` / `group_e2_adx` / `E2 ADX=34`：未通过阶段1
- **放弃** `V6_E3_P001` / `group_e3_pullback` / `E3 pull lb=3 prox=0.3 macd=True`：未通过阶段1
- **放弃** `V6_E3_P002` / `group_e3_pullback` / `E3 pull lb=3 prox=0.3 macd=False`：未通过阶段1
- **放弃** `V6_E3_P003` / `group_e3_pullback` / `E3 pull lb=3 prox=0.5 macd=True`：未通过阶段1
- **放弃** `V6_E3_P004` / `group_e3_pullback` / `E3 pull lb=3 prox=0.5 macd=False`：未通过阶段1
- **放弃** `V6_E3_P005` / `group_e3_pullback` / `E3 pull lb=3 prox=0.8 macd=True`：未通过阶段1
- **放弃** `V6_E3_P006` / `group_e3_pullback` / `E3 pull lb=3 prox=0.8 macd=False`：未通过阶段1
- **放弃** `V6_E3_P007` / `group_e3_pullback` / `E3 pull lb=5 prox=0.3 macd=True`：未通过阶段1
- **放弃** `V6_E3_P008` / `group_e3_pullback` / `E3 pull lb=5 prox=0.3 macd=False`：未通过阶段1
- **放弃** `V6_E3_P009` / `group_e3_pullback` / `E3 pull lb=5 prox=0.5 macd=True`：未通过阶段1
- **放弃** `V6_E3_P010` / `group_e3_pullback` / `E3 pull lb=5 prox=0.5 macd=False`：未通过阶段1
- **放弃** `V6_E3_P011` / `group_e3_pullback` / `E3 pull lb=5 prox=0.8 macd=True`：未通过阶段1
- **放弃** `V6_E3_P012` / `group_e3_pullback` / `E3 pull lb=5 prox=0.8 macd=False`：未通过阶段1
- **放弃** `V6_E3_P013` / `group_e3_pullback` / `E3 pull lb=8 prox=0.3 macd=True`：未通过阶段1
- **放弃** `V6_E3_P014` / `group_e3_pullback` / `E3 pull lb=8 prox=0.3 macd=False`：未通过阶段1
- **放弃** `V6_E3_P015` / `group_e3_pullback` / `E3 pull lb=8 prox=0.5 macd=True`：未通过阶段1
- **放弃** `V6_E3_P016` / `group_e3_pullback` / `E3 pull lb=8 prox=0.5 macd=False`：未通过阶段1
- **放弃** `V6_E3_P017` / `group_e3_pullback` / `E3 pull lb=8 prox=0.8 macd=True`：未通过阶段1
- **放弃** `V6_E3_P018` / `group_e3_pullback` / `E3 pull lb=8 prox=0.8 macd=False`：未通过阶段1
- **放弃** `V6_E4_P001` / `group_e4_exit` / `E4a DI exit bars=8 profit=-0.02`：未通过阶段1
- **放弃** `V6_E4_P002` / `group_e4_exit` / `E4a DI exit bars=8 profit=0.0`：未通过阶段1
- **放弃** `V6_E4_P003` / `group_e4_exit` / `E4a DI exit bars=8 profit=0.02`：未通过阶段1
- **放弃** `V6_E4_P004` / `group_e4_exit` / `E4a DI exit bars=12 profit=-0.02`：未通过阶段1
- **放弃** `V6_E4_P005` / `group_e4_exit` / `E4a DI exit bars=12 profit=0.0`：未通过阶段1
- **放弃** `V6_E4_P006` / `group_e4_exit` / `E4a DI exit bars=12 profit=0.02`：未通过阶段1
- **放弃** `V6_E4_P007` / `group_e4_exit` / `E4a DI exit bars=16 profit=-0.02`：未通过阶段1
- **放弃** `V6_E4_P008` / `group_e4_exit` / `E4a DI exit bars=16 profit=0.0`：未通过阶段1
- **放弃** `V6_E4_P009` / `group_e4_exit` / `E4a DI exit bars=16 profit=0.02`：未通过阶段1
- **放弃** `V6_E4_P010` / `group_e4_exit` / `E4a DI exit bars=20 profit=-0.02`：未通过阶段1
- **放弃** `V6_E4_P011` / `group_e4_exit` / `E4a DI exit bars=20 profit=0.0`：未通过阶段1
- **放弃** `V6_E4_P012` / `group_e4_exit` / `E4a DI exit bars=20 profit=0.02`：未通过阶段1
- **放弃** `V6_E4_P013` / `group_e4_exit` / `E4b ADX decay drop=3 profit=0.01`：未通过阶段1
- **放弃** `V6_E4_P014` / `group_e4_exit` / `E4b ADX decay drop=3 profit=0.03`：未通过阶段1
- **放弃** `V6_E4_P015` / `group_e4_exit` / `E4b ADX decay drop=5 profit=0.01`：未通过阶段1
- **放弃** `V6_E4_P016` / `group_e4_exit` / `E4b ADX decay drop=5 profit=0.03`：未通过阶段1
- **放弃** `V6_E4_P017` / `group_e4_exit` / `E4b ADX decay drop=8 profit=0.01`：未通过阶段1
- **放弃** `V6_E4_P018` / `group_e4_exit` / `E4b ADX decay drop=8 profit=0.03`：未通过阶段1
- **放弃** `V6_E5_P001` / `group_e5_leverage` / `E5 lev low=7 high=3 th=0.5`：未通过阶段1
- **放弃** `V6_E5_P002` / `group_e5_leverage` / `E5 lev low=7 high=3 th=0.7`：未通过阶段1
- **放弃** `V6_E5_P003` / `group_e5_leverage` / `E5 lev low=7 high=3 th=0.8`：未通过阶段1
- **放弃** `V6_E5_P004` / `group_e5_leverage` / `E5 lev low=6 high=3 th=0.5`：未通过阶段1
- **放弃** `V6_E5_P005` / `group_e5_leverage` / `E5 lev low=6 high=3 th=0.7`：未通过阶段1
- **放弃** `V6_E5_P006` / `group_e5_leverage` / `E5 lev low=6 high=3 th=0.8`：未通过阶段1
- **放弃** `V6_E6_P006` / `group_e6_mtf_dc` / `E6 4H-DC=14 brk=True atr=0.3`：未通过阶段1
- **放弃** `V6_E6_P009` / `group_e6_mtf_dc` / `E6 4H-DC=20 brk=True atr=0.0`：未通过阶段1
- **放弃** `V6_E6_P010` / `group_e6_mtf_dc` / `E6 4H-DC=20 brk=True atr=0.3`：未通过阶段1
- **放弃** `V6_E6_P011` / `group_e6_mtf_dc` / `E6 4H-DC=20 brk=False atr=0.0`：未通过阶段1
- **放弃** `V6_E6_P012` / `group_e6_mtf_dc` / `E6 4H-DC=20 brk=False atr=0.3`：未通过阶段1
- **放弃** `V6_E6_P013` / `group_e6_mtf_dc` / `E6 4H-DC=30 brk=True atr=0.0`：未通过阶段1
- **放弃** `V6_E6_P014` / `group_e6_mtf_dc` / `E6 4H-DC=30 brk=True atr=0.3`：未通过阶段1
- **放弃** `V6_E6_P015` / `group_e6_mtf_dc` / `E6 4H-DC=30 brk=False atr=0.0`：未通过阶段1
- **放弃** `V6_E6_P016` / `group_e6_mtf_dc` / `E6 4H-DC=30 brk=False atr=0.3`：未通过阶段1
- **放弃** `V6_E7_P005` / `group_e7_dyn_atr` / `E7 dynATR low=0.4 high=0.8 th=0.5`：未通过阶段1
- **放弃** `V6_E7_P009` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=1.0 th=0.5`：未通过阶段1
- **放弃** `V6_E7_P010` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=1.0 th=0.6`：未通过阶段1
- **放弃** `V6_E7_P011` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=1.0 th=0.7`：未通过阶段1
- **放弃** `V6_E7_P012` / `group_e7_dyn_atr` / `E7 dynATR low=0.3 high=1.0 th=0.8`：未通过阶段1
- **放弃** `V6_E7_P013` / `group_e7_dyn_atr` / `E7 dynATR low=0.5 high=1.0 th=0.5`：未通过阶段1
- **放弃** `V6_E7_P014` / `group_e7_dyn_atr` / `E7 dynATR low=0.5 high=1.0 th=0.6`：未通过阶段1
- **放弃** `V6_E7_P015` / `group_e7_dyn_atr` / `E7 dynATR low=0.5 high=1.0 th=0.7`：未通过阶段1
- **放弃** `V6_E7_P016` / `group_e7_dyn_atr` / `E7 dynATR low=0.5 high=1.0 th=0.8`：未通过阶段1
- **放弃** `V6_E8_P001` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.01 bars=24`：未通过阶段1
- **放弃** `V6_E8_P002` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.01 bars=40`：未通过阶段1
- **放弃** `V6_E8_P003` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.01 bars=56`：未通过阶段1
- **放弃** `V6_E8_P004` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.01 bars=80`：未通过阶段1
- **放弃** `V6_E8_P005` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.015 bars=24`：未通过阶段1
- **放弃** `V6_E8_P006` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.015 bars=40`：未通过阶段1
- **放弃** `V6_E8_P007` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.015 bars=56`：未通过阶段1
- **放弃** `V6_E8_P008` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.015 bars=80`：未通过阶段1
- **放弃** `V6_E8_P009` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.02 bars=24`：未通过阶段1
- **放弃** `V6_E8_P010` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.02 bars=40`：未通过阶段1
- **放弃** `V6_E8_P011` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.02 bars=56`：未通过阶段1
- **放弃** `V6_E8_P012` / `group_e8_adaptive_trail` / `E8 trail base=0.03 tight=0.02 bars=80`：未通过阶段1
- **放弃** `V6_E8_P013` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.01 bars=24`：未通过阶段1
- **放弃** `V6_E8_P014` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.01 bars=40`：未通过阶段1
- **放弃** `V6_E8_P015` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.01 bars=56`：未通过阶段1
- **放弃** `V6_E8_P016` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.01 bars=80`：未通过阶段1
- **放弃** `V6_E8_P017` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.015 bars=24`：未通过阶段1
- **放弃** `V6_E8_P018` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.015 bars=40`：未通过阶段1
- **放弃** `V6_E8_P019` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.015 bars=56`：未通过阶段1
- **放弃** `V6_E8_P020` / `group_e8_adaptive_trail` / `E8 trail base=0.04 tight=0.015 bars=80`：未通过阶段1
- **放弃** `V6_E10_P001` / `group_e10_stair_tp` / `E10 TP1=0.05/0.02 TP2=0.15/0.08 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P002` / `group_e10_stair_tp` / `E10 TP1=0.05/0.02 TP2=0.15/0.08 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P003` / `group_e10_stair_tp` / `E10 TP1=0.05/0.02 TP2=0.2/0.1 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P004` / `group_e10_stair_tp` / `E10 TP1=0.05/0.02 TP2=0.2/0.1 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P005` / `group_e10_stair_tp` / `E10 TP1=0.05/0.02 TP2=0.2/0.12 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P006` / `group_e10_stair_tp` / `E10 TP1=0.05/0.02 TP2=0.2/0.12 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P007` / `group_e10_stair_tp` / `E10 TP1=0.08/0.03 TP2=0.15/0.08 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P008` / `group_e10_stair_tp` / `E10 TP1=0.08/0.03 TP2=0.15/0.08 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P009` / `group_e10_stair_tp` / `E10 TP1=0.08/0.03 TP2=0.2/0.1 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P010` / `group_e10_stair_tp` / `E10 TP1=0.08/0.03 TP2=0.2/0.1 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P011` / `group_e10_stair_tp` / `E10 TP1=0.08/0.03 TP2=0.2/0.12 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P012` / `group_e10_stair_tp` / `E10 TP1=0.08/0.03 TP2=0.2/0.12 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P013` / `group_e10_stair_tp` / `E10 TP1=0.1/0.04 TP2=0.15/0.08 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P014` / `group_e10_stair_tp` / `E10 TP1=0.1/0.04 TP2=0.15/0.08 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P015` / `group_e10_stair_tp` / `E10 TP1=0.1/0.04 TP2=0.2/0.1 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P016` / `group_e10_stair_tp` / `E10 TP1=0.1/0.04 TP2=0.2/0.1 TP3=0.4`：未通过阶段1
- **放弃** `V6_E10_P017` / `group_e10_stair_tp` / `E10 TP1=0.1/0.04 TP2=0.2/0.12 TP3=0.3`：未通过阶段1
- **放弃** `V6_E10_P018` / `group_e10_stair_tp` / `E10 TP1=0.1/0.04 TP2=0.2/0.12 TP3=0.4`：未通过阶段1

## 7. 失败方向总结（按 group，避免重复踩坑）

### group `group_e10_stair_tp`

- **失败** `V6_E10_P001` / `E10 TP1=0.05/0.02 TP2=0.15/0.08 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-2.78, PF=0.29, 交易=1318, 回撤%=96.69)
- **失败** `V6_E10_P002` / `E10 TP1=0.05/0.02 TP2=0.15/0.08 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-2.67, PF=0.31, 交易=1328, 回撤%=96.61)
- **失败** `V6_E10_P003` / `E10 TP1=0.05/0.02 TP2=0.2/0.1 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-2.81, PF=0.27, 交易=1294, 回撤%=96.75)
- **失败** `V6_E10_P004` / `E10 TP1=0.05/0.02 TP2=0.2/0.1 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-2.72, PF=0.29, 交易=1314, 回撤%=96.61)
- **失败** `V6_E10_P005` / `E10 TP1=0.05/0.02 TP2=0.2/0.12 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-2.90, PF=0.27, 交易=1295, 回撤%=96.77)
- **失败** `V6_E10_P006` / `E10 TP1=0.05/0.02 TP2=0.2/0.12 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-2.90, PF=0.27, 交易=1298, 回撤%=96.72)
- **失败** `V6_E10_P007` / `E10 TP1=0.08/0.03 TP2=0.15/0.08 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.61, PF=0.54, 交易=1233, 回撤%=94.06)
- **失败** `V6_E10_P008` / `E10 TP1=0.08/0.03 TP2=0.15/0.08 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.59, PF=0.55, 交易=1237, 回撤%=93.62)
- **失败** `V6_E10_P009` / `E10 TP1=0.08/0.03 TP2=0.2/0.1 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.55, PF=0.55, 交易=1218, 回撤%=92.96)
- **失败** `V6_E10_P010` / `E10 TP1=0.08/0.03 TP2=0.2/0.1 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.54, PF=0.56, 交易=1219, 回撤%=92.64)
- **失败** `V6_E10_P011` / `E10 TP1=0.08/0.03 TP2=0.2/0.12 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.66, PF=0.54, 交易=1217, 回撤%=93.38)
- **失败** `V6_E10_P012` / `E10 TP1=0.08/0.03 TP2=0.2/0.12 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.65, PF=0.54, 交易=1218, 回撤%=93.19)
- **失败** `V6_E10_P013` / `E10 TP1=0.1/0.04 TP2=0.15/0.08 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.39, PF=0.61, 交易=1197, 回撤%=90.91)
- **失败** `V6_E10_P014` / `E10 TP1=0.1/0.04 TP2=0.15/0.08 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.33, PF=0.63, 交易=1199, 回撤%=90.22)
- **失败** `V6_E10_P015` / `E10 TP1=0.1/0.04 TP2=0.2/0.1 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.33, PF=0.63, 交易=1182, 回撤%=89.74)
- **失败** `V6_E10_P016` / `E10 TP1=0.1/0.04 TP2=0.2/0.1 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.28, PF=0.64, 交易=1187, 回撤%=89.03)
- **失败** `V6_E10_P017` / `E10 TP1=0.1/0.04 TP2=0.2/0.12 TP3=0.3`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.44, PF=0.61, 交易=1182, 回撤%=90.44)
- **失败** `V6_E10_P018` / `E10 TP1=0.1/0.04 TP2=0.2/0.12 TP3=0.4`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-1.43, PF=0.61, 交易=1185, 回撤%=90.09)

### group `group_e1_short`

- **失败** `V6_E1_P010` / `E1 adx_only ADX=24`：PF<1.3；回撤>25.0% (Sharpe=1.10, PF=1.08, 交易=5021, 回撤%=59.63)
- **失败** `V6_E1_P011` / `E1 adx_only ADX=28`：PF<1.3；回撤>25.0% (Sharpe=1.09, PF=1.10, 交易=3887, 回撤%=49.41)
- **失败** `V6_E1_P012` / `E1 adx_only ADX=32`：PF<1.3；回撤>25.0% (Sharpe=0.90, PF=1.11, 交易=2904, 回撤%=38.21)
- **失败** `V6_E1_P001` / `E1 mirror ADX=24`：PF<1.3 (Sharpe=1.48, PF=1.24, 交易=2801, 回撤%=15.07)
- **失败** `V6_E1_P002` / `E1 mirror ADX=28`：PF<1.3 (Sharpe=1.34, PF=1.27, 交易=2225, 回撤%=18.82)
- **失败** `V6_E1_P003` / `E1 mirror ADX=32`：PF<1.3；回撤>25.0% (Sharpe=0.92, PF=1.20, 交易=1745, 回撤%=27.68)
- **失败** `V6_E1_P007` / `E1 no_macd ADX=24`：PF<1.3 (Sharpe=1.49, PF=1.23, 交易=3056, 回撤%=17.21)
- **失败** `V6_E1_P008` / `E1 no_macd ADX=28`：PF<1.3 (Sharpe=1.37, PF=1.25, 交易=2413, 回撤%=18.84)
- **失败** `V6_E1_P009` / `E1 no_macd ADX=32`：PF<1.3；回撤>25.0% (Sharpe=1.04, PF=1.22, 交易=1870, 回撤%=31.93)
- **失败** `V6_E1_P004` / `E1 relaxed_ema ADX=24`：PF<1.3 (Sharpe=1.44, PF=1.21, 交易=3047, 回撤%=17.20)
- **失败** `V6_E1_P005` / `E1 relaxed_ema ADX=28`：PF<1.3 (Sharpe=1.32, PF=1.24, 交易=2403, 回撤%=18.84)
- **失败** `V6_E1_P006` / `E1 relaxed_ema ADX=32`：PF<1.3；回撤>25.0% (Sharpe=0.99, PF=1.21, 交易=1859, 回撤%=31.94)
- **失败** `V6_E1_P013` / `E1 short-only mirror ADX=24`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.18, PF=1.04, 交易=1404, 回撤%=35.52)
- **失败** `V6_E1_P014` / `E1 short-only mirror ADX=28`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.22, PF=1.06, 交易=1127, 回撤%=37.27)
- **失败** `V6_E1_P015` / `E1 short-only relaxed_ema ADX=24`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.32, PF=1.06, 交易=1650, 回撤%=38.49)
- **失败** `V6_E1_P016` / `E1 short-only relaxed_ema ADX=28`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.27, PF=1.07, 交易=1305, 回撤%=43.77)

### group `group_e2_adx`

- **失败** `V6_E2_P002` / `E2 ADX=24`：回撤>25.0% (Sharpe=1.30, PF=1.41, 交易=1397, 回撤%=26.87)
- **失败** `V6_E2_P007` / `E2 ADX=34`：Sharpe<0.9；交易数<800 (Sharpe=0.66, PF=1.33, 交易=754, 回撤%=14.16)

### group `group_e3_pullback`

- **失败** `V6_E3_P002` / `E3 pull lb=3 prox=0.3 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.23, PF=1.08, 交易=950, 回撤%=43.53)
- **失败** `V6_E3_P001` / `E3 pull lb=3 prox=0.3 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.36, PF=1.14, 交易=817, 回撤%=33.51)
- **失败** `V6_E3_P004` / `E3 pull lb=3 prox=0.5 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.40, PF=1.11, 交易=1215, 回撤%=45.49)
- **失败** `V6_E3_P003` / `E3 pull lb=3 prox=0.5 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.50, PF=1.15, 交易=1100, 回撤%=37.87)
- **失败** `V6_E3_P006` / `E3 pull lb=3 prox=0.8 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.67, PF=1.16, 交易=1405, 回撤%=47.54)
- **失败** `V6_E3_P005` / `E3 pull lb=3 prox=0.8 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.71, PF=1.19, 交易=1320, 回撤%=44.51)
- **失败** `V6_E3_P008` / `E3 pull lb=5 prox=0.3 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.23, PF=1.08, 交易=950, 回撤%=43.53)
- **失败** `V6_E3_P007` / `E3 pull lb=5 prox=0.3 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.36, PF=1.14, 交易=817, 回撤%=33.51)
- **失败** `V6_E3_P010` / `E3 pull lb=5 prox=0.5 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.40, PF=1.11, 交易=1215, 回撤%=45.49)
- **失败** `V6_E3_P009` / `E3 pull lb=5 prox=0.5 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.50, PF=1.15, 交易=1100, 回撤%=37.87)
- **失败** `V6_E3_P012` / `E3 pull lb=5 prox=0.8 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.67, PF=1.16, 交易=1405, 回撤%=47.54)
- **失败** `V6_E3_P011` / `E3 pull lb=5 prox=0.8 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.71, PF=1.19, 交易=1320, 回撤%=44.51)
- **失败** `V6_E3_P014` / `E3 pull lb=8 prox=0.3 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.23, PF=1.08, 交易=950, 回撤%=43.53)
- **失败** `V6_E3_P013` / `E3 pull lb=8 prox=0.3 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.36, PF=1.14, 交易=817, 回撤%=33.51)
- **失败** `V6_E3_P016` / `E3 pull lb=8 prox=0.5 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.40, PF=1.11, 交易=1215, 回撤%=45.49)
- **失败** `V6_E3_P015` / `E3 pull lb=8 prox=0.5 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.50, PF=1.15, 交易=1100, 回撤%=37.87)
- **失败** `V6_E3_P018` / `E3 pull lb=8 prox=0.8 macd=False`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.67, PF=1.16, 交易=1405, 回撤%=47.54)
- **失败** `V6_E3_P017` / `E3 pull lb=8 prox=0.8 macd=True`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.71, PF=1.19, 交易=1320, 回撤%=44.51)

### group `group_e4_exit`

- **失败** `V6_E4_P004` / `E4a DI exit bars=12 profit=-0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.79, PF=1.28, 交易=1143, 回撤%=13.23)
- **失败** `V6_E4_P005` / `E4a DI exit bars=12 profit=0.0`：Sharpe<0.9；PF<1.3 (Sharpe=0.83, PF=1.29, 交易=1130, 回撤%=14.41)
- **失败** `V6_E4_P006` / `E4a DI exit bars=12 profit=0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.28, 交易=1124, 回撤%=13.42)
- **失败** `V6_E4_P007` / `E4a DI exit bars=16 profit=-0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.79, PF=1.28, 交易=1142, 回撤%=13.89)
- **失败** `V6_E4_P008` / `E4a DI exit bars=16 profit=0.0`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.29, 交易=1130, 回撤%=14.37)
- **失败** `V6_E4_P009` / `E4a DI exit bars=16 profit=0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.29, 交易=1124, 回撤%=13.41)
- **失败** `V6_E4_P010` / `E4a DI exit bars=20 profit=-0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.77, PF=1.27, 交易=1142, 回撤%=13.71)
- **失败** `V6_E4_P011` / `E4a DI exit bars=20 profit=0.0`：Sharpe<0.9；PF<1.3 (Sharpe=0.82, PF=1.28, 交易=1130, 回撤%=14.38)
- **失败** `V6_E4_P012` / `E4a DI exit bars=20 profit=0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.83, PF=1.28, 交易=1124, 回撤%=13.44)
- **失败** `V6_E4_P001` / `E4a DI exit bars=8 profit=-0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.80, PF=1.28, 交易=1143, 回撤%=13.22)
- **失败** `V6_E4_P002` / `E4a DI exit bars=8 profit=0.0`：Sharpe<0.9；PF<1.3 (Sharpe=0.83, PF=1.29, 交易=1130, 回撤%=14.41)
- **失败** `V6_E4_P003` / `E4a DI exit bars=8 profit=0.02`：Sharpe<0.9；PF<1.3 (Sharpe=0.84, PF=1.28, 交易=1124, 回撤%=13.42)
- **失败** `V6_E4_P013` / `E4b ADX decay drop=3 profit=0.01`：Sharpe<0.9；PF<1.3 (Sharpe=0.58, PF=1.17, 交易=1232, 回撤%=13.62)
- **失败** `V6_E4_P014` / `E4b ADX decay drop=3 profit=0.03`：Sharpe<0.9；PF<1.3 (Sharpe=0.71, PF=1.21, 交易=1206, 回撤%=12.11)
- **失败** `V6_E4_P015` / `E4b ADX decay drop=5 profit=0.01`：Sharpe<0.9；PF<1.3 (Sharpe=0.63, PF=1.19, 交易=1212, 回撤%=13.61)
- **失败** `V6_E4_P016` / `E4b ADX decay drop=5 profit=0.03`：Sharpe<0.9；PF<1.3 (Sharpe=0.79, PF=1.24, 交易=1189, 回撤%=11.17)
- **失败** `V6_E4_P017` / `E4b ADX decay drop=8 profit=0.01`：Sharpe<0.9；PF<1.3 (Sharpe=0.81, PF=1.26, 交易=1192, 回撤%=14.10)
- **失败** `V6_E4_P018` / `E4b ADX decay drop=8 profit=0.03`：Sharpe<0.9；PF<1.3 (Sharpe=0.86, PF=1.27, 交易=1176, 回撤%=13.02)

### group `group_e5_leverage`

- **失败** `V6_E5_P004` / `E5 lev low=6 high=3 th=0.5`：Sharpe<0.9 (Sharpe=0.83, PF=1.31, 交易=1014, 回撤%=12.94)
- **失败** `V6_E5_P005` / `E5 lev low=6 high=3 th=0.7`：Sharpe<0.9 (Sharpe=0.85, PF=1.31, 交易=1038, 回撤%=14.10)
- **失败** `V6_E5_P006` / `E5 lev low=6 high=3 th=0.8`：Sharpe<0.9；PF<1.3 (Sharpe=0.82, PF=1.29, 交易=1050, 回撤%=15.20)
- **失败** `V6_E5_P001` / `E5 lev low=7 high=3 th=0.5`：Sharpe<0.9 (Sharpe=0.83, PF=1.31, 交易=1019, 回撤%=12.72)
- **失败** `V6_E5_P002` / `E5 lev low=7 high=3 th=0.7`：Sharpe<0.9；PF<1.3 (Sharpe=0.81, PF=1.29, 交易=1045, 回撤%=14.14)
- **失败** `V6_E5_P003` / `E5 lev low=7 high=3 th=0.8`：Sharpe<0.9；PF<1.3 (Sharpe=0.77, PF=1.27, 交易=1058, 回撤%=15.00)

### group `group_e6_mtf_dc`

- **失败** `V6_E6_P006` / `E6 4H-DC=14 brk=True atr=0.3`：Sharpe<0.9 (Sharpe=0.74, PF=1.35, 交易=814, 回撤%=10.48)
- **失败** `V6_E6_P011` / `E6 4H-DC=20 brk=False atr=0.0`：Sharpe<0.9 (Sharpe=0.82, PF=1.37, 交易=868, 回撤%=9.37)
- **失败** `V6_E6_P012` / `E6 4H-DC=20 brk=False atr=0.3`：Sharpe<0.9 (Sharpe=0.82, PF=1.37, 交易=868, 回撤%=9.37)
- **失败** `V6_E6_P009` / `E6 4H-DC=20 brk=True atr=0.0`：Sharpe<0.9 (Sharpe=0.82, PF=1.37, 交易=868, 回撤%=9.37)
- **失败** `V6_E6_P010` / `E6 4H-DC=20 brk=True atr=0.3`：Sharpe<0.9；交易数<800 (Sharpe=0.71, PF=1.37, 交易=752, 回撤%=9.87)
- **失败** `V6_E6_P015` / `E6 4H-DC=30 brk=False atr=0.0`：Sharpe<0.9 (Sharpe=0.78, PF=1.37, 交易=820, 回撤%=15.14)
- **失败** `V6_E6_P016` / `E6 4H-DC=30 brk=False atr=0.3`：Sharpe<0.9 (Sharpe=0.78, PF=1.37, 交易=820, 回撤%=15.14)
- **失败** `V6_E6_P013` / `E6 4H-DC=30 brk=True atr=0.0`：Sharpe<0.9 (Sharpe=0.78, PF=1.37, 交易=820, 回撤%=15.14)
- **失败** `V6_E6_P014` / `E6 4H-DC=30 brk=True atr=0.3`：Sharpe<0.9；交易数<800 (Sharpe=0.69, PF=1.39, 交易=701, 回撤%=15.29)

### group `group_e7_dyn_atr`

- **失败** `V6_E7_P009` / `E7 dynATR low=0.3 high=1.0 th=0.5`：Sharpe<0.9；PF<1.3 (Sharpe=0.67, PF=1.28, 交易=913, 回撤%=24.29)
- **失败** `V6_E7_P010` / `E7 dynATR low=0.3 high=1.0 th=0.6`：Sharpe<0.9；PF<1.3 (Sharpe=0.73, PF=1.29, 交易=966, 回撤%=23.42)
- **失败** `V6_E7_P011` / `E7 dynATR low=0.3 high=1.0 th=0.7`：Sharpe<0.9；回撤>25.0% (Sharpe=0.83, PF=1.31, 交易=1038, 回撤%=27.12)
- **失败** `V6_E7_P012` / `E7 dynATR low=0.3 high=1.0 th=0.8`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=0.81, PF=1.28, 交易=1099, 回撤%=26.10)
- **失败** `V6_E7_P005` / `E7 dynATR low=0.4 high=0.8 th=0.5`：Sharpe<0.9 (Sharpe=0.88, PF=1.34, 交易=1027, 回撤%=20.52)
- **失败** `V6_E7_P013` / `E7 dynATR low=0.5 high=1.0 th=0.5`：Sharpe<0.9；PF<1.3 (Sharpe=0.64, PF=1.28, 交易=856, 回撤%=20.08)
- **失败** `V6_E7_P014` / `E7 dynATR low=0.5 high=1.0 th=0.6`：Sharpe<0.9 (Sharpe=0.72, PF=1.32, 交易=887, 回撤%=16.94)
- **失败** `V6_E7_P015` / `E7 dynATR low=0.5 high=1.0 th=0.7`：Sharpe<0.9 (Sharpe=0.83, PF=1.35, 交易=934, 回撤%=20.24)
- **失败** `V6_E7_P016` / `E7 dynATR low=0.5 high=1.0 th=0.8`：Sharpe<0.9 (Sharpe=0.79, PF=1.30, 交易=982, 回撤%=22.14)

### group `group_e8_adaptive_trail`

- **失败** `V6_E8_P001` / `E8 trail base=0.03 tight=0.01 bars=24`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P002` / `E8 trail base=0.03 tight=0.01 bars=40`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P003` / `E8 trail base=0.03 tight=0.01 bars=56`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P004` / `E8 trail base=0.03 tight=0.01 bars=80`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P005` / `E8 trail base=0.03 tight=0.015 bars=24`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P006` / `E8 trail base=0.03 tight=0.015 bars=40`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P007` / `E8 trail base=0.03 tight=0.015 bars=56`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P008` / `E8 trail base=0.03 tight=0.015 bars=80`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P009` / `E8 trail base=0.03 tight=0.02 bars=24`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P010` / `E8 trail base=0.03 tight=0.02 bars=40`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P011` / `E8 trail base=0.03 tight=0.02 bars=56`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P012` / `E8 trail base=0.03 tight=0.02 bars=80`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P013` / `E8 trail base=0.04 tight=0.01 bars=24`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P014` / `E8 trail base=0.04 tight=0.01 bars=40`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P015` / `E8 trail base=0.04 tight=0.01 bars=56`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P016` / `E8 trail base=0.04 tight=0.01 bars=80`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P017` / `E8 trail base=0.04 tight=0.015 bars=24`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P018` / `E8 trail base=0.04 tight=0.015 bars=40`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P019` / `E8 trail base=0.04 tight=0.015 bars=56`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)
- **失败** `V6_E8_P020` / `E8 trail base=0.04 tight=0.015 bars=80`：Sharpe<0.9；PF<1.3；回撤>25.0% (Sharpe=-12.42, PF=0.01, 交易=1365, 回撤%=92.63)

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
