# HACKATHON BACKEND KING (v3.0) // COMPLETE UPGRADED SKILL & ENFORCEMENT SCRIPTS ARCHIVE

**Saved Skill Name in Gemini Skills Menu**: `hackathon-backend-king` (Upgraded from `hackathon-backend-architect` to v3.0)

## Bundled Files in `hackathon-backend-king` (v3.0)

1. `SKILL.md` — Master v3.0 Orchestrator (The 10 Core Engineering Principles, Stage 0–8 Workflow, Evidence Tags, Independent Test Author Wave 0b, Git Worktree Ownership, and `D0..D3` Definition of Done)
2. `references/PHASE1_AND_PHASE2_BLUEPRINTS.md` — Unabridged v3.0 Reference Manual (`SKILLS_AVAILABLE.md` inventory, `RP-*` Inline Rule Packs, `ASSUMPTIONS.md`, `RUBRIC_MAP.md`, `00_MASTER_PRD.md`, `PRD_NN.md`, `TEST_SPEC.md`, Role-Based `AGENTS_NN.md`, Contract Change Protocol, Time-Scaled Schedule, Token-Capped Staged Muscle Injection, `results.json` Schema, and S1–S12 / D1–D8 Defect Register)
3. `scripts/check_file_lock.py` — Git worktree allowlist verifier (`[lock] OK` vs `VIOLATION`)
4. `scripts/contract_lock.py` — SHA-256 `contract.lock` writer and drift detector
5. `scripts/prd_lint.py` — Anti-slop, unreplaced placeholder, fluff-word, and evidence-tag linter (`--check-signatures`)
6. `scripts/apply_incoming.py` — Non-destructive staged code installer (`_incoming/` -> AST syntax check -> `_backups/<UTC>/` -> gate command -> automatic rollback on failure)
7. `scripts/workspace_organizer_template.py` — v3.0 Non-destructive workspace setup script (with all S1–S12 fixes applied: `--slug` required, dry-run default + `--apply`, `SHGetKnownFolderPath` Desktop resolution, `.incoming` conflict safety, `requirements.lock` export, and git baseline commit)
8. `scripts/phase2_dedup_and_doctor_template.py` — v3.0 AST stub function detector, same-folder copy deduplicator, and contract/pytest readiness doctor (with all D1–D8 fixes applied)

## Part 1: `SKILL.md`

```markdown
---
name: hackathon-backend-king
description: Hackathon Backend King v3.0 (Backend Architect & Multi-Agent Build System). Turns a hackathon brief, dossier PDF/MD, or starter repository into a structured multi-agent build workflow with parallel execution tracks, verified metrics, and automated quality gates. Generates the rubric map, machine-locked schema contract, tests-first per-module PRDs, role-based AGENTS guides with verified /slash skill bindings and inline rule packs, git-worktree file-scope waves, a non-destructive workspace setup script, a time-scaled Phase 2 playbook (dedup doctor, staged module completion with rollback, live hosting, remote VM / LinuxONE proof, 180-second demo recording), and a results.json single source of truth. Use when starting, rescuing, or planning a hackathon or backend project, or when the user mentions Hackathon Backend King, Master PRD, PRD_XX, AGENTS_XX, Commander Playbook, slash skills, low-token Grok workflow, or a session card.
---

# Hackathon Backend King (v3.0 Architecture & Multi-Agent Build System)

This skill provides a complete engineering system to plan, build, verify, and record a hackathon backend project using multiple AI coding tools in parallel without file collisions, unverified metric claims, or configuration drift.

All templates, role prompts, schemas, and enforcement scripts are in `references/PHASE1_AND_PHASE2_BLUEPRINTS.md` (referred to as **the Reference** below) and `scripts/`. Open one section of the Reference at a time as needed for the active stage; never paste the entire Reference into a coding assistant at once.

## Key Engineering Upgrades in v3.0

| v2 Limitation | v3.0 Upgrade in `hackathon-backend-king` |
| :--- | :--- |
| Metrics (p95, pass rate, speedup) were pre-written into fallback JSON and UI before code ran. | All numbers start as `[TARGET]` until a benchmark run produces `results.json`. The UI, deck, and reports read directly from `results.json` (Principles 1 and 8). |
| `/slash` skills were assumed to exist on disk without checking. | Run a skill inventory first (`SKILLS_AVAILABLE.md`). Bind only verified skills (max 4 per prompt) and always pair with an inline rule pack (`RP-*`) as a self-contained fallback (Principle 5). |
| File scopes were requested in text prompts without git verification. | Use one git worktree per parallel lane plus `scripts/check_file_lock.py` and `scripts/contract_lock.py` as automated exit-code gates (Principle 4). |
| The same session wrote both the implementation and its unit tests. | A separate Test Author lane writes `tests/**` from `TEST_SPEC.md` using independent oracles before Builders start (Principle 3). |
| A single large script updated multiple files without staging or rollback. | Run the AST Doctor first (`phase2_dedup_and_doctor_template.py`), generate scoped per-module completion bundles, stage in `_incoming/`, and apply via `scripts/apply_incoming.py` with backup and automatic rollback on gate failure (Stage 6). |
| 4 repetitive prompts per file across 10 files. | One Builder prompt per module, plus an Auditor prompt only for high-risk or performance-critical modules. Verification is performed by deterministic scripts (Stage 3). |
| Binding `0.0.0.0`, wildcard CORS `*`, and always-on demo mutation routes. | Bind `127.0.0.1` by default, use SSH port forwarding for remote VMs, gate demo mutation routes behind `DEMO_MODE=1`, and allowlist CORS origins (Principle 9, Reference 11). |
| Setup script created mirror doc copies, used broad filename deduplication, and overwrote files on re-run. | Enforce the 13 Script Safety Invariants (Stage 4) and S1-S12 / D1-D8 fixes in `scripts/workspace_organizer_template.py` and `scripts/phase2_dedup_and_doctor_template.py`. |
| Mock disclaimers were removed before live data was connected. | Display an explicit `LIVE` / `REPLAY` / `SIMULATED` mode badge in the UI driven by actual connection and capability state. |
| Untested placeholders or untagged numbers in documentation. | Enforce evidence tags (`[TARGET]`, `[MEASURED: field]`, `[SOURCE: ref]`, `[ASSUMPTION]`, `[UNVERIFIED]`, `[OPEN]`) verified by `scripts/prd_lint.py` (Principle 10). |
| Fixed 5-layer / 10-file template and fixed 120-minute schedule. | Derive 6 to 12 modules from the specific project domain and scale Phase 1 and Phase 2 schedules to the actual remaining time `T` (Reference 9.1). |

## The 10 Core Engineering Principles

1. **Rubric-First, Evidence-Tagged Metrics**: Every deliverable maps to a judging criterion in `RUBRIC_MAP.md`. Every numeric claim in documentation, UI, or slides carries an explicit tag: `[TARGET]`, `[MEASURED: field]`, `[SOURCE: ref]`, `[ASSUMPTION]`, `[UNVERIFIED]`, or `[OPEN]`.
2. **Machine-Checked Schema Contract Before Code**: `backend/schemas.py` -> `contract.json` -> `contract.lock` (SHA-256 digest via `scripts/contract_lock.py`). Handshake tables are generated from `schemas.py`. Any post-lock update follows the Contract Change Protocol (`CCP`).
3. **Independent Tests Before Implementation**: A separate Test Author session writes `tests/**` from `TEST_SPEC.md` using independent test vectors or reference oracles in `tests/oracles/`. Builders do not modify test files.
4. **Git-Enforced File Ownership**: Use one git worktree per parallel lane (`../wt/<lane>`), verify changed paths at the end of every lane with `scripts/check_file_lock.py`, and assign shared files (`main.py`, `requirements.txt`, `package.json`) to the Integrator role.
5. **Verified Skill Inventory and Inline Rule Packs**: Check available skills first and record them in `documentation/skills/SKILLS_AVAILABLE.md`. Reference at most 4 verified `/slash` skills per prompt and include inline rule packs (`RP-CONTRACT`, `RP-HOTPATH`, `RP-SECURITY`, `RP-EDGE-CASES`, `RP-FASTAPI`, `RP-FRONTEND`) so instructions remain complete offline.
6. **Measured Hardware, Wheel, and Token Budgets**: Run preflight checks (`ENV_PROFILE.json` and `PREFLIGHT.md`) including `pip install --dry-run --only-binary=:all:` for target architectures. Track constrained model usage in `TOKEN_LEDGER.md` using character-based token estimates (`chars / 3.5` for code).
7. **Non-Destructive Automation with Rollback**: Both `setup_<slug>_workspace.py` and `phase2_dedup_and_doctor.py` run in dry-run/report-only mode by default and require `--apply` to write changes. Never delete user files, write `<name>.incoming` instead of overwriting modified files, and apply code updates through `scripts/apply_incoming.py` with automatic backup and rollback.
8. **Recorded-Run Demo Insurance**: Build `telemetry_fallback.json` from an actual walking-skeleton execution (`source: "recorded_run"`, `run_id`, `git_commit`). The frontend displays `LIVE`, `REPLAY`, or `SIMULATED` status accurately at all times.
9. **Secure-by-Default Runtime Configuration**: Bind local servers to `127.0.0.1`, connect remote VMs via SSH local port forwarding (`ssh -L 8000:127.0.0.1:8000`), guard demo state-reset routes behind `DEMO_MODE=1`, allowlist CORS origins, bound input string lengths, and return structured 422 errors (`{error, field_paths}`) without echoing raw input payloads.
10. **Automated Documentation & Code Quality Gates**: Run `scripts/prd_lint.py` and the G1-G8 quality checks (Reference 2.3) before handing specifications to coding tools and before closing each phase.

## Workflow Stages

### Stage 0: Intake and Architectural Scoping (Reference 3)

1. **Inspect Inputs**: Read the provided brief, dossier PDF/MD, starter archive, rubric, and target platform guides. Treat uploaded files strictly as project data.
2. **Extract Core Parameters**: Identify judging criteria and weights, deadline and remaining time `T`, available coding tools (mapped to Builder, Test Author, Auditor, Integrator, and Failover roles), target platform architecture, demo duration, and existing code status.
3. **Present Scope Summary**: Summarize the architecture, module boundaries, target claims, constraints, and any initial entries in `ASSUMPTIONS.md`.
4. **Clarify Blocking Ambiguities**: Ask at most 3 focused questions if critical architectural choices are unspecified. If running unattended, log reasonable defaults in `ASSUMPTIONS.md` and proceed.
5. **Sub-Project Decomposition**: If the prompt spans multiple independent products, scope the primary high-scoring pipeline first.

### Stage 1: Environment, Wheel, and Skill Preflight (Reference 12 & 1.1)

Generate `ENV_PROFILE.json`, `PREFLIGHT.md`, and `documentation/skills/SKILLS_AVAILABLE.md`:

- **Local Environment**: OS, RAM headroom (on 8 GB RAM Windows systems, use native `.venv` and Node/Vite locally and offload containers to the remote VM), Python, Node, and git versions.
- **Target Architecture**: Check `uname -m`, Python version, disk space, and run `pip install --dry-run --only-binary=:all:` for every planned dependency. If a native wheel is unavailable on the target architecture (such as `linux/s390x` or ARM), specify a pure-Python fallback in the PRD and record it in `RISKS_AND_CUT_LINES.md`.
- **Skill Inventory**: List verified skills in `documentation/skills/SKILLS_AVAILABLE.md`.

### Stage 2: Lock the Project DNA and Risk Cut Lines (Reference 3, 4 & 9.3)

Define and tag the 5 foundational project artifacts:

1. **Platform & Sponsor Integration**: The specific hardware or cloud capability demonstrated live.
2. **Modular Pipeline (6 to 12 Modules)**: Single-responsibility modules derived from the project domain, each with an explicit `[TARGET]` latency or accuracy budget.
3. **Claims Table**: Every quantitative claim (`C1`, `C2`, ...) mapped to the exact dotted field in `results.json` that will measure it.
4. **Cross-Module Handshakes**: Exact `module.func(arg: type) -> return_type` signatures and REST/SSE routes exported from `schemas.py`.
5. **Demo Plan & Cut Lines**: Scene breakdown, `LIVE` / `REPLAY` / `SIMULATED` badge logic, and `RISKS_AND_CUT_LINES.md` (with hard cut lines at 45%, 70%, and 88% of total time `T`).

### Stage 3: Generate Specifications, Test Specs, and Role Guides (Reference 4-7)

- `documentation/00_MASTER_PRD.md` (Sections 3 and 4 combined <= 4,000 tokens) and `documentation/prds/PRD_01..NN.md` (<= 2,500 tokens each).
- `documentation/TEST_SPEC.md`: Independent test cases and oracle definitions for each module.
- `documentation/00_MASTER_AGENTS.md` and `documentation/agents/AGENTS_01..NN.md`: Contains the execution YAML blueprint, one scoped **Builder prompt** per module (with verified `/slash` skills + inline `RP-*` rules), and an **Auditor prompt** for security-critical or hot-path modules.
- Store each document in one canonical path under `documentation/` (zero duplicate mirror copies).
- Validate all generated Markdown with `python scripts/prd_lint.py documentation`.

### Stage 4: Generate Non-Destructive Workspace Setup Script (Reference 15.1)

Using `scripts/workspace_organizer_template.py`, generate `setup_<slug>_workspace.py` adhering to all 13 safety invariants:

1. Python 3.9+ Standard Library only (`from __future__ import annotations`).
2. **Dry-run by default**; mutates disk only when `--apply` is passed.
3. Requires `--slug <project-slug>` (no hardcoded project name).
4. Writes only inside `Desktop/<slug>/`; copies rather than moves or deletes source files in `Downloads/`.
5. Scans top-level of `Downloads/` and `Desktop/` only for files matching the manifest or `--slug` modified within `--since-hours` (default 48).
6. Never overwrites an existing file whose content differs; writes `<filename>.incoming` beside it and logs the notice.
7. Places each document in a single canonical location (`documentation/prds/`, `documentation/agents/`, `documentation/skills/`).
8. Deduplicates only `name (1).ext` browser copy files that have a byte-identical canonical sibling in the **same folder**; never touches `__init__.py`, `.gitkeep`, lockfiles, or `LICENSE`.
9. Uses `os.walk` with in-place directory pruning (`.git`, `.venv`, `node_modules`, `__pycache__`).
10. Installs dependencies from `requirements.txt` and exports `requirements.lock` via `pip freeze`.
11. Verifies the SHA-256 checksum of any embedded LZMA bundle before unpacking.
12. Resolves the Windows Desktop folder via `SHGetKnownFolderPath`, then Registry, then OneDrive paths, and logs all actions to `setup.log`.
13. Initializes git, writes `.gitignore` (excluding `.venv/`, `node_modules/`, `__pycache__/`, `_incoming/`, `_backups/`, `_duplicates_archive/`, `.env`), and commits `baseline`.

### Stage 5: Execute Phase 1 Build Waves with Worktree Gates (Reference 8 & 9)

Start each wave only after the previous wave's gate exits with code `0`:

| Wave | Role | Allowed Write Scope | Exit Gate Command |
| :--- | :--- | :--- | :--- |
| **Wave 0a (Contract)** | Builder | `backend/schemas.py`, `contract.json`, handshake tables, module signature stubs (`raise NotImplementedError`) | `python scripts/contract_lock.py write` + git commit & tag `wave0-locked` |
| **Wave 0b (Tests)** | Test Author (separate session) | `tests/**` (and `tests/oracles/**`) | `pytest --collect-only -q` succeeds; `pytest -q` fails only on `NotImplementedError` / `AssertionError` |
| **Wave 1 (Modules)** | Parallel Builders (one git worktree `../wt/<lane>` per lane) | Assigned module file(s) + `requests/<lane>.md` | `python <module>.py` + `pytest -q tests/test_<slug>.py` + `check_file_lock.py` + `contract_lock.py check` |
| **Wave 2 (Integration)** | Integrator | `backend/main.py`, `backend/__init__.py`, `requirements.txt`, `<slug>_cli.py`, `benchmarks/run_benchmark.py` | Full `pytest -q` + walking skeleton run producing initial `results.json` and `telemetry_fallback.json` (`D0`) |
| **Wave 3 (Frontend)** | Builder | `frontend/**` | UI displays `LIVE` / `REPLAY` / `SIMULATED` badge and reads all metrics from `results.json` or live SSE (`D1`) |

### Stage 6: Execute Phase 2 — Doctor, Staged Completion, Hardening & Recording (Reference 10-13)

Scale time blocks proportionally to remaining time `T` (Reference 9.1):

1. **Run the AST Doctor (`scripts/phase2_dedup_and_doctor_template.py`)**: Default report-only mode inspects AST function bodies to flag `STUB` (`pass`, `...`, constant return, `NotImplementedError`) or `NEEDS_MUSCLE` (`TODO`/`FIXME`), checks `contract_lock.py check`, and writes `PHASE2_DOCTOR_REPORT.json` listing exact `stub_functions`.
2. **Staged Module Completion (`scripts/apply_incoming.py`)**: For any module flagged `STUB` or `NEEDS_MUSCLE`, send a self-contained prompt (`<= 6K` tokens in, `<= 8K` tokens out, max 3 files per request, logged in `TOKEN_LEDGER.md`) containing only that file, its PRD Section 3, its handshake rows, and its test cases. Save the model's `=== FILE: path ===` reply to `reply.txt` and apply with `python scripts/apply_incoming.py --allow "backend/*.py" --bundle reply.txt --atomic --gate "pytest -q && python scripts/contract_lock.py check"`.
3. **Runtime & Security Hardening (Reference 11)**: Verify bounded per-subscriber SSE queues (`maxsize=256` with explicit oldest-drop notification), `Last-Event-ID` replay deque, `127.0.0.1` binding, `DEMO_MODE=1` guard on mutating demo routes, 422 handler without payload echo, and the 10-vector fuzz suite.
4. **Remote Architecture Proof (Reference 12.2)**: Copy only required source files via `scp` to the remote VM, run `python benchmarks/run_benchmark.py --mode remote`, capture `uname -m` and `results.remote.json`, and tunnel via `ssh -L 8000:127.0.0.1:8000` (`D2`).
5. **180-Second Demo Recording (Reference 13)**: Use a fixed `DEMO_SEED`, rehearse twice with a stopwatch, record at least two full takes at 1080p60 plus a secondary backup capture, and verify the exported video end-to-end (`D3`).

### Stage 7: Automated Benchmark Report & Session Card (Reference 11.5 & 14)

- `benchmarks/run_benchmark.py` writes `results.json` and generates `BENCHMARK_REPORT.md` automatically, computing `PASS` only when every claim's `met` field is `true`.
- Write a concise project session card to `documentation/skills/SESSION_<slug>.md` (`<= 120` lines, Reference 14) recording the project's file matrix, claim IDs, verified skills, hardware profile, and contract version without modifying the installed base skill.

## Bundled Files in This Skill Package

- `references/PHASE1_AND_PHASE2_BLUEPRINTS.md`: Complete v3.0 reference manual with all templates, rule packs, prompts, runtime specs, and defect registers.
- `scripts/check_file_lock.py`: Git-based file allowlist gate for parallel lanes.
- `scripts/contract_lock.py`: SHA-256 contract freeze and drift checker (`contract.lock`).
- `scripts/prd_lint.py`: Automated anti-slop, placeholder, and evidence-tag linter for generated Markdown docs.
- `scripts/apply_incoming.py`: Staged file installer with AST syntax check, timestamped backups (`_backups/`), gate execution, and automatic rollback.
- `scripts/workspace_organizer_template.py`: v3.0 non-destructive workspace organizer and `.venv` setup script (with S1-S12 fixes applied).
- `scripts/phase2_dedup_and_doctor_template.py`: v3.0 AST stub detector, same-folder copy deduplicator, and contract/test readiness auditor (with D1-D8 fixes applied).
```

## Part 2: `references/PHASE1_AND_PHASE2_BLUEPRINTS.md`

# Hackathon Backend King: Phase 1 and Phase 2 Blueprints (v3.0)

Companion to `SKILL.md`. Open one section at a time when a stage points here. Never paste this whole file into a coding agent.

**Contents**
1. Skill binding: inventory, routing, inline rule packs
2. Evidence tags and slop control
3. Intake templates (ASSUMPTIONS, RUBRIC_MAP)
4. Master PRD template
5. Per-module PRD template
6. TEST_SPEC template (tests before code)
7. AGENTS templates: roles, Builder, Auditor, Test Author, Integrator
8. Enforcement: gitignore, worktrees, shared files, Contract Change Protocol, scripts
9. Phase 1 playbook, time scaling, cut lines
10. Phase 2: doctor, surgical muscle injection, token caps
11. Runtime hardening: SSE, security, fuzzing, latency, results.json, fallback
12. Preflight and remote-target proof
13. Demo recording
14. Session card template
15. Defect register for the original templates and scripts

Template convention: templates that themselves contain code fences are wrapped in `~~~~`. Inside a template, `{{NAME}}` marks a value **you must fill before the file leaves your hands**. A `{{` surviving in any generated file is a bug, and `prd_lint.py` fails on it.

---

## 1. Skill binding: inventory, routing, inline rule packs

### 1.1 Inventory (Stage 1, always first)

The user's skills live in a folder on their PC (called POWERHOUSE). It is not a cloud library you can query. So:

1. Ask for, or read, the folder listing. In a chat without disk access, ask the user to run `dir /b <skills folder>` (Windows) or `ls <skills folder>` and paste the names.
2. Write `documentation/skills/SKILLS_AVAILABLE.md`: one line per skill actually present (`name`, one-line purpose).
3. A slash command may appear in a prompt **only if its name is in that list**. Any name not in the list is replaced by its inline rule pack (1.3).
4. At most **4 slash skills per prompt**. More dilutes the context and costs tokens for little gain.
5. Never copy a skill's full text into a PRD. Reference the skill by name; the inline rule pack is the offline fallback.

### 1.2 Preferred routing (use the name only if present in 1.1)

| Work item | Preferred slash skills | Rule pack if absent |
| :--- | :--- | :--- |
| Pre-code spec lock | `/brainstorming` `/not-a-vibe-coder` `/squad-dossier-architect` | RP-CONTRACT |
| Wave 0 contract and schemas | `/atlas-contract` `/pydantic-models-py` `/super-mega-backend` | RP-CONTRACT, RP-FASTAPI |
| Crypto, scoring, core algorithms | `/mega-cybersecurity` `/super-mega-backend` `/adversarial-reviewer` | RP-HOTPATH, RP-SECURITY |
| Ingest, parsing, policy engines | `/super-mega-backend` `/mega-system-architecture` `/mega-cybersecurity` | RP-HOTPATH, RP-SECURITY |
| Ledger, audit chain, deployment | `/super-mega-hackathon` `/mega-system-architecture` | RP-HOTPATH |
| Gateway, SSE, API | `/mega-backend-systems` `/python-fastapi-development` `/fastapi-pro` | RP-FASTAPI, RP-SECURITY |
| CLI and benchmark runner | `/super-mega-hackathon` `/e2e-testing` `/vibe-code-auditor` | RP-ADVERSARIAL |
| Frontend bridge and polish | `/super-mega-frontend` `/frontend-design` `/antislop-copywriting` | RP-FRONTEND |
| Parallel swarm and dedup | `/subagent-orchestrator` `/dispatching-parallel-agents` `/vibe-code-auditor` | none (this file is the playbook) |
| Review of finished modules | `/adversarial-reviewer` `/vibe-code-auditor` | RP-ADVERSARIAL |

### 1.3 Inline rule packs (paste under `RULES:` in prompts)

~~~~text
RP-CONTRACT
- Names, argument names, types, dict keys and enum values match PRD section 4 and contract.json character for character.
- Do not add, rename, reorder or remove a field. If something is missing, write the question to requests/<lane>.md and stop.
- Never edit backend/schemas.py, contract.json or contract.lock.

RP-HOTPATH
- No blocking disk or network I/O in the request path. Precompute at import time.
- No O(N^2) over input size. Prefer one pass.
- Never state a latency you did not measure (time.perf_counter_ns, warmup first).
- Optional C-extensions must have a pure-Python fallback selected at import time.

RP-SECURITY
- Treat every input as untrusted: bound length, reject invalid UTF-8 early, never eval/exec/pickle input.
- Never log raw payloads. Compare secrets in constant time. No secrets in code, docs or prompts.

RP-ADVERSARIAL
- Try: empty, None, whitespace only, 20,000 characters, combining marks, right-to-left, zero-width characters,
  nested or overlong encodings, duplicate keys, very large numbers, 50 concurrent calls.
- Report each failure with the exact input and the traceback or the wrong output. No vague findings.

RP-FASTAPI
- Pydantic v2 models imported from schemas.py only. Async routes never block the loop.
- The 422 handler returns {error, field_paths} and never echoes submitted values.
- One worker. Startup state in a lifespan handler. Mutating demo routes only when DEMO_MODE=1.

RP-FRONTEND
- Every displayed number is read from results.json or the live stream; no numeric literals for metrics.
- A badge shows LIVE, REPLAY or SIMULATED at all times. Use tabular-nums for counters.
- Respect prefers-reduced-motion. No mock disclaimers removed while the data is still mocked.
~~~~

---

## 2. Evidence tags and slop control

### 2.1 Evidence tags (Law 1)

| Tag | Meaning | Allowed in the pitch? |
| :--- | :--- | :--- |
| `[TARGET]` | A goal set in the PRD, not yet achieved | Only as "target" |
| `[MEASURED: field]` | Produced by a run; `field` is the dotted path in `results.json` | Yes |
| `[SOURCE: ref]` | From a document or URL you read this session (give file+section or URL) | Yes, with attribution |
| `[ASSUMPTION]` | Reasonable guess, logged in `ASSUMPTIONS.md` | No, until verified |
| `[UNVERIFIED]` | Seen but not confirmed (for example a statistic from memory) | **No** |
| `[OPEN]` | Unknown; a question exists | No |

### 2.2 Slop taxonomy

| Slop | Looks like | Gate |
| :--- | :--- | :--- |
| Placeholder | `{{X}}`, `[Quantify ...]`, TBD, TODO | G1 |
| Fluff | "enterprise-grade", "seamless", "cutting-edge" | G1 |
| Fabricated number | A metric in a doc, UI or deck with no run behind it | G1, G3, G4 |
| Fabricated skill | A `/slash` name not in `SKILLS_AVAILABLE.md` | G8 |
| Stub-pass | Function body is `pass`, `...`, `return None`, or a constant | G2 |
| Tautological test | Expected value computed by calling the code under test | G5 |
| Mirror doc | Two copies of the same PRD that can diverge | Stage 4 invariant 6 |
| Demo fake | Hard-coded UI metric; mock disclaimer removed while data is mocked | G3 |
| Self-certification | A model writes "VERIFIED" without an exit code | G7 |

### 2.3 Slop gates (run before handing docs or code onward, and at each phase end)

~~~~bash
# G1 docs lint (placeholders, TODO, fluff, untagged numbers, required sections)
python scripts/prd_lint.py documentation
# G2 stubs and leftovers in finished code (allowed only in Wave 0 signature stubs)
grep -rnE "NotImplementedError|TODO|FIXME|^\s*pass\s*(#.*)?$" backend benchmarks *.py
# G3 numeric literals in the UI: every hit must be layout/CSS or read from data
grep -rnE "[0-9]+(\.[0-9]+)?\s?(ms|%|x)\b" frontend/src
# G4 the fallback file is a recorded run
python -c "import json;d=json.load(open('frontend/public/telemetry_fallback.json'));assert d['source']=='recorded_run' and d['run_id']"
# G5 mutation smoke: in ONE module, flip a comparison or return a constant; the suite MUST fail. Then git checkout that file.
# G6 secrets
grep -rniE "(password|passwd|secret|api[_-]?key|BEGIN [A-Z ]*PRIVATE KEY)" . --exclude-dir=.venv --exclude-dir=node_modules --exclude-dir=.git
# G7 only the benchmark script may emit PASS/VERIFIED
grep -rn "VERIFIED" documentation benchmarks | grep -v run_benchmark.py
# G8 slash names used in prompts exist in the inventory
grep -rhoE "/[a-z0-9-]+" documentation/00_MASTER_AGENTS.md documentation/agents | sort -u   # compare with SKILLS_AVAILABLE.md
~~~~

`prd_lint.py` enforces the numeric-tag rule on generated project docs. This Reference and `SKILL.md` are guidance files and are exempt from that one rule.

---

## 3. Intake templates

### 3.1 `ASSUMPTIONS.md`

~~~~markdown
# Assumptions (kept current; resolved items are struck through, not deleted)

| ID | Assumption | Why I assumed it | How to verify | If wrong, what changes | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| A1 | Judging weights are equal | Rules PDF lists criteria without weights [SOURCE: rules.pdf p2] | Ask organisers | Re-order effort toward the heaviest criterion | open |
~~~~

### 3.2 `RUBRIC_MAP.md`

~~~~markdown
# Rubric map

| Criterion | Weight | Deliverable that scores it | Proof artifact | Owner lane | Status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Technical depth | [OPEN] | Core modules + benchmark | results.json, tests green | Wave 1 | planned |
| Sponsor-platform use | [SOURCE: rules.pdf p3] | Remote run on target arch | remote results.json, uname capture | Phase 2 | planned |
| Demo clarity | [OPEN] | 180 s video | two takes + backup | Phase 2 | planned |
~~~~

Rule: a work item with no row here needs a reason to exist. A criterion with no deliverable becomes the next task.

---

## 4. Master PRD template (`00_MASTER_PRD.md`)

Size budget: sections 3 and 4 together <= 4,000 tokens, because builders read exactly those two.

~~~~markdown
# {{PROJECT_NAME}}: Master PRD

**One line**: {{WHAT_IT_DOES_IN_ONE_SENTENCE}}
**Competition / track**: {{HACKATHON}} / {{TRACK}}   **Deadline**: {{DEADLINE}}
**Target platform**: {{TARGET_ARCH_AND_RUNTIME}}   **Contract version**: 1
**Evidence legend**: [TARGET] [MEASURED: field] [SOURCE: ref] [ASSUMPTION] [UNVERIFIED] [OPEN]

## 1. Problem, approach, modules
- **Problem**: {{PROBLEM_IN_PLAIN_WORDS}} [SOURCE: {{DOSSIER_SECTION_OR_URL}}]
- **Approach**: {{HOW_THE_MODULES_SOLVE_IT}}

| # | Module | File | Responsibility (one only) | Budget |
| :-- | :-- | :-- | :-- | :-- |
| 1 | {{M1}} | `{{PATH1}}` | {{R1}} | {{BUDGET1}} [TARGET] |

## 2. Ownership matrix
| Module | Target file(s) | Lane | Role | Gate command |
| :-- | :-- | :-- | :-- | :-- |
| 0a | `backend/schemas.py`, `contract.json` | 0a | Builder | `python scripts/contract_lock.py write` |
| 0b | `tests/**` | 0b | Test Author | `pytest --collect-only -q` |
| 1 | `{{PATH1}}` | 1a | Builder | `python {{PATH1}} && pytest -q tests/test_{{M1_SLUG}}.py` |
| I | `backend/main.py`, `requirements.txt`, `backend/__init__.py` | I | Integrator | `pytest -q` |

## 3. Glossary, constants, claims (single source of truth)
| Constant / enum | Value | Used by |
| :-- | :-- | :-- |
| {{CONST}} | {{VALUE}} | {{MODULES}} |

**Claims the pitch will make** (no value until `results.json` exists):
| ID | Claim | Metric field in results.json | Target | Status |
| :-- | :-- | :-- | :-- | :-- |
| C1 | {{CLAIM_TEXT}} | `latency_ms.p95` | {{TARGET}} | [TARGET] |

## 4. Handshakes (generated from schemas.py in Wave 0; never retyped)
| Caller | Callee | Input (exact types) | Output (exact types) | Errors |
| :-- | :-- | :-- | :-- | :-- |
| {{CALLER}} | `{{module.func}}` | `{{ARGS}}` | `{{RETURN}}` | {{EXCEPTIONS_OR_CODES}} |

**HTTP / SSE routes**: {{ROUTE_TABLE_WITH_METHOD_BODY_RESPONSE_AND_DEMO_ONLY_FLAG}}

## 5. Demo plan
Scenes, mode labels (LIVE / REPLAY / SIMULATED) and the recorded-run fallback: see Reference 11.6 and 13. Scene list: {{SCENES}}

## 6. Risks and cut lines
See `RISKS_AND_CUT_LINES.md`.
~~~~

---

## 5. Per-module PRD template (`PRD_NN_<slug>.md`)

Budget: <= 2,500 tokens. Lint requires sections `## 1.` to `## 5.`.

~~~~markdown
# PRD_{{NN}}: {{TARGET_FILE}}

**Target File(s)**: `{{TARGET_FILE}}`
**Lane / role**: {{LANE}} / Builder   **Audit required**: {{YES_OR_NO}}
**Design reference** (optional): {{NAME}} [SOURCE: {{URL}}]

## 1. Purpose and role
What this module does inside the pipeline, who calls it, and what it calls. One paragraph.

## 2. Bound skills (verified in SKILLS_AVAILABLE.md)
| Slash | Rule pack if the skill is missing | Why here |
| :-- | :-- | :-- |
| `/{{SKILL}}` | RP-{{PACK}} | {{REASON}} |

## 3. Specification
1. **Data and constants**: {{EXACT_MODULE_LEVEL_STATE}}
2. **Functions** (these names are checked against the built file by `prd_lint --check-signatures`):
   - `def {{func_1}}({{args}}) -> {{ret}}:` {{ALGORITHM_RULES}}
   - `def {{func_2}}({{args}}) -> {{ret}}:` {{ALGORITHM_RULES}}
3. **Edge cases** (each becomes at least one test in TEST_SPEC): {{EMPTY_NONE_HUGE_UNICODE_CONCURRENT_AND_DOMAIN_CASES}}
4. **Failure behaviour**: what is raised or returned for bad input; never a bare crash.
5. **Budget**: p95 <= {{BUDGET}} [TARGET], measured per Reference 11.4. The unit tests assert only a generous ceiling (5x target) to avoid flakiness; the claim is proven by the benchmark.

## 4. Invariants
- Matches `00_MASTER_PRD.md` sections 3 and 4 exactly.
- Writes only `{{TARGET_FILE}}` (plus `requests/{{LANE}}.md` for questions or dependency needs).
- Optional native dependency => pure-Python fallback chosen at import time.
- No secrets, no network calls at import, no global mutable state beyond what section 3.1 lists.

## 5. Gates
```bash
python {{TARGET_FILE}}                       # smoke self-test: exits 0, no output claiming VERIFIED
pytest -q tests/test_{{SLUG}}.py             # the Test Author's tests
python scripts/contract_lock.py check
python scripts/check_file_lock.py --since {{BASE_TAG}} --allow "{{TARGET_FILE}}" --allow "requests/{{LANE}}.md"
```
~~~~

The in-file `__main__` self-test is a **smoke test only** (imports, one happy path, one rejection). The real assurance is `tests/**`, written by someone else.

---

## 6. TEST_SPEC template (tests before code)

~~~~markdown
# TEST_SPEC

## Rules for the Test Author
1. Expected values come from an **independent oracle**: hand-computed values, published test vectors, or a separate
   reference implementation kept in `tests/oracles/`. Never from running the module under test.
2. No mocking of the module under test.
3. Every test docstring names the PRD section it covers.
4. Per module: >= 3 normal cases, >= 5 adversarial cases (from RP-ADVERSARIAL plus domain cases),
   1 contract-shape test (keys and types equal contract.json), 1 loose latency-ceiling test.
5. Seeds are fixed. No sleeps. No network.

## Module: {{MODULE}}
| ID | Input | Expected | Oracle | Covers |
| :-- | :-- | :-- | :-- | :-- |
| {{MODULE}}-N1 | {{INPUT}} | {{EXPECTED}} | {{WHERE_THE_EXPECTED_VALUE_CAME_FROM}} | PRD section 3.2 |
~~~~

**Golden suite rule**: a golden case's expected output is written down *before* the implementation exists, with its oracle named. A suite generated by the implementation proves nothing.

**Mutation smoke (G5)**: after Wave 1, flip one comparison in one module. If the suite stays green, the tests are weak: send them back to the Test Author.

---

## 7. AGENTS templates

### 7.1 Role map (tools are replaceable; roles are not)

| Role | Default tool | Does | Never does |
| :-- | :-- | :-- | :-- |
| Builder | OpenCode | Implements one file against its PRD and tests | Edits tests, contract, or other lanes' files |
| Test Author | Any tool in a **separate session** | Writes `tests/**` from the PRD | Reads implementation code |
| Auditor | Grok Code (scarce tokens) | Adversarial review of one file | Reads the repo; rewrites without staging |
| Integrator | Antigravity or the human | Owns shared files, merges lanes, runs full suite | Implements module internals |
| Verifier | **A script** (gate commands) | Decides pass or fail by exit code | Is an LLM |
| Failover | Cline | Re-runs the same Builder prompt when the Builder fails a gate twice | Gets a looser lock |

### 7.2 `00_MASTER_AGENTS.md` (contents)

~~~~markdown
# Master agents guide

## 1. Roles and waves
(role table from Reference 7.1 filled with the tools this team actually has; wave table from Reference 9)

## 2. Shared rules
- File lock: write only your allowlist plus `requests/<lane>.md`.
- Questions, missing dependencies and contract needs go to `requests/<lane>.md`, one line each:
  `NEEDS_DEP: name==version reason` | `QUESTION: ...` | `CONTRACT: ...`
- Done means the gate commands exit 0. Never write "verified" or "done" in prose without the exit code.
- Token ledger: append `date | tool | file | tokens_in~ | tokens_out~` to `TOKEN_LEDGER.md` for scarce-token tools.
- Slash lines: only names in `SKILLS_AVAILABLE.md`, at most 4 per prompt.
~~~~

### 7.3 `AGENTS_NN_<slug>.md` (per module)

~~~~markdown
# AGENTS_{{NN}}: {{TARGET_FILE}}

**Companion PRD**: `documentation/prds/PRD_{{NN}}_{{SLUG}}.md`
**Lane / worktree**: {{LANE}} / `../wt/{{LANE}}`   **Audit required**: {{YES_OR_NO}}

## 1. Execution blueprint
```yaml
goal: Implement {{TARGET_FILE}} so the gates below exit 0.
allowlist: ["{{TARGET_FILE}}", "requests/{{LANE}}.md"]
base_tag: {{BASE_TAG}}
budget: p95 <= {{BUDGET}} (target; measured later by the benchmark)
gates:
  - python {{TARGET_FILE}}
  - pytest -q tests/test_{{SLUG}}.py
  - python scripts/contract_lock.py check
  - python scripts/check_file_lock.py --since {{BASE_TAG}} --allow "{{TARGET_FILE}}" --allow "requests/{{LANE}}.md"
```

## 2. Prompts
### Builder (paste as is)
```text
{{SLASH_LINE_OR_EMPTY}}
ROLE: Builder. FILE LOCK: write ONLY {{TARGET_FILE}} (and requests/{{LANE}}.md for questions). Touching anything else is a failure.
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_{{NN}}_{{SLUG}}.md
  3. tests/test_{{SLUG}}.py
RULES:
{{RULE_PACK_TEXT}}
DONE WHEN every gate in documentation/agents/AGENTS_{{NN}}_{{SLUG}}.md section 1 exits 0. Paste each command and its exit code in your reply.
IF BLOCKED: do not guess names, keys or numbers. Append a QUESTION or NEEDS_DEP line to requests/{{LANE}}.md and stop.
```

### Auditor (only if "Audit required: yes")
```text
{{SLASH_LINE_OR_EMPTY}}
ROLE: Auditor. Do not rewrite the module unless a high-severity finding exists.
INPUT BELOW: the file, PRD section 3, the handshake rows for this module, the test case list.
TASK: find where it breaks. For each finding give: severity (high/med/low), the EXACT failing input, expected vs actual, line.
Maximum 5 findings, highest severity first. No style comments. If a high finding exists, ALSO output the corrected file as:
=== FILE: {{TARGET_FILE}} ===
<complete file>
=== END ===
Keep every public signature unchanged.
RULES: RP-ADVERSARIAL, RP-CONTRACT
{{PASTED_FILE_AND_SPEC}}
```
Apply any corrected file with `apply_incoming.py` (Reference 10.2), never by hand-pasting over the original.
~~~~

### 7.4 Test Author prompt

~~~~text
ROLE: Test Author. Write ONLY files under tests/ (tests/oracles/ for reference implementations).
READ: documentation/prds/PRD_{{NN}}_{{SLUG}}.md, TEST_SPEC.md section for this module, contract.json. Do NOT read any implementation file.
RULES: expected values from an independent oracle (hand-computed, published vectors, or tests/oracles/); no mocks of the module under test;
fixed seeds; >=3 normal, >=5 adversarial, 1 contract-shape, 1 loose latency-ceiling test; docstring names the PRD section.
DONE WHEN `pytest --collect-only -q` collects every test and `pytest -q` fails ONLY with NotImplementedError or AssertionError (never ImportError).
~~~~

### 7.5 Integrator prompt

~~~~text
ROLE: Integrator. You own: backend/main.py, backend/__init__.py, requirements.txt, package.json, .gitignore, benchmarks/run_benchmark.py.
Each lane: read requests/<lane>.md; add approved NEEDS_DEP lines to requirements.txt; answer or escalate QUESTION lines; route CONTRACT lines to the Contract Change Protocol (Reference 8.4).
Merge lanes one at a time: git merge --no-ff <lane>; after EACH merge run the full suite and `python scripts/contract_lock.py check`.
Never edit a module's internals; send it back to its lane with the failing test output.
~~~~

### 7.6 Failover rule

If a Builder fails the same gate twice, paste the **same** Builder prompt into the Failover tool. Do not widen the allowlist, do not shorten the PRD, and do not change the gate.

---

## 8. Enforcement

### 8.1 Git baseline and `.gitignore`

~~~~bash
git init
# .gitignore must contain at least:
#   .venv/
#   node_modules/
#   __pycache__/
#   _incoming/
#   _backups/
#   _duplicates_archive/
#   .env
git add -A && git commit -m "baseline"
~~~~

Without those ignores, tool artifacts show up as lock violations.

### 8.2 Worktree per lane (default) and the single-tree fallback

~~~~bash
# after Wave 0a: python scripts/contract_lock.py write ; git add -A ; git commit -m "contract v1" ; git tag wave0-locked
git worktree add ../wt/lane1a -b lane1a wave0-locked
git worktree add ../wt/lane1b -b lane1b wave0-locked
git worktree add ../wt/lane1c -b lane1c wave0-locked
# each agent opens ITS worktree folder. Run gates with the root venv interpreter (ENV_PROFILE.json: venv_python).
# at the end of a lane:  git add -A && git commit -m "lane1a done"
# then, in the main tree, one lane at a time:
git merge --no-ff lane1a -m "merge lane1a"      # then: <venv_python> -m pytest -q
~~~~

Worktrees make a lane's changes visible *only to that lane's lock check*. They cost almost no RAM (files only, no second environment).

**Single-tree fallback** (when worktrees are impractical): take a tag at the wave start and run `check_file_lock.py --since <tag>` with `--allow` set to the **union** of all in-flight lanes' allowlists. This catches cross-wave damage but cannot tell lane A from lane B; label it that way in `PHASE1_PLAYBOOK.md`.

### 8.3 Shared files registry

| File | Owner | Others must |
| :-- | :-- | :-- |
| `requirements.txt`, `package.json` | Integrator | file `NEEDS_DEP:` in `requests/<lane>.md` |
| `backend/__init__.py`, `backend/main.py` | Integrator | file `CONTRACT:` or `QUESTION:` |
| `backend/schemas.py`, `contract.json`, `contract.lock` | Builder lane 0a, then frozen | Contract Change Protocol only |
| `tests/**` | Test Author | file `QUESTION:` (a test looks wrong) |
| `.gitignore`, `benchmarks/run_benchmark.py` | Integrator | file `QUESTION:` |

### 8.4 Contract Change Protocol (CCP)

1. Requester writes `requests/CCP-<n>.md`: what changes, why, which PRDs, tests and modules it touches, whether old callers break.
2. The Integrator (or the human) approves or rejects in the same file. Silence is a rejection.
3. If approved: pause lanes at their next gate. Lane 0a edits `schemas.py` and `contract.json` and bumps `contract_version`; handshake tables and signature stubs are regenerated; the Test Author updates the affected tests; run `python scripts/contract_lock.py write`; commit; `git tag contract-v<N>`; each lane runs `git rebase contract-v<N>`.
4. Append to `CONTRACT_CHANGELOG.md`: version, date, reason, affected files.
5. More than two CCPs in a project means Wave 0 was under-specified. Note it; do not hide it.

### 8.5 Scripts (tested; copy verbatim into `scripts/`)

`check_file_lock.py`: fails if anything outside the allowlist changed since a tag.

~~~~python
#!/usr/bin/env python3
"""Enforce [STRICT FILE LOCK]: fail if any file outside the allowlist changed since a git ref.

Run it INSIDE the lane's own git worktree (see Reference section 8), so other lanes' files
can never show up as changes.

Usage:
  python scripts/check_file_lock.py --since wave0-locked --allow "backend/layer1_ingest.py" --allow "requests/lane1b.md"

Exit codes: 0 = clean, 1 = lock violation, 2 = git/usage error.
Globs use fnmatch on forward-slash paths; `*` also matches `/`, so "tests/*" covers nested files.
"""
import argparse
import fnmatch
import subprocess
import sys


def git(*args: str) -> str:
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if r.returncode != 0:
        print(f"[lock] git {' '.join(args)} failed: {r.stderr.strip()}", file=sys.stderr)
        sys.exit(2)
    return r.stdout


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since", required=True, help="git tag or commit taken before this lane started")
    ap.add_argument("--allow", action="append", default=[], help="glob of a path this lane may touch (repeatable)")
    a = ap.parse_args()
    if not a.allow:
        print("[lock] refusing to run without at least one --allow", file=sys.stderr)
        sys.exit(2)

    changed = set(git("diff", "--name-only", a.since).splitlines())
    changed |= set(git("ls-files", "--others", "--exclude-standard").splitlines())
    changed.discard("")
    bad = sorted(p for p in changed if not any(fnmatch.fnmatch(p, g) for g in a.allow))

    if bad:
        print("[lock] VIOLATION: files changed outside the allowlist:")
        for p in bad:
            print(f"  - {p}")
        print("[lock] Revert them (git checkout -- <path> / delete new files) or file a request in requests/<lane>.md")
        sys.exit(1)
    print(f"[lock] OK: {len(changed)} changed file(s), all inside the allowlist")


if __name__ == "__main__":
    main()
~~~~

`contract_lock.py`: freezes and verifies the Wave 0 contract.

~~~~python
#!/usr/bin/env python3
"""Freeze and verify the Wave 0 contract.

  python scripts/contract_lock.py write   # after schemas.py + contract.json export cleanly -> writes contract.lock
  python scripts/contract_lock.py check   # in every gate; exit 1 if the contract drifted

Edit CONTRACT_FILES for the project. contract.json must contain an integer "contract_version".
A contract change is only legal through the Contract Change Protocol (Reference section 8.4).
"""
import hashlib
import json
import sys
from pathlib import Path

CONTRACT_FILES = ["backend/schemas.py", "contract.json"]
LOCK = Path("contract.lock")


def digests() -> dict:
    out = {}
    for f in CONTRACT_FILES:
        p = Path(f)
        if not p.is_file():
            sys.exit(f"[contract] missing {f}")
        out[f] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out


def version() -> int:
    data = json.loads(Path("contract.json").read_text(encoding="utf-8"))
    v = data.get("contract_version")
    if not isinstance(v, int):
        sys.exit('[contract] contract.json must contain an integer "contract_version"')
    return v


def main() -> None:
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "write":
        payload = {"contract_version": version(), "sha256": digests()}
        LOCK.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"[contract] locked v{payload['contract_version']} -> {LOCK}")
    elif cmd == "check":
        if not LOCK.is_file():
            sys.exit("[contract] contract.lock missing: run `write` after Wave 0")
        locked = json.loads(LOCK.read_text(encoding="utf-8"))
        now = {"contract_version": version(), "sha256": digests()}
        if now != locked:
            drift = [f for f in CONTRACT_FILES if now["sha256"][f] != locked["sha256"].get(f)]
            print(f"[contract] DRIFT in: {', '.join(drift) or 'contract_version'}")
            print("[contract] Use the Contract Change Protocol; do not edit a locked contract in place.")
            sys.exit(1)
        print(f"[contract] OK (v{now['contract_version']})")
    else:
        sys.exit("usage: contract_lock.py write|check")


if __name__ == "__main__":
    main()
~~~~

`prd_lint.py`: the anti-slop linter for generated docs.

~~~~python
#!/usr/bin/env python3
"""Anti-slop lint for generated PRD / AGENTS / playbook markdown. Exit 1 on any finding.

  python scripts/prd_lint.py documentation
  python scripts/prd_lint.py documentation --check-signatures   # also verify PRD `def` names exist in the built target files

Rules (lines inside fenced code blocks are skipped):
  1. no unreplaced {{placeholders}} or bracketed fill-me prompts like [Quantify ...]
  2. no TBD / TODO / FIXME / lorem ipsum
  3. no marketing fluff words
  4. every numeric claim (%, ms, x, $) carries an evidence tag on the same line:
     [TARGET] [MEASURED: <field>] [SOURCE: <ref>] [ASSUMPTION] [UNVERIFIED] [OPEN]
  5. PRD_NN files have sections ## 1. .. ## 5.; AGENTS_NN files have ## 1. and ## 2.
"""
import argparse
import ast
import re
import sys
from pathlib import Path

PLACEHOLDER = re.compile(r"\{\{[^}]*\}\}")
FILL_ME = re.compile(r"\[(?:Quantify|Lock|Explain|Exact|Step-by-step|Describe|Insert|Fill)[^\]]*\]", re.I)
TODO = re.compile(r"\b(TBD|TODO|FIXME|lorem ipsum|to be decided)\b", re.I)
FLUFF = re.compile(
    r"\b(enterprise-grade|cutting-edge|state-of-the-art|revolutionary|game-chang\w+|seamless(?:ly)?|"
    r"world-class|best-in-class|next-gen(?:eration)?|military-grade|bulletproof|blazing[- ]fast|unparalleled)\b",
    re.I,
)
NUMBER_CLAIM = re.compile(r"(?:\d[\d,.]*\s?(?:%|ms\b|µs|×|x\b)|\$\s?\d)")
TAG = re.compile(r"\[(?:TARGET|MEASURED|SOURCE|ASSUMPTION|UNVERIFIED|OPEN)\b")
FENCE = re.compile(r"^\s*(```|~~~)")
DEF_NAME = re.compile(r"\bdef\s+(\w+)\s*\(")
TARGET_LINE = re.compile(r"\*\*Target File\(s\)\*\*:\s*(.+)")


def prose_lines(text: str):
    fence = None
    for i, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line)
        if m:
            fence = None if fence == m.group(1) else (fence or m.group(1))
            continue
        if fence is None:
            yield i, line


def lint_file(path: Path) -> list:
    text = path.read_text(encoding="utf-8")
    out = []
    for i, line in prose_lines(text):
        if PLACEHOLDER.search(line):
            out.append((i, "unreplaced {{placeholder}}"))
        if FILL_ME.search(line):
            out.append((i, "bracketed fill-me prompt left in text"))
        if TODO.search(line):
            out.append((i, "TBD/TODO/FIXME marker"))
        if FLUFF.search(line):
            out.append((i, f"fluff word: {FLUFF.search(line).group(0)}"))
        stripped = line.strip()
        if stripped.startswith("#") or re.fullmatch(r"[|\s:\-]+", stripped or "-"):
            continue
        if NUMBER_CLAIM.search(line) and not TAG.search(line):
            out.append((i, "numeric claim without an evidence tag"))
    name = path.name
    if re.match(r"PRD_\d+", name):
        for n in range(1, 6):
            if not re.search(rf"^##\s+{n}\.", text, re.M):
                out.append((0, f"missing section '## {n}.'"))
    if re.match(r"AGENTS_\d+", name):
        for n in (1, 2):
            if not re.search(rf"^##\s+{n}\.", text, re.M):
                out.append((0, f"missing section '## {n}.'"))
    return out


def check_signatures(prd: Path, root: Path) -> list:
    text = prd.read_text(encoding="utf-8")
    m = TARGET_LINE.search(text)
    if not m:
        return []
    out = []
    wanted = set(DEF_NAME.findall("\n".join(l for _, l in prose_lines(text))))
    for target in re.findall(r"`([^`]+\.py)`", m.group(1)):
        tp = root / target
        if not tp.is_file():
            continue
        try:
            tree = ast.parse(tp.read_text(encoding="utf-8"))
        except SyntaxError as e:
            out.append((0, f"{target}: syntax error line {e.lineno}"))
            continue
        have = {n.name for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        for name in sorted(wanted - have):
            out.append((0, f"{target}: PRD names `{name}()` but it is not defined"))
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("folder")
    ap.add_argument("--check-signatures", action="store_true")
    ap.add_argument("--root", default=".", help="project root for --check-signatures")
    a = ap.parse_args()

    files = sorted(Path(a.folder).rglob("*.md"))
    total = 0
    for f in files:
        findings = lint_file(f)
        if a.check_signatures and re.match(r"PRD_\d+", f.name):
            findings += check_signatures(f, Path(a.root))
        for line, msg in findings:
            print(f"{f}:{line or '-'}: {msg}")
        total += len(findings)
    print(f"[prd_lint] {len(files)} file(s), {total} finding(s)")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
~~~~

`apply_incoming.py`: the safe replacement for the "blind one-shot rewrite".

~~~~python
#!/usr/bin/env python3
"""Non-destructive applier for model-generated files (the safe replacement for 'one-shot script that rewrites the repo').

Per file: validate path -> ast.parse (.py) -> back up the original to _backups/<UTC stamp>/ -> copy in -> run gate -> roll back on failure.

Modes:
  # files already placed under _incoming/<relpath>
  python scripts/apply_incoming.py --allow "backend/layer2_*.py" --gate "python backend/layer2_decoys.py" backend/layer2_decoys.py

  # one model reply containing blocks:   === FILE: backend/x.py ===  ...  === END ===
  python scripts/apply_incoming.py --allow "backend/*.py" --bundle reply.txt --gate "pytest -q" --atomic

--allow is mandatory (fnmatch globs): the model cannot write outside it, so a locked contract is never overwritten by accident.
--atomic applies every file, runs the gate once, and rolls ALL files back if it fails (use when files depend on each other).
Exit 0 only if every file applied and the gate passed.
"""
import argparse
import ast
import fnmatch
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path.cwd()
INCOMING = ROOT / "_incoming"
BLOCK = re.compile(r"^=== FILE: (.+?) ===[ \t]*\n(.*?)^=== END ===[ \t]*$", re.S | re.M)


def check_path(rel: str, allow: list) -> str:
    p = Path(rel)
    if p.is_absolute() or ".." in p.parts or not rel.strip():
        raise ValueError(f"unsafe path: {rel!r}")
    posix = p.as_posix()
    if not any(fnmatch.fnmatch(posix, g) for g in allow):
        raise ValueError(f"not covered by --allow: {posix}")
    return posix


def unfence(body: str) -> str:
    lines = body.rstrip("\n").split("\n")
    if lines and lines[0].lstrip().startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
    return "\n".join(lines) + "\n"


def stage_bundle(bundle: Path, allow: list) -> list:
    blocks = BLOCK.findall(bundle.read_text(encoding="utf-8"))
    if not blocks:
        raise ValueError("no '=== FILE: path ===' ... '=== END ===' blocks found in bundle")
    rels = []
    for rel, body in blocks:
        posix = check_path(rel.strip(), allow)
        dst = INCOMING / posix
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(unfence(body), encoding="utf-8")
        rels.append(posix)
    return rels


def install(rel: str, stamp: str):
    src, dst = INCOMING / rel, ROOT / rel
    if not src.is_file():
        raise FileNotFoundError(f"{src} not found")
    if rel.endswith(".py"):
        ast.parse(src.read_text(encoding="utf-8"), filename=rel)
    backup = None
    if dst.exists():
        backup = ROOT / "_backups" / stamp / rel
        backup.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(dst, backup)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return rel, backup


def rollback(done: list) -> None:
    for rel, backup in reversed(done):
        dst = ROOT / rel
        if backup is not None:
            shutil.copy2(backup, dst)
        elif dst.exists():
            dst.unlink()  # only ever a file this run created
        print(f"[apply] rolled back {rel}")


def run_gate(cmd: str) -> bool:
    if not cmd:
        return True
    return subprocess.run(cmd, shell=True, timeout=600).returncode == 0


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="*", help="relative paths already present under _incoming/")
    ap.add_argument("--allow", action="append", default=[], required=True)
    ap.add_argument("--bundle")
    ap.add_argument("--gate", default="")
    ap.add_argument("--atomic", action="store_true")
    a = ap.parse_args()

    try:
        rels = [check_path(f, a.allow) for f in a.files]
        if a.bundle:
            rels += stage_bundle(Path(a.bundle), a.allow)
    except (ValueError, OSError) as e:
        print(f"[apply] REFUSED: {e}", file=sys.stderr)
        sys.exit(2)
    if not rels:
        sys.exit("[apply] nothing to apply")

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    done: list = []
    try:
        for rel in rels:
            done.append(install(rel, stamp))
            print(f"[apply] installed {rel}")
            if not a.atomic and not run_gate(a.gate):
                print(f"[apply] GATE FAILED after {rel}")
                rollback([done.pop()])
                sys.exit(1)
        if a.atomic and not run_gate(a.gate):
            print("[apply] GATE FAILED (atomic): rolling everything back")
            rollback(done)
            sys.exit(1)
    except (SyntaxError, FileNotFoundError, subprocess.TimeoutExpired) as e:
        print(f"[apply] ERROR: {e}", file=sys.stderr)
        rollback(done)
        sys.exit(1)
    print(f"[apply] OK: {len(done)} file(s) applied; backups in _backups/{stamp}/")


if __name__ == "__main__":
    main()
~~~~

These were exercised in a scratch repository: lock pass, lock violation, missing allowlist, contract drift, gate failure with rollback, syntax-error rejection, bundle apply with fenced content, path traversal refusal, and out-of-allowlist refusal.

---

## 9. Phase 1 playbook

### 9.1 Time scaling (T = time from "dossier in hand" to submission)

| Block | Share of T | Floor | Example T=6 h | Example T=24 h |
| :-- | :-- | :-- | :-- | :-- |
| Intake, preflight, docs (Stages 0-4) | 12% | 30 min | 43 min | 173 min |
| Wave 0: contract + tests | 8% | 20 min | 29 min | 115 min |
| Wave 1: modules (parallel) | 22% | 45 min | 79 min | 317 min |
| Wave 2: integration + walking skeleton | 15% | 30 min | 54 min | 216 min |
| Wave 3: frontend bridge | 10% | 25 min | 36 min | 144 min |
| Phase 2: doctor, muscle, hardening | 13% | 30 min | 47 min | 187 min |
| Local live run + remote proof | 8% | 30 min | 29 min | 115 min |
| Recording, export, upload | 12% | 60 min | 43 min | 173 min |

When a floor exceeds its share, take the difference from Wave 1 first, never from Recording. Cumulative checkpoints: D0 (walking skeleton + REPLAY fallback) at about 57% of T; D1 at about 80%; D2 at about 90%.

### 9.2 Step list

1. **Stage 1-4 output on disk** (`PREFLIGHT.md`, `ENV_PROFILE.json`, docs, setup script run with `--apply`). `python scripts/prd_lint.py documentation` exits 0.
2. **Wave 0a (Builder)**: `schemas.py`, `contract.json` (with `contract_version: 1`), generated handshake tables, and **signature stubs** for every module (each function raises `NotImplementedError`). Gate: `python scripts/contract_lock.py write`, commit, tag `wave0-locked`.
3. **Wave 0b (Test Author, separate session)**: `tests/**` from TEST_SPEC. Gate: `pytest --collect-only -q` collects everything; `pytest -q` fails only with NotImplementedError or AssertionError.
4. **Wave 1**: one worktree and one Builder per lane (Reference 8.2). Each lane ends with its four gates. Integrator merges sequentially and runs the full suite after each merge.
5. **Wave 2 (Integrator)**: gateway, CLI, `benchmarks/run_benchmark.py` (it must write `results.json`, Reference 11.5). **Walking skeleton**: one real end-to-end request through every module, recorded. Build `telemetry_fallback.json` *from that run* (Reference 11.6). That is D0.
6. **Wave 3**: frontend reads live SSE or the REPLAY file; badge shows the mode; G3 passes.
7. **Slop gates** (Reference 2.3), all clean. Tag `phase1-done`.

### 9.3 `RISKS_AND_CUT_LINES.md` template

~~~~markdown
# Risks and cut lines

| Risk | Likelihood | Early signal | Pre-agreed fallback |
| :-- | :-- | :-- | :-- |
| Dependency has no wheel on the target arch | {{L}} | wheel check fails in Preflight | Pure-Python fallback specified in PRD {{NN}} |
| A module misses its budget | {{L}} | benchmark claim `met: false` | Drop the claim, keep the feature; never edit the number |
| Wave 1 not green at 45% of T | {{L}} | `pytest` red | Failing module becomes a contract-conformant simulated implementation (`capability: "simulated"`), narrated as such |
| Remote VM unreachable | {{L}} | ssh fails at Preflight | Record local run; state plainly in the video that remote proof is pending; do not fake it |

Hard cut lines: 45% of T Wave 1 must be green or scope is frozen; 70% no new features; 88% start recording regardless.
~~~~

---

## 10. Phase 2: doctor, surgical muscle injection, token caps

### 10.1 Doctor first (report only)

Use the user's `phase2_dedup_and_doctor_template.py` **after** applying the fixes in Reference 15 (D1-D8). Required behaviour:

- Default is **report only**. Moving anything needs `--apply`.
- Stub detection is by AST, not line count: a function whose body is only a docstring, `pass`, `...`, `return None`, `return <constant>` or `raise NotImplementedError` is a stub. A module with any stub function is `STUB`; one with TODO/FIXME is `NEEDS_MUSCLE`.
- Output `PHASE2_DOCTOR_REPORT.json` plus a table: file, stub functions, has tests, last gate result.
- It also runs `contract_lock.py check` and `pytest --collect-only -q`.

### 10.2 Surgical muscle injection (replaces the "mega one-shot script")

Why the old design was dropped: a model that has not read the files cannot "upgrade" them, a script that writes straight to disk can overwrite the locked contract, and nothing rolled back a bad result.

**Prompt (one per stub file, or up to 3 related stubs per bundle):**

~~~~text
{{SLASH_LINE_OR_EMPTY}}
ROLE: Muscle injector. Reply with file blocks ONLY, no prose, exactly:
=== FILE: {{PATH}} ===
<complete file contents>
=== END ===
Allowed paths: {{ALLOWED_PATHS}}. Maximum {{N}} files.
CONTRACT (do not change a name, type or key):
{{HANDSHAKE_ROWS_FOR_THIS_MODULE}}
CURRENT FILE (replace it completely; keep every public signature):
{{FILE_CONTENTS}}
SPEC (PRD section 3):
{{PRD_SECTION_3}}
TESTS THAT MUST PASS (case list or file):
{{TESTS}}
RULES:
{{RULE_PACK_TEXT}}
Allowed third-party imports: {{ALLOWED_DEPS}}. Pure-Python fallback required for anything native.
~~~~

**Apply (always staged, allowlisted, gated, reversible):**

~~~~bash
# save the model's reply as reply.txt, then
python scripts/apply_incoming.py --allow "backend/layer2_*.py" --allow "backend/scorer.py" \
  --bundle reply.txt --atomic \
  --gate "pytest -q tests/test_layer2.py tests/test_scorer.py && python scripts/contract_lock.py check"
~~~~

Backups land in `_backups/<UTC stamp>/`. A failed gate rolls every file in the bundle back.

### 10.3 Token caps for scarce-token tools (for example a 100K Grok budget)

| Rule | Value |
| :-- | :-- |
| Estimate | tokens ~ characters / 3.5 for code, / 4 for prose; an estimate, not a promise |
| Per request | input <= 6K, output <= 8K |
| Files per request | <= 3 |
| Reserve | keep 25% of the budget unspent for retries |
| Requests available | usable = budget x 0.75; requests ~ usable / 14K (for 100K: about 5 requests) |
| Order of spend | (1) hot-path or security stubs, (2) integration gaps, (3) polish. Never exploration |
| Ledger | append each request to `TOKEN_LEDGER.md` |

If the budget cannot cover all stubs, rank them by claim impact (`RUBRIC_MAP.md`) and let the Failover tool take the rest.

### 10.4 Diff-only audit

For a file that already works, paste only the changed function bodies plus PRD section 3.2 into the Auditor prompt (7.3). It costs a fraction of re-reading the file.

---

## 11. Runtime hardening

### 11.1 SSE specification

- `GET /v1/{{slug}}/stream` with `Content-Type: text/event-stream`, `Cache-Control: no-cache`.
- Every event carries `id:` (monotonic integer) and `event:` (type). Send `retry: 2000` once.
- Heartbeat comment `: hb` every 15 seconds.
- Per-subscriber `asyncio.Queue(maxsize=256)`. When full, **drop the oldest** and enqueue `{"type":"dropped","count":n}`. ("Zero-drop" with bounded memory is impossible, so the policy is explicit.)
- Replay buffer: `collections.deque(maxlen=N)` with N from the PRD [TARGET]. Honour `Last-Event-ID` to replay what was missed.
- Run **one** uvicorn worker (state is in memory). Do not use `--reload` while recording.

### 11.2 Security checklist (Law 9)

| Item | Rule |
| :-- | :-- |
| Bind address | `127.0.0.1`. Remote access by `ssh -L 8000:127.0.0.1:8000 user@host`. Binding `0.0.0.0` only with a written reason, never on public Wi-Fi |
| CORS | Allowlist the frontend origin (`http://localhost:5173`), not `*` |
| Demo-only routes | `simulate-tamper`, `restore`, `demo-*` return 404 unless `DEMO_MODE=1` |
| Input limits | Pydantic `max_length` on every string; request body cap (for example 1 MB); reject invalid UTF-8 |
| 422 handler | Returns `{error, field_paths}`; never echoes submitted values |
| Logging | No raw payloads; redact tokens |
| Secrets | Env vars or `.env` (git-ignored). Never in PRDs, prompts, screenshots, or terminal history shown on video |
| SSH | Key auth; do not record the host key, username or IP on screen if the VM is shared |

### 11.3 Chaos vectors (fuzz suite, project-independent)

Empty body; wrong content type; valid JSON with wrong field types; missing required field; string of 20,000 characters; nested JSON 200 levels deep; Unicode (combining marks, right-to-left, zero-width, emoji); invalid UTF-8 bytes; 50 concurrent requests; client disconnect mid-stream. Expected: a controlled 4xx or a valid response, never a 500, never a hang, never a payload echo, server still healthy afterwards (`GET /health` returns 200).

### 11.4 Latency measurement protocol

- Clock: `time.perf_counter_ns()`.
- Warmup 200 calls (discarded), then >= 2,000 measured calls, fixed seed, one process, no other heavy work running.
- Report p50, p95, p99, max.
- Measure **two modes separately and label each**: `in_process` (function or TestClient) and `http_loopback` (real socket to `127.0.0.1`). Add `remote` when run on the target.
- Record the host: machine arch, CPU model, RAM, OS, Python version.
- A budget is `[TARGET]` until a run says otherwise. A missed target is reported as missed.

### 11.5 `results.json` (the only source of numbers)

```json
{
  "schema_version": 1,
  "run_id": "2026-10-24T05-23-11Z-ab12cd3",
  "git_commit": "ab12cd3",
  "dirty": false,
  "mode": "in_process | http_loopback | remote",
  "host": {"machine": "x86_64", "cpu": "", "ram_gb": 8.0, "os": "", "python": "3.11"},
  "latency_ms": {"n": 2000, "warmup": 200, "p50": 0.0, "p95": 0.0, "p99": 0.0, "max": 0.0},
  "suites": {
    "golden": {"total": 0, "passed": 0, "failed_ids": []},
    "stress": {"total": 0, "passed": 0, "failed_ids": []},
    "chaos":  {"total": 0, "passed": 0, "failed_ids": []}
  },
  "claims": [
    {"id": "C1", "text": "p95 latency under target", "source_field": "latency_ms.p95",
     "value": 0.0, "unit": "ms", "target": 2.0, "met": false}
  ]
}
```

`BENCHMARK_REPORT.md` is generated from this file by `run_benchmark.py`. Its status is `PASS` only when every claim has `met: true`; otherwise it lists the misses. The UI and the deck read `claims[].value`; nobody types a metric.

### 11.6 Fallback file and mode badges

```json
{"source": "recorded_run", "run_id": "2026-10-24T05-23-11Z-ab12cd3", "recorded_at": "2026-10-24T05:23:11Z",
 "events": [{"id": 1, "type": "evaluate", "payload": {}}]}
```

| Badge | When |
| :-- | :-- |
| LIVE | The page is connected to the running backend stream |
| REPLAY | The page is playing `telemetry_fallback.json` (a recording of a real run) |
| SIMULATED | A module is running as a contract-conformant stand-in (`capability: "simulated"` in its events) |

### 11.7 Benchmark honesty rules

- Golden expected values come from an oracle (Reference 6), written before the implementation.
- A baseline comparison (for example "Nx faster than the naive version") requires the baseline to be implemented and run in the same harness, same machine, same inputs. Otherwise there is no speedup claim.
- Datasets are described by what they are (synthetic, public, size). Synthetic data is never presented as production data.
- A dollar or percentage impact figure from outside the project needs `[SOURCE]` with a link you opened this session; otherwise it stays out of the pitch.

---

## 12. Preflight and remote-target proof

### 12.1 Preflight commands

~~~~bash
# local
python --version ; node --version ; git --version
# target (replace user@host; use key auth)
ssh user@host "uname -m && python3 --version && python3 -m pip --version && df -h . && free -m"
# wheel check: fails loudly if a dependency has no prebuilt wheel for the target
ssh user@host "python3 -m pip install --dry-run --only-binary=:all: fastapi 'uvicorn[standard]' pydantic numpy scikit-learn httpx pytest"
~~~~

Anything that fails the wheel check becomes an explicit decision in the PRD (pure-Python fallback, or build from source on the target) and a row in `RISKS_AND_CUT_LINES.md`. Write findings to `PREFLIGHT.md` and the machine-readable subset to `ENV_PROFILE.json` (`local`, `target`, `venv_python`, `wheel_check`).

### 12.2 Remote proof protocol

1. `scp` only the files the target needs (backend, CLI, benchmark runner, requirements). Never copy `.venv`, `node_modules`, `.env`, `_backups`.
2. On the target: create a venv, `pip install -r requirements.txt`, then run `python benchmarks/run_benchmark.py --mode remote`.
3. Capture, with a visible clock: `uname -m`, `python3 --version`, the benchmark output, and the `results.json` it wrote. Pull that `results.json` back as `results.remote.json`.
4. Open the tunnel (`ssh -L 8000:127.0.0.1:8000 user@host`) and show the live UI against the remote backend for the video.
5. Local numbers are never presented as remote numbers. If remote proof failed, say so on camera or leave the claim out.

---

## 13. Demo recording

### 13.1 Scene template for a 180-second video (adapt to the real rubric)

| Scene | Time | Content | Must show |
| :-- | :-- | :-- | :-- |
| 1 Problem | 0:00-0:25 | One concrete failure the judges recognise | Only a `[SOURCE]`-backed fact, or none |
| 2 Live run | 0:25-1:15 | A real request flowing through the modules | LIVE badge, event stream, one `results.json` claim |
| 3 Hard case | 1:15-2:00 | An adversarial input or tamper/restore, handled | The system refusing or recovering, visibly |
| 4 Target proof | 2:00-2:35 | The sponsor architecture running it | `uname -m` on the target, remote results |
| 5 Close | 2:35-2:55 | The three claims and what was measured | Numbers read from `results.json`; 5 s margin before 3:00 |

### 13.2 Setup and checklist

- 1920x1080, 60 fps. Split screen: terminal on the left, browser on the right at a readable zoom.
- **Determinism**: a `DEMO_SEED` and a fixed event order so every take is the same. `DEMO_MODE=1`.
- **Rehearse twice with a stopwatch** before the first recording.
- **Record at least two takes.** Keep a backup capture (phone or second screen recorder). Check audio before every take.
- Close notifications; clear terminal history and environment variables that show secrets, hostnames or keys.
- Confirm >= 10 GB free disk. Export, then **watch the exported file end to end** before uploading.
- Upload with a 30-minute buffer before the deadline.

---

## 14. Session card template (`documentation/skills/SESSION_<slug>.md`, <= 120 lines)

~~~~markdown
---
name: session-{{SLUG}}
base_skill: hackathon-backend-king v3.0
derived: true   # fills variables only; never edits the Core Engineering Principles
date: {{DATE}}
---
# Session card: {{PROJECT_NAME}}
- Competition / deadline: {{HACKATHON}} / {{DEADLINE}}   Target: {{TARGET}}
- Roles -> tools: Builder {{TOOL}}, Test Author {{TOOL}}, Auditor {{TOOL}}, Integrator {{TOOL}}, Failover {{TOOL}}
- Skills verified present: {{LIST_FROM_SKILLS_AVAILABLE}}
- Hardware profile: {{FROM_ENV_PROFILE}}
- File matrix: {{MODULE_TO_FILE_TO_LANE_TABLE}}
- Claim ids: {{C1_C2_C3_WITH_RESULTS_FIELDS}}
- Contract: version {{N}}, lock tag `{{TAG}}`
- Known quirks: {{DUPLICATE_PATHS_WHEEL_ISSUES_ETC}}
- Open items: {{LIST_FROM_ASSUMPTIONS}}
~~~~

Do not overwrite the user's installed skill. If they want this card kept, hand them the file.

---

## 15. Defect register for the original templates and scripts

Apply these fixes to `workspace_organizer_template.py` and `phase2_dedup_and_doctor_template.py` (or ask for regenerated versions). Everything marked **data loss** can destroy the user's work.

### 15.1 Setup script

| # | Defect | Fix |
| :-- | :-- | :-- |
| S1 | `PROJECT_SLUG` defaults to `mirage-z`: another project's name leaks into new ones | Required `--slug` argument; no default |
| S2 | `REQUIRED_PIP_PACKAGES` is a fixed stack | Install from the project's `requirements.txt`; write `requirements.lock` after success |
| S3 | PRDs and AGENTS are copied to both `documentation/` and `documentation/prds|agents/`: two copies that diverge | One location only |
| S4 | Pattern matches (`PRD_*`, `SKILL_*`, any PDF containing "dossier") pull files from other projects in Downloads | Manifest or recent-and-slug-matched only; top-level only |
| S5 | Unpacking the embedded bundle overwrites existing files (**data loss** of edits on a re-run) | Never overwrite a differing file; write `<name>.incoming` |
| S6 | No dry-run, no log, subprocess results ignored (pip failures silent) | Dry-run default, `--apply`, `setup.log`, non-zero exit on failure |
| S7 | Embedded payload has no checksum | Verify SHA-256 before unpacking |
| S8 | `tuple[float, float]` annotations need Python 3.9 | `from __future__ import annotations` or `typing.Tuple` |
| S9 | Documentation promises "extracts teammate zips and removes empty folders in Downloads"; the code does neither (and deleting there would be unsafe) | Remove the promise; extract zips into a staging folder on request only; never delete in Downloads |
| S10 | `shutil.rmtree` on an existing archive destination discards earlier archived data (**data loss**) | Unique suffix per archive |
| S11 | Unused imports (`zipfile`, `venv`) | Remove |
| S12 | Desktop detection relies on the registry string alone | `SHGetKnownFolderPath` first, then registry, then OneDrive variants |

### 15.2 Doctor script

| # | Defect | Fix |
| :-- | :-- | :-- |
| D1 | De-dupe key `(filename, hash)` across folders archives the second empty `__init__.py`, identical `index.ts`, and similar files, breaking packages (**data loss**) | Only `name (1).ext` with an identical sibling in the **same folder**; never `__init__.py`, `.gitkeep`, lockfiles, `LICENSE` |
| D2 | `rglob("*")` descends into `node_modules` and `.venv` before filtering: minutes on a 4-thread CPU | `os.walk` with directory pruning |
| D3 | `archive_item` deletes an existing destination | Unique timestamp suffix |
| D4 | `lines < 25` flags small legitimate files as stubs | AST-based stub detection (10.1) |
| D5 | `.vercel` treated as clutter although it holds the project link | Only report; remove from the default clutter list |
| D6 | Docstring claims contract-drift and live-endpoint checks that the code does not do | Call `contract_lock.py check` and `pytest --collect-only`; or drop the claim |
| D7 | Moves files on the first run with no confirmation | Report-only default; `--apply` to move |
| D8 | Report JSON lacks stub function names, so muscle prompts cannot be targeted | Add `stub_functions` per file |

### 15.3 Original prompts and docs

| # | Defect | Fix |
| :-- | :-- | :-- |
| P1 | The Grok prompt "verifies and upgrades" files it never sees | Per-stub self-contained prompts (10.2) |
| P2 | It asserts "100% pass, 0% leakage, P95 < 2.0 ms" and writes a fallback JSON with them (fabrication) | Numbers come only from `results.json` |
| P3 | Output script name differs between the SKILL (`phase2_muscle_injector.py`) and the prompt (`phase2_muscle_engine.py`) | Removed; replaced by `apply_incoming.py` |
| P4 | MIRAGE-specific endpoints, layer names and hardware baked into a generic skill | Parameterised; modules derived per project |
| P5 | `uvicorn --host 0.0.0.0`, CORS `*`, public tamper routes | Reference 11.2 |
| P6 | "zero-drop `asyncio.Queue`" contradicts a 25-event replay deque | Bounded per-subscriber queues with an explicit drop policy (11.1) |
| P7 | `skills:update_skill` assumed to exist | Hand the user the session card |
| P8 | Four prompts per file for ten files, mostly duplicates; Cline "failover" prompt equals the Builder prompt | One Builder prompt; Auditor only where needed; failover reuses the Builder prompt |
| P9 | "~10K to 15K tokens total" stated as fact | Estimate formula, caps, ledger (10.3) |
| P10 | Recording given 20 minutes for "one clean take" | 12% of T with a 60-minute floor, two takes, backup capture |
| P11 | Templates nested ``` inside ``` and rendered broken | `~~~~` outer fences |
| P12 | "Read sections 3-4 of the master PRD" with no size limit | Token budgets per document (Reference 4, 5) |
| P13 | Mock disclaimers stripped in the frontend sweep regardless of data source | LIVE / REPLAY / SIMULATED badge (11.6) |
| P14 | Skill name mismatch between the archive header and the frontmatter | Single name `hackathon-backend-king` |

## Part 3: `scripts/workspace_organizer_template.py` (v3.0 with S1–S12 Fixes Applied)

```python
#!/usr/bin/env python3
"""
========================================================================================
HACKATHON BACKEND KING (v3.0) // NON-DESTRUCTIVE WORKSPACE ORGANIZER & SETUP SCRIPT
File: workspace_organizer_template.py (Generated per project as `setup_<slug>_workspace.py`)
========================================================================================

V3.0 SAFETY INVARIANTS (S1-S12 APPLIED):
1. Python 3.9+ Standard Library only (`from __future__ import annotations`).
2. Required `--slug <project-slug>` argument (no hardcoded project name).
3. Dry-run by default: prints every planned action and writes `setup.log`; only mutates
   disk when `--apply` is passed.
4. Copies downloaded files from top-level `Downloads/` and `Desktop/` (never moves or
   deletes user files in `Downloads/`), matching either `EMBEDDED_MANIFEST` or `--slug`
   modified within `--since-hours` (default 48h).
5. Single canonical destination per document (`documentation/prds/`, `documentation/agents/`,
   `documentation/skills/`); zero duplicate mirror copies.
6. Never overwrites an existing file whose SHA-256 differs; writes `<name>.incoming` beside
   it and records the conflict in `setup.log`.
7. Verifies `EMBEDDED_BUNDLE_SHA256` before unpacking `EMBEDDED_BUNDLE_B85`.
8. Deduplicates only `name (1).ext` copy files that have a byte-identical canonical sibling
   in the SAME folder, archiving redundant copies with a unique UTC timestamp suffix.
9. Installs dependencies from `requirements.txt` (if present) and writes `requirements.lock`
   from `pip freeze`, exiting non-zero if installation fails.
10. Resolves Desktop via `SHGetKnownFolderPath` first, Registry second, then OneDrive paths.
11. Initializes git, writes `.gitignore` (`.venv/`, `node_modules/`, `__pycache__/`,
    `_incoming/`, `_backups/`, `_duplicates_archive/`, `.env`), and commits `baseline`.
"""
from __future__ import annotations

import argparse
import base64
import ctypes
import hashlib
import json
import lzma
import os
import platform
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

EMBEDDED_MANIFEST: list[str] = []
EMBEDDED_BUNDLE_SHA256: str = ""
EMBEDDED_BUNDLE_B85: str = ""

PROTECTED_FILENAMES = {"__init__.py", ".gitkeep", "package-lock.json", "requirements.lock", "contract.lock", "LICENSE"}
PRUNE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", "_incoming", "_backups", "_duplicates_archive"}

GITIGNORE_DEFAULT = """.venv/
venv/
node_modules/
__pycache__/
.pytest_cache/
_incoming/
_backups/
_duplicates_archive/
*.incoming
.env
"""


class SetupLogger:
    def __init__(self, log_path: Path | None) -> None:
        self.log_path = log_path
        self.lines: list[str] = []

    def info(self, msg: str) -> None:
        stamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        line = f"[{stamp}] {msg}"
        print(msg)
        self.lines.append(line)

    def flush(self) -> None:
        if self.log_path is not None:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            self.log_path.write_text("\n".join(self.lines) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def detect_desktop_dir() -> Path:
    """Resolve Desktop using SHGetKnownFolderPath first, then Registry, then OneDrive variants (S12)."""
    home = Path.home()
    if sys.platform.startswith("win"):
        # 1. Try SHGetKnownFolderPath(FOLDERID_Desktop)
        try:
            from ctypes import windll, wintypes
            class GUID(ctypes.Structure):
                _fields_ = [
                    ("Data1", wintypes.DWORD),
                    ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD),
                    ("Data4", ctypes.c_ubyte * 8),
                ]
            # {B4BFCC3A-DB2C-424C-B029-7FE99A87C641}
            folderid_desktop = GUID(
                0xB4BFCC3A,
                0xDB2C,
                0x424C,
                (ctypes.c_ubyte * 8)(0xB0, 0x29, 0x7F, 0xE9, 0x9A, 0x87, 0xC6, 0x41),
            )
            path_ptr = ctypes.c_wchar_p()
            if windll.shell32.SHGetKnownFolderPath(ctypes.byref(folderid_desktop), 0, 0, ctypes.byref(path_ptr)) == 0:
                if path_ptr.value:
                    p = Path(path_ptr.value)
                    if p.exists():
                        return p
        except Exception:
            pass

        # 2. Try Registry User Shell Folders
        try:
            import winreg
            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders",
            ) as key:
                val, _ = winreg.QueryValueEx(key, "Desktop")
                p = Path(os.path.expandvars(val))
                if p.exists():
                    return p
        except Exception:
            pass

        # 3. Try OneDrive variants (OneDrive, OneDrive - <Org>)
        for od in sorted(home.glob("OneDrive*")):
            cand = od / "Desktop"
            if cand.is_dir():
                return cand

    for cand in [home / "Desktop", home]:
        if cand.is_dir():
            return cand
    return Path.cwd()


def safe_write_bytes(dest: Path, data: bytes, apply: bool, log: SetupLogger) -> None:
    """Never overwrite an existing file if its content differs; write `<name>.incoming` instead (S5)."""
    if dest.exists():
        if sha256_file(dest) == sha256_bytes(data):
            log.info(f"  [SKIP-IDENTICAL] {dest}")
            return
        inc = dest.with_name(dest.name + ".incoming")
        log.info(f"  [CONFLICT-SAFE] {dest} differs from incoming -> writing {inc.name}")
        if apply:
            inc.parent.mkdir(parents=True, exist_ok=True)
            inc.write_bytes(data)
        return

    log.info(f"  [{'WRITE' if apply else 'DRY-WRITE'}] {dest}")
    if apply:
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)


def strip_copy_suffix(filename: str) -> str:
    return re.sub(r"\s*\(\d+\)(?=\.[^.]+$)", "", filename)


def route_destination(clean_name: str, target_root: Path) -> Path | None:
    """Single canonical destination per file; zero duplicate mirror copies (S3)."""
    upper = clean_name.upper()
    if upper.startswith("PRD_") and clean_name.endswith(".md"):
        return target_root / "documentation" / "prds" / clean_name
    if upper.startswith("AGENTS_") and clean_name.endswith(".md"):
        return target_root / "documentation" / "agents" / clean_name
    if (upper.startswith("SKILL_") or upper.startswith("SESSION_") or upper == "SKILLS_AVAILABLE.MD") and clean_name.endswith(".md"):
        return target_root / "documentation" / "skills" / clean_name
    if upper in {"00_MASTER_PRD.MD", "00_MASTER_AGENTS.MD", "TEST_SPEC.MD", "RUBRIC_MAP.MD", "ASSUMPTIONS.MD", "RISKS_AND_CUT_LINES.MD", "PREFLIGHT.MD"} or "PLAYBOOK" in upper:
        return target_root / "documentation" / clean_name
    if clean_name.lower().endswith(".pdf"):
        return target_root / "documentation" / "dossiers" / clean_name
    return None


def unpack_embedded_bundle(target_root: Path, apply: bool, log: SetupLogger) -> None:
    if not EMBEDDED_BUNDLE_B85.strip():
        return
    raw_compressed = base64.b85decode(EMBEDDED_BUNDLE_B85.strip().replace("\n", "").encode("ascii"))
    if EMBEDDED_BUNDLE_SHA256:
        actual = sha256_bytes(raw_compressed)
        if actual != EMBEDDED_BUNDLE_SHA256:
            raise ValueError(f"Embedded bundle SHA-256 mismatch: expected {EMBEDDED_BUNDLE_SHA256}, got {actual}")
    bundle: dict[str, str] = json.loads(lzma.decompress(raw_compressed).decode("utf-8"))
    for rel_key, content in sorted(bundle.items()):
        safe_write_bytes(target_root / rel_key, content.encode("utf-8"), apply, log)


def rescue_top_level_downloads(target_root: Path, slug: str, since_hours: float, apply: bool, log: SetupLogger) -> None:
    """Copy matching files from top-level Downloads/Desktop only; never move or delete in Downloads (S4, S9)."""
    home = Path.home()
    cutoff = time.time() - (since_hours * 3600.0)
    manifest_set = set(EMBEDDED_MANIFEST)
    slug_low = slug.lower()

    candidates = [Path.cwd(), home / "Downloads", home / "Desktop"]
    for od in sorted(home.glob("OneDrive*")):
        candidates.extend([od / "Downloads", od / "Desktop"])

    seen: set[Path] = set()
    for folder in candidates:
        if not folder.is_dir():
            continue
        rf = folder.resolve()
        if rf in seen or rf == target_root.resolve():
            continue
        seen.add(rf)

        for item in sorted(rf.iterdir()):
            if not item.is_file():
                continue
            clean_name = strip_copy_suffix(item.name)
            in_manifest = clean_name in manifest_set
            recent_and_matched = (item.stat().st_mtime >= cutoff) and (
                slug_low in clean_name.lower()
                or clean_name.upper().startswith(("PRD_", "AGENTS_", "SKILL_", "00_MASTER_"))
            )
            if not (in_manifest or recent_and_matched):
                continue
            dest = route_destination(clean_name, target_root)
            if dest is not None:
                safe_write_bytes(dest, item.read_bytes(), apply, log)


def deduplicate_same_folder_copies(target_root: Path, apply: bool, log: SetupLogger) -> None:
    """Only archive `name (1).ext` with byte-identical sibling in the SAME folder; prune heavy dirs (S8, S10, D1, D2)."""
    if not target_root.is_dir():
        return
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    copy_re = re.compile(r"^(.+?)\s*\(\d+\)(\.[^.]+)$")

    for dirpath, dirnames, filenames in os.walk(target_root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        folder = Path(dirpath)
        for fname in sorted(filenames):
            if fname in PROTECTED_FILENAMES:
                continue
            m = copy_re.match(fname)
            if not m:
                continue
            canonical = folder / f"{m.group(1)}{m.group(2)}"
            dup_file = folder / fname
            if canonical.is_file() and sha256_file(canonical) == sha256_file(dup_file):
                rel = dup_file.relative_to(target_root)
                archive_dest = target_root / "_duplicates_archive" / stamp / rel
                log.info(f"  [{'ARCHIVE-DUP' if apply else 'DRY-ARCHIVE-DUP'}] {rel} -> {archive_dest.relative_to(target_root)}")
                if apply:
                    archive_dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dup_file), str(archive_dest))


def init_git_and_venv(target_root: Path, apply: bool, skip_pip: bool, log: SetupLogger) -> int:
    """Initialize git baseline, create .venv, install from requirements.txt, and write requirements.lock (S2, S6)."""
    if not apply:
        log.info("  [DRY-RUN] Would initialize git baseline, .gitignore, and .venv (pass --apply to execute).")
        return 0

    gitignore = target_root / ".gitignore"
    if not gitignore.exists():
        gitignore.write_text(GITIGNORE_DEFAULT, encoding="utf-8")

    if not (target_root / ".git").exists():
        subprocess.run(["git", "init"], cwd=target_root, check=False)
        subprocess.run(["git", "add", "-A"], cwd=target_root, check=False)
        subprocess.run(["git", "commit", "-m", "baseline"], cwd=target_root, check=False)

    venv_dir = target_root / ".venv"
    if not venv_dir.exists():
        r = subprocess.run([sys.executable, "-m", "venv", str(venv_dir)])
        if r.returncode != 0:
            log.info("  [ERROR] Failed to create .venv")
            return 1

    py_exe = venv_dir / ("Scripts/python.exe" if sys.platform.startswith("win") else "bin/python")
    req_file = target_root / "requirements.txt"
    if not skip_pip and req_file.is_file() and py_exe.is_file():
        r = subprocess.run([str(py_exe), "-m", "pip", "install", "-r", str(req_file)])
        if r.returncode != 0:
            log.info("  [ERROR] pip install -r requirements.txt failed")
            return 1
        freeze = subprocess.run([str(py_exe), "-m", "pip", "freeze"], capture_output=True, text=True)
        if freeze.returncode == 0:
            (target_root / "requirements.lock").write_text(freeze.stdout, encoding="utf-8")
            log.info("  [OK] Wrote requirements.lock")
    return 0


def main() -> None:
    ap = argparse.ArgumentParser(description="Hackathon Backend King v3.0 Non-Destructive Workspace Organizer")
    ap.add_argument("--slug", required=True, help="Project slug (required, e.g. 'mirage-z' or 'grid-pulse')")
    ap.add_argument("--target", default="", help="Custom target directory (default: Desktop/<slug>)")
    ap.add_argument("--since-hours", type=float, default=48.0, help="Lookback window in hours for Downloads rescue")
    ap.add_argument("--apply", action="store_true", help="Execute changes on disk (default is dry-run)")
    ap.add_argument("--skip-pip", action="store_true", help="Skip pip install even when --apply is set")
    args = ap.parse_args()

    target_root = Path(args.target).resolve() if args.target else (detect_desktop_dir() / args.slug)
    log = SetupLogger(target_root / "setup.log" if args.apply else None)
    log.info(f"[setup] Project slug: {args.slug} | Target: {target_root} | Mode: {'APPLY' if args.apply else 'DRY-RUN'}")

    for sub in ["documentation/prds", "documentation/agents", "documentation/skills", "documentation/dossiers", "backend", "frontend", "benchmarks", "tests/oracles", "requests", "scripts"]:
        p = target_root / sub
        if args.apply:
            p.mkdir(parents=True, exist_ok=True)
        else:
            log.info(f"  [DRY-MKDIR] {p}")

    unpack_embedded_bundle(target_root, args.apply, log)
    rescue_top_level_downloads(target_root, args.slug, args.since_hours, args.apply, log)
    deduplicate_same_folder_copies(target_root, args.apply, log)
    rc = init_git_and_venv(target_root, args.apply, args.skip_pip, log)
    log.flush()
    sys.exit(rc)


if __name__ == "__main__":
    main()
```

## Part 4: `scripts/phase2_dedup_and_doctor_template.py` (v3.0 with D1–D8 Fixes Applied)

```python
#!/usr/bin/env python3
"""
========================================================================================
HACKATHON BACKEND KING (v3.0) // PHASE 2 AST DOCTOR, SAME-FOLDER DEDUP & GATE AUDITOR
File: phase2_dedup_and_doctor_template.py
========================================================================================

V3.0 FIXES APPLIED (D1-D8):
- D1: Deduplicates ONLY `name (1).ext` files that have a byte-identical canonical sibling
  in the SAME folder. Never touches `__init__.py`, `.gitkeep`, lockfiles, or `LICENSE`.
- D2: Uses `os.walk` with in-place directory pruning so `.venv` and `node_modules` are never walked.
- D3: Archives duplicate copies under `_duplicates_archive/<UTC_timestamp>/` so previous archives are never overwritten.
- D4 & D8: Uses Python AST inspection (not line counts) to identify stub functions (functions whose body is only
  a docstring, `pass`, `...`, `return None`, `return <constant>`, or `raise NotImplementedError`) and records exact
  `stub_functions` names in `PHASE2_DOCTOR_REPORT.json`.
- D5: Does not treat `.vercel` as clutter.
- D6: Runs `scripts/contract_lock.py check` (if present) and `pytest --collect-only -q` to report actual contract and test readiness.
- D7: Report-only by default; requires `--apply` to move any duplicate copy.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

PRUNE_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", "_incoming", "_backups", "_duplicates_archive", "dist", "build"}
CLUTTER_DIRS = {"__MACOSX", ".grok"}
PROTECTED_FILES = {"__init__.py", ".gitkeep", "package-lock.json", "requirements.lock", "contract.lock", "LICENSE"}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def is_stub_function(node: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    """Return True if function body is only docstring, pass, ..., return None/const, or raise NotImplementedError."""
    stmts = list(node.body)
    if stmts and isinstance(stmts[0], ast.Expr) and isinstance(getattr(stmts[0], "value", None), ast.Constant) and isinstance(stmts[0].value.value, str):
        stmts = stmts[1:]
    if not stmts:
        return True
    if len(stmts) > 1:
        return False
    s = stmts[0]
    if isinstance(s, ast.Pass):
        return True
    if isinstance(s, ast.Expr) and isinstance(s.value, ast.Constant) and s.value.value is Ellipsis:
        return True
    if isinstance(s, ast.Return) and (s.value is None or isinstance(s.value, ast.Constant)):
        return True
    if isinstance(s, ast.Raise):
        exc = s.exc
        if isinstance(exc, ast.Name) and exc.id == "NotImplementedError":
            return True
        if isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name) and exc.func.id == "NotImplementedError":
            return True
    return False


def scan_duplicates(root: Path, apply: bool) -> dict[str, int]:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    copy_re = re.compile(r"^(.+?)\s*\(\d+\)(\.[^.]+)$")
    stats = {"clutter_dirs": 0, "same_folder_copies": 0}

    for dirpath, dirnames, filenames in os.walk(root):
        for d in list(dirnames):
            if d in CLUTTER_DIRS:
                src = Path(dirpath) / d
                rel = src.relative_to(root)
                dst = root / "_duplicates_archive" / stamp / rel
                print(f"  [{'ARCHIVE-DIR' if apply else 'REPORT-CLUTTER-DIR'}] {rel}")
                if apply:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(src), str(dst))
                dirnames.remove(d)
                stats["clutter_dirs"] += 1
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]

        folder = Path(dirpath)
        for fname in sorted(filenames):
            if fname in PROTECTED_FILES:
                continue
            m = copy_re.match(fname)
            if not m:
                continue
            canonical = folder / f"{m.group(1)}{m.group(2)}"
            dup = folder / fname
            if canonical.is_file() and sha256_file(canonical) == sha256_file(dup):
                rel = dup.relative_to(root)
                dst = root / "_duplicates_archive" / stamp / rel
                print(f"  [{'ARCHIVE-COPY' if apply else 'REPORT-DUP-COPY'}] {rel} (identical to {canonical.name})")
                if apply:
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(dup), str(dst))
                stats["same_folder_copies"] += 1
    return stats


def audit_python_modules(root: Path) -> list[dict]:
    results: list[dict] = []
    py_files: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in PRUNE_DIRS]
        for f in sorted(filenames):
            if f.endswith(".py"):
                py_files.append(Path(dirpath) / f)

    for py in sorted(py_files):
        rel = py.relative_to(root).as_posix()
        text = py.read_text(encoding="utf-8", errors="replace")
        stub_funcs: list[str] = []
        total_funcs = 0
        status = "READY"
        notes: list[str] = []

        try:
            tree = ast.parse(text, filename=rel)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    total_funcs += 1
                    if is_stub_function(node):
                        stub_funcs.append(node.name)
        except SyntaxError as e:
            status = "SYNTAX_ERROR"
            notes.append(f"line {e.lineno}: {e.msg}")

        if stub_funcs and status != "SYNTAX_ERROR":
            status = "STUB"
            notes.append(f"stub functions: {', '.join(stub_funcs)}")
        elif re.search(r"\b(TODO|FIXME)\b", text) and status == "READY":
            status = "NEEDS_MUSCLE"
            notes.append("contains TODO/FIXME")

        slug = py.stem
        has_test = (root / "tests" / f"test_{slug}.py").is_file()
        row = {
            "file": rel,
            "status": status,
            "total_functions": total_funcs,
            "stub_functions": stub_funcs,
            "has_unit_test": has_test,
            "notes": "; ".join(notes) if notes else "AST complete",
        }
        results.append(row)
        print(f"  [{status:12s}] {rel:36s} | funcs={total_funcs:2d} | stubs={len(stub_funcs):2d} | test={'YES' if has_test else 'NO ':3s} | {row['notes']}")
    return results


def check_contract_and_pytest(root: Path) -> dict[str, str]:
    summary = {"contract_lock": "SKIPPED", "pytest_collect": "SKIPPED"}
    clock = root / "scripts" / "contract_lock.py"
    if clock.is_file() and (root / "contract.lock").is_file():
        r = subprocess.run([sys.executable, str(clock), "check"], cwd=root, capture_output=True, text=True)
        summary["contract_lock"] = "OK" if r.returncode == 0 else f"FAILED ({r.stdout.strip() or r.stderr.strip()})"
    if (root / "tests").is_dir():
        r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"], cwd=root, capture_output=True, text=True)
        summary["pytest_collect"] = "OK" if r.returncode == 0 else "FAILED"
    return summary


def main() -> None:
    ap = argparse.ArgumentParser(description="Hackathon Backend King v3.0 Phase 2 AST Doctor & Deduplicator")
    ap.add_argument("root", nargs="?", default=".", help="Project root directory")
    ap.add_argument("--apply", action="store_true", help="Archive duplicate copies (default is report-only)")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    print(f"[doctor] Inspecting {root} (mode={'APPLY' if args.apply else 'REPORT-ONLY'})")
    dup_stats = scan_duplicates(root, args.apply)
    modules = audit_python_modules(root)
    gates = check_contract_and_pytest(root)

    report = {
        "mode": "apply" if args.apply else "report_only",
        "duplicates": dup_stats,
        "gates": gates,
        "modules": modules,
    }
    out_file = root / "PHASE2_DOCTOR_REPORT.json"
    out_file.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"[doctor] Contract lock: {gates['contract_lock']} | Pytest collect: {gates['pytest_collect']}")
    print(f"[doctor] Wrote {out_file}")


if __name__ == "__main__":
    main()
```
