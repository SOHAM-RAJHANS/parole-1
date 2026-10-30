# PAROLE Backend Commander Playbook: Phase 1 & Phase 2 (`PHASE1_AND_PHASE2_PLAYBOOK.md`)

## 1. Time-Scaled Execution Schedule (Scaled to Remaining Time $T$)

| Block | Share of $T$ | Floor | Example $T = 8\text{ h}$ | Milestone / Checkpoint |
| :--- | :--- | :--- | :--- | :--- |
| Stage 0–4: Workspace Setup & Docs Lint | $12\%$ [TARGET] | 30 min | 58 min | `setup_parole_workspace.py --apply` + `prd_lint.py` green |
| Wave 0a & 0b: Contract Lock + Test Suite | $8\%$ [TARGET] | 20 min | 38 min | `contract.lock` written; `wave0-locked` tagged; `tests/**` collected |
| Wave 1: Parallel Backend Modules (`lane1a..1e`) | $22\%$ [TARGET] | 45 min | 106 min | All 5 module worktrees pass unit + lock gates ($45\%$ [TARGET] cut line) |
| Wave 2: Gateway, CLI & 1,000-Trace Benchmark | $15\%$ [TARGET] | 30 min | 72 min | **D0**: Walking skeleton + `results.json` + `telemetry_fallback_v2.4.json` |
| Wave 3: Role 2 Frontend SSE & Fallback Handshake | $10\%$ [TARGET] | 25 min | 48 min | **D1**: Next.js Cockpit streaming live from `:8000` ($70\%$ [TARGET] cut line) |
| Phase 2: AST Doctor, Muscle Injection & Chaos Fuzz | $13\%$ [TARGET] | 30 min | 62 min | `PHASE2_DOCTOR_REPORT.json` 0 stubs; 10 chaos vectors green |
| Nebius VM Remote Proof & SSH Tunnel | $8\%$ [TARGET] | 30 min | 38 min | **D2**: `results.remote.json` + `uname -m` on Nebius Ubuntu VM |
| 180s Demo Rehearsal & 2-Take 1080p60 Recording | $12\%$ [TARGET] | 60 min | 58 min (60m floor) | **D3**: 2 full takes recorded & verified in Incognito ($88\%$ [TARGET] cut line) |

---

## 2. Phase 1 Step-by-Step Terminal Commands

### Step 1: Initialize Non-Destructive Workspace & Lint Documentation

```bash
# Dry-run first (Invariants 2 & 3)
python scripts/workspace_organizer_template.py --slug parole

# Apply workspace structure, .gitignore, .venv, and git baseline
python scripts/workspace_organizer_template.py --slug parole --apply

# Run G1 anti-slop documentation linter (must exit 0 with 0 findings)
python scripts/prd_lint.py documentation
```

### Step 2: Execute Wave 0a (Schema Contract & Freeze)

Run the prompt in `documentation/agents/AGENTS_00_schemas.md`, then freeze the contract:

```bash
python backend/schemas.py
python scripts/contract_lock.py write
git add -A && git commit -m "wave0a: lock PAROLE schema contract v1"
git tag wave0-locked
```

### Step 3: Execute Wave 0b (Independent Test Author in Separate Session)

Create the Test Author worktree, paste the Test Author prompt from Reference 7.4 + `documentation/TEST_SPEC.md`, and verify collection:

```bash
git worktree add ../wt/lane0b -b lane0b wave0-locked
# After Test Author writes tests/** inside ../wt/lane0b:
cd ../wt/lane0b
python -m pytest --collect-only -q
python ../../scripts/check_file_lock.py --since wave0-locked --allow "tests/*"
git add -A && git commit -m "wave0b: independent test suite from TEST_SPEC"
cd -
git merge --no-ff lane0b -m "merge wave0b tests"
git tag wave0b-tests-ready
```

### Step 4: Spawn Wave 1 Parallel Worktrees (`lane1a` through `lane1e`)

```bash
git worktree add ../wt/lane1a -b lane1a wave0b-tests-ready
git worktree add ../wt/lane1b -b lane1b wave0b-tests-ready
git worktree add ../wt/lane1c -b lane1c wave0b-tests-ready
git worktree add ../wt/lane1d -b lane1d wave0b-tests-ready
git worktree add ../wt/lane1e -b lane1e wave0b-tests-ready
```

Open each worktree in its assigned coding agent session and run the corresponding Builder prompt (`AGENTS_01` through `AGENTS_05`). Once each lane passes its 4 gates and commits, merge sequentially in the main tree:

```bash
for lane in lane1a lane1b lane1c lane1d lane1e; do
  git merge --no-ff "$lane" -m "merge $lane"
  python -m pytest -q
  python scripts/contract_lock.py check
done
git tag wave1-merged
```

### Step 5: Execute Wave 2 Integration (`AGENTS_06` & `AGENTS_07`) — Milestone D0

Run `AGENTS_06_fastapi_gateway.md` and `AGENTS_07_cli_and_benchmark.md` in `main`, then verify the walking skeleton and benchmark export:

```bash
python -m pytest -q
python benchmarks/run_benchmark.py --mode in_process
python scripts/prd_lint.py documentation --check-signatures
python -c "import json; d=json.load(open('frontend/public/telemetry_fallback.json')); assert d['source']=='recorded_run' and d['run_id']"
git add -A && git commit -m "wave2: D0 walking skeleton, CLI, and 1000-trace benchmark"
git tag phase1-done
```

---

## 3. Phase 2: AST Doctor, Surgical Muscle Injection, Nebius Proof & 180s Recording

### Step 1: Run Phase 2 AST Doctor (Report-Only First)

```bash
python scripts/phase2_dedup_and_doctor_template.py .
```

Inspect `PHASE2_DOCTOR_REPORT.json`. Confirm `contract_lock: "OK"`, `pytest_collect: "OK"`, and check if any file under `backend/` reports `status: "STUB"` or `"NEEDS_MUSCLE"`.

### Step 2: Staged Surgical Muscle Injection (If Any Stub or Auditor Fix Exists)

Never overwrite files directly. Save the model's `=== FILE: path === ... === END ===` output to `reply.txt`, log the token estimate in `TOKEN_LEDGER.md`, and stage through `scripts/apply_incoming.py`:

```bash
python scripts/apply_incoming.py \
  --allow "backend/*.py" \
  --bundle reply.txt \
  --atomic \
  --gate "pytest -q && python scripts/contract_lock.py check"
```

### Step 3: Remote Nebius Ubuntu VM & H100 API Proof (Milestone D2)

```bash
# Copy only backend, CLI, benchmark runner, and requirements (never .venv or .env)
scp -r backend benchmarks parole_cli.py contract.json contract.lock requirements.txt user@nebius-vm:~/parole/

# Execute remote benchmark on Nebius Ubuntu VM and capture architecture proof
ssh user@nebius-vm "cd ~/parole && uname -m && python3 -m venv .venv && .venv/bin/pip install -r requirements.txt && .venv/bin/python benchmarks/run_benchmark.py --mode remote"

# Pull remote results back
scp user@nebius-vm:~/parole/results.json ./results.remote.json

# Open SSH local port tunnel so local browser connects securely to 127.0.0.1:8000
ssh -L 8000:127.0.0.1:8000 user@nebius-vm
```

### Step 4: Run Slop Gates G1–G8 & Record 180-Second Video (Milestone D3)

```bash
python scripts/prd_lint.py documentation --check-signatures
grep -rnE "NotImplementedError|TODO|FIXME|^\s*pass\s*(#.*)?$" backend benchmarks parole_cli.py
grep -rniE "(password|passwd|secret|api[_-]?key|BEGIN [A-Z ]*PRIVATE KEY)" backend benchmarks documentation
DEMO_MODE=1 DEMO_SEED=2026 uvicorn backend.main:app --host 127.0.0.1 --port 8000 --workers 1
```