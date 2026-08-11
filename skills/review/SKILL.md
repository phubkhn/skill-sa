---
name: review
description: Independently review architecture advice and design artifacts for driver satisfaction, consistency, contracts, data ownership, security, resilience, observability, operability, simplicity, cost, and buildability. Use when the user asks whether a design is sound or ready to guide implementation. Not for source-code or pull-request review.
allowed-tools: Read, Grep, Glob
disallowed-tools: Edit, NotebookEdit
context: fork
---

# SA — Architecture review

Judge the design that exists on disk. Do not edit it. A conversation-only review is valid; write a report only when the user asks for one or the repository already uses review artifacts. Follow `../method/SKILL.md` and `../method/standards/workflow.md`.

## Scope

Read the architecture brief and specialised artifacts relevant to the change. Do not require a predefined profile or report absent optional documents as findings. State what was not reviewed.

## Method

1. Inventory the reviewed artifacts and their status.
2. Identify the prioritised drivers and show the design mechanism that satisfies each one.
3. Check consistency among decisions, diagrams, flows, contracts, and data ownership.
4. Review proportionally across: security, resilience, observability, operability, simplicity, cost direction, deployment, and buildability.
5. Raise a finding only with evidence and a violated driver, decision, contract, or explicit quality rule. Otherwise label it an observation.
6. Use `Blocker`, `Major`, `Minor`, or `Observation`.
7. Compute the verdict: any Blocker → `NOT READY`; otherwise any Major → `READY WITH CONDITIONS`; otherwise `READY`.
8. State what is good and what was not reviewed.

Use `../method/standards/review.md` and `../method/templates/design-review.md`. Prefer stable section references; use line numbers only when they are reliable. Default report location is `docs/architecture/reviews/design-review-<date>.md`.

Report the smallest corrective action and the owning core skill for each Blocker or Major. Never fix design artifacts during the review.
