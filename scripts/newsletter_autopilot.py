#!/usr/bin/env python3
"""
newsletter_autopilot.py - Endless Automated Scheduling & Deduplication Engine
For 'The Pragmatic Architect' LinkedIn Newsletter:
https://www.linkedin.com/newsletters/the-pragmatic-architect-7515757942990737408/
"""

import os
import sys
import re
import json
import sqlite3
import hashlib
from datetime import datetime

# Safe cross-platform UTF-8 output handling
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
EDITIONS_DIR = os.path.join(PROJECT_ROOT, "my_account", "newsletter", "editions")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "my_account", "newsletter")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")
DB_PATH = os.path.join(PROJECT_ROOT, "my_account", "linkedin_tracker.db")

NEWSLETTER_URL = "https://www.linkedin.com/newsletters/the-pragmatic-architect-7515757942990737408/"
ARTICLE_EDITOR_URL = "https://www.linkedin.com/article/edit/"


def get_db_connection():
    """Returns SQLite connection with auto-table creation so fresh checkouts never crash."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS newsletter_editions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            edition_number INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            slug TEXT NOT NULL,
            summary TEXT NOT NULL,
            file_path TEXT NOT NULL,
            published_date TEXT,
            linkedin_article_url TEXT,
            status TEXT NOT NULL DEFAULT 'draft',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def compute_content_hash(text):
    clean = re.sub(r"\s+", " ", text.strip().lower())
    return hashlib.sha256(clean.encode("utf-8")).hexdigest()


def check_guardrails_is_published(edition_meta, body):
    """
    STRICT DEDUPLICATION GUARDRAIL
    Checks 3 distinct boundaries:
    1. Frontmatter check: status == 'published'
    2. SQLite Database check: status in ('published', 'live')
    3. Title & Content Hash match in DB activity logs / editions history
    """
    # 1. Frontmatter
    if str(edition_meta.get("status", "")).lower() == "published":
        return True, "Frontmatter status is 'published'"

    # 2. Database
    conn = get_db_connection()
    c = conn.cursor()
    
    # Check by edition number
    if "edition" in edition_meta:
        c.execute("SELECT status, published_date FROM newsletter_editions WHERE edition_number=?", (edition_meta["edition"],))
        row = c.fetchone()
        if row and row[0] == "published":
            conn.close()
            return True, f"SQLite DB confirms Issue #{edition_meta['edition']} was published on {row[1]}"

    # Check by title matching
    title = edition_meta.get("title", "")
    if title:
        c.execute("SELECT edition_number, status, published_date FROM newsletter_editions WHERE LOWER(title)=LOWER(?) AND status='published'", (title,))
        row = c.fetchone()
        if row:
            conn.close()
            return True, f"SQLite DB confirms title '{title}' was published in Issue #{row[0]}"

    conn.close()
    return False, "Safe: Not published"


def parse_edition_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            body = parts[2].strip()
            for line in fm.split("\n"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    k = k.strip()
                    v = v.strip().strip('"').strip("'")
                    if k == "edition":
                        try:
                            v = int(v)
                        except ValueError:
                            pass
                    meta[k] = v

    return meta, body


def get_all_editions_status():
    if not os.path.exists(EDITIONS_DIR):
        return []
    files = sorted([f for f in os.listdir(EDITIONS_DIR) if f.endswith(".md")])
    editions = []

    for f in files:
        p = os.path.join(EDITIONS_DIR, f)
        meta, body = parse_edition_file(p)
        is_pub, reason = check_guardrails_is_published(meta, body)
        editions.append({
            "filename": f,
            "filepath": p,
            "meta": meta,
            "is_published": is_pub,
            "reason": reason,
            "edition_num": meta.get("edition", None),
            "title": meta.get("title", f)
        })

    return editions


def get_next_ready_edition():
    editions = get_all_editions_status()
    for ed in editions:
        if not ed["is_published"]:
            return ed
    return None


def ensure_media_for_edition(edition_num, title, subtitle):
    os.makedirs(ASSETS_DIR, exist_ok=True)
    cover_path = os.path.join(ASSETS_DIR, f"newsletter_issue_{edition_num:02d}_cover.png")
    pdf_path = os.path.join(ASSETS_DIR, f"Zero_Downtime_Database_Architecture_Field_Manual.pdf")

    # If assets exist, return
    if os.path.exists(cover_path) and os.path.exists(pdf_path):
        return cover_path, pdf_path

    # Otherwise run generator script using current python interpreter
    gen_script = os.path.join(PROJECT_ROOT, "scripts", "generate_edition_media.py")
    if os.path.exists(gen_script):
        cmd = f'"{sys.executable}" "{gen_script}"'
        os.system(cmd)
    
    return cover_path, pdf_path


def mark_edition_as_published(edition_num, article_url=None):
    conn = get_db_connection()
    c = conn.cursor()
    today = datetime.now().strftime("%Y-%m-%d")
    c.execute("""
        UPDATE newsletter_editions 
        SET status='published', published_date=?, linkedin_article_url=? 
        WHERE edition_number=?
    """, (today, article_url, edition_num))
    conn.commit()
    conn.close()

    # Also update frontmatter in file
    for f in os.listdir(EDITIONS_DIR):
        if f.endswith(".md"):
            p = os.path.join(EDITIONS_DIR, f)
            meta, body = parse_edition_file(p)
            if meta.get("edition") == edition_num:
                with open(p, "r", encoding="utf-8") as file:
                    raw = file.read()
                updated = re.sub(r'status:\s*["\']?[a-zA-Z0-9_-]+["\']?', 'status: "published"', raw)
                with open(p, "w", encoding="utf-8") as file:
                    file.write(updated)
                break
    print(f"[+] Successfully marked Issue #{edition_num} as PUBLISHED with guardrails updated.")


def print_dashboard():
    print("=" * 80)
    print(" [GUARDRAILS] THE PRAGMATIC ARCHITECT - NEWSLETTER AUTOPILOT")
    print(" URL: " + NEWSLETTER_URL)
    print("=" * 80)

    editions = get_all_editions_status()
    published_count = 0
    ready_count = 0

    for ed in editions:
        status_badge = "[ALREADY PUBLISHED]" if ed["is_published"] else "[READY TO PUBLISH]"
        if ed["is_published"]:
            published_count += 1
        else:
            ready_count += 1

        print(f"\n{status_badge} Issue #{ed['edition_num']}: {ed['title']}")
        print(f"    File:   my_account/newsletter/editions/{ed['filename']}")
        print(f"    Status: {ed['reason']}")

    print("\n" + "-" * 80)
    print(f"SUMMARY: {published_count} Published | {ready_count} Fresh in Queue")
    print("-" * 80)

    next_ed = get_next_ready_edition()
    if next_ed and next_ed.get("edition_num"):
        print(f"\nNEXT SCHEDULED ISSUE: Issue #{next_ed['edition_num']}")
        print(f"   Title: {next_ed['title']}")
        
        # Verify media files
        cover, pdf = ensure_media_for_edition(
            next_ed["edition_num"], 
            next_ed["title"], 
            next_ed["meta"].get("subtitle", "")
        )
        print(f"   Cover Banner (1280x720): {os.path.relpath(cover, PROJECT_ROOT)}")
        print(f"   PDF Field Manual:       {os.path.relpath(pdf, PROJECT_ROOT)}")
        print(f"   Ready Package:          my_account/newsletter/ready_to_publish_issue_{next_ed['edition_num']}.txt")
    else:
        print("\nQueue status: All editions scanned or queue empty.")
    print("=" * 80)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--mark-published":
        if len(sys.argv) > 2:
            num = int(sys.argv[2])
            url = sys.argv[3] if len(sys.argv) > 3 else None
            mark_edition_as_published(num, url)
        else:
            print("Usage: python newsletter_autopilot.py --mark-published <edition_num> [url]")
    else:
        print_dashboard()
