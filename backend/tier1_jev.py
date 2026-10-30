#!/usr/bin/env python3
"""PAROLE Module 3: Tier 1 System-1 Typed Risk Classifier (backend/tier1_jev.py).

Evaluates Tier 0 cache misses by computing discrete blast_radius_score (0..100)
and injection_risk_score (0..100). Commands with both scores < 20 resolve as ALLOWED.
"""
from __future__ import annotations

import re
import time
from typing import Any

TIER1_ALLOW_THRESHOLD: int = 20

SAFE_INSPECTION_PREFIXES: tuple[str, ...] = (
    "cat ",
    "head ",
    "tail ",
    "grep ",
    "rg ",
    "find ./",
    "find src/",
    "wc ",
    "stat ",
    "file ",
    "ls ",
    "pwd",
    "whoami",
    "python -m unittest",
    "tsc --noemit",
    "npm run build",
    "du -sh",
)

INTERNAL_SUBNET_RE = re.compile(r"https?://(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3})", re.I)
DESTRUCTIVE_TOKENS: tuple[str, ...] = (
    "rm -rf",
    "rm -fr",
    "mkfs",
    "dd if=",
    "chmod ",
    "chown ",
    "docker run --privileged",
    "kubectl delete",
    "sudo ",
    "su -",
    "/etc/",
    "/root/",
)
NETWORK_MUTATION_TOKENS: tuple[str, ...] = (
    "curl ",
    "wget ",
    "http://",
    "https://",
    "nc ",
    "netcat ",
    "scp ",
    "ssh ",
    "pip install",
    "npm install",
)
INLINE_EXEC_RE = re.compile(r"(?:\bpython3?\s+-c\b|\bnode\s+-e\b|\bsh\s+-c\b|\bbash\s+-c\b|\bperl\s+-e\b|\bruby\s+-e\b|\beval\s+)", re.I)


def compute_blast_radius(command: str, target_resource: str = "") -> int:
    """Compute discrete blast_radius_score in [0, 100]."""
    if not isinstance(command, str) or not command.strip():
        return 100

    cmd_clean = command.strip()
    cmd_lower = cmd_clean.lower()

    for bad in DESTRUCTIVE_TOKENS:
        if bad in cmd_lower:
            return 88

    if INLINE_EXEC_RE.search(cmd_clean):
        return 75

    # Outbound call to internal RFC1918 subnet that missed Tier 0 -> escalate to Tier 2 (score 52)
    if INTERNAL_SUBNET_RE.search(cmd_clean):
        return 52

    for net_tok in NETWORK_MUTATION_TOKENS:
        if net_tok in cmd_lower:
            return 68

    # Safe local workspace inspection / build commands
    if ".." not in cmd_clean:
        for pref in SAFE_INSPECTION_PREFIXES:
            if cmd_lower == pref.strip() or cmd_lower.startswith(pref):
                return 8

    return 35


def compute_injection_risk(
    command: str,
    provenance: str = "TRUSTED_USER",
    taint_flag: bool = False,
) -> int:
    """Compute discrete injection_risk_score in [0, 100]."""
    if not isinstance(command, str) or not command.strip():
        return 100

    if taint_flag or provenance == "web/repo_payload":
        return 92

    cmd_clean = command.strip()
    if INLINE_EXEC_RE.search(cmd_clean):
        return 68

    if any(op in cmd_clean for op in ("&&", "||", ";", "|", "`", "$(", "../", "%2e")):
        return 55

    return 6


def evaluate_tier1_jev(
    command: str,
    target_resource: str = "",
    provenance: str = "TRUSTED_USER",
    taint_flag: bool = False,
) -> dict[str, Any]:
    """Step 3 Tier 1 System-1 Typed Risk Classifier evaluation."""
    t0 = time.perf_counter_ns()
    blast = compute_blast_radius(command, target_resource)
    inj = compute_injection_risk(command, provenance, taint_flag)
    elapsed_ms = round((time.perf_counter_ns() - t0) / 1_000_000.0, 3)

    if blast < TIER1_ALLOW_THRESHOLD and inj < TIER1_ALLOW_THRESHOLD:
        return {
            "allow": True,
            "escalate_tier2": False,
            "blast_radius_score": blast,
            "injection_risk_score": inj,
            "tier_resolved": "TIER_1",
            "decision": "ALLOWED",
            "latency_ms": max(elapsed_ms, 0.11),
        }

    return {
        "allow": False,
        "escalate_tier2": True,
        "blast_radius_score": blast,
        "injection_risk_score": inj,
        "tier_resolved": "TIER_2",
        "decision": "ESCALATE",
        "latency_ms": max(elapsed_ms, 0.11),
    }


if __name__ == "__main__":
    r_safe = evaluate_tier1_jev("cat src/config.ts", "src/config.ts", "TRUSTED_USER", False)
    assert r_safe["allow"] is True and r_safe["blast_radius_score"] < 20
    r_esc = evaluate_tier1_jev("curl -s https://10.0.4.12/api/v1/users", "10.0.4.12/api/v1/users", "TRUSTED_USER", False)
    assert r_esc["allow"] is False and r_esc["escalate_tier2"] is True