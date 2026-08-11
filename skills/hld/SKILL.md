---
name: hld
description: Create or update a focused high-level architecture view using C4-style context, container, component, or deployment diagrams. Use when the user asks for system architecture, components, dependencies, boundaries, deployment topology, or an HLD. For runtime sequence behaviour use sa:flow; for choosing the architecture use sa:architect or sa:adr.
allowed-tools: Read, Grep, Glob
---

# SA — High-level design

Create only the view needed to answer the user's structural question. Default to a container view; add context, component, or deployment views only when they clarify a real boundary. Follow `../method/SKILL.md` and `../method/standards/workflow.md`.

## Inputs

Read the architecture brief or equivalent requirements, relevant accepted ADRs, and existing diagrams. Do not require a full SA workspace.

## Method

1. Define the view's scope and audience.
2. Give every element one clear responsibility and owner.
3. Give every relationship a direction, purpose, protocol or mechanism, sync/async nature, and failure expectation.
4. Show external systems and trust boundaries relevant to the scope.
5. Check for cycles, excessive fan-out, chatty calls, shared-store coupling, orphan elements, and unjustified components.
6. Ensure the view agrees with accepted decisions; surface contradictions instead of silently choosing.
7. Add a compact catalogue only when relationship details would make the diagram unreadable.

Use `../method/standards/hld.md` and `../method/standards/diagrams.md`. Load `deployment-view.md` only for deployment topology. Default output is `docs/architecture/hld/<view>.puml`, following existing repository conventions where present.

Validate declared aliases, diagram boundaries, and element names. Report any structural concern and recommend `/sa:flow` only for scenarios whose runtime behaviour remains unclear.
