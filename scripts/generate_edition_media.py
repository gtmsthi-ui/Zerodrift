#!/usr/bin/env python3
"""
generate_edition_media.py - Automated Media Engine for Newsletter Issues
Generates:
1. High-Resolution Cover Image (1280x720, Dark Architect Theme)
2. Companion PDF Field Manual (Multi-page 1080x1350 slide deck for LinkedIn document carousel)
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")
FONTS_DIR = r"C:\Windows\Fonts"

os.makedirs(ASSETS_DIR, exist_ok=True)

# Color Palette: Senior Architect Dark Theme
BG_COLOR = (15, 23, 42)          # Slate 900
CARD_BG = (30, 41, 59)          # Slate 800
BORDER_COLOR = (51, 65, 85)     # Slate 700
TEXT_WHITE = (248, 250, 252)    # White
TEXT_MUTED = (148, 163, 184)    # Slate 400
ACCENT_BLUE = (56, 189, 248)    # Sky 400
ACCENT_GREEN = (52, 211, 153)   # Emerald 400
ACCENT_AMBER = (251, 191, 36)   # Amber 400


def get_font(size, bold=False):
    font_file = "segoeuib.ttf" if bold else "segoeui.ttf"
    font_path = os.path.join(FONTS_DIR, font_file)
    if os.path.exists(font_path):
        try:
            return ImageFont.truetype(font_path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def generate_issue_02_cover():
    """Generates 1280x720 LinkedIn Newsletter Cover Banner"""
    w, h = 1280, 720
    img = Image.new("RGB", (w, h), color=BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Subtle background architectural grid
    for x in range(0, w, 40):
        draw.line([(x, 0), (x, h)], fill=(22, 33, 56), width=1)
    for y in range(0, h, 40):
        draw.line([(0, y), (w, y)], fill=(22, 33, 56), width=1)

    # Outer border accent
    draw.rectangle([20, 20, w - 20, h - 20], outline=BORDER_COLOR, width=2)

    # Top Tag
    f_tag = get_font(18, bold=True)
    draw.rectangle([60, 60, 460, 96], fill=(12, 74, 110), outline=ACCENT_BLUE, width=1)
    draw.text((80, 68), "THE PRAGMATIC ARCHITECT · ISSUE #2", fill=ACCENT_BLUE, font=f_tag)

    # Main Headline
    f_title = get_font(44, bold=True)
    draw.text((60, 130), "Zero-Downtime Database Architecture", fill=TEXT_WHITE, font=f_title)

    f_sub = get_font(26, bold=False)
    draw.text((60, 190), "The 3-Phase Expand/Contract Blueprint for High-Throughput Systems", fill=ACCENT_GREEN, font=f_sub)

    # 3 Phase Cards
    phases = [
        ("PHASE 1: EXPAND", "Additive Changes", "Add nullable columns, start dual-writes, read from old schema.", ACCENT_BLUE),
        ("PHASE 2: MIGRATE", "Background Backfill", "Batched async worker copies historical data with zero table locks.", ACCENT_AMBER),
        ("PHASE 3: CONTRACT", "Safe Deprecation", "Switch reads to new schema, drop dual-writes, safely prune old column.", ACCENT_GREEN)
    ]

    card_y = 260
    card_w = 360
    card_h = 320

    for i, (p_title, p_sub, p_desc, p_accent) in enumerate(phases):
        card_x = 60 + i * (card_w + 30)
        draw.rectangle([card_x, card_y, card_x + card_w, card_y + card_h], fill=CARD_BG, outline=BORDER_COLOR, width=2)
        draw.rectangle([card_x, card_y, card_x + card_w, card_y + 8], fill=p_accent)

        f_card_title = get_font(20, bold=True)
        draw.text((card_x + 20, card_y + 25), p_title, fill=p_accent, font=f_card_title)

        f_card_sub = get_font(16, bold=True)
        draw.text((card_x + 20, card_y + 55), p_sub, fill=TEXT_WHITE, font=f_card_sub)

        # Word-wrapped description
        f_desc = get_font(16, bold=False)
        words = p_desc.split()
        lines = []
        cur = []
        for word in words:
            if len(" ".join(cur + [word])) < 34:
                cur.append(word)
            else:
                lines.append(" ".join(cur))
                cur = [word]
        if cur:
            lines.append(" ".join(cur))

        for l_idx, line in enumerate(lines):
            draw.text((card_x + 20, card_y + 105 + l_idx * 26), line, fill=TEXT_MUTED, font=f_desc)

    # Footer
    f_footer = get_font(18, bold=True)
    draw.text((60, 640), "By Gautam Sethi · AI Enthusiast & Systems Architect", fill=TEXT_WHITE, font=f_footer)
    draw.text((w - 440, 640), "linkedin.com/newsletters/the-pragmatic-architect", fill=ACCENT_BLUE, font=get_font(16))

    out_path = os.path.join(ASSETS_DIR, "newsletter_issue_02_cover.png")
    img.save(out_path, "PNG", quality=95)
    print(f"[+] Cover banner generated: {out_path}")
    return out_path


def generate_issue_02_pdf():
    """Generates a 4-Slide PDF Companion Field Manual (1080x1350) for LinkedIn Document Carousels"""
    w, h = 1080, 1350
    slides = []

    slide_data = [
        {
            "tag": "EXECUTIVE FIELD MANUAL · ISSUE #2",
            "title": "Zero-Downtime Database Architecture",
            "subtitle": "How Staff+ Engineers evolve production schemas on 80M+ row tables without table locks or 504 timeouts.",
            "points": [
                "• The ALTER TABLE trap: Why naive migrations exhaust connection pools",
                "• The 3-phase Expand/Contract state transition blueprint",
                "• Shadow verification & CDC-driven dual-writing",
                "• Safe backfill worker batching without replication lag spikes"
            ]
        },
        {
            "tag": "PHASE 1: THE EXPAND PHASE",
            "title": "Additive Changes & Dual-Writes",
            "subtitle": "Never mutate existing columns in-place. Decouple storage expansion from read logic.",
            "points": [
                "1. Add new column as NULLABLE (Zero exclusive lock duration).",
                "2. Application starts Dual-Writing: Write to (Old + New).",
                "3. Read path remains 100% on the Old column.",
                "4. If deployment fails, instant zero-loss rollback is guaranteed."
            ]
        },
        {
            "tag": "PHASE 2: THE BACKFILL & SHADOW READ",
            "title": "Batched Async Backfill with WAL Throttling",
            "subtitle": "Migrating millions of historical records without starving OLTP write capacity.",
            "points": [
                "1. Background worker iterates by Primary Key in bounded batches (5,000 rows).",
                "2. Dynamic sleep intervals based on replica replication lag (<10ms target).",
                "3. Shadow Reads: Compare Old vs New outputs asynchronously in memory.",
                "4. Emit metric alerts on schema divergence before flipping the read switch."
            ]
        },
        {
            "tag": "PHASE 3: THE CONTRACT & CLEANUP",
            "title": "Cutover & Safe Schema Teardown",
            "subtitle": "Finalizing the state transition and safely reclaiming database overhead.",
            "points": [
                "1. Flip read traffic 100% to the New column via feature flag.",
                "2. Remove Dual-Write logic from code (Write only to New).",
                "3. Soak in production for 72 hours under peak traffic.",
                "4. Drop old column during scheduled low-traffic window."
            ]
        }
    ]

    for s_idx, data in enumerate(slide_data, 1):
        img = Image.new("RGB", (w, h), color=BG_COLOR)
        draw = ImageDraw.Draw(img)

        # Background grid
        for x in range(0, w, 50):
            draw.line([(x, 0), (x, h)], fill=(22, 33, 56), width=1)
        for y in range(0, h, 50):
            draw.line([(0, y), (w, y)], fill=(22, 33, 56), width=1)

        # Border
        draw.rectangle([30, 30, w - 30, h - 30], outline=BORDER_COLOR, width=2)

        # Header Pill
        draw.rectangle([80, 80, 680, 130], fill=(12, 74, 110), outline=ACCENT_BLUE, width=1)
        draw.text((100, 93), data["tag"], fill=ACCENT_BLUE, font=get_font(22, bold=True))

        # Slide Number
        draw.text((w - 180, 93), f"SLIDE {s_idx}/4", fill=TEXT_MUTED, font=get_font(22, bold=True))

        # Title
        f_title = get_font(52, bold=True)
        draw.text((80, 180), data["title"], fill=TEXT_WHITE, font=f_title)

        # Subtitle
        f_sub = get_font(26, bold=False)
        words = data["subtitle"].split()
        sub_lines = []
        cur = []
        for word in words:
            if len(" ".join(cur + [word])) < 48:
                cur.append(word)
            else:
                sub_lines.append(" ".join(cur))
                cur = [word]
        if cur:
            sub_lines.append(" ".join(cur))

        for l_idx, line in enumerate(sub_lines):
            draw.text((80, 270 + l_idx * 38), line, fill=ACCENT_GREEN, font=f_sub)

        # Content Card
        card_top = 400
        card_h = 750
        draw.rectangle([80, card_top, w - 80, card_top + card_h], fill=CARD_BG, outline=BORDER_COLOR, width=2)
        draw.rectangle([80, card_top, w - 80, card_top + 10], fill=ACCENT_BLUE)

        f_point = get_font(30, bold=False)
        for p_idx, pt in enumerate(data["points"]):
            pt_y = card_top + 60 + p_idx * 160
            # Wrap long points
            p_words = pt.split()
            p_lines = []
            c_w = []
            for w_item in p_words:
                if len(" ".join(c_w + [w_item])) < 42:
                    c_w.append(w_item)
                else:
                    p_lines.append(" ".join(c_w))
                    c_w = [w_item]
            if c_w:
                p_lines.append(" ".join(c_w))

            for li, pline in enumerate(p_lines):
                draw.text((120, pt_y + li * 42), pline, fill=TEXT_WHITE if li == 0 else TEXT_MUTED, font=f_point)

        # Footer
        draw.text((80, h - 80), "The Pragmatic Architect · By Gautam Sethi", fill=TEXT_MUTED, font=get_font(22, bold=True))
        draw.text((w - 380, h - 80), "Downloadable PDF Edition", fill=ACCENT_BLUE, font=get_font(22, bold=False))

        slides.append(img)

    pdf_path = os.path.join(ASSETS_DIR, "Zero_Downtime_Database_Architecture_Field_Manual.pdf")
    slides[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=slides[1:])
    print(f"[+] Companion PDF Field Manual generated: {pdf_path}")
    return pdf_path


def main():
    print("=" * 60)
    print(" Generating Rich Media for Newsletter Issue #2")
    print("=" * 60)
    generate_issue_02_cover()
    generate_issue_02_pdf()
    print("=" * 60)
    print(" Done! Media assets ready to attach.")


if __name__ == "__main__":
    main()

