---
name: adr
description: Write an Architecture Decision Record with real alternatives, evaluation against drivers, and negative consequences. Use when a structural, hard-to-reverse or contested choice must be recorded, or the user asks for an ADR or decision record.
---

# SA — Record an architecture decision with alternatives and consequences

| | |
|---|---|
| Journey step | 4 — Decisions |
| Produces | 02-decisions/ADR-NNNN-<slug>.md, updates adr-index.md |
| Inputs | 00-context/architecture-drivers.md, 01-analysis/impact-analysis.md, existing ADRs |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/05-adr-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/05-adr-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

Arguments: $ARGUMENTS — the decision, in a few words. If absent, list the open decisions found in drivers (conflicts) and impact analysis (unknowns) and ask which to record.

**P3:** read drivers (for the evaluation axes), impact analysis, and **all existing ADRs** — check whether this decision is already made or contradicts an accepted one. If it contradicts, this ADR must supersede the old one explicitly.

**Method:**

1. Determine the next ADR number: highest existing + 1, zero-padded to 4.
2. Write **Context** with no solution language — forces, driver IDs, constraints, what makes this hard.
3. Enumerate options. **Minimum two real ones**; include "do nothing / keep current" where it is credible. If the user offers only one, ask what was rejected and why — a decision with no alternative is a preference.
4. Build the **evaluation matrix**: rows = drivers (by ID), columns = options. This is the argument; make it explicit.
5. State the decision in one active sentence.
6. Write consequences — positive, **negative (mandatory)**, neutral, and what becomes harder later.
7. Define **compliance**: the concrete way anyone can check the decision is being followed.
8. Set status: `Proposed` unless the user confirms the deciders have agreed.

**P6:** show the evaluation matrix in the Change Summary. This is the part worth arguing about before it is written.

**P8:** `../method/templates/adr.md`; append a row to `adr-index.md`; if superseding, edit the old ADR's status line only.

**P9:** `Next: /sa:gen-hld <scope>` once the structural ADRs are Accepted.
