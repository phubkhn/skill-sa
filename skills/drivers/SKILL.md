---
name: drivers
description: Turn constraints and stakeholder concerns into measurable quality-attribute scenarios (performance, availability, security, modifiability...). Use when the user asks for NFRs, quality attributes, SLOs as requirements, or architecture drivers.
allowed-tools: Read, Grep, Glob
---

# SA — Turn constraints and concerns into measurable quality-attribute scenarios

| | |
|---|---|
| Journey step | 2 — Drivers |
| Produces | 00-context/architecture-drivers.md |
| Inputs | 00-context/sa-intent.md |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/03-drivers-nfr-standard.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/03-drivers-nfr-standard.md` — self-assess item by item in P9.

## When to use

- "what are the NFRs", "define the SLOs", "what quality attributes matter here"
- "how available / how fast does this need to be" — **setting** the target
- Whenever G1 fails for want of a measurable scenario

## When not to use

| Request | Use instead |
|---|---|
| "what happens when X fails" | `sa:resilience` — the target exists; that is failure design |
| "how do we measure it in production" | `sa:observability` — SLI implementation, not target setting |
| "how do we prove we met it" | Standard 24, recorded in `sa:handoff` |
| functional requirements generally | not this skill — only functionality that *shapes structure* belongs here |

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P3:** read `sa-intent.md` — stakeholders' concerns, constraints, success criteria. Read any existing drivers file (update mode). Read prior ADRs if present, to avoid re-litigating settled numbers.

**Method:**

1. Extract candidate drivers from intake: structure-shaping functionality, quality attributes, constraints, concerns.
2. Sweep the full attribute checklist in Standard 03. For every attribute, record either a scenario or an explicit `N/A — <reason>`. Silence is not allowed.
3. For each in-play attribute, write ≥1 six-part scenario (source, stimulus, environment, artifact, response, **measure**).
4. Where a measure is unknown, do not invent it. Write `MEASURE UNKNOWN — owner: <name>, needed by: <date>`. **Only an unknown measure on an H/H attribute blocks G1** — that is the gate's exact scope (Standard 00). Unknowns on other attributes are open items with owners, reported but not blocking; treating them as blockers stalls every project permanently and teaches people to override the gate.
5. Rank every attribute on business importance × architectural difficulty. If more than five land H/H, say so and ask the user to force-rank — do not proceed silently.
6. Identify conflicts between attributes and list them; each conflict becomes a candidate ADR.

**P6 Change Summary must include** the ranked table and every unknown measure, before writing.

**P8:** `../method/templates/architecture-drivers.md`.

**P9:** report the H/H set, the unknown measures, the conflict list, then `Next: sa:impact <scope>` (and `sa:adr` for each conflict).
