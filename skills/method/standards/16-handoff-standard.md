# Standard 16 — Implementation Handoff

**Artifact:** `10-handoff/dev-handoff-<YYYY-MM-DD>.md`
**Purpose:** a team should be able to start building on Monday without another architecture meeting.

## Required content

| Section | Content |
|---|---|
| Scope | what is being handed over, and explicitly what is not |
| Artifact index | every design artifact with path, version, and status — links only to `Accepted` ones |
| Build order | ordered work packages with dependencies and the reason for the order |
| Work packages | per package: goal, components touched, interfaces involved, acceptance criteria, drivers it must satisfy |
| Contracts to implement first | interfaces that unblock other teams — these lead |
| Non-negotiables | the design constraints that must not be changed without returning to the SA, each with its ADR |
| Free choices | explicitly what the team may decide alone — prevents unnecessary escalation |
| Environment & dependencies | what must exist before work starts (accounts, topics, stores, credentials, test doubles) |
| Verification | how each driver will be proven met (test type, tool, threshold) |
| Definition of done | per work package, including observability and runbook deliverables |
| Open items | unresolved design questions, with owner and the date they block work |
| Risks the team must know | subset of the risk register that affects implementation |
| Contact & escalation | who answers architecture questions, and how a design change is requested |

## Work package table

| ID | Package | Depends on | Components | Interfaces | Drivers | Acceptance criteria | Size | Notes |
|---|---|---|---|---|---|---|---|---|

## Rules

1. **Handoff is gated by G4.** No handoff from a `NOT READY` review.
2. **Only `Accepted` artifacts are linked.** Linking a draft transfers uncertainty silently.
3. **Sequencing is by dependency and risk** — highest-uncertainty, highest-coupling work first, so bad assumptions surface early.
4. **Say what the team may decide.** A handoff that specifies everything produces either resentment or paralysis.
5. **Every non-negotiable cites its ADR.** "Because the architect said so" does not survive contact with a deadline.
6. **Verification is designed here**, not discovered at the end. Each driver has a named way of being proven.
7. **Handoff includes operational deliverables** — dashboards, alerts, runbooks are part of done, not follow-up work.
8. **Design change requests have a route.** State it, or the design will be changed silently.

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] G3 passed: every component has an LLD and an interface spec; flows reference only existing components
- [ ] G4 passed: review verdict READY, or all conditions closed
- [ ] Every High risk mitigated or accepted with a signature
- [ ] Artifact index links only Accepted artifacts; Drafts listed separately
- [ ] Work packages have goal, components, interfaces, drivers, acceptance criteria, size
- [ ] Build order stated **with the reason** for the order
- [ ] Unblocking contracts sequenced first
- [ ] Highest-uncertainty work sequenced early
- [ ] Non-negotiables each cite an ADR
- [ ] Free choices stated explicitly
- [ ] Prerequisites for day one listed with owners and status
- [ ] Verification plan names test type, tool, and threshold per driver
- [ ] Definition of done includes dashboards, alerts, and runbooks
- [ ] Open items have owners and the date they start blocking
- [ ] Implementation-relevant risks extracted for the team
- [ ] Escalation and design-change route stated
