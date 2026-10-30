# HepatoFusion — Technical Specification Document

**Project:** HepatoFusion  
**Team members:** Shivam Sinay Kharangate (sinayksp@mail.uc.edu), Nipun Chandra (chandrnu@mail.uc.edu)  
**Advisor:** Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children’s Hospital  
**Partner:** Cincinnati Children’s Hospital  
**Courses:** CS 5001 Senior Design I (Fall 2026) and CS 5002 Senior Design II (Spring 2027)  
**Document:** Technical Specification (Week 9)  
**Version:** 1.0  
**Date:** 30 October 2026  
**Traces to:** [`Requirements_Document.md`](Requirements_Document.md) **version 1.0 (30 October 2026)**

This document answers **how** the system will be built. It does not introduce a new design. Architecture, interfaces, schemas, and error behavior are those already specified in `Design_Diagrams/D0_High_Level_Design.md`, `Design_Diagrams/D1_Detailed_Design.md`, and `Design_Diagrams/D2_Detailed_Design.md`. Diagrams are linked, not copied.

No PHI, medical record numbers, or slide files are in this file or in Git.

**AI use.** An AI tool helped format tables. Component boundaries, stack justifications, constraint consequences, and the traceability matrix are the team’s, taken from D0–D2 and the requirements document named above.

---

## 1. Version and change log

| Version | Date | Change | Author |
|---|---|---|---|
| 1.0 | 2026-10-30 | Initial technical specification tracing to Requirements Document v1.0. Consolidates D0 I1–I15, D1 schemas and ALG-01, D2 I16–I18, the D2 partial-score rule, the Week 8 pathology-first order, the 21 October 2026 team meeting, the 29 October 2026 advisor review, the six-architecture comparison table, and REQ-09 / REQ-10. | Shivam Sinay Kharangate, Nipun Chandra |

Logged design / scope changes since the Week 7 review (same events as Requirements Document v1.0 §1). D0 and D1 text are **not** rewritten (D2 R-10).

- **D2 R-02 / REQ-07.** Partial-score rule replaces D0 D-06.
- **D2 R-01 / REQ-06.** Identifier gate is deidentify-with-block-fallback, three-way `passed` / `passed_with_redaction` / `blocked`.
- **Week 8 plan.** Radiology intake, Genomics intake, Modality integrator, and Risk scorer remain specified here and sit at status Planned until milestone M36.
- **Team meeting, 21 Oct 2026 / REQ-10.** Six compared pathology architectures stay interchangeable. Outlier finding and fine-tune use the same run/test path. Declaring one official backbone this year is Won’t.
- **Team meeting, 21 Oct 2026 / OQ-06.** Viewer research broadened: QuPath, PathPresenter, ImageScope, and side-by-side opening of 2–4 `.svs` files. No new D0 box.
- **Advisor, 29 Oct 2026.** Must for the year is data cleanup and finalization (REQ-05, REQ-06, REQ-09), including Epic field search. A fused score is Could.

---

## 2. Architecture summary

HepatoFusion is a **file pipeline** on approved Cincinnati Children’s or University of Cincinnati shared storage. One case is one folder named by `study_id`. Each stage writes a file; the next stage reads that file. There is no public HTTP API and no consumer cloud (CON-02, D0 D-01, D-03).

**Major components we build (solid boxes on D0):** Identifier gate, Radiology intake, Genomics intake, Outcomes cleaner, Cohort case index, Modality integrator, Risk scorer, Review package. **Glue (D2):** Configuration (`pipeline_config.yaml`), Logging, Authentication (SSO / folder ACL only; no app-level users), Notifications (none pushed; `read_case_status` only).

**External systems we do not build (dashed boxes on D0):** Radiology team, Molecular Excel source, Outcomes spreadsheet, existing pathology pipeline (Silver/Gold + swappable localization model), PathPresenter (primary viewer), QuPath (alternate, not auto-wired), Pathologist. ImageScope is under research (OQ-06); it is not a new D0 box. Epic and eSlide Manager are hospital sources for Must cleanup (REQ-05, REQ-09), same pattern as the dashed outcomes spreadsheet.

**Deployment model.** Batch jobs on approved institutional or hospital compute, reading and writing the approved share. Authentication is the operator’s hospital / UC SSO. Nothing in this release is a deployed multi-user service, a container platform for the whole pipeline, or a cloud app. The one container in the Week 8 plan is a Docker image of the current pathology localization weights for QuPath inference (T8/T10), still on approved compute. The image’s `model_version` is swappable (REQ-10). Spring 2027 does not add a second deployment topology.

**Data flow (two pipelines, one case folder).**

1. **Collection (now — Must).** New DICOM or `.xlsx` lands in `incoming/`. The Identifier gate deidentifies or blocks (I1, I2). Accepted files go to Radiology intake or Genomics intake (I3, I4) when those stages thaw. The Outcomes cleaner joins the spreadsheet — including Epic-derived fields — to the cohort (I5). The existing pathology pipeline contributes a read-only localization pointer (I6, I11). The Cohort case index records inventory and link status (I7, I8, I9; REQ-09).
2. **Integration (later, REQ-02 Could).** The Modality integrator snapshots the case (I10, I11) into `input_list.json` (I12). If `assembly_decision` is `sufficient`, the Risk scorer writes one score or a block reason (I13). The Review package writes helper files for PathPresenter (I14). The pathologist reads the case in PathPresenter (I15). A missing extra modality does not count as present (REQ-07). Missing model-ready outcomes never produce a number (REQ-03).

**Pathology models (research analysis, not a frozen choice).** On 248 WSIs / 102 patients (1,566 Silver / 1,546 Gold), six architectures were comparable for tumor vs non-tumor. Higher-parameter models needed about twice the training time (2–3 hours vs 30–60 minutes). CoAtNet-0 had the highest HCN-NOS Dice and AUROC; HCN-NOS is **not** a product requirement. Table: §4.1. The localization model is a swappable callable (REQ-10).

Diagrams (source of truth; do not duplicate):

- [D0 block diagram](Design_Diagrams/D0_block_diagram.png) — components and I1–I15
- [D0 data-flow diagram](Design_Diagrams/D0_dataflow_diagram.png) — collection vs integration
- [D1 data model](Design_Diagrams/D1_data_model.png) — Case, ModalityLink, OutcomesRow, ExclusionLogEntry
- [D2 component error paths](Design_Diagrams/D2_component_error_paths.png) — red arrows
- [D2 case lifecycle](Design_Diagrams/D2_case_lifecycle.png) — scorable vs blocked states

Folder layout under the approved share is D2 Appendix B: `v1/config/`, `v1/incoming/`, `v1/accepted/`, `v1/cases/<study_id>/`, `v1/logs/`.

---

## 3. Interfaces and data formats

**Protocol for every pipeline boundary except I15:** a file written into the case’s folder (or `incoming/` / `accepted/` / `logs/`) on the approved share. I15 is a pathologist opening PathPresenter. Nothing in this section is a consumer-cloud API. Study IDs stand in for patient names.

There is **no HTTP API** (Won’t list; CON-02; D0 D-03; D1 D1-04). The contract is versioned JSON/CSV schemas plus the logical operations below. That operations table is the endpoint table for this project.

Full field tables live in D0 §4, D1 §5, and D2 §2. This section states inputs, outputs, format, protocol, and error behavior for every boundary, then the logical operations and the error catalog.

### 3.1 Component-boundary table (I1–I18)

| ID | From → to | Inputs | Outputs | Format | Error behavior |
|---|---|---|---|---|---|
| I1 | Radiology team → Identifier gate | DICOM, `study_id` | Three-way gate record | DICOM + `gate_status.json` | Not DICOM, leftover identifier, or burned-in pixels: leave in `incoming/`. Status names field **type**, never the value. |
| I2 | Molecular source → Identifier gate | Workbook, `study_id` | Same three-way record | `.xlsx` + `gate_status.json` | Non-Excel → `E_UNKNOWN_FORMAT`, blocked. Identifier columns dropped or file blocked. |
| I3 | Gate → Radiology intake | Accepted DICOM, pass record | Link or unmatched | DICOM + `radiology.json` | 0 or >1 cohort hits → `unmatched`, no guess. No DICOM conversion. |
| I4 | Gate → Genomics intake | Accepted `.xlsx`, pass record | Link or unmatched | `.xlsx` + `molecular.json` | Same unmatched rule as I3. Non-Excel never arrives (I2). |
| I5 | Outcomes sheet → Outcomes cleaner | `.xlsx` (may include Epic-derived fields), cohort list, agreed fields, join column | Ready row and/or exclusions + three counts | `outcomes.json`; exclusions JSONL | Unmatched / `ambiguous_join` / `field_not_coded`: exclude; log `study_id` and field name. Missing join column: fail the run, no silent rename. |
| I6 | Pathology pipeline → Case index | `study_id`, localization pointer | Membership record | JSON pointer (file stays in place) | Unknown `study_id` → `in_cohort = false`; no new patient created. |
| I7 | Radiology intake → Case index | DICOM link status | Updated case link | JSON + `annotation_status` | Unmatched I3 → radiology recorded not linked. No score implied. |
| I8 | Genomics intake → Case index | Workbook link status | Updated case link | JSON | Same as I7 for the molecular slot. |
| I9 | Outcomes cleaner → Case index | Ready row or exclusion | Updated case link | CSV/JSON or exclusion JSON | Exclusion → `outcomes: not_model_ready` plus I5 reason. |
| I10 | Case index → Integrator | Case link | Same record, read at integration | `case_link.json` | Not in cohort → integrator does not run. |
| I11 | Pathology pipeline → Integrator | Localization pointer | Slot marked present | JSON pointer, read-only | Unresolved pointer → `E_PATHOLOGY_POINTER_MISSING`; the localization model is not retrained as a side effect. |
| I12 | Integrator → Risk scorer | One-case input list | `input_list.json` + `assembly_decision` | JSON (example below) | Outcomes not ready: emit list, scorer refuses (REQ-03). No extra modality: `insufficient_modalities`, no predict (REQ-07). |
| I13 | Risk scorer → Review package | I12 list | Score or block, never both | `score_result.json` | REQ-03 / REQ-07 block reasons. `E_MODEL_LOAD` → still build `partial_no_score`. |
| I14 | Review package → PathPresenter | Score result + pointer | Helper files | JSON helper + overlay (OQ-02) | Overlay refused → `viewer_open_failed`; files stay; **no auto-QuPath**. Disclaimer always present. |
| I15 | PathPresenter → Pathologist | I14 files in the viewer | Pathologist review | PathPresenter case view | Blocked score: map + reason still shown, no number. Pathologist owns the read. |
| I16 | Any component → Logging | Component, `run_id`, event | Log line | `v1/logs/…`, no PHI | Unwritable dir → STDERR, stage continues. Sanitizer redacts identifier patterns. |
| I17 | Any component → Configuration | YAML path | Immutable config for that run | `pipeline_config.yaml` | Missing/invalid YAML → refuse to start. Gate must not use a defaulted rule set. |
| I18 | Human or component → status | `study_id` | Combined case status | JSON aggregate | Unknown id → `E_NOT_FOUND`. No empty success. No email or push. |

### 3.2 Logical API (endpoint table)

Callers are other pipeline stages or a teammate’s script on approved storage. Paths are on the approved share, never in Git.

| Operation | Component | Inputs | Outputs | Errors |
|---|---|---|---|---|
| `scan_and_deidentify` | Identifier gate | `incoming_path`, `study_id`, `format`, `rule_set_version` | `gate_status.json`; deidentified file in `accepted/` or block left in `incoming/` | `E_UNKNOWN_FORMAT`, `E_PIXEL_IDENTIFIER`, `E_REDACTION_FAILED`, `E_CONFIG_MISSING_RULES`, `E_IO` |
| `register_radiology` | Radiology intake | `study_id`, deidentified DICOM path, cohort list | `radiology.json`, I7 payload | `E_UNMATCHED_STUDY`, `E_AMBIGUOUS_STUDY`, `E_IO`, `E_SCHEMA` |
| `register_molecular` | Genomics intake | `study_id`, deidentified `.xlsx` path, cohort list | `molecular.json`, I8 payload | `E_UNMATCHED_STUDY`, `E_AMBIGUOUS_STUDY`, `E_IO`, `E_SCHEMA` |
| `run_outcomes_clean` | Outcomes cleaner | workbook path, cohort list path, `agreed_fields`, `join_column` | `outcomes.json` files, exclusions JSONL, summary dict | `E_IO`, `E_MISSING_JOIN_COLUMN`, `E_EMPTY_COHORT`, `E_AGREED_FIELDS_EMPTY` |
| `validate_and_write_case_link` | Cohort case index | path, JSON body | Written `case_link.json` | `E_SCHEMA`, `E_ID_MISMATCH`, `E_PHI_FIELD` |
| `read_case_record` | Cohort case index | `study_id` | Combined case_link + outcomes if present | `E_NOT_FOUND`, `E_SCHEMA` |
| `assemble_input_list` | Modality integrator | `study_id` | `input_list.json` | `E_PATHOLOGY_POINTER_MISSING`, `E_CASE_FOLDER_MISSING`, `E_SCHEMA`, `E_IO` |
| `score_case` | Risk scorer | `study_id`, `model_version` | `score_result.json` | `E_INPUT_LIST_MISSING`, `E_MODEL_LOAD`, `E_FEATURE_MISSING`, `E_MODEL_OUT_OF_RANGE`, `E_IO` |
| `run_localization` | Existing pathology pipeline | `study_id`, `model_version` | localization artifact + pointer | `E_MODEL_LOAD`, `E_IO`. Schema of the pointer does not change with `model_version` (REQ-10). |
| `build_review_package` | Review package | `study_id` | `review_package.json`, overlay + helper under `review/` | `E_LOCALIZATION_UNRESOLVED`, `E_SCORE_FILE_MISSING`, `E_OVERLAY_WRITE`, `E_IO` |
| `mark_viewer_result` | Review package | `study_id`, `opened`, `note?` | Updated `package_status` | `E_NOT_FOUND` |
| `load_config` | Configuration | path to YAML | parsed config | `E_CONFIG_NOT_FOUND`, `E_CONFIG_SCHEMA`, `E_CONFIG_PATH_INVALID` |
| `get_logger` / `log_event` | Logging | component, `run_id`, event | log line | `E_LOG_PATH_INVALID` |
| `read_case_status` | Notifications (pull) | `study_id` | combined status | `E_NOT_FOUND`, `E_SCHEMA` |

OS-level `E_PERMISSION_DENIED` (SSO expired or ACL deny) is not retried. The stage halts; a human re-authenticates and restarts the run.

### 3.3 Principal schemas (v1/)

Breaking field changes require `v2/` (NFR-05). Adding an optional field may stay in `v1/`. Forbidden keys on every schema: patient name, MRN, DOB, street address (`E_PHI_FIELD`).

**`case_link.json`** (D1): `study_id` (string, equals folder name), `in_cohort` (bool), `localization_pointer` (string or null), `modalities` object with keys subset of `radiology` / `molecular` / `pathology`, each with `status` ∈ {`linked`, `not_linked`, `unmatched`} and optional `artifact_path`, `outcomes.status` ∈ {`model_ready`, `not_model_ready`, `absent`}. Optional `model_version` on the pathology pointer is allowed in `v1/` (non-breaking add; REQ-10).

**`outcomes.json`** (D1): `study_id`, `ready = true`, `exclusion_reason = null`, `field_payload` object whose keys ⊆ `agreed_fields` and whose values are coded or numeric.

**Exclusions JSONL** (D1): `study_id_attempted`, `reason` ∈ {`unmatched`, `ambiguous_join`, `field_not_coded`}, `field_name` required when reason is `field_not_coded`.

**`gate_status.json`** (D2): `decision` ∈ {`passed`, `passed_with_redaction`, `blocked`}, `redactions[]` of `{field_type, action, location_hint}`, `rule_set_version`. Identifier **values** are not stored.

**`radiology.json` / `molecular.json`** (D2): `link_status`; radiology also has `annotation_status` ∈ {`present`, `pending`, `not_required`}. A DICOM counts toward REQ-07 only when `annotation_status = present`.

**`input_list.json`** (I12 example, radiology not collected yet):

```json
{
  "study_id": "HF-0102",
  "inputs": [
    {"name": "pathology_localization", "status": "linked", "source": "existing_pipeline"},
    {"name": "radiology", "status": "not_linked", "format": "DICOM"},
    {"name": "molecular", "status": "linked", "format": "xlsx"},
    {"name": "clinical_outcomes", "status": "model_ready"}
  ],
  "viewer_target": "PathPresenter",
  "assembly_decision": "sufficient",
  "rule_set_version": "2026-10-14",
  "assembled_at": "2027-04-10T14:00:00Z"
}
```

Under REQ-07 this payload is `sufficient` because molecular is linked. If molecular were also `not_linked`, `assembly_decision` would be `insufficient_modalities` and `score_case` would not predict.

**`score_result.json`:** `score` number in `[0.0, 1.0]` or null; `used_inputs` subset of `{pathology_localization, radiology, molecular, clinical_outcomes}`; `block_reason` null iff `score` is set; `disclaimer` must contain “research prototype, not a diagnostic device”; `model_version`; `rule_set_version`.

**`review_package.json`:** `package_status` ∈ {`built`, `viewer_open_failed`, `partial_no_score`}; `files_written`; `disclaimer` always present.

**`pipeline_config.yaml`:** `paths`, `identifier_rules` (OQ-01), `agreed_fields`, `scoring.model_version` (OQ-04), `localization.model_version` (OQ-07 / REQ-10), `logging.retention_days` (default 90, OQ-03). No credentials in this file.

Cleaner success summary (I5):

```json
{
  "schema_root": "hepato_fusion/v1",
  "source_rows": 120,
  "kept": 98,
  "excluded": 22,
  "exclusion_breakdown": {
    "unmatched": 10,
    "ambiguous_join": 2,
    "field_not_coded": 10
  }
}
```

Error body (same shape for every logical operation):

```json
{
  "ok": false,
  "error": "E_MISSING_JOIN_COLUMN",
  "message": "join_column study_id not present in workbook header",
  "study_id": null
}
```

### 3.4 Error catalog

Named codes used above: `E_UNKNOWN_FORMAT`, `E_PIXEL_IDENTIFIER`, `E_REDACTION_FAILED`, `E_CONFIG_MISSING_RULES`, `E_CONFIG_NOT_FOUND`, `E_CONFIG_SCHEMA`, `E_UNMATCHED_STUDY`, `E_AMBIGUOUS_STUDY`, `E_MISSING_JOIN_COLUMN`, `E_EMPTY_COHORT`, `E_AGREED_FIELDS_EMPTY`, `E_ID_MISMATCH`, `E_PHI_FIELD`, `E_SCHEMA`, `E_PATHOLOGY_POINTER_MISSING`, `E_CASE_FOLDER_MISSING`, `E_FEATURE_MISSING`, `E_MODEL_LOAD`, `E_MODEL_OUT_OF_RANGE`, `E_LOCALIZATION_UNRESOLVED`, `E_OVERLAY_WRITE`, `E_PERMISSION_DENIED`, `E_NOT_FOUND`.

Rules that apply to all of them: do not guess a `study_id`; do not fabricate missing features as zeros; do not run the gate on a defaulted rule set; do not auto-fall-back to QuPath; SSO denials are not retried. Full edge-case rows (E-01–E-43) stay in [D2 §3](Design_Diagrams/D2_Detailed_Design.md).

---

## 4. Technology stack

| Layer | Choice | Justification (tied to an ID) |
|---|---|---|
| Architecture | File pipeline, one case folder per `study_id` | CON-02 and CON-05 forbid a cloud client-server app. REQ-05 / REQ-06 / REQ-09 are collection and join problems, not a live multi-user service. D0 D-01 rejected microservices for a two-person team with no deployment environment this year. |
| Runtime / language | Python 3 on approved compute | CON-04 (reuse the existing PyTorch pathology stack; no new vendor). NFR-01 is a batch CPU bound, not a service SLA. |
| Case store | JSON and CSV under versioned `v1/` folders on the approved share | NFR-05 (folder versioning). D1 D1-02: SQL is a proposed later migration if joins hurt, not the store for this release. CON-02: the share is already the allowed location. |
| Spreadsheet I/O | pandas + openpyxl | REQ-05 / NFR-01. Permissive licenses (BSD-3 / MIT) satisfy CON-04. Microsoft Graph remains a human-side option only if the hospital allow-list says so; it is not the pipeline store. |
| Identifier scan | Config-driven tag/column rules; pydicom as the DICOM metadata reader (candidate) | REQ-06, NFR-02, OQ-01. Pixel OCR is **not** a redaction tool; a burned-in hit is `E_PIXEL_IDENTIFIER` (block). |
| Configuration | One PyYAML file, `pipeline_config.yaml` | REQ-06 / OQ-01 (identifier list changes without a code change). REQ-10 (`localization.model_version`). NFR-05 (`rule_set_version` written into every output). CON-02: no secrets in the file; SSO holds credentials. |
| Logging | Python stdlib `logging`, per-component files | NFR-02 (sanitizer, no PHI in the message field). NFR-04 (stage artifacts do not depend on log success). |
| Authentication | Hospital / UC SSO + folder ACL | CON-02, NFR-02. D1 build-versus-reuse: do not hand-roll auth. |
| Notifications | None pushed; `read_case_status` only | CON-02 (no approved PHI-adjacent SMTP/chat channel). Week 8 Won’t list. |
| Existing pathology model | Swappable PyTorch callable. Six architectures compared (§4.1). Weights on approved compute. | REQ-10, REQ-01, CON-04, A-01, A-06. Fine-tune on cleaned Gold is allowed (T7). **Freezing one official backbone this year is Won’t.** HCN-NOS is not a product feature. |
| Risk model | Swappable callable; winner of holdout comparison recorded as `model_version` | REQ-02 Could, OQ-04. Interface is specified so a model change does not change file schemas (D2 R-04). |
| Primary viewer | PathPresenter | REQ-01, NFR-03. Pathologist already has an account; no custom login. |
| Alternate / research viewers | QuPath (Docker of current weights); ImageScope and side-by-side 2–4 `.svs` files under research (OQ-06) | REQ-01 if OQ-02 stays open (OQ-05, OQ-06). CON-04: Docker on approved compute, not a purchased viewer platform. No automatic fallback (Won’t). |
| Rejected | Postgres/SQLite as the D1 store; Node/React custom viewer; consumer cloud (AWS/GCP student APIs, Colab) for PHI; HCN-NOS overlay as a deliverable | CON-02, CON-04. SQL remains a **proposed** migration only. |

### 4.1 Pathology architecture comparison (approved-compute analysis)

Team analysis on **248 WSIs, 102 patients**, **1,566 Silver / 1,546 Gold** annotations. Higher-parameter models showed modest gains and at least twice the training time (2–3 hours vs 30–60 minutes). All six were comparable for tumor vs non-tumor. HCN-NOS was best identified by CoAtNet-0; that finding is **not** a requirement (Requirements Document §4 glossary; Won’t list).

| Metric | U-Net | ConvNeXt-Tiny | ViT-Tiny/16 | Swin V2-Tiny | MobileViTv2-1.0 | CoAtNet-0 |
|---|---:|---:|---:|---:|---:|---:|
| Tumor Dice | 0.96 | 0.97 | 0.95 | 0.97 | 0.97 | 0.98 |
| Tumor IoU | 0.92 | 0.95 | 0.90 | 0.93 | 0.95 | 0.94 |
| Tumor mean slide Dice | 0.94 | 0.97 | 0.93 | 0.95 | 0.97 | 0.96 |
| Tumor AUROC | 0.99 | 0.99 | 0.98 | 0.99 | 0.99 | 0.99 |
| HCN-NOS Dice | 0.65 | 0.71 | 0.61 | 0.69 | 0.70 | 0.72 |
| HCN-NOS AUROC | 0.81 | 0.81 | 0.81 | 0.82 | 0.79 | 0.84 |

**How this is used.** Outlier finding (T6) and fine-tune (T7) may load any of these as `localization.model_version`. File schemas do not change (REQ-10). Project Description baseline for “did fine-tune help?” remains the U-Net numbers already published (0.96 mean slide Dice / 0.99 tumor AUROC) until a new holdout table exists (M26). Gold vs Silver: expert annotations improved subtype-style metrics in this analysis; Silver is still not ground truth (CON-01).

This work is a foundation for a later multimodal risk score (REQ-02 Could). It does not make that score a Must.

---

## 5. Known constraints (consequences)

Each CON from Requirements Document v1.0 §8, restated with what it **rules out** or **forces**.

| ID | Restated constraint | Forces | Rules out |
|---|---|---|---|
| CON-01 | Pediatric decision support; pathologist owns the read; Silver is not ground truth. | Disclaimer string on every review package and score result (REQ-01, REQ-02). Gold-only evaluation claims. HCN-NOS stays a research number, not a diagnosis. | Presenting Silver as truth in a demo. Any wording that the score or overlay is a diagnosis. |
| CON-02 | PHI off personal devices, off this Git repository, off consumer cloud; train and infer on approved compute. | Approved-share file pipeline; Identifier gate before `accepted/` (REQ-06); SSO/ACL; log sanitizer (NFR-02). | Public HTTP API. Cloud notebooks as a data path. Committing WSI, DICOM, or identified Excel. Storing MRN/name/DOB/address as schema fields. |
| CON-03 | Data-use agreements, UC IP rules, research prototype only. | Partner slides stay on approved channels. Deliverables labeled research prototype. | FDA / 510(k) / diagnostic-device claims. Redistributing partner slides with a course PDF or Git LFS. |
| CON-04 | No commercial budget beyond UC / CCHMC facilities and existing compute. | Open-source Python stack; reuse of the existing Silver/Gold stream and compared PyTorch architectures. Viewer research stays on tools already available (PathPresenter, QuPath, ImageScope). | Purchasing a commercial pathology platform or a new labeled dataset to “speed up” fusion. |
| CON-05 | When privacy isolation conflicts with speed or multimodal scale, compliance wins. | Week 8 ice on Radiology intake, Genomics intake, integrator, and scorer until extra modalities actually exist (REQ-02 Could). Must this year is cleanup (REQ-05, REQ-06, REQ-09). | Treating a fused risk score as a December 2026 Must. Skipping the gate to move faster. Scoring pathology + outcomes only so that a number exists for a demo. Freezing CoAtNet-0 (or any other backbone) just because one subtype metric was highest. |

---

## 6. Traceability matrix

Traces to **Requirements Document version 1.0 (30 October 2026)**. Columns are exactly those required for Week 9. Status is **Designed**, **In progress**, or **Planned**. Test Case is the Week 10 ID. No Design Component cell is blank. No row is ORPHANED.

| Req ID | Description | Design Component (D0/D1/D2) | Status | Test Case |
|---|---|---|---|---|
| REQ-01 | Existing tumor localization available as helper files / viewer, with prototype disclaimer; no automatic QuPath fallback | D0 Review package and PathPresenter (I14, I15); D2 §2.7 ReviewPackage, states `InReviewPackage` → `OpenedInViewer` / `ViewerOpenFailed`; E-32, E-33; OQ-06 ImageScope research | Planned | TC-001 |
| REQ-02 | At most one score in `[0.0, 1.0]`; `used_inputs` names only consumed modalities | D0 Risk scorer (I12, I13); D2 §2.6 ScoreResult; D2 §2.5 IntegratedInputList.inputs | Planned | TC-002 |
| REQ-03 | No numeric score when outcomes are not model-ready; exact block reason | D0 I13; D2 §2.5 `assembly_decision = outcomes_not_ready`; D2 §2.6 `block_reason`; D2 state `Blocked_NoOutcomes`; UC-01 E1 | Designed | TC-003 |
| REQ-04 | Radiology `linked` only on exact-one cohort match; never guess | D0 Radiology intake (I3, I7); D2 §2.3 RadiologyRecord.link_status; D1 Cohort case index ModalityLink; E-06, E-09 | Planned | TC-004 |
| REQ-05 | Outcomes keep iff exact-one join and agreed fields ready; three counts; named exclusions; Epic-derived fields allowed as source | D0 Outcomes cleaner (I5, I9); D1 ALG-01, OutcomesRow, ExclusionLogEntry; D2 E-14, E-16, E-17 | Planned | TC-005 |
| REQ-06 | Gate pass / pass-with-redaction / block; no identifier values in status JSON or Git | D0 Identifier gate (I1, I2); D2 §2.2 GateRecord and RedactionEntry; D2 §2.9 `identifier_rules`; E-04, E-05, E-40 | In progress | TC-006 |
| REQ-07 | Score only if pathology + model-ready outcomes + (annotated radiology **or** molecular) | D2 §2.5 assembler (replaces D0 D-06); D2 state `Blocked_InsufficientModalities`; E-22 | Designed | TC-007 |
| REQ-08 | Molecular intake `.xlsx` only; other types blocked at the gate | D0 D-05; D0 I2; D2 §2.4 GenomicsRecord; E-12 | Designed | TC-008 |
| REQ-09 | One `case_link.json` per inventoried `study_id`; `in_cohort` and localization pointer; no PHI fields | D0 Cohort case index (I6); D1 Case + ModalityLink; D1 `validate_and_write_case_link`; Week 8 T2/T5 | Planned | TC-015 |
| REQ-10 | Pathology `model_version` swappable among evaluated architectures; pointer schema unchanged | Existing pathology pipeline (D0 dashed); D2 R-04 analog; `pipeline_config.yaml` `localization.model_version`; this document §4.1; T6/T7 | In progress | TC-016 |
| NFR-01 | Cleaner: ≤ 2,000 rows, ≤ 200 cohort IDs, ≤ 120 s on approved CPU | D1 ALG-01 complexity note; D1 §6 pandas/openpyxl; Outcomes cleaner I5 | Designed | TC-009 |
| NFR-02 | 100% of new radiology/molecular files gated; SSO/ACL only; 0 identifier values in Git or logs | D2 §2.2 Identifier gate; D2 §2.8 Authentication; D2 §2.10 log sanitizer (E-40); D2 §2.9 `paths.approved_root` | In progress | TC-010 |
| NFR-03 | Pathologist finds overlay and score-or-reason in ≤ 5 minutes in an existing viewer, ≥ 2 of 3 cases | D0 I15 PathPresenter; D2 §2.7 Review package; D0 D-08 QuPath alternate; OQ-06; Week 8 T14 | Planned | TC-011 |
| NFR-04 | `.part` + rename; crash mid-write never yields a silently truncated valid record; 10/10 trials | D2 E-13, E-15, E-19, E-31; D1 `validate_and_write_case_link` | Designed | TC-012 |
| NFR-05 | Breaking schema change published as `v2/`; `v1/` remains readable | D1 §5 versioning; D2 §2.9 `paths.cases_root`; D1 D1-05 | Designed | TC-013 |
| CON-01 | Decision support; Silver not ground truth; disclaimer required | D0 I14 disclaimer; D2 §2.6 ScoreResult.disclaimer; D2 §2.7 ReviewPackage.disclaimer | Designed | TC-001 |
| CON-02 | PHI off personal devices, Git, and consumer cloud; approved compute only | D0 transport rule; D2 Identifier gate + Logging sanitizer + `approved_root`; D1 §6 hosting | In progress | TC-010 |
| CON-03 | Data-use agreements; research prototype; no FDA claim; no slide redistribution | D2 disclaimer fields; Review package files stay on the approved share, not Git (I14) | Designed | TC-001 |
| CON-04 | No commercial budget; open-source stack; reuse existing Silver/Gold | D1 §4 build-versus-reuse; D1 §6 Python / pandas / openpyxl; this document §4 stack table and §4.1 | Designed | TC-014 |
| CON-05 | Compliance-first: delay fusion rather than skip isolation or score on pathology-only | D2 R-02 / REQ-07; Week 8 ice of T15/T16 until M36; Requirements Document §7 Could / Won’t | Designed | TC-007 |

Week 10 will specify procedure, fixtures, and pass/fail for TC-001–TC-016. IDs above are reserved so they are not reused. TC-014 is an inspection of the §4 stack (Python, pandas, openpyxl, existing PyTorch localization stack; no commercial pathology platform on the bill). TC-015 inspects inventory vs `case_link.json` count. TC-016 runs two `model_version` values and checks the pointer schema is unchanged.

---

## 7. Record of advisor review

**Meetings recorded here.** Team meeting **21 October 2026**. Advisor review with Dr. Kalyani Patel **29 October 2026**. These meetings produced the edits listed below, which are already applied in Requirements Document v1.0 and in this Technical Specification v1.0.

| Field | Record |
|---|---|
| Date | Team meeting 21 October 2026. Advisor review with Dr. Patel 29 October 2026. |
| Attendees | 21 Oct: Shivam Sinay Kharangate, Nipun Chandra. 29 Oct: Dr. Kalyani Patel; Shivam Sinay Kharangate; Nipun Chandra. |
| Materials | Then-current D0–D2, Week 8 plan, pathology model-comparison table, viewer options |
| What was discussed | **21 Oct (team):** (1) **Find outliers** on the existing localization so the team can see how to fine-tune. (2) **Model-prediction analysis** across six architectures (this document §4.1); no backbone frozen because the pipeline already allows a swap and the same run/test path. (3) **Model export into a viewing tool**: QuPath, PathPresenter, and a broad look at other open-source viewers (including ImageScope); possible **side-by-side** viewing of 2–4 `.svs` files so model output can be compared. **29 Oct (Dr. Patel):** **Must for this academic year is data cleanup and finalization**, including Epic field search — not a fused risk score. |
| Changes this review produced | **Must set narrowed** to REQ-05, REQ-06, REQ-09, NFR-02 (Requirements Document §7) from the 29 Oct advisor meeting. **REQ-10 added** (swappable `model_version`; six architectures stay in play) and **OQ-06 added** (viewer research: ImageScope, side-by-side `.svs`) from the 21 Oct team meeting. **HCN-NOS kept as glossary-only**, not a product requirement. **§4.1 comparison table** added here. Week 8 tasks T6 (outliers) and T7 (fine-tune) confirmed, still on the existing pathology pipeline, not a new D0 box. No REQ / NFR / CON ID was reused. |

Prior advisor decisions already in force before this meeting: two-semester commitment through April 2027; research-prototype framing; PathPresenter as the hospital-facing viewer; PHI never in Git (`Team_Contract.md` signed KP 17 September 2026).
