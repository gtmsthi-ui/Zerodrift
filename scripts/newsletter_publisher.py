#!/usr/bin/env python3
"""
newsletter_publisher.py - Master Publisher for 'The Pragmatic Architect' Newsletter
URL: https://www.linkedin.com/newsletters/the-pragmatic-architect-7515757942990737408/

Commands:
  1. List all available newsletter editions:
     python scripts/newsletter_publisher.py --list

  2. Prepare an edition for instant publishing (generates formatted markdown, copy-paste buffer & launch post):
     python scripts/newsletter_publisher.py --edition 2

  3. Generate the next bespoke newsletter edition from a topic:
     python scripts/newsletter_publisher.py --generate "Topic Name"
"""

import argparse
import os
import re
import sys
import webbrowser

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
EDITIONS_DIR = os.path.join(PROJECT_ROOT, "my_account", "newsletter", "editions")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "my_account", "newsletter")
NEWSLETTER_URL = "https://www.linkedin.com/newsletters/the-pragmatic-architect-7515757942990737408/"
ARTICLE_EDITOR_URL = "https://www.linkedin.com/article/edit/"


def list_editions():
    print("=" * 70)
    print(" 📰 THE PRAGMATIC ARCHITECT - LINKEDIN NEWSLETTER EDITIONS")
    print(" URL: " + NEWSLETTER_URL)
    print("=" * 70)

    files = sorted(os.listdir(EDITIONS_DIR))
    editions = []
    for f in files:
        if f.endswith(".md"):
            p = os.path.join(EDITIONS_DIR, f)
            with open(p, "r", encoding="utf-8") as file:
                content = file.read()
                title_match = re.search(r'title:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)
                pillar_match = re.search(r'pillar:\s*["\']?(.*?)["\']?$', content, re.MULTILINE)
                title = title_match.group(1) if title_match else f
                pillar = pillar_match.group(1) if pillar_match else "General"
                editions.append((f, title, pillar))

    for idx, (fname, title, pillar) in enumerate(editions, 1):
        print(f"[{idx}] {title}")
        print(f"    File:   my_account/newsletter/editions/{fname}")
        print(f"    Pillar: {pillar}")
        print("-" * 70)


def prepare_edition(edition_num, open_browser=True):
    files = sorted([f for f in os.listdir(EDITIONS_DIR) if f.endswith(".md")])
    if edition_num < 1 or edition_num > len(files):
        print(f"[-] Invalid edition number. Choose between 1 and {len(files)}.")
        return

    target_file = files[edition_num - 1]
    target_path = os.path.join(EDITIONS_DIR, target_file)

    with open(target_path, "r", encoding="utf-8") as f:
        raw = f.read()

    # Extract metadata
    title_m = re.search(r'title:\s*["\']?(.*?)["\']?$', raw, re.MULTILINE)
    subtitle_m = re.search(r'subtitle:\s*["\']?(.*?)["\']?$', raw, re.MULTILINE)
    title = title_m.group(1) if title_m else "The Pragmatic Architect Edition"
    subtitle = subtitle_m.group(1) if subtitle_m else "A Senior Architect's Guide"

    # Extract clean article body without frontmatter
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()

    # Generate the Accompanying LinkedIn Launch Feed Post
    launch_post = (
        f"The latest issue of The Pragmatic Architect is live.\n\n"
        f"Headline: {title}\n\n"
        f"In mission-critical enterprise systems, superficial patterns collapse the moment they face real customer SLA requirements.\n\n"
        f"In this deep-dive edition, I broke down the complete architectural blueprint:\n"
        f"• The core failure modes teams overlook in staging\n"
        f"• The step-by-step production-safe transition topology\n"
        f"• Exact verification gates and observability traces before merging code\n\n"
        f"Read the full article and subscribe here:\n"
        f"{NEWSLETTER_URL}\n\n"
        f"#SoftwareArchitecture #DistributedSystems #EngineeringLeadership #SystemsDesign #TechCareers"
    )

    # Save ready-to-copy package
    out_pkg = os.path.join(OUTPUT_DIR, f"ready_to_publish_issue_{edition_num}.txt")
    with open(out_pkg, "w", encoding="utf-8") as f:
        f.write("=" * 70 + "\n")
        f.write(f"LINKEDIN NEWSLETTER PUBLISHING PACKAGE: ISSUE #{edition_num}\n")
        f.write("Target Newsletter: The Pragmatic Architect\n")
        f.write(f"URL: {NEWSLETTER_URL}\n")
        f.write("=" * 70 + "\n\n")

        f.write("STEP 1: HEADLINE (PASTE IN TITLE FIELD)\n")
        f.write("-" * 50 + "\n")
        f.write(title + "\n\n")

        f.write("STEP 2: SUBTITLE / BYLINE\n")
        f.write("-" * 50 + "\n")
        f.write(f"{subtitle}\nBy Gautam Sethi · AI Enthusiast\n\n")

        f.write("STEP 3: ACCOMPANYING FEED ANNOUNCEMENT POST\n")
        f.write("(When clicking 'Publish', LinkedIn asks: 'What do you want to talk about?')\n")
        f.write("-" * 50 + "\n")
        f.write(launch_post + "\n\n")

        f.write("STEP 4: ARTICLE BODY (COPY & PASTE INTO LINKEDIN ARTICLE EDITOR)\n")
        f.write("=" * 70 + "\n")
        f.write(body + "\n")

    print("\n" + "=" * 70)
    print(f" 🎉 NEWSLETTER PACKAGE READY: ISSUE #{edition_num}")
    print(f" File: {out_pkg}")
    print("=" * 70)
    print(f"\n[1] HEADLINE:\n{title}")
    print(f"\n[2] SUBTITLE:\n{subtitle}")
    print(f"\n[3] SAVED TO:\n{out_pkg}")
    print("\n[4] LINKEDIN ARTICLE EDITOR:")
    print(f"    Opening {ARTICLE_EDITOR_URL} in your browser...")
    print("    Make sure 'Publish to: The Pragmatic Architect' is selected at the top!")
    print("=" * 70)

    if open_browser:
        webbrowser.open(ARTICLE_EDITOR_URL)


def main():
    parser = argparse.ArgumentParser(description="Master Publisher for The Pragmatic Architect Newsletter.")
    parser.add_argument("--list", action="store_true", help="List all available newsletter editions")
    parser.add_argument("--edition", type=int, default=2, help="Prepare a specific edition number (default: 2)")
    args = parser.parse_args()

    if args.list:
        list_editions()
    else:
        prepare_edition(args.edition)


if __name__ == "__main__":
    main()
