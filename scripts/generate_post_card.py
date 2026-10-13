#!/usr/bin/env python3
"""
generate_post_card.py - High-Resolution Visual Architecture Summary Cards
Generates clean, premium, 1200x675 (16:9 LinkedIn standard) visual assets
summarizing the discussion topic for each post, without generic AI slop.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")
FONTS_DIR = r"C:\Windows\Fonts"

# Color Palette: Modern Dark Architecture Aesthetic
COLOR_BG = (15, 23, 42)          # Deep Slate #0f172a
COLOR_CARD_BG = (30, 41, 59)     # Slate 800 #1e293b
COLOR_CARD_BORDER = (51, 65, 85) # Slate 700 #334155
COLOR_TEXT_PRIMARY = (248, 250, 252) # Slate 50
COLOR_TEXT_MUTED = (148, 163, 184)   # Slate 400
COLOR_CYAN = (56, 189, 248)       # Sky/Cyan #38bdf8
COLOR_EMERALD = (52, 211, 153)    # Emerald #34d399
COLOR_AMBER = (251, 191, 36)      # Amber #fbbf24


def get_font(name="segoeuib.ttf", size=24):
    path = os.path.join(FONTS_DIR, name)
    if os.path.exists(path):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def create_post_02_card():
    """Generates Card for Post 02: Senior vs Architect: The 3 Core Shifts."""
    width, height = 1200, 675
    img = Image.new("RGB", (width, height), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Top Category Badge
    draw.rounded_rectangle([60, 45, 340, 80], radius=8, fill=(15, 45, 75), outline=COLOR_CYAN, width=1)
    f_badge = get_font("segoeuib.ttf", 15)
    draw.text((80, 52), "STAFF+ TECHNICAL LEADERSHIP", fill=COLOR_CYAN, font=f_badge)

    # Main Headline
    f_title = get_font("segoeuib.ttf", 36)
    draw.text((60, 105), "Senior Engineer vs. Software Architect", fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_subtitle = get_font("segoeui.ttf", 20)
    draw.text((60, 155), "The three non-obvious shifts when transitioning into Staff+ leadership:", fill=COLOR_TEXT_MUTED, font=f_subtitle)

    # Two Comparison Cards
    card_y = 205
    card_h = 360
    card_w = 515

    # Card 1: Senior Engineer
    c1_x = 60
    draw.rounded_rectangle([c1_x, card_y, c1_x + card_w, card_y + card_h], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=2)
    draw.rectangle([c1_x, card_y, c1_x + card_w, card_y + 8], fill=(100, 116, 139))
    
    f_card_hdr = get_font("segoeuib.ttf", 24)
    draw.text((c1_x + 30, card_y + 30), "Senior Engineer Focus", fill=(226, 232, 240), font=f_card_hdr)

    senior_points = [
        ("Core Metric:", "PR velocity & closing complex tickets"),
        ("Problem Scope:", "How to build it cleanly & efficiently"),
        ("Code Philosophy:", "Writing clever, highly performant code"),
        ("Stakeholders:", "Immediate engineering team & sprint goals")
    ]

    f_lbl = get_font("segoeuib.ttf", 17)
    f_val = get_font("segoeui.ttf", 17)
    py = card_y + 85
    for lbl, val in senior_points:
        draw.text((c1_x + 30, py), lbl, fill=COLOR_CYAN, font=f_lbl)
        draw.text((c1_x + 30, py + 26), val, fill=COLOR_TEXT_PRIMARY, font=f_val)
        py += 65

    # Card 2: Software Architect
    c2_x = 625
    draw.rounded_rectangle([c2_x, card_y, c2_x + card_w, card_y + card_h], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CYAN, width=2)
    draw.rectangle([c2_x, card_y, c2_x + card_w, card_y + 8], fill=COLOR_CYAN)

    draw.text((c2_x + 30, card_y + 30), "Software Architect Focus", fill=COLOR_CYAN, font=f_card_hdr)

    architect_points = [
        ("Core Metric:", "Bad code 40 engineers didn't write (ADRs)"),
        ("Problem Scope:", "Should we build it? What are the failure modes?"),
        ("Code Philosophy:", "Deleting moving parts so on-call can sleep"),
        ("Stakeholders:", "Execs, Product, Finance, & Engineering Leads")
    ]

    py = card_y + 85
    for lbl, val in architect_points:
        draw.text((c2_x + 30, py), lbl, fill=COLOR_EMERALD, font=f_lbl)
        draw.text((c2_x + 30, py + 26), val, fill=COLOR_TEXT_PRIMARY, font=f_val)
        py += 65

    # Footer Branding
    f_footer = get_font("segoeuib.ttf", 16)
    draw.text((60, 605), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_footer)
    f_footer_sub = get_font("segoeui.ttf", 15)
    draw.text((170, 606), "|  Senior Software Architect  •  Practical Architecture Insights", fill=COLOR_TEXT_MUTED, font=f_footer_sub)

    os.makedirs(ASSETS_DIR, exist_ok=True)
    out_path = os.path.join(ASSETS_DIR, "post_02_card.png")
    img.save(out_path, "PNG", quality=95)
    print(f"[+] Generated Post 02 summary card: {out_path}")
    return out_path


def create_post_03_card():
    """Generates Card for Post 03: Why RAG Pipelines Hallucinate in Production."""
    width, height = 1200, 675
    img = Image.new("RGB", (width, height), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Top Badge
    draw.rounded_rectangle([60, 45, 340, 80], radius=8, fill=(15, 50, 40), outline=COLOR_EMERALD, width=1)
    f_badge = get_font("segoeuib.ttf", 15)
    draw.text((80, 52), "PRACTICAL AI & SYSTEM ARCHITECTURE", fill=COLOR_EMERALD, font=f_badge)

    # Main Headline
    f_title = get_font("segoeuib.ttf", 36)
    draw.text((60, 105), "Why RAG Pipelines Hallucinate in Production", fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_subtitle = get_font("segoeui.ttf", 20)
    draw.text((60, 155), "The 3 silent failure modes between benchmark demos and live traffic:", fill=COLOR_TEXT_MUTED, font=f_subtitle)

    # 3 Summary Pillar Cards
    card_y = 205
    card_h = 360
    card_w = 338
    spacing = 33

    pillars = [
        {
            "num": "01",
            "title": "Naive Chunking",
            "color": COLOR_AMBER,
            "desc": "Splitting solely by token count cuts sentences in half and strips contextual headers.",
            "fix_lbl": "Production Fix:",
            "fix_val": "Semantic chunking with parent-document hierarchical retrieval."
        },
        {
            "num": "02",
            "title": "Cosine Trap",
            "color": COLOR_CYAN,
            "desc": "High vector similarity != answer relevance. Dense vectors easily match semantic fluff.",
            "fix_lbl": "Production Fix:",
            "fix_val": "Hybrid search (BM25 keyword + Vector) followed by a cross-encoder reranker."
        },
        {
            "num": "03",
            "title": "Zero Output Guardrails",
            "color": COLOR_EMERALD,
            "desc": "Passing unconstrained context directly to the LLM without schema or fact-checking.",
            "fix_lbl": "Production Fix:",
            "fix_val": "Strict JSON schema enforcement + citation verification before returning."
        }
    ]

    for i, p in enumerate(pillars):
        cx = 60 + i * (card_w + spacing)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=14, fill=COLOR_CARD_BG, outline=p["color"], width=2)
        draw.rectangle([cx, card_y, cx + card_w, card_y + 8], fill=p["color"])

        f_num = get_font("consola.ttf", 26)
        draw.text((cx + 25, card_y + 25), p["num"], fill=p["color"], font=f_num)

        f_hd = get_font("segoeuib.ttf", 22)
        draw.text((cx + 25, card_y + 65), p["title"], fill=COLOR_TEXT_PRIMARY, font=f_hd)

        f_desc = get_font("segoeui.ttf", 16)
        # Multiline text wrap for description
        lines = []
        words = p["desc"].split()
        cur = ""
        for w in words:
            test = cur + (" " if cur else "") + w
            if len(test) < 32:
                cur = test
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)

        dy = card_y + 110
        for l in lines:
            draw.text((cx + 25, dy), l, fill=COLOR_TEXT_MUTED, font=f_desc)
            dy += 24

        # Fix block
        draw.line([cx + 25, card_y + 225, cx + card_w - 25, card_y + 225], fill=COLOR_CARD_BORDER, width=1)
        f_flbl = get_font("segoeuib.ttf", 15)
        draw.text((cx + 25, card_y + 240), p["fix_lbl"], fill=p["color"], font=f_flbl)

        fix_lines = []
        cur = ""
        for w in p["fix_val"].split():
            test = cur + (" " if cur else "") + w
            if len(test) < 30:
                cur = test
            else:
                fix_lines.append(cur)
                cur = w
        if cur:
            fix_lines.append(cur)

        fy = card_y + 268
        for fl in fix_lines:
            draw.text((cx + 25, fy), fl, fill=COLOR_TEXT_PRIMARY, font=f_desc)
            fy += 24

    # Footer Branding
    f_footer = get_font("segoeuib.ttf", 16)
    draw.text((60, 605), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_footer)
    f_footer_sub = get_font("segoeui.ttf", 15)
    draw.text((170, 606), "|  Senior Software Architect  •  Practical Architecture Insights", fill=COLOR_TEXT_MUTED, font=f_footer_sub)

    os.makedirs(ASSETS_DIR, exist_ok=True)
    out_path = os.path.join(ASSETS_DIR, "post_03_card.png")
    img.save(out_path, "PNG", quality=95)
    print(f"[+] Generated Post 03 summary card: {out_path}")
    return out_path


def create_post_04_card():
    """Generates Card for Post 04: The 4-Section ADR Architecture Framework."""
    width, height = 1200, 675
    img = Image.new("RGB", (width, height), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Top Badge
    draw.rounded_rectangle([60, 45, 340, 80], radius=8, fill=(15, 45, 75), outline=COLOR_CYAN, width=1)
    f_badge = get_font("segoeuib.ttf", 15)
    draw.text((80, 52), "STAFF+ TECHNICAL LEADERSHIP", fill=COLOR_CYAN, font=f_badge)

    # Main Headline
    f_title = get_font("segoeuib.ttf", 36)
    draw.text((60, 105), "How to Write an ADR Executives Approve", fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_subtitle = get_font("segoeui.ttf", 20)
    draw.text((60, 155), "The 4-section Architecture Decision Record structure that eliminates endless committee debates:", fill=COLOR_TEXT_MUTED, font=f_subtitle)

    # 4 Quadrant / Grid Cards
    cards = [
        {"sec": "1. Context & Business Cost", "detail": "Frame in terms of revenue, latency SLA, or engineering risk—not just technical preference.", "color": COLOR_CYAN},
        {"sec": "2. Decision & Scope", "detail": "One declarative sentence stating the architectural direction with zero ambiguity.", "color": COLOR_EMERALD},
        {"sec": "3. Alternatives Rejected", "detail": "Explicitly explain why the 2 obvious alternatives were considered and rejected.", "color": COLOR_AMBER},
        {"sec": "4. Negative Consequences", "detail": "Acknowledge the trade-offs upfront. Builds instant credibility with CFOs and VPs.", "color": (244, 63, 94)}
    ]

    f_shd = get_font("segoeuib.ttf", 22)
    f_sdesc = get_font("segoeui.ttf", 17)

    card_coords = [
        (60, 205, 515, 160),
        (625, 205, 515, 160),
        (60, 395, 515, 160),
        (625, 395, 515, 160)
    ]

    for c_data, (x, y, w, h) in zip(cards, card_coords):
        draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=COLOR_CARD_BG, outline=c_data["color"], width=2)
        draw.rectangle([x, y, x + 6, y + h], fill=c_data["color"])

        draw.text((x + 25, y + 25), c_data["sec"], fill=c_data["color"], font=f_shd)

        # Wrap text
        words = c_data["detail"].split()
        lines = []
        cur = ""
        for wd in words:
            t = cur + (" " if cur else "") + wd
            if len(t) < 48:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)

        ly = y + 70
        for ln in lines:
            draw.text((x + 25, ly), ln, fill=COLOR_TEXT_PRIMARY, font=f_sdesc)
            ly += 26

    # Footer Branding
    f_footer = get_font("segoeuib.ttf", 16)
    draw.text((60, 605), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_footer)
    f_footer_sub = get_font("segoeui.ttf", 15)
    draw.text((170, 606), "|  Senior Software Architect  •  Practical Architecture Insights", fill=COLOR_TEXT_MUTED, font=f_footer_sub)

    os.makedirs(ASSETS_DIR, exist_ok=True)
    out_path = os.path.join(ASSETS_DIR, "post_04_card.png")
    img.save(out_path, "PNG", quality=95)
    print(f"[+] Generated Post 04 summary card: {out_path}")
    return out_path


def generate_all_cards():
    import sys
    sys.path.insert(0, HERE)
    from db_tracker import update_post_image

    repo_raw_base = "https://raw.githubusercontent.com/gtmsthi-ui/linkedin/main/my_account/assets"

    p2 = create_post_02_card()
    update_post_image(
        "post_02",
        p2,
        f"{repo_raw_base}/post_02_card.png",
        "Comparison Infographic: Senior Engineer vs Software Architect Focus & Metrics"
    )

    p3 = create_post_03_card()
    update_post_image(
        "post_03",
        p3,
        f"{repo_raw_base}/post_03_card.png",
        "Architecture Breakdown: The 3 Silent RAG Failure Modes in Production"
    )

    p4 = create_post_04_card()
    update_post_image(
        "post_04",
        p4,
        f"{repo_raw_base}/post_04_card.png",
        "Framework Grid: The 4-Section Architecture Decision Record (ADR) Structure"
    )


if __name__ == "__main__":
    generate_all_cards()
