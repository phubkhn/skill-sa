# Standard 09 — Interface & Contract Design

**Artifacts:** `06-interfaces/<component>-api.yaml` (OpenAPI 3.x), `<component>-events.yaml` (AsyncAPI 2.x), `schemas/`
**Purpose:** the contract is the architecture's load-bearing surface. Everything else can be refactored; contracts cannot.

## Universal contract rules

1. **Design the contract before the implementation.** The contract is an agreement, not an export of the code.
2. **Contracts are consumer-driven.** Name every known consumer and what it needs. An interface with no named consumer should not be built.
3. **Backward compatibility is the default.** Additive changes only; breaking changes require a new major version *and* a migration plan for every consumer.
4. **Explicit versioning strategy**, stated in the spec: URI version, header, or content negotiation for sync; schema version field for events.
5. **Never delete — deprecate.** Mark `deprecated: true`, state the sunset date and the replacement.
6. **Errors are part of the contract.** A consumer must be able to handle every failure without reading your code.
7. **Idempotency is stated for every non-safe operation**, with the mechanism (key header, natural key, dedup window).
8. **No leaking internals.** Contract vocabulary is the domain's, not the database's.

## Synchronous (HTTP/REST) requirements

| Aspect | Requirement |
|---|---|
| Resources | plural nouns; verbs only in the method |
| Status codes | success + `400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`, `503` where applicable |
| Error body | one consistent shape across all endpoints: `code`, `message`, `details`, `traceId` |
| Pagination | stated strategy (cursor preferred) with limits and defaults |
| Filtering/sorting | explicit allowed fields, not free-form |
| Auth | scheme, scopes/permissions per operation |
| Rate limits | documented, with the response shape when exceeded |
| Timeouts | server-side max processing time documented |
| Idempotency | `Idempotency-Key` (or equivalent) on POST/PATCH where retry is possible |
| Payload limits | max request/response size |
| Examples | at least one request and one response example per operation |

## Asynchronous (events/messages) requirements

| Aspect | Requirement |
|---|---|
| Naming | `<entity>.<past-tense-verb>` — events describe facts that happened |
| Envelope | `eventId`, `eventType`, `version`, `occurredAt`, `producer`, `traceId`, `payload` |
| Payload | minimal + stable; state whether it is a notification, an event-carried state transfer, or a command |
| Ordering | guarantee stated (none / per-key / global) and the partition key named |
| Delivery | at-least-once / at-most-once / exactly-once — and consumer dedup requirement |
| Retention | how long the topic keeps messages; replay policy |
| Poison handling | DLQ/retry topic named, with the operational procedure |
| Schema evolution | compatibility mode (backward/forward/full) stated |
| Consumers | named, with what each does on receipt |

## Other interface kinds

- **Batch/file:** format, encoding, delimiter, schema, naming convention, arrival window, late/duplicate file handling, checksum.
- **Scheduled jobs:** cadence, overlap policy, missed-run policy, max runtime, idempotency.
- **UI/BFF:** aggregate shape per screen, over-fetch policy, caching.

## Contract review checklist

- [ ] Every operation traces to an LLD responsibility
- [ ] Every consumer's need is met without a follow-up call ("chatty" check)
- [ ] Every error a consumer must branch on is documented
- [ ] No field name means two different things across specs
- [ ] Sensitive fields marked and justified
- [ ] Compatibility impact classified for every change

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Every operation has ≥1 named consumer and a stated need
- [ ] Every operation maps to an LLD responsibility
- [ ] Error responses defined for every operation a consumer must branch on
- [ ] One consistent error shape across the whole spec
- [ ] Auth scheme and per-operation permissions stated
- [ ] Idempotency mechanism stated for every non-safe operation
- [ ] Pagination, filtering, sorting constrained and documented
- [ ] Rate limits and their response documented
- [ ] Payload size limits stated
- [ ] ≥1 example per request and response schema
- [ ] Versioning strategy and compatibility mode stated
- [ ] Events named `<entity>.<past-tense-verb>` with the standard envelope
- [ ] Ordering guarantee, partition key, delivery semantics, dedup requirement stated
- [ ] Retention, replay, and DLQ/poison procedure stated
- [ ] Change compatibility classified per consumer (PATCH/MINOR/MAJOR)
- [ ] Nothing deleted — deprecations carry a sunset date and a replacement
- [ ] No field name means two things; no storage vocabulary leaks into the contract
- [ ] Sensitive fields marked and justified
- [ ] Document parses; every `$ref` resolves
