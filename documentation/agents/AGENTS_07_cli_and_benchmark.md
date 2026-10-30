# AGENTS_07: `parole_cli.py` & `benchmarks/run_benchmark.py`

**Companion PRD**: `documentation/prds/PRD_07_cli_and_benchmark.md`
**Lane / worktree**: `Integrator` / `main` (Wave 2)   **Audit required**: no

## 1. Execution Blueprint

```yaml
goal: Implement parole_cli.py and benchmarks/run_benchmark.py, generate the 1,000-trace dataset, and produce results.json, telemetry_fallback_v2.4.json, and BENCHMARK_REPORT_V2.4.md.
allowlist:
  - "parole_cli.py"
  - "benchmarks/run_benchmark.py"
  - "benchmarks/parole_replay_1000_traces.json"
  - "results.json"
  - "frontend/public/telemetry_fallback.json"
  - "frontend/public/telemetry_fallback_v2.4.json"
  - "BENCHMARK_REPORT.md"
  - "BENCHMARK_REPORT_V2.4.md"
base_tag: wave1-merged
budget: < 5000 ms for 1,000-trace in-process benchmark run
gates:
  - python parole_cli.py exec "git status"
  - python parole_cli.py exec --source="web/repo_payload" "curl http://169.254.169.254/latest/meta-data/"
  - python benchmarks/run_benchmark.py --mode in_process
  - pytest -q tests/test_cli_and_benchmark.py
  - python scripts/contract_lock.py check
```

## 2. Prompts

### Builder (Paste as is into OpenCode in `main`)

```text
/super-mega-hackathon /adversarial-reviewer /atlas-contract
ROLE: Builder (Wave 2 CLI & Benchmark Harness).
FILE LOCK: write ONLY parole_cli.py, benchmarks/run_benchmark.py, and the generated benchmark outputs (benchmarks/parole_replay_1000_traces.json, results.json, frontend/public/telemetry_fallback.json, frontend/public/telemetry_fallback_v2.4.json, BENCHMARK_REPORT.md, BENCHMARK_REPORT_V2.4.md).
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_07_cli_and_benchmark.md
  3. tests/test_cli_and_benchmark.py
RULES:
RP-CONTRACT
- results.json must conform to Reference 11.5 schema (schema_version, run_id, git_commit, dirty, mode, host, latency_ms, suites, claims).
- frontend/public/telemetry_fallback.json and frontend/public/telemetry_fallback_v2.4.json must include "source": "recorded_run", "run_id", "recorded_at", and "events".
RP-HOTPATH
- Measure latencies with time.perf_counter_ns() after 200 warmup calls.
- Compute PASS in BENCHMARK_REPORT.md and BENCHMARK_REPORT_V2.4.md if and only if every claim in results.json has met: true.
DONE WHEN every gate in documentation/agents/AGENTS_07_cli_and_benchmark.md section 1 exits 0. Paste each command and its exit code in your reply.
```