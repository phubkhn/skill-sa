# Data Architecture

Use data architecture to settle cross-boundary ownership, lifecycle, consistency, and migration. Physical schema and query tuning belong to implementation unless they change an architecture driver or public contract.

## Required content

- conceptual entities and relationships
- one authoritative owner and write path per entity
- sensitive-attribute classification
- lifecycle, retention, deletion, and legal basis
- cross-boundary consistency and reconciliation mechanism
- identifiers exposed across boundaries
- volume and growth where structurally relevant
- analytics path and freshness where relevant

## Migration

When existing data changes, state the strategy, ordered steps, validation, rollback, point of no return, coexistence source of truth, conflict handling, cleanup owner, and end date.

## Checklist

- [ ] Domain vocabulary is consistent
- [ ] Every entity has one authoritative owner
- [ ] Multi-writer behaviour is an explicit decision
- [ ] Sensitive attributes are classified
- [ ] Retention and deletion are decided
- [ ] Cross-boundary consistency has a mechanism
- [ ] Relevant volume assumptions have sources
- [ ] Migration is reversible or its point of no return is explicit
- [ ] Coexistence has one source of truth and an end date
