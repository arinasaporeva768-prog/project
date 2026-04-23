# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math
import textwrap

OUT_DIR = Path(r"C:\Users\evgen\Downloads\project1\langflow_copilot_seed")
PNG_PATH = OUT_DIR / "risk_matrix_template_style.png"
JPG_PATH = OUT_DIR / "risk_matrix_template_style.jpg"

W, H = 1600, 900
BG = "#ffffff"
BORDER = "#d9d9e3"
PURPLE = "#7b2bd3"
PURPLE_DARK = "#6a1fc4"
PURPLE_MID = "#9a4be6"
PURPLE_LIGHT = "#cfa8f2"
TEXT = "#111111"
MUTED = "#666666"
WHITE = "#ffffff"
CARD_BORDER = "#e7e7ef"
SHADOW = "#00000020"


def load_font(size: int, bold: bool = False):
    candidates = []
    if bold:
        candidates = [
            r"C:\Windows\Fonts\arialbd.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\calibrib.ttf",
        ]
    else:
        candidates = [
            r"C:\Windows\Fonts\arial.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\calibri.ttf",
        ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


FONT_TITLE = load_font(28, True)
FONT_LABEL = load_font(16, True)
FONT_TEXT = load_font(15, False)
FONT_TEXT_B = load_font(15, True)
FONT_NUM = load_font(22, True)
FONT_AXIS = load_font(15, True)
FONT_SMALL = load_font(11, False)


def rounded_rect(draw, box, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


def fit_text(draw, box, text, font, fill=TEXT, align="left", valign="middle", padding=12, spacing=3):
    x1, y1, x2, y2 = box
    width = x2 - x1 - padding * 2
    # simple wrap by words using current font
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        cur = words[0]
        for w in words[1:]:
            trial = cur + " " + w
            bb = draw.textbbox((0, 0), trial, font=font)
            if bb[2] - bb[0] <= width:
                cur = trial
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
    wrapped = "\n".join(lines)
    bb = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=spacing, align=align)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    tx = x1 + padding if align == "left" else x1 + ((x2 - x1 - tw) / 2)
    ty = y1 + ((y2 - y1 - th) / 2) if valign == "middle" else y1 + padding
    draw.multiline_text((tx, ty), wrapped, font=font, fill=fill, spacing=spacing, align=align)


def card(img, draw, box, radius=24):
    # shadow
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sx1, sy1, sx2, sy2 = box
    sd.rounded_rectangle((sx1+2, sy1+4, sx2+2, sy2+4), radius=radius, fill=(0, 0, 0, 28))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    img.alpha_composite(shadow)
    rounded_rect(draw, box, radius, WHITE, outline=CARD_BORDER, width=2)


def circle_num(draw, center, r, num):
    x, y = center
    draw.ellipse((x-r, y-r, x+r, y+r), fill=WHITE, outline=PURPLE, width=3)
    bb = draw.textbbox((0, 0), str(num), font=FONT_LABEL)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text((x - tw/2, y - th/2 - 1), str(num), font=FONT_LABEL, fill=PURPLE)


def arrow_circle(draw, center, r=20):
    x, y = center
    draw.ellipse((x-r, y-r, x+r, y+r), fill=PURPLE, outline=PURPLE, width=1)
    pts = [(x-5, y-8), (x+4, y), (x-5, y+8)]
    draw.line(pts, fill=WHITE, width=3)


def make_gradient_square(size, color1, color2):
    sq = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = sq.load()
    c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
    c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
    for y in range(size):
        for x in range(size):
            t = (x + y) / (2 * size)
            rgb = tuple(int(c1[k] * (1-t) + c2[k] * t) for k in range(3))
            px[x, y] = (*rgb, 255)
    return sq


def main():
    base = Image.new("RGBA", (W, H), BG)
    draw = ImageDraw.Draw(base)

    # outer border
    draw.rectangle((30, 20, W-30, H-20), outline=BORDER, width=2)
    draw.text((55, 45), "МАТРИЦА РИСКОВ", font=FONT_TITLE, fill=TEXT)

    # left matrix
    mx, my = 130, 150
    cell, gap = 165, 18
    labels_x = ["Низкая", "Средняя", "Высокая"]
    labels_y = ["Низкая", "Средняя", "Высокая"]

    # axis labels
    draw.text((85, 405), "Вероятность", font=FONT_AXIS, fill=MUTED, anchor="mm")
    # vertical-ish by char stacking is ugly; use rotate image
    tmp = Image.new("RGBA", (180, 40), (0, 0, 0, 0))
    td = ImageDraw.Draw(tmp)
    td.text((0, 0), "Вероятность", font=load_font(17, True), fill=MUTED)
    tmp = tmp.rotate(90, expand=True)
    base.alpha_composite(tmp, (45, 300))

    draw.text((335, 760), "Значимость", font=FONT_AXIS, fill=MUTED, anchor="mm")

    # grid cells
    color_map = {
        (0, 0): (PURPLE_LIGHT, "#ddc3f7"),
        (1, 0): ("#c49bea", "#b686e4"),
        (2, 0): ("#b67be7", "#a767dd"),
        (0, 1): ("#c39aea", "#b88ce2"),
        (1, 1): ("#b684e3", "#a96edb"),
        (2, 1): ("#a64bdf", "#8d36d1"),
        (0, 2): ("#b07adf", "#a96cd8"),
        (1, 2): ("#9b3fe0", "#832fd2"),
        (2, 2): ("#8e29d7", "#741fc8"),
    }

    # Risks placed like template style but with our risks
    placements = {
        1: (0, 0),  # low/low
        2: (0, 1),  # low significance / medium probability? using x,y from bottom-left
        3: (1, 0),
        4: (1, 2),
        5: (1, 1),
        6: (2, 0),
        7: (2, 1),
    }

    # Draw from top-left visual coordinates; our logical coordinates x 0..2 low->high, y 0..2 low->high
    for gx in range(3):
        for gy in range(3):
            vx = mx + gx * (cell + gap)
            vy = my + (2 - gy) * (cell + gap)
            g = make_gradient_square(cell, color_map[(gx, gy)][0], color_map[(gx, gy)][1])
            mask = Image.new("L", (cell, cell), 0)
            md = ImageDraw.Draw(mask)
            md.rounded_rectangle((0, 0, cell, cell), radius=28, fill=255)
            base.paste(g, (vx, vy), mask)

    # axis tick labels
    for i, lab in enumerate(labels_x):
        x = mx + i * (cell + gap) + cell / 2
        draw.text((x, 710), lab, font=FONT_TEXT_B, fill=MUTED, anchor="mm")
    for i, lab in enumerate(labels_y):
        y = my + (2 - i) * (cell + gap) + cell / 2
        # rotated labels on left
        tmp = Image.new("RGBA", (120, 30), (0, 0, 0, 0))
        td = ImageDraw.Draw(tmp)
        td.text((0, 0), lab, font=FONT_TEXT_B, fill=MUTED)
        tmp = tmp.rotate(90, expand=True)
        base.alpha_composite(tmp, (92, int(y - tmp.size[1] / 2)))

    # numbered circles
    risk_summaries = {
        1: ("R1/R13", "Несанкционированные действия и привилегированный админ"),
        2: ("R2/R6", "Утечка данных и межпользовательская утечка"),
        3: ("R3/R12", "Инъекции и лишние детали в explanation"),
        4: ("R4/R7", "Ошибки edit-перевода и невалидный workflow"),
        5: ("R5/R8", "Обход политик и approval bypass"),
        6: ("R9/R10", "Ресурсы и audit trail"),
        7: ("R11/R14/R15", "Supply chain, side effects, ложная уверенность"),
    }
    for n, (gx, gy) in placements.items():
        vx = mx + gx * (cell + gap)
        vy = my + (2 - gy) * (cell + gap)
        # vary location a bit like template
        offsets = {
            1: (38, 34), 2: (72, 72), 3: (110, 110), 4: (78, 62), 5: (96, 86), 6: (118, 128), 7: (125, 120)
        }
        ox, oy = offsets[n]
        circle_num(draw, (vx + ox, vy + oy), 24, n)

    # right headers
    rounded_rect(draw, (760, 85, 1040, 135), 22, PURPLE)
    rounded_rect(draw, (1130, 85, 1435, 135), 22, PURPLE)
    fit_text(draw, (760, 85, 1040, 135), "Риск", FONT_LABEL, fill=WHITE, align="center")
    fit_text(draw, (1130, 85, 1435, 135), "Митигация", FONT_LABEL, fill=WHITE, align="center")

    rows = [
        ("1", "Несанкционированные действия через Copilot", "RBAC, allow-list действий, approval перед apply/run, scoped tokens"),
        ("2", "Утечка чувствительных данных", "Redaction, masking секретов, PII scanning, role-based explanation"),
        ("3", "Prompt / workflow / KB injection", "Trusted KB, sanitization, isolated tools, prompt hardening"),
        ("4", "Ошибки при переводе JSON -> IR -> JSON", "Round-trip tests, strict schema, reject unknown fields, diff preview"),
        ("5", "Обход политик и approval", "Policy checks до/после edit, hash-bound approval, revalidation before apply"),
        ("6", "Ресурсные сбои и проблемы аудита", "Limits, timeouts, quotas, immutable audit log, dual logging"),
        ("7", "Supply chain, side effects, ложная уверенность", "Approved registry, sandboxing, validator gate, human approval"),
    ]

    row_y = 120
    for idx, risk, mitig in rows:
        y1 = row_y
        y2 = y1 + 78
        card(base, draw, (690, y1, 1500, y2), radius=32)
        circle_num(draw, (735, y1 + 39), 18, idx)
        fit_text(draw, (765, y1 + 8, 1030, y2 - 8), risk, FONT_TEXT, align="left")
        arrow_circle(draw, (1085, y1 + 39), 18)
        fit_text(draw, (1130, y1 + 8, 1470, y2 - 8), mitig, FONT_TEXT, align="left")
        row_y += 92

    # bottom line + source
    draw.line((55, 845, 1490, 845), fill=PURPLE_LIGHT, width=2)
    draw.text((58, 855), "Источник: внутренняя оценка рисков AI Copilot, NIST AI RMF 1.0", font=FONT_SMALL, fill=MUTED)
    draw.text((1460, 835), "1", font=load_font(22, True), fill=PURPLE)

    base.convert("RGB").save(PNG_PATH, "PNG")
    base.convert("RGB").save(JPG_PATH, "JPEG", quality=95, optimize=True)
    print(PNG_PATH)
    print(JPG_PATH)


if __name__ == "__main__":
    main()
