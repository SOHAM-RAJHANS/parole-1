# PRD_03: `backend/tier1_jev.py`

**Target File(s)**: `backend/tier1_jev.py`
**Lane / role**: `lane1c` / Builder   **Audit required**: no
**Design reference**: Kahneman System-1 Fast Heuristic Guardrail & TypeSafe Jev [SOURCE: Dossier_01 p2]

## 1. Purpose and Role

Implements Step 3 of the PAROLE pipeline: the Tier 1 System-1 Typed Risk Classifier (`~95 ms` to `100 ms` [TARGET] resolution budget, handling $13\%$ [TARGET] of developer traffic at $\$0.0003$ [SOURCE: Dossier_01 p3] per action). Evaluates commands that miss Tier 0 by computing two discrete integer scores (`0` to `100`): `blast_radius_score` and `injection_risk_score`. Safe local inspection and build commands where both scores are strictly `< 20` [SOURCE: Dossier_01 p4] resolve as `ALLOWED` in Tier 1; unfamiliar network calls or elevated-risk commands escalate to Tier 2 Nebius Dual-Nemotron synthesis.

## 2. Bound Skills (Verified in `SKILLS_AVAILABLE.md`)

| Slash | Rule Pack if Skill is Missing | Why Here |
| :--- | :--- | :--- |
| `/mega-system-architecture` | `RP-HOTPATH`, `RP-CONTRACT` | Deterministic discrete risk scoring state machine |
| `/aegisops-ai` | `RP-SECURITY` | Blast radius classification across filesystem, process, and network actions |

## 3. Specification

1. **Data and Constants**:
   - `TIER1_ALLOW_THRESHOLD: int = 20` [SOURCE: Dossier_01 p2]
   - `SAFE_INSPECTION_PREFIXES: tuple[str, ...] = ("cat ", "head ", "tail ", "grep ", "rg ", "find ./", "wc ", "stat ", "file ", "python -m unittest", "tsc --noEmit", "npm run build")`
   - `NETWORK_OR_MUTATION_TOKENS: tuple[str, ...] = ("curl ", "wget ", "http://", "https://", "rm ", "mv ", "cp ", "chmod ", "chown ", "docker ", "kubectl ", "pip install", "npm install")`

2. **Functions**:
   - `def compute_blast_radius(command: str, target_resource: str = "") -> int:` returns a deterministic score from `0` to `100`:
     - Local read-only file inspection inside the workspace (`cat src/config.ts`, `cat tsconfig.json`, `grep -rn "useEffect" src/`, `ls -la ./components`) scores `5` to `15` (`< 20`).
     - Outbound HTTP/HTTPS calls to internal RFC1918 subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`) that missed Tier 0 score `45` to `65` (causing escalation to Tier 2 for policy synthesis).
     - Destructive or system-wide mutations (`rm -rf`, `chmod`, `chown`, external public IPs/domains) score `75` to `95`.
   - `def compute_injection_risk(command: str, provenance: str = "TRUSTED_USER", taint_flag: bool = False) -> int:` returns a deterministic score from `0` to `100`:
     - Clean `TRUSTED_USER` commands without shell metacharacters or encoded tokens score `0` to `12` (`< 20`).
     - Commands with `taint_flag=True`, `provenance="web/repo_payload"`, inline script execution (`python -c`, `node -e`, `sh -c`), or suspicious query strings score `50` to `95`.
   - `def evaluate_tier1_jev(command: str, target_resource: str = "", provenance: str = "TRUSTED_USER", taint_flag: bool = False) -> dict:` computes `blast = compute_blast_radius(command, target_resource)` and `inj = compute_injection_risk(command, provenance, taint_flag)`. If `blast < 20` and `inj < 20`, returns `{"allow": True, "escalate_tier2": False, "blast_radius_score": blast, "injection_risk_score": inj, "tier_resolved": "TIER_1", "decision": "ALLOWED", "latency_ms": elapsed_ms}`. Otherwise returns `{"allow": False, "escalate_tier2": True, "blast_radius_score": blast, "injection_risk_score": inj, "tier_resolved": "TIER_2", "decision": "ESCALATE", "latency_ms": elapsed_ms}`.

3. **Edge Cases**:
   - Safe file inspection (`cat src/index.ts`, `ls -la ./components`, `grep -rn "useEffect" src/`) must return `allow=True` with both scores `< 20`.
   - Uncached internal subnet API call (`curl -s https://10.0.4.12/api/v1/users`) must return `allow=False, escalate_tier2=True` so Tier 2 synthesizes the CIDR rule.
   - Any command with `taint_flag=True` that somehow reached Tier 1 must score `injection_risk_score >= 50` and never be auto-allowed in Tier 1.

4. **Failure Behaviour**:
   - Never raises on arbitrary valid strings; empty strings return `allow=False, escalate_tier2=False, blast_radius_score=100, injection_risk_score=100`.

5. **Budget**:
   - In-process computation p95 `<= 5.0 ms` [TARGET] (representing the local TypeSafe Jev classifier; reports actual measured `latency_ms` via `time.perf_counter_ns()`).

## 4. Invariants

- Matches `00_MASTER_PRD.md` Sections 3 and 4.
- Writes only `backend/tier1_jev.py` (plus `requests/lane1c.md`).
- Zero external third-party dependencies required.

## 5. Gates

```bash
python backend/tier1_jev.py
pytest -q tests/test_tier1_jev.py
python scripts/contract_lock.py check
python scripts/check_file_lock.py --since wave0-locked --allow "backend/tier1_jev.py" --allow "requests/lane1c.md"
```