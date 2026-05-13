"""Build a BSides Aarhus 2026 PowerPoint template matching the website design.

Generates a 16:9 .pptx with:
  - Title / cover slide
  - Agenda slide (used before talks and between talks)
  - Section divider
  - Content slide (title + body)
  - Speaker bio slide

Design tokens come from static/css/main.css.
"""
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "images" / "logo.png"
OUT = ROOT / "Plans" / "template-output" / "bsides-aarhus-2026-template.pptx"

# --- Design tokens (from main.css) -------------------------------------------------
BG          = RGBColor(0x0A, 0x0A, 0x0F)
BG_ELEV     = RGBColor(0x12, 0x12, 0x1A)
BG_CARD     = RGBColor(0x1A, 0x1A, 0x25)
TEXT        = RGBColor(0xE8, 0xE8, 0xED)
TEXT_MUTED  = RGBColor(0x88, 0x88, 0xA0)
ACCENT      = RGBColor(0x4A, 0xB8, 0xD2)
ACCENT_LT   = RGBColor(0x6D, 0xD0, 0xE7)
BORDER      = RGBColor(0x2A, 0x2A, 0x3A)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)

FONT_HEAD = "Inter"
FONT_BODY = "Inter"
FONT_MONO = "JetBrains Mono"

# --- Slide geometry (16:9) ---------------------------------------------------------
SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)


def set_solid(shape, rgb):
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb
    shape.line.fill.background()


def paint_background(slide, rgb=BG):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, SLIDE_W, SLIDE_H)
    set_solid(bg, rgb)
    bg.shadow.inherit = False


def accent_bar(slide, top=Inches(0.55), left=Inches(0.6), width=Inches(0.9), height=Emu(38100)):
    """Thin cyan accent bar — used as a visual signature on most slides."""
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    set_solid(bar, ACCENT)


def add_text(slide, left, top, width, height, text, *,
             size=18, bold=False, color=TEXT, font=FONT_BODY,
             align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def footer(slide, page_label=""):
    add_text(slide, Inches(0.6), Inches(7.05), Inches(8), Inches(0.3),
             "BSides Aarhus 2026  ·  June 20  ·  INCUBA Next, Aarhus",
             size=10, color=TEXT_MUTED, font=FONT_MONO)
    if page_label:
        add_text(slide, Inches(11.5), Inches(7.05), Inches(1.3), Inches(0.3),
                 page_label, size=10, color=TEXT_MUTED, font=FONT_MONO,
                 align=PP_ALIGN.RIGHT)


def add_logo(slide, left, top, height=Inches(0.6)):
    if LOGO.exists():
        slide.shapes.add_picture(str(LOGO), left, top, height=height)


# --- Slide builders ----------------------------------------------------------------
def build_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    paint_background(slide)

    # Decorative glow band behind title
    glow = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                  0, Inches(3.0), SLIDE_W, Inches(1.6))
    set_solid(glow, BG_ELEV)

    add_logo(slide, Inches(0.6), Inches(0.55), height=Inches(0.7))

    add_text(slide, Inches(0.6), Inches(2.2), Inches(12), Inches(0.5),
             "SECURITY CONFERENCE  ·  AARHUS",
             size=14, color=ACCENT, font=FONT_MONO, bold=True)

    add_text(slide, Inches(0.6), Inches(2.7), Inches(12), Inches(1.6),
             "BSides Aarhus 2026",
             size=72, bold=True, color=TEXT, font=FONT_HEAD)

    add_text(slide, Inches(0.6), Inches(4.6), Inches(12), Inches(0.6),
             "Talk title goes here",
             size=32, color=ACCENT_LT, font=FONT_HEAD)

    add_text(slide, Inches(0.6), Inches(5.4), Inches(12), Inches(0.45),
             "Speaker Name  ·  Affiliation",
             size=20, color=TEXT_MUTED, font=FONT_BODY)

    # Bottom meta strip
    strip = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                   0, Inches(6.8), SLIDE_W, Emu(38100))
    set_solid(strip, ACCENT)
    add_text(slide, Inches(0.6), Inches(6.95), Inches(12), Inches(0.4),
             "JUNE 20, 2026  ·  INCUBA NEXT, KATRINEBJERG  ·  BSIDESAARHUS.DK",
             size=11, color=TEXT_MUTED, font=FONT_MONO)


def build_agenda(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    paint_background(slide)
    add_logo(slide, Inches(0.6), Inches(0.5), height=Inches(0.55))
    accent_bar(slide, top=Inches(1.35), left=Inches(0.6), width=Inches(0.9))

    add_text(slide, Inches(0.6), Inches(1.5), Inches(12), Inches(0.8),
             "Agenda", size=44, bold=True, color=TEXT, font=FONT_HEAD)

    rows = [
        ("09:00", "Breakfast & networking", ""),
        ("10:00", "Track 1 / Track 2", "Parallel talks"),
        ("11:00", "Track 1 / Track 2", "Parallel talks"),
        ("11:45", "Lunch", ""),
        ("12:45", "Track 1 / Track 2", "Parallel talks"),
        ("13:50", "Track 1 / Track 2", "Parallel talks"),
        ("14:50", "Track 1 / Track 2", "Parallel talks"),
        ("15:30", "Networking session", ""),
        ("16:30", "Continue at Fredagscaféen", ""),
    ]

    top = Inches(2.55)
    row_h = Inches(0.45)
    for i, (t, title, sub) in enumerate(rows):
        y = top + row_h * i
        if i % 2 == 0:
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                        Inches(0.6), y, Inches(12.1), row_h)
            set_solid(bg, BG_CARD)
        add_text(slide, Inches(0.85), y + Emu(50000), Inches(1.4), row_h,
                 t, size=14, color=ACCENT, font=FONT_MONO, bold=True,
                 anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, Inches(2.3), y + Emu(50000), Inches(7.5), row_h,
                 title, size=15, color=TEXT, font=FONT_BODY, bold=True,
                 anchor=MSO_ANCHOR.MIDDLE)
        add_text(slide, Inches(9.8), y + Emu(50000), Inches(2.8), row_h,
                 sub, size=12, color=TEXT_MUTED, font=FONT_BODY,
                 anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)

    footer(slide, "Agenda")


def build_section_divider(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    paint_background(slide, BG_ELEV)

    # Large vertical accent
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,
                                 Inches(0.6), Inches(2.2), Inches(0.12), Inches(3.0))
    set_solid(bar, ACCENT)

    add_text(slide, Inches(1.0), Inches(2.1), Inches(11), Inches(0.6),
             "SECTION", size=16, color=ACCENT, font=FONT_MONO, bold=True)
    add_text(slide, Inches(1.0), Inches(2.7), Inches(11.5), Inches(2.0),
             "Section title goes here",
             size=60, bold=True, color=TEXT, font=FONT_HEAD)
    add_text(slide, Inches(1.0), Inches(4.6), Inches(11.5), Inches(0.6),
             "Optional one-line description for this section.",
             size=22, color=TEXT_MUTED, font=FONT_BODY)

    footer(slide)


def build_content(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    paint_background(slide)
    add_logo(slide, Inches(0.6), Inches(0.5), height=Inches(0.5))
    accent_bar(slide, top=Inches(1.3), left=Inches(0.6), width=Inches(0.7))

    add_text(slide, Inches(0.6), Inches(1.45), Inches(12), Inches(0.8),
             "Slide title", size=36, bold=True, color=TEXT, font=FONT_HEAD)

    bullets = [
        "Primary point — short, declarative, one idea per line",
        "Supporting detail with concrete example",
        "Evidence, data, or reference",
        "Takeaway or call to action",
    ]
    box = slide.shapes.add_textbox(Inches(0.6), Inches(2.5),
                                   Inches(12.1), Inches(4.2))
    tf = box.text_frame
    tf.word_wrap = True
    for i, b in enumerate(bullets):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(10)
        r1 = p.add_run()
        r1.text = "▍ "
        r1.font.name = FONT_MONO
        r1.font.size = Pt(20)
        r1.font.color.rgb = ACCENT
        r2 = p.add_run()
        r2.text = b
        r2.font.name = FONT_BODY
        r2.font.size = Pt(22)
        r2.font.color.rgb = TEXT

    footer(slide, "Content")


def build_speaker_bio(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    paint_background(slide)
    add_logo(slide, Inches(0.6), Inches(0.5), height=Inches(0.5))

    # Photo placeholder card
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                  Inches(0.6), Inches(1.6), Inches(4.2), Inches(4.8))
    set_solid(card, BG_CARD)
    card.adjustments[0] = 0.04
    add_text(slide, Inches(0.6), Inches(3.7), Inches(4.2), Inches(0.6),
             "[ Photo ]", size=16, color=TEXT_MUTED, font=FONT_MONO,
             align=PP_ALIGN.CENTER)

    accent_bar(slide, top=Inches(1.5), left=Inches(5.2), width=Inches(0.7))
    add_text(slide, Inches(5.2), Inches(1.65), Inches(7.5), Inches(0.4),
             "SPEAKER", size=14, color=ACCENT, font=FONT_MONO, bold=True)
    add_text(slide, Inches(5.2), Inches(2.1), Inches(7.5), Inches(0.9),
             "Speaker Name", size=40, bold=True, color=TEXT, font=FONT_HEAD)
    add_text(slide, Inches(5.2), Inches(3.05), Inches(7.5), Inches(0.5),
             "Role  ·  Company", size=20, color=ACCENT_LT, font=FONT_BODY)
    add_text(slide, Inches(5.2), Inches(3.8), Inches(7.5), Inches(2.8),
             "Short bio. Two or three sentences about background, "
             "specialization, and what the audience will take away from the "
             "talk. Keep it conversational and specific.",
             size=18, color=TEXT_MUTED, font=FONT_BODY)
    add_text(slide, Inches(5.2), Inches(6.2), Inches(7.5), Inches(0.4),
             "@handle  ·  speaker.example.com",
             size=14, color=ACCENT, font=FONT_MONO)

    footer(slide, "Speaker")


def main():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    build_cover(prs)
    build_agenda(prs)
    build_section_divider(prs)
    build_content(prs)
    build_speaker_bio(prs)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
