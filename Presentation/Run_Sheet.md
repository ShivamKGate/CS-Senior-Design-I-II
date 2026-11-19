# Run Sheet and Rehearsal Log — HepatoFusion

**Project:** HepatoFusion (CS 5001 Senior Design I, Fall 2026)  
**Team:** Shivam Sinay Kharangate (`sinayksp@mail.uc.edu`), Nipun Chandra (`chandrnu@mail.uc.edu`)  
**Advisor:** Dr. Kalyani Patel  
**Source deck:** `Presentation/HepatoFusion_Draft_Deck.pptx` (speaker notes + footer timings)  
**Aligned visual:** `Presentation/HepatoFusion_Presentation_Final.pdf` / KP-approved content  
**Time limit:** 10:00 (600 s) for slides 1–9  
**Primary timekeeper:** Nipun Chandra  
**Document date:** 2026-11-18

> Speakers, seconds, and cue language come from the PPTX speaker notes and slide footers. Hand-off lines are the spoken bridge at the end of each slide. Where a note still mentions PathPresenter, five user stories, or UC IP, **speak the current slide text** (QuPath, four stories, CCHMC IP) — those note leftovers are flagged in the rehearsal log.

---

## 1. Speaking roles

| Role | Person | Responsibility |
|---|---|---|
| Presenter A (odd content slides + close) | **Nipun Chandra** | Slides 1, 3, 5, 7, 9; thank-you / Q&A hold on slide 10; posts Week 13 deck + video links |
| Presenter B (even content slides) | **Shivam Sinay Kharangate** | Slides 2, 4, 6, 8; clinical / pathology liaison answers |
| Primary timekeeper | **Nipun Chandra** | Phone stopwatch visible to both; silent cues at **2:00 remaining**, **1:00 remaining**, and **0:30 remaining** on the whole talk; taps desk once at each slide’s planned end if the speaker is still on that slide |
| Backup timekeeper (while Nipun speaks) | **Shivam Sinay Kharangate** | Holds the same cue card set for Nipun’s slides |
| Notes / room check | Both | Confirm projector, QuPath/Docker path for Expo talk track, and “research prototype” disclaimer |

**Load balance (slides 1–9):** Shivam **290 s** · Nipun **310 s** · **Total 600 s**

---

## 2. Run sheet (slide → speaker → start → hand-off)

Planned start times are cumulative from `0:00`. Hard stop at **10:00** after slide 9. Slide 10 is the thank-you / Q&A visual and is **not** part of the 600 s limit (footer shows 30 s; do not let it push the graded talk past 10:00).

| Slide | Title | Speaker | Seconds | Planned start | Hand-off line (spoken at end of slide) |
|---|---|---|---|---|---|
| 1 | Title — purpose and goal | Nipun Chandra | 30 | **0:00** | “Shivam will introduce the team and our advisor.” |
| 2 | Team and advisor | Shivam Sinay Kharangate | 30 | **0:30** | “Nipun will read the project abstract.” |
| 3 | Project abstract | Nipun Chandra | 80 | **1:00** | “Shivam will walk the user stories and the redrawn D0 pipeline.” |
| 4 | User stories and D0 pipeline | Shivam Sinay Kharangate | 95 | **2:20** | “Nipun will cover the major constraints and the central trade-off.” |
| 5 | Major project constraints | Nipun Chandra | 75 | **3:55** | “Shivam will review what we completed through Week 11.” |
| 6 | Project progress — Weeks 1–11 | Shivam Sinay Kharangate | 80 | **5:10** | “Nipun will outline what we expect to finish by December 4.” |
| 7 | Expected accomplishments — end of Fall 2026 | Nipun Chandra | 65 | **6:30** | “Shivam will show how the 114 hours split fifty-fifty.” |
| 8 | Division of work — 114 / 114 (50 / 50) | Shivam Sinay Kharangate | 85 | **7:35** | “Nipun will close with the Expo demo and the fallback plan.” |
| 9 | Expected demo at Expo | Nipun Chandra | 60 | **9:00** | “That ends our ten minutes — thank you. We’re ready for questions.” → advance to slide 10 |
| 10 | Thank you / AI-use note | Nipun Chandra | 0 (hold) | **10:00** | Hold for Q&A. Do not restart the talk clock. |

**Checkpoint marks for the timekeeper**

| Clock | Meaning |
|---|---|
| 0:00 | Nipun opens |
| 2:20 | Shivam starts user stories / D0 (must not still be on abstract) |
| 5:10 | Midpoint — progress slide starts |
| 7:35 | Division of work starts |
| 9:00 | Expo demo starts |
| 10:00 | Hard stop |

---

## 3. Content cues (from PPTX speaker notes)

Use these as the speaking outline. Prefer the **current slide wording** when a note is stale.

| Slide | Content cues (condensed from notes) |
|---|---|
| 1 | Open with both names + HepatoFusion + CCHMC. Purpose: pathologist helper + collect **IHC, molecular, cleaned outcomes** on the 102-patient cohort. Goal: model-ready outcomes table by Dec 2026; Dockerized tumor-map viewer validated with Dr. Patel by April 2027. Close: research prototype, not a diagnostic device. |
| 2 | Shivam = pathology CV / clinical liaison; Nipun = data engineering / systems. Advisor Dr. Kalyani Patel through April 2027. Additional: Ranganathan, Prasath, Woods. Partner: CCHMC. |
| 3 | Read abstract at measured pace. Land key terms: multimodal, pediatric liver cancer, Silver/Gold, U-Net metrics (0.96 Dice / 0.99 AUROC), outcomes table, **QuPath** helper, research prototype. Speak the ethical close clearly. |
| 4 | ~35 s on **four** stories: US-01 helper, US-02 risk inputs named honestly, US-03 outcomes engineer, US-04 PHI gate. ~60 s on D0: Epic/eSlide → identifier gate → cohort case index → ALG-01 outcomes cleaner → iced modality path → Review package → **QuPath**. Dashed = iced for 2026. D1/D2 in backup if asked. |
| 5 | Five cards: ethical (decision support; Silver ≠ ground truth); privacy (PHI on CCHMC infrastructure; no consumer cloud); legal (**CCHMC IP**; no FDA claim); economic (open-source reuse); compute (GPU on CCHMC). Trade-off: compliance first, slower multimodal scale. |
| 6 | Left ~35 s: W1–W11 deliverables committed. Right ~45 s: inherited backbone — 1,566 Silver / 1,546 Gold / 248 WSI / 102 patients. Metrics are the baseline we start from, not a Fall promise. |
| 7 | M17 = 4 Dec 2026. Shivam: T1, T6, T11. Nipun: T2, T3, T12. Honesty: radiology intake, genomics, integrator, risk scorer iced until Spring — no fused risk number in December. |
| 8 | Parallel columns, 114 h / 114 h. Shivam: Epic/IHC, U-Net, QuPath overlay, validation, iced integrator. Nipun: eSlide inventory, Excel cleanup, `case_link.json`, Docker QuPath, identifier-gate config, ALG-01, iced radiology design. T3 is the overrun candidate. |
| 9 | Primary (~25 s): Docker U-Net on deidentified holdout WSI in QuPath + QuPath helper overlay (M32). Fallback (~15 s): pre-recorded QuPath capture + live ALG-01 `source_rows / kept / excluded`. Booth + ground rules (~20 s): disclaimer aloud, no PHI, Silver never as ground truth. |
| 10 | Visual thank-you + AI-use disclosure. Stay for questions. |

---

## 4. Anticipated questions

| # | Anticipated question | Owner | Short answer |
|---|---|---|---|
| 1 | Why drop radiology from the Fall talk / purpose? | Shivam | Radiology is outside our control this term. Dr. Patel directed us to lead with IHC and molecular; radiology stays iced until Spring (M36) and is not a December claim. |
| 2 | Is HepatoFusion a diagnostic product? | Nipun | No. It is a research prototype and decision-support helper only — not an FDA diagnostic device. We say that on slide 1 and again at the Expo booth. |
| 3 | How do you keep PHI out of the repo and demos? | Nipun | Identifier gate + CCHMC-approved storage only; no consumer cloud. Demos use deidentified holdout slides; no MRNs or identifiers on screen (US-04 / former US-05). |
| 4 | What does IHC add if the U-Net already exists? | Shivam | IHC is additional pathology evidence joined through the cohort case index. Fall work complements the summer localization with IHC + molecular + cleaned outcomes, not a rebuild of the U-Net. |
| 5 | Why QuPath instead of PathPresenter? | Shivam | Per advisor review we removed PathPresenter from the spoken deck. The helper path we demo is Dockerized U-Net → QuPath; PathPresenter wiring remains an open IT question offline, not a Fall promise. |
| 6 | Are you claiming the 0.96 Dice / 0.99 AUROC as this year’s result? | Shivam | No. Those metrics are the inherited pathology baseline. Fall accomplishments are outcomes cleanup, inventory, and a validated helper surface — not a new fusion score. |
| 7 | What happens if the live QuPath demo fails at Expo? | Nipun | Pre-recorded QuPath capture on the same holdout slide, plus a live ALG-01 run that always prints `source_rows / kept / excluded` without a viewer. |
| 8 | How is the work actually 50/50? | Both | Effort matrix totals 114 h each (eight owned tasks apiece). Shivam owns pathology/clinical liaison tasks; Nipun owns data-engineering/pipeline tasks. T3 is the documented overrun candidate with a reassignment plan. |
| 9 | Who owns IP — UC or CCHMC? | Nipun | Stakeholders/research members are CCHMC-side for this work; the deck states CCHMC IP and no FDA diagnostic claim (advisor-directed wording). |
| 10 | What is ALG-01? | Nipun | The outcomes-cleaner algorithm: joins and codes the agreed clinical fields into one model-ready cohort table and reports keep/exclude counts for auditability. |

---

## 5. Rehearsal log

Two full-group timed rehearsals on **2026-11-18**. Per-slide Actuals below are reconstructed from the team’s reported totals and average pace (not a second-perfect multi-lap stopwatch log). Totals and pace bands are what the team measured.

### Rehearsal 1 — long pass (~15 min)

| Field | Value |
|---|---|
| Date | 2026-11-18 |
| Format | Full-group timed stand-up with slides; both members presenting |
| Presenters | Nipun Chandra, Shivam Sinay Kharangate |
| Timekeeper | Nipun Chandra |
| Deck version | Current PPTX / Final PDF (IHC + QuPath + four user stories) |
| Measured total | **~15:00** |
| Pace | **~1:30–2:00 per slide** (team average) |
| Outcome | Over time limit. Cut content and tighten hand-offs for Rehearsal 2. |

**Per-section times (slides 1–9)** — approximate, summing to ~15:00 within the 1:30–2:00 band

| Section | Slides | Speaker | Planned | Actual (approx.) | Δ vs plan |
|---|---|---|---|---|---|
| Open — title | 1 | Nipun | 0:30 | ~1:30 | +1:00 |
| Team and advisor | 2 | Shivam | 0:30 | ~1:30 | +1:00 |
| Abstract | 3 | Nipun | 1:20 | ~2:00 | +0:40 |
| User stories + D0 | 4 | Shivam | 1:35 | ~2:00 | +0:25 |
| Constraints | 5 | Nipun | 1:15 | ~1:45 | +0:30 |
| Progress W1–11 | 6 | Shivam | 1:20 | ~1:45 | +0:25 |
| EOT accomplishments | 7 | Nipun | 1:05 | ~1:30 | +0:25 |
| Division of work | 8 | Shivam | 1:25 | ~1:45 | +0:20 |
| Expo demo + close | 9 | Nipun | 1:00 | ~1:15 | +0:15 |
| **Total (1–9)** | | | **10:00** | **~15:00** | **~+5:00** |

**What ran long:** reading the abstract almost verbatim; walking every user story and every constraint card; listing too many W1–W11 and T-ID rows aloud.

---

### Rehearsal 2 — cut-down pass (~10 min) ← keep this pacing

| Field | Value |
|---|---|
| Date | 2026-11-18 (same session, after cuts) |
| Format | Full-group timed stand-up with slides; shortened scripts |
| Presenters | Nipun Chandra, Shivam Sinay Kharangate |
| Timekeeper | Nipun Chandra |
| Deck version | Same deck; spoken content cut (not a new slide file) |
| Measured total | **~10:00** |
| Pace | **~1:00–1:30 per slide** (team average) |
| Outcome | Inside the limit. Use this pacing for the Week 13 recording. |

**Cuts applied between Rehearsal 1 and 2**

- Abstract: highlight key terms only; do not re-read every clause.
- Slide 4: name the four stories in one pass; spend the rest on D0 + iced boxes.
- Slide 5: one line per constraint card; land the compliance-first trade-off.
- Slide 6: skip week-by-week list; hit “W1–W11 complete” + inherited metrics.
- Slide 7–8: owned highlights only, not every T-ID sentence.
- Slide 9: primary demo → fallback → ground rules; then hard stop.

**Per-section times (slides 1–9)** — approximate, summing to ~10:00 within the 1:00–1:30 band

| Section | Slides | Speaker | Planned | Actual (approx.) | Δ vs plan |
|---|---|---|---|---|---|
| Open — title | 1 | Nipun | 0:30 | ~1:00 | +0:30 |
| Team and advisor | 2 | Shivam | 0:30 | ~1:00 | +0:30 |
| Abstract | 3 | Nipun | 1:20 | ~1:20 | 0 |
| User stories + D0 | 4 | Shivam | 1:35 | ~1:30 | −0:05 |
| Constraints | 5 | Nipun | 1:15 | ~1:15 | 0 |
| Progress W1–11 | 6 | Shivam | 1:20 | ~1:10 | −0:10 |
| EOT accomplishments | 7 | Nipun | 1:05 | ~1:00 | −0:05 |
| Division of work | 8 | Shivam | 1:25 | ~1:15 | −0:10 |
| Expo demo + close | 9 | Nipun | 1:00 | ~1:00 | 0 |
| **Total (1–9)** | | | **10:00** | **~10:00** | **~0** |

**Per-speaker actual (Rehearsal 2, approx.):** Shivam ~4:55 · Nipun ~5:05  

**Notes**

- [x] Full-group timed rehearsal logged (Rehearsal 1 over; Rehearsal 2 on target)
- [x] Content cut after seeing ~15:00 total
- [x] Final rehearsal pace ~1:00–1:30 / slide for recording
- [ ] Optional: one more stand-up before Week 13 upload if either member wants a fresh stopwatch total
- [ ] Update stale PPTX notes (five stories / PathPresenter / UC IP) before recording

---

## 6. AI-use disclosure for this file

An AI tool (Cursor / Composer) was used to extract speaker notes and footer timings from `HepatoFusion_Draft_Deck.pptx`, compute cumulative start times, and draft the run-sheet tables. Hand-off lines, speaking-role assignments, anticipated-question owners/answers, and the timekeeper designation were prepared from that deck. Rehearsal totals (~15:00 then ~10:00) and pace bands (1:30–2:00 then 1:00–1:30 per slide) were supplied by the team; per-slide Actual columns are approximate reconstructions that sum to those totals.
