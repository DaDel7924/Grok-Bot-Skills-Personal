---
name: 学科网云南高三化学取卷
description: >-
  Use when monitoring or manually fetching Yunnan senior-year chemistry papers
  from 学科网 (zxxk), unzipping with GBK, renaming, and uploading to the fixed
  OneDrive folder.
---
# 学科网云南高三化学取卷

Reusable steps for fetching **云南 · 高三 · 化学试卷** from 学科网. Keep rolling state (current softid boundary, schedule, vault item ids) in memory or the routine—not in this skill.

## Helper scripts (prefer these for mechanical steps)

Scripts live next to this skill:

`/home/box/agent-data/workflows/skill-1793518670469/scripts/`

- **softid boundary**: `python3 …/scripts/softid_filter.py --boundary <N> --json --ids <id>…`  
  Only process `newer`; after successes, raise boundary toward `new_boundary_if_all_ok` (failed items do not advance past themselves).
- **GBK unzip**: `python3 …/scripts/unzip_gbk.py <zip> -o <outdir>`  
  Repairs Chinese filenames; use `--dry-run` to list names only.
- **Rename**: `python3 …/scripts/rename_papers.py <outdir> --school <校名> --session <届次学期次数> [--apply]`  
  Dry-run by default; with `--apply` writes `{学校}{session}试卷.pdf` / `{学校}{session}试卷答案.pdf`.

Browser login, download, duplicate judgment, and OneDrive upload stay with the bot; scripts only cover filter / unpack / rename.

## When to use

- Scheduled patrol finds a new softid on the Yunnan G12 chemistry papers list, or
- The user asks to fetch / backfill a paper with this fixed pipeline.

## Steps

1. Open 学科网. If login is needed, use sso.zxxk.com with the saved Vault login. On hx pages, complete the Aliyun slider captcha when it appears—**drag inside the page/slider widget**; a whole-desktop drag may miss the knob.
2. Confirm subject is **高中化学**, open the **试卷** tab.
3. Open the filtered list (region Yunnan, grade 高三; verified list shape like `https://hx.zxxk.com/h/papers-type4105-g12/area530000/`), sort by **最新**.
4. **softid boundary**: run `softid_filter.py` against the current boundary from memory/routine; only process returned `newer` ids. Do not hardcode the boundary number in this skill.
5. Open each paper page and download to the box using 网校通 free entitlement. List pages may load while logged out; **download requires login**—sign in first if needed. The download may be a zip, a single PDF, or a Word (docx) file. **If the page offers a 「精品解析版」, prefer that download over the plain 试题/答案版.**
6. Unpack: for a zip, run `unzip_gbk.py` into a per-softid folder. Identify 试卷 / 答案. If one PDF holds both paper and answer, split it at the page where the 参考答案 starts.
7. **Duplicate check**: before uploading, compare with the previously fetched paper(s) (e.g. same school/exam, identical objective-question answer key). If it is the same paper as one already uploaded, do not upload again; report it as a duplicate.
8. Rename with `rename_papers.py` (`--school` / `--session` from listing title and file content; never invent). Review dry-run output, then `--apply`.
9. Upload to OneDrive folder `文档/教案/高考专项/学科网试卷获取bot` via the OneDrive connector / UploadFile (do not rely on onedrive.live.com web upload from the box).
10. **Move the boundary right away**: as soon as a paper is handled successfully (uploaded, or confirmed duplicate), make the largest such softid the new boundary (in memory and the routine). Then re-check the list from that new boundary to see whether anything even newer appeared; process any found the same way, and repeat until nothing above the boundary remains. A failed item does not move the boundary past it. `softid_filter.py`’s `new_boundary_if_all_ok` is a proposal only after the batch’s successes.
11. Notify the user in this chat when something uploaded successfully. On a quiet scheduled run with no new papers, stay silent.

## Handoff fields (when notifying)

Include when useful: softid, original site title, renamed paper filename, renamed answer filename, OneDrive folder path above, new boundary softid, duplicates skipped, short note (e.g. 仅试题+答案 PDF / 精品解析版). SendToAgent to 高三试卷知识库Bot only if the user or a routine asked for that handoff.

## Stop conditions

Before download, confirm logged-in state. On login failure, captcha stuck, paywall/no entitlement, missing paper or answer, or OneDrive upload failure: stop that item, tell the user which step failed, do not invent alternate paths, do not retry endlessly. Do not change passwords or bypass captcha beyond the normal in-page drag.

## Keep out of this skill

Current softid boundary value; Tue/Fri ~09:00 Asia/Shanghai schedule and “silent if no new papers”; Vault login entry and OneDrive item ids; team naming / model routing / weekly journal standing tasks.
