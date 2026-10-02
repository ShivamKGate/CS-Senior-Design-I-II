"""Generate accurate HepatoFusion D0 block and data-flow PNGs."""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

OUT = Path(__file__).resolve().parent


def box(ax, x, y, w, h, text, external=False, fontsize=8):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.05",
        linewidth=1.6,
        edgecolor="#4a5568" if external else "#1d4ed8",
        facecolor="#f7fafc" if external else "#dbeafe",
        linestyle="--" if external else "-",
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, color="#1a202c")
    return patch


def arrow(ax, x1, y1, x2, y2, label="", label_offset=(0, 0.12), fontsize=7):
    ax.annotate(
        "",
        xy=(x2, y2),
        xytext=(x1, y1),
        arrowprops=dict(arrowstyle="->", color="#2d3748", lw=1.3),
    )
    if label:
        mx, my = (x1 + x2) / 2 + label_offset[0], (y1 + y2) / 2 + label_offset[1]
        ax.text(mx, my, label, ha="center", va="bottom", fontsize=fontsize, color="#1a365d")


def make_block():
    fig, ax = plt.subplots(figsize=(17, 11), dpi=180)
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_title(
        "HepatoFusion D0 Block Diagram\n"
        "Goal: Collect radiology, molecular, and cleaned outcomes; integrate with finished pathology "
        "localization into a research risk score for PathPresenter",
        fontsize=11,
        pad=14,
    )

    # Column 1: externals
    box(ax, 0.4, 9.2, 2.6, 0.9, "Radiology team\n(external)", external=True)
    box(ax, 0.4, 8.0, 2.6, 0.9, "Molecular Excel\n(external)", external=True)
    box(ax, 0.4, 6.4, 2.6, 0.9, "Outcomes spreadsheet\n(external)", external=True)
    box(ax, 0.4, 4.6, 2.6, 1.1, "Existing pathology\npipeline / U-Net\n(external)", external=True)

    # Column 2-3: built
    box(ax, 4.0, 8.4, 2.6, 1.0, "Identifier gate")
    box(ax, 7.5, 9.3, 2.5, 0.8, "Radiology intake")
    box(ax, 7.5, 7.9, 2.5, 0.8, "Genomics intake")
    box(ax, 4.0, 6.4, 2.6, 0.9, "Outcomes cleaner")
    box(ax, 11.0, 8.2, 2.7, 1.1, "Cohort case index")
    box(ax, 11.0, 5.8, 2.7, 1.0, "Modality integrator")
    box(ax, 11.0, 4.2, 2.7, 0.9, "Risk scorer")
    box(ax, 11.0, 2.6, 2.7, 0.9, "Review package")

    # Column 4: viewers
    box(ax, 14.4, 2.6, 2.2, 0.9, "PathPresenter\n(external)", external=True, fontsize=7)
    box(ax, 14.4, 1.2, 2.2, 0.9, "Pathologist\n(external)", external=True, fontsize=7)
    box(ax, 14.4, 4.4, 2.2, 1.0, "QuPath\nalternate, not wired", external=True, fontsize=7)

    # Arrows matching interface table
    arrow(ax, 3.0, 9.65, 4.0, 9.1, "I1 DICOM", (0, 0.15))
    arrow(ax, 3.0, 8.45, 4.0, 8.7, "I2 xlsx", (0, -0.2))
    arrow(ax, 6.6, 9.2, 7.5, 9.6, "I3 accepted DICOM", (0.1, 0.15))
    arrow(ax, 6.6, 8.6, 7.5, 8.2, "I4 accepted xlsx", (0.1, -0.25))
    arrow(ax, 3.0, 6.85, 4.0, 6.85, "I5 xlsx", (0, 0.12))
    arrow(ax, 10.0, 9.6, 11.0, 9.0, "I7", (-0.1, 0.15))
    arrow(ax, 10.0, 8.2, 11.0, 8.5, "I8", (-0.1, -0.2))
    arrow(ax, 6.6, 6.85, 11.0, 8.4, "I9 model-ready/\nexclusion", (0.4, -0.35))
    arrow(ax, 3.0, 5.4, 11.0, 8.5, "I6 study ID +\nlocalization ref", (-1.2, 0.9))
    arrow(ax, 12.35, 8.2, 12.35, 6.8, "I10 case link", (0.55, 0))
    arrow(ax, 3.0, 5.0, 11.0, 6.2, "I11 localization ref", (-0.8, -0.35))
    arrow(ax, 12.35, 5.8, 12.35, 5.1, "I12", (0.35, 0))
    arrow(ax, 12.35, 4.2, 12.35, 3.5, "I13", (0.35, 0))
    arrow(ax, 13.7, 3.05, 14.4, 3.05, "I14", (0, 0.12))
    arrow(ax, 15.5, 2.6, 15.5, 2.1, "I15", (0.35, 0))

    legend = Rectangle((0.4, 0.3), 6.2, 1.5, linewidth=1, edgecolor="#718096", facecolor="#fff")
    ax.add_patch(legend)
    ax.text(0.55, 1.55, "Legend", fontsize=9, fontweight="bold")
    box(ax, 0.6, 0.55, 1.7, 0.6, "we build", fontsize=7)
    box(ax, 2.5, 0.55, 1.7, 0.6, "external", external=True, fontsize=7)
    ax.text(4.4, 0.85, "Arrow = file handoff in\napproved shared folder", fontsize=7, va="center")

    fig.tight_layout()
    path = OUT / "D0_block_diagram.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


def make_dataflow():
    fig, ax = plt.subplots(figsize=(16, 10), dpi=180)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(
        "HepatoFusion D0 Data-Flow Diagram\n"
        "Flow A = collection (now). Flow B = integration later. No timing budget; constraint is approved compute location.",
        fontsize=11,
        pad=12,
    )

    ax.text(0.3, 9.5, "Flow A — Collection", fontsize=12, fontweight="bold", color="#1d4ed8")

    y = 8.3
    box(ax, 0.3, y, 2.0, 0.8, "Radiology team", external=True, fontsize=7)
    arrow(ax, 2.3, y + 0.4, 2.9, y + 0.4, "raw DICOM")
    box(ax, 2.9, y, 2.1, 0.8, "Identifier gate", fontsize=7)
    arrow(ax, 5.0, y + 0.4, 5.6, y + 0.4, "accepted / block")
    box(ax, 5.6, y, 2.1, 0.8, "Radiology intake", fontsize=7)
    arrow(ax, 7.7, y + 0.4, 8.3, y + 0.4, "DICOM + link status")
    box(ax, 8.3, y, 2.4, 0.8, "Cohort case index", fontsize=7)

    y = 7.1
    box(ax, 0.3, y, 2.0, 0.8, "Molecular Excel", external=True, fontsize=7)
    arrow(ax, 2.3, y + 0.4, 2.9, y + 0.4, "raw xlsx")
    box(ax, 2.9, y, 2.1, 0.8, "Identifier gate", fontsize=7)
    arrow(ax, 5.0, y + 0.4, 5.6, y + 0.4, "accepted / block")
    box(ax, 5.6, y, 2.1, 0.8, "Genomics intake", fontsize=7)
    arrow(ax, 7.7, y + 0.4, 8.3, y + 0.4, "xlsx + link status")
    box(ax, 8.3, y, 2.4, 0.8, "Cohort case index", fontsize=7)

    y = 5.9
    box(ax, 0.3, y, 2.0, 0.8, "Outcomes\nspreadsheet", external=True, fontsize=7)
    arrow(ax, 2.3, y + 0.4, 2.9, y + 0.4, "raw row")
    box(ax, 2.9, y, 2.8, 0.8, "Outcomes cleaner", fontsize=7)
    arrow(ax, 5.7, y + 0.4, 8.3, y + 0.4, "model-ready or exclusion")
    box(ax, 8.3, y, 2.4, 0.8, "Cohort case index", fontsize=7)

    y = 4.7
    box(ax, 0.3, y, 2.8, 0.8, "Existing pathology\npipeline", external=True, fontsize=7)
    arrow(ax, 3.1, y + 0.4, 8.3, y + 0.4, "study ID + localization pointer")
    box(ax, 8.3, y, 2.4, 0.8, "Cohort case index", fontsize=7)

    ax.text(0.3, 4.1, "Flow B — Integration", fontsize=12, fontweight="bold", color="#1d4ed8")

    y = 2.8
    box(ax, 0.3, y, 2.2, 0.9, "Cohort case\nindex", fontsize=7)
    arrow(ax, 2.5, y + 0.45, 3.1, y + 0.45, "case link record")
    box(ax, 3.1, y, 2.3, 0.9, "Modality\nintegrator", fontsize=7)
    box(ax, 3.1, 1.5, 2.3, 0.9, "Existing pathology\npipeline", external=True, fontsize=7)
    arrow(ax, 4.25, 2.4, 4.25, 2.8, "localization\npointer", (0.55, 0))
    arrow(ax, 5.4, y + 0.45, 6.0, y + 0.45, "input list JSON")
    box(ax, 6.0, y, 2.0, 0.9, "Risk scorer", fontsize=7)
    arrow(ax, 8.0, y + 0.45, 8.6, y + 0.45, "score / block")
    box(ax, 8.6, y, 2.1, 0.9, "Review package", fontsize=7)
    arrow(ax, 10.7, y + 0.45, 11.3, y + 0.45, "helper package")
    box(ax, 11.3, y, 2.1, 0.9, "PathPresenter", external=True, fontsize=7)
    arrow(ax, 13.4, y + 0.45, 14.0, y + 0.45, "case view")
    box(ax, 14.0, y, 1.7, 0.9, "Pathologist", external=True, fontsize=7)

    legend = Rectangle((0.3, 0.2), 6.5, 1.0, linewidth=1, edgecolor="#718096", facecolor="#fff")
    ax.add_patch(legend)
    ax.text(
        0.45,
        0.65,
        "Legend: solid = we build; dashed = external; arrow label = data form at that point",
        fontsize=8,
    )

    fig.tight_layout()
    path = OUT / "D0_dataflow_diagram.png"
    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    return path


if __name__ == "__main__":
    print(make_block())
    print(make_dataflow())
