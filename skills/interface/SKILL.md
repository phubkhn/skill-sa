---
name: interface
description: Design synchronous (OpenAPI) and asynchronous (AsyncAPI) contracts for a component, with consumers, error shapes, idempotency, versioning and compatibility classification. Use when the user asks for API design, an API spec, event contracts, or interface design.
---

# SA — Produce synchronous and asynchronous contracts for one component

| | |
|---|---|
| Journey step | 8 — Interfaces |
| Produces | 06-interfaces/<component>-api.yaml, 06-interfaces/<component>-events.yaml, 06-interfaces/schemas/* |
| Inputs | 05-lld/<component>.yaml, 04-flows/*, 07-data/*, existing specs |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/09-interface-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/09-interface-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

Arguments: $ARGUMENTS — `<component>` and optionally `sync|async|both` (default both).

**P3:** read the component's LLD (`provides` list is the authority on what operations exist), every flow that calls it (the consumer's real needs), the data model (schema fields, sensitivity), and existing specs for update mode.

**Method:**

1. **Name the consumers first.** For each provided operation, list who calls it and what they do with the result. An operation with no named consumer is not built — challenge it.
2. Map every operation back to an LLD responsibility. Orphans in either direction are a defect; report, don't silently reconcile.
3. **Sync spec:** resources as plural nouns, verbs only in methods; full status-code set; one consistent error shape (`code`, `message`, `details`, `traceId`); pagination strategy with limits; auth scheme + required scopes per operation; rate limits and their response; idempotency mechanism on every non-safe operation; payload size limits; ≥1 example per request and response.
4. **Async spec:** `<entity>.<past-tense-verb>` names; the standard envelope; message kind (notification / state transfer / command); ordering guarantee + partition key; delivery semantics + consumer dedup requirement; retention and replay; DLQ and poison-message procedure; schema compatibility mode; named consumers and their action on receipt.
5. **Compatibility classification** for every change in update mode: PATCH / MINOR / MAJOR, judged against each named consumer. A MAJOR change requires a migration plan per consumer before it is written.
6. Never delete an operation — mark `deprecated: true` with a sunset date and the replacement.
7. Check vocabulary: no field name meaning two things across specs; no internal/storage vocabulary leaking into the contract.
8. Mark sensitive fields and justify their presence.

**P6 Change Summary must list** the consumer table and, in update mode, the compatibility classification per change.

**P8:** `../method/templates/openapi.yaml` / `../method/templates/asyncapi.yaml`. Validate the document parses and every `$ref` resolves before reporting success.

**P9:** report operation↔responsibility coverage and breaking changes, then `Next: /sa:gen-data-design` or `/sa:review-design`.
