#!/usr/bin/env python3
"""Propose/apply rename for 试卷/答案 PDFs under a folder."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path


ANSWER_HINT = re.compile(r"(答案|参考答案|解析)", re.I)
PAPER_HINT = re.compile(r"(试卷|试题)", re.I)


def classify(path: Path) -> str:
    name = path.stem
    if ANSWER_HINT.search(name):
        return "answer"
    if PAPER_HINT.search(name):
        return "paper"
    # fallback by order later
    return "unknown"


def main() -> int:
    p = argparse.ArgumentParser(description="Rename paper/answer PDFs")
    p.add_argument("folder", type=Path)
    p.add_argument("--school", required=True)
    p.add_argument("--session", required=True, help="e.g. 2027届高三上第二次月考")
    p.add_argument("--apply", action="store_true", help="actually rename; default dry-run")
    p.add_argument("--ext", default=".pdf", help="file extension to consider")
    args = p.parse_args()

    if not args.folder.is_dir():
        print(f"missing folder: {args.folder}", file=sys.stderr)
        return 1

    files = sorted(
        [f for f in args.folder.rglob(f"*{args.ext}") if f.is_file()],
        key=lambda x: x.name,
    )
    if not files:
        print("no matching files", file=sys.stderr)
        return 2

    papers = [f for f in files if classify(f) == "paper"]
    answers = [f for f in files if classify(f) == "answer"]
    unknown = [f for f in files if classify(f) == "unknown"]

    # If only two unknowns, treat first as paper, second as answer by size name
    if not papers and not answers and len(unknown) == 2:
        papers, answers, unknown = [unknown[0]], [unknown[1]], []
    elif not papers and unknown:
        papers, unknown = [unknown[0]], unknown[1:]
    if not answers and unknown:
        answers, unknown = [unknown[0]], unknown[1:]

    base = f"{args.school}{args.session}"
    mapping: list[tuple[Path, Path]] = []
    if papers:
        mapping.append((papers[0], args.folder / f"{base}试卷{args.ext}"))
    if answers:
        mapping.append((answers[0], args.folder / f"{base}试卷答案{args.ext}"))

    if not mapping:
        print("could not classify paper/answer", file=sys.stderr)
        return 3

    for src, dst in mapping:
        action = "rename" if args.apply else "would_rename"
        print(f"{action}: {src.name} -> {dst.name}")
        if args.apply and src.resolve() != dst.resolve():
            if dst.exists():
                print(f"target exists, skip: {dst}", file=sys.stderr)
                continue
            shutil.move(str(src), str(dst))

    for u in unknown:
        print(f"left_unknown: {u.name}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
