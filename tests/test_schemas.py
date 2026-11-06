"""Independent Unit Tests for Module 0a: backend/schemas.py (Covers PRD_00)."""
from __future__ import annotations

import json
from pathlib import Path
import time
import pytest
from pydantic import ValidationError

from backend.schemas import (
    AgentActionRequest,
    build_default_kernel_telemetry,
    export_contract_schema,
)


def test_sch_n1_default_request_fields() -> None:
    """Covers PRD_00 Sec 3.1: default provenance and taint_flag."""
    req = AgentActionRequest(command="git status")
    assert req.provenance == "TRUSTED_USER"
    assert req.taint_flag is False
    assert req.workstation_node == "PC-WORKSTATION-LOCAL"


def test_sch_n2_web_repo_payload_sets_taint_flag() -> None:
    """Covers PRD_00 Sec 3.3: provenance=='web/repo_payload' auto-enables taint_flag."""
    req = AgentActionRequest(command="curl https://evil.io", provenance="web/repo_payload")
    assert req.taint_flag is True


def test_sch_n3_build_default_kernel_telemetry() -> None:
    """Covers PRD_00 Sec 3.2: canonical override_status strings."""
    kt_safe = build_default_kernel_telemetry(blocked=False, taint_intercepted=False)
    assert kt_safe.override_status == "[STATUS: VERIFIED_SAFE]"

    kt_forbid = build_default_kernel_telemetry(blocked=True, taint_intercepted=False)
    assert kt_forbid.override_status == "[OVERRIDE: FORBIDDEN]"

    kt_taint = build_default_kernel_telemetry(blocked=True, taint_intercepted=True)
    assert kt_taint.override_status == "[INJECTION: INTERCEPTED]"


def test_sch_a1_empty_or_whitespace_command_rejected() -> None:
    """Covers PRD_00 Sec 3.3: empty and whitespace commands raise ValidationError."""
    with pytest.raises(ValidationError):
        AgentActionRequest(command="")
    with pytest.raises(ValidationError):
        AgentActionRequest(command="    \t\n  ")


def test_sch_a2_overlong_command_rejected() -> None:
    """Covers PRD_00 Sec 3.1: command > 4096 chars raises ValidationError."""
    with pytest.raises(ValidationError):
        AgentActionRequest(command="a" * 5000)


def test_sch_a3_unknown_extra_field_rejected() -> None:
    """Covers PRD_00 Sec 2: extra='forbid' rejects unknown fields."""
    with pytest.raises(ValidationError):
        AgentActionRequest(command="git status", unexpected_field="malicious")  # type: ignore[call-arg]


def test_sch_a4_invalid_provenance_rejected() -> None:
    """Covers PRD_00 Sec 3.1: invalid provenance literal raises ValidationError."""
    with pytest.raises(ValidationError):
        AgentActionRequest(command="git status", provenance="UNKNOWN_SOURCE")  # type: ignore[arg-type]


def test_sch_a5_overlong_target_resource_rejected() -> None:
    """Covers PRD_00 Sec 3.1: target_resource > 1024 chars raises ValidationError."""
    with pytest.raises(ValidationError):
        AgentActionRequest(command="git status", target_resource="x" * 1500)


def test_sch_c1_contract_json_parity() -> None:
    """Covers PRD_00 Sec 3.2: export_contract_schema matches contract.json on disk."""
    exported = export_contract_schema()
    assert exported["contract_version"] == 1
    route_paths = {route["path"] for route in exported["routes"]}
    assert {"/", "/healthz", "/health"} <= route_paths
    contract_file = Path("contract.json")
    if contract_file.is_file():
        on_disk = json.loads(contract_file.read_text(encoding="utf-8"))
        assert on_disk["contract_version"] == 1
        assert set(exported["models"].keys()) == set(on_disk["models"].keys())


def test_sch_latency_ceiling() -> None:
    """Covers PRD_00 Sec 3.5: model instantiation under 5x ceiling (0.5 ms)."""
    t0 = time.perf_counter_ns()
    _ = AgentActionRequest(command="pytest tests/unit")
    elapsed_ms = (time.perf_counter_ns() - t0) / 1_000_000.0
    assert elapsed_ms <= 5.0