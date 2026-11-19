# Advisor Feedback — Assignment #8 Draft Deck

**Project:** HepatoFusion  
**Team members:** Shivam Sinay Kharangate (sinayksp@mail.uc.edu), Nipun Chandra (chandrnu@mail.uc.edu)  
**Advisor:** Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children's Hospital  
**Partner:** Cincinnati Children's Hospital  
**Deck under review:** `Presentation/HepatoFusion_Draft_Deck.pdf` (pre-meeting draft)  
**Revised / advisor-approved deck:** `Presentation/HepatoFusion_Draft_Deck_KP-approved.pdf`  
**Editable source:** `Presentation/HepatoFusion_Draft_Deck.pptx`  
**Document:** Advisor Feedback (Week 12)  
**Version:** 1.0 (post-meeting)  
**Date drafted:** 2026-11-18  
**Reviewed commit (pre-meeting draft):** `83b0935f3c56310b9d303a2e7d7969484da33b28` on `main`

> This file logs Dr. Patel's feedback on the Week 12 draft deck and the changes the team made in response. Changes were verified by comparing `HepatoFusion_Draft_Deck.pdf` (pre-meeting) to `HepatoFusion_Draft_Deck_KP-approved.pdf` (post-meeting). It is submitted alongside the draft PPTX and PDF for Assignment #8, and a revised copy becomes section 6 of the Week 14 design report.

---

## 1. Meeting record

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Duration | ~30 minutes |
| Attendees | Dr. Kalyani Patel (advisor); Shivam Sinay Kharangate; Nipun Chandra |
| Format | Live review with Dr. Patel (project advisor meeting) |
| Deck version reviewed | `HepatoFusion_Draft_Deck.pdf` / `.pptx` — commit `83b0935` on branch `main` |
| Deck version after edits | `HepatoFusion_Draft_Deck_KP-approved.pdf` (advisor-approved revisions applied) |
| Pre-reads sent | Draft PPTX + PDF, Week 1–11 repo link |
| Notes taker | Shivam Sinay Kharangate |
| Outcome | Dr. Patel approved the slides after the edits below were applied |

---

## 2. Feedback log

One row per comment. Status values: **Open**, **In progress**, **Done**, **Declined**.  
Responses and “Change made” columns were confirmed by diffing the pre-meeting PDF against the KP-approved PDF.

| # | Slide(s) | Dr. Patel said | Our response | Change made | Owner | Status |
|---|---|---|---|---|---|---|
| 1 | 1 (Purpose) | Add immunohistochemistry (IHC) before radiology in the purpose statement. | **Accepted** | Purpose rewritten from “collect radiology, molecular, and cleaned clinical outcomes…” to “Collect IHC, molecular, and cleaned clinical outcomes onto the same 102-patient cohort.” | Shivam | Done |
| 2 | 1, 3, 7 | Remove radiology for now (out of team control); keep IHC and molecular. | **Accepted** | Radiology dropped from the live purpose and near-term Fall scope. Slide 1 and abstract now foreground IHC + molecular; radiology retained only as later / iced scope language where still needed for the long-term risk-score story. | Nipun | Done |
| 3 | 3, 4, 7, 8, 9 | Remove PathPresenter from the talk. | **Accepted** | PathPresenter removed from the abstract (QuPath only), the D0 flowchart endpoint, Fall accomplishment wording (T2 = eSlide inventory), Expo primary demo (QuPath helper overlay), and T9 on the division-of-work slide (QuPath overlay + Review package). | Shivam | Done |
| 4 | 3 | Summer / Uprise work will be complemented by IHC and molecular. | **Accepted** | Abstract updated so senior-design work is framed as complementing previous summer work with IHC, plus the outcomes table, cohort inventory, and QuPath helper surface. | Nipun | Done |
| 5 | 4 | Remove US-03 (Radiology link). | **Accepted** | Radiology user story removed from Slide 4. Remaining stories shown as US-01 Pathologist helper, US-02 Case-level risk estimate, US-03 Outcomes engineer, US-04 PHI gate. | Shivam | Done |
| 6 | 4 (D0) | Remove PathPresenter (PP) from the flowchart. | **Accepted** | D0 live-room diagram endpoint changed from “PathPresenter + QuPath” to “QuPath” only. | Shivam | Done |
| 7 | 5 | Remove UC IP wording and similar framing. | **Accepted** | Legal / regulatory card changed from “CCHMC data-use agreement + UC IP” to “All stakeholders/research members from CCHMC, therefore CCHMC IP; no FDA diagnostic claim.” Privacy and compute cards also tightened to CCHMC infrastructure. | Nipun | Done |
| 8 | All | Approve the slides after the above edits. | **Accepted** | Revised deck saved as `HepatoFusion_Draft_Deck_KP-approved.pdf`; Dr. Patel approved this version for the draft presentation track. | Both | Done |

---

## 3. Summary of changes

The Week 12 review with Dr. Patel focused on scope honesty for a live faculty room: radiology is outside the team’s control this term, so IHC and molecular should lead the purpose and abstract, and PathPresenter should leave the spoken deck. The purpose slide and abstract now collect IHC, molecular, and cleaned outcomes, and frame Fall work as complementing summer / Uprise effort rather than promising radiology intake. Slide 4 drops the radiology user story and redraws D0 to end at QuPath only; Slide 5 replaces UC-IP language with CCHMC-IP framing; Expo and division-of-work wording follow the same QuPath-only helper path. No feedback item was declined. Dr. Patel approved the revised deck after these edits.

---

## 4. Open items

Items not yet closed, each with the date we expect to close them. If an item slips, update the row rather than deleting it.

| # | Open item | Owner | Target close date | Blocker / note |
|---|---|---|---|---|
| 1 | Slide 4 still labels the block “Five user stories” while only four stories remain after removing radiology US-03 — retitle to “Four user stories” (or restore a fifth non-radiology story if the team intentionally keeps five). | Shivam | 2026-11-24 | Cosmetic consistency before Week 13 final deck |
| 2 | Slide 8 (Nipun column) still lists “T2 eSlide / PathPresenter inventory” even though PathPresenter was removed elsewhere — align to “eSlide inventory” to match Slide 7 and advisor direction. | Nipun | 2026-11-24 | Leftover from pre-meeting effort matrix copy |
| 3 | Re-sync editable `HepatoFusion_Draft_Deck.pptx` with the KP-approved PDF content, restore backup slides (D1/D2, timing table, recording plan), and keep the PPTX beside the PDF in `Presentation/`. | Both | 2026-11-24 | KP-approved PDF currently has 10 pages (9 content + thank-you); draft PDF had full backup set |
| 4 | Week 13 final: commit both PDFs + this file, put repo link + commit hash in the Canvas comment, and post deck/video links to the team spreadsheet. | Nipun | Week 13 upload window | Recording plan already drafted on the pre-meeting backup slide |
| 5 | Test recording (PowerPoint Record Slide Show, ~10:00, both presenters) to check audio before the graded Week 13 upload. | Both | 2026-11-25 | Course suggestion; not blocked by advisor feedback |

---

## 5. Non-advisor notes (optional)

- Diff source of truth for this file: `HepatoFusion_Draft_Deck.pdf` (17 pages, pre-meeting) vs `HepatoFusion_Draft_Deck_KP-approved.pdf` (10 pages, post-meeting / approved).
- Pre-meeting deck already had speaker + seconds on each content slide and a backup timing table totaling 600 s (Shivam 290 / Nipun 310). Reconfirm totals after any Week 13 wording cuts.
- Recording plan (from pre-meeting backup): presenters Shivam + Nipun; software PowerPoint Record Slide Show; target 10:00; Nipun posts deck + video links to the team spreadsheet; Expo primary = Dockerized U-Net in QuPath on a deidentified holdout WSI; fallback = pre-recorded QuPath capture + live ALG-01 outcomes cleaner counts.
- “IGC” in raw meeting notes is treated as **IHC** (immunohistochemistry).

---

## 6. AI-use disclosure for this file

An AI tool (Cursor / Composer) was used to compare the pre-meeting and KP-approved PDFs, map Dr. Patel’s comments onto concrete slide diffs, and draft the prose of this feedback file. All feedback entries, response decisions (accepted / modified / declined), owners, and open-item dates were confirmed against the team’s advisor notes from the 2026-11-18 meeting. This statement mirrors the AI-use strip on the deck and the longer disclosure in `Ethics_Statement.md`.
