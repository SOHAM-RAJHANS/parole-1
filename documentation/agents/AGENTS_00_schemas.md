# AGENTS_00: `backend/schemas.py` & `contract.json`

**Companion PRD**: `documentation/prds/PRD_00_schemas.md`
**Lane / worktree**: `0a` / `main` (pre-branch baseline)   **Audit required**: no

## 1. Execution Blueprint

```yaml
goal: Implement backend/schemas.py, export contract.json, create Wave 0 signature stubs for backend modules, and lock contract.lock.
allowlist:
  - "backend/schemas.py"
  - "contract.json"
  - "contract.lock"
  - "backend/kernel_guard.py"
  - "backend/tier0_cache.py"
  - "backend/tier1_jev.py"
  - "backend/tier2_nebius.py"
  - "backend/sse_broadcaster.py"
  - "backend/main.py"
  - "parole_cli.py"
  - "benchmarks/run_benchmark.py"
  - "requests/0a.md"
base_tag: baseline
budget: p95 <= 0.1 ms validation target
gates:
  - python backend/schemas.py
  - python scripts/contract_lock.py write
  - python scripts/contract_lock.py check
  - python scripts/prd_lint.py documentation --check-signatures
```

## 2. Prompts

### Builder (Paste as is into OpenCode)

```text
/atlas-contract /super-mega-backend
ROLE: Builder (Wave 0a Contract Owner).
FILE LOCK: Write ONLY backend/schemas.py, contract.json, and the Wave 0 function signature stubs (raising NotImplementedError) for backend/kernel_guard.py, backend/tier0_cache.py, backend/tier1_jev.py, backend/tier2_nebius.py, backend/sse_broadcaster.py, backend/main.py, parole_cli.py, and benchmarks/run_benchmark.py (plus requests/0a.md if blocked).
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_00_schemas.md
  3. documentation/prds/PRD_01_kernel_guard.md through PRD_07_cli_and_benchmark.md (Section 3.2 function signatures only)
RULES:
RP-CONTRACT
- Names, argument names, types, dict keys and enum values match PRD section 4 and contract.json character for character.
- Do not add, rename, reorder or remove a field. If something is missing, write the question to requests/0a.md and stop.
RP-FASTAPI
- Pydantic v2 models with ConfigDict(extra="forbid") imported from backend/schemas.py.
- Running `python backend/schemas.py` must write `contract.json` with `"contract_version": 1` and exit 0.
DONE WHEN every gate in documentation/agents/AGENTS_00_schemas.md section 1 exits 0, followed by `python scripts/contract_lock.py write`. Paste each command and its exit code in your reply.
```