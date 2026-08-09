# Standard 05 — Architecture Decision Records

**Artifact:** `02-decisions/ADR-NNNN-<slug>.md`, indexed in `adr-index.md`
**Purpose:** make the *reasoning* durable, so future readers can tell a deliberate choice from an accident.

## When an ADR is required

Write one when the decision is: hard to reverse, cross-cutting, cost-bearing, contested, or surprising. Concretely:

- Structural style or decomposition boundary
- Synchronous vs asynchronous integration
- Data ownership and consistency model
- Persistence/storage class choice
- Authentication/authorisation approach
- Public contract style and versioning approach
- Build vs buy vs reuse
- Deployment/runtime topology
- Anything a reviewer asked "why?" about twice

If the decision could be reversed in an afternoon by one team, it does not need an ADR.

## Structure

```markdown
# ADR-NNNN — <decision in imperative, e.g. "Use event-driven integration between X and Y">

| Status | Proposed | Accepted | Rejected | Superseded by ADR-NNNN | Deprecated |
| Date | Deciders | Trace ID | Drivers addressed |

## Context
The forces at play: drivers (by ID), constraints, current state, what makes this hard.
No solution language here.

## Decision
One sentence, active voice, present tense. "We will ..."

## Options considered
| Option | Summary | Pros | Cons | Why not chosen |
Minimum two real options. "Do nothing" is a legitimate option and is often the right baseline.

## Evaluation against drivers
| Driver | Option A | Option B | Option C |
Score or reason per driver — this is the actual argument.

## Consequences
**Positive:** ...
**Negative:** ...  (mandatory — a decision with no downside was not a decision)
**Neutral / follow-on work:** ...
**What becomes harder later:** ...

## Compliance / verification
How we will know the decision is actually being followed (fitness function, lint rule, review check).

## Related
ADRs, drivers, artifacts affected.
```

## Rules

1. **Immutable once Accepted.** To change a decision, write a new ADR and mark the old one `Superseded by`. Never edit history.
2. **Minimum two genuine alternatives.** A straw-man option is worse than no option — it hides that no evaluation happened.
3. **Negative consequences are mandatory.** If you cannot name one, you have not understood the choice.
4. **Decide against drivers, not preferences.** Every evaluation row references a driver ID from Standard 03.
5. **One decision per ADR.** Bundled decisions cannot be superseded independently.
6. **Status is honest.** `Proposed` until the deciders have actually agreed.

## Index format (`adr-index.md`)

| ADR | Title | Status | Date | Drivers | Supersedes | Superseded by |
|---|---|---|---|---|---|---|

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Exactly one decision in this ADR
- [ ] Context contains no solution language
- [ ] Driver IDs cited in Context
- [ ] ≥2 genuine alternatives, none of them straw men
- [ ] "Do nothing / keep current" considered where credible
- [ ] Evaluation matrix scores options against drivers, not preferences
- [ ] Decision is one sentence, active voice
- [ ] **Negative consequences stated**
- [ ] "What becomes harder later" stated
- [ ] Compliance/verification mechanism defined
- [ ] Status honest (`Proposed` unless deciders actually agreed)
- [ ] Existing ADRs checked for conflict; supersession recorded if any
- [ ] Number is highest existing + 1, zero-padded
- [ ] `adr-index.md` updated
