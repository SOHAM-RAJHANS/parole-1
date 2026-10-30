# PRD_05: `backend/sse_broadcaster.py`

**Target File(s)**: `backend/sse_broadcaster.py`
**Lane / role**: `lane1e` / Builder + Auditor   **Audit required**: yes
**Design reference**: Stripe Webhook Fan-Out Broadcaster & Reference 11.1 SSE Spec [SOURCE: Dossier_01 p3]

## 1. Purpose and Role

Provides the asynchronous Server-Sent Events (SSE) fan-out hub, 25-event replay deque, preliminary Tier 2 state notifier, and live session telemetry aggregator for `GET /v1/policy/stream` and `GET /v1/metrics/summary`. Guarantees that multiple concurrent browser tabs and CLI listeners receive real-time events without throwing `RuntimeError: Set changed size during iteration` on tab refresh, honours `Last-Event-ID` or flushes the last 10 events on initial connect, and enforces bounded per-subscriber memory (`asyncio.Queue(maxsize=256)`) with explicit oldest-drop notification.

## 2. Bound Skills (Verified in `SKILLS_AVAILABLE.md`)

| Slash | Rule Pack if Skill is Missing | Why Here |
| :--- | :--- | :--- |
| `/super-mega-backend` | `RP-FASTAPI`, `RP-HOTPATH` | Safe snapshot iteration over subscriber queues and `finally:` cleanup on disconnect |
| `/mega-system-architecture` | `RP-CONTRACT` | Bounded queue backpressure (`maxsize=256`), `collections.deque(maxlen=25)` replay, and live KPI aggregation |

## 3. Specification

1. **Data and Constants**:
   - `REPLAY_BUFFER_MAXLEN: int = 25` [SOURCE: Dossier_01 p3]
   - `INITIAL_FLUSH_COUNT: int = 10` [SOURCE: Dossier_01 p3]
   - `SUBSCRIBER_QUEUE_MAXSIZE: int = 256`
   - `HEARTBEAT_INTERVAL_SEC: float = 10.0` [SOURCE: Dossier_01 p3]
   - `CANONICAL_COLLAPSE_CURVE: list[dict]` containing the 6 canonical time points (`0m: 100->100`, `2m: 98->48`, `5m: 97->19`, `10m: 96->8.4`, `15m: 95->4.9`, `20m: 95->3.8`) [SOURCE: Dossier_01 p5].

2. **Functions**:
   - `async def subscribe(last_event_id: int | None = None) -> tuple[int, asyncio.Queue]:` creates a new subscriber ID and `asyncio.Queue(maxsize=256)`, pre-populates the queue with replay events (either events with `id > last_event_id` if `last_event_id` is provided, or the last `10` events from `_replay_deque`), registers the subscriber in `_subscribers`, and returns `(sub_id, queue)`.
   - `def unsubscribe(sub_id: int) -> None:` removes `sub_id` from `_subscribers` safely using `.pop(sub_id, None)`.
   - `async def broadcast_event(event_type: str, payload: dict) -> int:` increments the monotonic integer `_event_seq`, wraps `{"id": seq, "event": event_type, "data": payload}`, appends to `_replay_deque`, and iterates over a cloned snapshot `list(_subscribers.items())`. If a subscriber's queue is full (`queue.full()`), pops the oldest item with `queue.get_nowait()`, increments that subscriber's drop counter, and enqueues `{"id": seq, "event": "dropped", "data": {"type": "dropped", "count": drop_count}}` before enqueuing the new event.
   - `def get_replay_events(limit: int = 10, since_id: int | None = None) -> list[dict]:` returns a list of buffered SSE event dicts from `_replay_deque`.
   - `def record_metrics(event: dict) -> None:` updates live session counters (`tier_0`, `tier_1`, `tier_2`, `kernel_hard_deny`, latencies, and costs) from each evaluated `AgentActionEvent`.
   - `def get_metrics_summary(active_tier0_rules: list[str] | None = None, capability: str = "live") -> dict:` returns a dictionary matching `MetricsSummaryResponse` in `backend/schemas.py`, reading verified benchmark metrics from `results.json` if present on disk or falling back to canonical baseline counters annotated with `capability`.
   - `def format_sse_frame(event_id: int, event_type: str, data: dict) -> str:` formats a standard SSE wire frame (`id: <id>\nevent: <type>\ndata: <json>\n\n`).

3. **Edge Cases**:
   - 50 concurrent clients subscribing and disconnecting mid-stream must never raise `RuntimeError: dictionary changed size during iteration`.
   - Slow consumer whose queue reaches `256` items must drop the oldest item and emit a `"dropped"` event rather than blocking the event loop or growing memory unboundedly.
   - Reconnecting client sending `Last-Event-ID: 5` receives only events with `id > 5`.

4. **Failure Behaviour**:
   - Never blocks the asyncio event loop; malformed subscriber removal is a no-op.

5. **Budget**:
   - `broadcast_event` and `record_metrics` p95 `<= 1.0 ms` [TARGET].

## 4. Invariants

- Matches `00_MASTER_PRD.md` Sections 3 and 4.
- Writes only `backend/sse_broadcaster.py` (plus `requests/lane1e.md`).
- Uses only Python standard library (`asyncio`, `collections`, `json`, `pathlib`, `time`).

## 5. Gates

```bash
python backend/sse_broadcaster.py
pytest -q tests/test_sse_broadcaster.py
python scripts/contract_lock.py check
python scripts/check_file_lock.py --since wave0-locked --allow "backend/sse_broadcaster.py" --allow "requests/lane1e.md"
```