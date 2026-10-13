#!/usr/bin/env python3
"""
generate_carousel_pdf.py - Automated LinkedIn Document Carousel (PDF) Generator
Generates high-engagement, 1080x1350 (4:5 portrait mobile standard) multi-page PDF slide decks
for LinkedIn carousel posts, based on newsletter editions and core architectural topics.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")
FONTS_DIR = r"C:\Windows\Fonts"

# Dimensions: LinkedIn 4:5 Mobile Portrait Carousel
W, H = 1080, 1350

# Modern Dark Architect Palette
COLOR_BG = (15, 23, 42)          # Deep Slate #0f172a
COLOR_CARD_BG = (30, 41, 59)     # Slate 800 #1e293b
COLOR_CARD_BORDER = (51, 65, 85) # Slate 700 #334155
COLOR_TEXT_PRIMARY = (248, 250, 252) # White/Slate 50
COLOR_TEXT_MUTED = (148, 163, 184)   # Slate 400
COLOR_TEXT_DIM = (100, 116, 139)     # Slate 500
COLOR_CYAN = (56, 189, 248)       # Sky #38bdf8
COLOR_EMERALD = (52, 211, 153)    # Emerald #34d399
COLOR_AMBER = (251, 191, 36)      # Amber #fbbf24


def get_font(name="segoeuib.ttf", size=32):
    path = os.path.join(FONTS_DIR, name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def draw_slide_chrome(draw, slide_num, total_slides, category="STAFF+ CAREER & LEADERSHIP"):
    """Draws top category badge, slide counter, and bottom author footer."""
    # Top Category Badge
    draw.rounded_rectangle([60, 60, 440, 105], radius=8, fill=(15, 45, 75), outline=COLOR_CYAN, width=1)
    f_badge = get_font("segoeuib.ttf", 16)
    draw.text((80, 72), category, fill=COLOR_CYAN, font=f_badge)

    # Top Right Slide Counter
    f_counter = get_font("consola.ttf", 22)
    counter_str = f"{slide_num:02d} / {total_slides:02d}"
    draw.text((W - 160, 72), counter_str, fill=COLOR_TEXT_MUTED, font=f_counter)

    # Bottom Branding Footer
    draw.line([60, H - 100, W - 60, H - 100], fill=COLOR_CARD_BORDER, width=1)
    f_brand = get_font("segoeuib.ttf", 18)
    draw.text((60, H - 75), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_brand)
    f_brand_sub = get_font("segoeui.ttf", 16)
    draw.text((180, H - 74), "| Senior Software Architect · The Pragmatic Architect", fill=COLOR_TEXT_MUTED, font=f_brand_sub)


def create_slide_1(total=6):
    """Cover Slide."""
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    draw_slide_chrome(draw, 1, total)

    # Main Big Hook Headline
    f_main = get_font("segoeuib.ttf", 64)
    lines = [
        "The Real Difference",
        "Between Senior Engineer",
        "& Software Architect"
    ]
    y = 280
    for l in lines:
        draw.text((60, y), l, fill=COLOR_TEXT_PRIMARY, font=f_main)
        y += 82

    # Accent decorative bar
    draw.rectangle([60, y + 20, 240, y + 26], fill=COLOR_CYAN)

    # Subtitle
    f_sub = get_font("segoeui.ttf", 28)
    sub_lines = [
        "Five years ago, I thought getting promoted meant",
        "writing the most clever code in the building.",
        "",
        "I was dead wrong. Here are the 3 non-obvious shifts",
        "when transitioning into Staff+ leadership:"
    ]
    sy = y + 60
    for sl in sub_lines:
        draw.text((60, sy), sl, fill=COLOR_TEXT_MUTED, font=f_sub)
        sy += 42

    # Bottom Call to Action box
    draw.rounded_rectangle([60, H - 240, W - 60, H - 140], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CYAN, width=2)
    f_cta = get_font("segoeuib.ttf", 24)
    draw.text((90, H - 200), "SWIPE TO EXPLORE THE 3 CORE SHIFTS  →", fill=COLOR_CYAN, font=f_cta)

    return img


def create_slide_2(total=6):
    """The Paradigm Flip."""
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    draw_slide_chrome(draw, 2, total)

    f_title = get_font("segoeuib.ttf", 46)
    draw.text((60, 160), "The Core Paradigm Flip", fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_sub = get_font("segoeui.ttf", 24)
    draw.text((60, 225), "As an architect, your primary metric inverts completely:", fill=COLOR_TEXT_MUTED, font=f_sub)

    # Box 1: Senior Engineer
    b1_y = 300
    b_h = 360
    draw.rounded_rectangle([60, b1_y, W - 60, b1_y + b_h], radius=16, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=2)
    draw.rectangle([60, b1_y, W - 60, b1_y + 8], fill=(100, 116, 139))
    
    f_bh = get_font("segoeuib.ttf", 28)
    draw.text((90, b1_y + 35), "Senior Engineer: Execution Superpower", fill=(226, 232, 240), font=f_bh)

    s_pts = [
        "• Your superpower is execution: close tickets, ship clean PRs.",
        "• Scope is tactical: how to build the feature fast & robustly.",
        "• Success is measured by output: lines of clean code and features."
    ]
    f_bp = get_font("segoeui.ttf", 22)
    py = b1_y + 100
    for p in s_pts:
        draw.text((90, py), p, fill=COLOR_TEXT_MUTED, font=f_bp)
        py += 60

    # Box 2: Software Architect
    b2_y = 700
    draw.rounded_rectangle([60, b2_y, W - 60, b2_y + b_h], radius=16, fill=COLOR_CARD_BG, outline=COLOR_CYAN, width=2)
    draw.rectangle([60, b2_y, W - 60, b2_y + 8], fill=COLOR_CYAN)

    draw.text((90, b2_y + 35), "Software Architect: Strategic Leverage", fill=COLOR_CYAN, font=f_bh)

    a_pts = [
        "• Your value is measured by the bad code 40 other engineers",
        "  DID NOT have to write because your ADR was clear.",
        "• Scope is strategic: failure modes, SLA risks, and maintenance cost.",
        "• Success is measured by stability: systems that run without pages."
    ]
    py = b2_y + 100
    for p in a_pts:
        draw.text((90, py), p, fill=COLOR_TEXT_PRIMARY, font=f_bp)
        py += 52

    # Bottom Callout
    draw.rounded_rectangle([60, 1100, W - 60, 1190], radius=12, fill=(15, 45, 75), outline=COLOR_CYAN, width=1)
    f_callout = get_font("segoeuib.ttf", 20)
    draw.text((90, 1130), "KEY TAKEAWAY: You trade execution speed for systemic leverage.", fill=COLOR_CYAN, font=f_callout)

    return img


def create_slide_3(total=6):
    """Shift 01: Trading IDE for Communication."""
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    draw_slide_chrome(draw, 3, total)

    f_num = get_font("consola.ttf", 32)
    draw.text((60, 160), "SHIFT 01", fill=COLOR_CYAN, font=f_num)

    f_title = get_font("segoeuib.ttf", 44)
    draw.text((60, 215), "Trading the IDE for Communication", fill=COLOR_TEXT_PRIMARY, font=f_title)

    # Narrative Card
    c_y = 310
    draw.rounded_rectangle([60, c_y, W - 60, c_y + 460], radius=16, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=2)
    
    narrative = [
        "If you can't explain why a distributed transaction is a bad",
        "idea in plain English to a Product Manager or CFO, your",
        "technical depth does not matter.",
        "",
        "As an Architect, 80% of your job is translation:",
        "",
        "• Translating business revenue goals into latency SLAs.",
        "• Translating technical debt into financial risk.",
        "• Writing Architecture Decision Records (ADRs) that non-engineers",
        "  can understand and approve without 6-week committee debates."
    ]
    f_p = get_font("segoeui.ttf", 23)
    ny = c_y + 40
    for n in narrative:
        color = COLOR_CYAN if n.startswith("•") else COLOR_TEXT_PRIMARY
        draw.text((90, ny), n, fill=color, font=f_p)
        ny += 38

    # Quote Box
    q_y = 810
    draw.rounded_rectangle([60, q_y, W - 60, q_y + 280], radius=16, fill=(20, 30, 48), outline=COLOR_CYAN, width=2)
    draw.rectangle([60, q_y, 70, q_y + 280], fill=COLOR_CYAN)
    
    f_qh = get_font("segoeuib.ttf", 24)
    draw.text((100, q_y + 40), "THE STAFF+ REALITY:", fill=COLOR_CYAN, font=f_qh)

    f_qp = get_font("segoeui.ttf", 26)
    q_lines = [
        "\"The best code you will write as an architect is",
        "often a 1-page document that aligns three teams",
        "before a single repository is created.\""
    ]
    qy = q_y + 90
    for ql in q_lines:
        draw.text((100, qy), ql, fill=COLOR_TEXT_PRIMARY, font=f_qp)
        qy += 44

    return img


def create_slide_4(total=6):
    """Shift 02: Best Architecture is Deleted Code."""
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    draw_slide_chrome(draw, 4, total)

    f_num = get_font("consola.ttf", 32)
    draw.text((60, 160), "SHIFT 02", fill=COLOR_EMERALD, font=f_num)

    f_title = get_font("segoeuib.ttf", 44)
    draw.text((60, 215), "The Best Architecture is the Code You Delete", fill=COLOR_TEXT_PRIMARY, font=f_title)

    # 3-Tier Hierarchy comparison
    c_y = 310
    c_h = 160
    tiers = [
        ("Junior Engineer", "Adds new libraries and external dependencies to solve problems quickly.", COLOR_AMBER),
        ("Senior Engineer", "Writes sophisticated custom logic, abstractions, and caching layers.", COLOR_CYAN),
        ("Software Architect", "Deletes moving parts, strips redundant layers, and simplifies contracts.", COLOR_EMERALD)
    ]

    ty = c_y
    for role, desc, col in tiers:
        draw.rounded_rectangle([60, ty, W - 60, ty + c_h], radius=14, fill=COLOR_CARD_BG, outline=col, width=2)
        draw.rectangle([60, ty, 70, ty + c_h], fill=col)

        f_rh = get_font("segoeuib.ttf", 24)
        draw.text((100, ty + 25), role, fill=col, font=f_rh)

        f_rd = get_font("segoeui.ttf", 21)
        draw.text((100, ty + 70), desc, fill=COLOR_TEXT_PRIMARY, font=f_rd)
        ty += 190

    # Summary callout
    draw.rounded_rectangle([60, 920, W - 60, 1180], radius=16, fill=(15, 50, 40), outline=COLOR_EMERALD, width=2)
    f_sh = get_font("segoeuib.ttf", 24)
    draw.text((90, 955), "WHY SIMPLICITY WINS IN PRODUCTION:", fill=COLOR_EMERALD, font=f_sh)

    f_sp = get_font("segoeui.ttf", 23)
    s_lines = [
        "Every additional service, queue, and abstraction is another failure mode.",
        "Your goal is not building a system only you can understand.",
        "Your goal is building a system so clean that the on-call engineer can",
        "sleep through the night."
    ]
    sy = 1005
    for sl in s_lines:
        draw.text((90, sy), sl, fill=COLOR_TEXT_PRIMARY, font=f_sp)
        sy += 36

    return img


def create_slide_5(total=6):
    """Shift 03: Consensus Beats Mandate."""
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    draw_slide_chrome(draw, 5, total)

    f_num = get_font("consola.ttf", 32)
    draw.text((60, 160), "SHIFT 03", fill=COLOR_AMBER, font=f_num)

    f_title = get_font("segoeuib.ttf", 44)
    draw.text((60, 215), "Consensus Beats Mandate Every Time", fill=COLOR_TEXT_PRIMARY, font=f_title)

    # Comparison Grid
    y_g = 310
    draw.rounded_rectangle([60, y_g, W - 60, y_g + 240], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=2)
    draw.rectangle([60, y_g, W - 60, y_g + 8], fill=(239, 68, 68)) # red
    
    f_gh = get_font("segoeuib.ttf", 24)
    draw.text((90, y_g + 30), "The Ivory Tower Trap (Mandates)", fill=(248, 113, 113), font=f_gh)
    
    m_lines = [
        "• Forcing architectural patterns by top-down executive decree.",
        "• Writing 40-page technical standards nobody actually follows.",
        "• Result: Underground engineering rebellions and friction."
    ]
    f_gp = get_font("segoeui.ttf", 21)
    my = y_g + 85
    for ml in m_lines:
        draw.text((90, my), ml, fill=COLOR_TEXT_MUTED, font=f_gp)
        my += 45

    # Bottom Grid: The Pragmatic Approach
    y_p = 590
    draw.rounded_rectangle([60, y_p, W - 60, y_p + 280], radius=14, fill=COLOR_CARD_BG, outline=COLOR_EMERALD, width=2)
    draw.rectangle([60, y_p, W - 60, y_p + 8], fill=COLOR_EMERALD)

    draw.text((90, y_p + 30), "The Pragmatic Architect Approach (Pull, Don't Push)", fill=COLOR_EMERALD, font=f_gh)

    p_lines = [
        "1. Build a working proof-of-concept (POC) solving a real bottleneck.",
        "2. Partner with one lead engineer to trial it on an active service.",
        "3. Share real metrics (50% latency drop, zero production incidents).",
        "4. Let team leads voluntarily pull the pattern into their codebases."
    ]
    py = y_p + 85
    for pl in p_lines:
        draw.text((90, py), pl, fill=COLOR_TEXT_PRIMARY, font=f_gp)
        py += 44

    # Bottom takeaway
    draw.rounded_rectangle([60, 910, W - 60, 1160], radius=14, fill=(30, 40, 60), outline=COLOR_CYAN, width=1)
    draw.text((90, 940), "THE LESSON:", fill=COLOR_CYAN, font=f_gh)
    
    t_lines = [
        "\"Engineers do not adopt standards because an architect",
        "told them to. They adopt standards because it makes",
        "their deploys safer and their on-call quieter.\""
    ]
    ty = 990
    for tl in t_lines:
        draw.text((90, ty), tl, fill=COLOR_TEXT_PRIMARY, font=get_font("segoeui.ttf", 24))
        ty += 42

    return img


def create_slide_6(total=6):
    """Checklist & Outro."""
    img = Image.new("RGB", (W, H), COLOR_BG)
    draw = ImageDraw.Draw(img)
    draw_slide_chrome(draw, 6, total)

    f_title = get_font("segoeuib.ttf", 46)
    draw.text((60, 160), "The Staff+ Architect Checklist", fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_sub = get_font("segoeui.ttf", 24)
    draw.text((60, 225), "4 mindset shifts to practice this week:", fill=COLOR_TEXT_MUTED, font=f_sub)

    # 4 Checklist items
    items = [
        ("1. Write the ADR First", "Document the context, decision, and rejected alternatives before opening an IDE."),
        ("2. Measure Systemic Risk", "Evaluate blast radius, recovery time, and observability—not just PR velocity."),
        ("3. Let Go of the Contribution Graph", "Your success is measured by team velocity and zero 3:00 AM pages."),
        ("4. Elevate the Engineers Around You", "A true Staff+ architect builds more architects, not dependents.")
    ]

    iy = 290
    for title, desc in items:
        draw.rounded_rectangle([60, iy, W - 60, iy + 145], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=2)
        draw.rectangle([60, iy, 70, iy + 145], fill=COLOR_CYAN)

        draw.text((100, iy + 22), title, fill=COLOR_CYAN, font=get_font("segoeuib.ttf", 24))
        draw.text((100, iy + 68), desc, fill=COLOR_TEXT_PRIMARY, font=get_font("segoeui.ttf", 20))
        iy += 170

    # Call to action & branding card
    draw.rounded_rectangle([60, 1000, W - 60, 1180], radius=16, fill=(15, 45, 75), outline=COLOR_CYAN, width=2)
    draw.text((90, 1030), "Join the Discussion on LinkedIn", fill=COLOR_TEXT_PRIMARY, font=get_font("segoeuib.ttf", 26))
    draw.text((90, 1075), "What was the hardest part of your transition from Senior to Staff+ Architect?", fill=COLOR_TEXT_MUTED, font=get_font("segoeui.ttf", 20))
    draw.text((90, 1120), "Connect & follow @Gautam Sethi for weekly enterprise architecture insights.", fill=COLOR_CYAN, font=get_font("segoeuib.ttf", 18))

    return img


def build_carousel_pdf():
    os.makedirs(ASSETS_DIR, exist_ok=True)
    slides = [
        create_slide_1(),
        create_slide_2(),
        create_slide_3(),
        create_slide_4(),
        create_slide_5(),
        create_slide_6()
    ]

    # Save individual high-res PNG previews for easy inspection
    for i, s in enumerate(slides, start=1):
        png_path = os.path.join(ASSETS_DIR, f"carousel_slide_{i}.png")
        s.save(png_path, "PNG", quality=95)

    # Save complete multi-page PDF slide deck
    pdf_path = os.path.join(ASSETS_DIR, "senior_vs_architect_carousel.pdf")
    slides[0].save(
        pdf_path,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=slides[1:]
    )

    print(f"[+] Successfully generated 6-slide PDF carousel: {pdf_path}")
    print(f"[+] PDF File Size: {os.path.getsize(pdf_path) / 1024:.1f} KB")
    return pdf_path


if __name__ == "__main__":
    build_carousel_pdf()
