# Research Time Workstation

[在线工作站](https://wesleyyao0302-netizen.github.io/time-planning-office/) · [订阅日历](https://wesleyyao0302-netizen.github.io/time-planning-office/calendar.ics)

从2026-09-28起：周一、二、四、五、六、日09:00–11:00与14:00–16:00各两小时科研，每周24小时；周三09:00–11:00准备组会，12:00–13:00组会。

全部课程移至19:00后：英语周三、五、日19:00–21:00；其他四晚自学19:00–20:45、21:00–22:45。课程视频与学习总时长保留，长块拆段，12月19日完成课程归档，英语12月20日结束。原圣诞休息期12-21至01-03保留。科研周期截至2027-07-09。

全部项目提前10分钟提醒；是否弹窗取决于日历客户端及通知权限。ENG5292已删除。

- [逐段学习路线](COURSE_ROADMAP.md)
- [本周任务](WEEK_PLAN.md)
- [负荷预测成果冲刺](LOAD_FORECAST_SPRINT.md)
- [年审证据台账](ANNUAL_REVIEW_EVIDENCE.md)

## 维护与订阅

数据源为 data/schedule.json；事件id保持稳定，跨段新增-part编号。执行 python3 scripts/build_calendar.py 生成日历，再执行 python3 -m unittest discover -s tests 验证。提交main后自动发布GitHub Pages。

通过URL订阅才会后续更新；直接导入只是静态副本。订阅刷新速度由客户端决定。每个项目默认10分钟提醒。

## 科研代码

安装 requirements.txt 后运行 research/baseline_forecast.py。没有真实数据时生成的合成示例仅验证程序，不作为研究结论。详见 research/README.md。

## 隐私

公开GitHub Pages中勿写入敏感数据。过去排期可通过Git提交历史恢复。
