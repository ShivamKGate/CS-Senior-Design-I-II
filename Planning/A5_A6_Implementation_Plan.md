# HepatoFusion — Assignments #5 and #6

**Task List, Milestones, Timeline, Effort Matrix, Work Breakdown Structure, and Risk Register**

**Project:** HepatoFusion  
**Team members:** Shivam Sinay Kharangate (sinayksp@mail.uc.edu), Nipun Chandra (chandrnu@mail.uc.edu)  
**Advisor:** Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children’s Hospital  
**Additional advisors:** Dr. Sangaranjan Ranganathan, Dr. Surya Prasath, Christopher Woods  
**Partner:** Cincinnati Children’s Hospital  
**Courses:** CS 5001 Senior Design I (Fall 2026) and CS 5002 Senior Design II (Spring 2027)  
**Document date:** 28 October 2026  
**Canonical task file:** [`../Tasklist.md`](../Tasklist.md)

Each student submits this PDF separately. Both names appear on page 1. No PHI, MRNs, or slide files are in this document or in Git.

**AI use.** An AI tool helped format the tables. Task content, ownership, parked-vs-active scope, dates, hours, and risks are the team’s, confirmed by both members on 28 October 2026.

---

## 0. Scope control

D2 closed detailed design for the full pipeline: Identifier gate, Radiology intake, Genomics intake, Outcomes cleaner, Cohort case index, Modality integrator, Risk scorer, Review package, plus glue (Authentication, Notifications, Configuration, Logging). Implementation does **not** start every component at once.

| Status | What | Why |
|---|---|---|
| **Active through December 2026** | Epic → Outcomes cleaner; eSlide Manager / PathPresenter → Cohort case index; Excel coding; IHC join spec | The spreadsheet and slide inventory are not model-ready. |
| **Active in parallel, then Spring 2027** | Existing pathology pipeline fine-tuning; Docker image for QuPath; Review package → PathPresenter | US-01: pathologist sees the tumor map in a tool already in the workflow. QuPath is the executable landing if PathPresenter overlay format (OQ-02) stays open. |
| **Side project, does not block pathology** | TMA grid study keys for the radiology collaborator | Starts the radiology data path without building Radiology intake this semester. |
| **On ice** | Radiology intake (beyond TMA keys), Genomics intake, Modality integrator, Risk scorer | D2 partial-score rule still requires pathology + cleaned outcomes + at least one of {radiology, molecular}. Ice is a date decision, not a design change. |

IHC is not a new D0 box. It is additional pathology evidence recorded on the **Cohort case index**. Epic and eSlide Manager are external hospital systems, like the Outcomes spreadsheet and PathPresenter already drawn as dashed boxes.

Protected calendar: Thanksgiving 26–29 Nov 2026; exam week 6–12 Dec 2026; winter break 13 Dec 2026 – 10 Jan 2027; MLK Day 18 Jan 2027; spring break 15–21 Mar 2027; CS 5002 exam week 24–29 Apr 2027. Neither member is on a co-op rotation this academic year. Classes end 5 Dec 2026 (Fall) and 23 Apr 2027 (Spring).

### 0.1 Owners

| Short name | Full name | Primary focus (`Team_Contract.md`) |
|---|---|---|
| Shivam | Shivam Sinay Kharangate | Pathology CV / multimodal ML; WSI pipeline; U-Net; clinical liaison |
| Nipun | Nipun Chandra | Data engineering / systems; ingestion; pipeline reliability; documentation |

### 0.2 Course calendar (Week 1 14-week roadmap)

Weeks and graded components are taken from *CS 5001 Week 1: Course Overview & Team Formation* (Justin Zhan). Completed dates are this team’s repository commits. Remaining CS 5001 Fridays run from this Week 8 submission through the last instructional week (classes end 5 Dec 2026).

| Week | Topic (Week 1 slide 13) | Graded component (slide 12) | Date | Status |
|---|---|---|---|---|
| 1 | Course Overview & Teams | Team contract and team formation (5%) | 29 Aug 2026 | **Complete** — repo, roster |
| 2 | Problem Framing & Topics | Topic statement, bios, and reflective essay (10%) | 9 Sep 2026 | **Complete** |
| 3 | Advisors & Constraints | Advisor selection and constraints essay (5%) | 17–18 Sep 2026 | **Complete** |
| 4 | Requirements Elicitation | User Stories | 28 Sep 2026 | **Complete** |
| 5 | High-Level Architecture | High-level system design (10%) | 2 Oct 2026 | **Complete** — D0 |
| 6 | Detailed Design Part 1 | Detailed system design (15%, split Weeks 6–7) | 8 Oct 2026 | **Complete** — D1 |
| 7 | Detailed Design Part 2 & Reviews | Detailed system design (15%, split Weeks 6–7) | 14 Oct 2026 | **Complete** — D2 + peer review |
| 8 | Project Management | Task timeline and effort matrix (10%) | 30 Oct 2026 | **This submission** |
| 9 | Requirements & Tech Spec Docs | Requirements and technical specification documents (15%) | 6 Nov 2026 | Remaining |
| 10 | Test & Validation Planning | Test and validation plan | 13 Nov 2026 | Remaining |
| 11 | Ethics & Responsible Use | Ethics / responsible-use write-up | 20 Nov 2026 | Remaining |
| 12 | Technical Communication | Technical communication artifact | 25 Nov 2026 | Remaining (short week; Thanksgiving 26–29 Nov) |
| 13 | Oral Presentations I | Oral presentation (15%) | 2 Dec 2026 | Remaining |
| 14 | Oral Presentations II & Wrap-Up | Design report, design notebook, and team assessment (15%) | 4 Dec 2026 | Remaining — report reprints Table 1 and Table 2 |

### 0.3 Effort method (PERT)

Expected hours = (O + 4M + P) / 6, rounded to a whole hour, confirmed by both owners. Calendar span is one or two weeks of owned work, plus **18% duration buffer** in Table 1, plus a **protected block** before each major milestone (Week 14 report, winter break, CS 5002 mid-demo, final presentation).

---

# 1. Task List (Assignment #5)

Sixteen numbered tasks, one statement each, verb-first, one primary owner, mapped to D0–D2 names. Same text as `Tasklist.md`. Eight tasks per member.

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

### 1.1 Module map

| ID | D0–D2 module or named external system | Weeks | Requirement |
|---|---|---|---|
| T1 | Outcomes cleaner | 2 | US-04, UC-02 |
| T2 | Cohort case index; existing pathology pipeline; PathPresenter | 2 | I6 |
| T3 | Outcomes cleaner | 2 | US-04, UC-02 |
| T4 | Cohort case index; existing pathology pipeline | 2 | I6 |
| T5 | Cohort case index | 2 | I6, I7, I9, I10 |
| T6 | Existing pathology pipeline | 2 | Project Description backbone |
| T7 | Existing pathology pipeline | 2 | Project Description backbone |
| T8 | QuPath; Review package | 2 | D0 D-08, OQ-05 |
| T9 | Review package; PathPresenter | 2 | US-01, OQ-02, I14 |
| T10 | QuPath | 2 | OQ-05 |
| T11 | Radiology intake (side project) | 2 | US-03 |
| T12 | Identifier gate; Configuration | 1 | US-05, OQ-01, I17 |
| T13 | Outcomes cleaner | 2 | US-04, ALG-01 |
| T14 | Review package; PathPresenter | 2 | US-01, I15 |
| T15 | Radiology intake (ice) | 2 | US-03, I3, I7 |
| T16 | Modality integrator (ice) | 1 | US-02, I10–I12 |

**Not given a Task List ID on purpose:** Genomics intake, Risk scorer, Authentication, Logging, Notifications. They appear in the work breakdown structure. Authentication remains hospital/UC SSO. Logging is a by-product of T5 and T13. Notifications remain pull-only (`read_case_status`, I18). Genomics intake and Risk scorer stay ice with T15 and T16.

---

# 2. Milestones List (Assignment #6)

A milestone is a dated, checkable outcome, not a task. Verification is what a reviewer can open or watch.

## 2.1 Completed course deliverables

| ID | Milestone | Week 1 topic | Date | What it demonstrates | How verified | By whom | Status |
|---|---|---|---|---|---|---|---|
| M1 | Repository and team roster | W1 Teams | 29 Aug 2026 | Team identity and contact path | Files in repo root | Instructor | **Complete** |
| M2 | Project Description and biographies | W2 Topics | 9 Sep 2026 | HepatoFusion goal, 102+ patient cohort, pathology U-Net metrics, advisor through April 2027 | `Project-Description.md`; bios | Instructor | **Complete** |
| M3 | Team Contract | W1 / W3 | 17 Sep 2026 | Two-person roles, PHI rule, meeting cadence | `Team_Contract.md` signed SK / NC / KP | Advisor + instructor | **Complete** |
| M4 | Constraints Essay | W3 Advisors & Constraints | 18 Sep 2026 | PHI, compute, research-prototype, no FDA claim | `Constraints_Essay_sinayksp.md` | Instructor | **Complete** |
| M5 | User Stories and Use Cases | W4 Requirements Elicitation | 28 Sep 2026 | US-01–US-05, UC-01–UC-02 | `User_Stories.md` | Instructor | **Complete** |
| M6 | D0 High-Level Design | W5 High-Level Architecture | 2 Oct 2026 | Eight built components; PathPresenter first; QuPath alternate | `Design_Diagrams/D0_High_Level_Design.md` | Instructor | **Complete** |
| M7 | D1 Detailed Design | W6 Detailed Design Part 1 | 8 Oct 2026 | Cohort case index; Outcomes cleaner ALG-01 | `Design_Diagrams/D1_Detailed_Design.md` | Instructor | **Complete** |
| M8 | Peer design review | W7 Reviews | 9 Oct 2026 | External critique of D1 before D2 | Review session; notes in `Peer_Review_Notes.md` | Peer teams + instructor | **Complete** |
| M9 | D2 Detailed Design | W7 Detailed Design Part 2 | 14 Oct 2026 | Remaining components, error paths, partial-score rule, OQ-01–OQ-05 | `Design_Diagrams/D2_Detailed_Design.md` | Instructor | **Complete** |

## 2.2 Remaining CS 5001 deliverables through Week 14

| ID | Milestone | Week 1 topic | Date | What it demonstrates | How verified | By whom | Status |
|---|---|---|---|---|---|---|---|
| M10 | Task List + implementation plan | W8 Project Management | 30 Oct 2026 | Sixteen owned tasks, dates, 50/50 hours, risks | `Tasklist.md` + this PDF | Instructor; advisor | This submission |
| M11 | Requirements and technical specification documents | W9 Requirements & Tech Spec Docs | 6 Nov 2026 | Specs aligned with D2 and the pathology-first scope, including IHC as pathology evidence | Spec PDF/MD in repo | Instructor | Planned |
| M12 | Test and validation plan | W10 Test & Validation Planning | 13 Nov 2026 | How T10, T13, and T14 are checked with no PHI in Git | Test-plan PDF/MD in repo | Instructor | Planned |
| M13 | Ethics and responsible-use write-up | W11 Ethics & Responsible Use | 20 Nov 2026 | PHI, research-prototype disclaimer, no diagnostic claim | Canvas PDF | Instructor | Planned |
| M14 | Technical communication artifact | W12 Technical Communication | 25 Nov 2026 | Audience-ready write-up of the pathology-first plan | Canvas PDF | Instructor | Planned (before Thanksgiving) |
| M15 | Oral Presentations I | W13 Oral Presentations I | 2 Dec 2026 | Pathology-first plan, ice list, TMA side project, QuPath/PathPresenter path | Live or recorded talk | Instructor; advisor invited | Planned |
| M16 | Oral Presentations II, design report, notebook, team assessment | W14 Wrap-Up | 4 Dec 2026 | Design report reprints Table 1 and Table 2 with actual vs. plan; notebook; team assessment | Report PDF; notebook; Canvas | Instructor; Dr. Patel | Planned |
| M17 | Fall data-cleanup checkpoint | Internal | 4 Dec 2026 | Epic fields landed; eSlide inventory in the Cohort case index; first-pass Excel coded; TMA keys handed off on the hospital side; Identifier gate rules written | Inventory + cleanup counts on approved storage; no PHI in Git | Shivam (clinical); Nipun (files); Dr. Patel (spot-check) | Internal, reported in M16 |

## 2.3 Internal and CS 5002 milestones (every one to three weeks through April 2027)

Winter break is empty on purpose. CS 5002 dates follow the Week 1 “Build & Deliver” semester: implement, test, iterate, handoff documentation, final product, report, and public presentation.

| ID | Milestone | Date | What it demonstrates | How verified | By whom | Status |
|---|---|---|---|---|---|---|
| M18 | Identifier gate rules frozen | 6 Nov 2026 | `identifier_rules` version in `pipeline_config.yaml` | Config on approved share; no identifier values | Nipun; Shivam liaison | Planned |
| M19 | Epic + eSlide extracts exist | 13 Nov 2026 | T1 and T2 produced files on approved storage | Study-ID list (no names) | Shivam; Nipun | Planned |
| M20 | TMA keys delivered to radiology collaborator | 20 Nov 2026 | Side project moved off the search list | Collaborator acknowledgement on the hospital system, not Git | Shivam | Planned |
| M21 | IHC join specified | 21 Nov 2026 | Written rule: how an IHC slide attaches to `case_link.json` | Spec paragraph in repo (no slide files) | Shivam; Dr. Patel | Planned |
| M22 | Thanksgiving / exam / winter protected block | 26 Nov 2026 – 10 Jan 2027 | No task completion dates inside this window | Table 1 empty in this range | Both | Planned |
| M23 | CS 5002 plan freeze | 15 Jan 2027 | Spring owners unchanged unless M16 said otherwise | Advisor meeting note | Dr. Patel | Planned |
| M24 | ALG-01 first clean run | 23 Jan 2027 | Model-ready `outcomes.json` + exclusion log with three counts | Summary dict from ALG-01; no PHI | Nipun; Shivam checks join keys | Planned |
| M25 | Outlier list closed | 4 Dec 2026 (inventory) / 23 Jan 2027 (labels) | Gold slides the U-Net fails, listed by `study_id` | List on approved share | Shivam | Planned |
| M26 | U-Net refinement checkpoint | 30 Jan 2027 | Retrain on cleaned Gold; holdout Dice/AUROC vs. Project Description baseline (0.96 mean slide Dice, 0.99 tumor AUROC). No claim of improvement until the number exists | Metrics table; weights on approved compute | Shivam; Dr. Patel | Planned |
| M27 | QuPath Docker image builds | 30 Jan 2027 | Container runs the current U-Net on approved compute | `docker build` log (no WSI in Git) | Nipun | Planned |
| M28 | CS 5002 progress check 1 | 5 Feb 2027 | Actual vs. Table 1 for T7, T8, T13 | Short PDF; tables reprinted | Instructor; advisor | Planned |
| M29 | QuPath holdout inference | 13 Feb 2027 | Dockerized model opens one holdout WSI in QuPath | Deidentified screenshot on hospital/UC machine | Nipun; Shivam | Planned |
| M30 | Review package overlay prototype | 13 Feb 2027 | Helper files from T9; PathPresenter import tried (OQ-02) | `review_package.json` + viewer_open status | Shivam | Planned |
| M31 | CS 5002 mid-implementation demo | 26 Feb 2027 | Live QuPath Docker inference and/or PathPresenter helper. Disclaimer spoken: research prototype, not a diagnostic device | Demo to advisor and instructor | Both; Dr. Patel | Planned |
| M32 | PathPresenter US-01 validation | 12 Mar 2027 | Dr. Patel opens a deidentified case and sees the existing tumor map as a helper | Advisor written OK | Dr. Patel (verifier); Shivam | Planned |
| M33 | CS 5002 progress check 2 | 12 Mar 2027 | Pre-break status; T14 result; ice/thaw decision for T15 | PDF | Instructor | Planned |
| M34 | Spring break protected block | 15–21 Mar 2027 | No completions | Table 1 | Both | Planned |
| M35 | CS 5002 progress check 3 | 2 Apr 2027 | Effort-matrix actuals | PDF | Instructor | Planned |
| M36 | Ice/thaw gate for radiology | 3 Apr 2027 | If TMA-linked DICOM arrived, T15 is real; if not, T15 is the parked schema only and T16 does not claim a score | Written gate note | Nipun; Shivam | Planned |
| M37 | Integrator dry run or explicit skip | 10 Apr 2027 | `input_list.json` for one case, or a written skip (`insufficient_modalities`) | File or skip note | Shivam | Planned |
| M38 | Final presentation / demo | 16 Apr 2027 | Pathology cleanup, U-Net refinement, QuPath Docker, PathPresenter helper; ice items labeled ice | Talk + demo | Instructor; advisor | Planned |
| M39 | CS 5002 final report | 23 Apr 2027 | Goals vs. achievements; reprinted Table 1–2 with actuals | Final report PDF | Instructor; advisor | Planned |

---

# 3. Table 1 — Timeline (Assignment #6)

One row per Task List item, then one row per milestone completion date. Buffer is explicit: **18% added to each task’s working duration**, plus protected blocks before M16, M22, M31, and M38.

**Critical path (fall checkpoint M17):** T1 → T3 → M17, with T12 on the PHI gate before any export. Parallel: T2 → T4 → T5; T2 → T6; T12 → T11 → M20.

**Critical path (CS 5002 demo M31):** T6 → T7 → T9 and T8 → T10. T14 is the advisor check after that.

**Critical path (optional fusion M37):** T11 → M36 → T15 → T16, and T13 → T16. This path is allowed to stop at M36 without failing the senior-design prototype.

### 3.1 Task rows

| ID | Statement | Owner | Start | Finish (+18%) | Dependencies | Buffer / notes |
|---|---|---|---|---|---|---|
| T12 | Specify Identifier gate `identifier_rules` in `pipeline_config.yaml` | Nipun | 2026-10-28 | 2026-11-06 | None | 1 week + 1d. PHI gate before Epic/TMA leave the clinical system. |
| T1 | Obtain Epic fields for Outcomes cleaner | Shivam | 2026-10-28 | 2026-11-13 | None | 2 weeks + 2d. Hospital access risk R1. |
| T2 | Obtain eSlide Manager / PathPresenter inventory for Cohort case index | Nipun | 2026-10-28 | 2026-11-10 | None | 2 weeks + 2d. Parallel with T1. |
| T11 | Obtain TMA-grid study keys for Radiology intake handoff | Shivam | 2026-11-02 | 2026-11-20 | T12 | 2 weeks + 2d. Side project. Keys stay on hospital systems. |
| T3 | Develop patient-by-patient Excel cleanup for Outcomes cleaner | Nipun | 2026-11-09 | 2026-11-24 | T1 | 2 weeks + 2d. Stops before Thanksgiving. Remaining free-text is R2. |
| T4 | Investigate IHC join into Cohort case index | Shivam | 2026-11-09 | 2026-11-21 | T2 | 2 weeks + 2d. |
| T5 | Develop `case_link.json` records | Nipun | 2026-11-16 | 2026-12-04 | T2, T4; uses T3 as it lands | 2 weeks of work; Thanksgiving pause 26–29 Nov. Radiology slot = `not_linked`. |
| T6 | Investigate U-Net outliers vs Gold | Shivam | 2026-11-16 | 2026-12-04 | T2 | Thanksgiving pause. List by `study_id` only. |
| T13 | Develop Outcomes cleaner ALG-01 run | Nipun | 2027-01-12 | 2027-01-23 | T3, T12 | 2 weeks + 2d after winter. MLK 18 Jan is a day off. |
| T7 | Refine pathology U-Net | Shivam | 2027-01-12 | 2027-01-30 | T6 | 2 weeks + 3d. Train only on approved compute. |
| T8 | Develop Docker image for QuPath | Nipun | 2027-01-12 | 2027-01-30 | None (current weights; swap T7 weights when ready) | 2 weeks + 3d. Parallel with T7 and T13. |
| T9 | Research PathPresenter format; develop Review package | Shivam | 2027-02-01 | 2027-02-13 | T7 (maps); OQ-02 conversation already open | 2 weeks + 2d. If OQ-02 is still closed, T9 still writes GeoJSON + helper JSON (D2). |
| T10 | Test QuPath Docker on holdout WSI | Nipun | 2027-02-01 | 2027-02-13 | T8 | 2 weeks + 2d. Protected 14–25 Feb before M31. |
| T14 | Validate PathPresenter helper with Dr. Patel | Shivam | 2027-03-01 | 2027-03-12 | T9 | 2 weeks. Protected 13 Mar, then spring break. |
| T15 | Design Radiology intake for TMA-returned DICOM | Nipun | 2027-03-23 | 2027-04-03 | T11; **ice unless M36 thaws** | 2 weeks + 2d. If no DICOM, deliverable is the parked schema. |
| T16 | Develop Modality integrator `input_list.json` | Shivam | 2027-04-06 | 2027-04-10 | T5, T13, T15 | 1 week. Ice unless M36 thaws. Protected 11–15 Apr before M38. |

No task completes during 6–12 Dec 2026, 13 Dec 2026 – 10 Jan 2027, 15–21 Mar 2027, or 24–29 Apr 2027.

### 3.2 Milestone rows (planned completion dates)

| ID | Milestone | Planned completion | Depends on |
|---|---|---|---|
| M1–M9 | Completed CS 5001 artifacts | See §2.1 | — |
| M10 | This plan submitted (W8) | 2026-10-30 | — |
| M18 | Identifier gate rules frozen | 2026-11-06 | T12 |
| M11 | Requirements and tech spec docs (W9) | 2026-11-06 | M10 |
| M12 | Test and validation plan (W10) | 2026-11-13 | M10 |
| M19 | Epic + eSlide extracts exist | 2026-11-13 | T1, T2 |
| M20 | TMA keys delivered | 2026-11-20 | T11 |
| M13 | Ethics write-up (W11) | 2026-11-20 | — |
| M21 | IHC join specified | 2026-11-21 | T4 |
| M14 | Technical communication (W12) | 2026-11-25 | — |
| **Protected** | Thanksgiving | 2026-11-26 to 2026-11-29 | — |
| M15 | Oral Presentations I (W13) | 2026-12-02 | M10 |
| M16 | Oral Presentations II + design report (W14) | 2026-12-04 | Table 1–2 reprint; T3 done |
| M17 | Fall data-cleanup checkpoint | 2026-12-04 | T1, T2, T3, T5, T11, T12 |
| M25 | Outlier list closed (inventory pass) | 2026-12-04 | T6 |
| **Protected** | Exams + winter break | 2026-12-06 to 2027-01-10 | — |
| M23 | CS 5002 plan freeze | 2027-01-15 | M16 |
| M24 | ALG-01 first clean run | 2027-01-23 | T13 |
| M25b | Outlier list closed (label pass) | 2027-01-23 | T6 follow-up |
| M26 | U-Net refinement checkpoint | 2027-01-30 | T7 |
| M27 | QuPath Docker builds | 2027-01-30 | T8 |
| M28 | CS 5002 progress check 1 | 2027-02-05 | M26, M27 |
| M29 | QuPath holdout inference | 2027-02-13 | T10 |
| M30 | Review package overlay prototype | 2027-02-13 | T9 |
| **Protected** | Pre-demo buffer | 2027-02-14 to 2027-02-25 | T10, T9 |
| M31 | Mid-implementation demo | 2027-02-26 | M29 or M30 |
| M32 | PathPresenter US-01 validation | 2027-03-12 | T14 |
| M33 | CS 5002 progress check 2 | 2027-03-12 | T14 |
| **Protected** | Spring break | 2027-03-15 to 2027-03-21 | — |
| M35 | CS 5002 progress check 3 | 2027-04-02 | Effort actuals |
| M36 | Ice/thaw gate | 2027-04-03 | T15 |
| M37 | Integrator dry run or skip | 2027-04-10 | T16 |
| **Protected** | Pre-final buffer | 2027-04-11 to 2027-04-15 | — |
| M38 | Final presentation | 2027-04-16 | M29, M32; T15/T16 optional |
| M39 | Final report | 2027-04-23 | All active tasks |

---

# 4. Table 2 — Effort Matrix (Assignment #6)

Hours are PERT expected hours from §0.3, confirmed by both members. The **primary owner is marked \*** and always has the larger share of that row. Secondary hours are review, pairing, or hospital-access support, not a second owner.

### 4.1 Three-point estimates

| ID | O | M | P | Expected (O+4M+P)/6 |
|---|---:|---:|---:|---:|
| T1 | 10 | 16 | 22 | 16 |
| T2 | 8 | 12 | 16 | 12 |
| T3 | 12 | 19 | 32 | 20 |
| T4 | 8 | 12 | 16 | 12 |
| T5 | 8 | 14 | 20 | 14 |
| T6 | 10 | 16 | 22 | 16 |
| T7 | 12 | 18 | 36 | 20 |
| T8 | 10 | 16 | 22 | 16 |
| T9 | 10 | 16 | 22 | 16 |
| T10 | 8 | 12 | 16 | 12 |
| T11 | 6 | 10 | 14 | 10 |
| T12 | 6 | 10 | 14 | 10 |
| T13 | 8 | 14 | 20 | 14 |
| T14 | 6 | 10 | 14 | 10 |
| T15 | 8 | 14 | 20 | 14 |
| T16 | 10 | 16 | 22 | 16 |
| **Total** | | | | **228** |

### 4.2 Matrix (hours)

| Task | Module | Shivam | Nipun | Row total |
|---|---|---:|---:|---:|
| T1 Obtain Epic fields | Outcomes cleaner | **13 \*** | 3 | 16 |
| T2 Obtain eSlide / PathPresenter inventory | Cohort case index | 3 | **9 \*** | 12 |
| T3 Develop Excel cleanup | Outcomes cleaner | 3 | **17 \*** | 20 |
| T4 Investigate IHC join | Cohort case index | **9 \*** | 3 | 12 |
| T5 Develop `case_link.json` | Cohort case index | 3 | **11 \*** | 14 |
| T6 Investigate U-Net outliers | Existing pathology pipeline | **13 \*** | 3 | 16 |
| T7 Refine pathology U-Net | Existing pathology pipeline | **16 \*** | 4 | 20 |
| T8 Develop Docker image for QuPath | QuPath / Review package | 3 | **13 \*** | 16 |
| T9 Research overlay; develop Review package | Review package / PathPresenter | **12 \*** | 4 | 16 |
| T10 Test QuPath Docker inference | QuPath | 3 | **9 \*** | 12 |
| T11 Obtain TMA-grid keys | Radiology intake (side) | **8 \*** | 2 | 10 |
| T12 Specify Identifier gate rules | Identifier gate / Configuration | 2 | **8 \*** | 10 |
| T13 Develop ALG-01 run | Outcomes cleaner | 3 | **11 \*** | 14 |
| T14 Validate PathPresenter helper | Review package / PathPresenter | **8 \*** | 2 | 10 |
| T15 Design Radiology intake (ice) | Radiology intake | 3 | **11 \*** | 14 |
| T16 Develop Modality integrator (ice) | Modality integrator | **12 \*** | 4 | 16 |
| **Column total (hours)** | | **114** | **114** | **228** |
| **Column share** | | **50%** | **50%** | **100%** |

Primary-owner hours (the \* cells): Shivam 91, Nipun 89. Support hours are the remainder.

### 4.3 Balance

Columns are **114 / 114 (50% / 50%)**. No reassignment is required at plan time.

**If actuals drift:**

1. T3 is the overrun candidate (patient-by-patient Excel, pessimistic 32 h). If Nipun exceeds 17 h on T3 before 24 Nov, Shivam takes the next batch of agreed-field coding under Nipun’s protocol. Primary owner of T3 stays Nipun.
2. If T7 GPU time slips, T9 still proceeds with current maps. US-01 does not wait on a better Dice.
3. T15 and T16 are ice. If Spring load is high, drop T16 first (M37 becomes an explicit skip).
4. Week 14 (M16) and CS 5002 progress checks reprint this table with actual hours. The syllabus uses the effort matrix when adjusting individual grades from the team grade.

---

# 5. Work breakdown structure

Two levels: phases, then Task List items. Every T-ID appears exactly once.

```text
HepatoFusion
│
├── 1. Course design (complete; no new Task List IDs)
│     ├── M1–M4  roster, Project Description, Team Contract, Constraints
│     ├── M5     User Stories
│     └── M6–M9  D0, D1, peer review, D2
│
├── 2. Data access and cleanup  [main effort through 4 Dec 2026]
│     ├── T12  Identifier gate + Configuration (`pipeline_config.yaml`)
│     ├── T1   Epic → Outcomes cleaner (obtain)
│     ├── T2   eSlide Manager / PathPresenter → Cohort case index (obtain)
│     ├── T3   Excel patient-by-patient coding (develop)
│     ├── T4   IHC join spec (investigate / specify)
│     ├── T5   `case_link.json` writes, radiology = not_linked (develop)
│     └── T13  ALG-01 model-ready table (develop)   [runs after winter]
│
├── 3. Existing pathology pipeline
│     ├── T6   Outlier investigation vs Gold (investigate)
│     └── T7   U-Net refine on cleaned Gold (refine)
│
├── 4. Viewer integration (US-01)
│     ├── T8   Docker image of U-Net for QuPath (develop)
│     ├── T10  QuPath holdout test (test)
│     ├── T9   Review package + PathPresenter overlay (research / develop)
│     └── T14  PathPresenter validation with Dr. Patel (validate)
│
├── 5. TMA side project (Radiology intake, not on the pathology critical path)
│     └── T11  Study keys for radiology collaborator (obtain)
│
├── 6. On ice until M36
│     ├── T15  Radiology intake for returned DICOM (design)
│     ├── T16  Modality integrator under D2 partial-score rule (develop)
│     ├── (no T-ID) Genomics intake
│     └── (no T-ID) Risk scorer   [interface exists in D2; model is OQ-04]
│
└── 7. Glue already decided in D2 (no extra Task List IDs)
      ├── Authentication  — SSO / folder ACL only
      ├── Logging         — emitted by T5 and T13 writes (I16)
      └── Notifications   — none pushed; I18 status read only
```

---

# 6. Risk register

Seven risks across technical, team, and external. High-impact schedule risks are visible in Table 1 (buffers, ice, protected blocks).

| ID | Category | Risk | Likelihood | Impact | Strategy | Mitigation | Owner | Trigger |
|---|---|---|---|---|---|---|---|---|
| R1 | External | Epic or eSlide Manager access slips, so T1/T2 miss 13 Nov | Medium | High (blocks T3, T5, M17) | Reduce | Start T1/T2 on 28 Oct; 18% buffer; if no extract by **14 Nov**, Shivam escalates to Dr. Patel the same day and T3 runs on fields already in the spreadsheet | Shivam | No approved extract by 14 Nov 2026 |
| R2 | Technical | Outcomes spreadsheet still has free-text after T3 | High | High (T13 and any later score stay blocked; UC-01 E1) | Reduce | T3 stops 24 Nov with a counted leftover list; T13 in January processes only ready rows; `field_not_coded` is success, not failure | Nipun | Kept-row count < 70% of source at M17 |
| R3 | External | PathPresenter overlay format (OQ-02) still unknown in February | Medium | High (US-01 PathPresenter path) | Reduce | T8/T10 make QuPath the executable viewer; T9 still writes D2 GeoJSON + helper JSON; M31 can demo QuPath if PathPresenter refuses | Shivam | No written import format from CCHMC IT by 1 Feb 2027 |
| R4 | Technical | U-Net refinement (T7) does not beat the Project Description baseline | Medium | Medium (demo still uses existing maps) | Accept + reduce | T9/T14 use the current localization if holdout Dice does not move | Shivam | Holdout mean slide Dice < 0.96 after T7 |
| R5 | External | Radiology collaborator does not return TMA-linked DICOM | High | High for fusion; **low for the pathology prototype** | Accept | T15/T16 are ice. M36 is a gate. T11 still delivers keys | Shivam | No DICOM on the approved share by 23 Mar 2027 |
| R6 | Team | Two-person team; exam week, winter break, or one illness hits T3/T7 | Medium | High | Reduce | Protected blocks in Table 1; 48-hour blocker rule from the Team Contract; T3 protocol written so Shivam can code rows without becoming owner | Nipun (calendar), both (coverage) | Missed standup, or a task still open 3 days after its Table 1 end |
| R7 | Technical / external | PHI (MRN, name) lands in Git or in a Docker context | Low | High (data-use breach; US-05) | Avoid | T12 before T1/T11 exports; Identifier gate blocks rather than guesses; no WSI, DICOM, or identified Excel in this repo | Nipun | MRN, name, DOB, or address in a commit, log, or `Dockerfile` |

R1, R2, R3, R5, and R6 are the schedule risks. They show up as: early T1/T2, leftover-row honesty at M17, QuPath parallel to PathPresenter, ice on T15/T16, and the empty winter/exam/break cells in Table 1.

---

## 7. Consistency pass

| Check | Result |
|---|---|
| Sixteen tasks, 10–25 range | Yes |
| Verb-first, one statement, one owner | Yes |
| Tasks per member | Eight each |
| Shivam IDs | T1, T4, T6, T7, T9, T11, T14, T16 |
| Nipun IDs | T2, T3, T5, T8, T10, T12, T13, T15 |
| Same ID/name/owner in Task List, WBS, Table 1, Table 2 | Yes |
| D0–D2 names | Outcomes cleaner, Cohort case index, existing pathology pipeline, Identifier gate, Configuration, Review package, PathPresenter, QuPath, Radiology intake, Modality integrator |
| Primary owner has the largest share on every row | Yes |
| Row and column totals | 228 h; **114 / 114 (50% / 50%)** |
| Ice visible in Table 1 | T15, T16 start after M36 |
| Remaining CS 5001 weeks match Week 1 roadmap | W8–W14 as in §0.2 |
| `Tasklist.md` at repo root | Yes |

---

## 8. Work starting 28 October 2026

**Shivam:** T1 Epic field list with Dr. Patel; start T11 TMA key search on approved systems only; keep the OQ-02 IT thread open for T9.

**Nipun:** T12 `identifier_rules` stub in `pipeline_config.yaml`; T2 eSlide Manager / PathPresenter inventory by `study_id`; create the approved-share folders named in D2 Appendix B, empty of PHI.
