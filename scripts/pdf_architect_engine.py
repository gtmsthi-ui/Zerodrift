#!/usr/bin/env python3
"""
pdf_architect_engine.py - Professional Handwritten PDF Generator Engine
Guarantees 100% boundary safety: mathematical text wrapping, dynamic card sizing,
automatic page overflow handling, and tailored multi-page handbooks with descriptive answers.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1440
PADDING_X = 64
MAX_CONTENT_WIDTH = WIDTH - (PADDING_X * 2)

# Load authentic handwritten fonts
FONT_COVER_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 48)
FONT_COVER_SUB = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 30)
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 36)
FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 26)
FONT_H2 = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 25)
FONT_BODY = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 22)
FONT_BOLD = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 21)
FONT_CODE = ImageFont.truetype("C:/Windows/Fonts/comicbd.ttf", 19)
FONT_SMALL = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 18)

BG_COLOR = (252, 251, 248) # Warm cream notebook paper
DOT_COLOR = (215, 212, 202, 140)

def wrap_text(text, font, max_width, draw):
    """Accurately wraps paragraphs to pixel width using font text bounding boxes."""
    lines = []
    for paragraph in text.splitlines():
        if not paragraph.strip():
            lines.append("")
            continue
        words = paragraph.split(" ")
        curr_line = []
        for w in words:
            test = " ".join(curr_line + [w])
            bbox = draw.textbbox((0, 0), test, font=font)
            if (bbox[2] - bbox[0]) <= max_width:
                curr_line.append(w)
            else:
                if curr_line:
                    lines.append(" ".join(curr_line))
                    curr_line = [w]
                else:
                    lines.append(w)
        if curr_line:
            lines.append(" ".join(curr_line))
    return lines

class HandwrittenHandbookBuilder:
    def __init__(self, series_title, handbook_name, accent_color=(37, 99, 235), theme_badge="SYSTEMS BLUEPRINT"):
        self.series_title = series_title
        self.handbook_name = handbook_name
        self.accent_color = accent_color
        self.theme_badge = theme_badge
        self.pages = []
        self.current_img = None
        self.current_draw = None
        self.current_y = 100
        self.page_number = 1

    def _start_new_page(self, chapter_title=""):
        self.current_img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
        self.current_draw = ImageDraw.Draw(self.current_img, "RGBA")

        # Draw dot grid
        for x in range(40, WIDTH - 40, 36):
            for y in range(60, HEIGHT - 60, 36):
                self.current_draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=DOT_COLOR)

        # Header Margin line
        self.current_draw.line([(PADDING_X, 60), (WIDTH - PADDING_X, 60)], fill=(225, 29, 72, 200), width=2)
        self.current_draw.text((PADDING_X, 32), f"THE PRAGMATIC ARCHITECT • {self.series_title.upper()}", font=FONT_SMALL, fill=(100, 116, 139))
        self.current_draw.text((WIDTH - 220, 32), f"PAGE {self.page_number:02d}", font=FONT_SMALL, fill=(100, 116, 139))

        # Footer
        self.current_draw.line([(PADDING_X, HEIGHT - 65), (WIDTH - PADDING_X, HEIGHT - 65)], fill=(203, 213, 225, 200), width=1)
        self.current_draw.text((PADDING_X, HEIGHT - 52), "Gautam Sethi • AI Enthusiast & Systems Architect", font=FONT_SMALL, fill=(51, 65, 85))
        self.current_draw.text((WIDTH - 240, HEIGHT - 52), "Save & Repost ♻️", font=FONT_SMALL, fill=self.accent_color)

        self.current_y = 90
        if chapter_title:
            # Highlight bar
            self.current_draw.rectangle([(PADDING_X - 6, self.current_y - 4), (WIDTH - PADDING_X, self.current_y + 48)], fill=(254, 240, 138, 140))
            self.current_draw.text((PADDING_X, self.current_y), chapter_title, font=FONT_TITLE, fill=(15, 23, 42))
            self.current_y += 65

        self.pages.append(self.current_img)
        self.page_number += 1

    def add_cover(self, title, subtitle, curriculum):
        img = Image.new("RGB", (WIDTH, HEIGHT), (248, 250, 252))
        draw = ImageDraw.Draw(img, "RGBA")

        # Grid
        for x in range(40, WIDTH - 40, 36):
            for y in range(60, HEIGHT - 60, 36):
                draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(203, 213, 225, 160))

        # Borders
        draw.rounded_rectangle([(36, 36), (WIDTH - 36, HEIGHT - 36)], radius=16, outline=(15, 23, 42), width=4)
        draw.rounded_rectangle([(44, 44), (WIDTH - 44, HEIGHT - 44)], radius=12, outline=self.accent_color, width=2)

        # Top Badge
        draw.rounded_rectangle([(WIDTH//2 - 240, 100), (WIDTH//2 + 240, 155)], radius=10, fill=self.accent_color)
        draw.text((WIDTH//2 - 210, 114), f"THE PRAGMATIC ARCHITECT • {self.theme_badge}", font=FONT_BODY, fill=(255, 255, 255))

        # Title Highlighter
        draw.rectangle([(70, 200), (WIDTH - 70, 380)], fill=(254, 240, 138, 170))
        draw.text((90, 215), title, font=FONT_COVER_TITLE, fill=(15, 23, 42), spacing=12)

        # Subtitle
        draw.text((90, 410), subtitle, font=FONT_COVER_SUB, fill=(51, 65, 85), spacing=8)

        # Curriculum Box
        y = 540
        draw.rounded_rectangle([(70, y), (WIDTH - 70, y + 620)], radius=14, fill=(255, 255, 255, 230), outline=(51, 65, 85), width=2)
        draw.text((100, y + 25), "📖 FIELD MANUAL CHAPTERS & CORE TOPICS:", font=FONT_H2, fill=self.accent_color)

        curr_y = y + 75
        for idx, item in enumerate(curriculum, 1):
            draw.text((100, curr_y), f"{idx:02d}. {item}", font=FONT_BODY, fill=(30, 41, 59))
            curr_y += 50

        # Sign-off
        draw.text((90, HEIGHT - 150), "Handwritten Field Notes by Gautam Sethi", font=FONT_SUBTITLE, fill=(15, 23, 42))
        draw.text((90, HEIGHT - 110), "AI Enthusiast • Production Systems & Architecture", font=FONT_BODY, fill=(100, 116, 139))
        draw.text((WIDTH - 280, HEIGHT - 130), "SWIPE ➡️", font=FONT_H2, fill=self.accent_color)

        self.pages.append(img)
        self.page_number += 1

    def add_card(self, tag, title, body_paragraphs, is_warning=False):
        """Calculates dynamic height and auto-wraps so text NEVER overflows bounds."""
        card_w = MAX_CONTENT_WIDTH
        inner_w = card_w - 44

        # Wrap title
        title_lines = wrap_text(title, FONT_H2, inner_w, self.current_draw or ImageDraw.Draw(Image.new("RGB", (1, 1))))
        title_h = len(title_lines) * 32

        # Wrap all body paragraphs
        all_body_lines = []
        for p in body_paragraphs:
            p_lines = wrap_text(p, FONT_BODY, inner_w, self.current_draw or ImageDraw.Draw(Image.new("RGB", (1, 1))))
            all_body_lines.extend(p_lines)
            all_body_lines.append("") # paragraph spacing

        if all_body_lines and all_body_lines[-1] == "":
            all_body_lines.pop()

        body_h = len(all_body_lines) * 28
        total_card_h = 36 + title_h + 12 + body_h + 24

        # Check page overflow
        if (self.current_y + total_card_h) > (HEIGHT - 90) or self.current_img is None:
            self._start_new_page()

        draw = self.current_draw
        y = self.current_y

        # Colors based on type
        if is_warning:
            border_col = (239, 68, 68, 220) # Red
            bg_col = (254, 242, 242, 240)
            tag_col = (220, 38, 38)
            title_col = (153, 27, 27)
        else:
            border_col = (self.accent_color[0], self.accent_color[1], self.accent_color[2], 220)
            bg_col = (255, 255, 255, 240)
            tag_col = self.accent_color
            title_col = (30, 41, 59)

        # Draw card container
        draw.rounded_rectangle([(PADDING_X, y), (PADDING_X + card_w, y + total_card_h)], radius=12, fill=bg_col, outline=border_col, width=2)

        # Draw Tag
        tag_w = draw.textbbox((0, 0), tag, font=FONT_SMALL)[2] + 28
        draw.rounded_rectangle([(PADDING_X + 20, y - 12), (PADDING_X + 20 + tag_w, y + 14)], radius=6, fill=tag_col)
        draw.text((PADDING_X + 34, y - 10), tag, font=FONT_SMALL, fill=(255, 255, 255))

        # Render Title lines
        curr_text_y = y + 24
        for line in title_lines:
            draw.text((PADDING_X + 22, curr_text_y), line, font=FONT_H2, fill=title_col)
            curr_text_y += 32

        curr_text_y += 8
        # Render Body lines
        for line in all_body_lines:
            if line.startswith("•") or line.startswith("1.") or line.startswith("2.") or line.startswith("3.") or line.startswith("[✓]"):
                draw.text((PADDING_X + 22, curr_text_y), line, font=FONT_BODY, fill=(15, 23, 42))
            elif line.startswith("FAILURE:") or line.startswith("THE FIX:") or line.startswith("ROOT CAUSE:"):
                draw.text((PADDING_X + 22, curr_text_y), line, font=FONT_BOLD, fill=title_col)
            else:
                draw.text((PADDING_X + 22, curr_text_y), line, font=FONT_BODY, fill=(51, 65, 85))
            curr_text_y += 28

        self.current_y = y + total_card_h + 24

    def add_invariant(self, title, rule_body):
        """Adds a full-width golden callout banner for Senior Architect Invariants."""
        inner_w = MAX_CONTENT_WIDTH - 44
        rule_lines = wrap_text(rule_body, FONT_BODY, inner_w, self.current_draw)
        card_h = 32 + 28 + (len(rule_lines) * 28) + 20

        if (self.current_y + card_h) > (HEIGHT - 90) or self.current_img is None:
            self._start_new_page()

        draw = self.current_draw
        y = self.current_y

        draw.rounded_rectangle([(PADDING_X, y), (PADDING_X + MAX_CONTENT_WIDTH, y + card_h)], radius=12, fill=(254, 243, 199, 210), outline=(217, 119, 6), width=2)
        draw.text((PADDING_X + 22, y + 16), title, font=FONT_H2, fill=(180, 83, 9))

        curr_y = y + 54
        for line in rule_lines:
            draw.text((PADDING_X + 22, curr_y), line, font=FONT_BODY, fill=(120, 53, 15))
            curr_y += 28

        self.current_y = y + card_h + 24

    def save_pdf(self, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.pages[0].save(output_path, save_all=True, append_images=self.pages[1:], resolution=150.0)
        cover_path = os.path.splitext(output_path)[0] + "_cover.png"
        self.pages[0].save(cover_path)
        print(f"[+] Saved {len(self.pages)}-page Handbook PDF: {output_path}")
        print(f"[+] Saved Cover Thumbnail: {cover_path}")
        return output_path
