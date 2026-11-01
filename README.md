# Grok Bots 个人备份 / Personal backup

这是一份 **公开、可参考** 的 Grok Bot 工作流备份：六个相互协作的 Bot、共享技能，以及定时例程的说明。副本做了轻量脱敏。

A **public, reference-friendly** backup of a Grok Bot fleet: six collaborating bots, shared skills, and scheduled-routine notes. This GitHub copy is lightly redacted.

适合想搭类似「多 Bot 分工 + 共享技能 + 定时例程」工作流的人对照结构；不是开箱即用的模板，也没有可直接登录的账号或密钥。

Useful if you want to study a multi-bot + shared-skills + routines setup. Not a turnkey template, and it ships with no credentials.

**备份日期 / Backup date:** 2026-11-01（Asia/Shanghai）

## 六个 Bot 怎么分工 / How the six bots split work

| Bot | 角色（概要） / Role (sketch) |
|---|---|
| Grok Bot | 协调、备份、简报与跨 Bot 编排 / coordination, backups, digests, cross-bot orchestration |
| 学科网试卷Bot | 从学科网取卷、整理进教学资料夹 / fetch & organize papers from 学科网 |
| 高三试卷知识库Bot | 把试卷补进 ima 化学试卷知识库（只增不改） / add papers into the ima chemistry KB (add-only) |
| 知识库索引Bot | 维护试卷索引与可交付清单 / maintain the paper index & deliverables |
| 阅卷复审Bot | 在线阅卷平台上的复查与异议整理 / online-marking review & dispute notes |
| DeepSeek Bot | 仅在明确点名时接手；走官方 DeepSeek API（文字 / 读图） / only when explicitly asked; official DeepSeek API (text / vision) |

日常各自用自己的默认模型。DeepSeek 只在你主动叫它时才介入。

Day-to-day each bot uses its own default model. DeepSeek only joins when you explicitly hand work over.

## 仓库里有什么 / What's in the repo

- `bots/`：六个 Bot 的 profile 与头像 / profiles + avatars
- `skills/`：共享自建技能（含辅助脚本） / custom shared skills (incl. helper scripts)
- `routines/`：定时例程说明（催交周报、半月简报、每月 GitHub 备份等） / routine notes (weekly nudge, biweekly digest, monthly GitHub backup, …)

分支约定：`main` 是完整备份；`skills` / `bots` / `routines` 是对应内容的长寿命更新分支。

Branch layout: `main` holds the full backup; long-lived `skills` / `bots` / `routines` branches track those slices.

## 占位符 / Placeholders

下列占位符表示公开副本里被脱敏的字段。

The placeholders below mark fields that are redacted in this public copy.

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

- 本仓库 **不含** API Key、密码、保险库导出或其他机密。
- Cursor 系统自带技能不在此备份（只备份自建技能）。

- No API keys, passwords, vault exports, or other secrets.
- Cursor-managed skills are omitted on purpose; only custom skills are here.

<img width="1128" height="785" alt="抱你！" src="https://github.com/user-attachments/assets/5c7437c2-b3c4-4b13-8287-117a72f83261" />

**<p align="center">在此，谢谢你！</p>**
**<p align="center">Thank you so much!</p>**
