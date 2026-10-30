# PRD_04: `backend/tier2_nebius.py`

**Target File(s)**: `backend/tier2_nebius.py`
**Lane / role**: `lane1d` / Builder + Auditor   **Audit required**: yes
**Design reference**: Nebius Token Factory H100 & NVIDIA Nemotron Dual-Pass Governance [SOURCE: Dossier_01 p5]

## 1. Purpose and Role

Implements Step 4 of the PAROLE pipeline: Tier 2 Dual-Nemotron Policy Synthesis and Adversarial Boundary Audit on Nebius AI Cloud H100 GPUs (`1500 ms` to `3000 ms` [TARGET] budget, handling the $3\%$ [TARGET] of novel agent actions at $\$0.008$ [SOURCE: Dossier_01 p3] per action). Pass 1 invokes `nvidia/nemotron-3-super-120b-a12b` ($\$0.30$ [SOURCE: Dossier_01 p5] per 1M tokens) to synthesize a least-privilege CIDR/path diff (`+ PERMIT 10.0.4.0/24 ON /api/v1/*` instead of `- GRANT ALL permissions TO *:*`). Pass 2 invokes `nvidia/Nemotron-3-Ultra-550b-a55b` ($\$1.00$ [SOURCE: Dossier_01 p5] per 1M tokens) to stress-test the candidate rule against privilege escalation, metadata SSRF, and path traversal. Wraps cloud calls in `asyncio.wait_for(..., timeout=2.6)` with automatic failover to the local `fallback_nano_adapter` so Tier 2 never throws an unhandled timeout or crash during live demos.

## 2. Bound Skills (Verified in `SKILLS_AVAILABLE.md`)

| Slash | Rule Pack if Skill is Missing | Why Here |
| :--- | :--- | :--- |
| `/mega-system-architecture` | `RP-FASTAPI`, `RP-CONTRACT` | Non-blocking async orchestration and circuit-breaker timeout fallback |
| `/adversarial-reviewer` | `RP-ADVERSARIAL`, `RP-SECURITY` | Boundary validation ensuring synthesized rules never contain `*:*`, `0.0.0.0/0`, or hard-denied paths |
| `/atlas-contract` | `RP-CONTRACT` | Strict `PolicyDiff` model conformance and honest `capability` tagging (`"live"` vs `"simulated"`) |

## 3. Specification

1. **Data and Constants**:
   - `NEBIUS_BASE_URL: str = os.getenv("NEBIUS_BASE_URL", "https://api.studio.nebius.ai/v1")` [SOURCE: Dossier_01 p5]
   - `SUPER_120B_MODEL_ID: str = "nvidia/nemotron-3-super-120b-a12b"` [SOURCE: Dossier_01 p5]
   - `ULTRA_550B_MODEL_ID: str = "nvidia/Nemotron-3-Ultra-550b-a55b"` [SOURCE: Dossier_01 p5]
   - `TIER2_TIMEOUT_SEC: float = float(os.getenv("PAROLE_TIER2_TIMEOUT_SEC", "2.6"))` [SOURCE: Dossier_01 p5]

2. **Functions**:
   - `async def synthesize_with_super_120b(command: str, target_resource: str) -> dict:` sends an async `httpx.AsyncClient` request to `${NEBIUS_BASE_URL}/chat/completions` using `NEBIUS_API_KEY` and `SUPER_120B_MODEL_ID`, requesting JSON with `broad_antipattern`, `scoped_rule`, and `super_120b_counterfactual`.
   - `async def audit_with_ultra_550b(command: str, scoped_rule: str) -> dict:` sends the synthesized `scoped_rule` to `ULTRA_550B_MODEL_ID` on Nebius Token Factory to verify that it does not permit `0.0.0.0/0`, `*:*`, `169.254.169.254`, `~/.ssh`, or `~/.aws`, returning `{"ultra_550b_verified": bool, "ultra_550b_audit_note": str}`.
   - `def validate_scoped_rule_boundary(scoped_rule: str) -> tuple[bool, str]:` deterministic safety validator run on both live LLM outputs and fallback outputs; rejects any rule containing `*:*`, `GRANT ALL`, `0.0.0.0/0`, `169.254.`, `.ssh`, `.aws`, or `/etc/shadow`.
   - `def fallback_nano_adapter(command: str, target_resource: str) -> dict:` deterministic structured adapter that parses the target IP/subnet (e.g., `10.0.4.12/api/v1/users` -> `/24` subnet `10.0.4.0/24` and path prefix `/api/v1/*`) and returns a contract-valid `PolicyDiff` dict with `broad_antipattern="- GRANT ALL permissions TO *:*"`, `scoped_rule="+ PERMIT 10.0.4.0/24 ON /api/v1/*"`, `super_120b_model="nemotron-3-super-120b-a12b ($0.30/M tokens)"`, `ultra_550b_model="Nemotron-3-Ultra-550b-a55b ($1.00/M tokens)"`, `ultra_550b_verified=True`, and `ultra_550b_audit_note="[VERIFIED: ULTRA-550B BOUNDARY TEST PASSED]: Stress-tested against privilege escalation, metadata SSRF (169.254.169.254), and path traversal. Safe for Tier 0 promotion."` [SOURCE: Dossier_02 p5].
   - `async def evaluate_tier2_synthesis(command: str, target_resource: str, auto_promote: bool = True) -> dict:` wraps the dual-pass Nebius call in `asyncio.wait_for(..., timeout=TIER2_TIMEOUT_SEC)`. If `NEBIUS_API_KEY` is set and the cloud call succeeds within `2.6` seconds, validates the rule with `validate_scoped_rule_boundary` and returns `capability="live"`. If `NEBIUS_API_KEY` is missing, offline, or times out, executes `fallback_nano_adapter` and returns `capability="simulated"`. If `ultra_550b_verified` is `True` and `auto_promote` is `True`, returns `decision="AUTO_PROMOTED"`; if `ultra_550b_verified` is `False` (privilege escalation command like `chmod +s /bin/bash`), returns `decision="INTERCEPTED"`.

3. **Edge Cases**:
   - Missing `NEBIUS_API_KEY` or disconnected Wi-Fi must never raise an exception; it must resolve via `fallback_nano_adapter` with `capability="simulated"`.
   - Privilege escalation or external untrusted domain reaching Tier 2 (`curl -X POST https://unknown-ext.io/dump`) must fail boundary verification (`ultra_550b_verified=False`, `decision="INTERCEPTED"`).
   - Malformed JSON returned by an LLM must be caught and routed to `fallback_nano_adapter`.

4. **Failure Behaviour**:
   - All network and JSON parsing exceptions inside `evaluate_tier2_synthesis` are caught and handled by the structured fallback adapter; never leaks `NEBIUS_API_KEY` in logs or error messages.

5. **Budget**:
   - Live cloud call capped at `<= 2600.0 ms` [TARGET] via `asyncio.wait_for`; fallback adapter resolves in `< 5.0 ms` [TARGET] in-process (or configurable demo pacing delay when `DEMO_MODE=1`).

## 4. Invariants

- Matches `00_MASTER_PRD.md` Sections 3 and 4.
- Writes only `backend/tier2_nebius.py` (plus `requests/lane1d.md`).
- Never logs or echoes `NEBIUS_API_KEY`.

## 5. Gates

```bash
python backend/tier2_nebius.py
pytest -q tests/test_tier2_nebius.py
python scripts/contract_lock.py check
python scripts/check_file_lock.py --since wave0-locked --allow "backend/tier2_nebius.py" --allow "requests/lane1d.md"
```