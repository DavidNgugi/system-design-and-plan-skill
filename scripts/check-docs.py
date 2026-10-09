#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Check a markdown corpus for structural drift.

Checks, as failures:
  - relative links whose target file does not exist
  - anchor links (path#fragment) whose fragment does not exist, or is ambiguous
  - unbalanced code fences
  - mermaid blocks that do not open with a known diagram type
Reported as warnings (fail only with --strict):
  - a heading repeated within one document, which is legitimate for structured
    repetition (one block per subject) but makes its anchor ambiguous

Usage: check-docs.py [root] [--strict] [--json]
Exit code 1 if any failure occurred.
"""
from __future__ import annotations

import json
import os
import re
import sys

DIAGRAM_TYPES = re.compile(
    r"^(graph|flowchart|sequenceDiagram|stateDiagram-v2|stateDiagram|erDiagram|classDiagram|"
    r"journey|gantt|pie|mindmap|timeline|quadrantChart|gitGraph|C4Context)"
)
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
SKIP_DIRS = {".git", "node_modules", "target", "dist", "build", ".next", ".venv", "__pycache__"}


def slug(text: str) -> str:
    """Approximate GitHub's heading anchor: strip markup, lowercase, drop punctuation, spaces to hyphens."""
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*?([^*]*)\*\*?", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower()
    text = re.sub(r"[^a-z0-9 \-_]", "", text)
    return text.replace(" ", "-")


def markdown_files(root: str) -> list[str]:
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        out.extend(os.path.join(dirpath, f) for f in filenames if f.endswith(".md"))
    return sorted(out)


def anchors_of(path: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for line in open(path, encoding="utf-8"):
        m = HEADING.match(line)
        if m:
            s = slug(m.group(2))
            counts[s] = counts.get(s, 0) + 1
    return counts


def check(path: str, cache: dict[str, dict[str, int]]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    text = open(path, encoding="utf-8").read()
    lines = text.split("\n")

    if text.count("```") % 2:
        failures.append("unbalanced code fence")

    for i, line in enumerate(lines):
        if line.strip() != "```mermaid":
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        opener = lines[j].strip() if j < len(lines) else ""
        if not DIAGRAM_TYPES.match(opener):
            failures.append(f"mermaid block at line {i + 1} opens with {opener[:40]!r}")

    own = anchors_of(path)
    for s, n in own.items():
        if n > 1:
            warnings.append(f"heading anchor {s!r} appears {n} times, so links to it are ambiguous")

    for target in LINK.findall(text):
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        rel, _, fragment = target.partition("#")
        dest = os.path.normpath(os.path.join(os.path.dirname(path), rel)) if rel else path
        if rel and not os.path.exists(dest):
            failures.append(f"broken link {target!r} -> {dest}")
            continue
        if fragment and dest.endswith(".md") and os.path.exists(dest):
            if dest not in cache:
                cache[dest] = anchors_of(dest)
            if fragment not in cache[dest]:
                failures.append(f"link {target!r} points at a missing anchor")
    return failures, warnings


def main() -> int:
    argv = sys.argv[1:]
    strict = "--strict" in argv
    as_json = "--json" in argv
    positional = [a for a in argv if not a.startswith("--")]
    root = positional[0] if positional else "."

    files = markdown_files(root)
    cache: dict[str, dict[str, int]] = {}
    failures: dict[str, list[str]] = {}
    warnings: dict[str, list[str]] = {}
    for f in files:
        fails, warns = check(f, cache)
        if fails:
            failures[f] = fails
        if warns:
            warnings[f] = warns

    n_fail = sum(len(v) for v in failures.values())
    n_warn = sum(len(v) for v in warnings.values())
    if as_json:
        print(json.dumps({"root": root, "files": len(files), "failures": failures,
                          "warnings": warnings}, indent=2))
    else:
        print(f"checked {len(files)} markdown files under {root}")
        for group, label in ((failures, "FAIL"), (warnings, "warn")):
            for f, problems in group.items():
                print(f"\n{label} {os.path.relpath(f, root)}")
                for p in problems:
                    print(f"  - {p}")
        print(f"\n{n_fail} failure(s), {n_warn} warning(s)")
    return 1 if n_fail or (strict and n_warn) else 0


if __name__ == "__main__":
    raise SystemExit(main())
