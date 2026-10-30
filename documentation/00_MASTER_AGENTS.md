# Master Agents Guide (`00_MASTER_AGENTS.md`)

## 1. Roles, Squad Tools, and Wave Schedule

| Role | Assigned Tool | Does | Never Does |
| :--- | :--- | :--- | :--- |
| **Builder** | OpenCode (with GitHub Copilot inline) | Implements one module file against its `PRD_NN` and `tests/test_<slug>.py` inside its dedicated git worktree | Edits `tests/**`, `backend/schemas.py`, `contract.json`, `contract.lock`, or another lane's files |
| **Test Author** | Separate OpenCode or Antigravity session | Writes `tests/**` and `tests/oracles/**` from `TEST_SPEC.md` and `contract.json` in Wave 0b | Reads or edits implementation code under `backend/**` |
| **Auditor** | Grok Code (token-capped at `<= 6K` in / `<= 8K` out) | Adversarial review of security-critical and hot-path modules (`PRD_01`, `PRD_02`, `PRD_04`, `PRD_05`, `PRD_06`) | Rewrites files directly on disk without staging through `scripts/apply_incoming.py` |
| **Integrator** | Antigravity + Human Backend Lead (Role 1) | Owns `backend/main.py`, `backend/__init__.py`, `requirements.txt`, `parole_cli.py`, `benchmarks/run_benchmark.py`; merges worktrees sequentially | Edits internal logic of Wave 1 modules without running lane gates |
| **Verifier** | Automated Python Gate Scripts | Decides pass/fail strictly by exit code (`pytest`, `contract_lock.py`, `check_file_lock.py`, `prd_lint.py`) | Self-certifies in prose without an exit code |
| **Failover** | Cline / Secondary OpenCode Session | Re-runs the exact same Builder prompt if a Builder fails a gate twice | Widens the allowlist or weakens the test suite |

### Wave Execution Sequence

| Wave | Lanes | Worktree / Branch | Target Files | Exit Gate |
| :--- | :--- | :--- | :--- | :--- |
| **Wave 0a** | `0a` | `main` | `backend/schemas.py`, `contract.json`, module signature stubs | `python scripts/contract_lock.py write && git tag wave0-locked` |
| **Wave 0b** | `0b` | `../wt/lane0b` | `tests/**`, `tests/oracles/**` | `pytest --collect-only -q` succeeds; `pytest -q` fails only on `NotImplementedError` |
| **Wave 1** | `lane1a..1e` (Parallel) | `../wt/lane1a` .. `../wt/lane1e` | `kernel_guard.py`, `tier0_cache.py`, `tier1_jev.py`, `tier2_nebius.py`, `sse_broadcaster.py` | Module smoke test + `pytest -q tests/test_<slug>.py` + `contract_lock.py check` + `check_file_lock.py` |
| **Wave 2** | `Integrator` | `main` | `backend/main.py`, `parole_cli.py`, `benchmarks/run_benchmark.py`, `results.json`, `telemetry_fallback_v2.4.json` | Full `pytest -q` + `python benchmarks/run_benchmark.py` (`D0`) |

## 2. Shared Engineering Rules

- **Strict File Lock**: Write only your allowlisted file(s) plus `requests/<lane>.md`. Verify at the end of every session using `python scripts/check_file_lock.py --since wave0-locked --allow ...`.
- **Escalation Channel (`requests/<lane>.md`)**: Record any dependency need, question, or contract change request as a single-line entry:
  - `NEEDS_DEP: package==version reason`
  - `QUESTION: concise architectural question`
  - `CONTRACT: requested field or signature change (triggers CCP in Reference 8.4)`
- **Verification Discipline**: Never write `VERIFIED` or `DONE` in prose without pasting the exact gate commands and their `0` exit codes.
- **Token Ledger (`TOKEN_LEDGER.md`)**: Before invoking Grok Code for Auditor or Phase 2 Muscle Injection tasks, log `UTC_timestamp | tool | target_file | est_tokens_in (chars/3.5) | est_tokens_out` in `TOKEN_LEDGER.md`. Keep each request `<= 6,000` input tokens, `<= 8,000` output tokens, and `<= 3` files per bundle.
- **Slash Skill Hygiene**: Only use slash skills verified in `documentation/skills/SKILLS_AVAILABLE.md` (maximum 4 per prompt), paired with inline `RP-*` rule packs.