---
name: review
description: Run an evidence-based design review against standards and drivers, producing findings with severity and a mechanical verdict. Use when the user asks to review, audit, or sign off an architecture design. Not for reviewing source code or pull requests — this reviews architecture design artifacts under docs-root only.
allowed-tools: Read, Grep, Glob
disallowed-tools: Edit, NotebookEdit
context: fork
---

# SA — Gated, evidence-based review of the whole design

| | |
|---|---|
| Journey step | 15 — Review |
| Produces | 09-review/design-review-<YYYY-MM-DD>.md |
| Inputs | everything under docs/architecture |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/15-review-standard.md`, `../method/standards/20-quality-bar.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. This skill executes **P1–P5 and P8–P9 only** — it produces a judgement on artifacts that already exist, so there is no design to propose and no Change Summary to confirm.

**Checklist:** the `## Checklist` section of `../method/standards/15-review-standard.md` — self-assess item by item in P9.

## When to use

- "review the architecture", "is this design ready to build", "sign off the design"
- Before handoff — G4 reads this verdict
- After a significant redesign, to find what the change broke

## When not to use

| Request | Use instead |
|---|---|
| review source code or a pull request | not this skill set at all |
| "what will this change break?" | `sa:impact` — forward-looking, before the design exists |
| "what could go wrong?" | `sa:risk` — sweeps and assigns owners; review judges and finds |
| "threat-model this" | `sa:security` — review checks that security was done, it does not do it |
| fix the problems found | the skill that owns the artifact; this one never edits a design |

---

**This skill does not modify any design artifact** — it only writes the review report. `disallowed-tools` enforces that for edits rather than merely asserting it.

**Fresh context is a requirement, not a preference.** `context: fork` runs this review in a subagent that has not watched the design being made. A reviewer present for every decision has already accepted every assumption behind it, and will confirm rather than examine. If the fork is unavailable, run the review in a new session — and if it is being run in the same session that produced the artifacts, say so in the report's "Not reviewed" section, because the finding set is weaker than it looks.

Read from the artifacts on disk, never from memory of writing them. Where the two disagree, the disk is right and the memory is the thing under review.

Arguments: $ARGUMENTS — scope, optionally `--dimension <n>` to review one dimension only (record the scope limit in the report).

**Method:**

1. **Read the profile first** from `sa-config.yaml` and apply `../method/standards/21-tailoring.md`. Artifacts the profile does not require are **not** findings — they go in the "Not required at this profile" section. Record the profile in the report header.
2. **Artifact inventory:** read **headers first** for everything required at this profile — path, version, status, trace-id — then open in full only what a check actually reasons over (Standard 26 §6). On a large initiative, reading every artifact in full degrades the review rather than deepening it. Record which artifacts were read in full and which by header only; that distinction belongs in "Not reviewed". Missing or `Draft` artifacts are recorded before any judgement is made.
3. **Quality bar pass:** evaluate each artifact against `../method/standards/20-quality-bar.md` — universal items plus its per-artifact items. Header block satisfies U1 in any of the four equivalent formats (Standard 01). Explicit pass/fail per item; no silent passes.
4. **Consistency matrix:** run **all 19** mechanical checks in Standard 15 and report result plus detail for each, passes included. Two deserve particular attention because nothing else catches them: **seed/authority conflicts** under the two-pass rule (Standard 00), and **stale artifacts** under the propagation table (Standard 17).
5. **Driver coverage:** for each driver, state whether the design satisfies it, **by what mechanism**, with evidence (file + location), and your confidence. A driver satisfied "by design" with no named mechanism is a Blocker.
6. **Dimension review:** walk all 15 dimensions in Standard 15. For dimension 11, count the simplicity signals and require a justification for each breach rather than asserting an opinion.
7. **Findings:** each with severity, dimension, evidence (`path:line`), the standard or driver violated, a recommendation, and an owner. No evidence → it is an Observation, not a Finding.
8. **Verdict, computed mechanically:** any Blocker → `NOT READY`. No Blocker but ≥1 Major → `READY WITH CONDITIONS` (list conditions with owner and by-when). Otherwise → `READY`.
9. **What is good** — state it explicitly.
10. **Not required at this profile** — list the excluded artifacts so their absence is understood.
11. **Not reviewed** — state the scope limits. An unstated limit reads as approval.

**P8:** `../method/templates/design-review.md`.

**P9:** report the verdict, blocker count, and the exact skill invocation that fixes each blocker. If `READY`, `Next: sa:handoff <scope>`.
