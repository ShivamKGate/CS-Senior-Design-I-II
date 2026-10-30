# HepatoFusion — Requirements Document

**Project:** HepatoFusion  
**Team members:** Shivam Sinay Kharangate (sinayksp@mail.uc.edu), Nipun Chandra (chandrnu@mail.uc.edu)  
**Advisor:** Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children’s Hospital  
**Partner:** Cincinnati Children’s Hospital  
**Courses:** CS 5001 Senior Design I (Fall 2026) and CS 5002 Senior Design II (Spring 2027)  
**Document:** Requirements Document (Week 9)  
**Version:** 1.0  
**Date:** 30 October 2026

This document answers **what** the system must do and **for whom**. It does not introduce a new design. Content is consolidated from [`User_Stories.md`](User_Stories.md), [`Design_Diagrams/D0_High_Level_Design.md`](Design_Diagrams/D0_High_Level_Design.md), [`Design_Diagrams/D1_Detailed_Design.md`](Design_Diagrams/D1_Detailed_Design.md), [`Design_Diagrams/D2_Detailed_Design.md`](Design_Diagrams/D2_Detailed_Design.md), [`Planning/A5_A6_Implementation_Plan.md`](Planning/A5_A6_Implementation_Plan.md), the 21 October 2026 team meeting, and the 29 October 2026 advisor review with Dr. Patel. How the system is built is in [`Technical_Specification.md`](Technical_Specification.md) version 1.0, which traces to this file.

No PHI, medical record numbers, or slide files are in this file or in Git.

**AI use.** An AI tool helped format tables. Requirement statements, MoSCoW priorities, constraint IDs, and open-question owners are the team’s, taken from the sources named above and from Dr. Patel’s review.

**Plain-language note (US-01).** “Show the tumor map to the doctor” means: put the **existing** tumor outline into a viewer the pathologist already uses (PathPresenter, QuPath, or another open-source viewer under research), as a **helper**, not as a diagnosis. Dr. Patel did **not** make that the Must for this academic year. The Must is **data cleanup and finalization**.

---

## 1. Version and change log

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-10-30 | Initial requirements. IDs REQ-01–REQ-10, NFR-01–NFR-05, CON-01–CON-05. Must set limited to data cleanup and finalization per the 29 October 2026 advisor review. Six pathology architectures recorded as interchangeable (REQ-10); HCN-NOS glossary-only. Design changes since Week 7 logged below. | Shivam Sinay Kharangate, Nipun Chandra |

Logged design / scope changes since the Week 7 review (D2, 14 October 2026). D0 and D1 text are **not** rewritten (D2 R-10).

| ID | What changed | Why | Effect on this document |
|---|---|---|---|
| D2 R-02 | Partial-score rule: score only if pathology + model-ready outcomes + (radiology **or** molecular). Replaces D0 D-06. | A pathology-only “fusion” score would be misleading. | REQ-07 Could (needed only when scoring runs). |
| D2 R-01 | Identifier gate is deidentify-with-block-fallback (three-way decision). | Hospital files routinely carry stripable tags. | REQ-06 Must. |
| Team meeting, 21 Oct 2026 | Pathology backbone not frozen. Six architectures stay interchangeable; outlier finding and fine-tune use the same run/test path. | Comparison is not finished; architecture already allows a model swap. | REQ-10 Should. Declaring one official backbone is Won’t. |
| Team meeting, 21 Oct 2026 | Viewer research broadened: QuPath, PathPresenter, ImageScope, and side-by-side opening of 2–4 `.svs` files. | Model export into a viewing tool is a team/advisor task, not a D0 rewrite. | OQ-06. No new Must viewer. |
| Advisor, 29 Oct 2026 | Must for the year = data cleanup and finalization (including Epic field search). | Dr. Patel decision. | REQ-05, REQ-06, REQ-09 Must. Viewer (REQ-01) is Should. |
| Week 8 plan | Radiology intake, Genomics intake, integrator, and scorer stay iced until M36. | Extra modalities are not in hand. | REQ-02, REQ-04, REQ-07, REQ-08 Could. |

IDs are stable. If a requirement is dropped later, mark it **withdrawn** in this log. Do not reuse the ID.

---

## 2. Purpose and scope

**Purpose.** HepatoFusion is a research pipeline with Cincinnati Children’s Hospital. It (1) keeps the existing pediatric-liver-tumor localization available as a pathologist helper, and (2) collects radiology, molecular data, and cleaned clinical outcomes onto the **same** 102-patient cohort so a later research risk score can use only inputs that are actually linked.

**In scope for this release (this academic year, through April 2027).**

- Data cleanup and finalization of the clinical-outcomes spreadsheet, including Epic field search, on approved storage (Must).
- Cohort inventory from eSlide Manager / PathPresenter written into the Cohort case index (Must).
- Identifier-safe handling of any new radiology or molecular file before it is accepted (Must).
- Outlier review and optional fine-tune of the existing pathology localization, with the model treated as **swappable** among six already-compared architectures (Should).
- Helper files for a pathologist viewer, plus research of open-source viewers (Should). Not the year’s Must.

**Out of scope for this release (see §7 Won’t).** A public HTTP API; consumer cloud; an FDA diagnostic device; a fused risk score as a December 2026 Must; HCN-NOS as a product feature; freezing one AI backbone as “the” model.

The Silver/Gold whole-slide pipeline is **already built** (1,566 Silver and 1,546 Gold annotations, 248 WSIs, 102 patients). These requirements do not rebuild it. They consume its localization pointer.

Diagrams (linked, not copied): [D0 block](Design_Diagrams/D0_block_diagram.png), [D0 data flow](Design_Diagrams/D0_dataflow_diagram.png), [D1 data model](Design_Diagrams/D1_data_model.png), [D2 error paths](Design_Diagrams/D2_component_error_paths.png), [D2 case lifecycle](Design_Diagrams/D2_case_lifecycle.png).

---

## 3. Stakeholders and user goals (Week 4)

Source: [`User_Stories.md`](User_Stories.md). Goals are unchanged. Priorities below reflect the 29 October 2026 advisor Must (data cleanup).

| Category | Who | Goal this system serves | Week 4 story |
|---|---|---|---|
| Primary | Pediatric liver pathologist at Cincinnati Children’s | Use the existing tumor outline as a helper while reading a slide, and later compare a research risk number with the clinical picture, without treating a missing scan or molecular file as if it were present. The pathologist owns the diagnosis. | US-01, US-02 |
| Secondary | Radiology team member at Cincinnati Children’s | Link a CT or MRI for a patient **already** in the pathology cohort, only when a study has actually been collected. | US-03 |
| Secondary | HepatoFusion research engineer (this two-person team) | Turn the outcomes spreadsheet (including Epic-derived fields) into a table a model can train on, and keep new files on approved compute. | US-04 |
| Hidden | Hospital data-use / privacy reviewer | Block newly collected radiology and molecular files from the course repository when a direct patient identifier is present. | US-05 |

**User stories (verbatim intent, short form).**

- **US-01.** Pathologist wants the existing tumor localization as a helper on the WSI.  
- **US-02.** Pathologist wants one case-level risk estimate that names only inputs actually used.  
- **US-03.** Radiology wants a CT/MRI linked to the same cohort case, or recorded as not linked.  
- **US-04.** Engineer wants each outcomes row reduced to an agreed field set that joins to exactly one cohort case.  
- **US-05.** Data-use reviewer wants new radiology/molecular files blocked from Git when a direct identifier is present.

Use cases **UC-01** (produce a risk estimate) and **UC-02** (make outcomes model-ready) remain the Week 4 expansions of US-02 and US-04.

---

## 4. Glossary

Each term is defined once. Later sections use these words only.

| Term | Definition |
|---|---|
| **Approved share / approved compute** | Cincinnati Children’s or University of Cincinnati storage and machines allowed to hold this cohort. Not a personal laptop, not this Git repository, not consumer cloud. |
| **Case** | One patient in the existing pathology cohort, identified only by `study_id`. |
| **Cohort case index** | Pipeline component that records, for one `study_id`, which files are linked (D0, detailed in D1). |
| **CoAtNet-0, ConvNeXt-Tiny, MobileViTv2-1.0, Swin V2-Tiny, U-Net, ViT-Tiny/16** | Six pathology localization architectures the team compared on the 248-WSI set. None is frozen as the official model this year (REQ-10). |
| **Deidentify** | Remove or blank configured identifier fields (for example MRN, address) so a file can be accepted. If a required identifier cannot be removed (burned-in pixels), the file is blocked, not guessed. |
| **DICOM** | Standard file type for a CT or MRI study. |
| **eSlide Manager** | Hospital slide inventory system. External. Source of study membership for the case index. |
| **Epic** | Hospital electronic health record. External. Source of clinical-outcome fields for the Outcomes cleaner. |
| **Genomics intake** | Component that stores an accepted molecular Excel file and records link status. Iced until extra modalities exist. |
| **Gold annotation** | Expert-validated tumor (or tissue) label used for training claims and evaluation. Silver is not treated as ground truth. |
| **HCN-NOS** | Hepatocellular neoplasm, not otherwise specified — a rare pediatric liver-tumor subtype in the team’s model comparison. **Glossary only.** Not a product requirement this release. |
| **Identifier gate** | First pipeline stage for new DICOM or `.xlsx`. Deidentifies or blocks. Writes `gate_status.json`. |
| **IHC** | Immunohistochemistry slides. Extra pathology evidence on the case index if present; not a new D0 box. |
| **ImageScope** | Open-source / hospital-available whole-slide viewer under research (OQ-06). Not wired in D0. |
| **Localization / tumor map** | Existing outline of tumor on a whole-slide image, produced by the finished pathology pipeline. Helper for the pathologist, not a diagnosis. |
| **Model-ready (outcomes)** | A spreadsheet row that joins to exactly one cohort `study_id` and whose agreed fields are all non-empty and coded or numeric. |
| **Modality integrator** | Later stage that snapshots which inputs are linked for one case. Iced until M36. |
| **Molecular / genomics file** | For this release, an Excel workbook (`.xlsx`) of genomic or molecular fields. Other types are blocked. |
| **MoSCoW** | Must / Should / Could / Won’t for **this** release (this academic year). |
| **Outcomes cleaner** | Component that joins the clinical-outcomes spreadsheet to the cohort and writes model-ready rows plus an exclusion log (D1 ALG-01). |
| **Pathologist** | Pediatric liver pathologist at Cincinnati Children’s. Primary clinical user. Owns the read. |
| **PathPresenter** | Hospital-facing slide viewer. First planned place to show the localization helper. |
| **PHI** | Protected health information (for this project: patient name, MRN, date of birth, street address, and the slide/DICOM files themselves). |
| **QuPath** | Open-source slide viewer. Alternate landing for the localization model (Docker image in the Week 8 plan). No automatic fallback from PathPresenter. |
| **Radiology intake** | Component that stores an accepted DICOM and records whether it links to one cohort case. Iced except TMA-key side work. |
| **Research engineer** | Shivam Sinay Kharangate and Nipun Chandra, operating the pipeline on approved compute. |
| **Research prototype** | Not a diagnostic device. No FDA or 510(k) claim. |
| **Review package** | Helper files (overlay + JSON) placed for a viewer. Always includes the prototype disclaimer. |
| **Risk scorer** | Later stage that writes at most one number in `[0.0, 1.0]` or a block reason. Iced. |
| **Silver annotation** | Provisional label produced at scale. Useful for comparison; **not** ground truth in demos or reports. |
| **`study_id`** | Internal cohort key (for example `HF-0102`). Never a patient name. Equals the case folder name. |
| **`.svs`** | A common whole-slide image file type. Advisor asked about opening 2–4 such files side by side (OQ-06). |
| **TMA** | Tissue microarray. Side project: study keys for a radiology collaborator. Does not block pathology cleanup. |
| **WSI** | Whole-slide image of a pathology slide. |

---

## 5. Functional requirements

One row per requirement. Statement is pass/fail. **Must** is only the cleanup set Dr. Patel named. Source stories are Week 4. Verification methods: **Test** (scripted fixtures), **Inspection** (read files/config/Git), **Demonstration** (human opens a viewer), **Analysis** (metrics table).

| ID | Statement | MoSCoW | Source | Verification |
|---|---|---|---|---|
| REQ-01 | The system shall make the existing tumor localization available as helper files for a pathologist viewer, and every helper JSON shall contain the substring `research prototype, not a diagnostic device`. If PathPresenter cannot open the overlay, the files shall remain on the approved share and the system shall **not** switch to QuPath automatically. | Should | US-01 | Demonstration (T14 / TC-001); Inspection of `disclaimer` field |
| REQ-02 | When scoring is run, the system shall write at most one `score` in `[0.0, 1.0]` (or `null`) and a `used_inputs` list that names only modalities actually consumed. A missing modality shall not appear as used. | Could | US-02 | Test (TC-002) |
| REQ-03 | If the case has no model-ready outcomes row, the system shall not write a numeric score. `block_reason` shall be exactly `clinical outcomes not model-ready`. | Should | US-02, UC-01 E1 | Test (TC-003) |
| REQ-04 | Radiology intake shall set `link_status = linked` only when the `study_id` matches **exactly one** cohort case. Zero matches or more than one shall be `unmatched`. The system shall not guess a match. | Could | US-03 | Test (TC-004) |
| REQ-05 | The Outcomes cleaner shall keep a source row in the model-ready table if and only if (a) the join key matches exactly one cohort `study_id` and (b) every name in `agreed_fields` is non-empty and coded or numeric. The source workbook may include Epic-derived fields delivered onto approved storage. After each run the system shall report three integers: `source_rows`, `kept`, `excluded`. Unmatched, ambiguous, and free-text rows shall be logged with `unmatched`, `ambiguous_join`, or `field_not_coded` and shall not be guessed into the table. | Must | US-04, UC-02 | Test (TC-005) |
| REQ-06 | For every new radiology DICOM or molecular `.xlsx` in `incoming/`, the Identifier gate shall write `gate_status.json` with `decision` ∈ {`passed`, `passed_with_redaction`, `blocked`} and shall not write any identifier **value** (name, MRN, DOB, street address) into that JSON, into logs, or into this Git repository. | Must | US-05 | Test + Inspection (TC-006) |
| REQ-07 | The system shall emit a numeric score only when pathology localization is linked **and** outcomes are model-ready **and** at least one of {radiology with `annotation_status = present`, molecular `linked`} is true. Otherwise `assembly_decision` shall be `insufficient_modalities` or `outcomes_not_ready` and no number shall be written. | Could | US-02, D2 R-02 | Test (TC-007) |
| REQ-08 | Genomics intake shall accept `.xlsx` only. Any other molecular file type shall be `blocked` at the Identifier gate with `E_UNKNOWN_FORMAT` and shall never be stored as linked molecular data. | Could | US-02, D0 D-05 | Test (TC-008) |
| REQ-09 | After the eSlide Manager / PathPresenter inventory is applied, the Cohort case index shall contain one `case_link.json` per inventoried `study_id`, with `in_cohort = true` for members of the existing 102-patient cohort, and `localization_pointer` either a path on the approved share or `null`. The file shall not contain patient name, MRN, DOB, or street address. | Must | US-03 (membership), T2, I6 | Inspection + Test (TC-015) |
| REQ-10 | The pathology localization stage shall accept a `model_version` naming one of the evaluated architectures (U-Net, ConvNeXt-Tiny, ViT-Tiny/16, Swin V2-Tiny, MobileViTv2-1.0, CoAtNet-0, or a later recorded name) and shall write the **same** localization-pointer schema regardless of which weights ran. Swapping weights shall not require a new `case_link.json` field. Fine-tune and outlier review shall use this same run/test path. | Should | Team meeting 21 Oct 2026; T6, T7 | Test two `model_version` values (TC-016) |

No functional requirement asks the system to display HCN-NOS as a subtype overlay or diagnosis.

---

## 6. Non-functional requirements

Each NFR has a number or threshold. The set covers **performance**, **security**, **usability**, and **reliability**.

| ID | Statement | Category | MoSCoW | Source | Verification |
|---|---|---|---|---|---|
| NFR-01 | On approved CPU, `run_outcomes_clean` on a workbook of ≤ 2,000 rows and a cohort of ≤ 200 `study_id`s shall finish in ≤ 120 seconds. | Performance | Should | US-04 | Timed Test (TC-009) |
| NFR-02 | 100% of new radiology DICOM and molecular `.xlsx` files shall pass through the Identifier gate before `accepted/`. Authentication shall be hospital / UC SSO and folder ACL only (zero application user accounts). This Git repository shall contain **0** values of MRN, patient name, DOB, or street address. | Security | Must | US-05, CON-02 | Test of gate + Inspection of Git and logs (TC-010) |
| NFR-03 | A pathologist who already has an account on the chosen viewer shall locate the localization overlay and the score-or-block-reason for a deidentified case in ≤ 5 minutes on at least 2 of 3 cases. | Usability | Could | US-01 | Demonstration (TC-011 / T14) |
| NFR-04 | Writers shall use `.part` then rename. If a process is killed after creating `.part` and before rename, the destination JSON shall be absent or a previous complete file. In 10 of 10 crash trials, a truncated file shall not validate as a complete record. | Reliability | Should | D2 E-13, E-15, E-19, E-31 | Test (TC-012) |
| NFR-05 | A breaking field rename, removal, or enum change in `case_link.json` or `outcomes.json` shall be published under a new folder root `v2/`. Existing `v1/` files shall remain readable. Adding an optional field may stay in `v1/`. | Maintainability (versioning) | Should | D1 D1-05 | Inspection (TC-013) |

---

## 7. MoSCoW summary (this release)

“This release” = CS 5001/5002 through April 2027, with fusion iced until milestone M36 (3 April 2027). Must count is 4 of 15 REQ+NFR rows (27%), below half.

### Must

- **REQ-05** — Outcomes join-and-clean, including Epic-derived fields on approved storage; three counts; no guessed joins.  
- **REQ-06** — Identifier gate, three-way decision, no identifier values in JSON/logs/Git.  
- **REQ-09** — Cohort case index populated from eSlide / PathPresenter inventory.  
- **NFR-02** — 100% of new files gated; SSO/ACL only; 0 identifiers in Git.

This is the advisor Must: **data cleanup and finalization**.

### Should

- **REQ-01** — Localization helper files + disclaimer; no automatic QuPath fallback.  
- **REQ-03** — Never emit a number if outcomes are not model-ready (safety rule, even while scoring is Could).  
- **REQ-10** — Swappable pathology `model_version`; same schemas.  
- **NFR-01** — Cleaner finishes in ≤ 120 s at the stated load.  
- **NFR-04** — Atomic writes; crash does not leave a silent bad record.  
- **NFR-05** — Breaking schema change → `v2/`.

### Could

- **REQ-02** — One fused research risk score.  
- **REQ-04** — Radiology exact-one linking (needs returned DICOM).  
- **REQ-07** — Partial-score rule (pathology + outcomes + one extra modality).  
- **REQ-08** — Molecular `.xlsx` intake.  
- **NFR-03** — 5-minute pathologist find-the-overlay task.  
- Open-source viewer extras from the advisor meeting: ImageScope, side-by-side 2–4 `.svs` files (OQ-06). These are research, not extra Must IDs.

### Won’t (written so they cannot creep back in)

- Public HTTP API or consumer-cloud path (AWS/GCP student APIs, Colab) for slides, DICOM, or identified Excel.  
- Custom React / Node viewer as the product UI.  
- Automatic fallback from PathPresenter to QuPath.  
- Scoring on pathology + outcomes **only** (no extra modality) so that a demo number exists.  
- Presenting Silver labels as ground truth.  
- FDA / 510(k) / diagnostic-device claims.  
- HCN-NOS subtype overlay or subtype diagnosis as a deliverable.  
- Freezing one of the six compared architectures as the official backbone this year.  
- Push email, chat, or pager notifications.  
- SQL (Postgres/SQLite) as the D1 store this release (remains a proposed later migration).  
- Purchasing a commercial pathology platform or a new labeled dataset.  
- Committing WSI, DICOM, identified Excel, or MRN/name/DOB/address to Git.

---

## 8. Inherited constraints (Week 3 essay)

Source: [`Constraints_Essay_sinayksp.md`](Constraints_Essay_sinayksp.md). Each constraint has a stable `CON-##` ID. Consequences (what it forces or rules out) are restated in Technical Specification §5.

| ID | Constraint | Essay theme |
|---|---|---|
| CON-01 | Pediatric decision support only. The pathologist owns the read. Silver is not ground truth. Evaluation claims that treat labels as truth shall use Gold. | Ethical |
| CON-02 | PHI stays off personal devices, off this Git repository, and off consumer cloud. Train and infer only on approved institutional or hospital compute. | Security / privacy |
| CON-03 | Solutions shall respect Cincinnati Children’s data-use agreements, permissions for the 102-patient / 248-WSI cohort, and UC IP rules. Deliverables remain a research prototype: no FDA diagnostic claim and no redistribution of partner slides outside approved channels. | Legal / regulatory |
| CON-04 | No commercial budget beyond UC and Cincinnati Children’s facilities and existing research compute. Use open-source stacks and reuse the existing Silver/Gold stream rather than buying a platform or a new labeled set. | Economic |
| CON-05 | When privacy isolation conflicts with speed or multimodal scale, **compliance wins**. Delay fusion or run smaller ablations rather than skip isolation or emit a pathology-only score for a demo. | Concrete trade-off |

---

## 9. Assumptions and open questions

### 9.1 Assumptions (in force unless an owner revises them)

| ID | Assumption | Owner | Since |
|---|---|---|---|
| A-01 | The Silver/Gold pipeline and its localization files already exist on approved compute. This team does not rebuild labeling. | Shivam | Week 4 |
| A-02 | Cohort size for planning is 102 patients / 248 WSIs. New patients are not created by unmatched radiology or molecular files. | Both | Project Description |
| A-03 | An approved CCHMC/UC share exists and both teammates can authenticate with hospital/UC SSO. | Nipun | D0 D-01 |
| A-04 | Agreed outcome field names will be written into `pipeline_config.yaml` before the first ALG-01 production run (T13). | Nipun | D1 |
| A-05 | IHC, if present, attaches to the Cohort case index as extra pathology evidence. It is not a new D0 component. | Shivam | Week 8 T4 |
| A-06 | The six-architecture comparison (tumor Dice ~0.95–0.98; HCN-NOS Dice ~0.61–0.72) is a research analysis on approved compute. It is not a clinical claim and does not freeze a backbone (REQ-10). | Shivam | Team meeting 21 Oct 2026 |
| A-07 | Epic extracts used by REQ-05 stay on approved storage. Study IDs, not names, are the join key. | Shivam | T1 |

### 9.2 Open questions

| ID | Question | Owner | Target date |
|---|---|---|---|
| OQ-01 | Exact identifier-field list Cincinnati Children’s requires the gate to remove. | Shivam (liaison); Nipun (config) | Freeze 6 Nov 2026 (M18) |
| OQ-02 | PathPresenter import format for localization overlay + score helper. | Shivam + CCHMC IT | Before T9 (1 Feb 2027) |
| OQ-03 | Log retention and rotation on the approved share (stub 90 days). | Nipun | When share quota is known |
| OQ-04 | Risk-scorer model (logistic / GBM / small MLP). Interface is specified; model is not. | Both | Only if M36 thaws fusion |
| OQ-05 | Whether QuPath becomes the executable US-01 path if PathPresenter stays blocked. | Both | After OQ-02, by M31 (26 Feb 2027) |
| OQ-06 | Open-source viewer research from the advisor meeting: ImageScope vs QuPath vs PathPresenter; whether 2–4 `.svs` files can be opened side by side to compare model output. Research only; not a Must. | Shivam | Written note before T9 (1 Feb 2027) |
| OQ-07 | Which `model_version` is used for T7 fine-tune. Not frozen; revisit with outlier list. | Shivam | M26, 30 Jan 2027 |

---

## 10. Trace to the technical specification

[`Technical_Specification.md`](Technical_Specification.md) **version 1.0 (30 October 2026)** traces to this document version 1.0. Every REQ, NFR, and CON above appears in that file’s traceability matrix with a Design Component cell and a Week 10 test ID (TC-001–TC-016).
