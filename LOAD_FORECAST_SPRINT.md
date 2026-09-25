# 负荷预测快速成果冲刺（2026-09-28 至 2026-10-30）

目标是在五周内形成第一份基于真实数据、可复现、可向导师展示的负荷预测成果包。它是研究起点，不宣称论文创新或数据中心普适结论。

## 1. 最小研究问题

> 在严格遵守时间顺序、避免数据泄漏的条件下，简单的日/周季节基线、线性模型和树模型，能否对半小时级聚合负荷形成稳定的日 ahead 点预测与 P50/P90 分位数预测？误差在峰值时段如何变化？

这一步对应研究主链：

```text
负荷预测误差与不确定性
→ 峰值时段/高负荷状态的风险
→ 后续配网 headroom、约束和接网筛查
```

第一阶段只证明预测与不确定性分析管线可信；没有网络模型或容量数据时，不把误差改善直接表述为接网价值。

## 2. 数据选择：24 小时止损规则

### 首选候选：数据中心/变电站负荷

- [UK Power Networks — Smart Meter Consumption: Substation](https://ukpowernetworks.opendatasoft.com/explore/assets/ukpn-smart-meter-consumption-substation/)
- 先核查：是否可下载、字段定义、时间覆盖、单位、匿名化方式、数据中心标签和许可证。
- 如果注册/权限或字段问题在 **24 小时内**不能解决，立即使用备用数据跑通研究管线，不让数据申请拖住第一份结果。

### 备用真实数据：Low Carbon London

- [London Datastore — SmartMeter Energy Consumption Data in London Households](https://data.london.gov.uk/dataset/smartmeter-energy-consumption-data-in-london-households-vqm0d)
- UK Power Networks 的 Low Carbon London 项目样本，5,567 户、半小时分辨率、2011-11 至 2014-02。
- 它可验证代码和方法，但属于住宅负荷；最终报告必须明确：不能据此声称数据中心负荷规律。

如两个来源均暂时不可用，再使用 UCI Electricity Load Diagrams 2011–2014；同样只作为方法基准。

## 3. 固定实验定义

| 项目 | 第一版决定 |
|---|---|
| 预测对象 | 单站/聚合有功或能耗时间序列；单位统一并记录转换 |
| 分辨率 | 半小时；若源数据不同则重采样并记录聚合规则 |
| 预测任务 | Day-ahead，预测未来 48 个半小时点 |
| 时间切分 | 最早 60% train、随后 20% validation、最后 20% test；不随机打乱 |
| 滚动验证 | 只在 train/validation 内做 expanding 或 rolling origin |
| 季节基线 | `t-48`、`t-336`、二者均值 |
| 模型 | 线性回归、Random Forest、HistGradientBoosting；XGBoost 仅在环境稳定时加入 |
| 特征 | lag-48、lag-336、rolling mean/std、half-hour、weekday、weekend；外生变量只在预测时可得时加入 |
| 点预测指标 | MAE、RMSE、sMAPE；MAPE 仅在接近零负荷不影响解释时报告 |
| 概率预测 | P50/P90 quantile；报告 pinball loss，并检查 `y ≤ q90` 的经验比例是否接近 90% |
| 分层检查 | 峰值 10%、工作日/周末、时段、站点；不能只报总体平均 |

任何归一化、缺失值填补和特征统计都只用训练窗口拟合。测试集只运行一次作为冻结结果。

## 4. 五周计划与成果冻结

| 截止日 | 工作 | 必须留下的成果 |
|---|---|---|
| 10-02 | 数据访问、字段核查、目标/边界和季节基线 | `data_dictionary-v01.csv`、`data_provenance-v01.md`、baseline 脚本 |
| 10-09 | 真实数据清洗和 Naive/线性模型 | `baseline_results-v01.csv`、最后 7 天预测图、可运行命令 |
| 10-16 | EDA、时间特征和质量分析 | 缺失/异常/周期图、`feature_availability-v01.csv`、泄漏检查表 |
| 10-23 | RF/Boosting 与 rolling validation | 同口径模型表、滚动验证图、训练耗时和失败记录 |
| 10-30 | P50/P90、峰值分析和成果包 | 两张核心图、一张结果表、两页 brief、复现 README、下一步实验 |

每周五 12:00–12:20 是“成果冻结”，只做四件事：确认文件可打开、更新版本号、写一句结论、登记下一步。不在该时段继续调模型。

## 5. 10 月 30 日成果包

```text
load-forecast-v01/
├── README.md
├── data_provenance.md
├── data_dictionary.csv
├── src/
│   ├── prepare_data.py
│   ├── build_features.py
│   ├── train_baselines.py
│   └── evaluate.py
├── configs/experiment-v01.yaml
├── results/model_comparison.csv
├── figures/forecast_last_7_days.png
├── figures/peak_and_p50_p90.png
└── brief/load_forecast_result_v01.pdf
```

两页 brief：

1. **问题、数据、切分和方法**：为什么这个预测对象有用，数据来自哪里，如何避免泄漏；
2. **结果、限制和下一步**：模型比较、峰值/P50/P90 图、不能推出什么、下一步如何连接配网或数据中心数据。

## 6. 成功、失败与停止标准

### 第一版成功

- 使用真实数据；
- 至少三个季节基线和两个学习模型；
- chronological/rolling validation 正确；
- 两张图和一张表可以复现；
- P50/P90 有清楚定义和校准检查；
- 结果、负面结果和限制均进入年审证据台账。

### 需要停止并修复

- 测试结果优于验证结果但无法解释；
- 使用未来信息或随机切分；
- 不同模型使用不同测试窗口；
- 只报告最好一次运行；
- 把住宅/通用负荷结果描述成数据中心结论；
- 为追求复杂模型而没有稳定基线。

## 7. 给导师看的最小版本

一句话结论模板：

> 在 `[数据/站点]` 的 `[测试期]`，`[模型]` 相对 `t-48/t-336` 基线在 `[指标]` 上变化 `[数值]`；但 `[峰值/跨站点/数据代表性]` 仍是主要限制。下一步将测试 `[一个最小实验]`，判断该改善是否影响 `[headroom/约束/连接筛查]`。

没有可靠数值时不要填入推测值；用“尚未建立”“结果不稳定”并说明下一次实验。
