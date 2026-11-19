"""Render Advisor_Feedback.md content to a formatted PDF for Canvas submission."""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)

OUT = Path(__file__).with_name("Advisor_Feedback.pdf")


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="DocTitle",
            parent=styles["Heading1"],
            fontSize=16,
            leading=20,
            spaceAfter=8,
            textColor=colors.HexColor("#1a365d"),
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="Section",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            spaceBefore=14,
            spaceAfter=6,
            textColor=colors.HexColor("#1a365d"),
            fontName="Helvetica-Bold",
        )
    )
    styles.add(
        ParagraphStyle(
            name="Body",
            parent=styles["Normal"],
            fontSize=9.5,
            leading=12.5,
            spaceAfter=6,
            alignment=TA_JUSTIFY,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Meta",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            spaceAfter=2,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Quote",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            leftIndent=10,
            rightIndent=6,
            textColor=colors.HexColor("#334155"),
            spaceBefore=4,
            spaceAfter=8,
            alignment=TA_JUSTIFY,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Cell",
            parent=styles["Normal"],
            fontSize=7.5,
            leading=9.5,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CellHead",
            parent=styles["Normal"],
            fontSize=7.5,
            leading=9.5,
            fontName="Helvetica-Bold",
            textColor=colors.white,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BulletBody",
            parent=styles["Normal"],
            fontSize=9,
            leading=12,
            leftIndent=12,
            spaceAfter=3,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Footer",
            parent=styles["Normal"],
            fontSize=8,
            leading=10,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#64748b"),
        )
    )
    return styles


def make_table(styles, headers, rows, col_widths):
    head = [Paragraph(h, styles["CellHead"]) for h in headers]
    body = [[Paragraph(str(c), styles["Cell"]) for c in row] for row in rows]
    table = Table([head] + body, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a365d")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("BACKGROUND", (0, 1), (-1, -1), colors.white),
                (
                    "ROWBACKGROUNDS",
                    (0, 1),
                    (-1, -1),
                    [colors.white, colors.HexColor("#f1f5f9")],
                ),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(0.75 * inch, 0.45 * inch, "HepatoFusion — Advisor Feedback (Week 12)")
    canvas.drawRightString(letter[0] - 0.75 * inch, 0.45 * inch, f"Page {doc.page}")
    canvas.restoreState()


def main():
    styles = build_styles()
    p = lambda text, style="Body": Paragraph(text, styles[style])
    meta = lambda label, value: p(f"<b>{label}:</b> {value}", "Meta")

    story = []
    story.append(p("Advisor Feedback — Assignment #8 Draft Deck", "DocTitle"))
    story.append(
        HRFlowable(
            width="100%",
            thickness=1,
            color=colors.HexColor("#1a365d"),
            spaceAfter=8,
        )
    )

    for label, value in [
        ("Project", "HepatoFusion"),
        (
            "Team members",
            "Shivam Sinay Kharangate (sinayksp@mail.uc.edu), Nipun Chandra (chandrnu@mail.uc.edu)",
        ),
        (
            "Advisor",
            "Dr. Kalyani Patel (Kalyani.Patel@cchmc.org), Department of Pathology and Laboratory Medicine, Cincinnati Children's Hospital",
        ),
        ("Partner", "Cincinnati Children's Hospital"),
        (
            "Deck under review",
            "Presentation/HepatoFusion_Draft_Deck.pdf (pre-meeting draft)",
        ),
        (
            "Revised / advisor-approved deck",
            "Presentation/HepatoFusion_Draft_Deck_KP-approved.pdf",
        ),
        ("Editable source", "Presentation/HepatoFusion_Draft_Deck.pptx"),
        ("Document", "Advisor Feedback (Week 12)"),
        ("Version", "1.0 (post-meeting)"),
        ("Date drafted", "2026-11-18"),
        (
            "Reviewed commit (pre-meeting draft)",
            "83b0935f3c56310b9d303a2e7d7969484da33b28 on main",
        ),
    ]:
        story.append(meta(label, value))

    story.append(Spacer(1, 6))
    story.append(
        p(
            "This file logs Dr. Patel's feedback on the Week 12 draft deck and the changes the team made in response. "
            "Changes were verified by comparing <i>HepatoFusion_Draft_Deck.pdf</i> (pre-meeting) to "
            "<i>HepatoFusion_Draft_Deck_KP-approved.pdf</i> (post-meeting). It is submitted alongside the draft PPTX and PDF "
            "for Assignment #8, and a revised copy becomes section 6 of the Week 14 design report.",
            "Quote",
        )
    )

    story.append(p("1. Meeting record", "Section"))
    story.append(
        make_table(
            styles,
            ["Field", "Value"],
            [
                ["Date", "2026-11-18"],
                ["Duration", "~30 minutes"],
                [
                    "Attendees",
                    "Dr. Kalyani Patel (advisor); Shivam Sinay Kharangate; Nipun Chandra",
                ],
                ["Format", "Live review with Dr. Patel (project advisor meeting)"],
                [
                    "Deck version reviewed",
                    "HepatoFusion_Draft_Deck.pdf / .pptx — commit 83b0935 on branch main",
                ],
                [
                    "Deck version after edits",
                    "HepatoFusion_Draft_Deck_KP-approved.pdf (advisor-approved revisions applied)",
                ],
                ["Pre-reads sent", "Draft PPTX + PDF, Week 1–11 repo link"],
                ["Notes taker", "Shivam Sinay Kharangate"],
                [
                    "Outcome",
                    "Dr. Patel approved the slides after the edits below were applied",
                ],
            ],
            [1.7 * inch, 5.3 * inch],
        )
    )

    story.append(p("2. Feedback log", "Section"))
    story.append(
        p(
            "One row per comment. Status values: <b>Open</b>, <b>In progress</b>, <b>Done</b>, <b>Declined</b>. "
            "Responses and “Change made” columns were confirmed by diffing the pre-meeting PDF against the KP-approved PDF.",
            "Body",
        )
    )
    story.append(
        make_table(
            styles,
            ["#", "Slide(s)", "Dr. Patel said", "Our response", "Change made", "Owner", "Status"],
            [
                [
                    "1",
                    "1 (Purpose)",
                    "Add immunohistochemistry (IHC) before radiology in the purpose statement.",
                    "<b>Accepted</b>",
                    "Purpose rewritten from “collect radiology, molecular, and cleaned clinical outcomes…” to “Collect IHC, molecular, and cleaned clinical outcomes onto the same 102-patient cohort.”",
                    "Shivam",
                    "Done",
                ],
                [
                    "2",
                    "1, 3, 7",
                    "Remove radiology for now (out of team control); keep IHC and molecular.",
                    "<b>Accepted</b>",
                    "Radiology dropped from the live purpose and near-term Fall scope. Slide 1 and abstract now foreground IHC + molecular; radiology retained only as later / iced scope language where still needed for the long-term risk-score story.",
                    "Nipun",
                    "Done",
                ],
                [
                    "3",
                    "3, 4, 7, 8, 9",
                    "Remove PathPresenter from the talk.",
                    "<b>Accepted</b>",
                    "PathPresenter removed from the abstract (QuPath only), the D0 flowchart endpoint, Fall accomplishment wording (T2 = eSlide inventory), Expo primary demo (QuPath helper overlay), and T9 on the division-of-work slide (QuPath overlay + Review package).",
                    "Shivam",
                    "Done",
                ],
                [
                    "4",
                    "3",
                    "Summer / Uprise work will be complemented by IHC and molecular.",
                    "<b>Accepted</b>",
                    "Abstract updated so senior-design work is framed as complementing previous summer work with IHC, plus the outcomes table, cohort inventory, and QuPath helper surface.",
                    "Nipun",
                    "Done",
                ],
                [
                    "5",
                    "4",
                    "Remove US-03 (Radiology link).",
                    "<b>Accepted</b>",
                    "Radiology user story removed from Slide 4. Remaining stories shown as US-01 Pathologist helper, US-02 Case-level risk estimate, US-03 Outcomes engineer, US-04 PHI gate.",
                    "Shivam",
                    "Done",
                ],
                [
                    "6",
                    "4 (D0)",
                    "Remove PathPresenter (PP) from the flowchart.",
                    "<b>Accepted</b>",
                    "D0 live-room diagram endpoint changed from “PathPresenter + QuPath” to “QuPath” only.",
                    "Shivam",
                    "Done",
                ],
                [
                    "7",
                    "5",
                    "Remove UC IP wording and similar framing.",
                    "<b>Accepted</b>",
                    "Legal / regulatory card changed from “CCHMC data-use agreement + UC IP” to “All stakeholders/research members from CCHMC, therefore CCHMC IP; no FDA diagnostic claim.” Privacy and compute cards also tightened to CCHMC infrastructure.",
                    "Nipun",
                    "Done",
                ],
                [
                    "8",
                    "All",
                    "Approve the slides after the above edits.",
                    "<b>Accepted</b>",
                    "Revised deck saved as HepatoFusion_Draft_Deck_KP-approved.pdf; Dr. Patel approved this version for the draft presentation track.",
                    "Both",
                    "Done",
                ],
            ],
            [
                0.28 * inch,
                0.72 * inch,
                1.35 * inch,
                0.75 * inch,
                2.55 * inch,
                0.55 * inch,
                0.5 * inch,
            ],
        )
    )

    story.append(p("3. Summary of changes", "Section"))
    story.append(
        p(
            "The Week 12 review with Dr. Patel focused on scope honesty for a live faculty room: radiology is outside the "
            "team’s control this term, so IHC and molecular should lead the purpose and abstract, and PathPresenter should "
            "leave the spoken deck. The purpose slide and abstract now collect IHC, molecular, and cleaned outcomes, and "
            "frame Fall work as complementing summer / Uprise effort rather than promising radiology intake. Slide 4 drops "
            "the radiology user story and redraws D0 to end at QuPath only; Slide 5 replaces UC-IP language with CCHMC-IP "
            "framing; Expo and division-of-work wording follow the same QuPath-only helper path. No feedback item was "
            "declined. Dr. Patel approved the revised deck after these edits.",
            "Body",
        )
    )

    story.append(p("4. Open items", "Section"))
    story.append(
        p(
            "Items not yet closed, each with the date we expect to close them. If an item slips, update the row rather than deleting it.",
            "Body",
        )
    )
    story.append(
        make_table(
            styles,
            ["#", "Open item", "Owner", "Target close date", "Blocker / note"],
            [
                [
                    "1",
                    "Slide 4 still labels the block “Five user stories” while only four stories remain after removing radiology US-03 — retitle to “Four user stories” (or restore a fifth non-radiology story if the team intentionally keeps five).",
                    "Shivam",
                    "2026-11-24",
                    "Cosmetic consistency before Week 13 final deck",
                ],
                [
                    "2",
                    "Slide 8 (Nipun column) still lists “T2 eSlide / PathPresenter inventory” even though PathPresenter was removed elsewhere — align to “eSlide inventory” to match Slide 7 and advisor direction.",
                    "Nipun",
                    "2026-11-24",
                    "Leftover from pre-meeting effort matrix copy",
                ],
                [
                    "3",
                    "Re-sync editable HepatoFusion_Draft_Deck.pptx with the KP-approved PDF content, restore backup slides (D1/D2, timing table, recording plan), and keep the PPTX beside the PDF in Presentation/.",
                    "Both",
                    "2026-11-24",
                    "KP-approved PDF currently has 10 pages (9 content + thank-you); draft PDF had full backup set",
                ],
                [
                    "4",
                    "Week 13 final: commit both PDFs + this file, put repo link + commit hash in the Canvas comment, and post deck/video links to the team spreadsheet.",
                    "Nipun",
                    "Week 13 upload window",
                    "Recording plan already drafted on the pre-meeting backup slide",
                ],
                [
                    "5",
                    "Test recording (PowerPoint Record Slide Show, ~10:00, both presenters) to check audio before the graded Week 13 upload.",
                    "Both",
                    "2026-11-25",
                    "Course suggestion; not blocked by advisor feedback",
                ],
            ],
            [0.28 * inch, 3.2 * inch, 0.65 * inch, 1.15 * inch, 1.72 * inch],
        )
    )

    story.append(p("5. Non-advisor notes (optional)", "Section"))
    for note in [
        "Diff source of truth for this file: HepatoFusion_Draft_Deck.pdf (17 pages, pre-meeting) vs HepatoFusion_Draft_Deck_KP-approved.pdf (10 pages, post-meeting / approved).",
        "Pre-meeting deck already had speaker + seconds on each content slide and a backup timing table totaling 600 s (Shivam 290 / Nipun 310). Reconfirm totals after any Week 13 wording cuts.",
        "Recording plan (from pre-meeting backup): presenters Shivam + Nipun; software PowerPoint Record Slide Show; target 10:00; Nipun posts deck + video links to the team spreadsheet; Expo primary = Dockerized U-Net in QuPath on a deidentified holdout WSI; fallback = pre-recorded QuPath capture + live ALG-01 outcomes cleaner counts.",
        "“IGC” in raw meeting notes is treated as <b>IHC</b> (immunohistochemistry).",
    ]:
        story.append(p(f"• {note}", "BulletBody"))

    story.append(p("6. AI-use disclosure for this file", "Section"))
    story.append(
        p(
            "An AI tool (Cursor / Composer) was used to compare the pre-meeting and KP-approved PDFs, map Dr. Patel’s "
            "comments onto concrete slide diffs, and draft the prose of this feedback file. All feedback entries, response "
            "decisions (accepted / modified / declined), owners, and open-item dates were confirmed against the team’s "
            "advisor notes from the 2026-11-18 meeting. This statement mirrors the AI-use strip on the deck and the longer "
            "disclosure in Ethics_Statement.md.",
            "Body",
        )
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.7 * inch,
        rightMargin=0.7 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.7 * inch,
        title="Advisor Feedback — HepatoFusion Assignment #8",
        author="Shivam Sinay Kharangate; Nipun Chandra",
    )
    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)
    print(f"Wrote {OUT}")
    print(f"Size: {OUT.stat().st_size} bytes")


if __name__ == "__main__":
    main()
