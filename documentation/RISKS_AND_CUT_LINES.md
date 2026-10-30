# Risks and Cut Lines (`RISKS_AND_CUT_LINES.md`)

**Hard Code Freeze**: October 18, 2026 at 23:59 IST ahead of the October 30, 2026 global deadline [SOURCE: Dossier_00 p1].

## 1. Technical & Operational Risk Matrix

| Risk | Likelihood | Early Signal | Pre-Agreed Fallback |
| :--- | :--- | :--- | :--- |
| Nebius Token Factory API experiences rate limits, high latency (`> 2600 ms` [TARGET]), or Wi-Fi drops during live demo | Medium | `httpx.TimeoutException` or HTTP 429/5xx in `tier2_nebius.py` | `asyncio.wait_for(..., timeout=2.6)` automatically triggers `fallback_nano_adapter()`, returning a verified `PolicyDiff` in `1800 ms` [TARGET] with `capability: "simulated"` |
| Go compiler (`go`) unavailable on teammate or judge machine for `picoclaw_cache.go` | Medium | `shutil.which("go") is None` during preflight | `backend/tier0_cache.py` runs its pure-Python `ipaddress.ip_network` + `fnmatch` engine in memory under `1.8 ms` [TARGET] with zero external process dependency |
| Browser tab refresh during SSE streaming raises `RuntimeError: Set changed size during iteration` | High (if naive) | Concurrent `curl -N /v1/policy/stream` disconnect test fails | `backend/sse_broadcaster.py` iterates over `list(subscribers.items())` snapshot and cleans up queues inside `finally:` blocks |
| Sneaky adversarial trace (octal IP, nested `$()` subshell, or Base64 pipe) bypasses naive regex | Medium | Any of the 150 adversarial traces in `run_benchmark.py` returns `ALLOWED` | `backend/kernel_guard.py` iteratively decodes Base64/hex pipes, strips subshells, and parses decimal/hex/octal/IPv6 addresses via `ipaddress` before checking denylists |
| Wave 1 module misses latency or accuracy target in `results.json` | Low | Benchmark claim `met: false` in `results.json` | Optimize hot-path precomputation in `kernel_guard.py` and `tier0_cache.py`; never hardcode or fabricate numbers in `results.json` |

## 2. Hard Time-Scaled Cut Lines (Percentage of Remaining Time $T$)

- **At $45\%$ [TARGET] of $T$ (Wave 1 Freeze Gate)**: All core backend modules (`kernel_guard.py`, `tier0_cache.py`, `tier1_jev.py`, `tier2_nebius.py`, `sse_broadcaster.py`) must pass `pytest -q`. Any incomplete external integration defaults to its contract-conformant `capability: "simulated"` adapter.
- **At $70\%$ [TARGET] of $T$ (Feature Freeze & D0/D1 Gate)**: Walking skeleton (`POST /v1/policy/evaluate`, `GET /v1/policy/stream`, `POST /v1/demo/run-180s`) and `telemetry_fallback_v2.4.json` export must be complete and wired into Role 2's Frontend. Zero new endpoints or schema changes after this point.
- **At $88\%$ [TARGET] of $T$ (Mandatory Demo Recording Gate)**: Stop all code edits, lock `DEMO_MODE=1` and `DEMO_SEED=2026`, rehearse twice with a stopwatch, and record two complete 180-second takes at 1080p60.