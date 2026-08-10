---
name: impact
description: Analyse what an architecture change disturbs: baseline, blast radius, impacted and unaffected elements, contract/data/operational impact, stale artifacts. Use when the user asks what a change affects or asks for an impact analysis.
allowed-tools: Read, Grep, Glob
---

# SA — Establish the baseline and determine what this change disturbs

| | |
|---|---|
| Journey step | 3 — Impact |
| Produces | 01-analysis/impact-analysis.md |
| Inputs | 00-context/sa-intent.md, 00-context/architecture-drivers.md, existing 03-hld/**, 05-lld/**, 06-interfaces/** |
| Gate | G1 (before running) |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/04-impact-analysis-standard.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/04-impact-analysis-standard.md` — self-assess item by item in P9.

## When to use

- "what will this change break", "what's the blast radius", "who else is affected"
- Establishing a baseline when no architecture documentation exists
- Before deciding anything — the impact analysis is what makes the ADR options concrete

## When not to use

| Request | Use instead |
|---|---|
| "is this design good" | `sa:review` — judging a finished design, not predicting a change |
| "what's now out of date" | `sa:trace --stale` — impact *predicts* staleness, trace *detects* it |
| "what could go wrong" | `sa:risk` — this emits candidate risks, it does not own the register |
| "which approach should we take" | `sa:options` — this analyses disturbance, it does not choose |

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P5 Gate G1:** intent has scope with a non-empty out-of-scope list and named stakeholders; drivers has ≥1 measurable scenario for every attribute in the **H/H quadrant** (high business importance × high architectural difficulty). Attributes outside H/H do not gate. This threshold is defined once in `../method/standards/00-sa-journey.md`; do not apply a stricter one. Report failures precisely; ask before overriding, and record any override as an accepted risk.

**P3:** read intent, drivers, and every existing design artifact. If the repository has no existing architecture docs, ask the user where the current-state knowledge lives (code, diagrams, people) and record the source of the baseline.

**Method:**

1. Write the **baseline** — current state relevant to this change only.
2. **Blast-radius walk:** for each element the change obviously touches, walk one hop outward (callers, callees, data readers, event consumers, co-deployed units). Repeat until a hop adds nothing new.
3. Record every element reached in the impacted table, including `None (verified)` rows with the evidence that made it verified.
4. Classify contract impact per consumer — breaking or not, judged from the consumer's tolerance, not the schema.
5. Record data impact, operational impact, organisational impact.
6. For every element with impact `Remove`, fill the **decommissioning table**: who still calls it, how they stop, migration deadline, switch-off date, data disposition, and the named person who confirms nothing reads it.
7. List **stale artifacts** by path — these become the re-run list.
8. Note effort and sequencing constraints (what must precede what).
9. Emit candidate risks for every `Unknown (investigate)` row; they go to the risk register.

**P8:** `../method/templates/impact-analysis.md`.

**P9:** report the impacted/new/stale counts and the unknowns, then `Next: sa:adr <decision-slug>` for each contested choice.
