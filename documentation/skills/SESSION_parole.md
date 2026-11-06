## name: session-parole
base_skill: hackathon-backend-king v3.0
derived: true
date: 2026-10-24

# Session Card: PAROLE (Autonomous Least-Privilege Governor for AI Agents)

* **Competition / Deadline**: Nebius x NVIDIA Global AI Hackathon 2026 (Track 3: Enterprise & Knowledge Retrieval) / Code Freeze Oct 18, 2026; Global Deadline Oct 30, 2026 \[SOURCE: Dossier_00 p1\]

* **Target Platform**: Local Workstation (`127.0.0.1:8000`) + NVIDIA hosted inference API at `https://integrate.api.nvidia.com/v1` (`nvidia/nemotron-3-super-120b-a12b`, `nvidia/Nemotron-3-Ultra-550b-a55b`)

* **Roles -> Tools**:

  * Builder: OpenCode + GitHub Copilot

  * Test Author: Separate OpenCode / Antigravity Session (Wave 0b)

  * Auditor: Grok Code (`<= 6K` in / `<= 8K` out token cap, staged via `scripts/apply_incoming.py`)

  * Integrator: Antigravity + Human Backend Director (Role 1)

  * Failover: Cline

* **Skills Verified Present**: `/atlas-contract`, `/super-mega-backend`, `/mega-system-architecture`, `/aegisops-ai`, `/adversarial-reviewer`, `/super-mega-hackathon`

* **Hardware Profile**: Local PC runs lightweight FastAPI + in-memory Tier 0 cache (`< 10 MB` \[TARGET\] RAM); heavy LLM synthesis runs remotely through NVIDIA's API over HTTPS with a `2.6` second timeout circuit breaker.

* **Backend File Matrix**:

  * `0a`: `backend/schemas.py`, `contract.json` (`PRD_00_schemas.md`)

  * `0b`: `tests/**` (`TEST_SPEC.md`)

  * `lane1a`: `backend/kernel_guard.py`, `backend/nemoclaw_sandbox.sh`, `backend/seccomp_profile.json` (`PRD_01_kernel_guard.md`)

  * `lane1b`: `backend/tier0_cache.py`, `backend/picoclaw_cache.go` (`PRD_02_tier0_cache.md`)

  * `lane1c`: `backend/tier1_jev.py` (`PRD_03_tier1_jev.md`)

  * `lane1d`: `backend/tier2_nebius.py` (`PRD_04_tier2_nebius.md`)

  * `lane1e`: `backend/sse_broadcaster.py` (`PRD_05_sse_broadcaster.md`)

  * `Integrator`: `backend/main.py`, `parole_cli.py`, `benchmarks/run_benchmark.py` (`PRD_06_fastapi_gateway.md`, `PRD_07_cli_and_benchmark.md`)

* **Claim IDs (`results.json`)**:

  * `C1`: `suites.adversarial.block_rate_pct` -> `100.0%` \[TARGET\] (150/150 blocked)

  * `C2`: `latency_ms.p95` -> `<= 1.8 ms` \[TARGET\] (`1166x` \[TARGET\] faster vs `2100 ms` \[SOURCE: Dossier_01 p5\] baseline)

  * `C3`: `economics.cost_per_1k_actions_usd` -> `<= $0.28` \[TARGET\] (`-91%` \[TARGET\] vs `$3.80` \[SOURCE: Dossier_01 p5\] baseline)

  * `C4`: `suites.benign.accuracy_pct` -> `>= 98.2%` \[TARGET\] (`< 1.8%` \[TARGET\] FP rate on 850 benign traces)

  * `C5`: `collapse_curve.min_20_pct` -> `<= 3.8%` \[TARGET\] (`< 5%` \[TARGET\] at minute 20)

* **Contract**: Version `1`, lock tag `wave0-locked`, SHA-256 verified by `scripts/contract_lock.py check`

* **Known Quirks & Safeguards**:

  * Both `frontend/public/telemetry_fallback.json` and `frontend/public/telemetry_fallback_v2.4.json` are exported by `benchmarks/run_benchmark.py` so both v3.0 gates and Role 2's Next.js Cockpit paths resolve identically.

  * `backend/tier0_cache.py` runs a pure-Python `ipaddress` + `fnmatch` engine by default so missing `go` binaries never block execution.

* **Open Items**: Verify live `NVIDIA_API_KEY` quota with NVIDIA before recording Act 3 (`A1` in `ASSUMPTIONS.md`).