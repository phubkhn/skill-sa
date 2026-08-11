---
name: flow
description: Create or update a runtime sequence diagram for one architecture-significant scenario, including failures, timeouts, retries, idempotency, consistency, and observability points. Use when the user asks how a request or event moves through the system or requests a sequence diagram. Not for CI/CD pipelines or general business process modelling.
allowed-tools: Read, Grep, Glob
---

# SA — Runtime flow

Model one scenario whose ordering, failure behaviour, or consistency is important. Do not diagram routine CRUD merely for completeness. Follow `../method/SKILL.md` and `../method/standards/workflow.md`.

## Inputs

Read the relevant architecture brief, HLD, ADRs, and existing contracts. Participant names must match the HLD or be explicitly marked as newly proposed.

## Method

1. State the trigger, preconditions, participants, and terminal outcomes.
2. Draw the numbered happy path.
3. Add applicable failure paths: timeout, dependency unavailable, invalid input, duplicate delivery, partial completion, and recovery.
4. Annotate cross-boundary timeouts and retries; ensure retries are bounded and safe.
5. State idempotency for non-safe operations.
6. Mark durability and eventual-consistency points, including visible inconsistency windows.
7. Show compensation or reconciliation for multi-step changes.
8. Add the few signals needed to detect failure and diagnose the flow.

Use `../method/standards/runtime-flow.md`, `../method/standards/diagrams.md`, and `../method/templates/flow-narrative.md`. Default output is `docs/architecture/flows/<flow-name>.puml`; add a narrative only when the diagram cannot hold the required operational detail clearly.

Report provisional timeout or retry values as assumptions. Recommend an interface update only when the flow reveals a missing or inconsistent contract.
