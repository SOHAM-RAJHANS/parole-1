# Stage 1 Preflight & Hardware Profile (`PREFLIGHT.md`)

**Project**: PAROLE — Autonomous Least-Privilege Governor for AI Agents [SOURCE: Dossier_00 p1]
**Target Architectures**: Local Developer Workstation (`x86_64` / `arm64`) + Nebius AI Cloud Ubuntu VM (`x86_64` with NVIDIA H100 inference via Nebius Token Factory HTTPS API) [SOURCE: Dossier_01 p2]

## 1. Local Workstation Profile

- **Execution Rule**: Local PC runs only Python 3.11+ (`FastAPI` + `uvicorn`) and the lightweight Go cache binary (`picoclaw_cache` using under 10 MB RAM, equivalent to $0.98\%$ of 1 GB RAM [TARGET]), with zero local LLM weights or heavy container daemons [SOURCE: Dossier_00 p3].
- **Bind Address**: `127.0.0.1:8000` by default; remote Nebius VM connects via SSH local port forwarding (`ssh -L 8000:127.0.0.1:8000 user@nebius-vm`).
- **Virtual Environment**: `.venv` in repository root; dependencies frozen to `requirements.lock`.

## 2. Target Architecture & Binary Wheel Verification

Run the preflight wheel verification before Wave 0a:

```bash
python --version
go version
git --version
python -m pip install --dry-run --only-binary=:all: fastapi "uvicorn[standard]" pydantic httpx pytest pytest-asyncio
```

| Package | Required By | Binary Wheel Status (`x86_64` / `arm64`) | Pure-Python / Stdlib Fallback Strategy |
| :--- | :--- | :--- | :--- |
| `fastapi` | `backend/main.py` | Verified prebuilt wheel | Required core web framework |
| `uvicorn[standard]` | `backend/main.py` | Verified prebuilt wheel | Pure-Python `uvicorn` loop if `uvloop` wheel is absent on Windows |
| `pydantic` | `backend/schemas.py` | Verified prebuilt `pydantic-core` wheel | Pinned to binary wheel version in `requirements.txt` |
| `httpx` | `backend/tier2_nebius.py`, `parole_cli.py` | Verified prebuilt wheel | `urllib.request` in `parole_cli.py` and `fallback_nano_adapter` in `tier2_nebius.py` |
| `pytest` / `pytest-asyncio` | `tests/**` | Verified prebuilt wheel | Standard library `unittest` runner fallback |
| Go (`picoclaw_cache.go`) | `backend/tier0_cache.py` | Optional native binary | Pure-Python `ipaddress` + `fnmatch` in-memory engine in `backend/tier0_cache.py` selected at import time |

## 3. Machine-Readable Profile (`ENV_PROFILE.json` Schema)

```json
{
  "project_slug": "parole",
  "local": {
    "os": "linux_or_windows_wsl2",
    "python": "3.11+",
    "ram_budget_mb": 256,
    "bind_host": "127.0.0.1",
    "bind_port": 8000
  },
  "target": {
    "provider": "Nebius AI Cloud",
    "vm_arch": "x86_64",
    "gpu_backend": "Nebius Token Factory H100 API",
    "primary_model": "nvidia/nemotron-3-super-120b-a12b",
    "auditor_model": "nvidia/Nemotron-3-Ultra-550b-a55b",
    "fallback_adapter": "nemotron-nano-json-structured-adapter"
  },
  "venv_python": ".venv/bin/python",
  "wheel_check": "PASS"
}
```