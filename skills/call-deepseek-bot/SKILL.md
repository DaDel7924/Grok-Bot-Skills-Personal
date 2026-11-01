---
name: Call DeepSeek Bot
description: >-
  Only when the user explicitly asks to involve DeepSeek Bot / official DeepSeek
  API—not for every text or vision task. Do not use Gemini.
---
# Call DeepSeek Bot

Use this **only when the user explicitly asks** to hand work to DeepSeek Bot, or names DeepSeek / deepseek-v4-pro / deepseek-flash. Day-to-day, each bot uses its **own** default model and tools—do **not** auto-forward every text or vision task.

DeepSeek Bot is a **tool teammate** for other bots, not a standing business bot.

**Do not use Google Gemini** (no default, fallback, or named path). **Do not use Composio DeepSeek** for this handoff.

## When to hand off

Send to DeepSeek Bot with `SendToAgent`:

- `target_id`: `{{DEEPSEEK_BOT_ID}}`
- `priority`: `true` when you need a reply or someone is waiting; `false` for FYI only
- Keep the message short: goal, constraints, language, and what to return
- Path (official DeepSeek API, `DEEPSEEK_API_KEY`): **文字 → deepseek-v4-pro**（强制推理档）; **阅卷读图 → deepseek-flash**（百炼 Qwen 仅备用）
- For vision, attach image paths/files

In chat you can write `@DeepSeek Bot` so the user sees a chip.

## Do not

- Treat DeepSeek as the default for all LLM work
- Call or fall back to Gemini
- Route text through Composio DeepSeek for this handoff
- Fan out the same ask to several bots unless the user asked
