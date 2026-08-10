---
name: trace
description: Build and query the end-to-end traceability index: what one decision touched, orphan artifacts, stale artifacts, and driver coverage. Use when the user asks why a design element exists, what a change affected, or what is now out of date. Not for distributed tracing, OpenTelemetry, or runtime request traces — that is the observability skill.
allowed-tools: Read, Grep, Glob
disallowed-tools: Edit, NotebookEdit
---

# SA — Build and query the end-to-end traceability index

| | |
|---|---|
| Journey step | 17 — Trace |
| Produces | _logs/.trace-index.md (regenerated), report to the conversation |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/17-traceability-and-change.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. This skill executes **P1–P5 and P8–P9 only** — it derives the index mechanically from existing headers and the design log, so there is nothing to propose and no Change Summary to confirm. It writes no design artifact.

## When to use

- "why does this component exist", "what did decision X touch", "what's now out of date"
- Before trusting any artifact set you did not just write — `--stale` first
- Publishing the trace index after a handoff

## When not to use

| Request | Use instead |
|---|---|
| distributed tracing, OpenTelemetry, request traces | `sa:observability` — this traces *design*, not runtime |
| "why did we choose X" | `sa:adr` — trace follows the id, the ADR holds the reasoning |
| "what will this change break" | `sa:impact` — forward-looking prediction |
| regenerate the stale artifacts | the owning skill — staleness is the architect's call, never automatic |

---

Arguments: $ARGUMENTS — one of:
- `<scope>` — rebuild the trace index for a scope (default)
- `<TR-scope-NNN>` — show everything one decision touched
- `--orphans` — artifacts with no trace-id, or trace-ids with no origin
- `--stale` — artifacts whose upstream changed after they were last written
- `--coverage` — drivers with no artifact, and artifacts with no driver

Steps:

1. Read `sa-config.yaml` for `docs-root` and `trace-prefix`.
2. Scan every artifact header for trace ids, change types, refs, versions and dates — accepting **all four header formats** (markdown table, PlantUML comment, OpenAPI/AsyncAPI `x-` fields, LLD YAML keys; see Standard 01). Parse `_logs/.design-log` as a YAML list.
3. **Rebuild `_logs/.trace-index.md`** from `../method/templates/trace-index.md` — one row per trace-id: origin, type, date, artifacts touched (path + version), status. Sort by trace-id. This file is the authority for the highest allocated trace-id.
4. **`<TR-...>` mode:** run `grep -rn "<TR-...>" <docs-root>` and present the results grouped by journey step, in dependency order, so the reader sees the decision propagate from driver to handoff.
5. **`--orphans`:** report (a) artifacts with no trace-id in their header, (b) trace-ids appearing in artifacts but never in an origin record. Both are traceability defects; state which artifact and what to add.
6. **`--stale`:** using the staleness table in Standard 17, compare each artifact's last-write date/version against its upstreams'. Report every artifact whose upstream moved after it did, with the skill that refreshes it. Also report **seed/authority conflicts** under the two-pass rule (Standard 00) — a seed can be stale even when neither file has changed since. **Do not regenerate anything** — staleness is the SA's call.
7. **`--coverage`:** cross-reference `00-context/architecture-drivers.md` against all artifacts. Report drivers addressed nowhere (a design gap) and design elements addressing no driver (possible over-engineering).

This command never writes to any artifact other than `_logs/.trace-index.md`.
