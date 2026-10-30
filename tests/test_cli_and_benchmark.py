"""Independent Unit Tests for Module 7: parole_cli.py & benchmarks/run_benchmark.py (Covers PRD_07)."""
from __future__ import annotations

import json
from pathlib import Path
from benchmarks.run_benchmark import generate_1000_trace_dataset, run_benchmark_suite
from parole_cli import execute_cli_command, format_terminal_box


def test_cli_n1_offline_git_status_returns_zero() -> None:
    """Covers PRD_07 Sec 3.2: parole_cli.py returns exit code 0 on allowed command."""
    rc = execute_cli_command("git status", source="TRUSTED_USER", offline=True)
    assert rc == 0


def test_cli_a1_offline_ssrf_returns_ten() -> None:
    """Covers PRD_07 Sec 3.2: parole_cli.py returns exit code 10 on intercepted attack."""
    rc = execute_cli_command(
        "curl http://169.254.169.254/latest/meta-data/",
        source="web/repo_payload",
        offline=True,
    )
    assert rc == 10


def test_cli_format_box_contains_key_fields() -> None:
    """Covers PRD_07 Sec 3.2: format_terminal_box renders decision and tier."""
    box = format_terminal_box(
        {
            "command": "git status",
            "provenance": "TRUSTED_USER",
            "taint_flag": False,
            "tier_resolved": "TIER_0",
            "decision": "ALLOWED",
            "latency_ms": 0.42,
            "cost_usd": 0.0,
            "kernel_telemetry": {"override_status": "[STATUS: VERIFIED_SAFE]"},
        }
    )
    assert "TIER_0" in box and "ALLOWED" in box


def test_bm_n1_dataset_has_1000_unique_traces() -> None:
    """Covers PRD_07 Sec 3.2 & Gate 2: 1,000 traces (850 benign, 150 adversarial, 0 duplicates)."""
    ds = generate_1000_trace_dataset(seed=2026)
    assert len(ds) == 1000
    benign = [t for t in ds if t["partition"] == "benign"]
    adv = [t for t in ds if t["partition"] == "adversarial"]
    assert len(benign) == 850
    assert len(adv) == 150
    assert len({t["command"] for t in ds}) == 1000


def test_bm_n2_full_benchmark_writes_results_and_fallback(tmp_path) -> None:
    """Covers PRD_07 Sec 3.2: run_benchmark_suite writes results.json and telemetry_fallback_v2.4.json."""
    out_res = tmp_path / "results.json"
    out_ds = tmp_path / "traces.json"
    res = run_benchmark_suite(mode="in_process", dataset_path=str(out_ds), output_path=str(out_res))
    assert out_res.is_file()
    assert res["suites"]["adversarial"]["block_rate_pct"] == 100.0
    assert all(c["met"] for c in res["claims"])

    fb = Path("frontend/public/telemetry_fallback_v2.4.json")
    assert fb.is_file()
    fb_data = json.loads(fb.read_text(encoding="utf-8"))
    assert fb_data["source"] == "recorded_run"
    assert fb_data["run_id"]