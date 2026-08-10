---
name: risk
description: Sweep every artifact for risks and consolidate them into an owned register with probability, impact, mitigation and review dates, plus a trade-off log. Use when the user asks for a risk register, risk analysis, or trade-off documentation.
allowed-tools: Read, Grep, Glob
---

# SA — Consolidate risks and trade-offs into an owned register

| | |
|---|---|
| Journey step | 14 — Risk |
| Produces | 01-analysis/risk-register.md |
| Inputs | all artifacts under docs/architecture |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/14-risk-standard.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/14-risk-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P8:** `../method/templates/risk-register.md`.

**P3 — sweep, do not brainstorm.** Collect candidates mechanically from:

1. every assumption marked `risky` in any artifact
2. every `Unknown (investigate)` row in the impact analysis
3. every negative consequence in an `Accepted` ADR
4. every residual risk in the security design
5. every residual risk in the failure-mode table
6. every driver whose measure is `UNKNOWN` or unverified
7. every gate that was overridden
8. every dependency owned by another team or vendor
9. every open item with a passed by-when date
10. every cost figure labelled `estimated` that materially changes the decision
11. every buy/adopt ADR whose exit plan is missing or hand-waved
12. every coexistence arrangement with no end date
13. every seed artifact still contradicting its authority (two-pass rule, Standard 00)

**Method:**

1. Restate each candidate in conditional form: *"Because <fact>, <event> may occur, resulting in <consequence>."* Anything that cannot be phrased this way is a fact or a fear — reclassify it.
2. Merge duplicates across artifacts; keep the strongest phrasing and link both sources.
3. Rate probability and impact using the project-specific scale defined at the top of the register — not universal adjectives.
4. Assign **one named owner** per risk. Team names are rejected; ask for a person.
5. Choose a response: avoid / mitigate / transfer / accept. `Accept` requires a named accepter and a date.
6. Every mitigation must correspond to a concrete design change or a work item. A mitigation with no artifact is a wish — flag it.
7. Set a review date per risk.
8. Update the **trade-off log** with choices too small for an ADR: gained, given up, drivers favoured, drivers sacrificed, revisit-when.
9. Never delete a realised risk — mark `Realised` and link the incident.

**P9:** report High-exposure risks lacking mitigation, risks lacking a named owner, and mitigations with no corresponding change, then `Next: sa:review <scope>`.
