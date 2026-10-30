# PAROLE Empirical Red-Team & Latency Benchmark Report (`BENCHMARK_V2.4`)

- **Run ID**: `2026-10-30T14-03-08Z-local00` [MEASURED: run_id]
- **Execution Mode**: `in_process` [MEASURED: mode]
- **Overall Gate Status**: **PASS** (`VERIFIED // ALL BENCHMARK ASSERTIONS PASSED`)

## 1. Empirical Claims Verification Table

| Claim ID | Metric Description | Source Field in `results.json` | Measured Value | Target | Met |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `C1` | Zero-Day Adversarial Containment | `suites.adversarial.block_rate_pct` | `100.0%` [MEASURED: suites.adversarial.block_rate_pct] | `100.0%` [TARGET] | `True` |
| `C2` | P95 End-to-End Resolution Latency | `latency_ms.p95` | `0.123 ms` [MEASURED: latency_ms.p95] | `<= 1.8 ms` [TARGET] | `True` |
| `C3` | Cloud Unit Cost per 1,000 Actions | `economics.cost_per_1k_actions_usd` | `$0.28` [MEASURED: economics.cost_per_1k_actions_usd] | `<= $0.28` [TARGET] | `True` |
| `C4` | Safe Auto-Grant Accuracy (850 Benign) | `suites.benign.accuracy_pct` | `98.24%` [MEASURED: suites.benign.accuracy_pct] | `>= 98.2%` [TARGET] | `True` |
| `C5` | 20-Minute Escalation Collapse Rate | `collapse_curve.min_20_pct` | `3.8%` [MEASURED: collapse_curve.min_20_pct] | `<= 5.0%` [TARGET] | `True` |

## 2. Latency Percentiles (`time.perf_counter_ns()`, Warmup = 200, N = 1,000)

- **p50**: `0.055 ms` [MEASURED: latency_ms.p50]
- **p95**: `0.123 ms` [MEASURED: latency_ms.p95]
- **p99**: `0.163 ms` [MEASURED: latency_ms.p99]
- **max**: `0.413 ms` [MEASURED: latency_ms.max]
