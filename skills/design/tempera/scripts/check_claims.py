#!/usr/bin/env python3
"""Check that factual values in a tempera package are registered in claims.json.

Usage: python3 check_claims.py claims.json PROJECT_DIR [--warn-only]

Scans visible text of .html/.md/.txt files (and .json files other than
claims.json/trace.json) for money, percent and magnitude values, e.g.
"€ 4,99", "US$ 300 mil", "25%", "1,2 mi", "4.6M". Each must match a value
listed in some claim's "values" (or in "ignore"). Also validates the registry:
verified claims need source and date; status must be verified|hypothesis|open.
Exit 1 on errors.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

CUR = r"(?:US\$|R\$|€|\$|£|EUR|USD|BRL)"
NUM = r"\d+(?:[.,\s]\d{3})*(?:[.,]\d+)?"
MAG = r"(?:mil|mi|bi|tri|k|K|M|Mio\.?|Mrd\.?|bn|million|billion|thousand)\b"
PATTERNS = [
    rf"{CUR}\s?{NUM}(?:\s?{MAG})?",   # € 4,99 · US$ 300 mil
    rf"{NUM}\s?{CUR}",                # 4,99 € · 173 €
    rf"{NUM}\s?%",                    # 25% · 3 %
    rf"{NUM}\s?{MAG}",                # 1,2 mi · 4.6M · 300 mil
]
VALUE_RE = re.compile("|".join(f"(?:{p})" for p in PATTERNS))
STRIP_BLOCKS = re.compile(r"<(script|style|helmet)\b.*?</\1>", re.S | re.I)
TAGS = re.compile(r"<[^>]+>")
SKIP_JSON = {"claims.json", "trace.json", "package.json", "canvas.json", "deck.json"}


def norm(v):
    v = v.replace(" ", " ").replace(" ", " ")
    v = re.sub(r"\s+", "", v).lower()
    return v.rstrip(".")


def visible_text(path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix == ".html":
        raw = STRIP_BLOCKS.sub(" ", raw)
        raw = TAGS.sub(" ", raw)
        raw = html.unescape(raw)
    elif path.suffix == ".json":
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return raw
        out = []

        def walk(x):
            if isinstance(x, str):
                out.append(x)
            elif isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
        walk(data)
        raw = "\n".join(out)
    return raw


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("claims")
    ap.add_argument("root")
    ap.add_argument("--warn-only", action="store_true", help="report unregistered values as warnings")
    a = ap.parse_args()

    reg = json.loads(Path(a.claims).read_text(encoding="utf-8"))
    errors, warnings = [], []
    known = set()
    for c in reg.get("claims", []):
        cid = c.get("id", "?")
        st = c.get("status")
        if st not in {"verified", "hypothesis", "open"}:
            errors.append(f"claim {cid}: status must be verified|hypothesis|open (got {st!r})")
        if st == "verified" and not (c.get("source") and c.get("date")):
            errors.append(f"claim {cid}: verified without source and date")
        if not c.get("values"):
            warnings.append(f"claim {cid}: no values listed (cannot be matched in content)")
        for v in c.get("values", []):
            known.add(norm(v))
    for v in reg.get("ignore", []):
        known.add(norm(v))
    for p in reg.get("people", []):
        if not p.get("source"):
            errors.append(f"person {p.get('name', '?')}: no source")

    root = Path(a.root)
    files = [p for p in root.rglob("*")
             if p.is_file() and p.suffix in {".html", ".md", ".txt", ".json"}
             and p.name not in SKIP_JSON and "node_modules" not in p.parts]
    unregistered = {}
    for f in sorted(files):
        for m in VALUE_RE.finditer(visible_text(f)):
            val = re.sub(r"\s+", " ", m.group(0).replace(" ", " ").replace(" ", " ")).strip()
            if norm(val) not in known:
                unregistered.setdefault(val, set()).add(str(f.relative_to(root)))

    for val, where in sorted(unregistered.items()):
        msg = f"unregistered value {val!r} in {', '.join(sorted(where)[:5])}" + \
              (f" (+{len(where) - 5} more)" if len(where) > 5 else "")
        (warnings if a.warn_only else errors).append(msg)

    n = len(reg.get("claims", []))
    by = {s: sum(1 for c in reg.get("claims", []) if c.get("status") == s)
          for s in ("verified", "hypothesis", "open")}
    print(f"claims {n} (verified {by['verified']}, hypothesis {by['hypothesis']}, open {by['open']}) · "
          f"files scanned {len(files)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print("OK" if not errors else f"FAILED: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
