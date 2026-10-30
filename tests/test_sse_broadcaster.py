"""Independent Unit Tests for Module 5: backend/sse_broadcaster.py (Covers PRD_05)."""
from __future__ import annotations

import asyncio
from backend.schemas import MetricsSummaryResponse
from backend.sse_broadcaster import (
    broadcast_event,
    get_metrics_summary,
    reset_broadcaster_state,
    subscribe,
    unsubscribe,
)


def test_sse_n1_fifo_delivery() -> None:
    """Covers PRD_05 Sec 3.2: subscriber receives broadcast events in FIFO order."""
    async def _run() -> None:
        reset_broadcaster_state()
        sub_id, q = await subscribe()
        seq = await broadcast_event("evaluate", {"cmd": "git status"})
        assert seq == 1
        item = q.get_nowait()
        assert item["id"] == 1
        assert item["event"] == "evaluate"
        unsubscribe(sub_id)

    asyncio.run(_run())


def test_sse_n2_initial_connect_flushes_last_10_events() -> None:
    """Covers PRD_05 Sec 3.1: new subscriber receives last 10 events from replay buffer."""
    async def _run() -> None:
        reset_broadcaster_state()
        for i in range(15):
            await broadcast_event("evaluate", {"idx": i + 1})
        sub_id, q = await subscribe()
        assert q.qsize() == 10
        first = q.get_nowait()
        assert first["id"] == 6
        unsubscribe(sub_id)

    asyncio.run(_run())


def test_sse_n3_last_event_id_replays_missed_only() -> None:
    """Covers PRD_05 Sec 3.2: Last-Event-ID replays only events with id > last_event_id."""
    async def _run() -> None:
        reset_broadcaster_state()
        for i in range(15):
            await broadcast_event("evaluate", {"idx": i + 1})
        sub_id, q = await subscribe(last_event_id=12)
        ids = []
        while not q.empty():
            ids.append(q.get_nowait()["id"])
        assert ids == [13, 14, 15]
        unsubscribe(sub_id)

    asyncio.run(_run())


def test_sse_a1_bounded_queue_oldest_drop_policy() -> None:
    """Covers PRD_05 Sec 3.2: queue overflow (>256) drops oldest and emits 'dropped' notification."""
    async def _run() -> None:
        reset_broadcaster_state()
        sub_id, q = await subscribe()
        for i in range(300):
            await broadcast_event("evaluate", {"idx": i})
        assert q.qsize() <= 256
        events = []
        while not q.empty():
            events.append(q.get_nowait())
        assert any(e["event"] == "dropped" for e in events)
        assert events[-1]["data"]["idx"] == 299
        unsubscribe(sub_id)

    asyncio.run(_run())


def test_sse_a2_concurrent_subscribe_unsubscribe_no_runtime_error() -> None:
    """Covers PRD_05 Sec 3.3: 50 concurrent subscribe/unsubscribe tasks during broadcast."""
    async def _run() -> None:
        reset_broadcaster_state()

        async def _churn(idx: int) -> None:
            sid, _ = await subscribe()
            await broadcast_event("evaluate", {"worker": idx})
            unsubscribe(sid)

        await asyncio.gather(*[_churn(i) for i in range(50)])

    asyncio.run(_run())


def test_sse_c1_metrics_summary_validates_against_schema() -> None:
    """Covers PRD_05 Sec 3.2: get_metrics_summary validates against MetricsSummaryResponse."""
    summary = get_metrics_summary(active_tier0_rules=["git status"], capability="live")
    model = MetricsSummaryResponse(**summary)
    assert model.zero_day_block_rate_pct == 100.0