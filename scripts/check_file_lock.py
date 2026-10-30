#!/usr/bin/env python3
"""Enforce [STRICT FILE LOCK]: fail if any file outside the allowlist changed since a git ref."""
from __future__ import annotations

import argparse
import fnmatch
import subprocess
import sys


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[lock] git {' '.join(args)} failed: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return r.stdout


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--since", required=True, help="git tag or commit taken before this lane started")
    ap.add_argument("--allow", action="append", default=[], help="glob of a path this lane may touch")
    a = ap.parse_args()
    if not a.allow:
        print("[lock] refusing to run without at least one --allow", file=sys.stderr)
        sys.exit(2)

    changed = set(git("diff", "--name-only", a.since).splitlines())
    changed |= set(git("ls-files", "--others", "--exclude-standard").splitlines())
    changed.discard("")
    bad = sorted(p for p in changed if not any(fnmatch.fnmatch(p, g) for g in a.allow))

    if bad:
        print("[lock] VIOLATION: files changed outside the allowlist:")
        for p in bad:
            print(f"  - {p}")
        sys.exit(1)
    print(f"[lock] OK: {len(changed)} changed file(s), all inside the allowlist")


if __name__ == "__main__":
    main()