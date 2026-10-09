#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Count tasks and sum estimates from a markdown task backlog, then roll up by epic, phase and tier.

Conventions expected in the backlog:
  - rows like  | PFX-E12-03 | description | acceptance | deps | M |
  - the epic is the numeric group in the id (E12); the task is the trailing number
  - one estimate token from the scale below, in any cell of the row

Usage:
  backlog-stats.py docs/TASKS.md
  backlog-stats.py docs/TASKS.md --phases "0:0-4,1:5-9,6:30-31"
  backlog-stats.py docs/TASKS.md --core "1:1-13,3:1-10" --contingency 0.3
  backlog-stats.py docs/TASKS.md --json
Both "--flag value" and "--flag=value" are accepted.
"""
from __future__ import annotations

import json
import re
import sys

SCALE = {"XS": 0.5, "S": 1.0, "M": 2.5, "L": 4.5, "XL": 8.0}
ID = re.compile(r"^\|\s*([A-Za-z]{2,6})-E(\d+)-(\d+)\s*\|")


def parse(path: str) -> dict[tuple[int, int], float]:
    tasks: dict[tuple[int, int], float] = {}
    for line in open(path, encoding="utf-8"):
        m = ID.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        estimates = [c for c in cells if c in SCALE]
        if estimates:
            tasks[(int(m.group(2)), int(m.group(3)))] = SCALE[estimates[-1]]
    return tasks


def parse_spec(spec: str) -> dict[int, list[tuple[int, int]]]:
    """'0:0-4,1:5-9' -> {0: [(0,4)], 1: [(5,9)]}; accepts ';' for extra ranges in one group."""
    out: dict[int, list[tuple[int, int]]] = {}
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        group, _, ranges = part.partition(":")
        for rng in ranges.split(";"):
            lo, _, hi = rng.partition("-")
            out.setdefault(int(group), []).append((int(lo), int(hi or lo)))
    return out


def in_spec(epic: int, task: int, spec: dict[int, list[tuple[int, int]]]) -> bool:
    return epic in spec and any(lo <= task <= hi for lo, hi in spec[epic])


def group(keys: list[tuple[int, int]], tasks: dict[tuple[int, int], float]) -> dict[str, float]:
    days = sum(tasks[k] for k in keys)
    return {"tasks": len(keys), "ideal_days": round(days, 1)}


def main() -> int:
    argv = sys.argv[1:]
    flags: dict[str, str] = {}
    positional: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--"):
            if "=" in a:
                k, v = a[2:].split("=", 1)
                flags[k] = v
            elif i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                flags[a[2:]] = argv[i + 1]
                i += 1
            else:
                flags[a[2:]] = "true"
        else:
            positional.append(a)
        i += 1

    path = positional[0] if positional else "docs/TASKS.md"
    tasks = parse(path)
    if not tasks:
        print(f"no task rows found in {path} (expected rows like '| PFX-E12-03 | ... | M |')")
        return 1

    by_epic: dict[int, list[tuple[int, int]]] = {}
    for key in tasks:
        by_epic.setdefault(key[0], []).append(key)

    result: dict[str, object] = {
        "file": path,
        **group(list(tasks), tasks),
        "epics": {f"E{e}": group(v, tasks) for e, v in sorted(by_epic.items())},
    }

    if flags.get("phases"):
        result["phases"] = {
            f"phase {g}": group([k for k in tasks if any(lo <= k[0] <= hi for lo, hi in r)], tasks)
            for g, r in sorted(parse_spec(flags["phases"]).items())
        }

    if flags.get("core"):
        core = parse_spec(flags["core"])
        keys = [k for k in tasks if in_spec(k[0], k[1], core)]
        contingency = float(flags.get("contingency", 0.3))
        days = sum(tasks[k] for k in keys)
        result["core"] = {
            **group(keys, tasks),
            "contingency": contingency,
            "budgeted_with_contingency": round(days * (1 + contingency), 1),
        }

    if flags.get("json"):
        print(json.dumps(result, indent=2))
        return 0

    print(f"{path}: {result['tasks']} tasks / {result['ideal_days']} ideal days")
    for epic, v in result["epics"].items():  # type: ignore[union-attr]
        print(f"  {epic:>5}  {v['tasks']:>3} tasks  {v['ideal_days']:>6} d")
    for phase, v in result.get("phases", {}).items():  # type: ignore[union-attr]
        print(f"  {phase:>10}  {v['tasks']:>3} tasks  {v['ideal_days']:>6} d")
    if "core" in result:
        c = result["core"]  # type: ignore[assignment]
        print(f"  CORE  {c['tasks']} tasks / {c['ideal_days']} d -> "
              f"budgeted {c['budgeted_with_contingency']} d (+{int(c['contingency'] * 100)}%)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
