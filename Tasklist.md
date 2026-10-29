# Tasklist.md

**Project:** HepatoFusion  
**Course:** CS 5001 Senior Design Project I / CS 5002 Senior Design Project II  
**Team members:** Shivam Sinay Kharangate, Nipun Chandra  
**Advisor:** Dr. Kalyani Patel, Department of Pathology and Laboratory Medicine, Cincinnati Children’s Hospital  
**Date:** 27 October 2026

This file is the Assignment #5 Task List. The same IDs, statements, modules, and owners are used in `Planning/A5_A6_Implementation_Plan.md` (milestones, Table 1, Table 2, work breakdown structure, and risk register).

## Scope used to build this list

D2 closed the design of the full file pipeline in `Design_Diagrams/D0_High_Level_Design.md`, `Design_Diagrams/D1_Detailed_Design.md`, and `Design_Diagrams/D2_Detailed_Design.md`. Implementation does **not** start every D0 component at once.

**In scope now (pathology-available work, through at least December 2026):**

- Patient-by-patient cleanup of the clinical-outcomes spreadsheet, including specific fields pulled from Epic, for the **Outcomes cleaner** (D1 ALG-01, US-04 / UC-02).
- Slide and case inventory from eSlide Manager and PathPresenter for the **Cohort case index** and the **existing pathology pipeline**.
- Immunohistochemistry (IHC) as additional pathology evidence joined through the **Cohort case index**. IHC was not a named D0 box; it is a pathology input to that index, not a new architecture.
- Fine-tuning of the existing pathology U-Net (outlier review, then refine), then a Docker image for **QuPath** and helper-file wiring for **PathPresenter** through the **Review package** (US-01, OQ-02, OQ-05).

**Parked on ice until that pathology data is model-ready:** **Radiology intake** (except the TMA-grid side project below), **Genomics intake**, **Modality integrator**, and **Risk scorer**. D2’s partial-score rule still stands: a score is produced only when pathology + cleaned outcomes + at least one of {radiology, molecular} are present. Those components stay in the work breakdown structure so the design is not rewritten; they do not consume the fall calendar.

**Side project (does not block the pathology path):** a TMA (tissue microarray) grid list, searched on approved Cincinnati Children’s systems, handed to the radiology collaborator so **Radiology intake** has a real incoming set later. MRNs and other identifiers never enter this Git repository (US-05, Identifier gate, Week 3 constraints).

External hospital systems used as sources, not as new D0 components: Epic, eSlide Manager, PathPresenter, QuPath, radiology collaborators.

## Owners

| Short name | Full name | Primary focus (Team_Contract.md) |
|---|---|---|
| Shivam | Shivam Sinay Kharangate | Pathology CV / multimodal ML; clinical stakeholder liaison |
| Nipun | Nipun Chandra | Data engineering / systems; ingestion, pipeline reliability, repo hygiene |

Eight tasks each. Each task is sized to about one or two weeks of owned work. Primary owner is the person named at the end of the statement.

## Task List

T1. Obtain Epic clinical-outcome fields for the existing 102+ patient cohort and deliver them to the Outcomes cleaner on approved Cincinnati Children’s storage. Owner: Shivam.

T2. Obtain the whole-slide inventory from eSlide Manager and PathPresenter and record study-ID membership in the Cohort case index. Owner: Nipun.

T3. Develop patient-by-patient cleanup of the clinical-outcomes spreadsheet so each agreed field is coded or numeric for the Outcomes cleaner. Owner: Nipun.

T4. Investigate immunohistochemistry (IHC) slide availability in eSlide Manager and PathPresenter and specify how IHC joins the Cohort case index. Owner: Shivam.

T5. Develop Cohort case index `case_link.json` records for cleaned pathology cases, including IHC when present and radiology as `not_linked`. Owner: Nipun.

T6. Investigate pathology U-Net outlier slides against Gold annotations in the existing pathology pipeline. Owner: Shivam.

T7. Refine the pathology U-Net on cleaned Gold labels after outlier review in the existing pathology pipeline. Owner: Shivam.

T8. Develop a Docker image of the pathology U-Net for QuPath inference on approved compute. Owner: Nipun.

T9. Research the PathPresenter overlay format (OQ-02) and develop Review package helper files for the existing tumor localization. Owner: Shivam.

T10. Test QuPath loading of the Dockerized U-Net on a holdout whole-slide image with no PHI in the course repository. Owner: Nipun.

T11. Obtain TMA-grid study keys on approved hospital systems for the radiology-collaborator handoff that will later feed Radiology intake. Owner: Shivam.

T12. Specify Identifier gate `identifier_rules` in `pipeline_config.yaml` for Epic and TMA exports before any file leaves the clinical system. Owner: Nipun.

T13. Develop the Outcomes cleaner ALG-01 run on the cleaned workbook and write model-ready `outcomes.json` plus the exclusion log. Owner: Nipun.

T14. Validate Review package open of the existing tumor localization inside PathPresenter with Dr. Patel. Owner: Shivam.

T15. Design Radiology intake registration for TMA-returned DICOM (parked until collaborators return studies). Owner: Nipun.

T16. Develop the Modality integrator `input_list.json` under the D2 partial-score rule (parked until pathology, cleaned outcomes, and at least one extra modality are linked). Owner: Shivam.

## Module map

Every task names a D0–D2 component or named external system from those diagrams.

| ID | D0–D2 module or named external system | Requirement |
|---|---|---|
| T1 | Outcomes cleaner | US-04, UC-02 |
| T2 | Cohort case index; existing pathology pipeline; PathPresenter | I6, US-03 membership |
| T3 | Outcomes cleaner | US-04, UC-02 |
| T4 | Cohort case index; existing pathology pipeline | I6 |
| T5 | Cohort case index | I6, I7, I9, I10 |
| T6 | Existing pathology pipeline | Project Description pathology backbone |
| T7 | Existing pathology pipeline | Project Description pathology backbone |
| T8 | QuPath; Review package | D0 D-08, OQ-05 |
| T9 | Review package; PathPresenter | US-01, OQ-02, I14 |
| T10 | QuPath | OQ-05 |
| T11 | Radiology intake (side project only) | US-03 |
| T12 | Identifier gate; Configuration | US-05, OQ-01, I17 |
| T13 | Outcomes cleaner | US-04, UC-02, ALG-01 |
| T14 | Review package; PathPresenter | US-01, I15 |
| T15 | Radiology intake (ice) | US-03, I3, I7 |
| T16 | Modality integrator (ice) | US-02, I10–I12 |

**Genomics intake**, **Risk scorer**, **Authentication**, **Logging**, and **Notifications** have no numbered task in this list. They remain in the work breakdown structure as ice or glue: Authentication stays hospital/UC SSO (D2 §2.8); Logging is produced by T5 and T13 writes; Notifications stay pull-only `read_case_status` (I18); Genomics intake and Risk scorer stay parked with Radiology intake and the Modality integrator.
