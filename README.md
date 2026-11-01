# Grok Bots 个人备份 / Personal backup

小呼的 Grok Bot 工作流备份（轻量脱敏公开版）。本机运行中的 Bot 不受影响，只有这份 GitHub 副本用了占位符。

Light-redacted public backup of 小呼's Grok Bot fleet. Live bots are unchanged; only this GitHub copy uses placeholders.

**备份日期 / Backup date:** 2026-11-01（Asia/Shanghai）

## 内容 / Contents

- `bots/`：六个 Bot 的 profile 与头像 / six bot profiles + avatars
- `skills/`：共享自建技能（含取卷脚本等）/ custom shared skills (incl. helper scripts)
- `routines/`：Grok Bot 定时例程说明 / scheduled routine descriptions

## 占位符 / Placeholders

真实值不在本仓库，由 Grok Bot 在本机保管，需要时可还原。
Real values are kept privately by Grok Bot, not in this repo, and can be restored when needed.

| 占位符 / Placeholder | 含义 / Meaning |
|---|---|
| `{{ONEDRIVE_TEACHING_ROOT}}` | OneDrive 教学试卷根目录 / OneDrive teaching-papers root |
| `{{IMA_CHEMISTRY_KB}}` | ima 化学试卷知识库名 / ima chemistry papers KB name |
| `{{GROK_BOT_ID}}` | Grok Bot ID |
| `{{XKW_BOT_ID}}` | 学科网试卷Bot ID |
| `{{KB_PAPERS_BOT_ID}}` | 高三试卷知识库Bot ID |
| `{{INDEX_BOT_ID}}` | 知识库索引Bot ID |
| `{{REVIEW_BOT_ID}}` | 阅卷复审Bot ID |
| `{{DEEPSEEK_BOT_ID}}` | DeepSeek Bot ID |

## 说明 / Notes

本仓库不含 API Key、密码、保险库导出或学生信息；系统自带 Cursor 技能不在此备份。

No API keys, passwords, vault exports, or student data. Cursor-managed skills are omitted on purpose.
