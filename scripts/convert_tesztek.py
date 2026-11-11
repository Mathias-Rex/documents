"""Convert the scanned Redmenta test PDFs to Markdown and clean PDFs.

Requires: pymupdf, numpy, rapidocr-onnxruntime.
Run from any directory: python scripts/convert_tesztek.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf
import numpy as np
from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "teacher" / "tesztek"
BACKUP = TESTS / "backup"


def make_ocr():
    # RapidOCR uses Shapely only for polygon area/perimeter. On locked-down
    # Windows installs its native DLL may be blocked; provide the same small
    # geometry operations as a pure-Python fallback.
    try:
        from rapidocr_onnxruntime import RapidOCR as _RapidOCR
        return _RapidOCR()
    except ImportError as exc:
        if "shapely" not in str(exc).lower() and "dll" not in str(exc).lower():
            raise
        import types
        shapely = types.ModuleType("shapely")
        geometry = types.ModuleType("shapely.geometry")

        class Polygon:
            def __init__(self, points):
                self.points = points

            @property
            def area(self):
                pts = self.points
                return abs(sum(pts[i][0] * pts[(i + 1) % len(pts)][1]
                               - pts[(i + 1) % len(pts)][0] * pts[i][1]
                               for i in range(len(pts))) / 2)

            @property
            def length(self):
                import math
                pts = self.points
                return sum(math.dist(pts[i], pts[(i + 1) % len(pts)])
                           for i in range(len(pts)))

        geometry.Polygon = Polygon
        shapely.geometry = geometry
        sys.modules["shapely"] = shapely
        sys.modules["shapely.geometry"] = geometry
        return RapidOCR()


def clean_lines(lines: list[str]) -> list[str]:
    cleaned = []
    for line in lines:
        line = re.sub(r"https?://\S+", "", line).strip()
        if not line or re.match(r"^(202\d\.|Redmenta\b|\d+/\d+$|OSSZES[IÍ]T[ŐO]|BEAD[AÁ]S)", line, re.I):
            continue
        if line in {"redmenta", "BV", "Kezdes", "Eredmenyek"}:
            continue
        cleaned.append(line)
    return cleaned


def ocr_pdf(path: Path, engine) -> list[str]:
    doc = pymupdf.open(path)
    pages = []
    for page in doc:
        pix = page.get_pixmap(matrix=pymupdf.Matrix(2, 2), alpha=False)
        result, _ = engine(np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n))
        lines = clean_lines([item[1] for item in (result or [])])
        pages.append("\n".join(lines))
    return pages


def to_markdown(title: str, pages: list[str]) -> str:
    out = [f"# {title}", "", "> Automatikus OCR-átirat. A forrás beszkennelt PDF, ezért az ékezeteket és a szöveget érdemes ellenőrizni.", ""]
    for number, page in enumerate(pages, 1):
        if not page.strip():
            continue
        out += [f"## Forrásoldal {number}", "", page.strip(), ""]
    return "\n".join(out).rstrip() + "\n"


def markdown_to_pdf(markdown: str, target: Path) -> None:
    """Render the two authored Markdown layouts with clear, separate cards."""
    regular_path = Path("C:/Windows/Fonts/arial.ttf")
    bold_path = Path("C:/Windows/Fonts/arialbd.ttf")
    regular_file = str(regular_path) if regular_path.exists() else None
    bold_file = str(bold_path) if bold_path.exists() else regular_file
    regular = pymupdf.Font(fontfile=regular_file) if regular_file else pymupdf.Font("helv")
    bold = pymupdf.Font(fontfile=bold_file) if bold_file else pymupdf.Font("hebo")
    is_answer = "megold" in target.name.lower()
    navy = (0.09, 0.17, 0.30)
    blue = (0.12, 0.39, 0.68)
    ink = (0.13, 0.17, 0.23)
    muted = (0.36, 0.42, 0.50)
    pale = (0.96, 0.975, 0.99)
    border = (0.83, 0.87, 0.92)

    def clean(text: str) -> str:
        text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
        return re.sub(r"`([^`]*)`", r"\1", text).strip()

    def wrap(text: str, font, size: float, max_width: float) -> list[str]:
        words, rows, current = text.split(), [], ""
        for word in words:
            trial = f"{current} {word}".strip()
            if current and font.text_length(trial, fontsize=size) > max_width:
                rows.append(current)
                current = word
            else:
                current = trial
        if current:
            rows.append(current)
        return rows or [""]

    lines = markdown.splitlines()
    title = next((clean(line.lstrip("# ")) for line in lines if line.startswith("# ")), "Feladatlap")
    blocks = []
    intro = []
    if is_answer:
        for line in lines:
            if not line.startswith("|"):
                if line.startswith("## "):
                    blocks.append(("section", clean(line[3:])))
                elif line.startswith("- "):
                    blocks.append(("note", clean(line[2:])))
                elif line.startswith("> ") or (line.strip() and not line.startswith("#")):
                    intro.append(clean(line.lstrip("> ")))
                continue
            cells = [clean(c.strip()) for c in line.strip("|").split("|")]
            if not cells or cells[0] == "#" or all(set(c) <= {"-", ":", " "} for c in cells):
                continue
            if cells[0].isdigit() and len(cells) >= 2:
                blocks.append(("answer", (cells[0], cells[1], cells[2] if len(cells) > 2 else "")))
    else:
        current_title, current_items = None, []
        for line in lines:
            if line.startswith("### "):
                if current_title is not None:
                    blocks.append(("question", (current_title, current_items)))
                current_title, current_items = clean(line[4:]), []
                continue
            if current_title is None:
                if line.startswith("> "):
                    intro.append(clean(line[2:]))
                continue
            line = line.strip()
            if not line:
                continue
            choice = re.match(r"^-\s+\[ \]\s+(.*)$", line)
            tf = re.match(r"^-\s+(.*?)\s+—\s+\*\*Igaz / Hamis\*\*$", line)
            bullet = re.match(r"^-\s+(.*)$", line)
            if choice:
                current_items.append(("choice", clean(choice.group(1))))
            elif tf:
                current_items.append(("truth", clean(tf.group(1))))
            elif bullet:
                current_items.append(("bullet", clean(bullet.group(1))))
            else:
                current_items.append(("text", clean(line)))
        if current_title is not None:
            blocks.append(("question", (current_title, current_items)))

    doc = pymupdf.open()
    page_number = 0
    page = None
    y = 0
    margin = 43
    page_bottom = 785
    content_width = 595 - 2 * margin

    def new_page():
        nonlocal page, y, page_number
        page_number += 1
        page = doc.new_page(width=595, height=842)
        page.draw_rect(pymupdf.Rect(0, 0, 595, 55), color=navy, fill=navy)
        page.insert_text((margin, 35), title, fontname="ArialBold" if bold_file else "hebo",
                         fontfile=bold_file, fontsize=15, color=(1, 1, 1))
        page.draw_line((margin, 812), (595 - margin, 812), color=border, width=0.7)
        footer = "Radnóti Hack & Code  •  Megoldókulcs" if is_answer else "Radnóti Hack & Code  •  Teszt"
        page.insert_text((margin, 829), footer, fontname="Arial" if regular_file else "helv",
                         fontfile=regular_file, fontsize=8, color=muted)
        page.insert_text((595 - margin - 25, 829), str(page_number), fontname="Arial" if regular_file else "helv",
                         fontfile=regular_file, fontsize=8, color=muted)
        y = 75

    def put(text: str, x: float, top: float, max_width: float, *, size=9.5, font=None, color=ink, leading=None):
        font = font or regular
        rows = wrap(text, font, size, max_width)
        line_step = leading or size * 1.38
        for i, row in enumerate(rows):
            page.insert_text((x, top + size + i * line_step), row,
                             fontname="ArialBold" if font is bold else "Arial" if regular_file else "helv",
                             fontfile=bold_file if font is bold else regular_file,
                             fontsize=size, color=color)
        return len(rows) * line_step

    new_page()
    for paragraph in intro:
        if paragraph.startswith("Automatikus OCR-átirat"):
            continue
        h = put(paragraph, margin, y, content_width, size=9, color=muted)
        y += h + 6
    if not is_answer:
        y += 2

    for kind, value in blocks:
        if kind == "section":
            if y + 36 > page_bottom:
                new_page()
            page.insert_text((margin, y + 17), value, fontname="ArialBold" if bold_file else "hebo",
                             fontfile=bold_file, fontsize=12, color=blue)
            y += 30
            continue
        if kind == "note":
            h = put("•  " + value, margin + 6, y, content_width - 12, size=9.2)
            y += h + 5
            continue

        if kind == "question":
            question, items = value
            prepared = []
            title_lines = wrap(question, bold, 10.5, content_width - 30)
            h = 10 + len(title_lines) * 14 + 3
            for item_kind, text in items:
                if item_kind == "choice":
                    rows = wrap(text, regular, 9.5, content_width - 64)
                    ih = max(15, len(rows) * 13.2)
                elif item_kind == "truth":
                    rows = wrap(text, regular, 9.5, content_width - 32)
                    ih = len(rows) * 13.2 + 15
                else:
                    rows = wrap(text, regular, 9.5, content_width - 54)
                    ih = len(rows) * 13.2
                prepared.append((item_kind, text, rows, ih))
                h += ih + 5
            h += 18
            if y + h > page_bottom:
                new_page()
            rect = pymupdf.Rect(margin, y, 595 - margin, y + h)
            page.draw_rect(rect, color=border, fill=pale, width=0.8)
            page.draw_line((margin + 1, y + 7), (margin + 1, y + h - 7), color=blue, width=2.2)
            top = y + 10
            for row in title_lines:
                page.insert_text((margin + 14, top + 11), row,
                                 fontname="ArialBold" if bold_file else "hebo", fontfile=bold_file,
                                 fontsize=10.5, color=navy)
                top += 14
            top += 3
            for item_kind, text, rows, ih in prepared:
                if item_kind == "choice":
                    box = pymupdf.Rect(margin + 15, top + 2, margin + 25, top + 12)
                    page.draw_rect(box, color=blue, fill=(1, 1, 1), width=1.1)
                    for i, row in enumerate(rows):
                        page.insert_text((margin + 34, top + 10 + i * 13.2), row,
                                         fontname="Arial" if regular_file else "helv", fontfile=regular_file,
                                         fontsize=9.5, color=ink)
                elif item_kind == "truth":
                    text_h = put(text, margin + 15, top, content_width - 30, size=9.5)
                    opt_y = top + text_h + 2
                    for label, dx in (("Igaz", 0), ("Hamis", 65)):
                        box = pymupdf.Rect(margin + 17 + dx, opt_y + 1, margin + 27 + dx, opt_y + 11)
                        page.draw_rect(box, color=blue, fill=(1, 1, 1), width=1.1)
                        page.insert_text((margin + 33 + dx, opt_y + 10), label,
                                         fontname="Arial" if regular_file else "helv", fontfile=regular_file,
                                         fontsize=9, color=ink)
                    top += text_h + 16
                    continue
                else:
                    prefix = "•" if item_kind == "bullet" else ""
                    x = margin + 16 if prefix else margin + 15
                    if prefix:
                        page.draw_circle((x + 2, top + 6), 1.5, color=blue, fill=blue)
                        x += 8
                    for i, row in enumerate(rows):
                        page.insert_text((x, top + 10 + i * 13.2), row,
                                         fontname="Arial" if regular_file else "helv", fontfile=regular_file,
                                         fontsize=9.5, color=ink)
                top += ih + 5
            y += h + 10
            continue

        number, answer, note = value
        answer_rows = wrap(answer, bold, 10, content_width - 68)
        note_rows = wrap(note, regular, 8.8, content_width - 68) if note else []
        h = max(42, 18 + len(answer_rows) * 14 + len(note_rows) * 12 + 14)
        if y + h > page_bottom:
            new_page()
        rect = pymupdf.Rect(margin, y, 595 - margin, y + h)
        page.draw_rect(rect, color=border, fill=(1, 1, 1), width=0.75)
        pill = pymupdf.Rect(margin + 10, y + 10, margin + 38, y + 32)
        page.draw_rect(pill, color=blue, fill=blue, width=0)
        page.insert_text((margin + 16, y + 25), number, fontname="ArialBold" if bold_file else "hebo",
                         fontfile=bold_file, fontsize=9, color=(1, 1, 1))
        top = y + 9
        for row in answer_rows:
            page.insert_text((margin + 50, top + 11), row, fontname="ArialBold" if bold_file else "hebo",
                             fontfile=bold_file, fontsize=10, color=navy)
            top += 14
        for row in note_rows:
            page.insert_text((margin + 50, top + 10), row, fontname="Arial" if regular_file else "helv",
                             fontfile=regular_file, fontsize=8.8, color=muted)
            top += 12
        y += h + 7

    doc.save(target)


def main():
    TESTS.mkdir(parents=True, exist_ok=True)
    if "--ocr-draft" in sys.argv:
        test_source = BACKUP / "teszt.pdf"
        answer_source = BACKUP / "válaszok.pdf"
        if not test_source.exists() or not answer_source.exists():
            raise FileNotFoundError("Az eredeti teszt- és válasz-PDF-ek a teacher/tesztek/backup mappában szükségesek.")
        engine = make_ocr()
        for name, source, title in (
            ("test.ocr-draft.md", test_source, "Teszt – nyers OCR-átirat"),
            ("megoldás.ocr-draft.md", answer_source, "Válaszlap – nyers OCR-átirat"),
        ):
            (TESTS / name).write_text(to_markdown(title, ocr_pdf(source, engine)), encoding="utf-8")
        print("Created separate OCR drafts; curated Markdown files were left untouched.")
        return

    test_md = (TESTS / "test.md").read_text(encoding="utf-8")
    answer_md = (TESTS / "megoldás.md").read_text(encoding="utf-8")
    markdown_to_pdf(test_md, TESTS / "test.pdf")
    markdown_to_pdf(answer_md, TESTS / "megoldás.pdf")
    print("Created test.pdf and megoldás.pdf from the curated Markdown files.")


if __name__ == "__main__":
    main()


