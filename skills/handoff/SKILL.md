---
name: handoff
description: Produce the implementation-ready handoff: artifact index, work packages, build order, non-negotiables, verification plan and definition of done. Use when the user asks to hand the design over to a development team or prepare it for implementation.
---

# SA — Produce the implementation-ready handoff package

| | |
|---|---|
| Journey step | 15 — Handoff |
| Produces | 10-handoff/dev-handoff-<YYYY-MM-DD>.md |
| Inputs | all Accepted artifacts, latest design review, risk register |
| Gate | G3 and G4 (before running) |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/16-handoff-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/16-handoff-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P5 Gates:**
- **G3 — contract frozen:** every HLD component has an LLD and an interface spec; every flow references only components present in the HLD.
- **G4 — fit to build:** the latest `09-review/design-review-*.md` verdict is `READY` (or `READY WITH CONDITIONS` with every condition closed) and every High risk has a mitigation or a signed acceptance.

On failure, stop and name the failing condition and the command that fixes it.

**Method:**

1. **Artifact index:** every artifact with path, version, status. Link only `Accepted` ones; list `Draft` ones separately under "not yet agreed".
2. **Work packages:** decompose the build. Per package: goal, components touched, interfaces involved, drivers it must satisfy, acceptance criteria, rough size.
3. **Sequencing by dependency and risk.** Contracts that unblock other teams go first; highest-uncertainty work goes early so bad assumptions surface while they are cheap. State the reason for the order, not just the order.
4. **Non-negotiables:** design constraints that must not change without returning to the SA — each citing its ADR.
5. **Free choices:** state explicitly what the team may decide alone. This is what prevents both escalation fatigue and silent drift.
6. **Prerequisites:** environments, accounts, topics, stores, credentials, test doubles that must exist before day one.
7. **Verification plan:** per driver — the test type, tool, and threshold that will prove it met.
8. **Definition of done** per work package, including dashboards, alerts, and runbooks as deliverables, not follow-ups.
9. **Open items** with owner and the date each starts blocking work.
10. **Risks the team must know**, extracted from the register.
11. **Escalation route:** who answers architecture questions, and how a design change is requested.

**P9:** report the package count, the critical path, and any open item that blocks day one. Then: `/sa:trace <scope>` to publish the trace index.
