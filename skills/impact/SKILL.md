---
name: impact
description: Analyse what an architecture change disturbs: baseline, blast radius, impacted and unaffected elements, contract/data/operational impact, stale artifacts. Use when the user asks what a change affects or asks for an impact analysis.
---

# SA — Establish the baseline and determine what this change disturbs

| | |
|---|---|
| Journey step | 3 — Impact |
| Produces | 01-analysis/impact-analysis.md |
| Inputs | 00-context/sa-intent.md, 00-context/architecture-drivers.md, existing 03-hld/**, 05-lld/**, 06-interfaces/** |
| Gate | G1 (before running) |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/04-impact-analysis-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/04-impact-analysis-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P5 Gate G1:** intent has scope with a non-empty out-of-scope list and named stakeholders; drivers has ≥1 measurable scenario per H/H attribute. Report failures precisely; ask before overriding.

**P3:** read intent, drivers, and every existing design artifact. If the repository has no existing architecture docs, ask the user where the current-state knowledge lives (code, diagrams, people) and record the source of the baseline.

**Method:**

1. Write the **baseline** — current state relevant to this change only.
2. **Blast-radius walk:** for each element the change obviously touches, walk one hop outward (callers, callees, data readers, event consumers, co-deployed units). Repeat until a hop adds nothing new.
3. Record every element reached in the impacted table, including `None (verified)` rows with the evidence that made it verified.
4. Classify contract impact per consumer — breaking or not, judged from the consumer's tolerance, not the schema.
5. Record data impact, operational impact, organisational impact.
6. List **stale artifacts** by path — these become the re-run list.
7. Note effort and sequencing constraints (what must precede what).
8. Emit candidate risks for every `Unknown (investigate)` row; they go to the risk register.

**P8:** `../method/templates/impact-analysis.md`.

**P9:** report the impacted/new/stale counts and the unknowns, then `Next: /sa:gen-adr <decision-slug>` for each contested choice.
