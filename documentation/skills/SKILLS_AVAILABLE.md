# Verified POWERHOUSE Skills Inventory (`SKILLS_AVAILABLE.md`)

**Repository Source**: `https://github.com/SOHAM-RAJHANS/POWERHOUSE` [SOURCE: Dossier_00 p1]
**Active Department**: Role 1 — Backend Product Layer, Kernel Governance, PC CLI & Nebius Orchestration [SOURCE: Dossier_01 p1]

## 1. Verified Slash Skills Present for Backend Tracks

| Skill Slash Name | One-Line Engineering Purpose | Assigned Backend Modules | Offline Inline Fallback Pack |
| :--- | :--- | :--- | :--- |
| `/atlas-contract` | Locks Pydantic v2 schemas, JSON Schema export, and cross-role TypeScript/Python field parity | `PRD_00`, `PRD_06`, `PRD_07` | `RP-CONTRACT`, `RP-FASTAPI` |
| `/super-mega-backend` | High-concurrency FastAPI architecture, non-blocking async I/O, and sub-millisecond hot-path design | `PRD_00`, `PRD_02`, `PRD_05`, `PRD_06` | `RP-HOTPATH`, `RP-FASTAPI` |
| `/mega-system-architecture` | Out-of-process boundary isolation, 3-tier routing state machines, and circuit-breaker design | `PRD_02`, `PRD_03`, `PRD_04`, `PRD_05` | `RP-HOTPATH`, `RP-CONTRACT` |
| `/aegisops-ai` | Linux kernel sandboxing (`Landlock`, `seccomp-bpf`), path/IP canonicalization, and taint tracking | `PRD_01`, `PRD_03` | `RP-SECURITY`, `RP-HOTPATH` |
| `/adversarial-reviewer` | MITRE ATT&CK and OWASP LLM01 bypass auditing, obfuscated pipe decoding, and chaos vector testing | `PRD_01`, `PRD_04`, `PRD_06`, `PRD_07` | `RP-ADVERSARIAL`, `RP-SECURITY` |
| `/super-mega-hackathon` | Walking-skeleton orchestration, deterministic demo replay seeding, and benchmark telemetry export | `PRD_06`, `PRD_07` | `RP-CONTRACT`, `RP-ADVERSARIAL` |

## 2. Prompt Binding Rules

1. Every prompt in `documentation/agents/AGENTS_00..07.md` binds at most 4 verified slash skills from the table above.
2. Every prompt embeds its paired Inline Rule Packs (`RP-CONTRACT`, `RP-HOTPATH`, `RP-SECURITY`, `RP-ADVERSARIAL`, `RP-FASTAPI`) directly under `RULES:` so any coding agent operates deterministically even when offline.