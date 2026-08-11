# Operating Guardrails

These guardrails protect evidence and scope without turning documentation into ceremony.

1. **Stay in scope.** SA skills create architecture advice and documentation; they do not modify source code, tests, CI, infrastructure, or agent instructions.
2. **Use evidence.** Cite current-system sources. Label anything unsupported as an assumption.
3. **Keep writes visible.** State intended files before writing and report actual files afterwards.
4. **Confirm consequential replacement.** Ask before superseding an accepted decision, deleting content, or making an ambiguous multi-file change. Ordinary requested document creation needs no extra stop.
5. **Preserve updates.** Change only sections affected by new evidence or decisions.
6. **Minimise context.** Read the target artifact and the few upstream sources needed to reason about it; do not load the entire standards library or documentation tree.
7. **Bound recovery.** If a required fact is missing, make one clearly labelled assumption when safe; otherwise state what is missing and who can answer it.
8. **Review independently.** A review reads artifacts from disk and does not edit the design it judges.

Tool permissions are a runtime property, not a substitute for these rules. Keep broad shell access unapproved by default and use deterministic validation tools when available.
