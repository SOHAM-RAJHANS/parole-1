# AGENTS_05: `backend/sse_broadcaster.py`

**Companion PRD**: `documentation/prds/PRD_05_sse_broadcaster.md`
**Lane / worktree**: `lane1e` / `../wt/lane1e`   **Audit required**: yes

## 1. Execution Blueprint

```yaml
goal: Implement backend/sse_broadcaster.py so all gates exit 0.
allowlist:
  - "backend/sse_broadcaster.py"
  - "requests/lane1e.md"
base_tag: wave0-locked
budget: p95 <= 1.0 ms enqueue target
gates:
  - python backend/sse_broadcaster.py
  - pytest -q tests/test_sse_broadcaster.py
  - python scripts/contract_lock.py check
  - python scripts/check_file_lock.py --since wave0-locked --allow "backend/sse_broadcaster.py" --allow "requests/lane1e.md"
```

## 2. Prompts

### Builder (Paste as is into OpenCode inside `../wt/lane1e`)

```text
/super-mega-backend /mega-system-architecture
ROLE: Builder. FILE LOCK: write ONLY backend/sse_broadcaster.py (and requests/lane1e.md for questions). Touching anything else is a failure.
READ, in this order and nothing else:
  1. documentation/00_MASTER_PRD.md sections 3 and 4
  2. documentation/prds/PRD_05_sse_broadcaster.md
  3. tests/test_sse_broadcaster.py
RULES:
RP-CONTRACT
- Names, argument names, types, dict keys and enum values match PRD section 4 and contract.json character for character.
- get_metrics_summary() output must validate against MetricsSummaryResponse in backend/schemas.py.
RP-FASTAPI
- Use per-subscriber asyncio.Queue(maxsize=256) and collections.deque(maxlen=25) for replay.
- Clone subscriber dict items via list(_subscribers.items()) before iterating in broadcast_event so concurrent tab disconnects never raise RuntimeError.
- When a subscriber queue is full, pop the oldest item and enqueue a {"type": "dropped", "count": n} notification before enqueuing the newest event.
DONE WHEN every gate in documentation/agents/AGENTS_05_sse_broadcaster.md section 1 exits 0. Paste each command and its exit code in your reply.
IF BLOCKED: do not guess names, keys or numbers. Append a QUESTION or NEEDS_DEP line to requests/lane1e.md and stop.
```

### Auditor (Paste into Grok Code after Builder gates pass)

```text
/adversarial-reviewer /super-mega-backend
ROLE: Auditor. Do not rewrite the module unless a high-severity finding exists.
INPUT BELOW: backend/sse_broadcaster.py, PRD_05 section 3, and tests/test_sse_broadcaster.py.
TASK: Audit for race conditions on concurrent subscribe/unsubscribe during broadcast, memory leaks from abandoned subscriber queues, off-by-one bugs in Last-Event-ID replay, and schema mismatches in get_metrics_summary().
Maximum 5 findings, highest severity first. If a high finding exists, ALSO output the corrected file as:
=== FILE: backend/sse_broadcaster.py ===
<complete file>
=== END ===
Keep every public signature unchanged.
RULES: RP-ADVERSARIAL, RP-CONTRACT, RP-FASTAPI
```