# Standard 02 — Intake

**Artifact:** `00-context/sa-intent.md` (+ `stakeholders.md`)
**Purpose:** fix the problem before anyone designs a solution.

## Required sections

| Section | Content | Done when |
|---|---|---|
| Problem statement | the situation, the pain, the cost of doing nothing — no solution words | a reader can restate it without using any technology noun |
| Outcome | the observable change in the world when this succeeds | expressed as a measurable business/user outcome, not an output |
| Scope | in-scope list **and** out-of-scope list | out-of-scope is non-empty |
| Actors & stakeholders | who uses it, who runs it, who is affected, who decides | each has a named concern |
| Existing landscape | systems, teams, contracts already in place that this must live with | each marked reuse / integrate / replace / avoid |
| Constraints | separated into **given** (imposed, non-negotiable) and **chosen** (our decision, revisitable) | every "given" names its source |
| Assumptions | what we are taking as true without proof | each marked safe / risky |
| Success criteria | how we will judge the architecture, not the project | measurable |
| Open questions | with owner and by-when | |
| Glossary | terms with exactly one meaning in this document | |

## Rules

1. **No solution in the intake.** If a section names a specific product, framework, or topology, it belongs in Constraints (given) or an ADR — not the problem statement.
2. **Out-of-scope is as important as in-scope.** An empty out-of-scope list means the boundary was never discussed.
3. **Given vs chosen constraints must be separated.** Teams routinely treat a chosen constraint as immutable for years. Label it.
4. **Every stakeholder has a concern.** A stakeholder with no stated concern is a name on a list; you will not design for them.
5. **Ambiguity is recorded, not resolved by assumption.** If two stakeholders want opposite things, that is an open question with both names on it.

## Stakeholder table format

| Stakeholder | Role | Concern | Influence (H/M/L) | Consulted on |
|---|---|---|---|---|

## Anti-patterns

- Problem statement that is a solution ("we need a message queue")
- Success criteria that restate the feature list
- "All users" as an actor — decompose until each actor has a distinct goal
- Constraints listed without source, so nobody can ever challenge them

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Problem statement contains no solution or technology nouns
- [ ] Outcome is observable and measurable, not a list of features
- [ ] In-scope list present
- [ ] **Out-of-scope list is non-empty**
- [ ] Boundary conditions stated
- [ ] Every stakeholder has a named concern
- [ ] Decision-makers and veto-holders identified
- [ ] Existing landscape elements each have a disposition (reuse/integrate/replace/avoid)
- [ ] Constraints split into given vs chosen
- [ ] Every given constraint names its source
- [ ] Every assumption marked safe or risky
- [ ] Risky assumptions queued for the risk register
- [ ] Architectural success criteria are measurable
- [ ] Every open question has an owner and a by-when
- [ ] Glossary terms have exactly one meaning
- [ ] No invented answers — unknowns are recorded as open questions
