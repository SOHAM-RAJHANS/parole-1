#!/usr/bin/env python3
"""Non-destructive applier for model-generated files with AST check, backup, and rollback."""
from __future__ import annotations

import argparse
import ast
import fnmatch
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
INCOMING = ROOT / "_incoming"
BLOCK = re.compile(r"^=== FILE: (.+?) ===[ \t]*\n(.*?)^=== END ===[ \t]*$", re.S | re.M)


def check_path(rel: str, allow: list[str]) -> str:
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts or not rel.strip():
        raise ValueError(f"unsafe path: {rel!r}")
    posix = p.as_posix()
    if not any(fnmatch.fnmatch(posix, g) for g in allow):
        raise ValueError(f"not covered by --allow: {posix}")
    return posix


def unfence(body: str) -> str:
    lines = body.rstrip("\n").split("\n")
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
    return "\n".join(lines) + "\n"


def stage_bundle(bundle: Path, allow: list[str]) -> list[str]:
    blocks = BLOCK.findall(bundle.read_text(encoding="utf-8"))
    if not blocks:
        raise ValueError("no '=== FILE: path ===' ... '=== END ===' blocks found in bundle")
    rels: list[str] = []
    for rel, body in blocks:
        posix = check_path(rel.strip(), allow)
        dst = INCOMING / posix
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(unfence(body), encoding="utf-8")
        rels.append(posix)
    return rels


def install(rel: str, stamp: str) -> tuple[str, Path | None]:
    src, dst = INCOMING / rel, ROOT / rel
    if not src.is_file():
        raise FileNotFoundError(f"{src} not found")
    if rel.endswith(".py"):
        ast.parse(src.read_text(encoding="utf-8"), filename=rel)
    backup = None
    if dst.exists():
        backup = ROOT / "_backups" / stamp / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, backup)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return rel, backup


def rollback(done: list[tuple[str, Path | None]]) -> None:
    for rel, backup in reversed(done):
        dst = ROOT / rel
        if backup is not None:
            shutil.copy2(backup, dst)
        elif dst.exists():
            dst.unlink()
        print(f"[apply] rolled back {rel}")


def run_gate(cmd: str) -> bool:
    if not cmd:
        return True
    return subprocess.run(cmd, shell=True, timeout=600).returncode == 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("files", nargs="*")
    ap.add_argument("--allow", action="append", default=[], required=True)
    ap.add_argument("--bundle")
    ap.add_argument("--gate", default="")
    ap.add_argument("--atomic", action="store_true")
    a = ap.parse_args()

    try:
        rels = [check_path(f, a.allow) for f in a.files]
        if a.bundle:
            rels += stage_bundle(Path(a.bundle), a.allow)
    except (ValueError, OSError) as e:
        print(f"[apply] REFUSED: {e}", file=sys.stderr)
        sys.exit(2)
    if not rels:
        sys.exit("[apply] nothing to apply")

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    done: list[tuple[str, Path | None]] = []
    try:
        for rel in rels:
            done.append(install(rel, stamp))
            print(f"[apply] installed {rel}")
            if not a.atomic and not run_gate(a.gate):
                print(f"[apply] GATE FAILED after {rel}")
                rollback([done.pop()])
                sys.exit(1)
        if a.atomic and not run_gate(a.gate):
            print("[apply] GATE FAILED (atomic): rolling everything back")
            rollback(done)
            sys.exit(1)
    except (SyntaxError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"[apply] ERROR: {e}", file=sys.stderr)
        rollback(done)
        sys.exit(1)
    print(f"[apply] OK: {len(done)} file(s) applied; backups in _backups/{stamp}/")


if __name__ == "__main__":
    main()