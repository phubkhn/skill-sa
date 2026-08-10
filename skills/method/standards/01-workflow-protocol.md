# Standard 01 — Universal Workflow Protocol

Every generating `sa:*` skill executes these nine phases in order. Skill files describe only what is *specific* to them; this file is the contract for everything else.

## P1 — Resolve arguments

- Parse arguments. If a required argument is missing: infer from session context; if still unknown, list the valid values found on disk and ask. Never guess a component or feature name.
- Normalise names per `19-naming-and-structure.md` (kebab-case, no spaces).

## P2 — Load standards and configuration

- Read `sa-config.yaml` at the repository root. If absent, stop and tell the user to run `sa:init`.
- Read `../SKILL.md` (the method hub), this file, `26-operating-guardrails.md`, and **every standard listed in the skill's metadata table** — most skills declare two to four, and the extra ones are not optional background.
- The skill's **primary standard** is the first one listed that is not `01`; its `## Checklist` is the one you self-assess against item by item in P9. There is no separate `checklists/` directory; each checklist lives at the end of its standard.
- Where a skill declares several standards, later ones supply specific sections (diagram conventions, deployment view, verification) rather than a second checklist.

### Honouring `sa-config.yaml` (mandatory)

| Key | Effect on this run |
|---|---|
| `docs-root` | **every path in this skill set is relative to this value.** `docs/architecture/` is only the default, never a constant. |
| `profile` | `light` \| `standard` \| `full` — see `21-tailoring.md`. If this step is not required by the active profile, say so and ask whether to run it anyway before proceeding. |
| `steps-enabled` | if this step is absent from the list, refuse to run and name the config line that excludes it. |
| `gates` | a gate set to `false` is skipped — **and skipping writes an accepted risk** naming who configured it off. |
| `contracts.sync` / `contracts.async` | use exactly these spec versions when generating interface artifacts. |
| `diagram` | use this diagram syntax. If it is not `plantuml`, state that Standard 18 only covers PlantUML and ask before improvising. |
| `language` | write artifact prose in this language. **IDs, file names, element names, field names and enum values stay English kebab-case regardless of `language`.** |
| `trace-prefix` | prefix for trace ids (default `TR`). |

## P3 — Load inputs

- Read every declared input artifact. For each missing input, emit one line:
  `MISSING INPUT: <path> — <what it would have told me> — proceeding with: <fallback>`
- Read `_logs/.design-log` and pick up `trace-id`, `change-type`, `ref` from the most recent relevant entry.

**Evidence rule.** Every statement this skill makes about the *existing* system must carry a source: a `path:line`, a named document, or a named person plus the date they confirmed it. A statement with no available source is written as an **Assumption**, never as a fact. This applies most sharply to the baseline section of `sa:impact`, where an unsourced claim is indistinguishable from an invention.

## P4 — Detect mode

| Mode | Condition | Version rule |
|---|---|---|
| `Initial` | target artifact does not exist | v1 / 1.0 / 1.0.0 per artifact type |
| `Update` | target exists, content changes | increment per artifact type |
| `No-op` | target exists and already reflects inputs | do not rewrite, do not bump the version, **do not write a design-log entry** — nothing changed, so there is nothing to log. Report why it is a no-op and stop. |

In `Update` mode, compute the delta from the artifact's own changelog first; only fall back to `git log` / `git diff` when the changelog is absent or stale. Prefer one `git log -1 --format=%H -- <path>` plus one `git diff` over multiple exploratory git calls.

**Determinism.** Running the same skill twice against unchanged inputs must produce the same artifact. The only permitted difference between two runs is content derived from input that actually changed. Never re-word, re-order, or "improve" existing sections that no input touched — that is a silent, untraceable change.

## P5 — Gate check

If the skill sits behind a gate (see `00-sa-journey.md`), evaluate it now. On failure, print the gate name, the failing condition, and the skill that fixes it. Ask whether to proceed anyway; if yes, record an accepted risk naming the person who overrode it.

## P6 — Change Summary (mandatory output)

```
## Change Summary — <artifact>

**Understood as:**   1–2 sentences, in your own words, of what is being designed.
**Mode:**            Initial | Update | No-op        **Version:** <old> -> <new>
**Trace:**           trace-id | change-type | ref
**Profile:**         light | standard | full          **Gates evaluated:** <G?: pass/fail/skipped>
**Inputs used:**     path — what I took from it            (one line each)
**Inputs missing:**  path — impact of its absence           (one line each)
**Files I will write:**
  path — Initial | Update — one line on what goes in it
**Files I will NOT touch, though you might expect me to:**
  path — why not
**Decisions I am about to encode:**  bullet list, each with the alternative I am rejecting
**Assumptions:**     bullet list, each marked (safe) or (risky — goes to risk register)
**Delta:**           what changes vs current artifact       (Update mode only)
**Downstream impact:** artifacts that become stale if this is written
**Open questions:**  numbered, each with who can answer it
```

## P7 — STOP

Do not write. Wait for explicit confirmation or correction. If the user corrects an assumption, regenerate the Change Summary before writing.

This is the tool-call boundary — the only irreversible moment in the journey. `26-operating-guardrails.md` governs it: no write of any kind before confirmation, silence is not confirmation, and a correction reopens the plan rather than passing through it.

## P8 — Write

- Use the template in `../templates/` for the artifact type. Preserve existing structure exactly; add content inside existing sections.
- Every artifact carries a header. **Four formats are equivalent** — use the one native to the file type; `sa:review` treats all four as satisfying quality-bar item U1.

### Header block equivalence

| Field | Markdown (table) | PlantUML (comment) | OpenAPI / AsyncAPI | LLD YAML (top-level key) |
|---|---|---|---|---|
| Artifact type | `Artifact` | `' Artifact:` | implied by file name | implied by file name |
| Version | `Version` | `' Version:` | `info.version` | `version` |
| Status | `Status` | `' Status:` | `info.x-status` | `status` |
| Last updated | `Last Updated` | `' Last updated:` | `info.x-last-updated` | `changelog[0].date` |
| Updated by | `Updated By` | `' Updated by:` | `info.x-updated-by` | `changelog[0].author` |
| Trace ID | `Trace ID` | `' Trace ID:` | `info.x-trace-id` | `trace-id` |
| Change type | `Change Type` | `' Change type:` | `info.x-change-type` | `changelog[0].change-type` |
| Ref | `Ref` | `' Ref:` | `info.x-ref` | `changelog[0].ref` |

Markdown form:

```
| Field | Value |
|---|---|
| Artifact | <type> |
| Version | <N> |
| Status | Draft \| In Review \| Accepted \| Superseded |
| Last Updated | YYYY-MM-DD |
| Updated By | <git config user.name> |
| Trace ID | <TR-...> |
| Change Type | Initial \| Update \| Change Request \| Corrective |
| Ref | <CR-... \| FINDING-... \| INC-...> \| none |
```

`Ref` is mandatory when `Change Type` is `Change Request` (a CR id) or `Corrective` (a review-finding or incident id). It is `none` for `Initial` and `Update`.

- Append (never overwrite) an entry to `_logs/.design-log`. The log is a **YAML list** so it can be parsed:

```yaml
- artifact: <path relative to docs-root>
  step: "<journey step, as in standard 00 — a number, or 3b for options>"
  date: <YYYY-MM-DD>
  author: <name>
  version: <N>
  mode: Initial | Update
  change-type: Initial | Update | Change Request | Corrective
  ref: <CR-... | FINDING-... | INC-...> | none
  trace-id: <TR-...>
  delta: <one line>
  stale-downstream: [<path>, <path>] | []
```

## P9 — Report

```
Written:   <path> (v<N>)   — and, if any file was not on the declared list, say which and why
Logged:    _logs/.design-log
Checklist: <n>/<m> passed  — completeness, not verification; list every failed item and why
Read:      in full: <paths>  |  header only: <paths>      (sweep skills only)
Stale:     <downstream artifacts that now need re-running>
Next:      <exact next skill, spelled as in standard 00>
```

Never report a checklist as passed without having evaluated each item, and never describe a passed checklist as "verified" — it is a completeness check against a list this same reasoning produced. Real verification is Standard 24.

On failure: at most one corrective attempt, then stop and escalate with what is missing, who owns it, and the assumption that would otherwise be required. Never weaken a requirement or fabricate an input to let a run finish (Standard 26 §7).
