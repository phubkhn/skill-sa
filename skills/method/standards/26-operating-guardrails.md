# Standard 26 — Operating Guardrails

Standards 00–25 describe *what to design*. This one describes *how this skill set must behave while designing it*.

The distinction matters because everything in the other standards is a prompt rule, and a prompt rule is an instruction, not an enforcement. An instruction is followed by a cooperative model on a good day. This standard says which rules must be backed by something stronger, and what "stronger" means here.

> Prompt rule = instruction. Runtime gate = enforcement. Where the two disagree, the runtime gate wins, and the design is safe only to the extent the gate exists.

## 1. The tool-call boundary

The moment a skill stops proposing and starts writing is the only irreversible moment in the journey. Everything before it is text; everything after it is a file on someone's disk, in someone's git history, cited by someone's implementation.

That boundary is **P7 STOP**. Its integrity is the single most important property of this skill set.

| Before P7 | After P7 |
|---|---|
| a proposal | a real change |
| costs nothing to correct | costs a commit, a review, and possibly a stale downstream chain |
| the user can redirect with one sentence | the user must ask for an Update run |

Rules:

1. **No write of any kind before the user confirms the Change Summary.** Not a "quick scaffold", not an empty file, not a `.gitkeep`. `sa:init` is the sole exception and it writes only structure, never content.
2. **The Change Summary declares the exact file list.** See §2 — a plan that does not name its files cannot be checked against what actually happened.
3. **Correction reopens the plan.** If the user corrects an assumption, regenerate the Change Summary and stop again. Do not carry a corrected assumption straight into a write.
4. **Silence is not confirmation.** Neither is "ok", "sounds good", or a question about something else, if the file list has changed since it was shown.

## 2. Scope declaration (plan validation)

The Change Summary in P6 must include an explicit, checkable list:

```
**Files I will write:**
  <path> — Initial | Update — <one line: what goes in it>
  <path> — Initial | Update — <...>
**Files I will NOT touch, though you might expect me to:**
  <path> — <why not>
```

This costs two lines and catches the failure mode that no downstream check catches: writing the right content into the wrong place, or quietly touching four artifacts when the user authorised one.

After writing, P9 reports the files actually written. **If that list differs from the declared list, say so explicitly** and explain the difference. An undeclared write is a scope violation even when its content is correct.

## 3. Path boundary

Every write goes under `<docs-root>` from `sa-config.yaml`, plus `sa-config.yaml` itself. Nothing else, ever.

| Location | Permitted |
|---|---|
| `<docs-root>/**` | yes — this is the skill set's whole surface |
| `sa-config.yaml` at repo root | `sa:init` only |
| source code, tests, CI config, `CLAUDE.md`, `AGENTS.md` | **no** — not even to fix something obviously broken |
| anything above the repository root | **no** |

Resolve paths before checking them. `<docs-root>/../../etc/` is outside `<docs-root>` however it is spelled, and a scope slug taken from user input can contain `..`.

If a design problem genuinely requires a change outside `<docs-root>` — a fitness function in CI, say — **describe it in the handoff as work for the team**. Do not implement it.

## 4. Tool permissions

Two frontmatter fields that are easy to confuse, and confusing them inverts the safety property:

| Field | What it does |
|---|---|
| `allowed-tools` | **Pre-approves** tools so they run without a permission prompt. It grants; it never restricts. |
| `disallowed-tools` | **Removes** tools from the pool while the skill is active. This is the one that restricts. |

Consequences for this skill set:

1. **`allowed-tools` lists reads only** — `Read, Grep, Glob`. Writing an artifact is the irreversible act; it goes through the normal permission prompt as a second gate behind P7. Pre-approving `Write`, `Edit` or `Bash` would remove that gate for the whole turn.
2. **`Bash` is never pre-approved.** A blanket bash grant is an unrestricted shell, which is the widest possible action surface for the narrowest possible benefit. Where a skill genuinely needs a command — `git log` for an Update delta, a PlantUML render check, a spec parse — it asks, and the user sees what it is about to run.
3. **`sa:review` and `sa:trace` set `disallowed-tools: Edit, NotebookEdit`.** Both are read-and-report skills; the review writes one report and the trace writes one index, and neither has any business editing a design artifact. Previously this was only asserted in prose, which enforced nothing.
4. **Least privilege beats a longer rule list.** If a skill cannot reach a file, no instruction about not touching it is needed.

## 5. Verification must be independent

A skill that self-assesses against its own checklist is grading its own homework, and it will pass. The checklists in standards 02–25 are useful — they catch omissions — but they are not verification, because the same reasoning that produced the artifact evaluates it.

Therefore:

1. **`sa:review` should run with fresh context.** Set `context: fork` on the review skill, or run it in a separate session. A reviewer that has been present for every design decision has already accepted every assumption behind them.
2. **The author does not review.** Where a person is involved, the reviewer named in the report is not the author named in the artifacts.
3. **Checklist self-assessment is reported as what it is** — a completeness check, not a correctness check. P9 says `Checklist: n/m` and never says "verified".
4. **The real verification of a design is Standard 24** — a numeric threshold, an environment, a tool, and a fitness function. Everything before that is review.

## 6. Context is a handoff, not a dump

Several skills declare "everything under `<docs-root>`" as their input — `sa:risk`, `sa:review`, `sa:trace`. On a real initiative that is more than fits usefully in one context, and reading it all indiscriminately degrades the output rather than improving it.

| Load | Do not load |
|---|---|
| the artifact headers (status, version, trace-id) for everything | full body of every artifact |
| the full body of artifacts this step actually reasons over | superseded artifacts, unless tracing supersession |
| the specific rows or sections a check needs | whole spec files when one operation is in question |
| the design log tail | the entire design log history |

For a sweep skill, read headers first, then open only what the sweep flags. Say in P9 which artifacts were read in full and which only by header — a review that skimmed is still useful, but only if it says so, and this belongs in the "Not reviewed" section.

**State outlives context.** Anything that must survive to the next run goes in `_logs/.design-log` or the artifact itself — never in the assumption that the next session remembers this one.

## 7. Bounded recovery

When a skill cannot complete — a missing input, a failing gate, a template that does not fit, a contradiction between two artifacts — the failure mode to avoid is retrying with a slightly different guess.

```
attempt
  ↓ fails
state precisely what failed and why
  ↓
one corrective attempt, if the correction is known
  ↓ fails again
STOP and escalate to the user
```

1. **At most one automatic retry**, and only when the correction is known rather than guessed.
2. **Never lower the bar to pass.** Do not drop a checklist item, weaken a threshold, remove a required section, or reclassify a Blocker as an Observation so a run can complete. This is the most likely way this skill set produces something worse than nothing.
3. **Never fabricate an input to get unblocked.** A missing measure is an OPEN item with an owner; an invented one is a number that will be designed against.
4. **Escalation names three things:** what is missing, who owns it, and the assumption that would otherwise have to be made.

## 8. Failure log

When this skill set produces a bad artifact, the fix is not a better prompt for next time — it is a rule that makes the failure impossible or visible.

Record it in `_logs/.failure-log`:

```yaml
- date: <YYYY-MM-DD>
  skill: <skill name>
  what-went-wrong: <one line>
  why-it-was-not-caught: <which gate, checklist item or standard should have caught it>
  guardrail-added: <the standard, checklist item, or gate condition added — or "none yet">
```

An entry with `guardrail-added: none yet` is a known hole; a review may cite it. The log is small, append-only, and worth more than any amount of re-prompting, because it is the only artifact that records how this method actually fails rather than how it is supposed to work.

## Checklist

Self-assess against this list on every run, before P8. Report pass/fail per item.

- [ ] No file written before the user confirmed the Change Summary
- [ ] Change Summary declared the exact file list, including files deliberately not touched
- [ ] Files actually written match the declared list, or the difference is reported
- [ ] Every write is under `<docs-root>` (or is `sa-config.yaml` from `sa:init`)
- [ ] Paths resolved before the boundary check; no traversal outside the root
- [ ] No source code, test, CI or agent-instruction file touched
- [ ] Checklist results reported as completeness, not as verification
- [ ] Sweep skills stated which artifacts were read in full and which by header only
- [ ] No more than one automatic retry; no requirement weakened to make a run pass
- [ ] No fabricated input used to get unblocked
- [ ] Any failure of this skill set recorded in `_logs/.failure-log` with the guardrail it implies
