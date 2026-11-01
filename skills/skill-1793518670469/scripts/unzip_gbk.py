#!/usr/bin/env python3
"""Unzip an archive; fix Chinese filenames that were stored as GBK/CP936."""
from __future__ import annotations

import argparse
import re
import sys
import zipfile
from pathlib import Path

CJK = re.compile(r"[\u4e00-\u9fff]")


def gbk_from_zip_name(filename: str) -> str | None:
    try:
        raw = filename.encode("cp437")
    except UnicodeEncodeError:
        return None
    for enc in ("gbk", "cp936", "gb18030"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return None


def repair_name(filename: str, flag_bits: int) -> str:
    """Return a usable relative path name."""
    candidate = gbk_from_zip_name(filename)
    utf8_flag = bool(flag_bits & 0x800)
    if candidate and CJK.search(candidate):
        # Prefer GBK repair when it yields Chinese (even if UTF-8 flag was set wrongly).
        if (not utf8_flag) or (not CJK.search(filename)) or (filename != candidate):
            # If original already has CJK and equals candidate, keep it.
            if CJK.search(filename) and filename == candidate:
                return filename
            if not CJK.search(filename) and CJK.search(candidate):
                return candidate
            if CJK.search(candidate) and not utf8_flag:
                return candidate
            if CJK.search(candidate) and CJK.search(filename) is None:
                return candidate
    if candidate and not CJK.search(filename) and CJK.search(candidate):
        return candidate
    # Fallbacks
    if candidate and not utf8_flag:
        return candidate
    return filename


def main() -> int:
    p = argparse.ArgumentParser(description="Unzip with GBK filename repair")
    p.add_argument("zip_path", type=Path)
    p.add_argument("-o", "--out", type=Path, required=True, help="output directory")
    p.add_argument("--dry-run", action="store_true", help="list names only, do not extract")
    args = p.parse_args()

    if not args.zip_path.is_file():
        print(f"missing zip: {args.zip_path}", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    with zipfile.ZipFile(args.zip_path) as zf:
        for info in zf.infolist():
            if info.is_dir():
                continue
            name = repair_name(info.filename, info.flag_bits)
            name = name.replace("\\", "/").lstrip("/")
            parts = [x for x in name.split("/") if x not in ("", ".", "..")]
            if not parts:
                continue
            rel = "/".join(parts)
            target = args.out.joinpath(*parts)
            if args.dry_run:
                print(rel)
                written.append(rel)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, open(target, "wb") as dst:
                dst.write(src.read())
            written.append(rel)
            print(rel)

    print(f"# extracted={len(written)} out={args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
