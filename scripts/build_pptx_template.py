"""Build a BSides Aarhus 2026 PowerPoint template matching the website design.

Generates a 16:9 .pptx with:
  - Title / cover slide
  - Agenda slide (used before talks and between talks)
  - Section divider
  - Content slide (title + body)
  - Speaker bio slide

Design tokens come from static/css/main.css.
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt, Emu

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "static" / "images" / "logo.png"
OUT_DIR = ROOT / "Plans" / "template-output"
OUT = OUT_DIR / "bsides-aarhus-2026-template.pptx"
BG_IMG = OUT_DIR / "_bg.png"
BG_IMG_ELEV = OUT_DIR / "_bg_elev.png"

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


# --- Background image (white dots + top-center cyan glow) --------------------------
def build_background(path: Path, *, base=(0x0A, 0x0A, 0x0F), width=2560, height=1440,
                     dot_count=70, glow_strength=0.22):
    """Render a static version of the website's particle + radial-gradient background.

    Mirrors static/js/main.js (particles, connecting lines) and main.css
    (radial-gradient ellipse at 50% 0%). Dots and lines are rendered white per
    request; the top-center glow uses the cyan accent.
    """
    rng = random.Random(20260620)
    img = Image.new("RGB", (width, height), base)

    # Top-center cyan radial glow — drawn as a soft blurred ellipse.
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gx, gy = width // 2, 0
    rx, ry = int(width * 0.6), int(height * 0.7)
    gd.ellipse((gx - rx, gy - ry, gx + rx, gy + ry),
               fill=(0x4A, 0xB8, 0xD2, int(255 * glow_strength)))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=180))
    img = Image.alpha_composite(img.convert("RGBA"), glow).convert("RGB")

    # Particles
    pts = []
    for _ in range(dot_count):
        pts.append((
            rng.uniform(0, width),
            rng.uniform(0, height),
            rng.uniform(2, 5),                 # radius in px
            rng.uniform(0.35, 0.85),           # alpha
        ))

    # Connecting lines (faint, white) — matches main.js connectDist behavior.
    connect = (width / 1920) * 150
    lines = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lines)
    for i, (x1, y1, _, _) in enumerate(pts):
        for x2, y2, _, _ in pts[i + 1:]:
            d = math.hypot(x1 - x2, y1 - y2)
            if d < connect:
                a = int(255 * (1 - d / connect) * 0.12)
                ld.line((x1, y1, x2, y2), fill=(255, 255, 255, a), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), lines).convert("RGB")

    # Dots (white, with a soft halo via blur+composite).
    dots = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for x, y, r, a in pts:
        dd.ellipse((x - r, y - r, x + r, y + r),
                   fill=(255, 255, 255, int(255 * a)))
    halo = dots.filter(ImageFilter.GaussianBlur(radius=6))
    img = Image.alpha_composite(img.convert("RGBA"), halo)
    img = Image.alpha_composite(img, dots).convert("RGB")

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    return path


def set_solid(shape, rgb):
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb
    shape.line.fill.background()


def paint_background(slide, rgb=BG, image: Path | None = None):
    if image is not None and image.exists():
        slide.shapes.add_picture(str(image), 0, 0, width=SLIDE_W, height=SLIDE_H)
    else:
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
    paint_background(slide, image=BG_IMG)

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
    paint_background(slide, image=BG_IMG)
    add_logo(slide, Inches(0.6), Inches(0.35), height=Inches(0.5))
    accent_bar(slide, top=Inches(1.1), left=Inches(0.6), width=Inches(0.7))

    add_text(slide, Inches(0.6), Inches(1.22), Inches(12), Inches(0.7),
             "Agenda", size=34, bold=True, color=TEXT, font=FONT_HEAD)
    add_text(slide, Inches(0.6), Inches(1.9), Inches(12), Inches(0.35),
             "JUNE 20, 2026  ·  INCUBA NEXT, KATRINEBJERG",
             size=11, color=TEXT_MUTED, font=FONT_MONO)

    # Two-track schedule from data/schedule.yaml + content/sessions/*.md
    # (time, kind, track1_title, track1_speaker, track2_title, track2_speaker)
    # kind: "talk" | "shared" — shared rows span both columns (breaks/plenary).
    rows = [
        ("09:00", "shared", "Breakfast & networking", "", "", ""),
        ("10:00", "talk",
            "WebAuthn: How to get rid of passwords.", "Joost van Dijk",
            "Kernel Wars: Anti-Cheat Reversing, BYOVD & Mitigations", "Ravshan Rikhsiev"),
        ("11:00", "talk",
            "Alert Fatigue Therapy: Fixing Broken Detection Rules", "Marvin Ngoma",
            "Remote Cold Execution", "Tom Kern"),
        ("11:45", "shared", "Lunch", "", "", ""),
        ("12:45", "talk",
            "We Scanned 10,000 Danish Orgs Without Sending a Single Packet", "Morten von Seelen",
            "Trustless Consensus Manipulation Through Bribing Contracts", "Bence Sooki-Toth"),
        ("13:50", "talk",
            "RTFM — When Documentation Creates Critical Misconfiguration", "Martin Sohn Christensen",
            "Emerging Frontiers: Ransomware Attacks in AI Systems", "Behnaz Karimi & Yuvaraj Govindarajulu"),
        ("14:50", "talk",
            "Build your own IDS", "Eleni Ioakeim",
            "Nebula — 5 years, still kicking *aaS", "Bleon Proko"),
        ("15:30", "shared", "Networking session", "", "", ""),
        ("16:30", "shared", "Continue at Fredagscaféen", "", "", ""),
    ]

    # Layout: time column | Track 1 | Track 2
    left_margin = Inches(0.6)
    time_w = Inches(1.05)
    gap = Inches(0.15)
    track_w = Inches((13.333 - 0.6 - 0.6 - 1.05 - 0.15 - 0.15) / 2)  # ~5.4"
    t1_left = left_margin + time_w + gap
    t2_left = t1_left + track_w + gap

    header_top = Inches(2.35)
    header_h = Inches(0.35)
    top = Inches(2.78)
    row_h = Inches(0.48)

    # Single ~15% opacity panel behind the entire agenda so dots stay visible.
    # Added BEFORE the headers/rows so it sits underneath them in z-order.
    panel_top = Inches(2.30)
    panel_h = Inches(0.50) + row_h * len(rows)
    panel = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left_margin, panel_top,
        Inches(13.333) - left_margin * 2, panel_h)
    panel.adjustments[0] = 0.02
    panel.fill.solid()
    panel.fill.fore_color.rgb = BG_CARD
    panel.line.fill.background()
    from pptx.oxml.ns import qn
    sppr = panel.fill._xPr
    solidFill = sppr.find(qn('a:solidFill'))
    srgb = solidFill.find(qn('a:srgbClr'))
    alpha = srgb.makeelement(qn('a:alpha'), {'val': '15000'})
    srgb.append(alpha)

    add_text(slide, t1_left, header_top, track_w, header_h,
             "TRACK 1  ·  ROOM 1", size=11, bold=True, color=ACCENT,
             font=FONT_MONO, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    add_text(slide, t2_left, header_top, track_w, header_h,
             "TRACK 2  ·  ROOM 2", size=11, bold=True, color=ACCENT,
             font=FONT_MONO, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

    for i, (t, kind, t1, s1, t2, s2) in enumerate(rows):
        y = top + row_h * i

        # Time column
        add_text(slide, left_margin, y, time_w, row_h,
                 t, size=14, color=ACCENT, font=FONT_MONO, bold=True,
                 anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)

        if kind == "shared":
            add_text(slide, t1_left, y,
                     Inches(13.333) - t1_left - left_margin, row_h,
                     t1, size=14, color=TEXT_MUTED, font=FONT_BODY, bold=False,
                     anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
            continue

        # Track 1
        _talk_cell(slide, t1_left, y, track_w, row_h, t1, s1)
        # Track 2
        _talk_cell(slide, t2_left, y, track_w, row_h, t2, s2)

    footer(slide, "Agenda")


def _talk_cell(slide, left, top, width, height, title, speaker):
    """Render a two-line talk cell: title (top) + speaker (bottom, muted)."""
    box = slide.shapes.add_textbox(left + Inches(0.15), top, width - Inches(0.3), height)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = 0
    tf.margin_top = Pt(2)
    tf.margin_bottom = Pt(2)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE

    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.LEFT
    r1 = p1.add_run()
    r1.text = title
    r1.font.name = FONT_BODY
    r1.font.size = Pt(11)
    r1.font.bold = True
    r1.font.color.rgb = TEXT

    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.LEFT
    r2 = p2.add_run()
    r2.text = speaker
    r2.font.name = FONT_MONO
    r2.font.size = Pt(9)
    r2.font.color.rgb = TEXT_MUTED


def build_section_divider(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    paint_background(slide, BG_ELEV, image=BG_IMG_ELEV)

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
    paint_background(slide, image=BG_IMG)
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
    paint_background(slide, image=BG_IMG)
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
    # Pre-render the dotted backgrounds (base + elevated tone for dividers).
    build_background(BG_IMG, base=(0x0A, 0x0A, 0x0F))
    build_background(BG_IMG_ELEV, base=(0x12, 0x12, 0x1A), glow_strength=0.18)

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
