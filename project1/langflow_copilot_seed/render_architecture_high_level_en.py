# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math


OUT_DIR = Path(r"C:\Users\evgen\Downloads\project1\langflow_copilot_seed")
PNG_PATH = OUT_DIR / "architecture_high_level.png"
JPG_PATH = OUT_DIR / "architecture_high_level.jpg"

W, H = 2400, 1350
BG = "white"

NAVY = "#1f3a5f"
BLUE = "#dceeff"
BLUE2 = "#eef6ff"
GREEN = "#dff6e3"
GRAY = "#f3f5f7"
ORANGE = "#fff2db"
DARK = "#1e293b"
MID = "#64748b"
LINE = "#9aa7b8"


def load_font(size: int):
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def rr(draw, xy, fill, outline=NAVY, width=3, radius=22):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def fit_text(draw, box, text, max_size, min_size=14, align="center", fill=DARK, valign="middle", padding=18, line_spacing=6):
    x1, y1, x2, y2 = box
    width = x2 - x1 - padding * 2
    height = y2 - y1 - padding * 2
    paragraphs = text.split("\n")

    for size in range(max_size, min_size - 1, -1):
        font = load_font(size)
        lines = []
        for paragraph in paragraphs:
            words = paragraph.split()
            if not words:
                lines.append("")
                continue
            current = words[0]
            for word in words[1:]:
                trial = current + " " + word
                bbox = draw.textbbox((0, 0), trial, font=font)
                if bbox[2] - bbox[0] <= width:
                    current = trial
                else:
                    lines.append(current)
                    current = word
            lines.append(current)
        wrapped = "\n".join(lines)
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=line_spacing, align=align)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        if tw <= width and th <= height:
            if align == "center":
                tx = x1 + (x2 - x1 - tw) / 2
            else:
                tx = x1 + padding
            if valign == "middle":
                ty = y1 + (y2 - y1 - th) / 2
            else:
                ty = y1 + padding
            draw.multiline_text((tx, ty), wrapped, font=font, fill=fill, spacing=line_spacing, align=align)
            return
    font = load_font(min_size)
    draw.multiline_text((x1 + padding, y1 + padding), text, font=font, fill=fill, spacing=line_spacing, align=align)


def arrow(draw, p1, p2, fill=NAVY, width=5, head=14):
    x1, y1 = p1
    x2, y2 = p2
    draw.line((x1, y1, x2, y2), fill=fill, width=width)
    ang = math.atan2(y2 - y1, x2 - x1)
    a1 = ang + math.pi * 0.85
    a2 = ang - math.pi * 0.85
    p3 = (x2 + head * math.cos(a1), y2 + head * math.sin(a1))
    p4 = (x2 + head * math.cos(a2), y2 + head * math.sin(a2))
    draw.polygon([p2, p3, p4], fill=fill)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    fit_text(draw, (300, 18, 2100, 80), "AI Copilot for Langflow 1.9 - High-Level Architecture", 38, fill=NAVY)

    # Top row
    user_box = (70, 105, 340, 190)
    ux_box = (420, 105, 760, 190)
    orch_box = (860, 85, 1360, 210)

    rr(draw, user_box, BLUE)
    rr(draw, ux_box, BLUE)
    rr(draw, orch_box, ORANGE)
    fit_text(draw, user_box, "Business User", 22)
    fit_text(draw, ux_box, "Copilot UX in Langflow", 22)
    fit_text(draw, orch_box, "AI Copilot Orchestrator", 28)
    arrow(draw, (340, 147), (420, 147))
    arrow(draw, (760, 147), (860, 147))

    # Left translation lane
    trans_group = (50, 290, 600, 1230)
    rr(draw, trans_group, GRAY, outline=LINE, width=2, radius=24)
    fit_text(draw, (70, 305, 580, 350), "Edit Translation Layer", 28, fill=NAVY)

    edit_json = (95, 390, 555, 470)
    in_adapter = (95, 520, 555, 610)
    ir_box = (95, 670, 555, 790)
    out_adapter = (95, 860, 555, 950)
    out_json = (95, 1000, 555, 1090)

    for box in (edit_json, in_adapter, ir_box, out_adapter, out_json):
        rr(draw, box, BLUE2, outline=LINE, width=2, radius=18)

    fit_text(draw, edit_json, "Existing Langflow Workflow JSON\n(edit mode input)", 22)
    fit_text(draw, in_adapter, "Input Adapter\nLangflow JSON -> Internal Representation", 22)
    fit_text(draw, ir_box, "Canonical Workflow IR\ncompact graph JSON preserving structure", 24)
    fit_text(draw, out_adapter, "Output Adapter\nInternal Representation -> Langflow JSON", 22)
    fit_text(draw, out_json, "Langflow Workflow JSON\n(output envelope)", 22)

    arrow(draw, (325, 470), (325, 520), fill=MID, width=3, head=10)
    arrow(draw, (325, 610), (325, 670), fill=MID, width=3, head=10)
    arrow(draw, (325, 790), (325, 860), fill=MID, width=3, head=10)
    arrow(draw, (325, 950), (325, 1000), fill=MID, width=3, head=10)

    # Middle top: internal representation emphasis
    ir_hub = (700, 280, 1260, 410)
    rr(draw, ir_hub, ORANGE, outline=NAVY, width=3, radius=22)
    fit_text(draw, ir_hub, "Internal Working Representation\nused by planning, editing, validation, and explanation", 28)

    # Middle lower: skills
    skills_group = (680, 470, 1280, 1230)
    rr(draw, skills_group, GRAY, outline=LINE, width=2, radius=24)
    fit_text(draw, (700, 485, 1260, 530), "Skill Layer", 28, fill=NAVY)

    skill_boxes = [
        ((740, 560, 1220, 640), "Requirement Intake"),
        ((740, 675, 1220, 755), "Workflow Planner"),
        ((740, 790, 1220, 870), "Graph Builder / Editor"),
        ((740, 905, 1220, 985), "Validator / Repair"),
        ((740, 1020, 1220, 1100), "Explainer"),
    ]
    for box, text in skill_boxes:
        rr(draw, box, GREEN, outline=LINE, width=2, radius=18)
        fit_text(draw, box, text, 23)

    # Right upper: context and governance
    ctx_group = (1370, 280, 1830, 830)
    gov_group = (1870, 280, 2330, 830)

    rr(draw, ctx_group, GRAY, outline=LINE, width=2, radius=24)
    rr(draw, gov_group, GRAY, outline=LINE, width=2, radius=24)

    fit_text(draw, (1390, 295, 1810, 340), "Context Layer", 28, fill=NAVY)
    fit_text(draw, (1890, 295, 2310, 340), "Governance Layer", 28, fill=NAVY)

    rag_box = (1420, 380, 1780, 520)
    state_box = (1420, 560, 1780, 730)
    policy_box = (1920, 380, 2280, 540)
    audit_box = (1920, 580, 2280, 760)

    for box in (rag_box, state_box, policy_box, audit_box):
        rr(draw, box, BLUE2, outline=LINE, width=2, radius=18)

    fit_text(draw, rag_box, "RAG\ncomponent catalog\nbank policies\nworkflow templates", 22, align="left", valign="top")
    fit_text(draw, state_box, "State and Versioning\ndialog history\nworkflow snapshot\nchange diff", 22, align="left", valign="top")
    fit_text(draw, policy_box, "Policy Engine\nallow-lists\napproval for risky actions", 22, align="left", valign="top")
    fit_text(draw, audit_box, "Audit Trail\nevents\ndecisions\nversions\ntrace", 22, align="left", valign="top")

    # Right lower: Langflow execution
    exec_group = (1560, 900, 2330, 1230)
    rr(draw, exec_group, GRAY, outline=LINE, width=2, radius=24)
    fit_text(draw, (1580, 915, 2310, 960), "Langflow Execution Layer", 28, fill=NAVY)

    store_box = (1610, 995, 1830, 1105)
    comp_box = (1880, 995, 2280, 1055)
    model_box = (1880, 1080, 2280, 1140)
    rr(draw, store_box, ORANGE, outline=LINE, width=2, radius=18)
    rr(draw, comp_box, BLUE2, outline=LINE, width=2, radius=18)
    rr(draw, model_box, BLUE2, outline=LINE, width=2, radius=18)
    fit_text(draw, store_box, "Langflow Canvas / Flow Store", 22)
    fit_text(draw, comp_box, "Approved Components", 20)
    fit_text(draw, model_box, "Approved Models", 20)

    # Orchestrator feeds layers
    draw.line((1040, 210, 1040, 250, 980, 250, 980, 280), fill=NAVY, width=5)
    arrow(draw, (980, 250), (980, 280))

    draw.line((1160, 210, 1160, 250, 1580, 250, 1580, 280), fill=NAVY, width=5)
    arrow(draw, (1580, 250), (1580, 280))

    draw.line((1240, 210, 1240, 250, 2100, 250, 2100, 280), fill=NAVY, width=5)
    arrow(draw, (2100, 250), (2100, 280))

    # IR flows
    draw.line((555, 730, 700, 730, 700, 345), fill=MID, width=3)
    arrow(draw, (700, 375), (700, 345), fill=MID, width=3, head=10)

    draw.line((1260, 345, 1360, 345, 1360, 830, 1220, 830), fill=MID, width=3)
    arrow(draw, (1250, 830), (1220, 830), fill=MID, width=3, head=10)

    draw.line((1260, 345, 1360, 345, 1360, 945, 1220, 945), fill=MID, width=3)
    arrow(draw, (1250, 945), (1220, 945), fill=MID, width=3, head=10)

    draw.line((1260, 345, 1360, 345, 1360, 1060, 1220, 1060), fill=MID, width=3)
    arrow(draw, (1250, 1060), (1220, 1060), fill=MID, width=3, head=10)

    # Context/governance to skills
    draw.line((1780, 450, 1860, 450, 1860, 600, 1220, 600), fill=MID, width=3)
    arrow(draw, (1250, 600), (1220, 600), fill=MID, width=3, head=10)

    draw.line((1780, 640, 1840, 640, 1840, 715, 1220, 715), fill=MID, width=3)
    arrow(draw, (1250, 715), (1220, 715), fill=MID, width=3, head=10)

    draw.line((1920, 460, 1860, 460, 1860, 945, 1220, 945), fill=MID, width=3)
    arrow(draw, (1250, 945), (1220, 945), fill=MID, width=3, head=10)

    # Skills to output adapter
    draw.line((1220, 830, 1400, 830, 1400, 905, 555, 905), fill=MID, width=3)
    arrow(draw, (585, 905), (555, 905), fill=MID, width=3, head=10)

    draw.line((1220, 945, 1500, 945, 1500, 915, 555, 915), fill=MID, width=3)
    arrow(draw, (585, 915), (555, 915), fill=MID, width=3, head=10)

    # Output JSON to store
    draw.line((555, 1045, 1610, 1045), fill=MID, width=3)
    arrow(draw, (1580, 1045), (1610, 1045), fill=MID, width=3, head=10)

    # Store to approved comps/models
    draw.line((1830, 1045, 1880, 1025), fill=MID, width=3)
    arrow(draw, (1850, 1035), (1880, 1025), fill=MID, width=3, head=10)
    draw.line((1830, 1060, 1880, 1110), fill=MID, width=3)
    arrow(draw, (1850, 1085), (1880, 1110), fill=MID, width=3, head=10)

    # Explain/validate/audit back to UX
    draw.line((1220, 1060, 1320, 1060, 1320, 160, 760, 160), fill=MID, width=3)
    arrow(draw, (790, 160), (760, 160), fill=MID, width=3, head=10)

    draw.line((2280, 670, 2360, 670, 2360, 140, 760, 140), fill=MID, width=3)
    arrow(draw, (790, 140), (760, 140), fill=MID, width=3, head=10)

    fit_text(
        draw,
        (150, 1260, 2250, 1315),
        "Edit mode uses a dedicated translation path: Langflow JSON is converted into a compact internal representation, updated there, and converted back into Langflow JSON on output.",
        18,
        fill=MID,
    )

    img.save(PNG_PATH, "PNG")
    img.save(JPG_PATH, "JPEG", quality=95, optimize=True)
    print(PNG_PATH)
    print(JPG_PATH)


if __name__ == "__main__":
    main()
