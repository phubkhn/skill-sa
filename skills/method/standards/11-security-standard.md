# Standard 11 — Security & Privacy Design

**Artifact:** `08-crosscutting/security-design.md`
**Purpose:** decide the security posture at design time, when it is still cheap.

## Required content

| Section | Content |
|---|---|
| Assets | what is worth protecting: data, functions, availability, reputation — with sensitivity |
| Trust boundaries | drawn on the HLD; every crossing is a control point |
| Actors & threat agents | including insiders and compromised dependencies |
| Threat model | per trust boundary, using a named method (STRIDE below) |
| Controls | one row per threat: preventive / detective / responsive |
| Identity & access | authentication of users, services, and jobs; authorisation model; least privilege |
| Secrets | where they live, how they rotate, who can read them, how they reach the runtime |
| Data protection | in transit, at rest, in use; key management; tokenisation/masking |
| Privacy | lawful basis, minimisation, subject rights (access/erasure/portability), cross-border transfer |
| Audit | what is recorded, immutability, retention, who reviews it |
| Compliance | applicable obligations and where each is satisfied in the design |
| Residual risk | anything accepted, with the accepting owner |

## STRIDE per boundary

| Threat | Question | Typical control |
|---|---|---|
| **S**poofing | can an actor pretend to be another? | strong authn, mutual TLS, signed tokens |
| **T**ampering | can data be modified in transit or at rest? | integrity checks, signing, immutable logs |
| **R**epudiation | can an actor deny an action? | audit trail with identity + time |
| **I**nformation disclosure | can data leak? | encryption, access control, redaction, minimisation |
| **D**enial of service | can availability be destroyed? | rate limits, quotas, isolation, backpressure |
| **E**levation of privilege | can an actor gain rights? | least privilege, separation of duties, input validation |

## Threat table format

| ID | Boundary | Threat (STRIDE) | Scenario | Likelihood | Impact | Control | Status | Residual |
|---|---|---|---|---|---|---|---|---|

## Rules

1. **Security is designed per trust boundary**, not per component.
2. **Every threat ends in a control or an accepted risk with a named owner.** No orphan threats.
3. **Authentication ≠ authorisation.** Both are specified, per interface operation.
4. **Service-to-service identity is designed explicitly.** "It's on the internal network" is not an authentication mechanism.
5. **Secrets never appear in artifacts, config in the repo, logs, or diagrams.**
6. **Defence in depth:** no single control is the only thing between an attacker and an asset.
7. **Fail closed.** State what happens to authorisation when the authorisation system is unavailable.
8. **Log what an investigator will need** — and nothing that itself becomes a breach.

## Design-time checklist

- [ ] Every external input validated at the boundary, with a stated validation strategy
- [ ] Every outbound call authenticated and its response treated as untrusted
- [ ] Least-privilege applied to data access, not just to APIs
- [ ] Multi-tenancy isolation model stated (if applicable)
- [ ] Dependency/supply-chain risk considered
- [ ] Backups protected to the same standard as the primary store
- [ ] Non-production environments' data handling stated

## Checklist

Self-assess against this list before reporting the artifact done. Report pass/fail **per item** — never a silent pass. A failed item becomes an OPEN item with an owner; it is not deleted to make the list pass.

- [ ] Assets enumerated with sensitivity and compromise impact
- [ ] Trust boundaries marked on the HLD
- [ ] STRIDE walked for every boundary; N/A entries justified
- [ ] Every threat has a concrete scenario, not a category name
- [ ] Every threat ends in a control or an accepted residual risk with a named owner
- [ ] Authentication defined for users, services, and jobs
- [ ] Authorisation model defined and mapped per interface operation
- [ ] Least privilege applied to data access, not only APIs
- [ ] Fail-closed behaviour stated for authz unavailability
- [ ] Secrets: storage, rotation, access, and runtime delivery defined; no values in artifacts
- [ ] Encryption in transit and at rest specified with key management
- [ ] Backups protected to the same standard as primary data
- [ ] Non-production data handling stated
- [ ] Privacy: lawful basis, minimisation, subject rights, cross-border transfer
- [ ] Audit events, immutability, retention, and reviewer defined
- [ ] Input validation strategy at every external boundary
- [ ] Outbound responses treated as untrusted
- [ ] Multi-tenancy isolation stated (or N/A justified)
- [ ] Supply-chain/dependency risk considered
- [ ] Residual risks pushed to the risk register
