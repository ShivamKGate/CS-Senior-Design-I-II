# HepatoFusion — Test Plan

**Project:** HepatoFusion  
**Team members:** Shivam Sinay Kharangate (sinayksp@mail.uc.edu), Nipun Chandra (chandrnu@mail.uc.edu)  
**Advisor:** Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children’s Hospital  
**Partner:** Cincinnati Children’s Hospital  
**Courses:** CS 5001 Senior Design I (Fall 2026) and CS 5002 Senior Design II (Spring 2027)  
**Document:** Test Plan (Week 10)  
**Version:** 1.0  
**Date:** 4 November 2026  
**Traces to:** [`Requirements_Document.md`](Requirements_Document.md) **v1.0** and [`Technical_Specification.md`](Technical_Specification.md) **v1.1**

This plan says how the team will **prove** the Week 9 requirements. It is written before full CS 5002 implementation. A teammate should be able to run each case without the author present. No PHI, MRNs, WSIs, or DICOM belong in this file or in Git.

**Roles.** Nipun Chandra is QA / test lead and owns this document. Each component owner writes the cases for their component (see §4 ownership). Cases execute mainly in CS 5002; this document freezes what “works” means now.

**AI use.** An AI tool helped format tables. Scope, metrics, case steps, and pass/fail thresholds are the team’s, taken from Requirements v1.0, D0–D2 edge cases, and the Week 8 plan.

**Current work note (4 Nov 2026).** Both teammates are collecting **IHC** evidence for the Cohort case index (in progress) and picking up the **old TMA** dataset files plus annotations on approved hospital systems (side path for later Radiology intake). These activities feed REQ-09 inventory / case-link readiness and the TMA side project (T4, T11). They do not add new Must IDs this week.

---

## 1. Scope: what is tested this cycle

### 1.1 In scope (by requirement ID and component)

| Req ID | MoSCoW | Component(s) | Why tested this cycle |
|---|---|---|---|
| **REQ-05** | Must | Outcomes cleaner (D1 ALG-01) | Advisor Must: model-ready outcomes table, including Epic-derived fields on approved storage |
| **REQ-06** | Must | Identifier gate (D2 §2.2) | Advisor Must: deidentify / block before `accepted/` |
| **REQ-09** | Must | Cohort case index (D1) | Advisor Must: inventory → one `case_link.json` per inventoried `study_id` (includes IHC join when present) |
| **NFR-02** | Must | Identifier gate + Logging + Auth (SSO/ACL) | Security Must: 100% gated; 0 identifiers in Git/logs |
| REQ-03 | Should | Risk scorer / integrator (design-level) | Spec safety rule; dry-run against fixtures even while scoring is iced |
| REQ-01 | Should | Review package | Helper files + disclaimer when T9/T14 land (CS 5002) |
| REQ-10 | Should | Existing pathology pipeline | Swappable `model_version`; same pointer schema (T6/T7) |
| NFR-01 | Should | Outcomes cleaner | Timed cleaner run |
| NFR-04 | Should | Case index / cleaner writers | Atomic `.part` + rename |
| NFR-05 | Should | Schema layout under `v1/` | Breaking change → `v2/` |
| CON-01, CON-03 | — | Review package / disclaimer | Inspection with REQ-01 |
| CON-02 | — | Gate + repo policy | With NFR-02 |
| CON-04 | — | Stack inspection | TC-014 |
| CON-05 | — | Ice / Won’t compliance | Design check with REQ-07 group |

**Supporting data work in scope for readiness (not separate Must IDs):** IHC inventory join into `case_link.json` (T4/T5); old TMA file pickup and annotations on approved systems (T11). Evidence is study-ID lists and join notes on the approved share — never PHI in Git.

### 1.2 Out of scope this cycle

| Item | Type | Reason |
|---|---|---|
| REQ-02 fused risk score end-to-end | Could / iced | No extra modality ready; M36 thaw gate |
| REQ-04 Radiology intake live DICOM linking | Could / iced | T15 parked until TMA DICOM returns |
| REQ-07 partial-score production scoring | Could / iced | Depends on integrator + scorer thaw |
| REQ-08 Genomics intake production | Could / iced | No molecular stream this semester |
| NFR-03 5-minute pathologist usability | Could | After PathPresenter / QuPath helper exists (T14) |
| Won’t: public HTTP API, consumer cloud, custom React viewer, auto QuPath fallback, pathology-only demo score, HCN-NOS product overlay, FDA claims, push notifications, SQL as D1 store | Won’t | Requirements Document §7 |
| Third-party: PathPresenter, QuPath, Epic, eSlide Manager, ImageScope internals | External | Not retested; only our handoff files and open status are checked |
| Retraining claims that Silver equals Gold | CON-01 | Silver never used as ground truth in pass criteria |
| Pixel OCR as a redaction tool | D2 | Burned-in text → block (`E_PIXEL_IDENTIFIER`), not redact |

---

## 2. Verification and validation strategy

**Verification (team vs. spec).** The team checks that outputs match schemas and rules in Requirements v1.0 / Technical Spec v1.1: Outcomes cleaner counts and exclusion reasons (REQ-05), gate three-way decisions with no identifier values (REQ-06, NFR-02), `case_link.json` inventory rules (REQ-09), atomic writes (NFR-04), schema versioning (NFR-05), stack inspection (CON-04), and design-level blocks for missing outcomes (REQ-03). Fixtures use synthetic `study_id`s and deidentified stand-ins on approved compute only.

**Validation (stakeholders vs. need).** Dr. Patel validates that cleanup and inventory are the right product for this year (advisor Must) and, later, that localization helpers are usable in PathPresenter or QuPath (REQ-01 / NFR-03 when ready). Pathologists do not re-label Silver as truth. Radiology / TMA collaborator validation of returned studies is deferred until files exist.

### 2.1 Test pyramid

| Layer | Approx. count | Coverage focus |
|---|---:|---|
| Unit | ~18 | ALG-01 row rules; gate decision helpers; JSON schema validators; sanitizer regex |
| Integration | ~12 | Gate → accepted path; cleaner → `outcomes.json` + exclusion JSONL; inventory → `case_link.json`; IHC optional slot |
| System | ~8 | Full cleanup run on seeded workbook; gate batch on `incoming/`; repo PHI scan; atomic-write crash suite |
| Acceptance | ~4 | Advisor spot-check of cleanup counts (M17/M24); PathPresenter/QuPath helper open when T14 runs; stack CON-04 inspection |

### 2.2 ML / pathology variables (when T6/T7 run)

| Variable | Metric | Tolerance / target | Trials |
|---|---|---|---|
| `model_version` (two of the six architectures) | Pointer schema unchanged (REQ-10) | Identical required fields in localization pointer / `case_link` | ≥ 2 versions × 1 holdout slide each |
| Localization quality (baseline check, not a Must) | Mean slide Dice / tumor AUROC vs Project Description | Report numbers; no fail if below 0.96/0.99 — document only (R4) | 1 holdout set on approved GPU |
| Gold vs Silver | Evaluation uses Gold only for “truth” claims | Silver never labeled ground truth in report | Inspection of metric tables |

---

## 3. Measurable success criteria

| Metric | Target threshold | How measured | Req ID |
|---|---|---|---|
| Cleaner summary counts | After each run, `source_rows`, `kept`, `excluded` are integers and `kept + excluded = source_rows` | Read cleaner summary JSON | REQ-05 |
| Join correctness | 0 guessed matches; unmatched / ambiguous / free-text rows only in exclusion log with correct reason enum | Fixture workbook + exclusion JSONL | REQ-05 |
| Gate coverage | 100% of new DICOM / molecular `.xlsx` under `incoming/` produce `gate_status.json` before any copy to `accepted/` | Place fixtures; inspect folders | REQ-06, NFR-02 |
| Identifier leak | 0 occurrences of MRN / patient name / DOB / street address in `gate_status.json`, pipeline logs, and this Git repo | Regex / manual inspection on approved share + `git grep` | REQ-06, NFR-02, CON-02 |
| Case index completeness | One `case_link.json` per inventoried `study_id`; `in_cohort = true` for known cohort members; no PHI keys | Compare inventory list to case folders | REQ-09 |
| Cleaner wall time | ≤ 120 s for ≤ 2,000 rows and ≤ 200 cohort IDs on approved CPU | Wall-clock timer around `run_outcomes_clean` | NFR-01 |
| Atomic write integrity | 10/10 kill-during-write trials leave no truncated file that validates as a complete record | Kill after `.part` create; validate destination | NFR-04 |
| Schema versioning | Breaking rename published under `v2/`; `v1/` still readable | Create breaking change in staging tree; open old `v1/` file | NFR-05 |
| Disclaimer present | Helper / score JSON contains substring `research prototype, not a diagnostic device` | String search in fixture output | REQ-01, CON-01, CON-03 |
| Stack compliance | Pipeline uses Python + pandas/openpyxl + existing PyTorch path; no commercial pathology platform billed | Dependency / Dockerfile / config inspection | CON-04 |
| Usability (when scheduled) | ≥ 2 of 3 cases: overlay + score-or-reason found in ≤ 5 minutes | Timed advisor/pathologist demo | NFR-03 |

---

## 4. Test cases

Status values: **Pass**, **Fail**, **Blocked**, or **Not Run**. All start as **Not Run**.  
IDs keep the Week 9 matrix anchors (TC-001–TC-016). Must groups expand as `TC-xxx-1` … so each major requirement has ≥ 3 cases. Matrix updated in Technical Spec v1.1.

**Owners by component:** Outcomes cleaner / NFR-01 — Nipun (cases), Shivam (Epic fixture source). Identifier gate / NFR-02 — Nipun. Cohort case index / REQ-09 / IHC — Nipun (files), Shivam (clinical inventory / IHC). Review package / REQ-01 — Shivam. Pathology `model_version` / REQ-10 — Shivam. Stack TC-014 — both. Risk-block REQ-03 — both (fixture design).

### 4.1 REQ-05 — Outcomes cleaner (Must) — TC-005-*

| ID | Description | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC-005-1 | Happy path: all rows exact-one join and agreed fields ready (REQ-05) | 1. On approved compute, place fixture workbook `clean_all_ready.xlsx` (N rows, every `study_id` in cohort list, all `agreed_fields` coded/numeric). 2. Set `pipeline_config.yaml` `agreed_fields` to match. 3. Run `run_outcomes_clean`. 4. Open summary JSON and each `outcomes.json`. | Summary: `source_rows = N`, `kept = N`, `excluded = 0`. Every kept file has `ready = true`, `exclusion_reason = null`. No patient name/MRN keys. | Not Run |
| TC-005-2 | Exclusion: unmatched join key (REQ-05, D2 E-14/UC-02 E1) | 1. Fixture with one row whose join key is absent from cohort. 2. Run cleaner. 3. Read exclusion JSONL and model-ready folder. | That row absent from model-ready table. Exclusion reason exactly `unmatched`. Summary `excluded ≥ 1`. No substitute `study_id` invented. | Not Run |
| TC-005-3 | Failure: missing join column (REQ-05, D2 E-16) | 1. Workbook without the configured `join_column` header. 2. Run cleaner. | Run fails with `E_MISSING_JOIN_COLUMN`. No partial `outcomes.json` written for that run. Summary not claiming success. | Not Run |
| TC-005-4 | Edge: free-text agreed field → `field_not_coded` (REQ-05, UC-02 A1) | 1. Matched `study_id` but one agreed field is unresolved free text. 2. Run cleaner. | Row excluded; reason `field_not_coded`; `field_name` set; study ID logged, not patient name. | Not Run |

### 4.2 REQ-06 — Identifier gate (Must) — TC-006-*

| ID | Description | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC-006-1 | Pass-with-redaction on stripable metadata (REQ-06, D2 R-01) | 1. Place synthetic DICOM or `.xlsx` in `incoming/<study_id>/` with configured identifier **tag/column present** but removable per `identifier_rules`. 2. Run `scan_and_deidentify`. 3. Read `gate_status.json` and `accepted/`. | `decision` is `passed` or `passed_with_redaction`. File copied to `accepted/`. `redactions[]` name field **types** only — no MRN/name/DOB/address **values** in JSON. | Not Run |
| TC-006-2 | Block burned-in / non-removable identifier (REQ-06, E-04) | 1. Fixture marked as `E_PIXEL_IDENTIFIER` path (or `require_block` column). 2. Run gate. | `decision = blocked`. File remains in `incoming/`. Nothing under `accepted/` for that file. | Not Run |
| TC-006-3 | Failure: missing `identifier_rules` config (REQ-06, E-05) | 1. Point stage at missing/invalid `pipeline_config.yaml` rules. 2. Attempt gate run. | `E_CONFIG_MISSING_RULES` (or schema error). Gate does **not** run with a defaulted rule set. No accept copy. | Not Run |

### 4.3 REQ-09 — Cohort case index (Must) — TC-015-*

| ID | Description | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC-015-1 | Inventory produces one `case_link.json` per listed `study_id` (REQ-09) | 1. Use deidentified inventory list (eSlide/PathPresenter extract on approved share). 2. Run index writer for each ID. 3. Count folders vs list. | Count of `case_link.json` equals inventory count. Each has `study_id` = folder name. Cohort members have `in_cohort = true`. | Not Run |
| TC-015-2 | PHI keys rejected (REQ-09, `E_PHI_FIELD`) | 1. Attempt `validate_and_write_case_link` with body containing `patient_name` or `mrn`. | Write refused with `E_PHI_FIELD`. No file written (or previous good file unchanged). | Not Run |
| TC-015-3 | Edge: unknown ID / folder mismatch (REQ-09, E-20) | 1. Write body where `study_id` ≠ folder name, or ID not in cohort. | `E_ID_MISMATCH` or `in_cohort = false` per D1 rules; no new patient invented. Localization pointer null or path only — never a name. | Not Run |
| TC-015-4 | IHC optional join note (supporting T4; still REQ-09 schema) | 1. For one inventoried case with IHC available on approved systems, record IHC presence per written join rule without PHI. 2. Re-read `case_link.json`. | Schema remains valid; IHC documented only as allowed non-PHI pathology evidence; radiology still `not_linked` until DICOM returns. | Not Run |

### 4.4 NFR-02 — Security (Must) — TC-010-*

| ID | Description | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC-010-1 | 100% gate before `accepted/` (NFR-02) | 1. Drop 5 fixture files into `incoming/`. 2. Run gate batch. 3. List `accepted/` and any bypass path. | Every accepted file has a corresponding `gate_status.json`. Zero files appear in `accepted/` without a gate record. | Not Run |
| TC-010-2 | Git contains 0 identifier values (NFR-02, CON-02) | 1. From repo root run agreed searches for MRN-like patterns / name fields in tracked files (no real PHI seeded). 2. Review last commit diff. | 0 matches for real or fixture MRN/name/DOB/address values in Git. WSI/DICOM/identified Excel absent. | Not Run |
| TC-010-3 | Log sanitizer strips identifier-like strings (NFR-02, E-40) | 1. Call `log_event` with a message containing a synthetic MRN-like token. 2. Read log line. | Log line contains `[REDACTED]` (or equivalent) instead of the token. Stage still completes. | Not Run |

### 4.5 Should / design / constraint cases (matrix anchors)

| ID | Description | Steps | Expected Result | Status |
|---|---|---|---|---|
| TC-001 | Review package disclaimer + no auto-QuPath (REQ-01, CON-01, CON-03) | 1. Build review package for fixture case with localization pointer. 2. Inspect helper JSON. 3. Simulate PathPresenter open failure (`mark_viewer_result` opened=false). | Disclaimer substring present. `package_status` reflects failure or built. Files remain on share. No automatic QuPath launch. | Not Run |
| TC-002 | Score names only used inputs (REQ-02) — **Blocked** until M36 | 1. When thawed, assemble sufficient input list. 2. Run `score_case`. | One score in `[0,1]` or null; `used_inputs` subset of linked modalities only. | Blocked |
| TC-003 | No score without model-ready outcomes (REQ-03) | 1. Build `input_list.json` with `assembly_decision = outcomes_not_ready`. 2. Call `score_case`. | `score = null`; `block_reason` exactly `clinical outcomes not model-ready`. | Not Run |
| TC-004 | Radiology exact-one link (REQ-04) — **Blocked** until DICOM | 1. When thawed, register DICOM with 0 and with 2 cohort hits. | Both → `unmatched`; never `linked`. | Blocked |
| TC-007 | Insufficient modalities block (REQ-07, CON-05) — design fixture | 1. Case with pathology + model-ready outcomes, radiology not annotated, molecular not linked. 2. `assemble_input_list`. | `assembly_decision = insufficient_modalities`; no numeric score file with a number. | Not Run |
| TC-008 | Non-xlsx molecular blocked (REQ-08) | 1. Place `.csv` or `.xls` in incoming as molecular. 2. Run gate. | `E_UNKNOWN_FORMAT` / blocked; never linked molecular. | Not Run |
| TC-009 | Cleaner ≤ 120 s at load (NFR-01) | 1. Workbook ≤ 2000 rows, cohort ≤ 200. 2. Time `run_outcomes_clean` on approved CPU. | Elapsed time ≤ 120 s; exit success or documented exclusion-only success. | Not Run |
| TC-011 | Usability ≤ 5 min on ≥ 2/3 cases (NFR-03) — later | 1. After helper exists, advisor opens 3 deidentified cases. 2. Time find overlay + score-or-reason. | Pass if ≥ 2 of 3 ≤ 5 minutes. | Blocked |
| TC-012 | Atomic write 10/10 (NFR-04) | 1. Hook writer to kill after `.part` create, 10 times. 2. Validate destination JSON. | 10/10: destination missing or previous complete file; never truncated-but-valid. | Not Run |
| TC-013 | Breaking schema → `v2/` (NFR-05) | 1. On staging share, publish breaking rename under `v2/`. 2. Open prior `v1/` case file. | `v1/` readable; new writes use `v2/` root. | Not Run |
| TC-014 | Open-source stack inspection (CON-04) | 1. List runtime deps / Docker base for QuPath image plan. 2. Confirm no commercial pathology platform purchase. | Python, pandas, openpyxl, existing PyTorch path present; CON-04 satisfied. | Not Run |
| TC-016 | Two `model_version` values, same pointer schema (REQ-10) | 1. Run localization for version A and B on same study (approved GPU). 2. Diff required pointer / case_link fields. | Required schema keys identical; only `model_version` (or equivalent) differs. | Not Run |

---

## 5. Test environment

| Aspect | Development | Staging (approved share) | Pilot / demo |
|---|---|---|---|
| **Hardware** | Team laptops for docs only (no PHI) | CCHMC/UC approved CPU; GPU for T6/T7 when scheduled | Same approved machines; PathPresenter or QuPath workstation |
| **OS** | Windows 10/11 (docs) | Institutional Linux or Windows as provided by hospital/UC IT | Viewer host OS as installed by hospital |
| **Software** | Git, Python 3, editor | Python 3, pandas, openpyxl, PyYAML, PyTorch (pathology), Docker (QuPath image when T8) | PathPresenter and/or QuPath; no custom browser app |
| **Browser** | N/A for pipeline | N/A | Only if PathPresenter is browser-based — use hospital-supported version; record version at demo |
| **Data** | Synthetic `study_id` fixtures in repo **without** PHI | Seeded deidentified workbooks, gate fixtures, inventory lists, optional IHC/TMA keys on approved share | Advisor-selected deidentified cases |
| **Config** | Sample `pipeline_config.yaml` with fake paths | Real `v1/config/pipeline_config.yaml` on share (`identifier_rules`, `agreed_fields`) | Same staging config frozen by `rule_set_version` |
| **Network** | No PHI over consumer cloud | Hospital/UC network + SSO; no consumer APIs | SSO session valid for demo |
| **Devices / sensors** | None | None (file pipeline). WSI scanners are external; we do not retest scanners | Viewer display only |

**TMA / IHC data path:** old TMA files and annotations, and IHC collection, stay on approved systems. Tests that need them run only after gate rules (T12) and study-ID-only inventories exist.

---

## 6. Pass and fail criteria

### 6.1 Per-test

| Outcome | Rule |
|---|---|
| **Pass** | Every step completed; **Expected Result** fully met; metric in §3 within threshold |
| **Fail** | Any Expected Result missed, or metric outside threshold, or PHI/identifier value observed in Git/log/status JSON |
| **Blocked** | Dependency missing (ice, OQ open, no SSO, no fixture). Record blocker ID (e.g., M36, OQ-02) |
| **Not Run** | Not yet executed |

### 6.2 Plan-level (this academic year Must)

The **cleanup Must set passes** only if all of the following are true:

1. TC-005-1 and at least one of TC-005-2 / TC-005-3 / TC-005-4 **Pass**.  
2. TC-006-1, TC-006-2, and TC-006-3 **Pass**.  
3. TC-015-1 and TC-015-2 **Pass** (TC-015-3 or TC-015-4 Pass or justified Blocked).  
4. TC-010-1, TC-010-2, and TC-010-3 **Pass**.  
5. Zero open **Fail** defects on Must cases without a written waiver from both teammates + advisor note.

**Plan fails** if any Must case is **Fail** at M17 / M24 checkpoints, or if a PHI value is found in Git at any time (immediate Fail of NFR-02 / CON-02).

Could/Should cases may remain **Blocked** without failing the year’s Must plan, except REQ-03 design fixture (TC-003) should **Pass** before any thawed scoring demo.

---

## 7. Schedule (milestones, owners, evidence)

Aligned to Week 8 milestones in [`Planning/A5_A6_Implementation_Plan.md`](Planning/A5_A6_Implementation_Plan.md).

| Milestone | Date | Test activity | Layer | Owner | Evidence |
|---|---|---|---|---|---|
| M11 / this plan | 6–13 Nov 2026 | Freeze cases; peer trade of 2 cases | Plan | Nipun (lead), Shivam | `Test_Plan.md` + PDF |
| M18 | 6 Nov 2026 | Gate rules freeze → enable TC-006 / TC-010 fixtures | Unit / integration | Nipun | `identifier_rules` version on share |
| M17 fall cleanup | 4 Dec 2026 | TC-005-*, TC-015-1, TC-010-2; IHC/TMA inventory status | System | Both | Count summary (no PHI); case-link count |
| M24 ALG-01 | 23 Jan 2027 | Full TC-005 suite + TC-009 | Integration / system | Nipun | Summary JSON + timer log |
| M26 / M27 | 30 Jan 2027 | TC-016; TC-014 on Docker/stack | Unit / system | Shivam / Nipun | Metrics table; build log |
| M29 / M30 | 13 Feb 2027 | TC-001 dry run (QuPath and/or review package) | System | Both | `review_package.json` |
| M31 mid-demo | 26 Feb 2027 | Acceptance spot-check; disclaimer spoken | Acceptance | Both + advisor | Demo notes |
| M32 | 12 Mar 2027 | TC-001 / TC-011 if PathPresenter ready | Acceptance | Shivam; Dr. Patel | Written OK |
| M36 ice/thaw | 3 Apr 2027 | Unblock TC-002/004/007 production paths only if DICOM arrived | Integration | Both | Gate note |
| M38 final | 16 Apr 2027 | Must suite green; Could labeled Blocked or Pass | System / acceptance | Both | Test log reprint |

**Risk order:** NFR-02 / REQ-06 (PHI) → REQ-05 (data integrity) → REQ-09 (index) → Should helpers → iced fusion.

---

## 8. Definition of done

### 8.1 Feature-level checklist

A component feature is **done** only when:

- [ ] Code/config on approved share (or repo for non-PHI only) matches the named D0/D1/D2 interface  
- [ ] All Must test cases for that feature are **Pass** (or waived in writing)  
- [ ] At least one edge/failure case in the group was executed  
- [ ] No PHI in Git, logs, or status JSON for the change  
- [ ] `rule_set_version` / `model_version` recorded where schemas require it  
- [ ] Peer or teammate reviewed steps once (can execute without asking the author)  
- [ ] README / design note updated if behavior changed  

### 8.2 Project-level checklist (CS 5002 handoff)

- [ ] Must set REQ-05, REQ-06, REQ-09, NFR-02: all plan-level pass rules in §6.2 met  
- [ ] Test log (Pass/Fail/Blocked/Not Run) committed or stored on approved share  
- [ ] Open defects listed with owner and severity; no unresolved Must Fail  
- [ ] Documentation: Requirements, Tech Spec, this Test Plan, Week 8 plan consistent  
- [ ] Advisor sign-off on cleanup checkpoint (M17/M24) recorded  
- [ ] IHC collection and TMA pickup status noted (complete / in progress / blocked) without PHI  
- [ ] Iced Could items explicitly labeled Blocked, not silently Pass  

---

## Appendix A — TC ID map to Week 9 matrix

| Matrix anchor | Cases in this plan | Requirement |
|---|---|---|
| TC-001 | TC-001 | REQ-01, CON-01, CON-03 |
| TC-002 | TC-002 | REQ-02 |
| TC-003 | TC-003 | REQ-03 |
| TC-004 | TC-004 | REQ-04 |
| TC-005 | TC-005-1 … TC-005-4 | REQ-05 |
| TC-006 | TC-006-1 … TC-006-3 | REQ-06 |
| TC-007 | TC-007 | REQ-07, CON-05 |
| TC-008 | TC-008 | REQ-08 |
| TC-009 | TC-009 | NFR-01 |
| TC-010 | TC-010-1 … TC-010-3 | NFR-02, CON-02 |
| TC-011 | TC-011 | NFR-03 |
| TC-012 | TC-012 | NFR-04 |
| TC-013 | TC-013 | NFR-05 |
| TC-014 | TC-014 | CON-04 |
| TC-015 | TC-015-1 … TC-015-4 | REQ-09 |
| TC-016 | TC-016 | REQ-10 |

No reserved ID was reused for a different requirement. Sub-IDs are expansions of the same anchor.
