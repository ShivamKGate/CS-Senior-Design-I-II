# User Stories and Use Cases

**Project:** HepatoFusion  
**Team members:** Shivam Sinay Kharangate, Nipun Chandra  
**Partner:** Cincinnati Children’s Hospital  
**Status:** Week 4 draft (revise in Week 9)

The Silver/Gold whole-slide pipeline is already built (1,566+ Silver and 1,546+ Gold annotations, 248+ slides, 102+ patients; pathology U-Net at 0.96 mean slide Dice and 0.99 tumor-localization AUROC). These stories do not rebuild that pipeline. Pathologists use that localization as a helper during review. The work still in front of the team is radiology (CT/MRI) after a meeting with a radiology team member, genomic and molecular data, and cleaning the existing clinical-outcomes spreadsheet so a risk model can train on it.

## Stakeholder map

| Category | Who | Why they matter |
|----------|-----|-----------------|
| Primary | Pediatric liver pathologist at Cincinnati Children’s | Uses the existing tumor map as a helper while reading a case, and will use a later risk estimate the same way: support, not a diagnosis |
| Secondary | Radiology team member at Cincinnati Children’s | Source of CT/MRI for patients already in the pathology cohort; collection is starting, so many cases will not have imaging yet |
| Secondary | HepatoFusion research engineer (student team) | Turns the outcomes spreadsheet into a table a risk model can train on, and keeps new files on approved compute |
| Hidden | Hospital data-use / privacy reviewer | Not a daily user; radiology and molecular files add protected health information that must not land in the course repository |

## User stories

**US-01 (primary):** As a pediatric liver pathologist at Cincinnati Children’s,  
I want the existing tumor localization available as a helper while I review a whole-slide image,  
so that I can compare the map with my own read and still own the diagnosis.

**US-02 (primary):** As a pediatric liver pathologist at Cincinnati Children’s,  
I want a case-level risk estimate that names only the inputs actually used (existing pathology result, CT/MRI if linked, genomic or molecular data if linked, and the cleaned clinical outcomes),  
so that I can compare the score with the clinical picture without treating a missing modality as if it were present.

**US-03 (secondary):** As a radiology team member at Cincinnati Children’s,  
I want a CT or MRI study for a patient already in the pathology cohort linked to that same case,  
so that later risk estimates can use imaging only when a study has actually been collected.

**US-04 (secondary):** As a HepatoFusion research engineer,  
I want each row of the clinical-outcomes spreadsheet reduced to an agreed field set that joins to exactly one case in the existing pathology cohort,  
so that a risk model can train on the table without hand-fixing free text or unmatched patients at training time.

**US-05 (hidden):** As a Cincinnati Children’s data-use reviewer,  
I want newly collected radiology and genomic or molecular files blocked from the course repository when a direct patient identifier is present,  
so that adding those modalities does not break the hospital data-use agreement.

## INVEST self-check

| ID | I | N | V | E | S | T | Notes |
|----|---|---|---|---|---|---|--------|
| US-01 | Yes | Yes | Yes | Yes | Yes | Yes | Uses the finished localization as decision support; does not reopen Silver/Gold labeling |
| US-02 | Yes | Yes | Yes | Yes | Yes | Yes | One score plus the input list; which modalities are required can still be negotiated |
| US-03 | Yes | Yes | Yes | Yes | Yes | Yes | Link-or-not for one study; separate from model training |
| US-04 | Yes | Yes | Yes | Yes | Yes | Yes | Join and field check only; does not choose a model |
| US-05 | Yes | Yes | Yes | Yes | Yes | Yes | Pass/fail on identifiers in new modality files |

No story names a control, layout, or screen element.

## Use cases

### UC-01 — Produce a case risk estimate from the inputs on hand

**Expands:** US-02  
**Primary actor:** Pediatric liver pathologist  
**Secondary actors:** HepatoFusion risk model on approved institutional or hospital compute; radiology and molecular stores (may be empty for a case)

**Preconditions (a tester can verify):**
1. The case is one of the existing pathology-cohort patients and already has a tumor-localization result from the finished pipeline.
2. The clinical-outcomes row for that case is in the model-ready table from UC-02.
3. CT/MRI and genomic or molecular data are optional and are either linked to that same case or recorded as not linked.
4. Slide, imaging, molecular, and outcome data stay on approved compute. No consumer cloud API is a destination for them.

**Main success flow:**
1. Pathologist requests a risk estimate for one case.
2. System lists the inputs that are actually linked: existing pathology result, radiology (CT or MRI), genomic or molecular data, and cleaned clinical outcomes.
3. Pathologist confirms that list.
4. System computes one risk score from only those linked inputs.
5. Pathologist reads the result.
6. System returns the score, the input list, and the statement “research prototype, not a diagnostic device.”

**Alternate flow — A1: No radiology study is linked yet**
1. At step 2, the case has no CT or MRI linked (collection with the radiology team has not reached this patient).
2. System leaves radiology off the input list and labels it “not linked.”
3. If the pathologist still confirms the reduced list, the system scores only the linked inputs and does not describe the score as using imaging.
4. Flow continues at step 5.

**Exception flow — E1: The clinical-outcomes row is not model-ready**
1. At step 2, the case has no row in the model-ready outcomes table.
2. System does not compute a score.
3. System reports the case as blocked and the reason “clinical outcomes not model-ready,” with no risk number.

**Postcondition:** A score exists only when a model-ready outcomes row exists, and the result names every input that was used and no input that was not linked. The existing pathology model is not retrained in this flow.

### UC-02 — Make the clinical-outcomes table model-ready

**Expands:** US-04  
**Primary actor:** HepatoFusion research engineer  
**Secondary actors:** Hospital data store that holds the outcomes spreadsheet; existing pathology cohort list

**Preconditions (a tester can verify):**
1. The source spreadsheet is opened only on approved institutional or hospital compute.
2. The pathology cohort list used for joining is the existing 102+ patient list, not a new unlabeled cohort.
3. The team has a written field list for the risk model. A field counts as ready only if it is non-empty and coded or numeric, not unresolved free text.
4. The join key on a spreadsheet row matches a cohort case by that case’s internal study identifier, not by patient name.

**Main success flow:**
1. Engineer submits the outcomes spreadsheet for a readiness check.
2. System compares each row’s join key to the pathology cohort and checks the agreed fields.
3. Engineer confirms the field list.
4. System writes a model-ready table that keeps only rows whose join key matches exactly one cohort case and whose agreed fields are all ready.
5. Engineer requests the summary.
6. System reports three counts: rows in the source spreadsheet, rows kept, and rows excluded.

**Alternate flow — A1: A matched row still has one free-text field**
1. At step 2, the join key matches exactly one cohort case, but one agreed field is unresolved free text.
2. System excludes that row from the model-ready table and adds it to an exclusion log with the reason “field not coded.”
3. The log records the internal study identifier and the field name, not the patient name.
4. Flow continues with the remaining rows.

**Exception flow — E1: A join key matches zero cases or more than one**
1. At step 2, a row’s join key matches no cohort case, or it matches more than one.
2. System does not place that row in the model-ready table and does not guess a match.
3. System adds the row to the exclusion log with the reason “unmatched” or “ambiguous join” and still reports the three counts in step 6 for the other rows.

**Postcondition:** Every row in the model-ready table joins to exactly one existing pathology-cohort case and has only ready fields. Excluded rows are counted. Patient names are not written to the course repository.

## Acceptance criteria

**AC-01.1 (UC-01 main success)**  
Given a cohort case with an existing pathology localization, a model-ready outcomes row, a linked CT or MRI, and linked genomic or molecular data,  
When the pathologist requests a risk estimate and confirms that full input list,  
Then the result contains exactly one risk score, the input list contains pathology, radiology, genomic or molecular data, and clinical outcomes, and the prototype disclaimer is present.

**AC-01.2 (UC-01 exception E1)**  
Given a cohort case whose outcomes row was excluded by UC-02,  
When the pathologist requests a risk estimate,  
Then no risk number is returned and the reason is “clinical outcomes not model-ready.”

**AC-01.3 (UC-01 alternate A1)**  
Given a cohort case with a model-ready outcomes row and no linked CT or MRI,  
When the pathologist confirms a risk estimate on the reduced list,  
Then radiology is reported as “not linked,” and the score’s input list does not include radiology.

**AC-02.1 (UC-02 main success)**  
Given a source spreadsheet in which every row’s join key matches exactly one of the existing pathology-cohort cases and every agreed field is non-empty and coded or numeric,  
When the engineer runs the readiness check and confirms the field list,  
Then rows kept equals rows in the source spreadsheet, rows excluded equals 0, and each kept row joins to exactly one cohort case.

**AC-02.2 (UC-02 exception E1)**  
Given a source row whose join key matches zero cohort cases,  
When the engineer runs the readiness check,  
Then that row is absent from the model-ready table, the exclusion log reason is “unmatched,” and no second cohort case is substituted.
