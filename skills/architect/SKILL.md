---
name: architect
description: Primary entry point for Solution Architecture work. Use for any request to understand an architecture problem, inspect an existing system, compare solution approaches, propose a target architecture, create a concise architecture brief, plan a change, or decide which SA artifact is needed. Prefer this skill whenever the user has not explicitly requested ADR, HLD, flow, interface, data design, or architecture review.
allowed-tools: Read, Grep, Glob
---

# SA Architect

Turn an architecture question into the smallest useful answer or artifact. Do not make the user choose a process step first. Follow `../method/SKILL.md` and `../method/standards/workflow.md`.

## Core outcomes

Choose one outcome from the request and available evidence:

| Outcome | Use when | Result |
|---|---|---|
| `quick` | The user needs advice, diagnosis, trade-offs, or a recommendation | Answer in the conversation; write nothing |
| `brief` | The change needs a shared design baseline | `docs/architecture/architecture-brief.md` by default |
| `artifact` | The user explicitly needs a decision, diagram, flow, contract, data design, or review | Follow the matching core skill |

Default to `quick` for exploratory questions and `brief` for requests to design or document a solution. Never require `sa-config.yaml` just to start.

## Core artifact routing

| Need | Read and follow |
|---|---|
| Record one consequential decision | `../adr/SKILL.md` |
| Draw static system structure or deployment | `../hld/SKILL.md` |
| Explain runtime behaviour and failure paths | `../flow/SKILL.md` |
| Define an API or event contract | `../interface/SKILL.md` |
| Decide data ownership, lifecycle, or migration | `../data/SKILL.md` |
| Judge whether a design is fit to build | `../review/SKILL.md` |

If several artifacts are needed, create the brief first and add only the artifacts that resolve a real ambiguity or unblock another team.

## Working method

1. **Understand.** Read the user's sources and inspect only the repository areas relevant to the change. Separate evidence, assumptions, and open questions.
2. **Frame.** State the problem, scope, constraints, stakeholders, measurable drivers, and current-state impact. Ask at most three questions, only when different answers would materially change the design.
3. **Explore.** Compare two or three credible approaches, including keeping the current design when credible. Evaluate them against the drivers, delivery risk, operational burden, cost direction, and reversibility.
4. **Recommend.** Name the recommended shape, the deciding trade-off, negative consequences, and the fact that would change the recommendation.
5. **Deliver.** Answer in chat or use `../method/templates/architecture-brief.md`. If writing, honour an existing `sa-config.yaml`; otherwise use `docs/architecture` and the user's language.
6. **Check.** Verify names agree across the brief and existing artifacts; label unsupported claims as assumptions; report unresolved decisions and the exact next core skill only when another artifact is justified.

## Architecture brief content

Keep the brief concise enough to review in one sitting. Include:

- problem, outcome, in/out of scope
- stakeholders and constraints
- three to five measurable architecture drivers
- current state and change impact, with sources
- options considered and recommendation
- target structure and primary runtime flow
- interface and data ownership implications
- security, resilience, observability, cost direction, and delivery implications
- decisions, risks, assumptions, and open questions

Use diagrams only when they clarify relationships that prose cannot. Cover risk, cost, security, resilience, observability, and delivery implications proportionally in the brief; split a concern only when its complexity or audience requires it.

## Interaction rules

- Start from the user's goal, not from the method vocabulary.
- Make reasonable, labelled assumptions instead of running a questionnaire.
- Do not scaffold an empty documentation tree.
- Do not create an artifact merely because a template exists.
- When the user asks to create or update files, give a concise one-paragraph scope and proceed. Ask for explicit confirmation only before replacing an accepted decision, deleting content, or making a materially ambiguous multi-file change.
- Preserve existing project conventions when they are clear; introduce this method's defaults only where the repository has none.

Load a detailed standard only when the selected artifact needs it.
