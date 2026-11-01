#!/usr/bin/env python3
"""Filter softids strictly greater than a boundary; optionally propose new boundary."""
from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    p = argparse.ArgumentParser(description="Filter softids > boundary")
    p.add_argument("--boundary", type=int, required=True, help="current softid boundary")
    p.add_argument(
        "--ids",
        nargs="*",
        type=int,
        help="softids to filter (or pass JSON array on stdin)",
    )
    p.add_argument("--json", action="store_true", help="print JSON result")
    args = p.parse_args()

    if args.ids is not None and len(args.ids) > 0:
        ids = list(args.ids)
    else:
        raw = sys.stdin.read().strip()
        if not raw:
            ids = []
        else:
            data = json.loads(raw)
            if isinstance(data, dict) and "ids" in data:
                ids = [int(x) for x in data["ids"]]
            elif isinstance(data, list):
                ids = [int(x) for x in data]
            else:
                raise SystemExit("stdin must be a JSON list or {\"ids\":[...]}")

    newer = sorted({i for i in ids if i > args.boundary})
    skipped = sorted({i for i in ids if i <= args.boundary})
    new_boundary = max(newer) if newer else args.boundary
    out = {
        "boundary": args.boundary,
        "newer": newer,
        "skipped": skipped,
        "new_boundary_if_all_ok": new_boundary,
        "count_newer": len(newer),
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"boundary={args.boundary}")
        print(f"newer={','.join(map(str, newer)) or '(none)'}")
        print(f"skipped={','.join(map(str, skipped)) or '(none)'}")
        print(f"new_boundary_if_all_ok={new_boundary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
