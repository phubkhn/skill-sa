---
name: options
description: Compare two to four whole-solution options against weighted drivers, cost and reversibility, and recommend one before any ADR is written. Use when the user asks to compare approaches, evaluate alternatives, choose between architectures, or produce an options paper or trade-off study for a solution.
allowed-tools: Read, Grep, Glob
---

# SA — Compare whole-solution options and recommend one

| | |
|---|---|
| Journey step | 3b — Options |
| Produces | 01-analysis/solution-options.md |
| Inputs | 00-context/sa-intent.md, 00-context/architecture-drivers.md, 01-analysis/impact-analysis.md |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/25-options-standard.md`, `../method/standards/23-cost-standard.md` |

**Method contract:** read `../method/SKILL.md`, `../method/standards/01-workflow-protocol.md` and `../method/standards/26-operating-guardrails.md` before acting. All nine execution phases (P1–P9) are mandatory, as is the write boundary at P7.

**Checklist:** the `## Checklist` section of `../method/standards/25-options-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

Arguments: $ARGUMENTS — scope slug.

**P3:** read the intent (what problem, what is out of scope), the drivers (the H/H set becomes the evaluation axes), and the impact analysis (what already exists constrains which shapes are credible).

**Method:**

1. **State the decision as one question** before anything else. If it needs the word "and", it is two decisions — split it or hand the smaller one to `sa:adr`.
2. **Fix the evaluation axes and their weights now**, before describing any option: every H/H driver, plus run cost, plus delivery risk. Show these to the user and get agreement before proceeding — axes chosen after the options are known are not axes.
3. **Generate 2–4 genuinely different shapes.** Always include "do nothing" and "extend what already exists" where either is credible. Variants of the same architecture are one option, not three.
4. Describe every option in the **identical format** from Standard 25. Asymmetric description is the most common way an options paper lies.
5. **Cost every option** — build, and run at the 36-month volume from the data design or the intake's growth numbers. Label each figure measured / quoted / estimated. If no capacity basis exists, say so and mark the comparison cost-blind rather than inventing figures.
6. Fill the comparison matrix with **reasons, not scores**.
7. State **reversibility** per option: what abandoning it in 12 months would cost.
8. Recommend one option and **name the single axis that decided it**.
9. State **what would change the answer** — the fact whose reversal flips the recommendation.
10. List the **consequent ADRs** the recommendation implies. This artifact recommends; it does not decide.

**P6 Change Summary must include** the axes and their weights, and the option names — before any option is written up. This is the part worth arguing about.

**P8:** `../method/templates/solution-options.md`.

**P9:** report the recommendation, the deciding axis, the cost spread between options, and the list of consequent ADRs, then `Next: sa:adr <decision-slug>` for each.
