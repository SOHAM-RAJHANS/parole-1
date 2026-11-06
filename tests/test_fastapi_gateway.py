"""Independent Unit & 10-Vector Chaos Tests for Module 6: backend/main.py (Covers PRD_06)."""
from __future__ import annotations

import asyncio
from fastapi.testclient import TestClient

from backend import tier0_cache
from backend.main import app

client = TestClient(app)


def test_gw_n1_evaluate_tier0_happy_path() -> None:
    """Covers PRD_06 Sec 3.2: POST /v1/policy/evaluate resolves git status in TIER_0."""
    tier0_cache.reset_promoted_rules()
    resp = client.post("/v1/policy/evaluate", json={"command": "git status"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["tier_resolved"] == "TIER_0"
    assert data["decision"] == "ALLOWED"


def test_gw_n2_approve_diff_and_followup_tier0_hit() -> None:
    """Covers PRD_06 Sec 3.2: POST /v1/policy/approve-diff promotes rule and resolves follow-up in TIER_0."""
    tier0_cache.reset_promoted_rules()
    resp = client.post(
        "/v1/policy/approve-diff",
        json={"scoped_rule": "+ PERMIT 10.0.4.0/24 ON /api/v1/*", "trigger_followup": True},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["promoted"] is True
    assert body["followup_event"]["tier_resolved"] == "TIER_0"
    assert body["followup_event"]["decision"] == "ALLOWED"
    tier0_cache.reset_promoted_rules()


def test_gw_n3_metrics_summary_endpoint() -> None:
    """Covers PRD_06 Sec 3.2: GET /v1/metrics/summary returns canonical KPIs."""
    resp = client.get("/v1/metrics/summary")
    assert resp.status_code == 200
    body = resp.json()
    assert body["zero_day_block_rate_pct"] == 100.0
    assert len(body["escalation_collapse_curve"]) == 6


def test_gw_n4_root_and_render_healthcheck() -> None:
    for path in ("/", "/healthz"):
        resp = client.get(path)
        assert resp.status_code == 200
        assert resp.json() == {"status": "ok", "service": "parole-backend"}


def test_gw_n5_frontend_origin_cors(monkeypatch) -> None:
    from backend.main import _get_allowed_origins

    monkeypatch.setenv("FRONTEND_ORIGIN", "https://parole.example/, https://preview.example")
    assert _get_allowed_origins() == ["https://parole.example", "https://preview.example"]


def test_gw_a1_10_chaos_vectors_and_422_no_echo() -> None:
    """Covers PRD_06 Sec 3.3 & Reference 11.3: 10 chaos vectors never 500 or echo payload."""
    secret_marker = "SUPER_SECRET_MARKER_DO_NOT_ECHO_999"

    # 1. Empty body
    r1 = client.post("/v1/policy/evaluate", content=b"")
    assert r1.status_code == 422

    # 2. Wrong content type
    r2 = client.post("/v1/policy/evaluate", content=b"command=ls", headers={"Content-Type": "text/plain"})
    assert r2.status_code == 422

    # 3. Wrong field types
    r3 = client.post("/v1/policy/evaluate", json={"command": 12345, "taint_flag": "not_a_bool"})
    assert r3.status_code == 422

    # 4. Missing required field
    r4 = client.post("/v1/policy/evaluate", json={"workstation_node": "PC"})
    assert r4.status_code == 422

    # 5. 20,000-char string (must not echo secret_marker in 422 response)
    huge_str = secret_marker + ("A" * 20000)
    r5 = client.post("/v1/policy/evaluate", json={"command": huge_str})
    assert r5.status_code == 422
    assert secret_marker not in r5.text
    assert "field_paths" in r5.json()

    # 6. Extra unknown field
    r6 = client.post("/v1/policy/evaluate", json={"command": "git status", "evil": secret_marker})
    assert r6.status_code == 422
    assert secret_marker not in r6.text

    # 7. Unicode combining marks, RTL, zero-width space, emoji
    r7 = client.post("/v1/policy/evaluate", json={"command": "git\u200b status"})
    assert r7.status_code == 200

    # 8. Invalid rule syntax on approve-diff
    r8 = client.post("/v1/policy/approve-diff", json={"scoped_rule": "GRANT ALL TO *:*"})
    assert r8.status_code == 400

    # 9. 50 concurrent evaluations
    for _ in range(50):
        rc = client.post("/v1/policy/evaluate", json={"command": "git status"})
        assert rc.status_code == 200

    # 10. Health check after chaos suite remains 200 OK
    r10 = client.get("/health")
    assert r10.status_code == 200 and r10.json()["status"] == "ok"


def test_gw_a2_demo_route_guarded_by_demo_mode(monkeypatch) -> None:
    """Covers PRD_06 Sec 3.2: POST /v1/demo/run-180s returns 404 when DEMO_MODE=0."""
    monkeypatch.setenv("DEMO_MODE", "0")
    resp = client.post("/v1/demo/run-180s")
    assert resp.status_code == 404

    monkeypatch.setenv("DEMO_MODE", "1")
    resp_ok = client.post("/v1/demo/run-180s")
    assert resp_ok.status_code == 200
    assert resp_ok.json()["events_emitted"] == 7