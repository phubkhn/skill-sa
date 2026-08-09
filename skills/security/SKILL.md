---
name: security
description: Threat-model the design per trust boundary using STRIDE and specify controls, identity, secrets, encryption, privacy and audit. Use when the user asks for a security design, threat model, or security review of an architecture.
---

# SA — Threat-model the design and specify controls

| | |
|---|---|
| Journey step | 10 — Security |
| Produces | 08-crosscutting/security-design.md |
| Inputs | 03-hld/*, 04-flows/*, 06-interfaces/*, 07-data/*, 00-context/architecture-drivers.md |
| Gate | none |
| Standards | `../method/standards/01-workflow-protocol.md`, `../method/standards/11-security-standard.md` |

**Method contract:** read `../method/SKILL.md` and `../method/standards/01-workflow-protocol.md` before acting. All nine execution phases (P1–P9) are defined there and are mandatory.

**Checklist:** the `## Checklist` section of `../method/standards/11-security-standard.md` — self-assess item by item in P9.

---

Follow `../method/standards/01-workflow-protocol.md` P1–P9.

**P3:** read the HLD (boundaries), flows (where credentials and data move), interfaces (entry points), data design (what is worth stealing), drivers (security and compliance obligations).

**Method:**

1. **Assets:** enumerate what is worth protecting — data sets, functions, availability, reputation — with sensitivity from the data design.
2. **Trust boundaries:** mark them on the HLD. Every boundary crossing is a control point. If the HLD has no boundaries marked, add them there first.
3. **Threat model per boundary using STRIDE.** For each boundary, walk all six categories; record `N/A — <reason>` where a category genuinely does not apply. Each threat gets a concrete scenario, not a category name.
4. **Controls:** every threat resolves to a preventive/detective/responsive control **or** an accepted residual risk with a named owner. No orphan threats.
5. **Identity & access:** authentication for users, services, and jobs; authorisation model; least privilege applied to data as well as APIs; per-operation permissions cross-checked against the interface specs.
6. **Secrets:** storage, rotation, access, delivery to runtime. Never a value in an artifact.
7. **Data protection:** in transit, at rest, in use; key management; masking/tokenisation; backups held to the same standard; non-production data handling.
8. **Privacy:** lawful basis, minimisation, subject rights, cross-border transfer.
9. **Audit:** what is recorded, immutability, retention, reviewer.
10. **Fail-closed behaviour:** state what happens when the authorisation system is unavailable.
11. Run the design-time checklist in Standard 11; report every unchecked item.

**P9:** report threats without controls, residual risks (which go to the risk register), and checklist failures, then `Next: /sa:gen-observability`.
