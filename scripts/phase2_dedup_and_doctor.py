#!/usr/bin/env python3
"""Hackathon Backend King v3.0 Phase 2 AST Doctor, Same-Folder Deduplicator & Gate Auditor."""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PRUNE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", "_incoming", "_backups", "_duplicates_archive", "dist", "build"}
CLUTTER_DIRS = {"__MACOSX", ".grok"}
PROTECTED_FILES = {"__init__.py", ".gitkeep", "package-lock.json", "requirements.lock", "contract.lock", "LICENSE"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_stub_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    stmts = list(node.body)
    if stmts and isinstance(stmts[0], ast.Expr) and isinstance(getattr(stmts[0], "value", None), ast.Constant) and isinstance(stmts[0].value.value, str):
        stmts = stmts[1:]
    if not stmts:
        return True
    if len(stmts) > 1:
        return False
    s = stmts[0]
    if isinstance(s, ast.Pass):
        return True
    if isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and s.value.value is Ellipsis:
        return True
    if isinstance(s, ast.Return) and (s.value is None or isinstance(s.value, ast.Constant)):
        return True
    if isinstance(s, ast.Raise):
        exc = s.exc
        if isinstance(exc, ast.Name) and exc.id == "NotImplementedError":
            return True
        if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == "NotImplementedError":
            return True
    return False


def scan_duplicates(root: Path, apply: bool) -> dict[str, int]:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    copy_re = re.compile(r"^(.+?)\s*\(\d+\)(\.[^.]+)$")
    stats = {"clutter_dirs": 0, "same_folder_copies": 0}

    for dirpath, dirnames, filenames in os.walk(root):
        for d in list(dirnames):
            if d in CLUTTER_DIRS:
                src = Path(dirpath) / d
                rel = src.relative_to(root)
                dst = root / "_duplicates_archive" / stamp / rel
                print(f"  [{'ARCHIVE-DIR' if apply else 'REPORT-CLUTTER-DIR'}] {rel}")
                if apply:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                dirnames.remove(d)
                stats["clutter_dirs"] += 1
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]

        folder = Path(dirpath)
        for fname in sorted(filenames):
            if fname in PROTECTED_FILES:
                continue
            m = copy_re.match(fname)
            if not m:
                continue
            canonical = folder / f"{m.group(1)}{m.group(2)}"
            dup = folder / fname
            if canonical.is_file() and sha256_file(canonical) == sha256_file(dup):
                rel = dup.relative_to(root)
                dst = root / "_duplicates_archive" / stamp / rel
                print(f"  [{'ARCHIVE-COPY' if apply else 'REPORT-DUP-COPY'}] {rel} (identical to {canonical.name})")
                if apply:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dup), str(dst))
                stats["same_folder_copies"] += 1
    return stats


def audit_python_modules(root: Path) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    py_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        for f in sorted(filenames):
            if f.endswith(".py"):
                py_files.append(Path(dirpath) / f)

    for py in sorted(py_files):
        rel = py.relative_to(root).as_posix()
        text = py.read_text(encoding="utf-8", errors="replace")
        stub_funcs: list[str] = []
        total_funcs = 0
        status = "READY"
        notes: list[str] = []

        try:
            tree = ast.parse(text, filename=rel)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total_funcs += 1
                    if is_stub_function(node):
                        stub_funcs.append(node.name)
        except SyntaxError as e:
            status = "SYNTAX_ERROR"
            notes.append(f"line {e.lineno}: {e.msg}")

        if stub_funcs and status != "SYNTAX_ERROR":
            status = "STUB"
            notes.append(f"stub functions: {', '.join(stub_funcs)}")
        elif re.search(r"\b(TODO|FIXME)\b", text) and status == "READY":
            status = "NEEDS_MUSCLE"
            notes.append("contains TODO/FIXME")

        slug = py.stem
        has_test = (root / "tests" / f"test_{slug}.py").is_file()
        row = {
            "file": rel,
            "status": status,
            "total_functions": total_funcs,
            "stub_functions": stub_funcs,
            "has_unit_test": has_test,
            "notes": "; ".join(notes) if notes else "AST complete",
        }
        results.append(row)
        print(f"  [{status:12s}] {rel:36s} | funcs={total_funcs:2d} | stubs={len(stub_funcs):2d} | test={'YES' if has_test else 'NO ':3s} | {row['notes']}")
    return results


def check_contract_and_pytest(root: Path) -> dict[str, str]:
    summary = {"contract_lock": "SKIPPED", "pytest_collect": "SKIPPED"}
    clock = root / "scripts" / "contract_lock.py"
    if clock.is_file() and (root / "contract.lock").is_file():
        r = subprocess.run([sys.executable, str(clock), "check"], cwd=root, capture_output=True, text=True)
        summary["contract_lock"] = "OK" if r.returncode == 0 else f"FAILED ({r.stdout.strip() or r.stderr.strip()})"
    if (root / "tests").is_dir():
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"], cwd=root, capture_output=True, text=True)
        summary["pytest_collect"] = "OK" if r.returncode == 0 else "FAILED"
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description="Hackathon Backend King v3.0 Phase 2 AST Doctor & Deduplicator")
    ap.add_argument("root", nargs="?", default=".", help="Project root directory")
    ap.add_argument("--apply", action="store_true", help="Archive duplicate copies (default is report-only)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    print(f"[doctor] Inspecting {root} (mode={'APPLY' if args.apply else 'REPORT-ONLY'})")
    dup_stats = scan_duplicates(root, args.apply)
    modules = audit_python_modules(root)
    gates = check_contract_and_pytest(root)

    report = {
        "mode": "apply" if args.apply else "report_only",
        "duplicates": dup_stats,
        "gates": gates,
        "modules": modules,
    }
    out_file = root / "PHASE2_DOCTOR_REPORT.json"
    out_file.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[doctor] Contract lock: {gates['contract_lock']} | Pytest collect: {gates['pytest_collect']}")
    print(f"[doctor] Wrote {out_file}")


if __name__ == "__main__":
    main()