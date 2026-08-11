---
name: adr
description: Create or update an Architecture Decision Record for one consequential, contested, cross-cutting, or expensive-to-reverse choice. Use when the user asks for an ADR, wants to preserve why an option was chosen, or needs to supersede an earlier architecture decision. For broad solution exploration or general design, use sa:architect.
allowed-tools: Read, Grep, Glob
---

# SA — Architecture Decision Record

Record one decision so a future reader can understand the forces, credible alternatives, choice, and consequences. Follow `../method/SKILL.md` and `../method/standards/workflow.md`.

## Inputs

Read the architecture brief or relevant requirements, the affected design, and existing ADRs. `sa-config.yaml` is optional. If the decision basis is unclear, ask only for the missing fact that could change the choice.

## Method

1. Phrase the decision as one question. Split it if it contains independent choices.
2. Identify the measurable drivers and constraints that decide it.
3. Compare at least two credible options, including keeping the current design when credible.
4. State the decision in one active sentence.
5. Record positive and negative consequences, reversibility, and what would trigger reconsideration.
6. Define a concrete compliance check.
7. Use `Proposed` unless the authorised deciders have agreed; do not infer acceptance.

Write `docs/architecture/decisions/ADR-NNNN-<slug>.md` by default, adapting the repository's existing ADR location and numbering when present. Use `../method/templates/adr.md` and the quality rules in `../method/standards/adr.md`.

Before superseding an accepted ADR, state the old and new files and ask for confirmation. Ordinary new ADR creation needs no extra confirmation.

Report the deciding trade-off, unresolved evidence, and whether an HLD or interface now needs updating.
