# PRD_06: `backend/main.py`

**Target File(s)**: `backend/main.py`
**Lane / role**: `Integrator` / Integrator + Auditor   **Audit required**: yes
**Design reference**: Cloudflare Radar API + Stripe Webhook Streaming Gateway [SOURCE: Dossier_01 p1]

## 1. Purpose and Role

Serves as the unified FastAPI Sovereign Gateway orchestrating Modules 0a through 5. Exposes `POST /v1/policy/evaluate`, `GET /v1/policy/stream`, `POST /v1/policy/approve-diff`, `GET /v1/metrics/summary`, `POST /v1/demo/run-180s`, and `GET /health`. Enforces non-blocking Tier 2 execution (emitting preliminary `"SYNTHESIZING_TIER_2"` SSE status immediately so Tier 0 `< 2 ms` [TARGET] requests continue concurrently without head-of-line blocking), guards mutating demo routes behind `DEMO_MODE=1`, allowlists CORS origins, and sanitizes 422 validation errors so raw malicious payloads are never echoed back.

## 2. Bound Skills (Verified in `SKILLS_AVAILABLE.md`)

| Slash | Rule Pack if Skill is Missing | Why Here |
| :--- | :--- | :--- |
| `/super-mega-backend` | `RP-FASTAPI`, `RP-HOTPATH` | Lifespan state initialization, non-blocking async routing, and SSE streaming |
| `/atlas-contract` | `RP-CONTRACT`, `RP-FASTAPI` | Strict Pydantic v2 response validation against `backend/schemas.py` |
| `/adversarial-reviewer` | `RP-SECURITY`, `RP-ADVERSARIAL` | 422 payload-echo suppression, `DEMO_MODE=1` route gating, and 10-vector chaos resilience |

## 3. Specification

1. **Data and Constants**:
   - `DEMO_MODE: bool = os.getenv("DEMO_MODE", "1") == "1"`
   - `ALLOWED_ORIGINS: list[str]` defaults to `["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"]` plus any comma-separated origins in `os.getenv("PAROLE_CORS_ORIGINS", "")`.
   - `_demo_lock: asyncio.Lock` preventing overlapping 180s demo choreography runs on rapid button clicks.

2. **Functions**:
   - `async def evaluate_policy(req: AgentActionRequest) -> AgentActionEvent:` (`POST /v1/policy/evaluate`)
     1. Starts high-resolution timer `time.perf_counter_ns()`.
     2. Calls `kernel_guard.evaluate_kernel_gate(req.command, req.provenance, bool(req.taint_flag))`. If `blocked` is `True`, builds `AgentActionEvent` with `tier_resolved="KERNEL_HARD_DENY"`, `decision="INTERCEPTED"`, `cost_usd=0.0`, broadcasts via `sse_broadcaster.broadcast_event("evaluate", ...)`, records metrics, and returns immediately.
     3. Calls `tier0_cache.match_tier0_cache(req.command)`. If `hit` is `True`, builds `AgentActionEvent` with `tier_resolved="TIER_0"`, `decision="ALLOWED"`, `cost_usd=0.0`, broadcasts, records metrics, and returns.
     4. If `chained_rejected` is `False`, calls `tier1_jev.evaluate_tier1_jev(req.command, target_resource, req.provenance, effective_taint)`. If `allow` is `True`, builds `AgentActionEvent` with `tier_resolved="TIER_1"`, `decision="ALLOWED"`, `cost_usd=0.0003`, broadcasts, records metrics, and returns.
     5. Otherwise escalates to Tier 2: immediately broadcasts preliminary SSE event `{"status": "SYNTHESIZING_TIER_2", "command": req.command, "target_resource": target_resource}` [SOURCE: Dossier_01 p3], awaits `tier2_nebius.evaluate_tier2_synthesis(req.command, target_resource, auto_promote=req.auto_promote)`, promotes the scoped rule into `tier0_cache` if `decision == "AUTO_PROMOTED"`, broadcasts the final resolved `AgentActionEvent` (`tier_resolved="TIER_2"`, `cost_usd=0.008`), records metrics, and returns.
   - `async def stream_policy_events(request: Request) -> StreamingResponse:` (`GET /v1/policy/stream`) sends `retry: 2000\n\n`, flushes replay buffer (or `Last-Event-ID`), yields formatted SSE frames from the subscriber queue, sends `: heartbeat\n\n` every `10.0` seconds on queue timeout, and always calls `sse_broadcaster.unsubscribe(sub_id)` inside `finally:`.
   - `async def approve_policy_diff(req: ApproveDiffRequest) -> ApproveDiffResponse:` (`POST /v1/policy/approve-diff`) calls `tier0_cache.promote_scoped_rule(req.scoped_rule)`, broadcasts `"rule_promoted"`, and if `req.trigger_followup` is `True`, evaluates the canonical follow-up command `curl -s https://10.0.4.19/api/v1/orders` (which resolves in `TIER_0` under `1.8 ms` [TARGET]) and includes it in `followup_event` [SOURCE: Dossier_02 p5].
   - `async def metrics_summary() -> MetricsSummaryResponse:` (`GET /v1/metrics/summary`) returns `sse_broadcaster.get_metrics_summary(active_tier0_rules=tier0_cache.get_active_rules())`.
   - `async def run_demo_180s() -> dict:` (`POST /v1/demo/run-180s`) returns HTTP 404 if `os.getenv("DEMO_MODE", "1") != "1"`. If a demo is already in progress (`_demo_lock.locked()`), returns `{"status": "already_running", "acts_scheduled": 3}` cleanly (debounced). Otherwise runs the 3-act sequence from Dossier 01 Subtask 5.2 (Act 1 routine `git status`, `pytest tests/unit`, `cat src/config.ts`; Act 2 poisoned README `169.254.169.254` SSRF with `web/repo_payload` + `tar -czf - ~/.ssh/* ~/.aws/*`; Act 3 `10.0.4.12/api/v1/users` Tier 2 synthesis + promotion + `10.0.4.19/api/v1/orders` Tier 0 hit).
   - `async def health_check() -> dict:` (`GET /health`) returns `{"status": "ok", "contract_version": 1, "active_tier0_rules": len(tier0_cache.get_active_rules())}`.

3. **Edge Cases**:
   - Rapidly calling `POST /v1/demo/run-180s` 5 times in 1 second must debounce cleanly without duplicating stream events.
   - Sending invalid JSON, wrong field types, or a 20,000-character `command` returns HTTP 422 with `{"error": "validation_error", "field_paths": [...]}` and never echoes the raw payload string.
   - While Tier 2 is synthesizing (`1500 ms` [TARGET]), concurrent `POST /v1/policy/evaluate` requests for `git status` must still complete in `< 5 ms` [TARGET].

4. **Failure Behaviour**:
   - Custom `@app.exception_handler(RequestValidationError)` returns HTTP 422 `ValidationErrorResponse` without echoing user input. Invalid rule syntax in `/v1/policy/approve-diff` returns HTTP 400 with structured error detail.

5. **Budget**:
   - In-process and loopback Tier 0 evaluation p95 `<= 2.0 ms` [TARGET].

## 4. Invariants

- Matches `00_MASTER_PRD.md` Sections 3 and 4.
- Owned by the Integrator role (`backend/main.py`, `backend/__init__.py`).
- Default `if __name__ == "__main__":` binds `127.0.0.1` on port `8000` with a single worker (`workers=1`).

## 5. Gates

```bash
python backend/main.py --smoke
pytest -q tests/test_fastapi_gateway.py
python scripts/contract_lock.py check
```