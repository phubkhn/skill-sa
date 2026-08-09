# Standard 01 — Universal Workflow Protocol

Every generating `/sa:*` command executes these nine phases in order. Command files describe only what is *specific* to them; this file is the contract for everything else.

## P1 — Resolve arguments

- Parse arguments. If a required argument is missing: infer from session context; if still unknown, list the valid values found on disk and ask. Never guess a component or feature name.
- Normalise names per `standards/19-naming-and-structure.md` (kebab-case, no spaces).

## P2 — Load standards

- Read `sa-config.yaml`. Read this file. Read the step standard declared by the command.
- Read `checklists/<step>.md` — you will self-assess against it in P9.

## P3 — Load inputs

- Read every declared input artifact. For each missing input, emit one line: `MISSING INPUT: <path> — <what it would have told me> — proceeding with: <fallback>`.
- Read the log (`_logs/.design-log`) and pick up `trace-id`, `change-type`, `cr-ref` from the most recent relevant entry.

## P4 — Detect mode

| Mode | Condition | Version rule |
|---|---|---|
| `Initial` | target artifact does not exist | v1 / 1.0 / 1.0.0 per artifact type |
| `Update` | target exists, content changes | increment per artifact type |
| `No-op` | target exists and already reflects inputs | do not rewrite; report and stop |

In `Update` mode, compute the delta from the artifact's own changelog first; only fall back to `git log`/`git diff` when the changelog is absent or stale. Prefer one `git log -1 --format=%H -- <path>` plus one `git diff` over multiple exploratory git calls.

## P5 — Gate check

If the command sits behind a gate (see `standards/00-sa-journey.md`), evaluate it now. On failure, print the gate name, the failing condition, and the command that fixes it. Ask whether to proceed anyway; if yes, record an accepted risk.

## P6 — Change Summary (mandatory output)

```
## Change Summary — <artifact>

**Understood as:**   1–2 sentences, in your own words, of what is being designed.
**Mode:**            Initial | Update | No-op        **Version:** <old> -> <new>
**Trace:**           trace-id | change-type | cr-ref
**Inputs used:**     path — what I took from it            (one line each)
**Inputs missing:**  path — impact of its absence           (one line each)
**Decisions I am about to encode:**  bullet list, each with the alternative I am rejecting
**Assumptions:**     bullet list, each marked (safe) or (risky — goes to risk register)
**Delta:**           what changes vs current artifact       (Update mode only)
**Downstream impact:** artifacts that become stale if this is written
**Open questions:**  numbered, each with who can answer it
```

## P7 — STOP

Do not write. Wait for explicit confirmation or correction. If the user corrects an assumption, regenerate the Change Summary before writing.

## P8 — Write

- Use the template in `templates/` for the artifact type. Preserve existing structure exactly; add content inside existing sections.
- Every artifact begins with the standard header block:

```
| Field | Value |
|---|---|
| Artifact | <type> |
| Version | <N> |
| Status | Draft \| In Review \| Accepted \| Superseded |
| Last Updated | YYYY-MM-DD |
| Updated By | <git config user.name> |
| Trace ID | <TR-...> |
| Change Type | Initial \| Update \| Change Request |
| CR Ref | <ref> \| none |
```

- Append (never overwrite) an entry to `_logs/.design-log`:

```
artifact: <path>
step: <journey step>
date: <YYYY-MM-DD>
author: <name>
version: <N>
mode: Initial | Update
change-type: Initial | Update | Change Request
cr-ref: <ref> | none
trace-id: <TR-...>
delta: <one line>
stale-downstream: <comma-separated paths> | none
```

## P9 — Report

```
Written:   <path> (v<N>)
Logged:    _logs/.design-log
Checklist: <n>/<m> passed  — list every failed item and why
Stale:     <downstream artifacts that now need re-running>
Next:      <exact next command>
```

Never report a checklist as passed without having evaluated each item.
