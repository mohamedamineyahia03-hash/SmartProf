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

KNOWN LIMITATION: exercise "visual" fields (emoji scenes like counting
apples or a position diagram) are not rendered here — the bundled/system
fonts used for Arabic text don't carry color-emoji glyphs, and adding an
emoji-capable font is a separate follow-up. Exercises with a visual still
print their question text; the visual just doesn't appear on paper yet.
"""

import io
import os
from datetime import datetime, timezone

import arabic_reshaper
from bidi.algorithm import get_display
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer

FONT_NAME = "SmartProfArabic"

TRIMESTER_LABELS_AR = {"T1": "الفصل الأول", "T2": "الفصل الثاني", "T3": "الفصل الثالث"}

# First candidate is the one that makes PDF generation portable across dev
# machines and whatever the app eventually deploys on — it isn't bundled yet
# (see server/pdf/fonts/README below-equivalent note); drop in a real Arabic
# TTF there (e.g. Noto Naskh Arabic, SIL Open Font License) and every other
# environment stops depending on a system font being present at all.
_FONT_CANDIDATES = [
    os.path.join(os.path.dirname(__file__), "fonts", "NotoNaskhArabic-Regular.ttf"),
    "/usr/share/fonts/truetype/noto/NotoNaskhArabic-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSansArabic-Regular.ttf",
    "/usr/share/fonts/noto/NotoNaskhArabic-Regular.ttf",
    "C:/Windows/Fonts/arial.ttf",
]

_font_registered = False


def _register_font():
    global _font_registered
    if _font_registered:
        return
    for path in _FONT_CANDIDATES:
        if os.path.exists(path):
            pdfmetrics.registerFont(TTFont(FONT_NAME, path))
            _font_registered = True
            return
    raise RuntimeError(
        "No Arabic-capable font found for PDF export. Bundle one at "
        "server/pdf/fonts/NotoNaskhArabic-Regular.ttf (e.g. Noto Naskh Arabic, "
        "SIL Open Font License) — see the module docstring."
    )


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
        "meta": ParagraphStyle("meta", fontName=FONT_NAME, fontSize=10, textColor=HexColor("#6B6F94"), alignment=TA_RIGHT, spaceAfter=3),
        "title": ParagraphStyle("title", fontName=FONT_NAME, fontSize=18, textColor=HexColor("#181B33"), alignment=TA_RIGHT, spaceAfter=10),
        "section": ParagraphStyle("section", fontName=FONT_NAME, fontSize=14, textColor=HexColor("#E8225F"), alignment=TA_RIGHT, spaceBefore=6, spaceAfter=12),
        "q_ar": ParagraphStyle("q_ar", fontName=FONT_NAME, fontSize=12, alignment=TA_RIGHT, leading=17, spaceAfter=4),
        "q_ltr": ParagraphStyle("q_ltr", fontName=FONT_NAME, fontSize=12, alignment=TA_LEFT, leading=17, spaceAfter=4),
        "choice_ar": ParagraphStyle("choice_ar", fontName=FONT_NAME, fontSize=11, alignment=TA_RIGHT, leading=15),
        "choice_ltr": ParagraphStyle("choice_ltr", fontName=FONT_NAME, fontSize=11, alignment=TA_LEFT, leading=15),
        "blank_ar": ParagraphStyle("blank_ar", fontName=FONT_NAME, fontSize=11, alignment=TA_RIGHT, textColor=HexColor("#9296C4")),
        "blank_ltr": ParagraphStyle("blank_ltr", fontName=FONT_NAME, fontSize=11, alignment=TA_LEFT, textColor=HexColor("#9296C4")),
        "answer": ParagraphStyle("answer", fontName=FONT_NAME, fontSize=11, alignment=TA_RIGHT, leading=15, textColor=HexColor("#0E9F6E"), spaceAfter=2),
        "explanation": ParagraphStyle("explanation", fontName=FONT_NAME, fontSize=10, alignment=TA_RIGHT, leading=14, textColor=HexColor("#6B6F94"), spaceAfter=10),
    }


def _para(text, style, rtl=True):
    return Paragraph(_shape(text) if rtl else str(text), style)


def _watermark(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT_NAME, 60)
    canvas.setFillColor(HexColor("#F1EEFA"))
    canvas.translate(A4[0] / 2, A4[1] / 2)
    canvas.rotate(35)
    canvas.drawCentredString(0, 0, "SmartProf")
    canvas.restoreState()


def render_session_pdf(session_row, exercises, child_name=None, level_label=None, subject_label=None):
    """exercises: ordered list of LibraryCacheExercise rows matching
    session_row.exercise_ids. Returns PDF bytes."""
    _register_font()
    styles = _styles()
    today = datetime.now(timezone.utc).astimezone().strftime("%d/%m/%Y")

    story = []
    story.append(_para("SmartProf", styles["title"]))
    meta_bits = [f"التاريخ: {today}"]
    if child_name:
        meta_bits.append(f"الاسم: {child_name}")
    if level_label:
        meta_bits.append(f"المستوى: {level_label}")
    if subject_label:
        meta_bits.append(f"المادة: {subject_label}")
    # A spelled-out Arabic ordinal ("الفصل الثاني") rather than the internal
    # "T2" code -- avoids a Latin+digit token getting visually reversed by
    # the bidi algorithm when embedded in an RTL sentence, and reads better
    # on a printed worksheet anyway.
    meta_bits.append(TRIMESTER_LABELS_AR.get(session_row.trimester, session_row.trimester))
    story.append(_para(" — ".join(meta_bits), styles["meta"]))
    story.append(Spacer(1, 10 * mm))

    for i, exercise in enumerate(exercises, start=1):
        content = exercise.content
        rtl = exercise.language == "ar"
        q_style = styles["q_ar"] if rtl else styles["q_ltr"]
        c_style = styles["choice_ar"] if rtl else styles["choice_ltr"]
        blank_style = styles["blank_ar"] if rtl else styles["blank_ltr"]

        question_text = content.get("question", "")
        story.append(_para(f"{i}. {question_text}", q_style, rtl=rtl))

        if content.get("sub_questions"):
            for j, sub in enumerate(content["sub_questions"], start=1):
                story.append(_para(f"{i}.{j}) {sub.get('question', '')}", q_style, rtl=rtl))
                if sub.get("choices"):
                    for choice in sub["choices"]:
                        story.append(_para(f"○ {choice}", c_style, rtl=rtl))
                else:
                    story.append(_para("......................................", blank_style, rtl=False))
        elif content.get("choices"):
            for choice in content["choices"]:
                story.append(_para(f"○ {choice}", c_style, rtl=rtl))
        else:
            story.append(_para("......................................", blank_style, rtl=False))

        story.append(Spacer(1, 6 * mm))

    story.append(PageBreak())
    story.append(_para("الحل", styles["section"]))

    for i, exercise in enumerate(exercises, start=1):
        content = exercise.content
        rtl = exercise.language == "ar"
        if content.get("sub_questions"):
            for j, sub in enumerate(content["sub_questions"], start=1):
                story.append(_para(f"{i}.{j}) {sub.get('answer', '')}", styles["answer"], rtl=rtl))
                if sub.get("explanation"):
                    story.append(_para(sub["explanation"], styles["explanation"], rtl=rtl))
        else:
            story.append(_para(f"{i}. {content.get('answer', '')}", styles["answer"], rtl=rtl))
            if content.get("explanation"):
                story.append(_para(content["explanation"], styles["explanation"], rtl=rtl))

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=20 * mm,
        bottomMargin=18 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
    )
    doc.build(story, onFirstPage=_watermark, onLaterPages=_watermark)
    return buffer.getvalue()
