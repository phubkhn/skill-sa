# Standard 25 — Solution Options

**Artifact:** `01-analysis/solution-options.md`
**Purpose:** an ADR compares options *for one decision*. This compares options *for the whole solution*, before the shape is fixed and while the alternatives are still cheap to imagine.

Skipping this step is how a design ends up with twelve well-argued ADRs that collectively describe a solution nobody ever compared to anything.

## When it is required

- `full` profile: always.
- `standard` profile: whenever two or more credible whole-solution shapes exist.
- `light` profile: not required.

If only one shape is credible, write that down with the reason — that sentence is the artifact.

## Required content

| Section | Content |
|---|---|
| Decision to be made | the one question these options answer, in a sentence |
| Evaluation axes | the H/H drivers, plus cost, plus delivery risk — chosen and weighted **before** the options are described |
| Options | 2–4 whole-solution shapes, each described the same way |
| Comparison matrix | options × axes, with a reason per cell, not just a score |
| Cost comparison | build and 36-month run cost per option (Standard 23) |
| Risk comparison | the two or three risks that differ materially between options |
| Reversibility | how expensive each option is to abandon in 12 months |
| Recommendation | one option, with the axis that decided it |
| Consequent decisions | the ADRs that follow from the recommendation |
| What would change the answer | the fact that, if it turned out differently, would flip the recommendation |

## Option description format

Each option is described identically, or the comparison is rigged.

```
### Option <N> — <name>
**Shape:**            2–4 sentences, plus a sketch of the container view
**Key mechanism:**    the one technical idea that makes it work
**What it assumes:**  the assumptions this option depends on that the others do not
**Build cost:**       <range, with confidence>
**Run cost (36m):**   <range, with confidence>
**Time to first value:** <duration>
**Reversibility:**    easy | costly | one-way, and why
**Best case:**        what we get if the assumptions hold
**Worst case:**       what we are left with if they do not
```

## Comparison matrix

| Axis | Weight | Option A | Option B | Option C |
|---|---|---|---|---|
| QA-AVAIL-01 | H | | | |
| QA-PERF-01 | H | | | |
| Run cost (36m) | H | | | |
| Delivery risk | M | | | |
| Reversibility | M | | | |

Each cell holds a short reason. A matrix of bare scores hides the argument, which is the only part worth reading.

## Rules

1. **Axes are fixed before options are written.** Choosing the axes after you know the answer is how a preference becomes a "analysis".
2. **"Do nothing" and "extend what exists" are options** and are evaluated on the same axes. They are frequently the right answer and are almost never written down.
3. **Options must be genuinely different in shape.** Three variants of the same architecture is one option with three configurations — say so and compare the configurations inside a single option.
4. **No straw men.** Each option is described by someone arguing for it. If nobody can argue for an option, delete it rather than including it to make the count.
5. **Cost is an axis, always.** An options comparison with no cost row has not compared anything a sponsor cares about.
6. **State what would change the answer.** This is the most useful sentence in the document, and it is the one that gets reviewed when reality shifts.
7. **The recommendation names the deciding axis.** "On balance" is not a reason.
8. **This artifact does not decide.** It recommends; the ADRs decide, and they cite this document.

## Anti-patterns

- Options written after the decision, to justify it
- An option list where two entries differ only by vendor
- No cost, or cost only for the recommended option
- A recommendation with no stated deciding axis
- Options never revisited when the "what would change the answer" fact changes

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] The decision is stated as one question
- [ ] Evaluation axes chosen and weighted before options were described
- [ ] Axes include every H/H driver, cost, and delivery risk
- [ ] 2–4 options, genuinely different in shape
- [ ] "Do nothing" / "extend what exists" evaluated on the same axes
- [ ] Every option described in the identical format
- [ ] Every option has build cost and 36-month run cost with confidence
- [ ] Every option states its assumptions, best case and worst case
- [ ] Reversibility stated per option
- [ ] Comparison matrix cells carry reasons, not bare scores
- [ ] Recommendation names the deciding axis
- [ ] "What would change the answer" stated
- [ ] Consequent ADRs listed
- [ ] No straw-man options
