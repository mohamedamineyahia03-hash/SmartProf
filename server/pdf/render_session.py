"""Renders a session as a printable worksheet PDF: the questions with blank
space to answer on paper, followed by a "corrigé" (answer key) page.

Pure-Python (reportlab) on purpose — WeasyPrint would give nicer HTML/CSS
reuse but needs a Pango/Cairo/GTK system runtime that isn't installed here
and can't be assumed on every deploy target; reportlab has no such
dependency.

Always dated the day the PDF is generated (never a date tied to any
exercise's source — there isn't one in the content model anyway, but the
rule is: always datetime.now(), never anything read out of exercise
content). "SmartProf" appears as a light watermark, not as exercise
content — see project memory, PDF export requirement (2026-09-01).

Font: Amiri (SIL Open Font License), bundled at server/pdf/fonts/. Chosen
over more "brand-matching" options (e.g. Baloo Bhaijaan 2, the Arabic
sibling of the web app's Baloo 2) because arabic-reshaper + reportlab only
draw glyphs straight from the font's cmap — there's no real OpenType
shaping engine in this pipeline — so the font must carry legacy Arabic
Presentation Forms glyphs (U+FE70-FEFF) directly; most modern Arabic
Google Fonts (including Baloo Bhaijaan 2) only shape via GSUB and render as
tofu here. Amiri is a classical naskh face with full presentation-forms
coverage and was designed for exactly this kind of print/typesetting use,
which also suits a literacy worksheet well.

KNOWN LIMITATION: exercise "visual" fields (emoji scenes like counting
apples or a position diagram) are not rendered here — emoji glyphs aren't
in Amiri either. Exercises with a visual still print their question text;
the visual just doesn't appear on paper yet.
"""

import io
import os
from datetime import datetime, timezone

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

FONT_NAME = "SmartProfArabic"
FONT_NAME_BOLD = "SmartProfArabic-Bold"

_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")
_FONT_REGULAR = os.path.join(_FONT_DIR, "Amiri-Regular.ttf")
_FONT_BOLD = os.path.join(_FONT_DIR, "Amiri-Bold.ttf")

# Brand palette — matches the web app's light-theme accent (pink/coral) and
# neutrals, so a printed worksheet still reads as the same product.
ACCENT = HexColor("#E8225F")
ACCENT_SOFT = HexColor("#FBE3EA")
INK = HexColor("#181B33")
MUTED = HexColor("#6B6F94")
PAPER_SOFT = HexColor("#F5F3FB")
GOOD = HexColor("#0E9F6E")
GOOD_SOFT = HexColor("#E3F6EE")

TRIMESTER_LABELS_AR = {"T1": "الفصل الأول", "T2": "الفصل الثاني", "T3": "الفصل الثالث"}

_font_registered = False


def _register_font():
    global _font_registered
    if _font_registered:
        return
    if not (os.path.exists(_FONT_REGULAR) and os.path.exists(_FONT_BOLD)):
        raise RuntimeError(
            f"Bundled font missing at {_FONT_DIR} — expected Amiri-Regular.ttf and "
            "Amiri-Bold.ttf (SIL Open Font License). See the module docstring."
        )
    pdfmetrics.registerFont(TTFont(FONT_NAME, _FONT_REGULAR))
    pdfmetrics.registerFont(TTFont(FONT_NAME_BOLD, _FONT_BOLD))
    _font_registered = True


def _shape(text):
    """Arabic letters change glyph shape depending on their position in the
    word (isolated/initial/medial/final) and the whole line needs reordering
    for right-to-left display — reportlab has no text-shaping engine, so
    both steps happen here before anything is drawn. Non-Arabic text passes
    through untouched."""
    if text is None:
        return ""
    return get_display(arabic_reshaper.reshape(str(text)))


def _styles():
    return {
        "brand": ParagraphStyle("brand", fontName=FONT_NAME_BOLD, fontSize=22, textColor=white, alignment=TA_CENTER),
        "tagline": ParagraphStyle("tagline", fontName=FONT_NAME, fontSize=10, textColor=white, alignment=TA_CENTER, spaceBefore=2),
        "meta": ParagraphStyle("meta", fontName=FONT_NAME, fontSize=10.5, textColor=MUTED, alignment=TA_RIGHT, leading=15),
        "section": ParagraphStyle("section", fontName=FONT_NAME_BOLD, fontSize=15, textColor=ACCENT, alignment=TA_RIGHT, spaceBefore=2, spaceAfter=10),
        "q": ParagraphStyle("q", fontName=FONT_NAME_BOLD, fontSize=12, textColor=INK, alignment=TA_RIGHT, leading=17),
        "q_ltr": ParagraphStyle("q_ltr", fontName=FONT_NAME_BOLD, fontSize=12, textColor=INK, alignment=TA_LEFT, leading=17),
        "q_sub": ParagraphStyle("q_sub", fontName=FONT_NAME_BOLD, fontSize=11.5, textColor=INK, alignment=TA_RIGHT, leading=16, spaceBefore=6),
        "q_sub_ltr": ParagraphStyle("q_sub_ltr", fontName=FONT_NAME_BOLD, fontSize=11.5, textColor=INK, alignment=TA_LEFT, leading=16, spaceBefore=6),
        "choice": ParagraphStyle("choice", fontName=FONT_NAME, fontSize=11, textColor=INK, alignment=TA_RIGHT, leading=15),
        "choice_ltr": ParagraphStyle("choice_ltr", fontName=FONT_NAME, fontSize=11, textColor=INK, alignment=TA_LEFT, leading=15),
        "blank": ParagraphStyle("blank", fontName=FONT_NAME, fontSize=11, textColor=MUTED, alignment=TA_RIGHT),
        "blank_ltr": ParagraphStyle("blank_ltr", fontName=FONT_NAME, fontSize=11, textColor=MUTED, alignment=TA_LEFT),
        "badge": ParagraphStyle("badge", fontName=FONT_NAME_BOLD, fontSize=13, textColor=white, alignment=TA_CENTER),
        "answer": ParagraphStyle("answer", fontName=FONT_NAME_BOLD, fontSize=11.5, textColor=GOOD, alignment=TA_RIGHT, leading=15),
        "answer_ltr": ParagraphStyle("answer_ltr", fontName=FONT_NAME_BOLD, fontSize=11.5, textColor=GOOD, alignment=TA_LEFT, leading=15),
        "explanation": ParagraphStyle("explanation", fontName=FONT_NAME, fontSize=9.5, textColor=MUTED, alignment=TA_RIGHT, leading=13.5, spaceBefore=2),
        "explanation_ltr": ParagraphStyle("explanation_ltr", fontName=FONT_NAME, fontSize=9.5, textColor=MUTED, alignment=TA_LEFT, leading=13.5, spaceBefore=2),
    }


def _p(text, style, rtl=True):
    return Paragraph(_shape(text) if rtl else str(text), style)


def _choice_grid(choices, style, rtl=True):
    """Choices side by side, 2 per row, instead of one bare line each — the
    single biggest fix for a worksheet that otherwise reads as mostly empty
    space when most exercises only have 2-3 short choices."""
    # U+2022 (•), not U+25CB (○) -- Amiri (Arabic-focused) doesn't carry the
    # latter and it silently renders as a missing-glyph box.
    cells = [_p(f"•  {c}", style, rtl=rtl) for c in choices]
    rows = [cells[i : i + 2] for i in range(0, len(cells), 2)]
    if rows and len(rows[-1]) == 1:
        rows[-1].append("")
    col_width = 82 * mm
    table = Table(rows, colWidths=[col_width, col_width])
    table.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return table


def _exercise_card(number, content, styles, rtl):
    """One exercise wrapped in a shaded rounded box with a numbered badge —
    gives the page real visual structure instead of plain flowing text."""
    suffix = "" if rtl else "_ltr"
    badge = Table([[_p(str(number), styles["badge"])]], colWidths=[9 * mm], rowHeights=[9 * mm])
    badge.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ROUNDEDCORNERS", [9, 9, 9, 9]),
    ]))

    body = [_p(content.get("question", ""), styles["q" + suffix], rtl=rtl)]

    sub_questions = content.get("sub_questions")
    if sub_questions:
        for j, sub in enumerate(sub_questions, start=1):
            body.append(_p(f"{j}) {sub.get('question', '')}", styles["q_sub" + suffix], rtl=rtl))
            if sub.get("choices"):
                body.append(Spacer(1, 2 * mm))
                body.append(_choice_grid(sub["choices"], styles["choice" + suffix], rtl=rtl))
            else:
                body.append(Spacer(1, 2 * mm))
                body.append(_p("......................................", styles["blank" + suffix], rtl=False))
    elif content.get("choices"):
        body.append(Spacer(1, 3 * mm))
        body.append(_choice_grid(content["choices"], styles["choice" + suffix], rtl=rtl))
    else:
        body.append(Spacer(1, 3 * mm))
        body.append(_p("......................................", styles["blank" + suffix], rtl=False))

    row = Table([[body, badge]], colWidths=[160 * mm, 12 * mm])
    row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("BACKGROUND", (0, 0), (-1, -1), PAPER_SOFT),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
        ("LEFTPADDING", (0, 0), (0, 0), 6 * mm),
        ("RIGHTPADDING", (0, 0), (0, 0), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5 * mm),
    ]))
    return KeepTogether([row, Spacer(1, 5 * mm)])


def _answer_row(number, content, styles, rtl):
    suffix = "" if rtl else "_ltr"
    body = []
    sub_questions = content.get("sub_questions")
    if sub_questions:
        for j, sub in enumerate(sub_questions, start=1):
            body.append(_p(f"{number}.{j}  {sub.get('answer', '')}", styles["answer" + suffix], rtl=rtl))
            if sub.get("explanation"):
                body.append(_p(sub["explanation"], styles["explanation" + suffix], rtl=rtl))
    else:
        body.append(_p(f"{number}.  {content.get('answer', '')}", styles["answer" + suffix], rtl=rtl))
        if content.get("explanation"):
            body.append(_p(content["explanation"], styles["explanation" + suffix], rtl=rtl))

    table = Table([[body]], colWidths=[172 * mm])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GOOD_SOFT),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ("LEFTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3.5 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.5 * mm),
    ]))
    return KeepTogether([table, Spacer(1, 3.5 * mm)])


def _watermark(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME_BOLD, 90)
    canvas.setFillColor(ACCENT_SOFT)
    canvas.translate(A4[0] / 2, A4[1] / 2)
    canvas.rotate(35)
    canvas.drawCentredString(0, 0, "SmartProf")
    canvas.restoreState()


def _header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(ACCENT)
    canvas.rect(0, A4[1] - 28 * mm, A4[0], 28 * mm, stroke=0, fill=1)
    canvas.restoreState()


def _on_page(canvas, doc):
    _watermark(canvas, doc)
    _header(canvas, doc)


def render_session_pdf(session_row, exercises, child_name=None, level_label=None, subject_label=None):
    """exercises: ordered list of LibraryCacheExercise rows matching
    session_row.exercise_ids. Returns PDF bytes."""
    _register_font()
    styles = _styles()
    today = datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y")

    story = [Spacer(1, 6 * mm)]
    story.append(_p("SmartProf", styles["brand"], rtl=False))
    story.append(_p("ورقة عمل — SmartProf", styles["tagline"]))
    story.append(Spacer(1, 12 * mm))

    meta_bits = [f"التاريخ: {today}"]
    if child_name:
        meta_bits.append(f"الاسم: {child_name}")
    if level_label:
        meta_bits.append(f"المستوى: {level_label}")
    if subject_label:
        meta_bits.append(f"المادة: {subject_label}")
    meta_bits.append(TRIMESTER_LABELS_AR.get(session_row.trimester, session_row.trimester))
    story.append(_p("  •  ".join(meta_bits), styles["meta"]))
    story.append(Spacer(1, 8 * mm))

    for i, exercise in enumerate(exercises, start=1):
        rtl = exercise.language == "ar"
        story.append(_exercise_card(i, exercise.content, styles, rtl))

    story.append(PageBreak())
    story.append(Spacer(1, 6 * mm))
    story.append(_p("الحل", styles["section"]))

    for i, exercise in enumerate(exercises, start=1):
        rtl = exercise.language == "ar"
        story.append(_answer_row(i, exercise.content, styles, rtl))

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=34 * mm,
        bottomMargin=16 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
    )
    doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
    return buffer.getvalue()
