#!/usr/bin/env python3
"""
render_article_video.py - 100% Automated 60-Second Video Generator
Converts any newsletter article or technical script into an MP4 video with:
  1. Professional Dark-Theme 9:16 Vertical Video Slides (1080x1920)
  2. Synthesized Technical Voice Narration (gTTS / MoviePy)
  3. Dynamic Scene Transitions & Lower-Third Graphic Directives
  4. Ready to publish directly to LinkedIn Video / YouTube Shorts / Reels
"""

import os
import sys
import re
from PIL import Image, ImageDraw, ImageFont
import gtts
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "my_account", "videos")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# 5 Visual Scenes matching the 60-second video directives
SCENES = [
    {
        "id": 1,
        "tag": "CRITICAL ARCHITECTURE INCIDENT",
        "tag_color": "#EF4444",
        "title": "The Silent Failure in\\nSemantic Caching",
        "subtitle": "Why 0.88 Cosine Similarity Destroys Enterprise SLAs",
        "points": [
            "• Naive vector stores assume semantic proximity equals authorization.",
            "• 0.94 similarity matches queries across completely different tenants.",
            "• Result: Private enterprise policy text leaks to external users."
        ],
        "speech": "The most expensive optimization in production AI systems is the one that looks flawless in staging. Here is the silent failure mode that destroys enterprise SLAs under concurrency."
    },
    {
        "id": 2,
        "tag": "THE ROOT CAUSE",
        "tag_color": "#F59E0B",
        "title": "The 500ms Invalidation Race",
        "subtitle": "Approximate Nearest Neighbor Graphs Cannot Re-index in Real Time",
        "points": [
            "• When a source document updates in Postgres, vector embeddings lag.",
            "• In-flight read queries hit un-evicted graph clusters.",
            "• Your inference gateway continues serving stale hallucinations for minutes."
        ],
        "speech": "Most teams look at prompt engineering. But the real issue is event-driven invalidation. When source records mutate, in-flight queries continue serving stale hallucinations."
    },
    {
        "id": 3,
        "tag": "THE PRODUCTION TOPOLOGY",
        "tag_color": "#3B82F6",
        "title": "The Partitioned\\nCompound Key",
        "subtitle": "Cryptographic Isolation + Sub-50ms CDC Purging",
        "points": [
            "• Key: SHA256(Tenant ID + Role Clearance + Routing Tier)",
            "• Tier 1: Sub-2ms exact Redis hash ring for high-volume identical queries.",
            "• Tier 2: Dynamic similarity gates (0.96 for facts, 0.86 for conversation)."
        ],
        "speech": "Here is the production-safe standard we built in the AEM Reliability Toolkit: We isolate tenant memory cryptographically, enforce dynamic similarity gates, and trigger event-driven purges."
    },
    {
        "id": 4,
        "tag": "CHANGE DATA CAPTURE (CDC)",
        "tag_color": "#10B981",
        "title": "Sub-50ms Global Cache Eviction",
        "subtitle": "Debezium + Kafka Event-Driven Invalidation Vectors",
        "points": [
            "• Every cached item records source document SHA256 fingerprints.",
            "• Debezium streams database mutations instantly to Redis invalidation keys.",
            "• Optimistic gateway read checks evict stale cache before returning."
        ],
        "speech": "We connect database mutations directly to Kafka and Redis. Stale entries are evicted within 50 milliseconds before in-flight queries complete."
    },
    {
        "id": 5,
        "tag": "THE PRAGMATIC ARCHITECT",
        "tag_color": "#8B5CF6",
        "title": "Full Field Manual &\\nOpen-Source Code",
        "subtitle": "Issue #6 Live on LinkedIn Newsletters",
        "points": [
            "• Read the complete 4-slide field manual in The Pragmatic Architect.",
            "• Open-source audit scripts available at github.com/gtmsthi-ui/aem-reliability-toolkit.",
            "• Subscribe on LinkedIn for weekly enterprise systems blueprints."
        ],
        "speech": "I have published the complete 4-slide field manual and open-source verification scripts. Read the deep-dive in The Pragmatic Architect newsletter at the link below."
    }
]


def render_scene_slide(scene, out_path):
    W, H = 1080, 1920
    img = Image.new("RGB", (W, H), color="#0B0F19")
    draw = ImageDraw.Draw(img)

    # Frame border & accents
    draw.rectangle([(40, 40), (W - 40, H - 40)], outline="#1E293B", width=3)
    draw.rectangle([(40, 40), (W - 40, 52)], fill=scene["tag_color"])

    try:
        f_badge = ImageFont.truetype("arialbd.ttf", 26)
        f_title = ImageFont.truetype("arialbd.ttf", 64)
        f_sub = ImageFont.truetype("arial.ttf", 34)
        f_bullet = ImageFont.truetype("arial.ttf", 32)
        f_author = ImageFont.truetype("arialbd.ttf", 28)
    except Exception:
        f_badge = f_title = f_sub = f_bullet = f_author = ImageFont.load_default()

    # Pill badge
    draw.rectangle([(80, 120), (560, 180)], fill="#1E293B", outline=scene["tag_color"], width=2)
    draw.text((105, 134), scene["tag"], fill=scene["tag_color"], font=f_badge)

    # Title & Subtitle
    title_text = scene["title"].replace("\\n", "\n")
    draw.text((80, 240), title_text, fill="#FFFFFF", font=f_title, spacing=16)
    draw.text((80, 440), scene["subtitle"], fill="#94A3B8", font=f_sub)

    # Divider
    draw.line([(80, 530), (W - 80, 530)], fill="#334155", width=2)

    # Architectural Card Container
    card_top = 580
    card_bottom = 1580
    draw.rectangle([(80, card_top), (W - 80, card_bottom)], fill="#111827", outline="#1E293B", width=2)

    # Card header bar
    draw.rectangle([(80, card_top), (W - 80, card_top + 60)], fill="#1E293B")
    draw.text((110, card_top + 16), f"SCENE 0{scene['id']} · PRODUCTION INVARIANT", fill="#60A5FA", font=f_badge)

    # Bullet points
    y = card_top + 110
    for pt in scene["points"]:
        # Wrap long lines
        words = pt.split(" ")
        lines = []
        cur = ""
        for w in words:
            if len(cur + " " + w) < 42:
                cur += (" " if cur else "") + w
            else:
                lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)

        for line in lines:
            draw.text((120, y), line, fill="#E2E8F0", font=f_bullet)
            y += 46
        y += 40

    # Footer
    draw.line([(80, 1680), (W - 80, 1680)], fill="#1E293B", width=2)
    draw.text((80, 1720), "THE PRAGMATIC ARCHITECT", fill="#60A5FA", font=f_author)
    draw.text((80, 1765), "By Gautam Sethi · AI Enthusiast", fill="#64748B", font=f_sub)

    img.save(out_path)
    return out_path


def build_full_video():
    clips = []
    print("=" * 70)
    print(" 🎥 RENDERING 60-SECOND ARCHITECTURAL VIDEO (MP4)")
    print(" Target: Safe Semantic Caching in Production (Issue #6)")
    print("=" * 70)

    for sc in SCENES:
        idx = sc["id"]
        slide_img = os.path.join(ASSETS_DIR, f"scene_{idx}_slide.png")
        audio_file = os.path.join(ASSETS_DIR, f"scene_{idx}_audio.mp3")

        print(f"[*] Rendering Scene {idx}: {sc['tag']}...")
        render_scene_slide(sc, slide_img)

        # Synthesize narration
        tts = gtts.gTTS(sc["speech"], lang="en", tld="com")
        tts.save(audio_file)

        # Create synchronized clip
        a_clip = AudioFileClip(audio_file)
        # Add 0.4s buffer for smooth transitions
        dur = a_clip.duration + 0.4
        v_clip = ImageClip(slide_img).set_duration(dur).set_audio(a_clip)
        clips.append(v_clip)

    print("[*] Concatenating scenes into final video...")
    final_video = concatenate_videoclips(clips, method="compose")
    
    out_mp4 = os.path.join(OUTPUT_DIR, "Safe_Semantic_Caching_60s_Reel.mp4")
    print(f"[*] Writing MP4 to {out_mp4} (Duration: {int(final_video.duration)}s)...")
    final_video.write_videofile(
        out_mp4,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        logger=None
    )

    print("\n" + "=" * 70)
    print(" 🎉 MP4 VIDEO FILE GENERATED SUCCESSFULLY!")
    print(f" File: {out_mp4}")
    print(f" Size: {os.path.getsize(out_mp4) / 1024:.1f} KB")
    print(f" Duration: {final_video.duration:.1f} seconds")
    print("=" * 70)
    return out_mp4


if __name__ == "__main__":
    build_full_video()

