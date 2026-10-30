#!/usr/bin/env python3
"""Freeze and verify the Wave 0 contract (backend/schemas.py + contract.json -> contract.lock)."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

CONTRACT_FILES = ["backend/schemas.py", "contract.json"]
LOCK = Path("contract.lock")


def digests() -> dict[str, str]:
    out: dict[str, str] = {}
    for f in CONTRACT_FILES:
        p = Path(f)
        if not p.is_file():
            sys.exit(f"[contract] missing {f}")
        out[f] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def version() -> int:
    data = json.loads(Path("contract.json").read_text(encoding="utf-8"))
    v = data.get("contract_version")
    if not isinstance(v, int):
        sys.exit('[contract] contract.json must contain an integer "contract_version"')
    return v


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "write":
        payload = {"contract_version": version(), "sha256": digests()}
        LOCK.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"[contract] locked v{payload['contract_version']} -> {LOCK}")
    elif cmd == "check":
        if not LOCK.is_file():
            sys.exit("[contract] contract.lock missing: run `write` after Wave 0")
        locked = json.loads(LOCK.read_text(encoding="utf-8"))
        now = {"contract_version": version(), "sha256": digests()}
        if now != locked:
            drift = [f for f in CONTRACT_FILES if now["sha256"][f] != locked["sha256"].get(f)]
            print(f"[contract] DRIFT in: {', '.join(drift) or 'contract_version'}")
            sys.exit(1)
        print(f"[contract] OK (v{now['contract_version']})")
    else:
        sys.exit("usage: contract_lock.py write|check")


if __name__ == "__main__":
    main()