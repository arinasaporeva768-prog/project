# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
import math


OUT_DIR = Path(r"C:\Users\evgen\Downloads\project1\langflow_copilot_seed")
PNG_PATH = OUT_DIR / "architecture_high_level.png"
JPG_PATH = OUT_DIR / "architecture_high_level.jpg"


def load_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\ARIAL.TTF",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


FONT_TITLE = load_font(36)
FONT_SUB = load_font(27)
FONT_TEXT = load_font(23)
FONT_SMALL = load_font(19)

W, H = 2200, 1400
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


def rr(draw, xy, fill, outline=NAVY, width=3, radius=22):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def center_text(draw, box, text, font, fill=DARK):
    x1, y1, x2, y2 = box
    bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=6, align="center")
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    tx = x1 + (x2 - x1 - tw) / 2
    ty = y1 + (y2 - y1 - th) / 2
    draw.multiline_text((tx, ty), text, font=font, fill=fill, spacing=6, align="center")


def wrapped_text(draw, box, text, font, fill=DARK, width_chars=26, top_pad=18):
    x1, y1, _, _ = box
    lines = []
    for part in text.split("\n"):
        wrapped = textwrap.wrap(part, width=width_chars) or [""]
        lines.extend(wrapped)
    draw.multiline_text((x1 + 20, y1 + top_pad), "\n".join(lines), font=font, fill=fill, spacing=8)


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

    center_text(
        draw,
        (0, 28, W, 92),
        "AI Copilot для Langflow 1.9 — верхнеуровневая архитектура",
        FONT_TITLE,
        fill=NAVY,
    )

    user_box = (80, 140, 420, 250)
    ux_box = (520, 140, 900, 250)
    orch_box = (1020, 125, 1500, 265)

    rr(draw, user_box, BLUE)
    rr(draw, ux_box, BLUE)
    rr(draw, orch_box, ORANGE)

    center_text(draw, user_box, "Бизнес-пользователь", FONT_SUB)
    center_text(draw, ux_box, "Copilot UX в Langflow", FONT_SUB)
    center_text(draw, orch_box, "AI Copilot Orchestrator", FONT_SUB)

    arrow(draw, (420, 195), (520, 195))
    arrow(draw, (900, 195), (1020, 195))

    ctx_group = (70, 360, 730, 1280)
    rr(draw, ctx_group, GRAY, outline=LINE, width=2, radius=28)
    center_text(draw, (70, 374, 730, 424), "Контекст и управление", FONT_SUB, fill=NAVY)

    ctx1 = (110, 450, 690, 610)
    ctx2 = (110, 650, 690, 830)
    ctx3 = (110, 870, 690, 1050)
    ctx4 = (110, 1090, 690, 1240)
    for box in (ctx1, ctx2, ctx3, ctx4):
        rr(draw, box, BLUE2, outline=LINE, width=2, radius=20)

    wrapped_text(draw, ctx1, "RAG слой\n- каталог компонентов\n- банковские политики\n- шаблоны workflow", FONT_TEXT)
    wrapped_text(draw, ctx2, "Состояние и версии\n- история диалога\n- снимок workflow\n- diff изменений", FONT_TEXT)
    wrapped_text(draw, ctx3, "Policy Engine\n- allow-list компонентов и моделей\n- approval для risky actions", FONT_TEXT)
    wrapped_text(draw, ctx4, "Audit Trail\n- события\n- решения\n- версии\n- trace", FONT_TEXT)

    skills_group = (790, 360, 1440, 1280)
    rr(draw, skills_group, GRAY, outline=LINE, width=2, radius=28)
    center_text(draw, (790, 374, 1440, 424), "Набор skills", FONT_SUB, fill=NAVY)

    skill_boxes = [
        ((840, 470, 1390, 570), "Requirement Intake"),
        ((840, 620, 1390, 720), "Workflow Planner"),
        ((840, 770, 1390, 870), "Graph Builder / Editor"),
        ((840, 920, 1390, 1020), "Validator / Repair"),
        ((840, 1070, 1390, 1170), "Explainer"),
    ]
    for box, label in skill_boxes:
        rr(draw, box, GREEN, outline=LINE, width=2, radius=20)
        center_text(draw, box, label, FONT_TEXT)

    exec_group = (1510, 360, 2120, 1280)
    rr(draw, exec_group, GRAY, outline=LINE, width=2, radius=28)
    center_text(draw, (1510, 374, 2120, 424), "Исполнительный слой Langflow", FONT_SUB, fill=NAVY)

    ex1 = (1570, 500, 2060, 620)
    ex2 = (1570, 700, 2060, 820)
    ex3 = (1570, 900, 2060, 1020)
    rr(draw, ex1, ORANGE, outline=LINE, width=2, radius=20)
    rr(draw, ex2, BLUE2, outline=LINE, width=2, radius=20)
    rr(draw, ex3, BLUE2, outline=LINE, width=2, radius=20)
    center_text(draw, ex1, "Workflow Canvas / Flow Store", FONT_TEXT)
    center_text(draw, ex2, "Разрешенные компоненты", FONT_TEXT)
    center_text(draw, ex3, "Разрешенные модели", FONT_TEXT)

    # Orchestrator -> three areas
    draw.line((1150, 265, 1150, 320, 400, 320, 400, 360), fill=NAVY, width=5)
    arrow(draw, (400, 320), (400, 360))

    draw.line((1260, 265, 1260, 360), fill=NAVY, width=5)
    arrow(draw, (1260, 330), (1260, 360))

    draw.line((1370, 265, 1370, 320, 1815, 320, 1815, 360), fill=NAVY, width=5)
    arrow(draw, (1815, 320), (1815, 360))

    # Context -> skills
    for y in (530, 690, 960):
        draw.line((690, y, 840, y), fill=MID, width=3)
        arrow(draw, (810, y), (840, y), fill=MID, width=3, head=10)

    # Skills -> execution
    draw.line((1390, 820, 1570, 560), fill=MID, width=3)
    arrow(draw, (1540, 560), (1570, 560), fill=MID, width=3, head=10)

    draw.line((1390, 970, 1570, 560), fill=MID, width=3)
    arrow(draw, (1540, 560), (1570, 560), fill=MID, width=3, head=10)

    # Explain / validate / audit back to UX
    draw.line((1390, 1120, 1460, 1120, 1460, 190, 900, 190), fill=MID, width=3)
    arrow(draw, (930, 190), (900, 190), fill=MID, width=3, head=10)

    center_text(
        draw,
        (120, 1320, 2080, 1380),
        "Схема показывает архитектурные блоки без детального перечисления технических I/O-компонентов.",
        FONT_SMALL,
        fill=MID,
    )

    img.save(PNG_PATH, "PNG")
    img.save(JPG_PATH, "JPEG", quality=95, optimize=True)
    print(PNG_PATH)
    print(JPG_PATH)


if __name__ == "__main__":
    main()
