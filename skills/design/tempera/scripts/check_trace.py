#!/usr/bin/env python3
"""Check coverage of a tempera trace.json.

Usage: python3 check_trace.py trace.json [--root PROJECT_DIR]

Errors (exit 1): duplicate ids, Must requirement without story, story without
board (unless "no_board"), unknown references, board file missing under --root.
Warnings: board that belongs to no story (unless "support": true), unused
requirement that is not Must.
"""
import argparse
import json
import sys
from pathlib import Path


def ids(items, kind, errors):
    seen = set()
    for item in items:
        i = item.get("id")
        if not i:
            errors.append(f"{kind}: item without id: {item}")
        elif i in seen:
            errors.append(f"{kind}: duplicate id {i}")
        seen.add(i)
    return seen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("trace")
    ap.add_argument("--root", help="project dir; board files are searched recursively here")
    a = ap.parse_args()

    t = json.loads(Path(a.trace).read_text(encoding="utf-8"))
    errors, warnings = [], []

    reqs = t.get("requirements", [])
    stories = t.get("stories", [])
    flows = t.get("flows", [])
    boards = t.get("boards", [])
    slides = t.get("slides", [])

    req_ids = ids(reqs, "requirement", errors)
    story_ids = ids(stories, "story", errors)
    ids(flows, "flow", errors)
    ids(slides, "slide", errors)
    # boards may repeat the same id once per language; key on (id, lang)
    board_ids = {b.get("id") for b in boards if b.get("id")}
    seen_bl = set()
    for b in boards:
        key = (b.get("id"), b.get("lang"))
        if not b.get("id"):
            errors.append(f"board: item without id: {b}")
        elif key in seen_bl:
            errors.append(f"board: duplicate id {key[0]} (lang {key[1]})")
        seen_bl.add(key)

    covered_reqs, boards_in_stories = set(), set()
    for s in stories:
        for r in s.get("requirements", []):
            if r not in req_ids:
                errors.append(f"story {s['id']}: unknown requirement {r}")
            covered_reqs.add(r)
        sb = s.get("boards", [])
        if not sb and not s.get("no_board"):
            errors.append(f"story {s['id']}: no board (add one or \"no_board\": \"reason\")")
        for b in sb:
            if b not in board_ids:
                errors.append(f"story {s['id']}: unknown board {b}")
            boards_in_stories.add(b)

    for r in reqs:
        if r["id"] in covered_reqs:
            continue
        if str(r.get("moscow", "")).lower() == "must":
            errors.append(f"requirement {r['id']} (Must): no story")
        elif str(r.get("moscow", "")).lower() != "won't":
            warnings.append(f"requirement {r['id']}: no story")

    for f in flows:
        steps = f.get("steps", [])
        if not steps:
            errors.append(f"flow {f['id']}: no steps")
        for n, st in enumerate(steps, 1):
            if st.get("board") not in board_ids:
                errors.append(f"flow {f['id']} step {n}: unknown board {st.get('board')}")
            if st.get("do") and not st.get("expect"):
                warnings.append(f"flow {f['id']} step {n}: action without expect")

    for sl in slides:
        for b in sl.get("boards", []):
            if b not in board_ids:
                errors.append(f"slide {sl['id']}: unknown board {b}")

    for b in boards:
        if b.get("id") not in boards_in_stories and not b.get("support"):
            warnings.append(f"board {b.get('id')}: in no story (or mark \"support\": true)")

    if a.root:
        root = Path(a.root)
        names = {p.name for p in root.rglob("*") if p.is_file()}
        for b in boards:
            fname = b.get("file")
            if not fname:
                errors.append(f"board {b.get('id')}: no file")
            elif Path(fname).name not in names:
                errors.append(f"board {b.get('id')}: file not found under root: {fname}")

    print(f"requirements {len(reqs)} · stories {len(stories)} · flows {len(flows)} · "
          f"boards {len(boards)} · slides {len(slides)}")
    for w in warnings:
        print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print("OK" if not errors else f"FAILED: {len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
