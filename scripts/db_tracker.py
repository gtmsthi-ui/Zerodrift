#!/usr/bin/env python3
"""
db_tracker.py - Central Database & Activity Log for LinkedIn Autonomous System
Stores and tracks:
- All drafted, queued, and published posts
- Schedule timestamps, scores, and Buffer post IDs
- Attached personalized infographics / diagram images
- Daily engagement audits & Telegram activity history
"""

import os
import sys
import sqlite3
import datetime
import json

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
DB_PATH = os.path.join(PROJECT_ROOT, "my_account", "linkedin_tracker.db")
POSTS_DIR = os.path.join(PROJECT_ROOT, "my_account", "posts")

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_db()
    with conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_key TEXT UNIQUE NOT NULL,
            filename TEXT NOT NULL,
            title TEXT NOT NULL,
            pillar TEXT NOT NULL,
            day_slot TEXT NOT NULL,
            content TEXT NOT NULL,
            human_score REAL DEFAULT 0.0,
            status TEXT NOT NULL DEFAULT 'draft', -- draft, queued, buffer_scheduled, published
            buffer_post_id TEXT,
            image_path TEXT,
            image_url TEXT,
            image_summary TEXT,
            scheduled_at TEXT,
            published_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action_type TEXT NOT NULL, -- POST_BUFFER_QUEUED, POST_PUBLISHED, IMAGE_GENERATED, MANUAL_SCHEDULE, SYSTEM_EVENT
            summary TEXT NOT NULL,
            details TEXT,
            status TEXT NOT NULL DEFAULT 'SUCCESS', -- SUCCESS, PENDING, FAILED, SKIPPED
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        conn.execute("""
        CREATE TABLE IF NOT EXISTS system_config (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

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
            status TEXT NOT NULL DEFAULT 'draft', -- draft, ready, published
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
    conn.close()


def seed_posts_from_disk():
    """Populates the database from existing markdown post files if not already present."""
    init_db()
    conn = get_db()

    post_meta = [
        {
            "key": "post_01",
            "file": "01_tuesday_ai.md",
            "title": "Why most LLM prototypes fail in staging",
            "pillar": "Practical AI & System Architecture",
            "day": "Tuesday 8:30 AM",
            "score": 72.8,
            "status": "draft", # Moved to draft by user
            "buffer_id": "6ace135e06d8b03d5e0272bc"
        },
        {
            "key": "post_02",
            "file": "02_thursday_career.md",
            "title": "The real difference between Senior and Architect",
            "pillar": "Staff+ Career & Technical Leadership",
            "day": "Thursday 8:30 AM",
            "score": 87.1,
            "status": "buffer_scheduled",
            "buffer_id": "6ace363e1077be9dba26a4e8"
        },
        {
            "key": "post_03",
            "file": "03_friday_ai.md",
            "title": "The 3 Silent Production RAG Failure Modes",
            "pillar": "Practical AI & System Architecture",
            "day": "Friday 8:30 AM",
            "score": 78.1,
            "status": "queued",
            "buffer_id": None
        },
        {
            "key": "post_04",
            "file": "04_sunday_career.md",
            "title": "The $42k Cloud Mistake That Changed How I Talk to CFOs",
            "pillar": "Staff+ Career & Technical Leadership",
            "day": "Sunday 4:30 PM",
            "score": 76.7,
            "status": "queued",
            "buffer_id": None
        }
    ]

    for p in post_meta:
        path = os.path.join(POSTS_DIR, p["file"])
        content = ""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()

        with conn:
            conn.execute("""
            INSERT INTO posts (post_key, filename, title, pillar, day_slot, content, human_score, status, buffer_post_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(post_key) DO UPDATE SET
                title = excluded.title,
                pillar = excluded.pillar,
                day_slot = excluded.day_slot,
                content = excluded.content,
                human_score = excluded.human_score,
                status = CASE WHEN posts.status = 'published' THEN 'published' ELSE excluded.status END,
                buffer_post_id = COALESCE(posts.buffer_post_id, excluded.buffer_post_id),
                updated_at = CURRENT_TIMESTAMP;
            """, (p["key"], p["file"], p["title"], p["pillar"], p["day"], content, p["score"], p["status"], p["buffer_id"]))

    conn.close()


def record_log(action_type, summary, details="", status="SUCCESS"):
    init_db()
    conn = get_db()
    with conn:
        conn.execute("""
        INSERT INTO activity_logs (action_type, summary, details, status)
        VALUES (?, ?, ?, ?);
        """, (action_type, summary, details, status))
    conn.close()


def update_post_image(post_key, image_path, image_url, image_summary=""):
    init_db()
    conn = get_db()
    with conn:
        conn.execute("""
        UPDATE posts
        SET image_path = ?, image_url = ?, image_summary = ?, updated_at = CURRENT_TIMESTAMP
        WHERE post_key = ?;
        """, (image_path, image_url, image_summary, post_key))
    conn.close()
    record_log("IMAGE_GENERATED", f"Attached infographic/image for {post_key}", f"Path: {image_path}\nURL: {image_url}")


def update_post_status(post_key, status, buffer_id=None):
    init_db()
    conn = get_db()
    with conn:
        conn.execute("""
        UPDATE posts
        SET status = ?, buffer_post_id = COALESCE(?, buffer_post_id), updated_at = CURRENT_TIMESTAMP
        WHERE post_key = ?;
        """, (status, buffer_id, post_key))
    conn.close()
    record_log("POST_STATUS_UPDATED", f"Post {post_key} transitioned to {status}", f"Buffer ID: {buffer_id}")


def get_all_posts():
    init_db()
    conn = get_db()
    rows = conn.execute("SELECT * FROM posts ORDER BY id ASC;").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_next_queued_post():
    init_db()
    conn = get_db()
    row = conn.execute("SELECT * FROM posts WHERE status = 'queued' ORDER BY id ASC LIMIT 1;").fetchone()
    conn.close()
    return dict(row) if row else None


def get_recent_logs(limit=10):
    init_db()
    conn = get_db()
    rows = conn.execute("SELECT * FROM activity_logs ORDER BY id DESC LIMIT ?;", (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def print_dashboard():
    """Prints a clean CLI summary dashboard for the user."""
    posts = get_all_posts()
    logs = get_recent_logs(5)

    print("\n" + "=" * 76)
    print("                LINKEDIN CENTRAL DATABASE DASHBOARD")
    print("=" * 76)
    print(f"{'KEY':<9} | {'SCHEDULE SLOT':<17} | {'STATUS':<17} | {'SCORE':<6} | {'IMAGE':<6} | {'TITLE'}")
    print("-" * 76)
    for p in posts:
        has_img = "YES" if p["image_path"] else "NO"
        status_disp = p["status"].upper()
        print(f"{p['post_key']:<9} | {p['day_slot']:<17} | {status_disp:<17} | {p['human_score']:<6.1f} | {has_img:<6} | {p['title'][:25]}")

    print("\n" + "=" * 76)
    print("                    RECENT SYSTEM ACTIVITY LOGS")
    print("=" * 76)
    for l in logs:
        ts = l["created_at"]
        print(f"[{ts}] [{l['action_type']}] {l['summary']} ({l['status']})")
    print("=" * 76 + "\n")


if __name__ == "__main__":
    init_db()
    seed_posts_from_disk()
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        print_dashboard()
    else:
        print_dashboard()
