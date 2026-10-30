# AGENTS_03: `backend/tier1_jev.py`

**Companion PRD**: `documentation/prds/PRD_03_tier1_jev.md`
**Lane / worktree**: `lane1c` / `../wt/lane1c`   **Audit required**: no

## 1. Execution Blueprint

```yaml
goal: Implement backend/tier1_jev.py so all gates exit 0.
allowlist:
  - "backend/tier1_jev.py"
  - "requests/lane1c.md"
base_tag: wave0-locked
budget: p95 <= 100.0 ms (target; measured by benchmark)
gates:
  - python backend/tier1_jev.py
  - pytest -q tests/test_tier1_jev.py
  - python scripts/contract_lock.py check
  - python scripts/check_file_lock.py --since wave0-locked --allow "backend/tier1_jev.py" --allow "requests/lane1c.md"
```

## 2. Prompts

### Builder (Paste as is into OpenCode inside `../wt/lane1c`)

```text
/mega-system-architecture /aegisops-ai
ROLE: Builder. FILE LOCK: write ONLY backend/tier1_jev.py (and requests/lane1c.md for questions). Touching anything else is a failure.
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_03_tier1_jev.md
  3. tests/test_tier1_jev.py
RULES:
RP-CONTRACT
- Names, argument names, types, dict keys and enum values match PRD section 4 and contract.json character for character.
- Never edit backend/schemas.py, contract.json or contract.lock.
RP-HOTPATH
- Deterministic single-pass scoring for compute_blast_radius and compute_injection_risk.
- Return ALLOWED in Tier 1 if and only if both blast_radius_score < 20 and injection_risk_score < 20; otherwise escalate to Tier 2.
RP-SECURITY
- Any command with taint_flag=True or provenance="web/repo_payload" must score injection_risk_score >= 50 and never be auto-allowed in Tier 1.
DONE WHEN every gate in documentation/agents/AGENTS_03_tier1_jev.md section 1 exits 0. Paste each command and its exit code in your reply.
IF BLOCKED: do not guess names, keys or numbers. Append a QUESTION or NEEDS_DEP line to requests/lane1c.md and stop.
```