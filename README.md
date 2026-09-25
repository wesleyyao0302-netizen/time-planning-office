# Research Time Workstation

这是一个已发布到 GitHub Pages 的“科研时间规划工作站”。它把 University of Glasgow 课程、科研保护时间、Python、机器学习、电力电子本科/研究生理论与仿真、每周组会和年审证据节点写在同一份标准 iCalendar 日历中，并提供稳定订阅地址。

- 在线工作站：<https://wesleyyao0302-netizen.github.io/time-planning-office/>
- HTTPS 日历：<https://wesleyyao0302-netizen.github.io/time-planning-office/calendar.ics>
- 详细路线：[COURSE_ROADMAP.md](COURSE_ROADMAP.md)
- 负荷预测快速成果：[LOAD_FORECAST_SPRINT.md](LOAD_FORECAST_SPRINT.md)
- 年审证据台账：[ANNUAL_REVIEW_EVIDENCE.md](ANNUAL_REVIEW_EVIDENCE.md)

当前版本已经包含：

- 每周三 12:00–13:00 组会（从 2026-09-30 开始）；
- 每周三 14:00–16:00、周五 19:00–21:00 英语课程（至 2026-12-18）；
- 小甲鱼 Python 完整课程 86 个视频：先用 3 个速通块启动负荷预测，再用 8 个成果块补齐全部内容；
- 每周 14 小时科研保护块（圣诞两周暂停），周日留空；
- 傅旻帆《电力电子（本科）》24 讲，压缩为 15 个成果块并于 2026-11-19 完成；
- 傅旻帆《电力电子（研）》28 讲，本科结束后以 4 周、16 个成果块完成；
- MATLAB/Simulink 黑库 8 讲、蓝库 10 讲及 2 次综合实作，压缩为 6 个周六；
- 李沐《实用机器学习》负荷预测选段及 RNN/LSTM 对照，压缩为 7 周；
- 所有新增自学课程在 2026-12-19 完成，12 月 21 日起不再排课程；
- 2026-09-28 至 10-30 的负荷预测快速成果冲刺与五次周五成果冻结；
- 每项科研/课程工作的成果路径、结论、限制、导师反馈和下一步台账；
- 一个可直接运行的负荷预测 baseline 脚手架；
- 自动生成、测试并发布 `calendar.ics` 的 GitHub Actions 工作流。

## 1. 立即使用本地日历

运行：

```bash
python3 scripts/build_calendar.py
python3 -m unittest discover -s tests
```

生成文件：`docs/calendar.ics`。

你可以直接把它导入 Google Calendar、Apple Calendar 或 Outlook。直接导入只会复制当前事件；如果以后要自动同步，请按下一节发布订阅地址。

## 2. 订阅可更新日历

在工作站页面点击“订阅日历”，或把以下地址粘贴到支持 URL 订阅的日历应用：

```text
https://wesleyyao0302-netizen.github.io/time-planning-office/calendar.ics
```

直接下载并导入 `.ics` 只会复制当时的事件；使用 URL 订阅，后续发布的修改才会由日历应用定期获取。刷新频率由 Google Calendar、Apple Calendar 或 Outlook 决定。

### 在其他仓库重新部署

1. 在 GitHub 新建仓库，例如 `research-time-workstation`。
2. 将本项目完整上传到仓库的 `main` 分支。
3. 进入 `Settings → Pages`，将 `Source` 设为 `GitHub Actions`。
4. 打开 `Actions`，等待 `Build and deploy calendar` 完成。
5. 访问：`https://YOUR_USERNAME.github.io/YOUR_REPOSITORY/`。
6. 页面里的“订阅日历”按钮会使用稳定的 `webcal://` 地址。

命令行方式：

```bash
git init
git add .
git commit -m "Create research time workstation"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

## 3. 以后怎样更新

日程唯一数据源是 `data/schedule.json`。新增或修改事件后提交到 `main`：

```bash
python3 scripts/build_calendar.py
python3 -m unittest discover -s tests
git add data/schedule.json docs/calendar.ics
git commit -m "Update schedule"
git push
```

GitHub Actions 会重新生成并发布日历。已经订阅的设备会按各自刷新周期获取新版；刷新不是实时的，通常由日历应用自行决定。

事件示例：

```json
{
  "id": "unique-stable-id",
  "title": "事件名称",
  "start": "2026-10-01T09:00:00",
  "end": "2026-10-01T10:00:00",
  "location": "可选地点",
  "categories": ["科研"],
  "description": "完成标准"
}
```

循环事件增加 `rrule`，例如每周三：

```json
"rrule": "FREQ=WEEKLY;BYDAY=WE"
```

不要修改既有事件的 `id`，否则订阅端可能把它识别成新事件。

## 4. 课程—科研长期路线

详细安排见 [COURSE_ROADMAP.md](COURSE_ROADMAP.md)。压缩路线分三段：9 月底 Python 速通；10 月至 11 月 19 日并行完成 Python 补全、机器学习、本科电力电子和 Simulink；11 月 23 日至 12 月 19 日完成研究生电力电子冲刺。周一至周五上午仍保护 14 小时科研，周日留空。课程学习必须产生代码、图表、模型、推导或对照表并登记到 [年审证据台账](ANNUAL_REVIEW_EVIDENCE.md)，不能只以“看完视频”计进度。

近期最高优先级仍是 [负荷预测快速成果冲刺](LOAD_FORECAST_SPRINT.md)：最迟 2026-10-30 形成真实数据、泄漏安全的基线/树模型比较、P50/P90 初稿、两张图、一张表和两页 brief。课程采用成果门槛：不得挤占科研上午；当周研究成果不足时，先压缩课程笔记美化和拓展练习，不删研究实验。

## 5. 本周交付逻辑

详细安排见 [WEEK_PLAN.md](WEEK_PLAN.md)。本周先完成 Python 速通层，让代码直接服务 9 月 30 日组会；未在速通层展开的内容已排入后续 8 个补全块：

1. 研究领域和 gap 分类；
2. 数据中心接网/拓扑分类；
3. 数据与测量边界；
4. 前一天、前一周、均值与线性回归 baseline；
5. chronological split、MAE/RMSE/MAPE 和预测图；
6. 公式、数据泄漏和单位的人工核查。

## 6. 负荷预测脚手架

安装并运行：

```bash
python3 -m pip install -r requirements.txt
python3 research/baseline_forecast.py
```

如 `data/hourly_load.csv` 不存在，脚本会创建一份固定随机种子的合成演示数据；这只用于验证代码，不能作为研究结论。真实数据格式和输出说明见 [research/README.md](research/README.md)。

## 隐私提醒

GitHub Pages 地址通常可通过互联网访问。不要把未公开数据、受限论文材料、个人信息或敏感研究内容写入公开日历。需要私密订阅时，应使用支持访问控制的日历服务。
