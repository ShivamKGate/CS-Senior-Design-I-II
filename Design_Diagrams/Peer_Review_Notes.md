# Peer Design Review Notes

**Project:** HepatoFusion
**Team members:** Shivam Sinay Kharangate, Nipun Chandra
**Document:** Week 7 peer design review, consolidated for submission with D2 (Week 8).
**Status at the time of initial commit:** scaffold. Fill in after the review session. If an item is marked **must-fix**, apply it to `D2_Detailed_Design.md` before the Week 8 submission and tick the “applied” column; cite the item in that document’s rationale section (R-10).

---

## 1. Feedback received (from every reviewing team)

Convert every piece of feedback into an action item. One row per item.

| ID | Rubric criterion | Issue (one sentence) | Raised by (team name) | Action (verb + concrete artifact) | Owner | Priority | Due | Applied to D2 (Y/N) |
|---|---|---|---|---|---|---|---|---|
| PR-01 | _completeness / feasibility / clarity / risk_ | | | | Nipun / Shivam | must-fix / worth-considering / out-of-scope | 2026-10-?? | |
| PR-02 | | | | | | | | |
| PR-03 | | | | | | | | |
| PR-04 | | | | | | | | |
| PR-05 | | | | | | | | |

**Rubric criteria reminder** (same wording as the Week 8 brief):
- **Completeness** — every D0 component has data model + behavior + interface + edge cases; glue treated the same; at least one diagram shows error paths; conventions on every diagram.
- **Feasibility** — the design can actually be built with the team’s resources and compute.
- **Clarity** — a reviewer with no context can follow the design.
- **Risk** — the design surfaces the right failure modes (PHI leak, missing modality, viewer refusal, model-swap).

**Priority definitions** (same as the Week 8 brief):
- **must-fix** — apply to D2 before this submission; cite in rationale R-10 if it causes an edit to D0 or D1 text.
- **worth considering** — park on the backlog; revisit when the component becomes a Week-9 task.
- **out of scope for now** — explicitly declined with a one-line reason.

---

## 2. Feedback the team gave (while reviewing others)

The Week 8 brief asks for the top two issues the team raised while reviewing other teams, plus the criterion each falls under.

| Issue # | Reviewed team | Rubric criterion | Issue (one sentence) | What we suggested they do |
|---|---|---|---|---|
| 1 | | | | |
| 2 | | | | |

---

## 3. Summary

- **Criterion that drew the most feedback on our design:** _[completeness / feasibility / clarity / risk]_
- **Top two issues we raised while reviewing other teams:** _(copy from §2, two bullets)_
- **Must-fix items applied to D2 before this submission:** _(list PR-IDs; if none, say “none”)_
- **Decisions in `D2_Detailed_Design.md §5` that were changed by the review:** _(list R-IDs; if none, say “none — R-10 states this explicitly”)_

---

## 4. Links

- `D2_Detailed_Design.md` — rationale §5 marks any decision the review changed.
- `D0_High_Level_Design.md` and `D1_Detailed_Design.md` — only edited if the review surfaces an errata; such an edit must be referenced here.
