# 半月四 bot 工作简报
- schedule: CRON_TZ=Asia/Shanghai 25 9 1,15 * *
- timing: flexible ±15 min
- enabled: true

## Prompt
每月 1 日与 15 日早上，汇总业务 bot 近半个月的工作，并单独做「模型余额」一块，做成图文并茂的直观半月报（Asia/Shanghai）。全文必须用简体中文。

三个业务 bot 仍每周日向你交工作周报；DeepSeek Bot 每周日向你交模型与余额周报。改卷复审Bot 没有定时周报任务：每次做半月报时，用 SendToAgent 向他要本期简短材料即可。

收集来源：近半个月三位业务队友周报、改卷复审Bot 本期材料、DeepSeek 模型周报、对话备份素材、催交状态与上期余额快照。

做一份可回看的图文半月报 Page：按 bot 分节（含头像）+「模型余额」板块（上期/本期剩余金额与用过模型名，不要 token 细账）。把 Page 链接发到本聊天给用户。
