# -*- coding: utf-8 -*-
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


OUT_DIR = Path(r"C:\Users\evgen\Downloads\project1\langflow_copilot_seed")
PNG_PATH = OUT_DIR / "risk_matrix_inherent.png"
JPG_PATH = OUT_DIR / "risk_matrix_inherent.jpg"

W, H = 2500, 1600
MARGIN = 60

BG = "white"
DARK = "#1e293b"
MUTED = "#64748b"
GRID = "#cbd5e1"
NAVY = "#1f3a5f"
LOW = "#dcfce7"
MED = "#fef3c7"
HIGH = "#fed7aa"
CRIT = "#fecaca"
HEADER = "#eff6ff"


def load_font(size: int):
    candidates = [
        r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\ARIAL.TTF",
        r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\calibri.ttf",
        r"C:\Windows\Fonts\tahoma.ttf",
    ]
    for c in candidates:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


FONT_TITLE = load_font(34)
FONT_SUB = load_font(22)
FONT_TEXT = load_font(20)
FONT_SMALL = load_font(17)


def fit_text(draw, box, text, max_size, min_size=12, align="left", fill=DARK, valign="top", padding=12, spacing=4):
    x1, y1, x2, y2 = box
    width = x2 - x1 - padding * 2
    height = y2 - y1 - padding * 2

    for size in range(max_size, min_size - 1, -1):
        font = load_font(size)
        lines = []
        for para in text.split("\n"):
            words = para.split()
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
        bbox = draw.multiline_textbbox((0, 0), wrapped, font=font, spacing=spacing, align=align)
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
            draw.multiline_text((tx, ty), wrapped, font=font, fill=fill, spacing=spacing, align=align)
            return
    draw.multiline_text((x1 + padding, y1 + padding), text, font=load_font(min_size), fill=fill, spacing=spacing, align=align)


def band(score: int):
    if score >= 16:
        return "Критический", CRIT
    if score >= 12:
        return "Высокий", HIGH
    if score >= 6:
        return "Средний", MED
    return "Низкий", LOW


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    fit_text(draw, (MARGIN, 20, W - MARGIN, 70), "Матрица рисков для AI Copilot в Langflow", 34, align="center", fill=NAVY, valign="middle")
    fit_text(draw, (MARGIN, 72, W - MARGIN, 112), "Методология: NIST AI RMF 1.0 | Шкала: 5x5 | Балл риска = Вероятность x Влияние", 20, align="center", fill=MUTED, valign="middle")

    matrix_left = 150
    matrix_top = 180
    cell = 180
    header_h = 70
    axis_w = 95

    for c in range(5):
        x1 = matrix_left + axis_w + c * cell
        x2 = x1 + cell
        draw.rectangle((x1, matrix_top, x2, matrix_top + header_h), fill=HEADER, outline=GRID, width=2)
        fit_text(draw, (x1, matrix_top, x2, matrix_top + header_h), str(c + 1), 24, align="center", valign="middle", fill=NAVY)

    for r in range(5):
        y1 = matrix_top + header_h + r * cell
        y2 = y1 + cell
        impact = 5 - r
        draw.rectangle((matrix_left, y1, matrix_left + axis_w, y2), fill=HEADER, outline=GRID, width=2)
        fit_text(draw, (matrix_left, y1, matrix_left + axis_w, y2), str(impact), 24, align="center", valign="middle", fill=NAVY)

        for c in range(5):
            likelihood = c + 1
            score = impact * likelihood
            _, fill = band(score)
            x1 = matrix_left + axis_w + c * cell
            x2 = x1 + cell
            draw.rectangle((x1, y1, x2, y2), fill=fill, outline=GRID, width=2)

    fit_text(draw, (matrix_left + axis_w, matrix_top - 55, matrix_left + axis_w + 5 * cell, matrix_top - 10), "Вероятность", 24, align="center", valign="middle", fill=NAVY)
    fit_text(draw, (25, matrix_top + header_h, 130, matrix_top + header_h + 5 * cell), "Влияние", 24, align="center", valign="middle", fill=NAVY)

    placements = {
        (4, 5): ["R1", "R2"],
        (3, 5): ["R5", "R6", "R8", "R11", "R14"],
        (2, 5): ["R13"],
        (4, 4): ["R3", "R4", "R7"],
        (3, 4): ["R10", "R12", "R15"],
        (4, 3): ["R9"],
    }

    for (likelihood, impact), ids in placements.items():
        c = likelihood - 1
        r = 5 - impact
        x1 = matrix_left + axis_w + c * cell
        y1 = matrix_top + header_h + r * cell
        x2 = x1 + cell
        y2 = y1 + cell
        fit_text(draw, (x1 + 8, y1 + 8, x2 - 8, y2 - 8), "\n".join(ids), 24, min_size=14, align="center", valign="middle", fill=DARK)

    right_left = 1270
    fit_text(draw, (right_left, 180, W - 70, 220), "Легенда", 28, align="left", fill=NAVY, valign="middle")

    legend_items = [
        ("Критический", "16-25", CRIT),
        ("Высокий", "12-15", HIGH),
        ("Средний", "6-10", MED),
        ("Низкий", "1-5", LOW),
    ]
    y = 235
    for label, rng, color in legend_items:
        draw.rectangle((right_left, y, right_left + 42, y + 42), fill=color, outline=GRID, width=2)
        fit_text(draw, (right_left + 58, y, right_left + 280, y + 42), f"{label} ({rng})", 20, align="left", valign="middle")
        y += 58

    fit_text(draw, (right_left, 485, W - 70, 525), "Расшифровка рисков", 28, align="left", fill=NAVY, valign="middle")

    legend_lines = [
        "R1  Несанкционированное выполнение действий через Copilot",
        "R2  Утечка чувствительных данных в промптах, объяснениях или логах",
        "R3  Prompt injection / workflow injection / KB injection",
        "R4  Семантическое искажение при переводе JSON -> IR -> JSON",
        "R5  Обход политик через неподдерживаемые поля или custom components",
        "R6  Утечка данных между пользователями или workflow",
        "R7  Галлюцинированный или структурно невалидный workflow",
        "R8  Обход approval или гонка между approval и apply",
        "R9  Истощение ресурсов или слишком большой граф / JSON payload",
        "R10 Неполный или изменяемый audit trail",
        "R11 Supply chain риск в моделях, коннекторах, шаблонах и компонентах",
        "R12 Слишком подробное объяснение раскрывает лишние детали исполнения",
        "R13 Злоупотребление привилегиями администратора при allow-lists или policies",
        "R14 Небезопасный коннектор или внешний side effect, добавленный Copilot",
        "R15 Некорректная валидация или объяснение создает ложную уверенность",
    ]

    y = 535
    line_h = 56
    for line in legend_lines:
        fit_text(draw, (right_left, y, W - 80, y + line_h), line, 18, min_size=14, align="left", valign="middle")
        y += line_h

    fit_text(
        draw,
        (MARGIN, H - 72, W - MARGIN, H - 20),
        "Наибольшая концентрация исходного риска находится в зонах несанкционированных действий, утечки чувствительных данных, инъекций в prompts/workflow/knowledge base, ошибок перевода в edit mode и небезопасных внешних side effects.",
        18,
        align="center",
        fill=MUTED,
        valign="middle",
    )

    img.save(PNG_PATH, "PNG")
    img.save(JPG_PATH, "JPEG", quality=95, optimize=True)
    print(PNG_PATH)
    print(JPG_PATH)


if __name__ == "__main__":
    main()
