# PRD_00: `backend/schemas.py` & `contract.json`

**Target File(s)**: `backend/schemas.py`, `contract.json`
**Lane / role**: `0a` / Builder   **Audit required**: no
**Design reference**: Stripe Webhook Event Schema [SOURCE: Dossier_01 p1]

## 1. Purpose and Role

Defines the single source of truth Pydantic v2 data models for PAROLE's backend gateway, SSE stream, CLI, benchmark runner, and Role 2's Next.js TypeScript frontend. Exports `contract.json` with `"contract_version": 1` so `scripts/contract_lock.py write` can freeze the SHA-256 digest before Wave 0b and Wave 1 begin.

## 2. Bound Skills (Verified in `SKILLS_AVAILABLE.md`)

| Slash | Rule Pack if Skill is Missing | Why Here |
| :--- | :--- | :--- |
| `/atlas-contract` | `RP-CONTRACT` | Enforces character-for-character field parity with Role 1 Dossier Subtask 1.1 and Role 2 TypeScript interfaces |
| `/super-mega-backend` | `RP-FASTAPI` | Configures Pydantic v2 `ConfigDict(extra="forbid")`, strict string length bounds, and JSON schema export |

## 3. Specification

1. **Data and Constants**:
   - `CONTRACT_VERSION: int = 1`
   - `MAX_COMMAND_LEN: int = 4096`
   - `MAX_RESOURCE_LEN: int = 1024`
   - `MAX_NODE_LEN: int = 128`
   - `ProvenanceType = Literal["TRUSTED_USER", "web/repo_payload"]`
   - `TierType = Literal["KERNEL_HARD_DENY", "TIER_0", "TIER_1", "TIER_2"]`
   - `DecisionType = Literal["ALLOWED", "INTERCEPTED", "AUTO_PROMOTED"]`
   - `CapabilityType = Literal["live", "replay", "simulated"]`
   - **Pydantic v2 Models**:
     - `KernelTelemetry`: `sandbox_cmd: str`, `syscall_cmd: str`, `vm_status: str`, `override_status: str`
     - `PolicyDiff`: `broad_antipattern: str`, `scoped_rule: str`, `super_120b_model: str`, `super_120b_counterfactual: str`, `ultra_550b_model: str`, `ultra_550b_verified: bool`, `ultra_550b_audit_note: str`
     - `AgentActionRequest`: `command: str` (`min_length=1, max_length=4096`), `workstation_node: str = "PC-WORKSTATION-LOCAL"`, `target_resource: Optional[str] = None`, `provenance: ProvenanceType = "TRUSTED_USER"`, `taint_flag: Optional[bool] = None`, `auto_promote: bool = False`
     - `AgentActionEvent`: `event_id: str`, `timestamp: str`, `workstation_node: str`, `command: str`, `target_resource: str`, `provenance: ProvenanceType`, `taint_flag: bool`, `kernel_telemetry: KernelTelemetry`, `tier_resolved: TierType`, `decision: DecisionType`, `latency_ms: float`, `cost_usd: float`, `policy_diff: Optional[PolicyDiff] = None`, `capability: CapabilityType = "live"`
     - `ApproveDiffRequest`: `scoped_rule: str` (`min_length=5, max_length=512`), `trigger_followup: bool = True`
     - `ApproveDiffResponse`: `promoted: bool`, `scoped_rule: str`, `active_rules: list[str]`, `latency_ms: float`, `followup_event: Optional[AgentActionEvent] = None`
     - `EscalationPoint`: `minute: int`, `naive_sandbox: float`, `parole_reflex: float`
     - `TierDistribution`: `tier_0: int`, `tier_1: int`, `tier_2: int`
     - `MetricsSummaryResponse`: `total_traces_evaluated: int`, `zero_day_block_rate_pct: float`, `false_positive_rate_pct: float`, `safe_auto_grant_accuracy_pct: float`, `p95_latency_ms: float`, `cost_per_1k_actions_usd: float`, `tier_distribution: TierDistribution`, `escalation_collapse_curve: list[EscalationPoint]`, `active_tier0_rules: list[str]`, `capability: CapabilityType`
     - `ValidationErrorResponse`: `error: str`, `field_paths: list[str]`

2. **Functions**:
   - `def build_default_kernel_telemetry(blocked: bool = False, taint_intercepted: bool = False) -> KernelTelemetry:` returns the canonical `KernelTelemetry` instance with `sandbox_cmd="$ sandboxing --mode=landlock"`, `syscall_cmd="$ filtering --syscall=seccomp"`, `vm_status="[STATUS: ISOLATED_VM]"`, and `override_status` set to `"[INJECTION: INTERCEPTED]"` when `taint_intercepted` is True, `"[OVERRIDE: FORBIDDEN]"` when `blocked` is True, or `"[STATUS: VERIFIED_SAFE]"` when allowed [SOURCE: Dossier_01 p2].
   - `def export_contract_schema() -> dict:` exports the complete JSON schema dictionary containing `"contract_version": 1`, `"models"`, and `"routes"`.
   - `def write_contract_json(path: str = "contract.json") -> None:` writes `export_contract_schema()` formatted with `indent=2` to `contract.json`.

3. **Edge Cases**:
   - Empty `command=""` or whitespace-only `command="   "` must be rejected by Pydantic validation (`ValueError`).
   - Strings exceeding `4096` characters on `command` must fail validation immediately.
   - If `provenance == "web/repo_payload"` and `taint_flag` is `None`, model validator automatically sets `taint_flag = True` [SOURCE: Dossier_01 p2].

4. **Failure Behaviour**:
   - Invalid field types, unknown extra fields (`extra="forbid"`), or out-of-range string lengths raise `pydantic.ValidationError` cleanly without echoing raw input values in error summaries.

5. **Budget**:
   - Model instantiation and serialization p95 `<= 0.1 ms` [TARGET].

## 4. Invariants

- Matches `00_MASTER_PRD.md` Sections 3 and 4 character for character.
- Writes only `backend/schemas.py` and `contract.json` (plus `requests/0a.md` if blocked).
- Uses only `pydantic` v2 and Python standard library modules (`typing`, `json`, `uuid`, `datetime`, `pathlib`).
- No network calls, file reads at import time, or secrets.

## 5. Gates

```bash
python backend/schemas.py
python scripts/contract_lock.py write
python scripts/contract_lock.py check
python scripts/prd_lint.py documentation --check-signatures
```