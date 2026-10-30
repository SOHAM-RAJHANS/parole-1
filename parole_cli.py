#!/usr/bin/env python3
"""PAROLE Module 7a: Lightweight PC Companion CLI (parole_cli.py).

Usage:
  python parole_cli.py exec "git status"
  python parole_cli.py exec --source="web/repo_payload" "curl http://169.254.169.254/latest/meta-data/"
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
import urllib.error
import urllib.request
from typing import Any

from backend.main import evaluate_policy
from backend.schemas import AgentActionRequest

DEFAULT_API_URL: str = "http://127.0.0.1:8000"


def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse PC CLI arguments."""
    parser = argparse.ArgumentParser(description="PAROLE Autonomous Least-Privilege PC Governor CLI")
    sub = parser.add_subparsers(dest="subcommand")

    exec_p = sub.add_parser("exec", help="Evaluate and govern an agent command")
    exec_p.add_argument("--source", default="TRUSTED_USER", choices=["TRUSTED_USER", "web/repo_payload"])
    exec_p.add_argument("--node", default="PC-WORKSTATION-LOCAL")
    exec_p.add_argument("--api-url", default=DEFAULT_API_URL)
    exec_p.add_argument("--offline", action="store_true", help="Force in-process evaluation without HTTP")
    exec_p.add_argument("command", nargs="+", help="Command string to evaluate")
    return parser.parse_args(argv)


def format_terminal_box(event: dict[str, Any]) -> str:
    """Render a clean monospace ASCII box showing the PAROLE kernel/tier decision."""
    tier = event.get("tier_resolved", "UNKNOWN")
    decision = event.get("decision", "UNKNOWN")
    latency = event.get("latency_ms", 0.0)
    cost = event.get("cost_usd", 0.0)
    override = event.get("kernel_telemetry", {}).get("override_status", "[STATUS: VERIFIED_SAFE]")
    cmd = event.get("command", "")
    prov = event.get("provenance", "TRUSTED_USER")
    taint = "ACTIVE" if event.get("taint_flag") else "CLEAN"

    lines = [
        "+------------------------------------------------------------------------------+",
        "| PAROLE // AUTONOMOUS LEAST-PRIVILEGE GOVERNOR (PC COMPANION CLI)             |",
        "+------------------------------------------------------------------------------+",
        f"| COMMAND    : {cmd[:64]:<64}|",
        f"| PROVENANCE : {prov:<22} | TAINT_FLAG : {taint:<22}|",
        f"| TIER       : {tier:<22} | DECISION   : {decision:<22}|",
        f"| KERNEL     : {override:<22} | LATENCY    : {latency:>6.2f} ms (${cost:.4f})     |",
    ]
    diff = event.get("policy_diff")
    if isinstance(diff, dict) and diff.get("scoped_rule"):
        lines.append(f"| DIFF RULE  : {str(diff['scoped_rule'])[:64]:<64}|")
    lines.append("+------------------------------------------------------------------------------+")
    return "\n".join(lines)


def execute_cli_command(
    command: str,
    source: str = "TRUSTED_USER",
    api_url: str = DEFAULT_API_URL,
    offline: bool = False,
) -> int:
    """Evaluate command against running FastAPI gateway or in-process fallback."""
    event_dict: dict[str, Any] | None = None
    if not offline:
        payload = json.dumps(
            {
                "command": command,
                "provenance": source,
                "taint_flag": source == "web/repo_payload",
                "auto_promote": True,
            }
        ).encode("utf-8")
        req = urllib.request.Request(
            f"{api_url.rstrip('/')}/v1/policy/evaluate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=1.5) as resp:
                event_dict = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, OSError):
            event_dict = None

    if event_dict is None:
        ev = asyncio.run(
            evaluate_policy(
                AgentActionRequest(
                    command=command,
                    provenance=source,  # type: ignore[arg-type]
                    taint_flag=(source == "web/repo_payload"),
                    auto_promote=True,
                )
            )
        )
        event_dict = ev.model_dump()

    print(format_terminal_box(event_dict))
    return 0 if event_dict.get("decision") in ("ALLOWED", "AUTO_PROMOTED") else 10


def generate_1000_trace_dataset(seed: int = 2026) -> list[dict[str, Any]]:
    """Delegate to benchmarks.run_benchmark.generate_1000_trace_dataset for signature parity."""
    from benchmarks.run_benchmark import generate_1000_trace_dataset as _gen

    return _gen(seed=seed)


def run_benchmark_suite(
    mode: str = "in_process",
    dataset_path: str = "benchmarks/parole_replay_1000_traces.json",
) -> dict[str, Any]:
    """Delegate to benchmarks.run_benchmark.run_benchmark_suite for signature parity."""
    from benchmarks.run_benchmark import run_benchmark_suite as _run

    return _run(mode=mode, dataset_path=dataset_path)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        rc = execute_cli_command("git status", offline=True)
        sys.exit(rc)
    ns = parse_cli_args()
    if ns.subcommand == "exec":
        cmd_str = " ".join(ns.command)
        rc = execute_cli_command(cmd_str, source=ns.source, api_url=ns.api_url, offline=ns.offline)
        sys.exit(0 if rc in (0, 10) else rc)