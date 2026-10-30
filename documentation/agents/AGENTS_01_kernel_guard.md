# AGENTS_01: `backend/kernel_guard.py`, `backend/nemoclaw_sandbox.sh` & `backend/seccomp_profile.json`

**Companion PRD**: `documentation/prds/PRD_01_kernel_guard.md`
**Lane / worktree**: `lane1a` / `../wt/lane1a`   **Audit required**: yes

## 1. Execution Blueprint

```yaml
goal: Implement backend/kernel_guard.py, backend/nemoclaw_sandbox.sh, and backend/seccomp_profile.json so all gates exit 0.
allowlist:
  - "backend/kernel_guard.py"
  - "backend/nemoclaw_sandbox.sh"
  - "backend/seccomp_profile.json"
  - "requests/lane1a.md"
base_tag: wave0-locked
budget: p95 <= 0.5 ms (target; measured by benchmark)
gates:
  - python backend/kernel_guard.py
  - pytest -q tests/test_kernel_guard.py
  - python scripts/contract_lock.py check
  - python scripts/check_file_lock.py --since wave0-locked --allow "backend/kernel_guard.py" --allow "backend/nemoclaw_sandbox.sh" --allow "backend/seccomp_profile.json" --allow "requests/lane1a.md"
```

## 2. Prompts

### Builder (Paste as is into OpenCode inside `../wt/lane1a`)

```text
/aegisops-ai /adversarial-reviewer /atlas-contract
ROLE: Builder. FILE LOCK: write ONLY backend/kernel_guard.py, backend/nemoclaw_sandbox.sh, and backend/seccomp_profile.json (and requests/lane1a.md for questions). Touching anything else is a failure.
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_01_kernel_guard.md
  3. tests/test_kernel_guard.py
RULES:
RP-CONTRACT
- Names, argument names, types, dict keys and enum values match PRD section 4 and contract.json character for character.
- Never edit backend/schemas.py, contract.json or contract.lock.
RP-HOTPATH
- No blocking disk or network I/O in the request path. Precompile all regexes and IP networks at import time.
- Measure latency with time.perf_counter_ns().
RP-SECURITY
- Treat every input as untrusted: bound length, strip null/zero-width chars, decode Base64/hex pipes in memory, never eval/exec/subprocess input.
- Normalize decimal (2852039166), hex (0xa9fea9fe), octal (0251.0376.0251.0376), and IPv6 ([::ffff:169.254.169.254], fd00:ec2::254) metadata IPs deterministically.
DONE WHEN every gate in documentation/agents/AGENTS_01_kernel_guard.md section 1 exits 0. Paste each command and its exit code in your reply.
IF BLOCKED: do not guess names, keys or numbers. Append a QUESTION or NEEDS_DEP line to requests/lane1a.md and stop.
```

### Auditor (Paste into Grok Code after Builder gates pass)

```text
/adversarial-reviewer /aegisops-ai
ROLE: Auditor. Do not rewrite the module unless a high-severity finding exists.
INPUT BELOW: backend/kernel_guard.py, PRD_01 section 3, the handshake row for kernel_guard, and tests/test_kernel_guard.py.
TASK: Act as an offensive red-team penetration tester trying to bypass kernel_guard.py to reach 169.254.169.254, ~/.ssh/id_rsa, or ~/.aws/credentials, or exfiltrate data when provenance="web/repo_payload". For each finding give: severity (high/med/low), the EXACT failing input command string, expected vs actual, and line number.
Maximum 5 findings, highest severity first. No style comments. If a high finding exists, ALSO output the corrected file as:
=== FILE: backend/kernel_guard.py ===
<complete file>
=== END ===
Keep every public signature unchanged.
RULES: RP-ADVERSARIAL, RP-CONTRACT, RP-SECURITY
```