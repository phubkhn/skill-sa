# Lightweight Workflow

Use this workflow for every core skill.

## 1. Understand

- Resolve the requested outcome from the conversation before asking for arguments.
- Read sources named by the user and the repository files directly relevant to the claim or artifact.
- If `sa-config.yaml` exists, honour it. If absent, continue with repository conventions or the defaults in `../SKILL.md`.
- Separate evidence, assumptions, and open questions.

## 2. Scope

Choose the smallest output that answers the request:

- conversation answer
- one architecture brief
- one explicitly requested specialised artifact
- a small, named set of files when their relationship makes separate delivery necessary

Ask no more than three questions at once, and only when the answer changes a boundary, a consequential decision, or a public contract. Otherwise make a labelled assumption and proceed.

## 3. Produce

- State the intended output and files in a short paragraph.
- Use the closest template, adapting it to the problem rather than filling irrelevant sections.
- Preserve untouched content when updating an existing artifact.
- Use `OPEN — owner: <name or role>` when a missing fact matters; never invent it.

Explicit confirmation is required only before:

- replacing or superseding an accepted decision
- deleting existing content
- writing a materially ambiguous multi-file change

## 4. Check and report

Check the relevant standard's checklist, but report only failed or not-applicable items unless the user asks for the full matrix.

Report:

```text
Created/updated: <paths, or none>
Key decision: <one sentence>
Assumptions/open items: <short list>
Next: <one justified core skill, or none>
```

## Evidence and naming

- Cite a file, document, or named source for claims about the current system.
- Use stable names consistently across diagrams, flows, contracts, and data designs.
- Prefer section references over brittle line numbers in long-lived architecture documents.
- Use the user's language for prose and English identifiers when the project has no contrary convention.
