# CS-Senior-Design-I-II

This repository is for the University of Cincinnati Senior Design I and II courses (CS 5001 Fall 2026 through CS 5002 Spring 2027).

**Project:** HepatoFusion — a research pipeline with Cincinnati Children’s Hospital that makes the existing pediatric liver-cancer tumor localization available as a pathologist helper and collects radiology, molecular, and cleaned clinical outcomes onto the same cohort for a later research risk score.

No PHI, medical record numbers, whole-slide images, or DICOM files belong in this repository.

## 1. Overview

The Silver/Gold whole-slide pipeline is already built (1,566 Silver and 1,546 Gold annotations, 248 WSIs, 102 patients). This repository holds the senior-design documents for the work still in front of the team. The Must for this academic year is data cleanup and finalization (see the requirements document).

## 2. Team members

| Name | Role | Email |
|---|---|---|
| Shivam Sinay Kharangate | Pathology CV / multimodal ML; clinical liaison | sinayksp@mail.uc.edu |
| Nipun Chandra | Data engineering / systems; pipeline reliability; documentation | chandrnu@mail.uc.edu |

**Advisor:** Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children’s Hospital  
**Partner:** Cincinnati Children’s Hospital

## 3. Documents

| File | What it is |
|---|---|
| [`Project-Description.md`](Project-Description.md) | Week 2 project description |
| [`Team_Contract.md`](Team_Contract.md) | Team contract |
| [`Constraints_Essay_sinayksp.md`](Constraints_Essay_sinayksp.md) | Week 3 constraints essay (source of CON-01–CON-05) |
| [`User_Stories.md`](User_Stories.md) | Week 4 user stories, use cases, and acceptance criteria |
| [`Design_Diagrams/`](Design_Diagrams/) | D0 high-level design, D1 data model and API contract, D2 edge cases and component specs, and the linked figures |
| [`Planning/A5_A6_Implementation_Plan.md`](Planning/A5_A6_Implementation_Plan.md) | Week 8 task list, milestones, timeline, effort matrix, WBS, risk register |
| [`Tasklist.md`](Tasklist.md) | Canonical sixteen-task list |
| [`Requirements_Document.md`](Requirements_Document.md) | Week 9 requirements (what the system must do and for whom). Version 1.0. |
| [`Technical_Specification.md`](Technical_Specification.md) | Week 9 technical specification (how it will be built). Version 1.0, traces to Requirements Document v1.0. |

Diagrams live under `Design_Diagrams/` and are linked from the two Week 9 documents rather than duplicated.

## 4. Repository policy

Do not commit PHI, credentials, WSIs, DICOM, or identified Excel. Training and inference stay on approved Cincinnati Children’s compute. See REQ-06, NFR-02, and CON-02 in the requirements document.
