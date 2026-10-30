#!/usr/bin/env python3
"""Anti-slop lint for generated PRD / AGENTS / playbook markdown. Exit 1 on any finding."""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")
FILL_ME = re.compile(r"\[(?:Quantify|Lock|Explain|Exact|Step-by-step|Describe|Insert|Fill)[^\]]*\]", re.I)
TODO = re.compile(r"\b(TBD|TODO|FIXME|lorem ipsum|to be decided)\b", re.I)
FLUFF = re.compile(
    r"\b(enterprise-grade|cutting-edge|state-of-the-art|revolutionary|game-chang\w+|seamless(?:ly)?|"
    r"world-class|best-in-class|next-gen(?:eration)?|military-grade|bulletproof|blazing[- ]fast|unparalleled)\b",
    re.I,
)
NUMBER_CLAIM = re.compile(r"(?:\d[\d,.]*\s?(?:%|ms\b|µs|×|x\b)|\$\s?\d)")
TAG = re.compile(r"\[(?:TARGET|MEASURED|SOURCE|ASSUMPTION|UNVERIFIED|OPEN)\b")
FENCE = re.compile(r"^\s*(```|~~~)")
DEF_NAME = re.compile(r"\bdef\s+(\w+)\s*\(")
TARGET_LINE = re.compile(r"\*\*Target File\(s\)\*\*:\s*(.+)")


def prose_lines(text: str):
    fence = None
    for i, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            continue
        if fence is None:
            yield i, line


def lint_file(path: Path) -> list[tuple[int, str]]:
    text = path.read_text(encoding="utf-8")
    out: list[tuple[int, str]] = []
    for i, line in prose_lines(text):
        if PLACEHOLDER.search(line):
            out.append((i, "unreplaced {{placeholder}}"))
        if FILL_ME.search(line):
            out.append((i, "bracketed fill-me prompt left in text"))
        if TODO.search(line):
            out.append((i, "TBD/TODO/FIXME marker"))
        if FLUFF.search(line):
            out.append((i, f"fluff word: {FLUFF.search(line).group(0)}"))
        stripped = line.strip()
        if stripped.startswith("#") or re.fullmatch(r"[|\s:\-]+", stripped or "-"):
            continue
        if NUMBER_CLAIM.search(line) and not TAG.search(line):
            out.append((i, "numeric claim without an evidence tag"))
    name = path.name
    if re.match(r"PRD_\d+", name):
        for n in range(1, 6):
            if not re.search(rf"^##\s+{n}\.", text, re.M):
                out.append((0, f"missing section '## {n}.'"))
    if re.match(r"AGENTS_\d+", name):
        for n in (1, 2):
            if not re.search(rf"^##\s+{n}\.", text, re.M):
                out.append((0, f"missing section '## {n}.'"))
    return out


def check_signatures(prd: Path, root: Path) -> list[tuple[int, str]]:
    text = prd.read_text(encoding="utf-8")
    m = TARGET_LINE.search(text)
    if not m:
        return []
    out: list[tuple[int, str]] = []
    wanted = set(DEF_NAME.findall("\n".join(l for _, l in prose_lines(text))))
    for target in re.findall(r"`([^`]+\.py)`", m.group(1)):
        tp = root / target
        if not tp.is_file():
            continue
        try:
            tree = ast.parse(tp.read_text(encoding="utf-8"))
        except SyntaxError as e:
            out.append((0, f"{target}: syntax error line {e.lineno}"))
            continue
        have = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for name in sorted(wanted - have):
            out.append((0, f"{target}: PRD names `{name}()` but it is not defined"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("folder")
    ap.add_argument("--check-signatures", action="store_true")
    ap.add_argument("--root", default=".", help="project root for --check-signatures")
    a = ap.parse_args()

    files = sorted(Path(a.folder).rglob("*.md"))
    total = 0
    for f in files:
        findings = lint_file(f)
        if a.check_signatures and re.match(r"PRD_\d+", f.name):
            findings += check_signatures(f, Path(a.root))
        for line, msg in findings:
            print(f"{f}:{line or '-'}: {msg}")
        total += len(findings)
    print(f"[prd_lint] {len(files)} file(s), {total} finding(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()