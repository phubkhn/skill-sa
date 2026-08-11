---
name: interface
description: Design or review a synchronous API or asynchronous event contract with named consumers, errors, authentication, idempotency, compatibility, and migration impact. Use when the user asks for OpenAPI, AsyncAPI, API design, event schemas, or a cross-system interface. Not for implementing handlers or client code.
allowed-tools: Read, Grep, Glob
---

# SA — Interface contract

Design a contract from consumer needs and architecture boundaries, not from an internal class or database schema. Follow `../method/SKILL.md` and `../method/standards/workflow.md`.

## Inputs

Read the architecture brief, relevant flow, data vocabulary, named consumers, and existing specs.

## Method

1. Name every consumer and the outcome it needs.
2. Define only operations or events with a real consumer.
3. Specify authentication and authorisation, consistent errors, limits, idempotency, and examples.
4. For events, define the envelope, meaning, ordering, partitioning, delivery semantics, retention, replay, and consumer deduplication.
5. Mark sensitive fields and justify crossing the boundary.
6. In update mode, classify compatibility per consumer. A breaking change needs a migration and sunset plan before removal.
7. Keep public vocabulary stable and independent of storage details.

Use `../method/standards/interface.md` and the OpenAPI or AsyncAPI template in `../method/templates/`. Default output is `docs/architecture/interfaces/<name>.yaml`, following existing repository conventions where present.

Validate YAML, required fields, examples, and local `$ref` targets. Report breaking changes and affected consumers explicitly.
