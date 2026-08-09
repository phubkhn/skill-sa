# Standard 07 — Runtime Flows

**Artifact:** `04-flows/<flow-name>.puml` + a short narrative per flow
**Purpose:** show behaviour over time — the thing static diagrams cannot express.

## Which flows to document

Not all of them. Document a flow when it is:

- A primary use case that drives structure
- Cross-component (≥ 2 containers involved)
- Asynchronous or eventually consistent
- Failure/compensation-heavy
- Security-sensitive (authn/authz, secret handling)
- The subject of a quality-attribute scenario (latency, throughput, recovery)

A flow entirely inside one component belongs in the LLD, not here.

## Mandatory content per flow

| # | Element |
|---|---|
| 1 | Trigger — what starts it (user action, schedule, event, retry) |
| 2 | Participants — all identical to HLD element names |
| 3 | Happy path, numbered steps |
| 4 | At least one failure path per external dependency |
| 5 | Timeouts, retries, and backoff where calls cross a boundary |
| 6 | Idempotency handling for any non-safe operation |
| 7 | Consistency points — where state becomes durable, where it is only eventual |
| 8 | Compensation/rollback for multi-step state changes |
| 9 | Terminal states — success, failure, partial, timed-out |
| 10 | Observability hooks — what is logged/emitted at each significant step |

## Narrative table (accompanies every diagram)

| Step | Actor | Action | Data | Sync/Async | Failure behaviour | Emits |
|---|---|---|---|---|---|---|

## Rules

1. **A flow with only a happy path is not finished.** The failure paths are why the diagram exists.
2. **Participants must exist in the HLD, with the same names.** A participant that isn't in the HLD means one of the two is wrong.
3. **Every cross-boundary call declares its timeout.** "Default" is an answer only if you state the default value.
4. **Retries must state whether the operation is idempotent.** Retrying a non-idempotent operation is a defect on the diagram.
5. **Eventual consistency is drawn, not assumed.** Show the window and what a reader sees during it.
6. **No flow longer than ~20 steps.** Decompose into sub-flows and reference them.

## Failure paths to cover (checklist)

Dependency timeout · dependency error response · dependency unavailable · partial success · duplicate/replayed request · concurrent conflicting request · invalid input · authorisation denied · resource exhausted · message lost · message out of order · poison message

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Trigger stated
- [ ] Every participant exists in the HLD with an identical name
- [ ] Happy path numbered and complete to a terminal state
- [ ] ≥1 failure path per external dependency
- [ ] Failure checklist walked; skipped items justified
- [ ] Every cross-boundary call declares a timeout value
- [ ] Timeout budgets nest correctly across the chain
- [ ] Retries only on idempotent operations, with backoff, jitter, and a cap
- [ ] Idempotency mechanism stated for every non-safe operation
- [ ] Consistency points marked; eventual windows and visible effects stated
- [ ] Compensation/rollback shown for multi-step state changes
- [ ] All terminal states shown (success, failure, partial, timed-out)
- [ ] Observability hooks noted per significant step
- [ ] ≤ ~20 steps, or decomposed into referenced sub-flows
