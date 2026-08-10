# Architecture Principles — <organisation or scope>

<!-- Header block — copy from standards/01-workflow-protocol.md, phase P8 -->

Principles outlive any one initiative. Every ADR is checked against them; a deviation is permitted but must be argued in the ADR, never passed over silently.

**A principle nobody could disagree with is not a principle.** "We value quality" forecloses nothing. A usable principle rules something out.

5–10 principles. More than that and none of them are load-bearing.

---

## P1 — <principle, stated as a preference with a direction>

**Rationale** — why this, for this organisation, now.

**Implication** — what teams must actually do differently. This is the part that gets cited.

**What it rules out** — the concrete thing you are agreeing not to do.

**Exception route** — an ADR naming <who> must approve a deviation.

---

## P2 — <…>

**Rationale**

**Implication**

**What it rules out**

**Exception route**

---

## Worked example (delete when the real ones are written)

### P0 — Prefer boring technology

**Rationale** — our operational capacity, not our engineering appetite, is the binding constraint. Every new runtime, store or broker adds an on-call burden that outlives the team that chose it.

**Implication** — a technology not already in the estate requires its own ADR, naming who will operate it and what its run cost is.

**What it rules out** — adopting a new datastore because it fits one query pattern better.

**Exception route** — ADR approved by the head of platform.

---

## Deviations on record

| ADR | Principle | Deviation | Argument accepted by | Date |
|---|---|---|---|---|
| | | | | |
