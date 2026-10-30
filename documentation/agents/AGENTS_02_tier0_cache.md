# AGENTS_02: `backend/tier0_cache.py` & `backend/picoclaw_cache.go`

**Companion PRD**: `documentation/prds/PRD_02_tier0_cache.md`
**Lane / worktree**: `lane1b` / `../wt/lane1b`   **Audit required**: yes

## 1. Execution Blueprint

```yaml
goal: Implement backend/tier0_cache.py and backend/picoclaw_cache.go so all gates exit 0.
allowlist:
  - "backend/tier0_cache.py"
  - "backend/picoclaw_cache.go"
  - "requests/lane1b.md"
base_tag: wave0-locked
budget: p95 <= 1.8 ms (target; measured by benchmark)
gates:
  - python backend/tier0_cache.py
  - pytest -q tests/test_tier0_cache.py
  - python scripts/contract_lock.py check
  - python scripts/check_file_lock.py --since wave0-locked --allow "backend/tier0_cache.py" --allow "backend/picoclaw_cache.go" --allow "requests/lane1b.md"
```

## 2. Prompts

### Builder (Paste as is into OpenCode inside `../wt/lane1b`)

```text
/super-mega-backend /mega-system-architecture /adversarial-reviewer
ROLE: Builder. FILE LOCK: write ONLY backend/tier0_cache.py and backend/picoclaw_cache.go (and requests/lane1b.md for questions). Touching anything else is a failure.
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_02_tier0_cache.md
  3. tests/test_tier0_cache.py
RULES:
RP-CONTRACT
- Names, argument names, types, dict keys and enum values match PRD section 4 and contract.json character for character.
- Never edit backend/schemas.py, contract.json or contract.lock.
RP-HOTPATH
- No blocking disk or network I/O in match_tier0_cache. Pre-parse CIDR networks via ipaddress.ip_network at promotion time.
- Pure-Python engine in tier0_cache.py must work standalone with zero external dependencies; picoclaw_cache.go provides the companion Go source.
RP-SECURITY
- Reject any command containing shell chaining (&&, ||, ;, |, backticks, $(), newlines, redirection) before matching safe rules.
DONE WHEN every gate in documentation/agents/AGENTS_02_tier0_cache.md section 1 exits 0. Paste each command and its exit code in your reply.
IF BLOCKED: do not guess names, keys or numbers. Append a QUESTION or NEEDS_DEP line to requests/lane1b.md and stop.
```

### Auditor (Paste into Grok Code after Builder gates pass)

```text
/adversarial-reviewer /super-mega-backend
ROLE: Auditor. Do not rewrite the module unless a high-severity finding exists.
INPUT BELOW: backend/tier0_cache.py, PRD_02 section 3, and tests/test_tier0_cache.py.
TASK: Test command smuggling, shell chaining bypasses, CIDR boundary off-by-one bugs, and path traversal inside URLs (such as curl https://10.0.4.12/api/v1/../../admin) against match_tier0_cache and promote_scoped_rule. For each finding give: severity (high/med/low), the EXACT failing input, expected vs actual, and line number.
Maximum 5 findings, highest severity first. If a high finding exists, ALSO output the corrected file as:
=== FILE: backend/tier0_cache.py ===
<complete file>
=== END ===
Keep every public signature unchanged.
RULES: RP-ADVERSARIAL, RP-CONTRACT, RP-HOTPATH
```