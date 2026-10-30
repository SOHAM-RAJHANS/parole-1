# AGENTS_04: `backend/tier2_nebius.py`

**Companion PRD**: `documentation/prds/PRD_04_tier2_nebius.md`
**Lane / worktree**: `lane1d` / `../wt/lane1d`   **Audit required**: yes

## 1. Execution Blueprint

```yaml
goal: Implement backend/tier2_nebius.py so all gates exit 0.
allowlist:
  - "backend/tier2_nebius.py"
  - "requests/lane1d.md"
base_tag: wave0-locked
budget: p95 <= 2600.0 ms (target; measured by benchmark)
gates:
  - python backend/tier2_nebius.py
  - pytest -q tests/test_tier2_nebius.py
  - python scripts/contract_lock.py check
  - python scripts/check_file_lock.py --since wave0-locked --allow "backend/tier2_nebius.py" --allow "requests/lane1d.md"
```

## 2. Prompts

### Builder (Paste as is into OpenCode inside `../wt/lane1d`)

```text
/mega-system-architecture /adversarial-reviewer /atlas-contract
ROLE: Builder. FILE LOCK: write ONLY backend/tier2_nebius.py (and requests/lane1d.md for questions). Touching anything else is a failure.
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_04_tier2_nebius.md
  3. tests/test_tier2_nebius.py
RULES:
RP-CONTRACT
- Names, argument names, types, dict keys and enum values match PRD section 4 and contract.json character for character.
- PolicyDiff fields (broad_antipattern, scoped_rule, super_120b_model, super_120b_counterfactual, ultra_550b_model, ultra_550b_verified, ultra_550b_audit_note) must match backend/schemas.py exactly.
RP-FASTAPI
- Use async httpx.AsyncClient wrapped in asyncio.wait_for(..., timeout=2.6) for Nebius Token Factory calls; never block the event loop with synchronous requests.
- When NEBIUS_API_KEY is absent or the cloud request times out, resolve cleanly via fallback_nano_adapter and tag capability="simulated" (or capability="live" when real Nebius API responds).
RP-SECURITY
- Never log or echo NEBIUS_API_KEY. Always run validate_scoped_rule_boundary on synthesized rules before marking ultra_550b_verified=True.
DONE WHEN every gate in documentation/agents/AGENTS_04_tier2_nebius.md section 1 exits 0. Paste each command and its exit code in your reply.
IF BLOCKED: do not guess names, keys or numbers. Append a QUESTION or NEEDS_DEP line to requests/lane1d.md and stop.
```

### Auditor (Paste into Grok Code after Builder gates pass)

```text
/adversarial-reviewer /atlas-contract
ROLE: Auditor. Do not rewrite the module unless a high-severity finding exists.
INPUT BELOW: backend/tier2_nebius.py, PRD_04 section 3, and tests/test_tier2_nebius.py.
TASK: Audit backend/tier2_nebius.py for: (1) blocking synchronous calls inside async functions, (2) unhandled exceptions when Nebius returns malformed JSON or HTTP 500/429, (3) boundary validator weaknesses allowing 0.0.0.0/0 or *:* rules, and (4) API key leakage in tracebacks.
Maximum 5 findings, highest severity first. If a high finding exists, ALSO output the corrected file as:
=== FILE: backend/tier2_nebius.py ===
<complete file>
=== END ===
Keep every public signature unchanged.
RULES: RP-ADVERSARIAL, RP-CONTRACT, RP-SECURITY
```