#!/usr/bin/env python3
"""
========================================================================================
PAROLE // DOWNLOADED CHAT FILES SORTER & REPOSITORY ORGANIZER (`setup_parole_workspace.py`)
Target Repository: Desktop/parole-1
========================================================================================

WHAT THIS SCRIPT DOES:
  1. Scans your `Downloads`, `Desktop`, and current folder for all files downloaded from
     this chat (matching BOTH the Gemini `snake_case` title names shown in your Windows
     Downloads folder AND the canonical filenames).
  2. Copies and renames every file into its exact canonical path inside `Desktop/parole-1/`
     (never deletes anything from your `Downloads` folder).
  3. Strips any accidental outer ```python / ```json markdown fences from code/config
     files so every `.py`, `.go`, `.json`, `.sh`, and `.txt` file is valid and runnable.
  4. Writes `contract.lock`, runs the 1,000-trace benchmark to populate `results.json`
     and `frontend/public/telemetry_fallback_v2.4.json`, and initializes Git in `Desktop/parole-1`.

HOW TO RUN:
  python parole_downloaded_files_sorter_and_repo_organizer.py
  (or: python setup_parole_workspace.py)
"""
from __future__ import annotations

import argparse
import ctypes
import hashlib
import os
import re
import subprocess
import sys
import time
from pathlib import Path

# --------------------------------------------------------------------------------------
# 1. EXACT GEMINI CANVAS SNAKE_CASE STEM -> CANONICAL REPO PATH MAPPING
#    (Matches every single file shown in your Windows `Downloads` screenshot!)
# --------------------------------------------------------------------------------------
STEM_TO_REPO_PATH: dict[str, str] = {
    # Stage 0-2 Documentation & Skills
    "verified_skills_inventory": "documentation/skills/SKILLS_AVAILABLE.md",
    "skills_available": "documentation/skills/SKILLS_AVAILABLE.md",
    "environment_and_nebius_preflight": "documentation/PREFLIGHT.md",
    "preflight": "documentation/PREFLIGHT.md",
    "architectural_assumptions_log": "documentation/ASSUMPTIONS.md",
    "assumptions": "documentation/ASSUMPTIONS.md",
    "hackathon_rubric_to_deliverable_map": "documentation/RUBRIC_MAP.md",
    "rubric_map": "documentation/RUBRIC_MAP.md",
    "risks_and_hard_time_cut_lines": "documentation/RISKS_AND_CUT_LINES.md",
    "risks_and_cut_lines": "documentation/RISKS_AND_CUT_LINES.md",
    "master_backend_prd": "documentation/00_MASTER_PRD.md",
    "00_master_prd": "documentation/00_MASTER_PRD.md",
    "independent_test_author_specification": "documentation/TEST_SPEC.md",
    "test_spec": "documentation/TEST_SPEC.md",
    "master_agents_orchestration_guide": "documentation/00_MASTER_AGENTS.md",
    "00_master_agents": "documentation/00_MASTER_AGENTS.md",
    "phase_1_and_phase_2_commander_playbook": "documentation/PHASE1_AND_PHASE2_PLAYBOOK.md",
    "phase1_and_phase2_playbook": "documentation/PHASE1_AND_PHASE2_PLAYBOOK.md",
    "parole_project_session_card": "documentation/skills/SESSION_parole.md",
    "session_parole": "documentation/skills/SESSION_parole.md",
    "hackathon_backend_king_v3_complete": "documentation/skills/hackathon_backend_king_v3_complete.md",

    # Module PRDs (PRD_00 .. PRD_07)
    "prd_00_schema_contract": "documentation/prds/PRD_00_schemas.md",
    "prd_00_schemas": "documentation/prds/PRD_00_schemas.md",
    "prd_01_kernel_guard_and_taint_engine": "documentation/prds/PRD_01_kernel_guard.md",
    "prd_01_kernel_guard": "documentation/prds/PRD_01_kernel_guard.md",
    "prd_02_tier_0_picoclaw_cache": "documentation/prds/PRD_02_tier0_cache.md",
    "prd_02_tier0_cache": "documentation/prds/PRD_02_tier0_cache.md",
    "prd_03_tier_1_typed_risk_classifier": "documentation/prds/PRD_03_tier1_jev.md",
    "prd_03_tier1_jev": "documentation/prds/PRD_03_tier1_jev.md",
    "prd_04_tier_2_nebius_dual_nemotron_orchestrator": "documentation/prds/PRD_04_tier2_nebius.md",
    "prd_04_tier2_nebius": "documentation/prds/PRD_04_tier2_nebius.md",
    "prd_05_sse_broadcaster_and_telemetry_hub": "documentation/prds/PRD_05_sse_broadcaster.md",
    "prd_05_sse_broadcaster": "documentation/prds/PRD_05_sse_broadcaster.md",
    "prd_06_fastapi_sovereign_gateway": "documentation/prds/PRD_06_fastapi_gateway.md",
    "prd_06_fastapi_gateway": "documentation/prds/PRD_06_fastapi_gateway.md",
    "prd_07_pc_cli_and_benchmark_runner": "documentation/prds/PRD_07_cli_and_benchmark.md",
    "prd_07_cli_and_benchmark": "documentation/prds/PRD_07_cli_and_benchmark.md",

    # Role-Based Agent Guides (AGENTS_00 .. AGENTS_07)
    "agents_00_schema_contract": "documentation/agents/AGENTS_00_schemas.md",
    "agents_00_schemas": "documentation/agents/AGENTS_00_schemas.md",
    "agents_01_kernel_guard": "documentation/agents/AGENTS_01_kernel_guard.md",
    "agents_02_tier_0_picoclaw_cache": "documentation/agents/AGENTS_02_tier0_cache.md",
    "agents_02_tier0_cache": "documentation/agents/AGENTS_02_tier0_cache.md",
    "agents_03_tier_1_typed_risk_classifier": "documentation/agents/AGENTS_03_tier1_jev.md",
    "agents_03_tier1_jev": "documentation/agents/AGENTS_03_tier1_jev.md",
    "agents_04_tier_2_nebius_dual_nemotron": "documentation/agents/AGENTS_04_tier2_nebius.md",
    "agents_04_tier2_nebius": "documentation/agents/AGENTS_04_tier2_nebius.md",
    "agents_05_sse_broadcaster": "documentation/agents/AGENTS_05_sse_broadcaster.md",
    "agents_06_fastapi_gateway_integrator": "documentation/agents/AGENTS_06_fastapi_gateway.md",
    "agents_06_fastapi_gateway": "documentation/agents/AGENTS_06_fastapi_gateway.md",
    "agents_07_cli_and_benchmark_suite": "documentation/agents/AGENTS_07_cli_and_benchmark.md",
    "agents_07_cli_and_benchmark": "documentation/agents/AGENTS_07_cli_and_benchmark.md",

    # Backend Implementation Modules
    "backend_pydantic_v2_schema_contract": "backend/schemas.py",
    "schemas": "backend/schemas.py",
    "out_of_process_kernel_guard_and_taint_engine": "backend/kernel_guard.py",
    "kernel_guard": "backend/kernel_guard.py",
    "nemoclaw_linux_landlock_and_seccomp_sandbox_script": "backend/nemoclaw_sandbox.sh",
    "nemoclaw_sandbox": "backend/nemoclaw_sandbox.sh",
    "nemoclaw_seccomp_bpf_syscall_profile": "backend/seccomp_profile.json",
    "seccomp_profile": "backend/seccomp_profile.json",
    "tier_0_picoclaw_sub_millisecond_policy_cache": "backend/tier0_cache.py",
    "tier0_cache": "backend/tier0_cache.py",
    "picoclaw_companion_go_runtime_cache": "backend/picoclaw_cache.go",
    "picoclaw_cache": "backend/picoclaw_cache.go",
    "tier_1_system_1_typed_risk_classifier": "backend/tier1_jev.py",
    "tier1_jev": "backend/tier1_jev.py",
    "tier_2_nebius_dual_nemotron_policy_synthesizer": "backend/tier2_nebius.py",
    "tier2_nebius": "backend/tier2_nebius.py",
    "sse_fan_out_broadcaster_and_telemetry_hub": "backend/sse_broadcaster.py",
    "sse_broadcaster": "backend/sse_broadcaster.py",
    "fastapi_sovereign_governance_gateway": "backend/main.py",
    "main": "backend/main.py",
    "backend_package_initializer": "backend/__init__.py",
    "__init__": "backend/__init__.py",

    # Root CLI, Contract, Config & Benchmark Runner
    "parole_machine_contract_json": "contract.json",
    "contract": "contract.json",
    "pc_companion_terminal_cli": "parole_cli.py",
    "parole_cli": "parole_cli.py",
    "1000_trace_empirical_red_team_benchmark_runner": "benchmarks/run_benchmark.py",
    "run_benchmark": "benchmarks/run_benchmark.py",
    "python_backend_dependencies": "requirements.txt",
    "requirements": "requirements.txt",
    "machine_readable_environment_profile": "ENV_PROFILE.json",
    "env_profile": "ENV_PROFILE.json",
    "parole_downloaded_files_sorter_and_repo_organizer": "setup_parole_workspace.py",
    "setup_parole_workspace": "setup_parole_workspace.py",

    # Independent Unit Test Suite (Wave 0b)
    "independent_unit_tests_for_module_0a_schemas": "tests/test_schemas.py",
    "test_schemas": "tests/test_schemas.py",
    "independent_unit_tests_for_module_1_kernel_guard": "tests/test_kernel_guard.py",
    "test_kernel_guard": "tests/test_kernel_guard.py",
    "independent_unit_tests_for_module_2_tier_0_cache": "tests/test_tier0_cache.py",
    "test_tier0_cache": "tests/test_tier0_cache.py",
    "independent_unit_tests_for_module_3_tier_1_jev": "tests/test_tier1_jev.py",
    "test_tier1_jev": "tests/test_tier1_jev.py",
    "independent_unit_tests_for_module_4_tier_2_nebius": "tests/test_tier2_nebius.py",
    "test_tier2_nebius": "tests/test_tier2_nebius.py",
    "independent_unit_tests_for_module_5_sse_broadcaster": "tests/test_sse_broadcaster.py",
    "test_sse_broadcaster": "tests/test_sse_broadcaster.py",
    "independent_unit_and_chaos_tests_for_module_6_fastapi_gateway": "tests/test_fastapi_gateway.py",
    "test_fastapi_gateway": "tests/test_fastapi_gateway.py",
    "independent_unit_tests_for_module_7_cli_and_benchmark": "tests/test_cli_and_benchmark.py",
    "test_cli_and_benchmark": "tests/test_cli_and_benchmark.py",

    # Enforcement & Doctor Scripts
    "git_worktree_file_lock_enforcement_script": "scripts/check_file_lock.py",
    "check_file_lock": "scripts/check_file_lock.py",
    "wave_0_contract_sha_256_lock_script": "scripts/contract_lock.py",
    "contract_lock": "scripts/contract_lock.py",
    "anti_slop_and_evidence_tag_documentation_linter": "scripts/prd_lint.py",
    "prd_lint": "scripts/prd_lint.py",
    "non_destructive_staged_code_applier_with_rollback": "scripts/apply_incoming.py",
    "apply_incoming": "scripts/apply_incoming.py",
    "phase_2_ast_doctor_and_same_folder_deduplicator": "scripts/phase2_dedup_and_doctor.py",
    "phase2_dedup_and_doctor": "scripts/phase2_dedup_and_doctor.py",
    "phase2_dedup_and_doctor_template": "scripts/phase2_dedup_and_doctor.py",
}

GITIGNORE_CONTENT = """.venv/
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


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def normalize_stem(filename: str) -> str:
    """Normalize a downloaded filename into a clean lowercase stem without (1) or extensions."""
    name = filename.strip()
    # Strip browser duplicate suffixes like ` (1)`, ` (2)`, `_1` before extension
    name = re.sub(r"\s*\(\d+\)(?=\.[^.]+$|$)", "", name)
    # Strip known extensions (including double extensions like `.go.txt` or `.py.txt`)
    for ext in (".py", ".md", ".json", ".go", ".sh", ".txt", ".yaml", ".yml"):
        if name.lower().endswith(ext):
            name = name[: -len(ext)]
    for ext in (".py", ".md", ".json", ".go", ".sh", ".txt"):
        if name.lower().endswith(ext):
            name = name[: -len(ext)]
    # Normalize non-alphanumeric characters to underscores
    stem = re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")
    return stem


def clean_code_fences_if_needed(raw_bytes: bytes, dest_rel: str) -> bytes:
    """Strip outer ```python / ```go / ```json markdown fences if present in non-Markdown files."""
    if dest_rel.endswith(".md") or dest_rel.endswith(".pdf"):
        return raw_bytes
    try:
        text = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes

    lines = text.strip().splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        return ("\n".join(lines) + "\n").encode("utf-8")
    return raw_bytes


def detect_desktop_dir() -> Path:
    """Resolve Windows/macOS/Linux Desktop folder reliably (including OneDrive Desktop)."""
    home = Path.home()
    if sys.platform.startswith("win"):
        try:
            from ctypes import windll, wintypes

            class GUID(ctypes.Structure):
                _fields_ = [
                    ("Data1", wintypes.DWORD),
                    ("Data2", wintypes.WORD),
                    ("Data3", wintypes.WORD),
                    ("Data4", ctypes.c_ubyte * 8),
                ]

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

        for od in sorted(home.glob("OneDrive*")):
            cand = od / "Desktop"
            if cand.is_dir():
                return cand

    for cand in [home / "Desktop", home]:
        if cand.is_dir():
            return cand
    return Path.cwd()


def resolve_destination_by_content(fpath: Path) -> str | None:
    """Fallback detector that inspects the first 15 lines of a file if its filename was truncated."""
    if fpath.suffix.lower() in (".pdf", ".png", ".jpg", ".exe", ".zip"):
        return None
    try:
        head = fpath.read_text(encoding="utf-8", errors="ignore")[:1200]
    except OSError:
        return None

    content_markers: list[tuple[str, str]] = [
        ("PAROLE Wave 0a Schema Contract (backend/schemas.py)", "backend/schemas.py"),
        ("PAROLE Module 1: Out-of-Process Kernel & Provenance Taint Gate", "backend/kernel_guard.py"),
        ("PAROLE Module 2: Tier 0 PicoClaw In-Memory Policy Cache", "backend/tier0_cache.py"),
        ("PAROLE Module 2 Companion: PicoClaw Sub-Millisecond Go Policy Cache", "backend/picoclaw_cache.go"),
        ("PAROLE Module 3: Tier 1 System-1 Typed Risk Classifier", "backend/tier1_jev.py"),
        ("PAROLE Module 4: Tier 2 Nebius Dual-Nemotron Policy Synthesis", "backend/tier2_nebius.py"),
        ("PAROLE Module 5: Asynchronous SSE Fan-Out Hub", "backend/sse_broadcaster.py"),
        ("PAROLE Module 6: FastAPI Sovereign Gateway", "backend/main.py"),
        ("PAROLE Module 7a: Lightweight PC Companion CLI", "parole_cli.py"),
        ("PAROLE Module 7b: 1,000-Trace Empirical Red-Team", "benchmarks/run_benchmark.py"),
        ("PAROLE Sovereign Backend Package", "backend/__init__.py"),
        ("NemoClaw Out-of-Process Linux Landlock", "backend/nemoclaw_sandbox.sh"),
        ("SCMP_ACT_ERRNO", "backend/seccomp_profile.json"),
        ("Independent Unit Tests for Module 0a: backend/schemas.py", "tests/test_schemas.py"),
        ("Independent Unit Tests for Module 1: backend/kernel_guard.py", "tests/test_kernel_guard.py"),
        ("Independent Unit Tests for Module 2: backend/tier0_cache.py", "tests/test_tier0_cache.py"),
        ("Independent Unit Tests for Module 3: backend/tier1_jev.py", "tests/test_tier1_jev.py"),
        ("Independent Unit Tests for Module 4: backend/tier2_nebius.py", "tests/test_tier2_nebius.py"),
        ("Independent Unit Tests for Module 5: backend/sse_broadcaster.py", "tests/test_sse_broadcaster.py"),
        ("Independent Unit & 10-Vector Chaos Tests for Module 6", "tests/test_fastapi_gateway.py"),
        ("Independent Unit Tests for Module 7: parole_cli.py", "tests/test_cli_and_benchmark.py"),
    ]
    for marker, rel in content_markers:
        if marker in head:
            return rel
    return None


def resolve_relative_destination(fpath: Path, since_hours: float) -> str | None:
    """Map a downloaded file in Downloads/Desktop to its target path inside `parole-1`."""
    stem = normalize_stem(fpath.name)
    if stem in STEM_TO_REPO_PATH:
        return STEM_TO_REPO_PATH[stem]

    # Prefix match for long Windows filenames that got truncated
    for known_stem, target_rel in STEM_TO_REPO_PATH.items():
        if len(stem) >= 18 and (known_stem.startswith(stem) or stem.startswith(known_stem)):
            return target_rel

    # Content-based fallback for recently downloaded text/code files
    try:
        if fpath.stat().st_mtime >= (time.time() - since_hours * 3600.0):
            by_content = resolve_destination_by_content(fpath)
            if by_content:
                return by_content
            if fpath.suffix.lower() == ".pdf" and any(
                k in stem for k in ("parole", "dossier", "nebius", "download")
            ):
                return f"documentation/dossiers/{fpath.name}"
    except OSError:
        pass

    return None


def collect_downloaded_files(target_root: Path, since_hours: float, extra_source: str = "") -> dict[str, Path]:
    """Scan Downloads, Desktop, and current directory for all PAROLE artifacts."""
    home = Path.home()
    search_dirs: list[Path] = []
    if extra_source:
        search_dirs.append(Path(extra_source))
    # Script's own folder first (e.g. if script itself is sitting inside Downloads)
    try:
        search_dirs.append(Path(__file__).resolve().parent)
    except NameError:
        pass
    search_dirs.extend([Path.cwd(), home / "Downloads", home / "Desktop"])
    for od in sorted(home.glob("OneDrive*")):
        search_dirs.extend([od / "Downloads", od / "Desktop"])

    best_by_dest: dict[str, Path] = {}
    seen_folders: set[Path] = set()

    for folder in search_dirs:
        if not folder.is_dir():
            continue
        rf = folder.resolve()
        if rf in seen_folders or rf == target_root.resolve():
            continue
        seen_folders.add(rf)

        for item in sorted(rf.iterdir()):
            if not item.is_file():
                continue
            rel_dest = resolve_relative_destination(item, since_hours)
            if rel_dest is None:
                continue
            prev = best_by_dest.get(rel_dest)
            try:
                if prev is None or item.stat().st_mtime >= prev.stat().st_mtime:
                    best_by_dest[rel_dest] = item
            except OSError:
                continue

    return best_by_dest


def write_sorted_file(src: Path, dst: Path, rel_dest: str, dry_run: bool, log_lines: list[str]) -> str:
    """Copy `src` to `dst`, stripping accidental markdown fences from code/json files."""
    raw_bytes = src.read_bytes()
    cleaned_bytes = clean_code_fences_if_needed(raw_bytes, rel_dest)

    if dst.exists():
        existing_bytes = dst.read_bytes()
        if sha256_bytes(existing_bytes) == sha256_bytes(cleaned_bytes):
            msg = f"  [SKIP-IDENTICAL] {src.name:48s} -> {rel_dest}"
            print(msg)
            log_lines.append(msg)
            return "identical"

    tag = "DRY-SORT" if dry_run else "SORTED  "
    msg = f"  [{tag}]       {src.name:48s} -> {rel_dest}"
    print(msg)
    log_lines.append(msg)
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(cleaned_bytes)
    return "copied"


def main() -> None:
    ap = argparse.ArgumentParser(description="Sort downloaded PAROLE chat files into Desktop/parole-1.")
    ap.add_argument("--slug", default="parole-1", help="Target folder name on Desktop (default: parole-1)")
    ap.add_argument("--target", default="", help="Custom target directory path (default: Desktop/parole-1)")
    ap.add_argument("--source", default="", help="Optional extra source directory to scan")
    ap.add_argument("--since-hours", type=float, default=96.0, help="Lookback hours for downloads (default: 96)")
    ap.add_argument("--dry-run", action="store_true", help="Preview only without writing files")
    ap.add_argument("--apply", action="store_true", help="Write files to disk (enabled by default unless --dry-run)")
    args = ap.parse_args()

    dry_run = bool(args.dry_run)
    target_root = Path(args.target).resolve() if args.target else (detect_desktop_dir() / args.slug)
    log_lines: list[str] = []

    banner = (
        f"========================================================================================\n"
        f"PAROLE-1 REPOSITORY SORTER\n"
        f"Target Folder : {target_root}\n"
        f"Mode          : {'DRY-RUN (Preview Only)' if dry_run else 'ACTIVE SORT (Writing to Desktop/parole-1)'}\n"
        f"========================================================================================"
    )
    print(banner)
    log_lines.append(banner)

    subdirs = [
        "documentation/prds",
        "documentation/agents",
        "documentation/skills",
        "documentation/dossiers",
        "backend",
        "benchmarks",
        "tests/oracles",
        "frontend/public",
        "requests",
        "scripts",
    ]
    for sd in subdirs:
        p = target_root / sd
        if not dry_run:
            p.mkdir(parents=True, exist_ok=True)

    matched_files = collect_downloaded_files(target_root, args.since_hours, args.source)
    stats = {"copied": 0, "identical": 0}

    for rel_dest, src_path in sorted(matched_files.items()):
        dst_path = target_root / rel_dest
        res = write_sorted_file(src_path, dst_path, rel_dest, dry_run, log_lines)
        stats[res] = stats.get(res, 0) + 1

    print("----------------------------------------------------------------------------------------")
    print(
        f"[summary] Matched & sorted: {len(matched_files)} file(s) into {target_root} "
        f"(Written: {stats['copied']}, Already identical: {stats['identical']})"
    )

    if not dry_run:
        gitignore_path = target_root / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text(GITIGNORE_CONTENT, encoding="utf-8")

        # 1. Generate contract.json & contract.lock if schemas.py and contract_lock.py are in place
        if (target_root / "backend/schemas.py").is_file():
            subprocess.run([sys.executable, "backend/schemas.py"], cwd=target_root, check=False)
        if (target_root / "scripts/contract_lock.py").is_file() and (target_root / "contract.json").is_file():
            subprocess.run([sys.executable, "scripts/contract_lock.py", "write"], cwd=target_root, check=False)

        # 2. Run benchmark suite to auto-generate results.json, telemetry_fallback_v2.4.json & BENCHMARK_REPORT_V2.4.md
        if (target_root / "benchmarks/run_benchmark.py").is_file():
            print("[post-sort] Running 1,000-trace benchmark to generate results.json & telemetry_fallback_v2.4.json...")
            subprocess.run(
                [sys.executable, "benchmarks/run_benchmark.py", "--mode", "in_process"],
                cwd=target_root,
                check=False,
            )

        # 3. Initialize git repository baseline
        if not (target_root / ".git").exists():
            subprocess.run(["git", "init"], cwd=target_root, check=False)
            subprocess.run(["git", "add", "-A"], cwd=target_root, check=False)
            subprocess.run(["git", "commit", "-m", "baseline: sorted PAROLE-1 repository"], cwd=target_root, check=False)

        (target_root / "setup.log").write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        print("========================================================================================")
        print(f"[SUCCESS] Your complete PAROLE repository is ready at: {target_root}")
        print("========================================================================================")


if __name__ == "__main__":
    main()