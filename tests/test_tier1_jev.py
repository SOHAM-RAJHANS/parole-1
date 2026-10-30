"""Independent Unit Tests for Module 3: backend/tier1_jev.py (Covers PRD_03)."""
from __future__ import annotations

from backend.tier1_jev import evaluate_tier1_jev


def test_t1_n1_safe_file_cat_allowed() -> None:
    """Covers PRD_03 Sec 3.2: safe workspace file inspection scores < 20 and is ALLOWED."""
    res = evaluate_tier1_jev("cat src/config.ts", "src/config.ts", "TRUSTED_USER", False)
    assert res["allow"] is True
    assert res["blast_radius_score"] < 20
    assert res["injection_risk_score"] < 20
    assert res["tier_resolved"] == "TIER_1"


def test_t1_n2_safe_grep_allowed() -> None:
    """Covers PRD_03 Sec 3.2: grep on local src directory is ALLOWED in Tier 1."""
    res = evaluate_tier1_jev('grep -rn "useEffect" src/', "src/", "TRUSTED_USER", False)
    assert res["allow"] is True
    assert res["decision"] == "ALLOWED"


def test_t1_n3_uncached_internal_api_escalates_to_tier2() -> None:
    """Covers PRD_03 Sec 3.2: unfamiliar internal subnet API call escalates to Tier 2."""
    res = evaluate_tier1_jev("curl -s https://10.0.4.12/api/v1/users", "10.0.4.12/api/v1/users", "TRUSTED_USER", False)
    assert res["allow"] is False
    assert res["escalate_tier2"] is True
    assert res["blast_radius_score"] >= 20


def test_t1_a1_tainted_provenance_never_allowed_in_tier1() -> None:
    """Covers PRD_03 Sec 3.3: web/repo_payload taint scores injection_risk >= 50."""
    res = evaluate_tier1_jev("cat src/config.ts", "src/config.ts", "web/repo_payload", True)
    assert res["allow"] is False
    assert res["injection_risk_score"] >= 50


def test_t1_a2_destructive_rm_rf_escalates() -> None:
    """Covers PRD_03 Sec 3.2: rm -rf scores high blast radius and is not auto-allowed."""
    res = evaluate_tier1_jev("rm -rf ./dist", "./dist", "TRUSTED_USER", False)
    assert res["allow"] is False
    assert res["blast_radius_score"] >= 70


def test_t1_a3_inline_python_exec_escalates() -> None:
    """Covers PRD_03 Sec 3.2: python -c inline code execution scores >= 50."""
    res = evaluate_tier1_jev("python -c 'import os; os.system(\"id\")'", "", "TRUSTED_USER", False)
    assert res["allow"] is False
    assert res["injection_risk_score"] >= 50


def test_t1_a4_empty_command_rejected() -> None:
    """Covers PRD_03 Sec 3.4: empty command returns allow=False and score 100."""
    res = evaluate_tier1_jev("", "", "TRUSTED_USER", False)
    assert res["allow"] is False
    assert res["blast_radius_score"] == 100


def test_t1_a5_privileged_docker_escalates() -> None:
    """Covers PRD_03 Sec 3.2: docker run --privileged scores high blast radius."""
    res = evaluate_tier1_jev("docker run --privileged alpine", "", "TRUSTED_USER", False)
    assert res["allow"] is False
    assert res["blast_radius_score"] >= 80