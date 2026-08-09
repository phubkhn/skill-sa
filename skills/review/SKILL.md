---
name: review
description: Run an evidence-based design review against standards and drivers, producing findings with severity and a mechanical verdict. Use when the user asks to review, audit, or sign off an architecture design.
---

# SA — Gated, evidence-based review of the whole design

| | |
|---|---|
| Journey step | 14 — Review |
| Produces | 09-review/design-review-<YYYY-MM-DD>.md |
| Inputs | everything under docs/architecture |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/15-review-standard.md`, `../method/standards/20-quality-bar.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/15-review-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P5 and P8–P9. **This command does not modify any design artifact** — it only writes the review report.

Arguments: $ARGUMENTS — scope, optionally `--dimension <n>` to review one dimension only (record the scope limit in the report).

**Method:**

1. **Artifact inventory:** list every expected artifact with its path, version, and status. Missing or `Draft` artifacts are recorded before any judgement is made.
2. **Quality bar pass:** evaluate each artifact against `../method/standards/20-quality-bar.md` — universal items plus its per-artifact items. Explicit pass/fail per item; no silent passes.
3. **Consistency matrix:** run every mechanical check in Standard 15 (HLD↔LLD, responsibility↔operation, flow participants↔HLD, event publisher↔consumer, single data owner, vocabulary drift, dependency cycles, ADR status, driver coverage, risk coverage). Report result and detail per check.
4. **Driver coverage:** for each driver, state whether the design satisfies it, **by what mechanism**, with evidence (file + location), and your confidence. A driver satisfied "by design" with no named mechanism is a Blocker.
5. **Dimension review:** walk all 13 dimensions in Standard 15.
6. **Findings:** each with severity, dimension, evidence (`path:line`), the standard or driver violated, a recommendation, and an owner. No evidence → it is an Observation, not a Finding.
7. **Verdict, computed mechanically:** any Blocker → `NOT READY`. No Blocker but ≥1 Major → `READY WITH CONDITIONS` (list conditions with owner and by-when). Otherwise → `READY`.
8. **What is good** — state it explicitly.
9. **Not reviewed** — state the scope limits. An unstated limit reads as approval.

**P9:** report the verdict, blocker count, and the exact commands that fix each blocker. If `READY`, `Next: /sa:gen-handoff <scope>`.
