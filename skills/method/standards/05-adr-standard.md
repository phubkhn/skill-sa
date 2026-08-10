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

## Build vs buy vs reuse — required evaluation axes

When the decision involves adopting a third-party product or service, the options table is not enough. Add these rows to the evaluation matrix, because they are the ones that hurt three years later and none of them are visible in a feature comparison.

| Axis | The question to answer concretely |
|---|---|
| Exit cost | what does leaving cost, in effort and in elapsed time? Who has done it? |
| Data portability | can we get our data out, in a usable shape, without the vendor's cooperation? |
| Lock-in surface | how much of our code and our data model has to know this vendor exists? |
| SLA vs our driver | is their contractual availability at least our target? (Standard 13 — a hard dependency caps you at its own ceiling) |
| Data residency | where does data physically live, and does that satisfy the compliance obligations in the security design? |
| Roadmap dependency | are we depending on something they have promised but not shipped? |
| Support model | response times, escalation path, and what happens outside business hours |
| Total cost at scale | licence plus consumption at the 36-month volume (Standard 23), not at today's |
| Viability | is the vendor likely to exist, and to still support this product, for the life of our system? |

**Every buy decision states its exit plan** in the Consequences section. Not a detailed migration — a paragraph naming what we would do and roughly what it would cost. An adoption with no exit plan is not a decision, it is a marriage.

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
- [ ] Compliance/verification mechanism defined — automated as a fitness function where the property is mechanically checkable (Standard 24)
- [ ] Consistent with the architecture principles, or the deviation is stated and argued
- [ ] For a buy/adopt decision: all nine vendor axes evaluated, and an exit plan stated in Consequences
- [ ] Status honest (`Proposed` unless deciders actually agreed)
- [ ] Existing ADRs checked for conflict; supersession recorded if any
- [ ] Number is highest existing + 1, zero-padded
- [ ] `adr-index.md` updated
