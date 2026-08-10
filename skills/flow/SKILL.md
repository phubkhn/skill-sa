---
name: flow
description: Produce a runtime sequence diagram for one flow, including failure paths, timeouts, retries, idempotency and consistency points. Use when the user asks for a flow, sequence diagram, or how a scenario behaves at runtime. Not for CI/CD pipeline definitions or business process modelling notation.
allowed-tools: Read, Grep, Glob
---

# SA — Produce a runtime sequence diagram for one flow

| | |
|---|---|
| Journey step | 6 — Flows |
| Produces | 04-flows/<flow-name>.puml + narrative table |
| Inputs | 03-hld/*, 00-context/architecture-drivers.md, 02-decisions/* |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/07-flow-standard.md`, `../method/standards/18-diagram-conventions.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/07-flow-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

Arguments: $ARGUMENTS — `<flow-name>`. If absent, propose the flow list using Standard 07's selection criteria (cross-component, async, failure-heavy, security-sensitive, driver-linked) and ask which to generate.

**P3:** read the HLD element catalogue — participant names must match it exactly. Read drivers linked to this flow, and ADRs governing its integration style.

**Method:**

1. State the trigger and all participants. **Reject any participant not present in the HLD** — either add it to the HLD first or rename.
2. Draw the happy path, numbered.
3. For **every** cross-boundary call, annotate timeout, retry policy, and backoff. Verify timeout budgets nest (caller > callee total).

   **Two-pass rule (Standard 00):** the flow is the *seed* for timeouts and retries; `sa:resilience` is the *authority* on the nested budget. If no resilience design exists yet, set provisional values and mark them so; re-run this flow in Update mode once the budget is fixed.
4. For every non-safe operation, state the idempotency mechanism.
5. Add failure paths — walk the failure checklist in Standard 07 and cover every applicable one, or state why not.
6. Mark consistency points: where state becomes durable, where it is eventual, and the visible window.
7. Add compensation/rollback for any multi-step state change.
8. Show terminal states: success, failure, partial, timed-out.
9. Add observability hooks — what is emitted at each significant step; these feed `sa:observability`.
10. If the flow exceeds ~20 steps, decompose into sub-flows and reference them.

**P8:** sequence diagram + narrative table (`../method/templates/flow-narrative.md`). Validate participant names against the HLD one final time before writing.

**P9:** report which failure modes were covered and which were consciously skipped, then the next flow or `sa:lld <component>`.
