#!/usr/bin/env python3
"""Generate a print-friendly PDF from SCENARIUSZ.md."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import reportlab
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph, Table, TableStyle


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "SCENARIUSZ.md"
OUTPUT = ROOT / "output" / "pdf" / "SCENARIUSZ.pdf"

INK = colors.HexColor("#221323")
MUTED = colors.HexColor("#665C67")
MAGENTA = colors.HexColor("#B01972")
CYAN = colors.HexColor("#007F89")
PAPER = colors.HexColor("#FFFFFF")
SOFT = colors.HexColor("#F5F0F4")
LINE = colors.HexColor("#D9CDD6")


def register_fonts() -> None:
    dependency_root = Path(sys.executable).resolve().parents[2]
    runtime_fonts = (
        dependency_root
        / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
    )
    system_fonts = Path("/System/Library/Fonts/Supplemental")
    reportlab_fonts = Path(reportlab.__file__).resolve().parent / "fonts"
    candidates = [
        (
            runtime_fonts / "NotoSans-Regular.ttf",
            runtime_fonts / "NotoSans-Bold.ttf",
            runtime_fonts / "NotoSans-Italic.ttf",
        ),
        (
            system_fonts / "Arial.ttf",
            system_fonts / "Arial Bold.ttf",
            system_fonts / "Arial Italic.ttf",
        ),
        (
            reportlab_fonts / "Vera.ttf",
            reportlab_fonts / "VeraBd.ttf",
            reportlab_fonts / "VeraIt.ttf",
        ),
    ]
    regular, bold, italic = next(fonts for fonts in candidates if all(path.exists() for path in fonts))
    pdfmetrics.registerFont(TTFont("Scenario", str(regular)))
    pdfmetrics.registerFont(TTFont("Scenario-Bold", str(bold)))
    pdfmetrics.registerFont(TTFont("Scenario-Italic", str(italic)))
    pdfmetrics.registerFontFamily(
        "Scenario",
        normal="Scenario",
        bold="Scenario-Bold",
        italic="Scenario-Italic",
        boldItalic="Scenario-Bold",
    )


def normalize_text(text: str) -> str:
    return (
        text.replace("\u2011", "-")
        .replace("\u2012", "-")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .replace("\u2212", "-")
    )


def inline_markup(text: str) -> str:
    """Convert the small Markdown subset used by SCENARIUSZ.md to ReportLab XML."""
    text = normalize_text(text.strip())
    chunks = re.split(r"(\*\*.*?\*\*|`.*?`)", text)
    output: list[str] = []
    for chunk in chunks:
        if chunk.startswith("**") and chunk.endswith("**"):
            output.append(f"<b>{escape(chunk[2:-2])}</b>")
        elif chunk.startswith("`") and chunk.endswith("`"):
            output.append(f'<font name="Scenario-Bold">{escape(chunk[1:-1])}</font>')
        else:
            output.append(escape(chunk))
    return "".join(output)


def parse_source() -> tuple[list[str], list[tuple[int, str, list[str]]]]:
    raw = SOURCE.read_text(encoding="utf-8")
    raw = re.sub(r"^# .+\n+", "", raw, count=1)
    heading = re.compile(r"^## (\d+)\. (.+)$", re.MULTILINE)
    matches = list(heading.finditer(raw))
    if not matches:
        raise ValueError("No slide sections found in SCENARIUSZ.md")

    intro = [p.strip() for p in raw[: matches[0].start()].strip().split("\n\n") if p.strip()]
    sections: list[tuple[int, str, list[str]]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(raw)
        body = raw[match.end() : end].strip()
        paragraphs = [p.replace("\n", " ").strip() for p in body.split("\n\n") if p.strip()]
        sections.append((int(match.group(1)), match.group(2).strip(), paragraphs))
    return intro, sections


def draw_cover(canvas: Canvas) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(INK)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(MAGENTA)
    canvas.rect(0, 0, 13 * mm, height, fill=1, stroke=0)
    canvas.setFillColor(CYAN)
    canvas.rect(13 * mm, height - 6 * mm, width - 13 * mm, 6 * mm, fill=1, stroke=0)
    canvas.restoreState()


def draw_page(canvas: Canvas) -> None:
    width, height = A4
    canvas.saveState()
    canvas.setFillColor(PAPER)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setStrokeColor(MAGENTA)
    canvas.setLineWidth(1.2)
    canvas.line(18 * mm, height - 13 * mm, width - 18 * mm, height - 13 * mm)
    canvas.setFont("Scenario-Bold", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, height - 10 * mm, "AI ENABLEMENT | CLAUDE CODE KICKOFF")
    canvas.setFont("Scenario", 7.5)
    canvas.drawRightString(width - 18 * mm, 10 * mm, f"SCENARIUSZ PROWADZĄCEGO  |  {canvas.getPageNumber()}")
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(18 * mm, 13 * mm, width - 18 * mm, 13 * mm)
    canvas.restoreState()


def build_pdf() -> None:
    register_fonts()
    intro, sections = parse_source()
    if len(sections) != 52:
        raise ValueError(f"Expected 52 slide sections, found {len(sections)}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    cover_eyebrow = ParagraphStyle(
        "CoverEyebrow",
        parent=styles["Normal"],
        fontName="Scenario-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#45CBD0"),
        tracking=1.1,
        alignment=TA_LEFT,
        spaceAfter=7 * mm,
    )
    cover_title = ParagraphStyle(
        "CoverTitle",
        parent=styles["Title"],
        fontName="Scenario-Bold",
        fontSize=31,
        leading=37,
        textColor=colors.white,
        alignment=TA_LEFT,
        spaceAfter=8 * mm,
    )
    cover_subtitle = ParagraphStyle(
        "CoverSubtitle",
        parent=styles["Normal"],
        fontName="Scenario",
        fontSize=14,
        leading=20,
        textColor=colors.HexColor("#E6DCE4"),
        alignment=TA_LEFT,
    )
    title_style = ParagraphStyle(
        "DocumentTitle",
        parent=styles["Heading1"],
        fontName="Scenario-Bold",
        fontSize=22,
        leading=27,
        textColor=INK,
        spaceAfter=6 * mm,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["BodyText"],
        fontName="Scenario",
        fontSize=9.4,
        leading=13.4,
        textColor=INK,
        alignment=TA_LEFT,
        spaceAfter=3.2 * mm,
        allowWidows=0,
        allowOrphans=0,
    )
    small_style = ParagraphStyle(
        "Small",
        parent=body_style,
        fontSize=8.4,
        leading=11.8,
        textColor=MUTED,
        spaceAfter=0,
    )
    cover_small_style = ParagraphStyle(
        "CoverSmall",
        parent=small_style,
        textColor=colors.HexColor("#E6DCE4"),
    )
    slide_number_style = ParagraphStyle(
        "SlideNumber",
        parent=styles["Normal"],
        fontName="Scenario-Bold",
        fontSize=15,
        leading=18,
        textColor=colors.white,
        alignment=TA_CENTER,
    )
    slide_title_style = ParagraphStyle(
        "SlideTitle",
        parent=styles["Heading2"],
        fontName="Scenario-Bold",
        fontSize=13.2,
        leading=16.5,
        textColor=INK,
        alignment=TA_LEFT,
    )

    canvas = Canvas(str(OUTPUT), pagesize=A4)
    canvas.setTitle("Scenariusz prowadzącego - AI Enablement: Claude Code kickoff")
    canvas.setAuthor("Michael Dubel")
    canvas.setSubject("Polish presenter script for the AI Enablement kickoff deck")

    page_width, page_height = A4
    content_x = 18 * mm
    content_width = page_width - 36 * mm
    content_top = page_height - 22 * mm
    content_bottom = 18 * mm

    def draw_flowable(flowable, x: float, y: float, width: float) -> float:
        _, height = flowable.wrap(width, page_height)
        flowable.drawOn(canvas, x, y - height)
        return y - height

    draw_cover(canvas)
    cover_x = 20 * mm
    cover_width = 132 * mm
    y = page_height - 62 * mm
    y = draw_flowable(Paragraph("AI ENABLEMENT | CLAUDE CODE KICKOFF", cover_eyebrow), cover_x, y, cover_width)
    y -= 7 * mm
    y = draw_flowable(Paragraph("Scenariusz<br/>prowadzącego", cover_title), cover_x, y, cover_width)
    y -= 8 * mm
    y = draw_flowable(Paragraph("Polskie notatki do 52 angielskich slajdów", cover_subtitle), cover_x, y, cover_width)
    y -= 17 * mm

    cover_info = Table(
        [
            [Paragraph("FORMAT", cover_small_style), Paragraph("A4 | wersja do druku", cover_small_style)],
            [Paragraph("CZAS", cover_small_style), Paragraph("około 2 godzin", cover_small_style)],
            [Paragraph("TRYB", cover_small_style), Paragraph("materiał modułowy", cover_small_style)],
        ],
        colWidths=[32 * mm, 70 * mm],
        hAlign="LEFT",
    )
    cover_info.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#32192F")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#704C6A")),
                ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
            ]
        )
    )
    draw_flowable(cover_info, cover_x, y, 102 * mm)
    canvas.showPage()

    draw_page(canvas)
    y = content_top
    y = draw_flowable(Paragraph("Jak korzystać z dokumentu", title_style), content_x, y, content_width)
    y -= 6 * mm
    for paragraph in intro:
        flowable = Paragraph(inline_markup(paragraph), body_style)
        y = draw_flowable(flowable, content_x, y, content_width) - flowable.style.spaceAfter

    agenda_rows = [
        ("START", "Slajdy 1-4", "Cel i mapa spotkania"),
        ("01", "Slajdy 5-11", "Poziomy adopcji"),
        ("02", "Slajdy 12-18", "Architektura systemów agentowych"),
        ("03", "Slajdy 19-25", "Claude Code"),
        ("04", "Slajdy 26-31", "Niezawodność i guardrails"),
        ("05", "Slajdy 32-36", "SDLC i współpraca"),
        ("06", "Slajdy 37-46", "Koszt, jakość i analiza porażek"),
        ("07", "Slajdy 47-52", "Hackathon i zamknięcie"),
    ]
    agenda = Table(
        [[Paragraph(f"<b>{a}</b>", small_style), Paragraph(b, small_style), Paragraph(c, small_style)] for a, b, c in agenda_rows],
        colWidths=[18 * mm, 30 * mm, 115 * mm],
        hAlign="LEFT",
    )
    agenda.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, -1), INK),
                ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
                ("BACKGROUND", (1, 0), (-1, -1), SOFT),
                ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.white),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.4 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.4 * mm),
            ]
        )
    )
    y -= 4 * mm
    draw_flowable(agenda, content_x, y, content_width)
    canvas.showPage()
    draw_page(canvas)
    y = content_top

    for number, title, paragraphs in sections:
        heading = Table(
            [
                [
                    Paragraph(f"{number:02d}", slide_number_style),
                    Paragraph(escape(normalize_text(title)), slide_title_style),
                ]
            ],
            colWidths=[18 * mm, 145 * mm],
            hAlign="LEFT",
        )
        heading.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (0, 0), MAGENTA),
                    ("BACKGROUND", (1, 0), (1, 0), SOFT),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("LEFTPADDING", (0, 0), (0, 0), 2 * mm),
                    ("RIGHTPADDING", (0, 0), (0, 0), 2 * mm),
                    ("TOPPADDING", (0, 0), (-1, -1), 3.2 * mm),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 3.2 * mm),
                    ("LEFTPADDING", (1, 0), (1, 0), 4 * mm),
                    ("RIGHTPADDING", (1, 0), (1, 0), 4 * mm),
                    ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ]
            )
        )
        body_flowables = [Paragraph(inline_markup(p), body_style) for p in paragraphs]
        _, heading_height = heading.wrap(content_width, page_height)
        body_heights = []
        for flowable in body_flowables:
            _, paragraph_height = flowable.wrap(content_width, page_height)
            body_heights.append(paragraph_height + flowable.style.spaceAfter)
        block_height = heading_height + 3 * mm + sum(body_heights) + 4.5 * mm

        if y - block_height < content_bottom:
            canvas.showPage()
            draw_page(canvas)
            y = content_top

        y = draw_flowable(heading, content_x, y, content_width)
        y -= 3 * mm
        for flowable in body_flowables:
            y = draw_flowable(flowable, content_x, y, content_width) - flowable.style.spaceAfter
        y -= 4.5 * mm

    canvas.save()
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build_pdf()
