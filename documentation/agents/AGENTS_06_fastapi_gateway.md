# AGENTS_06: `backend/main.py`

**Companion PRD**: `documentation/prds/PRD_06_fastapi_gateway.md`
**Lane / worktree**: `Integrator` / `main` (Wave 2 after merging `lane1a..1e`)   **Audit required**: yes

## 1. Execution Blueprint

```yaml
goal: Implement backend/main.py wiring all Wave 1 modules, SSE stream, 180s demo choreography, and security hardening so all gates exit 0.
allowlist:
  - "backend/main.py"
  - "backend/__init__.py"
  - "requirements.txt"
  - "requests/integrator.md"
base_tag: wave1-merged
budget: p95 <= 2.0 ms Tier 0 HTTP loopback target
gates:
  - python backend/main.py --smoke
  - pytest -q tests/test_fastapi_gateway.py
  - pytest -q
  - python scripts/contract_lock.py check
```

## 2. Prompts

### Builder / Integrator (Paste as is into OpenCode / Antigravity in `main`)

```text
/super-mega-backend /atlas-contract /adversarial-reviewer
ROLE: Integrator & Gateway Builder. FILE LOCK: write ONLY backend/main.py, backend/__init__.py, and requirements.txt (and requests/integrator.md). Do not edit internals of Wave 1 modules.
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_06_fastapi_gateway.md
  3. backend/schemas.py
  4. tests/test_fastapi_gateway.py
RULES:
RP-CONTRACT
- Route paths, HTTP methods, request models, and response models match 00_MASTER_PRD.md section 4 and backend/schemas.py exactly.
RP-FASTAPI
- Pydantic v2 models imported from backend/schemas.py only. Async routes never block the event loop.
- Custom 422 RequestValidationError handler returns {error, field_paths} and never echoes submitted values.
- One worker. Startup state in a lifespan handler. POST /v1/demo/run-180s returns HTTP 404 unless DEMO_MODE=1, and debounces overlapping clicks using an asyncio.Lock.
- Bind 127.0.0.1:8000 by default. Allowlist CORS origins (http://localhost:3000, http://localhost:5173, plus PAROLE_CORS_ORIGINS).
DONE WHEN every gate in documentation/agents/AGENTS_06_fastapi_gateway.md section 1 exits 0. Paste each command and its exit code in your reply.
```

### Auditor (Paste into Grok Code after Builder gates pass)

```text
/adversarial-reviewer /super-mega-backend
ROLE: Auditor. Do not rewrite the module unless a high-severity finding exists.
INPUT BELOW: backend/main.py, PRD_06 section 3, and tests/test_fastapi_gateway.py.
TASK: Audit backend/main.py against the 10 Chaos Vectors (Reference 11.3: empty body, wrong content-type, 20,000-char strings, invalid UTF-8, 50 concurrent requests, client disconnect mid-SSE stream) and Law 9 security rules (127.0.0.1 bind, DEMO_MODE=1 guard, no 422 payload echo).
Maximum 5 findings, highest severity first. If a high finding exists, ALSO output the corrected file as:
=== FILE: backend/main.py ===
<complete file>
=== END ===
Keep every public signature and route unchanged.
RULES: RP-ADVERSARIAL, RP-FASTAPI, RP-SECURITY
```