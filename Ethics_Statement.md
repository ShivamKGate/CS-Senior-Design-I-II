# Ethics Statement

**Project:** HepatoFusion
**Team members:** Nipun Chandra (chandrnu@mail.uc.edu), Shivam Sinay Kharangate (sinayksp@mail.uc.edu)
**Advisor:** Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children's Hospital
**Partner:** Cincinnati Children's Hospital (CCHMC)
**Documentation lead:** Nipun Chandra
**Date:** 2026-11-10
**Traces to:** [`Constraints_Essay_sinayksp.md`](Constraints_Essay_sinayksp.md), [`Constraints_Essay_chandrnn.md`](Constraints_Essay_chandrnn.md), [`Requirements_Document.md`](Requirements_Document.md) v1.0, [`Technical_Specification.md`](Technical_Specification.md) v1.1, D0–D2 diagrams

**Repository scope note.** This GitHub repository is **documentation-only**. The HepatoFusion code (identifier gate, intakes, cleaner, integrator, scorer, review package, pathology localization model) lives in a **separate private repository owned by CCHMC** because it sits adjacent to PHI and is subject to the Cincinnati Children's data-use agreement and HIPAA-aligned handling.

---

## 1. Privacy summary

Every arrow on the D0–D2 diagrams represents a file on approved CCHMC or UC shared storage; no PHI, WSI, DICOM, or identified Excel is ever written to this repository or to any consumer cloud (CON-02). Consent is obtained upstream by Cincinnati Children's through **IRB approval** and the clinical data-use agreement that covers the existing 102-patient / 248-WSI cohort; the team consumes data under that approval and does not re-consent patients. When the project ends in April 2027, **all PHI-bearing data stays with CCHMC on hospital storage** — the team does not retain, copy, or hand off patient data. Pipeline log retention is **90 days by default** (`logging.retention_days` in `pipeline_config.yaml`, OQ-03), rotated on institutional storage.

| Data item | Source | Purpose | Consent | Storage | Access | Retention |
|---|---|---|---|---|---|---|
| DICOM (radiology) | CCHMC Radiology (I1) | Radiology intake, future fusion input | IRB + DUA | Approved share `v1/incoming/` → `v1/accepted/` after gate | SSO + folder ACL | With CCHMC after project end |
| Molecular `.xlsx` | CCHMC molecular source (I2) | Genomics intake | IRB + DUA | Approved share, same path pattern | SSO + folder ACL | With CCHMC after project end |
| Outcomes `.xlsx` (may include Epic-derived fields) | CCHMC outcomes spreadsheet (I5) | Outcomes cleaner input for later risk score | IRB + DUA | Approved share | SSO + folder ACL | With CCHMC after project end |
| Whole-slide images + Silver/Gold annotations | Existing pathology pipeline (I6, I11) | Localization pointer + eval set | IRB + DUA | Approved CCHMC compute; pointer only, file stays in place | SSO + folder ACL | With CCHMC after project end |
| `gate_status.json` | Identifier gate output | Three-way deidentification record | Derived; no patient values stored | `v1/cases/<study_id>/` | SSO + folder ACL | With case folder |
| `case_link.json`, `radiology.json`, `molecular.json`, `outcomes.json` | Intakes + cleaner | Modality/cohort link records | Derived | `v1/cases/<study_id>/` | SSO + folder ACL | With case folder |
| `input_list.json`, `score_result.json`, `review_package.json` | Integrator, scorer, review package | Research risk-score artifacts (Could) | Derived | `v1/cases/<study_id>/` | SSO + folder ACL | With case folder |
| `pipeline_config.yaml` | Team-authored | Rule sets, model versions, paths — **no credentials** | N/A (config) | Approved share `v1/config/` | SSO + folder ACL | Project duration + CCHMC archive |
| Pipeline logs (`v1/logs/…`) | All components (I16) | Operational audit; sanitizer strips identifier-like tokens | Derived | Approved share, no PHI in message field (NFR-02) | SSO + folder ACL | 90 days default, then rotated |
| Pathology model weights | Research compute | Localization backbone (swappable, REQ-10) | N/A (not PHI) | Approved compute + Docker image for QuPath (T8/T10) | SSO + folder ACL | With CCHMC after project end |

**Fields removed because they could not be justified.** `case_link.json` and every other `v1/` schema **forbids** patient name, medical record number (MRN), date of birth, and street address (Technical_Specification.md §3.3 "Forbidden keys"; error code `E_PHI_FIELD`). Early schema drafts considered carrying patient name alongside `study_id` for operator convenience during cleaning; that field was removed because `study_id` is sufficient for every join (ALG-01) and carrying names would both widen the PHI surface and conflict with the log sanitizer (NFR-02, E-40). Identifier **values** are never stored in `gate_status.json`; only field *types* and redaction actions are recorded.

---

## 2. Security summary

Security is enforced by the deployment topology before it is enforced by code: HepatoFusion is a file pipeline on approved institutional storage with no public HTTP surface, no app-level user accounts, and no secrets in version control (CON-02, D0 D-01, D-03, D1 D1-04).

**Default credentials.** There are **no default credentials to rotate** because there are no app-level users. Authentication is delegated to the operator's **CCHMC / UC Single Sign-On (SSO)**, and authorization is enforced by the **folder ACL** on the approved share (Technical_Specification.md §4 "Authentication"; D2 §2.8). A new team member gets access by being added to the ACL by the institutional data steward, not by being issued an application password. When SSO expires or ACL denies, the stage halts with `E_PERMISSION_DENIED` and a human re-authenticates; the pipeline does not retry or cache credentials.

**Unauthenticated endpoints.** There are **no HTTP endpoints** in the system (CON-02, D0 D-03, Requirements Document Won't list). The "API" is the logical operations table in Technical_Specification.md §3.2, invoked as Python function calls on approved compute by another pipeline stage or a teammate's script running under their own SSO session. Every boundary (I1–I18) is a file on an ACL-guarded folder, so anonymous access is physically impossible from outside the approved network.

**Secrets in source control.** `pipeline_config.yaml` is specified to hold **no credentials** — only paths, identifier rules, model versions, and retention (Technical_Specification.md §3.3, §4). Credentials live in SSO, which the pipeline never reads. A full-history git search (`git log --all -p | grep -iE '(password|passwd|secret|api[_-]?key|token|BEGIN RSA|BEGIN OPENSSH|BEGIN PRIVATE|AWS_|AKIA|bearer|credentials)'`) across all 22 commits returned **zero committed secrets**; the only matches were our own *prohibition* strings in `README.md`, `Technical_Specification.md`, `Team_Contract.md`, and D2 (e.g., "no secrets in this file", "do not commit credentials"). No remediation was required; the scan is part of the ongoing commit discipline rather than a one-time cleanup. Secrets in the separate CCHMC-owned private code repository are governed by the same rule — SSO plus folder ACL, no in-file credentials — because that repository runs the pipeline against the same approved share.

**Self-audit.**

| Question | Answer |
|---|---|
| Are there default credentials anywhere? | No. SSO + folder ACL only. No app-level users exist. |
| Are any endpoints reachable without authentication? | No. No HTTP surface; file-pipeline boundaries are behind the share ACL. |
| Are secrets or credentials committed to git? | No. Full-history scan is clean across 22 commits. |
| Is HTTPS enforced where relevant? | N/A at the pipeline layer (no HTTP). Hospital SSO and share access are HTTPS/SMB-with-TLS per institutional policy. |
| Is rate limiting needed? | No. Batch pipeline on institutional compute; no exposed service. |
| What is the token lifetime / session policy? | Inherited from CCHMC/UC SSO. `E_PERMISSION_DENIED` on expiry is not retried. |
| Where do secrets live if not in git? | SSO; nowhere in the pipeline, config file, or environment variables. |
| Is PHI redacted in logs? | Yes. Log sanitizer (NFR-02, E-40, I16) strips identifier-like strings; message field holds no PHI. |
| Is data encrypted at rest? | Yes, by the institutional storage provider (CCHMC / UC approved share and compute). The pipeline does not add a second encryption layer. |
| Is there an auditable record of writes? | Yes. Per-component log files (`v1/logs/…`, I16) with `run_id` and `rule_set_version` written into every artifact. |

---

## 3. Licensing summary

This documentation repository has **no public license**. HepatoFusion is a **research prototype under CCHMC/UC agreement**, built on partner clinical data with redistribution governed by the data-use agreement and UC IP rules for student work (CON-03). No license is granted to the public, and the repository is not intended for third-party reuse. The separate CCHMC-owned private code repository follows the same posture.

The code that this documentation describes (and that lives in the private CCHMC repository) is **planned to depend on** the Python stack listed in Technical_Specification.md §4. The licenses below were pre-cleared before being named in the stack table so that CON-04 (open-source only, no commercial budget) is satisfied by construction.

| Name | Version | License (SPDX) | Permissive / Copyleft | Obligation |
|---|---|---|---|---|
| Python (CPython runtime + stdlib `json`, `csv`, `logging`) | 3.x | `PSF-2.0` | Permissive | Retain upstream notice; no copyleft reach. |
| pandas | latest stable | `BSD-3-Clause` | Permissive | Retain copyright + license notice. |
| openpyxl | latest stable | `MIT` | Permissive | Retain copyright + license notice. |
| pydicom (candidate DICOM metadata reader) | latest stable | `MIT` | Permissive | Retain copyright + license notice. |
| PyYAML | latest stable | `MIT` | Permissive | Retain copyright + license notice. |
| PyTorch (existing pathology stack per CON-04) | per existing pipeline | `BSD-3-Clause` | Permissive | Retain copyright + license notice. |

**Project license compatibility.** Because the project itself is "no public license, internal research prototype," there is no outbound distribution to a third party that would trigger any of these notices externally; internal use is covered by every row. **No copyleft dependencies** (no GPL / LGPL / AGPL / MPL) are in the planned stack. This was a deliberate choice: copyleft on a core dependency would have made the status of partner-owned code and weights harder to reason about, so the team restricted the stack to permissive licenses at D1 build-versus-reuse (D1 §4). **Decision recorded:** permissive-only; revisit only if a strictly better permissive alternative is unavailable for a needed capability.

**Datasets.** The 102-patient / 248-WSI cohort with 1,566 Silver / 1,546 Gold annotations is **CCHMC internal data under IRB approval and data-use agreement**. It is **not** an open-license dataset, has no SPDX identifier, and **is not redistributable** — slides, tiles, derived annotations, and trained weights stay on approved channels (CON-03). No public benchmark dataset is used in this phase.

**Creative assets.** Diagrams under `Design_Diagrams/` (D0 block and data-flow, D1 data model, D2 case lifecycle and error paths) are **team-authored** in draw.io; no third-party icons, fonts, or images are embedded. The repository contains no logos, photography, or audio.

---

## 4. Attribution list

**Libraries (planned dependencies — source URLs for the private code repository):**

- pandas — https://github.com/pandas-dev/pandas — BSD-3-Clause
- openpyxl — https://foss.heptapod.net/openpyxl/openpyxl — MIT
- pydicom — https://github.com/pydicom/pydicom — MIT
- PyYAML — https://github.com/yaml/pyyaml — MIT
- PyTorch — https://github.com/pytorch/pytorch — BSD-3-Clause
- Python stdlib (`json`, `csv`, `logging`) — https://github.com/python/cpython — PSF-2.0

**Code adapted from tutorials or other repositories.** None in this documentation repository. In the private CCHMC code repository, AI-assisted **boilerplate** (typed function signatures, argparse scaffolds, pytest fixtures, JSON-schema stubs) is reviewed line by line and tested before merge; no verbatim copy-paste from external tutorials or Stack Overflow is included. If a snippet is adapted, the source is named in a code comment at the point of use.

**Datasets.** Cincinnati Children's pediatric liver-cancer cohort — 102 patients, 248 WSIs, 1,566 Silver and 1,546 Gold annotations. **Collection method:** retrospective clinical and pathology records assembled by CCHMC Pathology under IRB approval; Silver labels produced at scale by the existing in-house pipeline, Gold labels expert-validated by pathologists. **Usage restrictions:** data-use agreement with CCHMC; no redistribution of slides, tiles, derived annotations, or trained weights outside approved channels; no public benchmark submissions; research-prototype use only, no FDA / 510(k) / diagnostic-device claims (CON-01, CON-03, REQ-01 disclaimer string).

**Non-code assets.** All diagrams are team-authored in draw.io (`D0_diagrams.drawio`, `D1_diagrams.drawio`, `D2_diagrams.drawio`); no third-party icons, fonts, or images are used. The `proof.png` file is an advisor-approval screenshot captured by the team.

**NOTICE.** The library list above will also be mirrored into a `NOTICE` file in the private CCHMC code repository alongside `requirements.txt` when that repository is populated, and the same list is linked from this repository's `README.md` section 5.

---

## 5. AI-use disclosure

> "Generative AI tools may be used for drafting and code assistance but not for the design decisions or written analysis that are assessed in this course."

Every AI use on this project is logged below, sorted by the two-column framework from class: **Generally OK** (boilerplate, syntactic cleanup, formatting, scaffolding) versus **Not a substitute for** (design decisions, architecture, written analysis, requirements).

| Tool | Used by | Task | Column | How verified |
|---|---|---|---|---|
| ChatGPT | Nipun Chandra | Markdown table cleanup and prose tightening on Requirements, Technical Specification, Test Plan, Constraints Essay | Generally OK | Read line by line; every table and claim re-checked against D0–D2, the requirements IDs, and the test IDs; no fact adopted unless already in the source documents. |
| ChatGPT | Shivam Sinay Kharangate | Markdown table cleanup and prose tightening on User Stories, D0–D2 narrative sections, Constraints Essay | Generally OK | Read line by line; every requirement, user story, and acceptance criterion re-checked against team meeting notes and the advisor meeting log before commit. |
| Claude | Nipun Chandra | Draft scaffolding for sections of D1, D2, Test Plan, and this Ethics Statement; markdown cleanup; help structuring traceability-matrix columns | Generally OK | Section-by-section review against D0 IDs, D1 schemas, and D2 error catalog; any sentence not grounded in those sources was deleted. |
| Claude | Shivam Sinay Kharangate | Draft scaffolding for sections of Requirements, D0–D2, and the Implementation Plan; markdown cleanup | Generally OK | Reviewed against the 21 Oct team meeting notes and the 29 Oct advisor review; advisor-narrowed Must list was entered by hand to avoid tool drift. |
| Claude | Nipun Chandra, Shivam Sinay Kharangate | Diagram generation help — producing draw.io XML scaffolds for D0 block / dataflow, D1 data model, and D2 lifecycle / error-path figures | Generally OK | Opened each generated draw.io file, re-laid out boxes and arrows to match the component boundaries the team had already chosen in D0, and re-exported PNGs; the component list, interface IDs (I1–I18), and error paths are the team's, not the tool's. |
| Cursor | Nipun Chandra, Shivam Sinay Kharangate | Boilerplate code generation in the **private CCHMC code repository** — typed function signatures, argparse scaffolds, pytest fixtures, JSON-schema stubs | Generally OK | Reviewed line by line; unit tests (TC-005-*, TC-006-*, TC-010-*, TC-015-*) are written by the team against the team-authored schemas, and no generated code is merged until it passes those tests on approved compute. No PHI, slide data, or identifier samples are ever entered into Cursor prompts. |


**Confirmation.**

The architecture (file pipeline on approved compute, I1–I18 boundaries), the data model (Case / ModalityLink / OutcomesRow / ExclusionLogEntry), the priorities (Must = REQ-05, REQ-06, REQ-09, NFR-02 per the 29 Oct advisor review), and the design rationale (CON-01–CON-05 consequences) are the team's own, taken from D0–D2, the advisor meetings on 17 September 2026 and 29 October 2026, and the team meeting on 21 October 2026. AI tools were used for drafting and code assistance only, within the "Generally OK" column, and every "Not a substitute for" attempt was discarded and disclosed above.

Signed:

- Nipun Chandra — 2026-11-10
- Shivam Sinay Kharangate — 2026-11-10
