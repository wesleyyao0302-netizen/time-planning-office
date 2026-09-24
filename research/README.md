# Baseline forecast quick start

## 研究边界（第一版）

- 预测对象：数据中心在 PCC / 接网节点处的有功功率；
- 时间分辨率：1 小时；
- 预测时域：下一时段/下一天可在获得真实数据后进一步确定；
- 第一组特征：前 24 小时同一时刻、前 168 小时同一时刻；
- 第一组模型：previous day、previous week、50/50 lag mean、linear regression；
- 划分方式：按时间先后 chronological split，不随机打乱；
- 指标：MAE、RMSE、MAPE。

这一边界是为了在本周先跑通最小可验证结果，不代表最终论文范围已经确定。

## 输入数据

把真实数据放在 `data/hourly_load.csv`：

```csv
timestamp,power_mw
2026-01-01T00:00:00+00:00,41.2
2026-01-01T01:00:00+00:00,40.7
```

要求：

- 至少 21 天逐小时数据；
- 时间戳唯一并可按时间排序；
- `power_mw` 是同一测量边界下的有功功率；
- 缺失值、时区和 daylight-saving 处理需要在使用真实数据时单独记录。

如果文件不存在，脚本会自动生成 60 天合成数据。生成图会带有 `SYNTHETIC DEMO` 标记。

## 运行

```bash
python3 -m pip install -r requirements.txt
python3 research/baseline_forecast.py
```

输出：

- `research/outputs/metrics.csv`
- `research/outputs/predictions.csv`
- `research/outputs/model_summary.json`
- `research/outputs/forecast_plot.png`

## 组会前人工核查

1. 随机挑 3 个测试时点，手算 lag-24、lag-168 和 lag mean。
2. 确认 test 数据没有参与线性回归系数拟合。
3. 检查 MW/kW 单位是否混用。
4. 检查时间戳时区与夏令时是否导致重复或缺失小时。
5. 把每个公式与来源论文逐一核对；AI 生成的解释不能代替核查。
