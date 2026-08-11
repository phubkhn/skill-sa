---
name: method
description: Internal shared method for the SA plugin, plus guidance on which core architecture skill to use. Use when the user asks how the SA skill set works or which SA command to run. For general architecture work, prefer sa:architect.
allowed-tools: Read, Grep, Glob
---

# SA Method

Keep architecture work proportional to the decision being made. Start with `/sa:architect`; create specialised artifacts only when they resolve ambiguity, preserve an important decision, or provide a contract another team needs.

## Core skills

| Skill | Core question | Default output |
|---|---|---|
| `/sa:architect` | What should we build and why? | advice or `architecture-brief.md` |
| `/sa:adr` | Which consequential choice was made? | one ADR |
| `/sa:hld` | What are the parts and relationships? | focused C4/deployment view |
| `/sa:flow` | How does one important scenario behave? | sequence diagram + short narrative |
| `/sa:interface` | What is the contract across a boundary? | OpenAPI or AsyncAPI |
| `/sa:data` | Who owns the data and how does it live or move? | data design; migration plan when needed |
| `/sa:review` | Is the design coherent and fit to build? | review report or conversation findings |

Problem framing, drivers, current-state impact, options, cross-cutting concerns, risk, and delivery implications are sections of the architecture brief by default. Split them into separate documents only when scale, regulation, ownership, or an explicit user request justifies it. Low-level implementation detail belongs to the delivery team unless it exposes a cross-team architectural contract.

## Modes

| Mode | Behaviour |
|---|---|
| `quick` | Analyse and advise in the conversation. No config or files required. |
| `brief` | Create or update one concise architecture brief. |
| `artifact` | Create the explicitly requested ADR, view, flow, contract, data design, or review. |

Choose the smallest mode that answers the request. Do not force a complete journey.

## Minimal workflow

1. Read the request and named sources.
2. Inspect only the relevant repository areas and existing target artifact.
3. State evidence, assumptions, and any genuinely blocking question.
4. Produce the answer or requested artifact using the closest template.
5. Check internal consistency and report what remains undecided.

`sa-config.yaml` is optional. When present, honour `docs-root`, `language`, `diagram`, and contract versions. When absent, use the repository's existing conventions or default to:

```yaml
mode: brief
language: en
docs-root: docs/architecture
diagram: plantuml
contracts:
  sync: openapi-3.1
  async: asyncapi-2.6
```

## Non-negotiable quality rules

- Do not invent facts. Label unsupported claims as assumptions.
- Cite repository evidence for claims about the current system.
- Make scope explicit, including what is out.
- Use measurable drivers where numbers affect the design.
- Compare at least two credible options before a consequential recommendation.
- State negative consequences and reversibility.
- Give every boundary a direction, purpose, owner, and failure behaviour.
- Give every shared data entity one authoritative owner.
- Cover security, resilience, observability, cost direction, and delivery impact proportionally.
- Preserve existing conventions and untouched content on update.

## Writing policy

Writing a requested architecture artifact is normal work and does not require a separate ceremony. Before writing, state the intended files briefly. Ask for confirmation only when replacing an accepted decision, deleting content, or when a materially ambiguous multi-file change cannot be resolved from context.

Write under `docs-root` when configured. Otherwise follow the repository's existing documentation layout. Never modify application code, tests, CI, or agent instructions as part of an SA documentation task.

## Targeted references

Load only what the current artifact needs:

| Task | Standard | Template |
|---|---|---|
| Architecture brief | this file | `templates/architecture-brief.md` |
| ADR | `standards/adr.md` | `templates/adr.md` |
| HLD | `standards/hld.md`, plus `standards/diagrams.md` or `standards/deployment-view.md` when relevant | `templates/hld-catalogue.md` |
| Runtime flow | `standards/runtime-flow.md`, `standards/diagrams.md` | `templates/flow-narrative.md` |
| Interface | `standards/interface.md` | `templates/openapi.yaml` or `asyncapi.yaml` |
| Data | `standards/data.md` | `templates/data-design.md`; migration only when needed |
| Review | `standards/review.md` | `templates/design-review.md` |

Diagram conventions, deployment guidance, and migration templates are optional references. Do not load them unless the selected artifact needs them.
