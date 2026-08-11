---
name: data
description: Create or review architecture-level data ownership, conceptual models, classification, lifecycle, consistency, and migration plans. Use when data crosses component boundaries, ownership or retention is unclear, or an existing store must migrate. Not for SQL, physical schema tuning, query optimisation, or dataset analysis.
allowed-tools: Read, Grep, Glob
---

# SA — Data architecture

Focus on decisions that cross system or team boundaries. Leave physical schema and query implementation to the delivery team unless they change a public contract or a key architecture driver. Follow `../method/SKILL.md` and `../method/standards/workflow.md`.

## Inputs

Read the architecture brief, HLD, significant flows, existing contracts, and current data documentation.

## Method

1. Define the conceptual entities and relationships using domain vocabulary.
2. Assign one authoritative owner and write path per entity; raise multi-writer conflicts as decisions.
3. Classify sensitive attributes and state regulatory constraints.
4. State lifecycle, retention, deletion, legal basis, and analytics freshness.
5. Define cross-boundary consistency and the mechanism that maintains or reconciles it.
6. Record volumes and growth only when they influence the design, citing the source.
7. When existing data changes, provide reversible migration steps, validation, rollback, coexistence ownership, and an end date.

Use `../method/standards/data.md` and `../method/templates/data-design.md`. Add `migration-plan.md` only when existing data must move or change shape. Default output is under `docs/architecture/data/`.

Report ownership conflicts, missing retention decisions, and irreversible migration steps.
