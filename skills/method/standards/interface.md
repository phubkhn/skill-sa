# Interface Contracts

Design contracts from named consumer outcomes. Do not expose internal storage vocabulary or create operations with no consumer.

## Synchronous contracts

Define resources and operations, authentication and scopes, request and response examples, consistent errors, limits, idempotency for non-safe operations, and versioning/deprecation policy.

## Asynchronous contracts

Define event meaning, envelope, producer, consumers, ordering and partitioning, delivery semantics, deduplication, retention, replay, schema compatibility, and poison-message handling.

## Change compatibility

Classify each change per consumer. Breaking changes require a migration path, parallel support where needed, sunset date, and named consumer readiness. Deprecate before removal.

## Checklist

- [ ] Every operation or event has a named consumer and outcome
- [ ] Authentication and authorisation are explicit
- [ ] Errors and limits are defined
- [ ] Idempotency or deduplication is defined where needed
- [ ] Examples make schemas usable
- [ ] Sensitive fields are justified
- [ ] Compatibility was assessed per consumer
- [ ] Breaking changes have a migration and sunset plan
- [ ] Document parses and local references resolve
