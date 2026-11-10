"""Generate HepatoFusion draft deck for Assignment #8 (Fall Design Presentations)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree

# ---------- Palette (user-supplied) ----------
SEBUM       = RGBColor(0x59, 0x60, 0x70)
CARTILAGE   = RGBColor(0x75, 0x7F, 0x99)
SUBSTANTIA  = RGBColor(0x94, 0xA9, 0xBE)
LYMPHATIC   = RGBColor(0xB2, 0xCD, 0xDF)
NEUTROPHILS = RGBColor(0xC9, 0xD9, 0xE6)
ANTIBIOTICS = RGBColor(0xEA, 0xF1, 0xF1)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
NEAR_BLACK  = RGBColor(0x1F, 0x29, 0x37)

FONT = "Calibri"

# ---------- Presentation setup ----------
prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height

BLANK = prs.slide_layouts[6]  # fully blank


def add_background(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, SH)
    bg.line.fill.background()
    bg.fill.solid(); bg.fill.fore_color.rgb = color
    bg.shadow.inherit = False
    return bg


def add_header(slide, slide_num, total=9):
    # Top accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.35))
    bar.line.fill.background()
    bar.fill.solid(); bar.fill.fore_color.rgb = SEBUM
    # Project name right
    name = slide.shapes.add_textbox(Inches(10.3), Inches(0.03), Inches(3.0), Inches(0.3))
    tf = name.text_frame; tf.margin_left=tf.margin_right=0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
    r = p.add_run(); r.text = "HepatoFusion   |   CS 5001"
    r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = ANTIBIOTICS; r.font.bold = True
    # Slide counter left
    counter = slide.shapes.add_textbox(Inches(0.15), Inches(0.03), Inches(3.0), Inches(0.3))
    tf = counter.text_frame; tf.margin_left=tf.margin_right=0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = f"  {slide_num} / {total}"
    r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = ANTIBIOTICS; r.font.bold = True


def add_footer(slide, speaker, seconds):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.2), SW, Inches(0.3))
    bar.line.fill.background()
    bar.fill.solid(); bar.fill.fore_color.rgb = NEUTROPHILS
    tb = slide.shapes.add_textbox(Inches(0.15), Inches(7.22), Inches(13.0), Inches(0.26))
    tf = tb.text_frame; tf.margin_left=tf.margin_right=0
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = f"Speaker: {speaker}"
    r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = SEBUM; r.font.bold = True
    # right side time
    tb2 = slide.shapes.add_textbox(Inches(0.15), Inches(7.22), Inches(13.05), Inches(0.26))
    tf2 = tb2.text_frame; tf2.margin_left=tf2.margin_right=0
    p2 = tf2.paragraphs[0]; p2.alignment = PP_ALIGN.RIGHT
    r2 = p2.add_run(); r2.text = f"{seconds} s"
    r2.font.name = FONT; r2.font.size = Pt(11); r2.font.color.rgb = SEBUM; r2.font.bold = True


def add_title(slide, text, top=Inches(0.55), left=Inches(0.6), width=Inches(12.1), height=Inches(0.8), size=36, color=SEBUM):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.margin_left=tf.margin_right=0; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
    r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = color
    return tb


def add_accent_rule(slide, top=Inches(1.35), left=Inches(0.6), width=Inches(1.5)):
    rule = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Emu(38100))
    rule.line.fill.background()
    rule.fill.solid(); rule.fill.fore_color.rgb = CARTILAGE


def add_textbox(slide, left, top, width, height, bullets, size=16, color=NEAR_BLACK, bullet_char="•  ", line_spacing=1.15):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = Inches(0.05); tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.02); tf.margin_bottom = Inches(0.02)
    for i, item in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        if isinstance(item, tuple):
            # (text, is_bold, is_bullet, custom_size, custom_color)
            text = item[0]
            bold = item[1] if len(item) > 1 else False
            bullet = item[2] if len(item) > 2 else True
            isize = item[3] if len(item) > 3 else size
            icol  = item[4] if len(item) > 4 else color
            r = p.add_run()
            r.text = (bullet_char if bullet else "") + text
            r.font.name = FONT; r.font.size = Pt(isize); r.font.bold = bold; r.font.color.rgb = icol
        else:
            r = p.add_run()
            r.text = bullet_char + item
            r.font.name = FONT; r.font.size = Pt(size); r.font.color.rgb = color
        p.space_after = Pt(4)
    return tb


def add_plain_text(slide, left, top, width, height, lines, size=16, color=NEAR_BLACK, align=PP_ALIGN.LEFT, line_spacing=1.2, bold_terms=None):
    tb = slide.shapes.add_textbox(left, top, width, height)
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = Inches(0.05); tf.margin_right = Inches(0.05)
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = line_spacing
        if bold_terms and isinstance(line, str):
            # split on bold terms
            remaining = line
            while remaining:
                hit = None
                for term in bold_terms:
                    idx = remaining.find(term)
                    if idx >= 0 and (hit is None or idx < hit[0]):
                        hit = (idx, term)
                if hit is None:
                    r = p.add_run(); r.text = remaining
                    r.font.name = FONT; r.font.size = Pt(size); r.font.color.rgb = color
                    break
                idx, term = hit
                if idx > 0:
                    r = p.add_run(); r.text = remaining[:idx]
                    r.font.name = FONT; r.font.size = Pt(size); r.font.color.rgb = color
                r = p.add_run(); r.text = term
                r.font.name = FONT; r.font.size = Pt(size); r.font.bold = True; r.font.color.rgb = SEBUM
                remaining = remaining[idx+len(term):]
        else:
            r = p.add_run(); r.text = line
            r.font.name = FONT; r.font.size = Pt(size); r.font.color.rgb = color
        p.space_after = Pt(4)
    return tb


def add_card(slide, left, top, width, height, fill=NEUTROPHILS, border=CARTILAGE):
    rect = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    rect.adjustments[0] = 0.08
    rect.fill.solid(); rect.fill.fore_color.rgb = fill
    rect.line.color.rgb = border; rect.line.width = Pt(0.75)
    return rect


def set_notes(slide, text):
    notes = slide.notes_slide.notes_text_frame
    notes.text = text


def new_slide(num, total=9):
    slide = prs.slides.add_slide(BLANK)
    add_background(slide, ANTIBIOTICS)
    add_header(slide, num, total)
    return slide


# =====================================================================
# SLIDE 1 — Title (Nipun, 30s)
# =====================================================================
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
# Big color block left
block = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(5.0), SH)
block.line.fill.background()
block.fill.solid(); block.fill.fore_color.rgb = SEBUM
# Decorative stripes
for i, c in enumerate([CARTILAGE, SUBSTANTIA, LYMPHATIC]):
    stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(5.0), Inches(1.0 + i*0.15), Inches(0.6), Inches(0.08))
    stripe.line.fill.background(); stripe.fill.solid(); stripe.fill.fore_color.rgb = c

# Big title
tb = s.shapes.add_textbox(Inches(0.5), Inches(1.4), Inches(4.3), Inches(1.4))
tf = tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "Hepato"
r.font.name = FONT; r.font.size = Pt(58); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
p2 = tf.add_paragraph(); p2.alignment = PP_ALIGN.LEFT
r2 = p2.add_run(); r2.text = "Fusion"
r2.font.name = FONT; r2.font.size = Pt(58); r2.font.bold = True; r2.font.color.rgb = LYMPHATIC

tb = s.shapes.add_textbox(Inches(0.5), Inches(4.2), Inches(4.3), Inches(0.5))
p = tb.text_frame.paragraphs[0]
r = p.add_run(); r.text = "CS 5001 Senior Design I — Fall 2026"
r.font.name = FONT; r.font.size = Pt(16); r.font.color.rgb = NEUTROPHILS; r.font.bold = True

tb = s.shapes.add_textbox(Inches(0.5), Inches(4.7), Inches(4.3), Inches(0.4))
p = tb.text_frame.paragraphs[0]
r = p.add_run(); r.text = "Draft Design Presentation"
r.font.name = FONT; r.font.size = Pt(14); r.font.color.rgb = ANTIBIOTICS; r.font.italic = True

# Right side: purpose + goal
add_title(s, "Purpose", top=Inches(0.9), left=Inches(5.6), width=Inches(7.3), size=28, color=SEBUM)
add_plain_text(s, Inches(5.6), Inches(1.5), Inches(7.3), Inches(1.8),
    ["Keep the existing pediatric-liver tumor localization",
     "available to a pathologist as decision support, and",
     "collect radiology, molecular, and cleaned clinical",
     "outcomes onto the same 102-patient cohort."],
    size=16, color=NEAR_BLACK)

add_title(s, "Goal", top=Inches(3.6), left=Inches(5.6), width=Inches(7.3), size=28, color=SEBUM)
add_plain_text(s, Inches(5.6), Inches(4.2), Inches(7.3), Inches(2.4),
    ["Deliver a model-ready outcomes table on the cohort",
     "by December 2026, and a Dockerized tumor-map viewer",
     "prototype validated with Dr. Patel by April 2027.",
     "",
     "Research prototype — not a diagnostic device."],
    size=16, color=NEAR_BLACK)
add_footer(s, "Nipun Chandra", 30)
set_notes(s,
"SPEAKER: Nipun. 30 seconds. Open: 'Good afternoon, I'm Nipun Chandra, and with Shivam Kharangate I'm presenting HepatoFusion — our senior-design project with Cincinnati Children's Hospital.' Then state the purpose (helper + cohort collection) and the goal (cleaned outcomes by Dec, Docker viewer by April). Close with 'research prototype, not a diagnostic device.'")

# =====================================================================
# SLIDE 2 — Team & Advisor (Shivam, 30s)
# =====================================================================
s = new_slide(2)
add_title(s, "Team and advisor")
add_accent_rule(s)

# Team card
add_card(s, Inches(0.6), Inches(1.7), Inches(6.1), Inches(4.3), fill=NEUTROPHILS)
add_plain_text(s, Inches(0.9), Inches(1.85), Inches(5.7), Inches(0.5),
    ["Team"], size=22, color=SEBUM)
add_plain_text(s, Inches(0.9), Inches(2.4), Inches(5.7), Inches(0.6),
    ["Shivam Sinay Kharangate"], size=18, color=NEAR_BLACK)
add_plain_text(s, Inches(0.9), Inches(2.85), Inches(5.7), Inches(0.5),
    ["Pathology CV / multimodal ML; clinical liaison"], size=14, color=CARTILAGE)
add_plain_text(s, Inches(0.9), Inches(3.3), Inches(5.7), Inches(0.5),
    ["sinayksp@mail.uc.edu"], size=14, color=SEBUM)

add_plain_text(s, Inches(0.9), Inches(4.0), Inches(5.7), Inches(0.6),
    ["Nipun Chandra"], size=18, color=NEAR_BLACK)
add_plain_text(s, Inches(0.9), Inches(4.45), Inches(5.7), Inches(0.5),
    ["Data engineering / systems; pipeline reliability"], size=14, color=CARTILAGE)
add_plain_text(s, Inches(0.9), Inches(4.9), Inches(5.7), Inches(0.5),
    ["chandrnu@mail.uc.edu"], size=14, color=SEBUM)

# Advisor card
add_card(s, Inches(7.0), Inches(1.7), Inches(5.8), Inches(4.3), fill=LYMPHATIC, border=SEBUM)
add_plain_text(s, Inches(7.3), Inches(1.85), Inches(5.3), Inches(0.5),
    ["Advisor"], size=22, color=SEBUM)
add_plain_text(s, Inches(7.3), Inches(2.4), Inches(5.3), Inches(0.6),
    ["Dr. Kalyani Patel"], size=18, color=NEAR_BLACK)
add_plain_text(s, Inches(7.3), Inches(2.85), Inches(5.3), Inches(0.9),
    ["Department of Pathology & Laboratory Medicine,",
     "Cincinnati Children's Hospital"], size=14, color=SEBUM)
add_plain_text(s, Inches(7.3), Inches(3.75), Inches(5.3), Inches(0.5),
    ["Kalyani.Patel@cchmc.org"], size=14, color=SEBUM)

add_plain_text(s, Inches(7.3), Inches(4.35), Inches(5.3), Inches(0.5),
    ["Additional advisors"], size=14, color=SEBUM)
add_plain_text(s, Inches(7.3), Inches(4.75), Inches(5.3), Inches(1.0),
    ["Dr. S. Ranganathan   |   Dr. S. Prasath   |   C. Woods",
     "Partner: Cincinnati Children's Hospital"], size=13, color=NEAR_BLACK)

add_footer(s, "Shivam Sinay Kharangate", 30)
set_notes(s,
"SPEAKER: Shivam. 30 seconds. Introduce the two of us: me on pathology CV and clinical liaison, Nipun on data engineering and systems. Our advisor is Dr. Kalyani Patel in Pathology & Laboratory Medicine at Cincinnati Children's, confirmed through April 2027. We also consult Dr. Ranganathan, Dr. Prasath, and Chris Woods. CCHMC is our clinical partner.")

# =====================================================================
# SLIDE 3 — Abstract (Nipun, 80s)
# =====================================================================
s = new_slide(3)
add_title(s, "Project abstract")
add_accent_rule(s)

bold_terms = [
    "multimodal", "pediatric liver cancer", "Silver/Gold",
    "whole-slide", "pathology U-Net", "0.96 mean-slide Dice",
    "0.99 tumor AUROC", "model-ready", "decision support",
    "PathPresenter", "QuPath", "research prototype",
]

abstract_lines = [
    "HepatoFusion is a multimodal research pipeline developed with Cincinnati Children's",
    "Hospital for pediatric liver cancer decision support. The existing Silver/Gold",
    "whole-slide workflow has produced 1,566 Silver and 1,546 Gold annotations across",
    "248 slides from 102 patients, powering a pathology U-Net at 0.96 mean-slide Dice",
    "and 0.99 tumor AUROC for localization. This senior-design work finalizes a",
    "model-ready clinical-outcomes table, inventories the cohort, and surfaces the",
    "existing tumor map inside PathPresenter and QuPath as a pathologist helper.",
    "Radiology and molecular intake remain scoped for a later research risk score.",
    "The system is a research prototype, not a diagnostic device.",
]
add_plain_text(s, Inches(0.7), Inches(1.75), Inches(12.0), Inches(5.0),
    abstract_lines, size=16, color=NEAR_BLACK, line_spacing=1.35,
    bold_terms=bold_terms)

# Word-count caption
add_plain_text(s, Inches(0.7), Inches(6.7), Inches(12.0), Inches(0.3),
    ["—  Approx. 100 words  |  Key terms bolded in accent"],
    size=11, color=CARTILAGE)
add_footer(s, "Nipun Chandra", 80)
set_notes(s,
"SPEAKER: Nipun. 80 seconds. Read the abstract aloud at a measured pace, letting the bolded terms land: multimodal, pediatric liver cancer, Silver/Gold, pathology U-Net metrics, model-ready outcomes, PathPresenter and QuPath, research prototype. Make sure the last sentence 'research prototype, not a diagnostic device' is spoken clearly — it is the ethical throughline for the whole talk.")

# =====================================================================
# SLIDE 4 — User stories & design diagrams (Shivam, 95s)
# =====================================================================
s = new_slide(4)
add_title(s, "User stories and D0 pipeline")
add_accent_rule(s)

# Left: user stories as a tight list
add_plain_text(s, Inches(0.6), Inches(1.7), Inches(5.8), Inches(0.4),
    ["Five user stories (Week 4)"], size=18, color=SEBUM)
us_items = [
    ("US-01 Pathologist helper", "Existing tumor map as decision support"),
    ("US-02 Case-level risk estimate", "Names only inputs actually used"),
    ("US-03 Radiology link", "CT or MRI linked, or recorded as not-linked"),
    ("US-04 Outcomes engineer", "One cohort row, agreed fields coded"),
    ("US-05 PHI gate", "Block identifier values from leaving storage"),
]
y = 2.25
for title, desc in us_items:
    add_plain_text(s, Inches(0.6), Inches(y), Inches(5.9), Inches(0.35),
        [title], size=15, color=SEBUM)
    add_plain_text(s, Inches(0.6), Inches(y+0.32), Inches(5.9), Inches(0.35),
        [desc], size=14, color=NEAR_BLACK)
    y += 0.78

# Right: redrawn D0 pipeline (live-room version — simplified)
add_plain_text(s, Inches(6.9), Inches(1.7), Inches(6.2), Inches(0.4),
    ["D0 pipeline (redrawn for the live room)"], size=18, color=SEBUM)

# Pipeline boxes top row
row_top = 2.2
box_w, box_h = 1.85, 0.75
gap = 0.1

def draw_pipeline_box(s, left_in, top_in, w_in, h_in, text, fill=LYMPHATIC, dashed=False, text_color=None):
    rect = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_in), Inches(top_in), Inches(w_in), Inches(h_in))
    rect.adjustments[0] = 0.18
    rect.fill.solid(); rect.fill.fore_color.rgb = fill
    rect.line.color.rgb = SEBUM; rect.line.width = Pt(1.0)
    if dashed:
        rect.line.dash_style = 7  # dashed
    tf = rect.text_frame; tf.word_wrap = True
    tf.margin_left=Inches(0.05); tf.margin_right=Inches(0.05)
    tf.margin_top=Inches(0.03); tf.margin_bottom=Inches(0.03)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(12); r.font.bold = True
    r.font.color.rgb = text_color if text_color else SEBUM

def draw_arrow(s, x1, y1, x2, y2):
    line = s.shapes.add_connector(1, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    line.line.color.rgb = SEBUM; line.line.width = Pt(1.75)
    # arrowhead via XML
    ln = line.line._get_or_add_ln()
    tail = etree.SubElement(ln, qn('a:tailEnd'))
    tail.set('type', 'triangle'); tail.set('w', 'med'); tail.set('len', 'med')

# Row 1: external (dashed)
draw_pipeline_box(s, 6.9, row_top, box_w, box_h, "Hospital sources\n(Epic, eSlide)", fill=ANTIBIOTICS, dashed=True)
draw_pipeline_box(s, 6.9+box_w+gap, row_top, box_w, box_h, "Identifier gate", fill=LYMPHATIC)
draw_pipeline_box(s, 6.9+2*(box_w+gap), row_top, box_w, box_h, "Cohort case\nindex", fill=LYMPHATIC)

draw_arrow(s, 6.9+box_w, row_top+box_h/2, 6.9+box_w+gap, row_top+box_h/2)
draw_arrow(s, 6.9+2*box_w+gap, row_top+box_h/2, 6.9+2*(box_w+gap), row_top+box_h/2)

# Row 2
row2 = row_top + box_h + 0.45
draw_pipeline_box(s, 6.9, row2, box_w, box_h, "Outcomes\ncleaner (ALG-01)", fill=NEUTROPHILS)
draw_pipeline_box(s, 6.9+box_w+gap, row2, box_w, box_h, "Modality intake\n(iced)", fill=ANTIBIOTICS)
draw_pipeline_box(s, 6.9+2*(box_w+gap), row2, box_w, box_h, "Modality\nintegrator (iced)", fill=ANTIBIOTICS)

# Down arrow from cohort index to row 2
draw_arrow(s, 6.9+2.5*(box_w+gap)-box_w/2, row_top+box_h, 6.9+2.5*(box_w+gap)-box_w/2, row2)
draw_arrow(s, 6.9+box_w, row2+box_h/2, 6.9+box_w+gap, row2+box_h/2)
draw_arrow(s, 6.9+2*box_w+gap, row2+box_h/2, 6.9+2*(box_w+gap), row2+box_h/2)

# Row 3
row3 = row2 + box_h + 0.45
draw_pipeline_box(s, 6.9, row3, box_w, box_h, "Risk scorer\n(iced)", fill=ANTIBIOTICS)
draw_pipeline_box(s, 6.9+box_w+gap, row3, box_w, box_h, "Review package", fill=LYMPHATIC)
draw_pipeline_box(s, 6.9+2*(box_w+gap), row3, box_w, box_h, "PathPresenter\n+ QuPath", fill=ANTIBIOTICS, dashed=True)

draw_arrow(s, 6.9+box_w, row3+box_h/2, 6.9+box_w+gap, row3+box_h/2)
draw_arrow(s, 6.9+2*box_w+gap, row3+box_h/2, 6.9+2*(box_w+gap), row3+box_h/2)
# down from row 2 col 1 into row 3 col 1
draw_arrow(s, 6.9+box_w/2, row2+box_h, 6.9+box_w/2, row3)

# Legend
add_plain_text(s, Inches(6.9), Inches(row3+box_h+0.2), Inches(6.2), Inches(0.35),
    ["Dashed box = external system / iced for 2026. Full D1/D2 in backup."],
    size=11, color=CARTILAGE)

add_footer(s, "Shivam Sinay Kharangate", 95)
set_notes(s,
"SPEAKER: Shivam. 95 seconds. Walk the five user stories left-to-right in 35 seconds — US-01 and US-02 are the pathologist; US-03 is radiology; US-04 is the research engineer; US-05 is the privacy reviewer. Spend the remaining 60 seconds on the redrawn D0: external hospital sources on the left, identifier gate guards everything that enters, cohort case index is the join point, outcomes cleaner runs ALG-01, and the review package is what lands in PathPresenter or QuPath. Point out the dashed boxes are 'on ice' for this academic year — radiology intake, genomics, and the risk scorer. The full D1 and D2 diagrams are in backup.")

# =====================================================================
# SLIDE 5 — Constraints (Nipun, 75s)
# =====================================================================
s = new_slide(5)
add_title(s, "Major project constraints")
add_accent_rule(s)

cards = [
    ("Ethical", "Decision support only; Silver labels never shown as ground truth.", LYMPHATIC),
    ("Privacy & security", "PHI stays on approved CCHMC / UC compute; no consumer cloud.", NEUTROPHILS),
    ("Legal / regulatory", "CCHMC data-use agreement + UC IP; no FDA diagnostic claim.", LYMPHATIC),
    ("Economic", "Open-source PyTorch stack; reuse existing Silver/Gold pipeline.", NEUTROPHILS),
    ("Compute", "Staged fusion fits inside existing GPU allocation.", LYMPHATIC),
]

col_w = 2.42
col_gap = 0.08
total_w = 5*col_w + 4*col_gap  # ≈ 12.42
start_x = (13.333 - total_w) / 2

for i, (title, body, fill) in enumerate(cards):
    x = start_x + i*(col_w + col_gap)
    add_card(s, Inches(x), Inches(1.9), Inches(col_w), Inches(3.5), fill=fill)
    # Title ribbon
    ribbon = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(1.9), Inches(col_w), Inches(0.55))
    ribbon.line.fill.background(); ribbon.fill.solid(); ribbon.fill.fore_color.rgb = SEBUM
    tf = ribbon.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.1); tf.margin_right = Inches(0.1)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = title
    r.font.name = FONT; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
    # Body
    add_plain_text(s, Inches(x+0.15), Inches(2.6), Inches(col_w-0.3), Inches(2.6),
        [body], size=14, color=NEAR_BLACK, line_spacing=1.25)

# Trade-off strip
tradeoff = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.7), Inches(12.1), Inches(1.1))
tradeoff.adjustments[0] = 0.15
tradeoff.fill.solid(); tradeoff.fill.fore_color.rgb = CARTILAGE
tradeoff.line.fill.background()
tf = tradeoff.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left=Inches(0.3); tf.margin_right=Inches(0.3)
tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "Central trade-off:  "
r.font.name = FONT; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
r2 = p.add_run()
r2.text = "security and compliance first — accepting slower multimodal scale in exchange for a prototype that fits inside the CCHMC data-use envelope."
r2.font.name = FONT; r2.font.size = Pt(15); r2.font.color.rgb = ANTIBIOTICS

add_footer(s, "Nipun Chandra", 75)
set_notes(s,
"SPEAKER: Nipun. 75 seconds. Walk the five constraint cards left-to-right in ~45 seconds — ethical (decision support, Silver never as ground truth), privacy (PHI stays on approved compute, no consumer cloud), legal (CCHMC DUA plus UC IP, no FDA claim), economic (open-source stack, reuse existing pipeline), compute (staged fusion inside GPU budget). Spend the last 30 seconds on the trade-off banner: 'the sharpest tension is security and compliance versus development speed. We chose compliance-first scoping, even where that delays fusion features.'")

# =====================================================================
# SLIDE 6 — Review of project progress (Shivam, 80s)
# =====================================================================
s = new_slide(6)
add_title(s, "Project progress — Weeks 1-11")
add_accent_rule(s)

# Left column: completed deliverables
add_plain_text(s, Inches(0.6), Inches(1.7), Inches(6.3), Inches(0.4),
    ["Completed deliverables"], size=18, color=SEBUM)
completed = [
    ("W1-W2", "Team contract, project description, bios"),
    ("W3", "Constraints essay"),
    ("W4", "User stories & use cases (US-01–US-05)"),
    ("W5-W7", "D0 high-level, D1 detailed, D2 error paths + peer review"),
    ("W8", "Task list, timeline, effort matrix, risk register"),
    ("W9", "Requirements doc v1.0, tech spec v1.1"),
    ("W10", "Test plan v1.0 (TC-001 – TC-016)"),
    ("W11", "Ethics statement, AI-use disclosure"),
]
y = 2.2
for wk, item in completed:
    # week chip
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(y), Inches(0.95), Inches(0.32))
    chip.adjustments[0] = 0.5
    chip.fill.solid(); chip.fill.fore_color.rgb = SEBUM; chip.line.fill.background()
    tf = chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left=Inches(0.03); tf.margin_right=Inches(0.03)
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = wk
    r.font.name = FONT; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
    # item text
    add_plain_text(s, Inches(1.7), Inches(y+0.02), Inches(5.3), Inches(0.35),
        [item], size=14, color=NEAR_BLACK)
    y += 0.42

# Right column: inherited backbone stats (large)
add_plain_text(s, Inches(7.4), Inches(1.7), Inches(5.5), Inches(0.4),
    ["Inherited backbone (not rebuilt)"], size=18, color=SEBUM)

stats = [
    ("1,566", "Silver annotations"),
    ("1,546", "Gold annotations"),
    ("248", "whole-slide images"),
    ("102", "patients in the cohort"),
]
y = 2.2
for num, label in stats:
    add_card(s, Inches(7.4), Inches(y), Inches(5.5), Inches(0.68), fill=NEUTROPHILS)
    add_plain_text(s, Inches(7.55), Inches(y+0.05), Inches(2.0), Inches(0.6),
        [num], size=24, color=SEBUM)
    add_plain_text(s, Inches(9.5), Inches(y+0.17), Inches(3.4), Inches(0.5),
        [label], size=15, color=NEAR_BLACK)
    y += 0.78

# Metrics highlight
add_card(s, Inches(7.4), Inches(5.42), Inches(5.5), Inches(1.4), fill=LYMPHATIC, border=SEBUM)
add_plain_text(s, Inches(7.55), Inches(5.5), Inches(5.2), Inches(0.4),
    ["Pathology U-Net metrics"], size=14, color=SEBUM)
add_plain_text(s, Inches(7.55), Inches(5.9), Inches(5.2), Inches(0.9),
    ["0.96  mean-slide Dice",
     "0.98  tumor Dice   |   0.99  tumor AUROC"],
    size=16, color=NEAR_BLACK, line_spacing=1.2)

add_footer(s, "Shivam Sinay Kharangate", 80)
set_notes(s,
"SPEAKER: Shivam. 80 seconds. Walk left column top-to-bottom quickly (~35s): every graded deliverable from weeks 1 through 11 is complete and committed to the repo. Then shift to the right (~45s): remind the audience that the Silver/Gold whole-slide pipeline is inherited, not rebuilt — 1,566 Silver, 1,546 Gold, 248 WSIs, 102 patients. Close on the pathology U-Net metrics card: 0.96 mean-slide Dice and 0.99 tumor AUROC are the baseline we start from, not what we promise this year.")

# =====================================================================
# SLIDE 7 — Expected accomplishments EOT (Nipun, 65s)
# =====================================================================
s = new_slide(7)
add_title(s, "Expected accomplishments  —  end of Fall 2026")
add_accent_rule(s)

# Date pill
pill = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.6), Inches(3.2), Inches(0.45))
pill.adjustments[0] = 0.5
pill.fill.solid(); pill.fill.fore_color.rgb = SEBUM; pill.line.fill.background()
tf = pill.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
r = p.add_run(); r.text = "Target: 4 Dec 2026  (M17)"
r.font.name = FONT; r.font.size = Pt(14); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS

items = [
    ("T1", "Epic clinical fields landed on approved storage", "Shivam"),
    ("T2", "eSlide / PathPresenter inventory in Cohort case index", "Nipun"),
    ("T3", "First-pass Excel coded, agreed fields coded or numeric", "Nipun"),
    ("T6", "U-Net outlier list closed on Gold slides (M25)", "Shivam"),
    ("T11", "TMA keys handed to radiology collaborator", "Shivam"),
    ("T12", "Identifier-gate rules frozen in pipeline_config.yaml (M18)", "Nipun"),
]

y = 2.3
for tid, text, owner in items:
    add_card(s, Inches(0.6), Inches(y), Inches(12.1), Inches(0.62), fill=NEUTROPHILS)
    # task ID chip
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), Inches(y+0.1), Inches(0.75), Inches(0.42))
    chip.adjustments[0] = 0.5
    chip.fill.solid(); chip.fill.fore_color.rgb = CARTILAGE; chip.line.fill.background()
    tf = chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = tid
    r.font.name = FONT; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
    # text
    add_plain_text(s, Inches(1.7), Inches(y+0.15), Inches(8.8), Inches(0.4),
        [text], size=15, color=NEAR_BLACK)
    # owner chip
    owner_chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.7), Inches(y+0.1), Inches(1.85), Inches(0.42))
    owner_chip.adjustments[0] = 0.5
    owner_chip.fill.solid(); owner_chip.fill.fore_color.rgb = SEBUM; owner_chip.line.fill.background()
    tf = owner_chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = owner
    r.font.name = FONT; r.font.size = Pt(12); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
    y += 0.72

# Not promising banner
banner = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(y+0.1), Inches(12.1), Inches(0.42))
banner.adjustments[0] = 0.5
banner.fill.solid(); banner.fill.fore_color.rgb = LYMPHATIC; banner.line.color.rgb = SEBUM
banner.line.width = Pt(0.75)
tf = banner.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.2)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "Not promised in Fall: "
r.font.name = FONT; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = SEBUM
r2 = p.add_run(); r2.text = "radiology intake, genomics, modality integrator, risk scorer — all iced until M36 in Spring."
r2.font.name = FONT; r2.font.size = Pt(13); r2.font.color.rgb = NEAR_BLACK

add_footer(s, "Nipun Chandra", 65)
set_notes(s,
"SPEAKER: Nipun. 65 seconds. Frame M17 as the December 4 checkpoint. Read the six owned items in ~35 seconds, showing which ones Shivam owns (T1, T6, T11) and which ones I own (T2, T3, T12). Close with the honesty banner: radiology intake, genomics, the modality integrator, and the risk scorer are iced until M36 in April. We will not claim a fused risk number in December.")

# =====================================================================
# SLIDE 8 — Division of work (Shivam, 85s)
# =====================================================================
s = new_slide(8)
add_title(s, "Division of work  —  114 / 114 hours (50 / 50)")
add_accent_rule(s)

# Two columns of task ownership
col_specs = [
    ("Shivam  (114 h)", SEBUM, [
        ("T1", "Obtain Epic clinical fields"),
        ("T4", "Investigate IHC join into case index"),
        ("T6", "U-Net outlier investigation"),
        ("T7", "Refine pathology U-Net on Gold"),
        ("T9", "PathPresenter overlay + Review package"),
        ("T11", "TMA-grid study keys (radiology side)"),
        ("T14", "Validate helper with Dr. Patel"),
        ("T16", "Modality integrator  (iced)"),
    ]),
    ("Nipun  (114 h)", CARTILAGE, [
        ("T2", "eSlide / PathPresenter inventory"),
        ("T3", "Patient-by-patient Excel cleanup"),
        ("T5", "case_link.json records"),
        ("T8", "Dockerize U-Net for QuPath"),
        ("T10", "Test QuPath Docker on holdout WSI"),
        ("T12", "Identifier-gate rules in config"),
        ("T13", "Outcomes cleaner ALG-01 run"),
        ("T15", "Radiology intake design  (iced)"),
    ]),
]

col_x = [0.6, 6.95]
col_w = 5.78

for ci, (header, color, rows) in enumerate(col_specs):
    x = col_x[ci]
    # Header
    hdr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(1.7), Inches(col_w), Inches(0.5))
    hdr.adjustments[0] = 0.25
    hdr.fill.solid(); hdr.fill.fore_color.rgb = color; hdr.line.fill.background()
    tf = hdr.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = header
    r.font.name = FONT; r.font.size = Pt(18); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
    y = 2.35
    for tid, label in rows:
        row_bg = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(col_w), Inches(0.5))
        row_bg.adjustments[0] = 0.15
        row_bg.fill.solid(); row_bg.fill.fore_color.rgb = NEUTROPHILS if (int(y*10) % 2 == 0) else LYMPHATIC
        row_bg.line.fill.background()
        # tid chip
        chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x+0.12), Inches(y+0.08), Inches(0.7), Inches(0.34))
        chip.adjustments[0] = 0.5
        chip.fill.solid(); chip.fill.fore_color.rgb = SEBUM; chip.line.fill.background()
        tf = chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
        r = p.add_run(); r.text = tid
        r.font.name = FONT; r.font.size = Pt(11); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
        add_plain_text(s, Inches(x+0.95), Inches(y+0.12), Inches(col_w-1.0), Inches(0.35),
            [label], size=14, color=NEAR_BLACK)
        y += 0.55

# Bottom note
note = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(6.7), Inches(12.1), Inches(0.4))
note.adjustments[0] = 0.4
note.fill.solid(); note.fill.fore_color.rgb = LYMPHATIC; note.line.fill.background()
tf = note.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left = Inches(0.2)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "8 owned tasks each  |  totals confirmed by both members  |  T3 is the overrun candidate (pessimistic 32 h)"
r.font.name = FONT; r.font.size = Pt(12); r.font.color.rgb = SEBUM

add_footer(s, "Shivam Sinay Kharangate", 85)
set_notes(s,
"SPEAKER: Shivam. 85 seconds. Walk the two columns in parallel. Left is mine: pathology-side work — Epic fields with Dr. Patel, IHC join, U-Net outliers and refine, PathPresenter overlay, validation, and the iced Modality integrator. Right is Nipun's: data-engineering side — eSlide inventory, Excel cleanup, case_link.json, Docker for QuPath, the identifier-gate config, ALG-01, and the iced Radiology intake. Columns total 114 and 114 — 50/50. Finish with the honest note at the bottom: T3 is the overrun candidate, with a documented reassignment plan if Nipun exceeds 17 hours before 24 November.")

# =====================================================================
# SLIDE 9 — Expo Demo & Fallback (Nipun, 60s)
# =====================================================================
s = new_slide(9)
add_title(s, "Expected demo at Expo")
add_accent_rule(s)

# Primary demo card
add_card(s, Inches(0.6), Inches(1.7), Inches(6.1), Inches(2.6), fill=NEUTROPHILS)
ribbon = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(1.7), Inches(6.1), Inches(0.55))
ribbon.line.fill.background(); ribbon.fill.solid(); ribbon.fill.fore_color.rgb = SEBUM
tf = ribbon.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left=Inches(0.2)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "Primary demo"
r.font.name = FONT; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
add_plain_text(s, Inches(0.8), Inches(2.4), Inches(5.7), Inches(1.9),
    ["Dockerized U-Net inference on a deidentified",
     "holdout whole-slide image, opened in QuPath.",
     "",
     "Followed by the PathPresenter helper overlay",
     "that Dr. Patel validated in M32 (12 Mar 2027)."],
    size=14, color=NEAR_BLACK, line_spacing=1.3)

# Fallback card
add_card(s, Inches(7.0), Inches(1.7), Inches(5.8), Inches(2.6), fill=LYMPHATIC)
ribbon = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(7.0), Inches(1.7), Inches(5.8), Inches(0.55))
ribbon.line.fill.background(); ribbon.fill.solid(); ribbon.fill.fore_color.rgb = CARTILAGE
tf = ribbon.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
tf.margin_left=Inches(0.2)
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "If the live viewer fails"
r.font.name = FONT; r.font.size = Pt(16); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
add_plain_text(s, Inches(7.2), Inches(2.4), Inches(5.4), Inches(1.9),
    ["Pre-recorded QuPath screen capture on the",
     "same holdout slide (recorded on approved compute).",
     "",
     "Plus live ALG-01 run of the Outcomes cleaner,",
     "showing source_rows / kept / excluded counts."],
    size=14, color=NEAR_BLACK, line_spacing=1.3)

# Logistics row
add_plain_text(s, Inches(0.6), Inches(4.6), Inches(6.0), Inches(0.4),
    ["What the booth shows"], size=16, color=SEBUM)
add_plain_text(s, Inches(0.6), Inches(5.0), Inches(6.0), Inches(2.0),
    ["Laptop  with the Docker image + QuPath",
     "Monitor  mirror for the audience view",
     "Printed one-page handout: pipeline + metrics",
     "No PHI, no WSI files, no identifiers displayed"],
    size=14, color=NEAR_BLACK, line_spacing=1.35)

add_plain_text(s, Inches(7.0), Inches(4.6), Inches(5.8), Inches(0.4),
    ["Ground rules"], size=16, color=SEBUM)
add_plain_text(s, Inches(7.0), Inches(5.0), Inches(5.8), Inches(2.0),
    ["Prototype disclaimer spoken aloud at the start",
     "Silver labels never presented as ground truth",
     "Only metrics shown are the backup slide numbers",
     "Dr. Patel's validation note available on request"],
    size=14, color=NEAR_BLACK, line_spacing=1.35)

add_footer(s, "Nipun Chandra", 60)
set_notes(s,
"SPEAKER: Nipun. 60 seconds. Primary demo in 25 seconds: Docker U-Net running on a holdout WSI in QuPath, deidentified, with the PathPresenter overlay as the second scene. Fallback in 15 seconds: a pre-recorded screen capture plus a live ALG-01 run that prints the source_rows / kept / excluded counts — that always works because it needs no viewer. Last 20 seconds: booth logistics and the ground rules — disclaimer spoken aloud, no PHI on screen, Silver never shown as ground truth. Close: 'That ends our ten minutes. Dr. Patel, we're ready for feedback.'")

# =====================================================================
# SLIDE 10 — Advisor Feedback placeholder 1
# =====================================================================
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
# Decorative stripe
stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.35))
stripe.line.fill.background(); stripe.fill.solid(); stripe.fill.fore_color.rgb = CARTILAGE
name = s.shapes.add_textbox(Inches(10.3), Inches(0.03), Inches(3.0), Inches(0.3))
tf = name.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
r = p.add_run(); r.text = "Advisor Feedback  |  Placeholder"
r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = ANTIBIOTICS; r.font.bold = True

add_title(s, "Advisor feedback  —  capture 1", top=Inches(0.6), size=34)
add_accent_rule(s)

add_plain_text(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(0.5),
    ["To be filled after the Week 12 advisor review with Dr. Patel."],
    size=14, color=CARTILAGE)

# 4 feedback slot cards
slots = [
    ("Slide / topic", "Dr. Patel's comment", "Team response", "Owner  |  Status"),
]
# Draw a grid of 4 empty feedback slots
y = 2.1
labels = ["Feedback #1", "Feedback #2", "Feedback #3", "Feedback #4"]
for lab in labels:
    add_card(s, Inches(0.6), Inches(y), Inches(12.1), Inches(1.15), fill=NEUTROPHILS)
    # left label
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), Inches(y+0.2), Inches(1.6), Inches(0.75))
    chip.adjustments[0] = 0.25
    chip.fill.solid(); chip.fill.fore_color.rgb = SEBUM; chip.line.fill.background()
    tf = chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = lab
    r.font.name = FONT; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
    # placeholder lines
    add_plain_text(s, Inches(2.5), Inches(y+0.1), Inches(10.1), Inches(1.0),
        ["Slides affected:  _________________________________________",
         "Comment:  ________________________________________________",
         "Response + change:  ______________________________________   Owner / Status: _____"],
        size=12, color=CARTILAGE, line_spacing=1.4)
    y += 1.25

# Footer
bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.2), SW, Inches(0.3))
bar.line.fill.background(); bar.fill.solid(); bar.fill.fore_color.rgb = NEUTROPHILS
tb = s.shapes.add_textbox(Inches(0.15), Inches(7.22), Inches(13.05), Inches(0.26))
tf = tb.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "Mirrors rows 1-4 of Advisor_Feedback.md"
r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = SEBUM; r.font.bold = True
set_notes(s, "Placeholder slide. Does not count toward the 9-slide budget. Fill rows after the Week 12 advisor meeting; sync with Advisor_Feedback.md. Not spoken aloud in the 10-minute recording.")

# =====================================================================
# SLIDE 11 — Advisor Feedback placeholder 2
# =====================================================================
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
stripe = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.35))
stripe.line.fill.background(); stripe.fill.solid(); stripe.fill.fore_color.rgb = CARTILAGE
name = s.shapes.add_textbox(Inches(10.3), Inches(0.03), Inches(3.0), Inches(0.3))
tf = name.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
r = p.add_run(); r.text = "Advisor Feedback  |  Placeholder"
r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = ANTIBIOTICS; r.font.bold = True

add_title(s, "Advisor feedback  —  capture 2 + summary", top=Inches(0.6), size=34)
add_accent_rule(s)

# Right: Summary of changes + open items
add_plain_text(s, Inches(0.6), Inches(1.5), Inches(12.1), Inches(0.5),
    ["Summary of changes, open items, and additional feedback rows."],
    size=14, color=CARTILAGE)

# More feedback rows
y = 2.1
for lab in ["Feedback #5", "Feedback #6"]:
    add_card(s, Inches(0.6), Inches(y), Inches(12.1), Inches(1.0), fill=NEUTROPHILS)
    chip = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.75), Inches(y+0.17), Inches(1.6), Inches(0.65))
    chip.adjustments[0] = 0.25
    chip.fill.solid(); chip.fill.fore_color.rgb = SEBUM; chip.line.fill.background()
    tf = chip.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = lab
    r.font.name = FONT; r.font.size = Pt(13); r.font.bold = True; r.font.color.rgb = ANTIBIOTICS
    add_plain_text(s, Inches(2.5), Inches(y+0.1), Inches(10.1), Inches(0.85),
        ["Slides affected:  _________________________________________",
         "Comment / Response / Change / Owner / Status: ______________________"],
        size=12, color=CARTILAGE, line_spacing=1.4)
    y += 1.1

# Summary + open items row
add_card(s, Inches(0.6), Inches(y+0.1), Inches(5.95), Inches(2.35), fill=LYMPHATIC)
add_plain_text(s, Inches(0.8), Inches(y+0.2), Inches(5.6), Inches(0.4),
    ["Summary of changes (3-6 sentences)"], size=15, color=SEBUM)
add_plain_text(s, Inches(0.8), Inches(y+0.65), Inches(5.6), Inches(1.7),
    ["____________________________________",
     "____________________________________",
     "____________________________________",
     "____________________________________",
     "____________________________________"],
    size=12, color=CARTILAGE, line_spacing=1.3)

add_card(s, Inches(6.75), Inches(y+0.1), Inches(5.95), Inches(2.35), fill=LYMPHATIC)
add_plain_text(s, Inches(6.95), Inches(y+0.2), Inches(5.6), Inches(0.4),
    ["Open items (with target close date)"], size=15, color=SEBUM)
add_plain_text(s, Inches(6.95), Inches(y+0.65), Inches(5.6), Inches(1.7),
    ["____________________________________",
     "____________________________________",
     "____________________________________",
     "____________________________________",
     "____________________________________"],
    size=12, color=CARTILAGE, line_spacing=1.3)

bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(7.2), SW, Inches(0.3))
bar.line.fill.background(); bar.fill.solid(); bar.fill.fore_color.rgb = NEUTROPHILS
tb = s.shapes.add_textbox(Inches(0.15), Inches(7.22), Inches(13.05), Inches(0.26))
tf = tb.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
r = p.add_run(); r.text = "Mirrors rows 5-6 + §Summary + §Open items of Advisor_Feedback.md"
r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = SEBUM; r.font.bold = True
set_notes(s, "Placeholder slide 2. Not spoken aloud; mirrors Advisor_Feedback.md §Summary of changes and §Open items.")

# =====================================================================
# BACKUP SLIDES
# =====================================================================

def backup_header(slide, title_text):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SW, Inches(0.35))
    bar.line.fill.background(); bar.fill.solid(); bar.fill.fore_color.rgb = CARTILAGE
    name = slide.shapes.add_textbox(Inches(10.3), Inches(0.03), Inches(3.0), Inches(0.3))
    tf = name.text_frame; p = tf.paragraphs[0]; p.alignment = PP_ALIGN.RIGHT
    r = p.add_run(); r.text = "Backup slide"
    r.font.name = FONT; r.font.size = Pt(11); r.font.color.rgb = ANTIBIOTICS; r.font.bold = True
    add_title(slide, title_text, top=Inches(0.55), size=34)
    add_accent_rule(slide, top=Inches(1.3))

# ---- Backup B1: Full D1 data model ----
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
backup_header(s, "Backup  —  D1 data model (full)")
try:
    s.shapes.add_picture("/home/nipun/CS-Senior-Design-I-II/Design_Diagrams/D1_data_model.png",
                         Inches(0.7), Inches(1.5), height=Inches(5.3))
except Exception:
    add_plain_text(s, Inches(0.7), Inches(2.0), Inches(12.0), Inches(0.5),
        ["[D1 data model image]"], size=14, color=CARTILAGE)
add_plain_text(s, Inches(0.7), Inches(6.9), Inches(12.0), Inches(0.4),
    ["Source: Design_Diagrams/D1_Detailed_Design.md"], size=11, color=CARTILAGE)

# ---- Backup B2: Full D2 case lifecycle ----
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
backup_header(s, "Backup  —  D2 case lifecycle (full)")
try:
    s.shapes.add_picture("/home/nipun/CS-Senior-Design-I-II/Design_Diagrams/D2_case_lifecycle.png",
                         Inches(0.7), Inches(1.5), height=Inches(5.3))
except Exception:
    add_plain_text(s, Inches(0.7), Inches(2.0), Inches(12.0), Inches(0.5),
        ["[D2 case lifecycle image]"], size=14, color=CARTILAGE)
add_plain_text(s, Inches(0.7), Inches(6.9), Inches(12.0), Inches(0.4),
    ["Source: Design_Diagrams/D2_Detailed_Design.md"], size=11, color=CARTILAGE)

# ---- Backup B3: D2 error paths ----
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
backup_header(s, "Backup  —  D2 component error paths (full)")
try:
    s.shapes.add_picture("/home/nipun/CS-Senior-Design-I-II/Design_Diagrams/D2_component_error_paths.png",
                         Inches(0.7), Inches(1.5), height=Inches(5.3))
except Exception:
    add_plain_text(s, Inches(0.7), Inches(2.0), Inches(12.0), Inches(0.5),
        ["[D2 error paths image]"], size=14, color=CARTILAGE)
add_plain_text(s, Inches(0.7), Inches(6.9), Inches(12.0), Inches(0.4),
    ["Source: Design_Diagrams/D2_Detailed_Design.md"], size=11, color=CARTILAGE)

# ---- Backup B4: D0 original (for reference) ----
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
backup_header(s, "Backup  —  D0 original block diagram (reference)")
try:
    s.shapes.add_picture("/home/nipun/CS-Senior-Design-I-II/Design_Diagrams/D0_block_diagram.png",
                         Inches(0.7), Inches(1.5), height=Inches(5.3))
except Exception:
    pass
add_plain_text(s, Inches(0.7), Inches(6.9), Inches(12.0), Inches(0.4),
    ["Redrawn on Slide 4 for a live-room read. Source: Design_Diagrams/D0_High_Level_Design.md"],
    size=11, color=CARTILAGE)

# ---- Backup B5: Speaker + timing table ----
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
backup_header(s, "Backup  —  Speaker outline and timing")

rows = [
    ("Slide", "Title", "Visual", "Speaker", "Seconds"),
    ("1", "Title + purpose + goal", "Hero block + text", "Nipun", "30"),
    ("2", "Team and advisor", "Two contact cards", "Shivam", "30"),
    ("3", "Project abstract (~100 w)", "Highlighted paragraph", "Nipun", "80"),
    ("4", "User stories + D0 (redrawn)", "5 USs + pipeline sketch", "Shivam", "95"),
    ("5", "Major constraints", "Five cards + trade-off", "Nipun", "75"),
    ("6", "Project progress", "Completed list + stats", "Shivam", "80"),
    ("7", "Expected EOT accomplishments", "6 task cards", "Nipun", "65"),
    ("8", "Division of work (50/50)", "Two-column T-ID table", "Shivam", "85"),
    ("9", "Expo demo + fallback", "Primary / fallback cards", "Nipun", "60"),
    ("—", "TOTAL", "", "Shivam 290  |  Nipun 310", "600"),
]
col_x = [0.6, 1.3, 4.6, 8.3, 10.6]
col_w = [0.7, 3.3, 3.7, 2.3, 1.6]
y = 1.5
for i, row in enumerate(rows):
    is_header = (i == 0)
    is_total  = (i == len(rows)-1)
    bg_color = SEBUM if is_header else (LYMPHATIC if is_total else (NEUTROPHILS if i % 2 == 1 else ANTIBIOTICS))
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(col_x[0]), Inches(y),
                            Inches(sum(col_w)+0.2), Inches(0.42))
    bg.line.fill.background(); bg.fill.solid(); bg.fill.fore_color.rgb = bg_color
    for j, cell in enumerate(row):
        tb = s.shapes.add_textbox(Inches(col_x[j]+0.08), Inches(y+0.06),
                                   Inches(col_w[j]), Inches(0.35))
        tf = tb.text_frame; tf.margin_left=tf.margin_right=0
        p = tf.paragraphs[0]; p.alignment = PP_ALIGN.LEFT
        r = p.add_run(); r.text = cell
        r.font.name = FONT; r.font.size = Pt(12 if not is_header else 13)
        r.font.bold = is_header or is_total
        r.font.color.rgb = ANTIBIOTICS if is_header else (SEBUM if is_total else NEAR_BLACK)
    y += 0.44

# ---- Backup B6: Recording plan + AI use ----
s = prs.slides.add_slide(BLANK)
add_background(s, ANTIBIOTICS)
backup_header(s, "Backup  —  Recording plan and AI use")

add_plain_text(s, Inches(0.6), Inches(1.45), Inches(6.2), Inches(0.4),
    ["Recording plan"], size=20, color=SEBUM)
add_plain_text(s, Inches(0.6), Inches(1.95), Inches(6.2), Inches(5.0),
    ["Presenters:  Shivam Kharangate + Nipun Chandra",
     "Software:  PowerPoint Record Slide Show",
     "Target length:  10:00 (±10 s)",
     "Rehearsal recording:  before Week 12 review",
     "Final recording:  Week 13 upload window",
     "Deck + video links posted by:  Nipun",
     "Shared link location:  team project spreadsheet",
     "Repo path:  Presentation/ folder",
     "Commit hash:  recorded in Canvas submission"],
    size=14, color=NEAR_BLACK, line_spacing=1.3)

add_plain_text(s, Inches(7.0), Inches(1.45), Inches(5.8), Inches(0.4),
    ["AI use (Assignment #8 draft)"], size=20, color=SEBUM)
add_plain_text(s, Inches(7.0), Inches(1.95), Inches(5.8), Inches(5.0),
    ["Tool:  Claude (Anthropic) via Claude Code CLI",
     "",
     "Used for: layout scaffolding of the deck,",
     "timing-table formatting, and prose polish of",
     "the abstract and bullet phrasings.",
     "",
     "The team wrote all technical content, timing",
     "numbers, task assignments, metrics, and",
     "advisor-facing commitments. Content was",
     "confirmed by both members prior to draft",
     "submission."],
    size=13, color=NEAR_BLACK, line_spacing=1.25)

# =====================================================================
# Save
# =====================================================================
out_path = "/home/nipun/CS-Senior-Design-I-II/Presentation/HepatoFusion_Draft_Deck.pptx"
prs.save(out_path)
print(f"Wrote {out_path}")
print(f"Slide count: {len(prs.slides)}")
