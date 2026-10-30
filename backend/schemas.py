#!/usr/bin/env python3
"""PAROLE Wave 0a Schema Contract (backend/schemas.py).

Single source of truth for Pydantic v2 models, enums, constants, and contract.json export.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

CONTRACT_VERSION: int = 1
MAX_COMMAND_LEN: int = 4096
MAX_RESOURCE_LEN: int = 1024
MAX_NODE_LEN: int = 128

PROVENANCE_VALUES = ("TRUSTED_USER", "web/repo_payload")
TIER_VALUES = ("KERNEL_HARD_DENY", "TIER_0", "TIER_1", "TIER_2")
DECISION_VALUES = ("ALLOWED", "INTERCEPTED", "AUTO_PROMOTED")
CAPABILITY_VALUES = ("live", "replay", "simulated")

SUPER_120B_LABEL = "nemotron-3-super-120b-a12b ($0.30/M tokens)"
ULTRA_550B_LABEL = "Nemotron-3-Ultra-550b-a55b ($1.00/M tokens)"
CANONICAL_BROAD_RULE = "- GRANT ALL permissions TO *:*"
CANONICAL_SCOPED_RULE = "+ PERMIT 10.0.4.0/24 ON /api/v1/*"

COST_USD_BY_TIER: dict[str, float] = {
    "KERNEL_HARD_DENY": 0.0,
    "TIER_0": 0.0,
    "TIER_1": 0.0003,
    "TIER_2": 0.008,
}

ProvenanceType = Literal["TRUSTED_USER", "web/repo_payload"]
TierType = Literal["KERNEL_HARD_DENY", "TIER_0", "TIER_1", "TIER_2"]
DecisionType = Literal["ALLOWED", "INTERCEPTED", "AUTO_PROMOTED"]
CapabilityType = Literal["live", "replay", "simulated"]


class KernelTelemetry(BaseModel):
    model_config = ConfigDict(extra="forbid")

    sandbox_cmd: str = Field(default="$ sandboxing --mode=landlock", min_length=1, max_length=256)
    syscall_cmd: str = Field(default="$ filtering --syscall=seccomp", min_length=1, max_length=256)
    vm_status: str = Field(default="[STATUS: ISOLATED_VM]", min_length=1, max_length=128)
    override_status: str = Field(default="[STATUS: VERIFIED_SAFE]", min_length=1, max_length=128)


class PolicyDiff(BaseModel):
    model_config = ConfigDict(extra="forbid")

    broad_antipattern: str = Field(default=CANONICAL_BROAD_RULE, min_length=1, max_length=512)
    scoped_rule: str = Field(default=CANONICAL_SCOPED_RULE, min_length=1, max_length=512)
    super_120b_model: str = Field(default=SUPER_120B_LABEL, min_length=1, max_length=128)
    super_120b_counterfactual: str = Field(min_length=1, max_length=1024)
    ultra_550b_model: str = Field(default=ULTRA_550B_LABEL, min_length=1, max_length=128)
    ultra_550b_verified: bool
    ultra_550b_audit_note: str = Field(min_length=1, max_length=1024)


class AgentActionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    command: str = Field(min_length=1, max_length=MAX_COMMAND_LEN)
    workstation_node: str = Field(default="PC-WORKSTATION-LOCAL", min_length=1, max_length=MAX_NODE_LEN)
    target_resource: Optional[str] = Field(default=None, max_length=MAX_RESOURCE_LEN)
    provenance: ProvenanceType = Field(default="TRUSTED_USER")
    taint_flag: Optional[bool] = Field(default=None)
    auto_promote: bool = Field(default=False)

    @field_validator("command")
    @classmethod
    def validate_non_whitespace_command(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("command must not be empty or whitespace-only")
        try:
            v.encode("utf-8")
        except UnicodeEncodeError as exc:
            raise ValueError("command must be valid UTF-8") from exc
        return v

    @model_validator(mode="after")
    def set_default_taint_flag(self) -> "AgentActionRequest":
        if self.taint_flag is None:
            self.taint_flag = self.provenance == "web/repo_payload"
        elif self.provenance == "web/repo_payload":
            self.taint_flag = True
        return self


class AgentActionEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    event_id: str = Field(min_length=1, max_length=128)
    timestamp: str = Field(min_length=1, max_length=64)
    workstation_node: str = Field(min_length=1, max_length=MAX_NODE_LEN)
    command: str = Field(min_length=1, max_length=MAX_COMMAND_LEN)
    target_resource: str = Field(min_length=1, max_length=MAX_RESOURCE_LEN)
    provenance: ProvenanceType
    taint_flag: bool
    kernel_telemetry: KernelTelemetry
    tier_resolved: TierType
    decision: DecisionType
    latency_ms: float = Field(ge=0.0)
    cost_usd: float = Field(ge=0.0)
    policy_diff: Optional[PolicyDiff] = None
    capability: CapabilityType = Field(default="live")


class ApproveDiffRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scoped_rule: str = Field(default=CANONICAL_SCOPED_RULE, min_length=5, max_length=512)
    trigger_followup: bool = Field(default=True)


class ApproveDiffResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    promoted: bool
    scoped_rule: str
    active_rules: list[str]
    latency_ms: float = Field(ge=0.0)
    followup_event: Optional[AgentActionEvent] = None


class EscalationPoint(BaseModel):
    model_config = ConfigDict(extra="forbid")

    minute: int = Field(ge=0)
    naive_sandbox: float = Field(ge=0.0, le=100.0)
    parole_reflex: float = Field(ge=0.0, le=100.0)


class TierDistribution(BaseModel):
    model_config = ConfigDict(extra="forbid")

    tier_0: int = Field(ge=0, le=100)
    tier_1: int = Field(ge=0, le=100)
    tier_2: int = Field(ge=0, le=100)


class MetricsSummaryResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    total_traces_evaluated: int = Field(ge=0)
    zero_day_block_rate_pct: float = Field(ge=0.0, le=100.0)
    false_positive_rate_pct: float = Field(ge=0.0, le=100.0)
    safe_auto_grant_accuracy_pct: float = Field(ge=0.0, le=100.0)
    p95_latency_ms: float = Field(ge=0.0)
    cost_per_1k_actions_usd: float = Field(ge=0.0)
    tier_distribution: TierDistribution
    escalation_collapse_curve: list[EscalationPoint]
    active_tier0_rules: list[str]
    capability: CapabilityType = Field(default="live")


class ValidationErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    error: str
    field_paths: list[str]


def build_default_kernel_telemetry(
    blocked: bool = False,
    taint_intercepted: bool = False,
) -> KernelTelemetry:
    """Build canonical KernelTelemetry instance per Dossier 01 Task 1.1."""
    if taint_intercepted:
        override = "[INJECTION: INTERCEPTED]"
    elif blocked:
        override = "[OVERRIDE: FORBIDDEN]"
    else:
        override = "[STATUS: VERIFIED_SAFE]"
    return KernelTelemetry(
        sandbox_cmd="$ sandboxing --mode=landlock",
        syscall_cmd="$ filtering --syscall=seccomp",
        vm_status="[STATUS: ISOLATED_VM]",
        override_status=override,
    )


def export_contract_schema() -> dict[str, Any]:
    """Export machine-readable contract schema with contract_version=1."""
    return {
        "contract_version": CONTRACT_VERSION,
        "project": "PAROLE",
        "constants": {
            "PROVENANCE_VALUES": list(PROVENANCE_VALUES),
            "TIER_VALUES": list(TIER_VALUES),
            "DECISION_VALUES": list(DECISION_VALUES),
            "CAPABILITY_VALUES": list(CAPABILITY_VALUES),
            "COST_USD_BY_TIER": COST_USD_BY_TIER,
            "SUPER_120B_LABEL": SUPER_120B_LABEL,
            "ULTRA_550B_LABEL": ULTRA_550B_LABEL,
            "CANONICAL_BROAD_RULE": CANONICAL_BROAD_RULE,
            "CANONICAL_SCOPED_RULE": CANONICAL_SCOPED_RULE,
        },
        "routes": [
            {"method": "POST", "path": "/v1/policy/evaluate", "request": "AgentActionRequest", "response": "AgentActionEvent", "demo_only": False},
            {"method": "GET", "path": "/v1/policy/stream", "request": None, "response": "SSE[AgentActionEvent]", "demo_only": False},
            {"method": "POST", "path": "/v1/policy/approve-diff", "request": "ApproveDiffRequest", "response": "ApproveDiffResponse", "demo_only": False},
            {"method": "GET", "path": "/v1/metrics/summary", "request": None, "response": "MetricsSummaryResponse", "demo_only": False},
            {"method": "POST", "path": "/v1/demo/run-180s", "request": None, "response": "dict", "demo_only": True},
            {"method": "GET", "path": "/health", "request": None, "response": "dict", "demo_only": False},
        ],
        "models": {
            "KernelTelemetry": KernelTelemetry.model_json_schema(),
            "PolicyDiff": PolicyDiff.model_json_schema(),
            "AgentActionRequest": AgentActionRequest.model_json_schema(),
            "AgentActionEvent": AgentActionEvent.model_json_schema(),
            "ApproveDiffRequest": ApproveDiffRequest.model_json_schema(),
            "ApproveDiffResponse": ApproveDiffResponse.model_json_schema(),
            "EscalationPoint": EscalationPoint.model_json_schema(),
            "TierDistribution": TierDistribution.model_json_schema(),
            "MetricsSummaryResponse": MetricsSummaryResponse.model_json_schema(),
            "ValidationErrorResponse": ValidationErrorResponse.model_json_schema(),
        },
    }


def write_contract_json(path: str = "contract.json") -> None:
    """Write contract.json to disk."""
    out_path = Path(path)
    out_path.write_text(json.dumps(export_contract_schema(), indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    req = AgentActionRequest(command="git status")
    assert req.provenance == "TRUSTED_USER" and req.taint_flag is False
    tainted_req = AgentActionRequest(command="curl https://evil.io", provenance="web/repo_payload")
    assert tainted_req.taint_flag is True
    write_contract_json("contract.json")