---
name: intake
description: Capture the architecture problem: scope, stakeholders, constraints, assumptions, open questions, into sa-intent.md. Use at the start of any solution design, or when the user asks to clarify the problem, define scope, or run an architecture intake.
allowed-tools: Read, Grep, Glob
---

# SA — Capture the problem, scope, stakeholders and constraints

| | |
|---|---|
| Journey step | 1 — Intake |
| Produces | 00-context/sa-intent.md, 00-context/stakeholders.md, 00-context/principles.md (if none exists) |
| Inputs | any requirement docs, tickets, notes the user points at |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/02-intake-standard.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/02-intake-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9. Step-specific detail below.

**P3 inputs:** every requirement source the user names; existing `sa-intent.md` (update mode); `00-wiki`-style glossary if the repo has one.

**Elicitation — before the Change Summary, ask about anything the sources do not answer.** Batch questions; do not ask one at a time. Minimum coverage:

1. What breaks today, and what does it cost? Who feels it?
2. What is explicitly *out* of scope?
3. Who decides? Who can veto? Who must be consulted?
4. What already exists that this must live with — systems, contracts, teams?
5. Which constraints are imposed on us, and by whom? Which did we choose?
6. What does "done well" look like six months after launch?
7. What has been tried before, and why did it not work?
8. What is the deadline, and what is driving it?

If a question cannot be answered, it becomes an Open Question with an owner — never an invented answer.

**Architecture principles.** If `00-context/principles.md` does not exist, offer to create it from `../method/templates/principles.md` — 5–10 principles, each with a rationale and a stated implication. Principles are organisation-level and outlive the initiative, so ask whether one already exists elsewhere before writing a new one. Every ADR is later checked against them; a deviation is allowed but must be argued in the ADR, not passed over.

A principle nobody could disagree with ("we value quality") is not a principle. A usable one forecloses something: "we prefer boring technology — a new runtime requires an ADR naming who operates it."

**P8 write:** use `../method/templates/sa-intent.md`, `../method/templates/stakeholders.md`. Enforce Standard 02 rules:
- no solution language in the problem statement
- non-empty out-of-scope list
- constraints split into `given` (with source) and `chosen`
- every stakeholder has a concern
- every assumption marked safe/risky; risky ones are queued for the risk register

**P9 report:** list the open questions with owners, then `Next: sa:drivers <scope>`.
