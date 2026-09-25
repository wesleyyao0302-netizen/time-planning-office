# 年审成果与证据台账

这份台账把“做过什么”转化为可核查的 evidence。它记录的是文件、代码、模型、图表、结论与决策，不把观看视频、阅读时长或模糊的“了解了”作为成果。

## 1. 每类时间块的最低成果

| 时间块 | 最低可接受成果 | 完成判据 |
|---|---|---|
| 周一：问题与数据 | 一页研究问题/数据边界，或更新后的数据字典 | 文件已保存；写明本周要减少的一个不确定性 |
| 周二：模型与实验 | 代码提交 + 实验配置 + 原始结果 | 能从固定输入重新运行；记录数据版本与时间切分 |
| 周三：组会准备 | 一页结果、限制、导师决策问题 | 能在 3 分钟内讲清；组会后补记反馈 |
| 周四上午：分析与验证 | 泄漏/单位/假设检查，或对照/敏感性分析 | 至少记录一项通过、一项风险和处理决定 |
| 周五：结果与记录 | 周总结 + 下周最小实验 | 所有证据链接可打开；未完成项有原因和新日期 |
| 电力电子理论 | 推导页、拓扑/器件对照表或研究映射 | 至少一个公式/图表经过手算或第二来源核对 |
| MATLAB/Simulink | 模型、参数表、关键波形、理论误差 | 模型可运行；记录求解器/采样时间与异常解释 |
| 机器学习 | Notebook/脚本、指标表、预测图 | chronological split；基线和数据泄漏检查齐全 |
| 电力电子（研） | 推导/设计表/最小模型 + 数据中心 PSU 映射 | 不仅复述课程；明确与效率、可靠性或 PCC 的关系 |

英语课程和一般行政任务不作为核心研究成果，但可在年审的 training/professional development 部分列为参与记录。

## 2. 统一记录格式

每项成果使用文件名：

```text
YYYY-MM-DD_topic_artifact-v01.ext
```

每周在下面追加一行：

| 日期 | 研究问题/任务 | 成果路径或链接 | 一句话结论 | 限制/负面结果 | 导师反馈 | 下一步 | 状态 |
|---|---|---|---|---|---|---|---|
| YYYY-MM-DD | 示例：lag-168 是否改善周周期负荷预测？ | `research/...` | 示例：验证集 MAE 降低，但峰值误差仍大 | 数据仅为合成数据 | 待讨论 | 换真实数据并按负荷水平分层 | Planned |

状态只使用：`Planned`、`In progress`、`Evidence ready`、`Reviewed`。只有成果路径可打开时才能使用 `Evidence ready`。

## 3. Python 完整课程成果关口

| 截止日期 | 必须归档的成果 | 状态 |
|---|---|---|
| 2026-09-29 | `python/2026-09-29_load-csv-baseline-fast-track-v01.py` + 运行记录 | Planned |
| 2026-10-28 | `python/2026-10-28_forecast-experiment-classes-v01.py` + 测试 | Planned |
| 2026-11-18 | `python/2026-11-18_load-forecast-package-v01/`（模块、测试、README） | Planned |

速通只证明可以开始研究代码；11 月 18 日的包结构、测试和复现说明才构成完整课程的收口证据。

## 4. 电力电子（研）成果登记

以下均为计划，不代表已经完成。

| 日期 | 阶段 | 必须归档的成果 | 状态 |
|---|---|---|---|
| 2026-11-23 | 课程框架 | `power-electronics/2026-11-23_course-research-map-v01.pdf` | Planned |
| 2026-11-24 | 本科诊断 | `power-electronics/2026-11-24_prerequisite-gap-table-v01.xlsx` | Planned |
| 2026-11-26 | 谐振基本模态 | `power-electronics/2026-11-26_resonant-modes-zvs-map-v01.pdf` | Planned |
| 2026-11-28 | SRC 设计 | `power-electronics/2026-11-28_src-gain-design-sheet-v01.xlsx` | Planned |
| 2026-11-30 | 拓扑选择 | `power-electronics/2026-11-30_src-prc-lcc-llc-matrix-v01.pdf` | Planned |
| 2026-12-01 | LLC 模态 | `power-electronics/2026-12-01_llc-mode-boundaries-v01.pdf` | Planned |
| 2026-12-03 | LLC 设计 | `power-electronics/2026-12-03_llc-design-worksheet-v01.xlsx` | Planned |
| 2026-12-05 | 整流/保护/控制 | `power-electronics/2026-12-05_efficiency-protection-control-v01.pdf` | Planned |
| 2026-12-07 | 多元件谐振 | `power-electronics/2026-12-07_multielement-vs-llc-v01.pdf` | Planned |
| 2026-12-08 | ZCS | `power-electronics/2026-12-08_zcs-stress-comparison-v01.pdf` | Planned |
| 2026-12-10 | ZVS/多谐振 | `power-electronics/2026-12-10_zcs-zvs-multiresonant-v01.pdf` | Planned |
| 2026-12-12 | PWM 软开关 | `power-electronics/2026-12-12_soft-switching-selection-v01.pdf` | Planned |
| 2026-12-14 | WPT 模型 | `power-electronics/2026-12-14_wpt-equivalent-model-v01.pdf` | Planned |
| 2026-12-15 | 耦合/补偿 | `power-electronics/2026-12-15_coupler-compensation-matrix-v01.pdf` | Planned |
| 2026-12-17 | 高频变换 | `power-electronics/2026-12-17_high-frequency-loss-chain-v01.pdf` | Planned |
| 2026-12-19 | 综合成果 | `power-electronics/2026-12-19_datacentre-psu-research-map-v01.pdf` + 最小模型 | Planned |

## 5. 压缩周期的年审检查点

| 截止日期 | 汇总成果 | 年审价值 |
|---|---|---|
| 2026-11-28 | 课程映射、先修诊断、SRC 模态与设计包 | 证明压缩学习仍有明确研究目的和核查证据 |
| 2026-12-05 | LLC 拓扑、模态、设计、保护与控制包 | 证明已从概念进入设计与权衡 |
| 2026-12-12 | 多元件、ZCS/ZVS 与 PWM 软开关对照 | 证明分析和技术选择能力 |
| 2026-12-19 | 数据中心 PSU 一页总图 + 模型/波形包 | 形成可放入年审附件的技术能力证据 |

每个检查点压缩成一页：`问题 → 做了什么 → 证据 → 发现 → 局限 → 下一步`。如果课程成果不能连接到负荷预测、配网影响或数据中心连接研究，只放入 training 记录，不把它包装成主要研究结果。

## 6. 年审材料建议结构

1. **研究问题与演化**：从负荷预测不确定性，到配网影响，再到连接/运行决策；
2. **文献与证据基础**：来源、分类、关键 gap 和证据质量；
3. **数据与方法**：数据来源、测量边界、时间切分、基线、指标与不确定性；
4. **已完成结果**：图表、代码、实验、负面结果及其解释；
5. **技术训练如何服务研究**：Python、ML、MATLAB/Simulink、电力电子，不按观看时长计量；
6. **导师反馈与决策记录**：每次组会改变了什么；
7. **下一阶段计划与风险**：数据、方法、范围、时间与缓解措施。

## 7. 真实性边界

- `Planned` 不能写成“已掌握”或“已完成”；
- 合成数据结果只能证明代码可运行，不能作为研究结论；
- 课程复现必须区分教师示例和自己的独立工作；
- 负面结果、失败模型和被否定假设同样是证据，但必须记录条件和原因；
- 预测误差改善只有在网络影响或决策价值被验证后，才能声称对配网/接网有意义。
