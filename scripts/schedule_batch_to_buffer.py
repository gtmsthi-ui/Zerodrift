#!/usr/bin/env python3
"""
schedule_batch_to_buffer.py - Schedules the complete pipeline of posts into Buffer.
Ensures every post has its exact dueAt timestamp, attached infographic image,
and updates both markdown frontmatter and SQLite tracker.
"""

import os
import sys
import json
import sqlite3
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
POSTS_DIR = os.path.join(PROJECT_ROOT, "my_account", "posts")
DB_PATH = os.path.join(PROJECT_ROOT, "my_account", "linkedin_tracker.db")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "my_account"))
sys.path.insert(0, HERE)

from buffer_publisher import schedule_buffer_post
from cloud_autopilot import parse_post_file, update_post_file

SCHEDULE_PLAN = [
    {
        "key": "post_04",
        "file": "04_sunday_career.md",
        "due_at": "2026-10-18T11:00:00.000Z", # Sunday Oct 18, 4:30 PM IST
        "image_url": "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets/post_04_card.png",
        "existing_buffer_id": "6ad0910c675f058f0b406b9a"
    },
    {
        "key": "post_05",
        "file": "05_tuesday_ai.md",
        "due_at": "2026-10-20T03:00:00.000Z", # Tuesday Oct 20, 8:30 AM IST
        "image_url": "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets/post_05_card.png"
    },
    {
        "key": "post_06",
        "file": "06_thursday_career.md",
        "due_at": "2026-10-22T03:00:00.000Z", # Thursday Oct 22, 8:30 AM IST
        "image_url": "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets/post_06_card.png"
    },
    {
        "key": "post_07",
        "file": "07_friday_ai.md",
        "due_at": "2026-10-23T03:00:00.000Z", # Friday Oct 23, 8:30 AM IST
        "image_url": "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets/post_07_card.png"
    },
    {
        "key": "post_08",
        "file": "08_sunday_career.md",
        "due_at": "2026-10-25T11:00:00.000Z", # Sunday Oct 25, 4:30 PM IST
        "image_url": "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets/post_08_card.png"
    }
]

def update_file_frontmatter(filepath, meta, body, buf_id, due_at):
    meta["status"] = "scheduled"
    meta["scheduled_at"] = due_at
    meta["buffer_post_id"] = buf_id
    
    lines = ["---"]
    for k, v in meta.items():
        lines.append(f'{k}: "{v}"')
    lines.append("---")
    lines.append("")
    lines.append(body)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def update_db(post_key, buf_id, due_at):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur.execute("""
            UPDATE posts 
            SET status = 'scheduled',
                buffer_post_id = ?,
                scheduled_at = ?,
                updated_at = ?
            WHERE post_key = ?
        """, (buf_id, due_at, now, post_key))
        
        cur.execute("""
            INSERT INTO activity_logs (action_type, summary, details, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            "POST_SCHEDULED",
            f"Scheduled {post_key} in Buffer for {due_at}",
            f"Buffer ID: {buf_id}",
            "SUCCESS",
            now
        ))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] DB Update Error: {e}")

def main():
    print(f"[*] Starting Batch Post Scheduler to Buffer ({len(SCHEDULE_PLAN)} posts)...")
    
    for item in SCHEDULE_PLAN:
        post_path = os.path.join(POSTS_DIR, item["file"])
        if not os.path.exists(post_path):
            print(f"[-] File not found: {post_path}")
            continue
            
        meta, body = parse_post_file(post_path)
        buf_id = item.get("existing_buffer_id")
        
        if buf_id:
            print(f"[+] Post {item['key']} already pushed to Buffer (ID: {buf_id}). Updating local state...")
        else:
            print(f"[*] Pushing {item['key']} ({meta.get('title')}) to Buffer for {item['due_at']}...")
            res = schedule_buffer_post(
                post_text=body,
                due_at=item["due_at"],
                image_url=item["image_url"]
            )
            if res and "id" in res:
                buf_id = res["id"]
                print(f"  [+] Success! Buffer Post ID: {buf_id}")
            else:
                print(f"  [-] Failed to push {item['key']} to Buffer!")
                continue
                
        # Update markdown
        update_file_frontmatter(post_path, meta, body, buf_id, item["due_at"])
        # Update sqlite
        update_db(item["key"], buf_id, item["due_at"])
        
    print("\n[+] Batch Scheduling Complete!")

if __name__ == "__main__":
    main()
