---
name: drivers
description: Turn constraints and stakeholder concerns into measurable quality-attribute scenarios (performance, availability, security, modifiability...). Use when the user asks for NFRs, quality attributes, SLOs as requirements, or architecture drivers.
---

# SA — Turn constraints and concerns into measurable quality-attribute scenarios

| | |
|---|---|
| Journey step | 2 — Drivers |
| Produces | 00-context/architecture-drivers.md |
| Inputs | 00-context/sa-intent.md |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/03-drivers-nfr-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/03-drivers-nfr-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P3:** read `sa-intent.md` — stakeholders' concerns, constraints, success criteria. Read any existing drivers file (update mode). Read prior ADRs if present, to avoid re-litigating settled numbers.

**Method:**

1. Extract candidate drivers from intake: structure-shaping functionality, quality attributes, constraints, concerns.
2. Sweep the full attribute checklist in Standard 03. For every attribute, record either a scenario or an explicit `N/A — <reason>`. Silence is not allowed.
3. For each in-play attribute, write ≥1 six-part scenario (source, stimulus, environment, artifact, response, **measure**).
4. Where a measure is unknown, do not invent it. Write `MEASURE UNKNOWN — owner: <name>, needed by: <date>` and flag it as a G1 blocker.
5. Rank every attribute on business importance × architectural difficulty. If more than five land H/H, say so and ask the user to force-rank — do not proceed silently.
6. Identify conflicts between attributes and list them; each conflict becomes a candidate ADR.

**P6 Change Summary must include** the ranked table and every unknown measure, before writing.

**P8:** `../method/templates/architecture-drivers.md`.

**P9:** report the H/H set, the unknown measures, the conflict list, then `Next: /sa:gen-impact-analysis <scope>` (and `/sa:gen-adr` for each conflict).
