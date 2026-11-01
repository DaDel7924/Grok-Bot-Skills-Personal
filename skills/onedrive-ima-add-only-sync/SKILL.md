---
name: onedrive-ima-add-only-sync
description: >-
  Use when adding missing senior-year chemistry exam papers from the user’s
  OneDrive {{ONEDRIVE_TEACHING_ROOT}} into the ima KB「{{IMA_CHEMISTRY_KB}}」 for 各校试卷 / 本校考试试卷 /
  日常练习资料—add-only, year folders must match, skip zip/html, report
  near-duplicates; after new uploads notify 知识库索引Bot. Not for 高考真题 import, index
  write-back to ima, deletes, or overwrites.
---
# OneDrive→ima 试卷只增同步

把 OneDrive「{{ONEDRIVE_TEACHING_ROOT}}」里缺的卷**只增**同步进 ima「{{IMA_CHEMISTRY_KB}}」（各校试卷 / 本校考试试卷 / 日常练习资料）。学年文件夹名两边必须一字对齐；永不删、永不覆盖、永不改两侧已有文件，也不改 OneDrive。具体 kb_id、folder_id、OneDrive item id、队友 agent id、API 密钥、以及 OD 顶层文件夹与 ima 三段的精确映射，放记忆/例程/环境变量，不要写进本技能。

可复用本机既有比较/上传脚本思路（如 `/workspace/ima-onedrive-compare/`、`/workspace/ima-import/`），技能正文只写通用步骤。

## When to use

- 例程周一定时跑，或用户/队友明确要求「把 OneDrive {{ONEDRIVE_TEACHING_ROOT}} 缺的卷补进 ima」。
- 范围仅 ima 侧三段主题对照（各校 / 本校 / 日常）。
- **不要**用于：高考真题导入、索引表写回 ima、电子教材整包解压、任意删改覆盖。

## OneDrive 顶层与 ima 映射（规则，细节在记忆/例程）

{{ONEDRIVE_TEACHING_ROOT}} 顶层**不是**「各校/本校/日常」三个文件夹，常见顶层是：`学科网试卷获取bot`、`教学补充资料`、`配套练习`（外加 zip）。对照时：

- `教学补充资料` 内各学期「各校试卷」→ ima「各校试卷」
- `配套练习` 内「本校考试试卷」→ ima「本校考试试卷」；其下日常/周测等 → ima「日常练习资料」（比对日常时仍**排除**日常树下的本校考试试卷子树；本校段单独比）
- `学科网试卷获取bot` 收件箱默认并入 ima「各校试卷」
- 顶层 zip 等压缩包只列报告、不上传

具体学年子路径与 folder_id 以记忆/例程为准，技能不硬编码。

## 学年文件夹归类

上传时必须按**届别 → 学年文件夹**归类，不能只看文件名里的日历年随便塞。规则：`N` 届对应学年文件夹 `{(N-1)}-{N}`。例如标题或路径里写 **2027届** → 放到 **`2026-2027`**；2026届 → `2025-2026`。OD 与 ima 同学年文件夹名必须一字对齐；ima 缺该学年文件夹时先 `create_folder` 再建再传。无法从卷名/路径可靠读出届别时，停该文件、列入报告，不猜年。

## Steps

1. **两侧盘点**
   - OneDrive（personal 连接器）：打开用户资料根下 `{{ONEDRIVE_TEACHING_ROOT}}`，按上节映射递归列出对应树。
   - ima：对目标知识库用 OpenAPI `get_knowledge_list` 分页拉全量（`limit`≤50、cursor；`media_type=99` 为文件夹，其 `media_id` 即 `folder_id`）。Base：`https://ima.qq.com/openapi/wiki/v1/`；请求头变量名：`ima-openapi-clientid` / `ima-openapi-apikey`（从环境变量读取，禁止在技能或聊天打印真实值）。

2. **对齐与判新**
   - OneDrive 为权威源；按**同学年 / 同路径叶子文件名**比对。
   - 学年归类见上节；学年文件夹名必须两边一字对齐；ima 缺对应学年或子文件夹则先 `create_folder`（父级字段名是 `folder_id`，不是 `parent_folder_id`），再建再传。
   - 已存在：同名（忽略扩展名差异、轻微空白/标点差异）→ 视为已有，不传。
   - 疑似近重复但文件名明显不同 → **不上传**，只进报告待用户判断。

3. **过滤**
   - 跳过全部 `.zip` / `.rar` 等压缩包与 `.html` / `.htm`：不上传，只列报告。

4. **入 ima（只增）**
   - 仅上传「OD 有、ima 同学年路径无」的文件；目标路径必须落在正确学年文件夹下（如 2027届 → `…/2026-2027/…`）。
   - 单文件三步：`create_media` → COS 上传（临时凭证，勿落盘打印）→ `add_knowledge`（带目标 `folder_id`）。上传前可 `check_repeated_names`；若同文件夹已重复，**默认停该文件并记报告**（不要擅自加时间戳改名，除非用户当场要求）。

5. **成功确认**
   - 每个新文件：`add_knowledge` 成功码，并记下 `media_id`、最终 title、ima 路径（含学年文件夹）。
   - 可选：再 `get_knowledge_list` 抽查目标文件夹是否出现该 title。

6. **善后通知**
   - **有成功新上传**：立刻 SendToAgent（priority true）→「知识库索引Bot」，每条含 title、存储路径、media_id、卷/答关系线索（便于填索引列：试卷名称｜试卷类型｜试卷文件｜答案文件｜存储路径｜备注）。本 bot **不**往 ima 写索引 CSV/xlsx。
   - **三段皆一致且无跳过、无新文件**：只给用户一句「本周三段一致」；**不**叫醒索引Bot。
   - 用户侧报告四块：已复制清单与落点｜跳过的 zip/html｜近重复待判｜错误/断点。

## Stop conditions

- OneDrive 连接器未授权或 list/download 失败 → 停，告知用户重连 OneDrive。
- ima 环境变量缺失、401/403、或连续不可恢复 API 错误 → 停，告知检查/更新 API key（勿打印密钥）。
- 对不上学年文件夹、读不出届别、或无法安全判定应对齐哪一层 → 停该支路/该文件，列入报告，不猜传。
- COS / `add_knowledge` 卡住或反复 429/5xx 超重试 → 停该文件及后续同批高风险上传；已成功的仍记报告并按规则通知索引Bot。
- 若出现登录/人机验证墙（浏览器旁路）→ 停，交回用户；主路径应是连接器 + OpenAPI，不默认浏览器。

## Keep out of this skill

某次具体试卷文件名、临时 softid/COS 凭证、某次 comparison 快照路径；具体 kb_id、folder_id、OneDrive item id、队友 agent id、API 密钥；近重复是否导入、是否改名消重、是否扩到真题/电子教材、是否解压 zip 再导等需用户当场拍板的事；周一 cron 时刻与当周日期文案。
