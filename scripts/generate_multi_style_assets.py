#!/usr/bin/env python3
"""
generate_multi_style_assets.py - Multi-Format Visual Asset & Carousel Engine for LinkedIn
Breaks post visual monotony with 5 distinct architectural presentation styles:
1. Style A: 2-Box Comparison Grid (Naive Anti-Pattern vs Production Architecture)
2. Style B: 3-Stage Sequential Pipeline Flowchart (Ingest -> Route -> Verify)
3. Style C: SRE Metric & Benchmark Dashboard (Big bold stat callouts + SLA guarantees)
4. Style D: Architecture Decision Matrix / Cheat Sheet (Multi-row comparative guide)
5. Style E: 4:5 Mobile PDF Document Carousel (6-slide swipeable LinkedIn deck)
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")
FONTS_DIR = r"C:\Windows\Fonts"

# Standard Dimensions
W_CARD, H_CARD = 1200, 675   # 16:9 Landscape Card
W_PDF, H_PDF = 1080, 1350    # 4:5 Portrait Mobile Carousel

# Modern Cyber Obsidian & Technical Color Palette
COLOR_BG = (15, 23, 42)          # Deep Slate #0f172a
COLOR_CARD_BG = (30, 41, 59)     # Slate 800 #1e293b
COLOR_CARD_BORDER = (51, 65, 85) # Slate 700 #334155
COLOR_TEXT_PRIMARY = (248, 250, 252) # Slate 50
COLOR_TEXT_MUTED = (148, 163, 184)   # Slate 400
COLOR_TEXT_DIM = (100, 116, 139)     # Slate 500
COLOR_CYAN = (56, 189, 248)       # Sky/Cyan #38bdf8
COLOR_EMERALD = (52, 211, 153)    # Emerald #34d399
COLOR_AMBER = (251, 191, 36)      # Amber #fbbf24
COLOR_ROSE = (244, 63, 94)        # Rose #f43f5e
COLOR_PURPLE = (168, 85, 247)     # Violet #a855f7


def get_font(name="segoeuib.ttf", size=24, is_bold=False):
    candidates = []
    if FONTS_DIR and os.path.exists(FONTS_DIR):
        candidates.append(os.path.join(FONTS_DIR, name))

    is_bold_request = is_bold or ("b.ttf" in name.lower()) or ("bold" in name.lower())
    if is_bold_request:
        candidates.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
            r"C:\Windows\Fonts\segoeuib.ttf",
            r"C:\Windows\Fonts\arialbd.ttf",
        ])
    else:
        candidates.extend([
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
            r"C:\Windows\Fonts\segoeui.ttf",
            r"C:\Windows\Fonts\arial.ttf",
        ])

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()


# ==============================================================================
# STYLE A: 2-Box Comparison Grid (Flawed Approach vs Production Pattern)
# ==============================================================================
def render_style_comparison_grid(post_key, badge, headline, subtitle, box1_title, box1_lines, box2_title, box2_lines, out_name=None):
    img = Image.new("RGB", (W_CARD, H_CARD), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Category Badge
    badge_w = min(500, max(260, len(badge) * 11 + 40))
    draw.rounded_rectangle([60, 45, 60 + badge_w, 80], radius=8, fill=(15, 45, 75), outline=COLOR_CYAN, width=1)
    f_badge = get_font("segoeuib.ttf", 15)
    draw.text((80, 52), badge.upper(), fill=COLOR_CYAN, font=f_badge)

    # Headline & Subtitle
    f_title = get_font("segoeuib.ttf", 34)
    draw.text((60, 102), headline, fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_sub = get_font("segoeui.ttf", 20)
    draw.text((60, 155), subtitle, fill=COLOR_TEXT_MUTED, font=f_sub)

    card_y = 205
    card_h = 360
    card_w = 515

    # Box 1 (Amber / Flawed)
    c1_x = 60
    draw.rounded_rectangle([c1_x, card_y, c1_x + card_w, card_y + card_h], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=1)
    draw.line([(c1_x + 25, card_y + 65), (c1_x + card_w - 25, card_y + 65)], fill=COLOR_CARD_BORDER, width=1)
    f_hdr = get_font("segoeuib.ttf", 20)
    draw.text((c1_x + 30, card_y + 25), box1_title, fill=COLOR_AMBER, font=f_hdr)

    f_pt = get_font("segoeui.ttf", 16)
    y_pt = card_y + 85
    for pt in box1_lines[:5]:
        draw.ellipse([c1_x + 30, y_pt + 6, c1_x + 40, y_pt + 16], fill=COLOR_AMBER)
        draw.text((c1_x + 55, y_pt), pt, fill=COLOR_TEXT_PRIMARY, font=f_pt)
        y_pt += 52

    # Box 2 (Cyan / Production)
    c2_x = 625
    draw.rounded_rectangle([c2_x, card_y, c2_x + card_w, card_y + card_h], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CYAN, width=1)
    draw.line([(c2_x + 25, card_y + 65), (c2_x + card_w - 25, card_y + 65)], fill=COLOR_CARD_BORDER, width=1)
    draw.text((c2_x + 30, card_y + 25), box2_title, fill=COLOR_CYAN, font=f_hdr)

    y_pt = card_y + 85
    for pt in box2_lines[:5]:
        draw.ellipse([c2_x + 30, y_pt + 6, c2_x + 40, y_pt + 16], fill=COLOR_CYAN)
        draw.text((c2_x + 55, y_pt), pt, fill=COLOR_TEXT_PRIMARY, font=f_pt)
        y_pt += 52

    # Footer
    draw.line([(60, 585), (W_CARD - 60, 585)], fill=COLOR_CARD_BORDER, width=1)
    f_foot = get_font("segoeuib.ttf", 16)
    draw.text((60, 605), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_foot)
    f_sub = get_font("segoeui.ttf", 15)
    draw.text((170, 606), "|  AI Enthusiast  •  ZeroDrift Systems Group", fill=COLOR_TEXT_MUTED, font=f_sub)

    os.makedirs(ASSETS_DIR, exist_ok=True)
    out_path = os.path.join(ASSETS_DIR, out_name or f"{post_key}_card.png")
    img.save(out_path, "PNG", quality=95)
    return out_path


# ==============================================================================
# STYLE B: 3-Stage Sequential Pipeline Flowchart
# ==============================================================================
def render_style_pipeline_flow(post_key, badge, headline, subtitle, stages, out_name=None):
    """
    Renders 3 horizontal sequential pipeline nodes with arrow connectors:
    stages: list of 3 dicts: [{'num': '01', 'title': '...', 'badge': '...', 'points': [...]}, ...]
    """
    img = Image.new("RGB", (W_CARD, H_CARD), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Top Badge & Titles
    draw.rounded_rectangle([60, 45, 420, 80], radius=8, fill=(15, 50, 40), outline=COLOR_EMERALD, width=1)
    f_badge = get_font("segoeuib.ttf", 15)
    draw.text((80, 52), badge.upper(), fill=COLOR_EMERALD, font=f_badge)

    f_title = get_font("segoeuib.ttf", 34)
    draw.text((60, 102), headline, fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_sub = get_font("segoeui.ttf", 19)
    draw.text((60, 153), subtitle, fill=COLOR_TEXT_MUTED, font=f_sub)

    # 3 Pipeline Cards
    card_w = 330
    card_h = 365
    card_y = 200
    start_x = 60
    spacing = 45

    colors = [COLOR_CYAN, COLOR_EMERALD, COLOR_PURPLE]

    for i, s in enumerate(stages[:3]):
        cx = start_x + i * (card_w + spacing)
        c_accent = colors[i % len(colors)]

        # Box
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=14, fill=COLOR_CARD_BG, outline=c_accent, width=1)
        # Top Accent stripe
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 8], radius=8, fill=c_accent)

        # Step Number & Title
        f_step = get_font("segoeuib.ttf", 14)
        draw.text((cx + 25, card_y + 24), f"STAGE {s.get('num', f'0{i+1}')}", fill=c_accent, font=f_step)
        f_s_title = get_font("segoeuib.ttf", 20)
        draw.text((cx + 25, card_y + 48), s.get("title", ""), fill=COLOR_TEXT_PRIMARY, font=f_s_title)

        # Metric / SLA Pill
        if s.get("badge"):
            draw.rounded_rectangle([cx + 25, card_y + 90, cx + card_w - 25, card_y + 118], radius=6, fill=(15, 23, 42), outline=COLOR_CARD_BORDER, width=1)
            f_pill = get_font("segoeui.ttf", 13)
            draw.text((cx + 35, card_y + 95), s["badge"], fill=c_accent, font=f_pill)

        # Bullet Points
        f_desc = get_font("segoeui.ttf", 14)
        py = card_y + 138
        for pt in s.get("points", [])[:4]:
            draw.ellipse([cx + 25, py + 5, cx + 33, py + 13], fill=c_accent)
            draw.text((cx + 42, py), pt, fill=COLOR_TEXT_MUTED, font=f_desc)
            py += 44

        # Arrow connector to next node
        if i < 2:
            arrow_x = cx + card_w + 12
            arrow_y = card_y + (card_h // 2)
            draw.line([(arrow_x, arrow_y), (arrow_x + 20, arrow_y)], fill=COLOR_CYAN, width=2)
            draw.polygon([(arrow_x + 20, arrow_y - 6), (arrow_x + 28, arrow_y), (arrow_x + 20, arrow_y + 6)], fill=COLOR_CYAN)

    # Footer
    draw.line([(60, 585), (W_CARD - 60, 585)], fill=COLOR_CARD_BORDER, width=1)
    f_foot = get_font("segoeuib.ttf", 16)
    draw.text((60, 605), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_foot)
    draw.text((170, 606), "|  ZeroDrift Architecture Blueprint  •  https://gtmsthi-ui.github.io/Zerodrift", fill=COLOR_TEXT_MUTED, font=f_sub)

    os.makedirs(ASSETS_DIR, exist_ok=True)
    out_path = os.path.join(ASSETS_DIR, out_name or f"{post_key}_pipeline_card.png")
    img.save(out_path, "PNG", quality=95)
    return out_path


# ==============================================================================
# STYLE C: SRE Metric & Benchmark Dashboard Card
# ==============================================================================
def render_style_metric_dashboard(post_key, badge, headline, subtitle, metrics, key_takeaways, out_name=None):
    """
    Renders big bold numerical metric callouts + key architectural takeaways:
    metrics: list of 3 dicts: [{'val': '640ms', 'lbl': 'p99 Tail Latency', 'sub': '-84% reduction', 'color': COLOR_EMERALD}, ...]
    """
    img = Image.new("RGB", (W_CARD, H_CARD), COLOR_BG)
    draw = ImageDraw.Draw(img)

    # Top Category Badge
    draw.rounded_rectangle([60, 45, 380, 80], radius=8, fill=(35, 20, 55), outline=COLOR_PURPLE, width=1)
    f_badge = get_font("segoeuib.ttf", 15)
    draw.text((80, 52), badge.upper(), fill=COLOR_PURPLE, font=f_badge)

    f_title = get_font("segoeuib.ttf", 34)
    draw.text((60, 102), headline, fill=COLOR_TEXT_PRIMARY, font=f_title)
    f_sub = get_font("segoeui.ttf", 20)
    draw.text((60, 153), subtitle, fill=COLOR_TEXT_MUTED, font=f_sub)

    # 3 Big Metric Hero Cards
    m_y = 200
    m_h = 135
    m_w = 338
    spacing = 33
    start_x = 60

    for i, m in enumerate(metrics[:3]):
        mx = start_x + i * (m_w + spacing)
        c_box = m.get("color", COLOR_CYAN)

        draw.rounded_rectangle([mx, m_y, mx + m_w, m_y + m_h], radius=14, fill=COLOR_CARD_BG, outline=c_box, width=1)
        
        # Big Stat
        f_val = get_font("segoeuib.ttf", 44)
        draw.text((mx + 25, m_y + 16), m["val"], fill=c_box, font=f_val)

        # Label & Context
        f_lbl = get_font("segoeuib.ttf", 17)
        draw.text((mx + 25, m_y + 75), m["lbl"], fill=COLOR_TEXT_PRIMARY, font=f_lbl)
        f_sub_val = get_font("segoeui.ttf", 14)
        draw.text((mx + 25, m_y + 102), m.get("sub", ""), fill=COLOR_TEXT_MUTED, font=f_sub_val)

    # Lower Architectural Insights Panel
    p_y = 360
    p_h = 205
    draw.rounded_rectangle([60, p_y, W_CARD - 60, p_y + p_h], radius=14, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=1)
    
    f_p_hdr = get_font("segoeuib.ttf", 20)
    draw.text((90, p_y + 22), "PRODUCTION ARCHITECTURAL TAKEAWAYS", fill=COLOR_CYAN, font=f_p_hdr)

    f_pt = get_font("segoeui.ttf", 16)
    t_y = p_y + 65
    for t in key_takeaways[:3]:
        draw.ellipse([90, t_y + 6, 100, t_y + 16], fill=COLOR_EMERALD)
        draw.text((115, t_y), t, fill=COLOR_TEXT_PRIMARY, font=f_pt)
        t_y += 42

    # Footer
    draw.line([(60, 585), (W_CARD - 60, 585)], fill=COLOR_CARD_BORDER, width=1)
    f_foot = get_font("segoeuib.ttf", 16)
    draw.text((60, 605), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_foot)
    f_sub = get_font("segoeui.ttf", 15)
    draw.text((170, 606), "|  ZeroDrift Benchmark Audit  •  https://gtmsthi-ui.github.io/Zerodrift", fill=COLOR_TEXT_MUTED, font=f_sub)

    os.makedirs(ASSETS_DIR, exist_ok=True)
    out_path = os.path.join(ASSETS_DIR, out_name or f"{post_key}_metric_card.png")
    img.save(out_path, "PNG", quality=95)
    return out_path


# ==============================================================================
# STYLE D: 4:5 Mobile LinkedIn PDF Document Carousel (6-Slide Deck)
# ==============================================================================
def render_style_document_carousel(post_key, category, title, hook_subtitle, slides_content, out_name=None):
    """
    Renders a 6-slide 1080x1350 swipeable LinkedIn PDF Document Carousel:
    slides_content: list of 4 dicts for internal slides 2 to 5:
      [{'headline': '...', 'desc': '...', 'bullets': [...]}, ...]
    """
    images = []
    total_slides = 6

    def create_base_slide(slide_idx):
        img = Image.new("RGB", (W_PDF, H_PDF), (10, 14, 23))
        draw = ImageDraw.Draw(img)

        # Top Accent stripe
        draw.rectangle([0, 0, W_PDF, 8], fill=COLOR_CYAN)

        # Top Category & Counter
        f_badge = get_font("segoeuib.ttf", 16)
        draw.text((60, 45), category.upper(), fill=COLOR_CYAN, font=f_badge)
        f_num = get_font("segoeuib.ttf", 18)
        draw.text((W_PDF - 130, 45), f"{slide_idx:02d} / {total_slides:02d}", fill=COLOR_TEXT_MUTED, font=f_num)
        draw.line([(60, 80), (W_PDF - 60, 80)], fill=COLOR_CARD_BORDER, width=1)

        # Bottom Footer
        draw.line([(60, H_PDF - 90), (W_PDF - 60, H_PDF - 90)], fill=COLOR_CARD_BORDER, width=1)
        f_brand = get_font("segoeuib.ttf", 18)
        draw.text((60, H_PDF - 65), "Gautam Sethi", fill=COLOR_TEXT_PRIMARY, font=f_brand)
        f_sub = get_font("segoeui.ttf", 16)
        draw.text((180, H_PDF - 64), "| AI Enthusiast · The Pragmatic Architect", fill=COLOR_TEXT_MUTED, font=f_sub)

        return img, draw

    # ------------------ SLIDE 1: Cover ------------------
    s1, d1 = create_base_slide(1)
    f_cover_badge = get_font("segoeuib.ttf", 18)
    d1.rounded_rectangle([60, 240, 440, 290], radius=8, fill=(15, 45, 75), outline=COLOR_CYAN, width=1)
    d1.text((85, 253), "EXECUTIVE ARCHITECTURE GUIDE", fill=COLOR_CYAN, font=f_cover_badge)

    f_cover_title = get_font("segoeuib.ttf", 52)
    # Split title if long
    words = title.split()
    line1 = " ".join(words[:5])
    line2 = " ".join(words[5:11])
    line3 = " ".join(words[11:])
    d1.text((60, 340), line1, fill=COLOR_TEXT_PRIMARY, font=f_cover_title)
    if line2:
        d1.text((60, 410), line2, fill=COLOR_TEXT_PRIMARY, font=f_cover_title)
    if line3:
        d1.text((60, 480), line3, fill=COLOR_TEXT_PRIMARY, font=f_cover_title)

    f_cover_sub = get_font("segoeui.ttf", 26)
    d1.text((60, 580), hook_subtitle, fill=COLOR_TEXT_MUTED, font=f_cover_sub)

    # Swipe CTA
    d1.rounded_rectangle([60, 850, 420, 920], radius=12, fill=COLOR_CYAN)
    f_cta = get_font("segoeuib.ttf", 22)
    d1.text((95, 872), "SWIPE FOR BLUEPRINT →", fill=(10, 14, 23), font=f_cta)
    images.append(s1)

    # ------------------ SLIDES 2 to 5: Content ------------------
    for idx, sc in enumerate(slides_content[:4], start=2):
        s, d = create_base_slide(idx)
        
        f_s_hdr = get_font("segoeuib.ttf", 38)
        d.text((60, 160), sc.get("headline", ""), fill=COLOR_TEXT_PRIMARY, font=f_s_hdr)

        f_s_desc = get_font("segoeui.ttf", 22)
        d.text((60, 230), sc.get("desc", ""), fill=COLOR_TEXT_MUTED, font=f_s_desc)

        # Content Card
        c_y = 330
        c_h = 680
        d.rounded_rectangle([60, c_y, W_PDF - 60, c_y + c_h], radius=16, fill=COLOR_CARD_BG, outline=COLOR_CARD_BORDER, width=1)
        
        # Bullets
        f_b_hdr = get_font("segoeuib.ttf", 24)
        f_b_txt = get_font("segoeui.ttf", 20)
        by = c_y + 50
        for b in sc.get("bullets", [])[:4]:
            d.ellipse([100, by + 8, 116, by + 24], fill=COLOR_CYAN)
            if isinstance(b, tuple):
                d.text((135, by), b[0], fill=COLOR_CYAN, font=f_b_hdr)
                d.text((135, by + 34), b[1], fill=COLOR_TEXT_PRIMARY, font=f_b_txt)
                by += 125
            else:
                d.text((135, by + 4), str(b), fill=COLOR_TEXT_PRIMARY, font=f_b_txt)
                by += 90

        images.append(s)

    # ------------------ SLIDE 6: Summary & Outro ------------------
    s6, d6 = create_base_slide(6)
    f_s6_title = get_font("segoeuib.ttf", 46)
    d6.text((60, 240), "The Staff+ Architect's Summary", fill=COLOR_TEXT_PRIMARY, font=f_s6_title)

    f_s6_sub = get_font("segoeui.ttf", 24)
    d6.text((60, 320), "Key principles to apply in your production systems tomorrow:", fill=COLOR_TEXT_MUTED, font=f_s6_sub)

    # Summary box
    d6.rounded_rectangle([60, 410, W_PDF - 60, 880], radius=16, fill=COLOR_CARD_BG, outline=COLOR_EMERALD, width=2)
    f_sum = get_font("segoeui.ttf", 22)
    points = [
        "1. Never alter schemas or run unconstrained agent loops in-place.",
        "2. Enforce deterministic state gates, schemas, and 10% retry budgets.",
        "3. Cache semantic completions behind multi-tenant cryptographic keys.",
        "4. Quantify technical debt in financial risk ($) before executive reviews."
    ]
    sy = 460
    for p in points:
        d6.text((100, sy), p, fill=COLOR_TEXT_PRIMARY, font=f_sum)
        sy += 90

    # Hub CTA
    f_hub = get_font("segoeuib.ttf", 22)
    d6.text((60, 940), "Read the full research whitepaper library:", fill=COLOR_CYAN, font=f_hub)
    f_url = get_font("segoeuib.ttf", 26)
    d6.text((60, 980), "https://gtmsthi-ui.github.io/Zerodrift", fill=COLOR_TEXT_PRIMARY, font=f_url)

    images.append(s6)

    # Save multi-page PDF
    os.makedirs(ASSETS_DIR, exist_ok=True)
    out_pdf = os.path.join(ASSETS_DIR, out_name or f"{post_key}_carousel.pdf")
    first = images[0]
    first.save(out_pdf, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
    
    # Also save Slide 1 as PNG thumbnail for Buffer document thumbnail
    thumb_path = os.path.join(ASSETS_DIR, f"{post_key}_slide_1.png")
    first.save(thumb_path, "PNG", quality=95)

    print(f"[+] Generated 6-Slide Document Carousel PDF: {out_pdf}")
    return out_pdf, thumb_path
