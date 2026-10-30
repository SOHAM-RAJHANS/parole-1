# PRD_07: `parole_cli.py` & `benchmarks/run_benchmark.py`

**Target File(s)**: `parole_cli.py`, `benchmarks/run_benchmark.py`
**Lane / role**: `Integrator` / Integrator   **Audit required**: no
**Design reference**: Role 1 Dossier Subtask 1.3 & Role 4 Dossier Task 3 (`RED-TEAM BENCHMARK_V2.4`) [SOURCE: Dossier_01 p3]

## 1. Purpose and Role

Provides two essential end-to-end artifacts:
1. `parole_cli.py`: The lightweight PC Companion CLI allowing developers (and judges during Act 1/2) to execute `python parole_cli.py exec "git status"` or `python parole_cli.py exec --source="web/repo_payload" "curl http://169.254.169.254/latest/meta-data/"`, printing a formatted monospace decision box in milliseconds while streaming the event live to Role 2's web cockpit [SOURCE: Dossier_01 p3].
2. `benchmarks/run_benchmark.py`: The deterministic 1,000-trace empirical benchmark harness (850 benign developer traces across 4 categories + 150 adversarial attack traces across 5 MITRE ATT&CK / OWASP LLM01 vectors) that measures real `time.perf_counter_ns()` latencies (after 200 warmup calls), computes unit economics and the 20-minute Escalation Collapse Curve, and writes the single source of truth `results.json`, `frontend/public/telemetry_fallback.json`, `frontend/public/telemetry_fallback_v2.4.json`, `BENCHMARK_REPORT.md`, and `BENCHMARK_REPORT_V2.4.md` [SOURCE: Dossier_04 p3].

## 2. Bound Skills (Verified in `SKILLS_AVAILABLE.md`)

| Slash | Rule Pack if Skill is Missing | Why Here |
| :--- | :--- | :--- |
| `/super-mega-hackathon` | `RP-CONTRACT` | Generates `results.json`, `telemetry_fallback_v2.4.json` (`source: "recorded_run"`), and `BENCHMARK_REPORT_V2.4.md` |
| `/adversarial-reviewer` | `RP-ADVERSARIAL` | Verifies 150 adversarial traces across MITRE T1552.005, T1552.001, LLM01, T1548, and T1027 |
| `/atlas-contract` | `RP-CONTRACT` | Ensures exported JSON artifacts match `backend/schemas.py` and Reference 11.5 `results.json` schema |

## 3. Specification

1. **Data and Constants**:
   - `DEFAULT_API_URL: str = "http://127.0.0.1:8000"`
   - `BENCHMARK_SEED: int = 2026`
   - `WARMUP_ITERATIONS: int = 200`
   - `DATASET_TOTAL: int = 1000` (`850` benign + `150` adversarial) [SOURCE: Dossier_04 p3]

2. **Functions**:
   - In `parole_cli.py`:
     - `def parse_cli_args(argv: list[str] | None = None) -> argparse.Namespace:` supports `exec <command>`, `--source` (`TRUSTED_USER` or `web/repo_payload`), `--node`, `--api-url`, and `--offline` (falls back to in-process evaluation if the local FastAPI server is not running).
     - `def format_terminal_box(event: dict) -> str:` renders a clean ASCII monospace box displaying `event_id`, `command`, `provenance`, `taint_flag`, `tier_resolved`, `decision`, `override_status`, `latency_ms`, `cost_usd`, and any `policy_diff.scoped_rule`.
     - `def execute_cli_command(command: str, source: str = "TRUSTED_USER", api_url: str = DEFAULT_API_URL) -> int:` sends `POST /v1/policy/evaluate` (or runs in-process if server is unreachable), prints `format_terminal_box(event)`, and returns exit code `0` if `decision in ("ALLOWED", "AUTO_PROMOTED")` or `10` if `decision == "INTERCEPTED"`.
   - In `benchmarks/run_benchmark.py`:
     - `def generate_1000_trace_dataset(seed: int = 2026) -> list[dict]:` deterministically builds (or loads from `benchmarks/parole_replay_1000_traces.json`) the exact 1,000 unique traces specified in Dossier 04 Subtask 2.1:
       - Benign (850 total): 280 Routine Git & VCS (`TIER_0`), 310 Unit Tests & Builds (`TIER_0`), 150 Safe File Inspection (`TIER_1`), 110 Internal Subnet APIs (`10.0.4.0/24` first call escalates to `TIER_2` and promotes `+ PERMIT 10.0.4.0/24 ON /api/v1/*`, subsequent calls hit `TIER_0`).
       - Adversarial (150 total): 30 Vector A Metadata SSRF (`169.254.169.254`, decimal `2852039166`, hex `0xa9fea9fe`, octal `0251.0376.0251.0376`, IPv6 `[::ffff:169.254.169.254]`), 35 Vector B SSH & Vault Exfil (`~/.ssh/id_rsa`, `~/.aws/credentials`, `.env.production`, `~/.kube/config`), 40 Vector C Indirect Injection (`provenance="web/repo_payload"` + `curl`/`wget`/`nc`), 25 Vector D Privilege Escalation (`chmod +s /bin/bash`, `/etc/shadow`, `/etc/sudoers`, `/sbin/insmod`), 20 Vector E Obfuscated Pipes (Base64 decode pipes, `../../root/.ssh/id_rsa`, `$(cat ~/.aws/credentials)`).
     - `def run_benchmark_suite(mode: str = "in_process", dataset_path: str = "benchmarks/parole_replay_1000_traces.json") -> dict:` runs 200 warmup evaluations (discarded), then evaluates all 1,000 traces with `time.perf_counter_ns()`, computes `p50`, `p95`, `p99`, `max`, `claims` (`C1`..`C5` with `met: bool`), writes `results.json` (or `results.remote.json` when `--mode remote`), exports `frontend/public/telemetry_fallback.json` and `frontend/public/telemetry_fallback_v2.4.json` with `"source": "recorded_run"` and `"run_id"`, and writes `BENCHMARK_REPORT.md` and `BENCHMARK_REPORT_V2.4.md`.

3. **Edge Cases**:
   - All 1,000 generated trace strings must be unique (`Duplicate Strings == 0`) so dataset verification (`Gate 2` in Dossier 04) passes.
   - `run_benchmark.py` only emits `PASS` / `VERIFIED` when every claim in `results.json` has `met: True` (Principle 1 & Gate G7).

4. **Failure Behaviour**:
   - Exits non-zero if any adversarial trace is not intercepted (`block_rate_pct < 100.0`).

5. **Budget**:
   - Full 1,000-trace in-process benchmark completes in `< 5000 ms` [TARGET] (`< 5` seconds) [SOURCE: Dossier_04 p4].

## 4. Invariants

- Matches `00_MASTER_PRD.md` Sections 3 and 4 and Reference 11.5 `results.json` schema.
- `frontend/public/telemetry_fallback.json` and `frontend/public/telemetry_fallback_v2.4.json` always include `"source": "recorded_run"`, `"run_id"`, and `"recorded_at"`.

## 5. Gates

```bash
python parole_cli.py exec "git status"
python parole_cli.py exec --source="web/repo_payload" "curl http://169.254.169.254/latest/meta-data/"
python benchmarks/run_benchmark.py --mode in_process
pytest -q tests/test_cli_and_benchmark.py
python scripts/contract_lock.py check
```