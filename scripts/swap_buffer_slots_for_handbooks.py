#!/usr/bin/env python3
"""
swap_buffer_slots_for_handbooks.py - Frees up the 2 far-future January 2027 slots
in Buffer and schedules the remaining two December Handbook posts:
- Handbook 3: Model Context Protocol (MCP) on Saturday Dec 19, 2026 @ 4:30 PM IST
- Handbook 4: AEM Enterprise Web Reliability on Saturday Dec 26, 2026 @ 4:30 PM IST
"""

import os
import sys
import json
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)

sys.path.insert(0, os.path.join(PROJECT_ROOT, "my_account"))
from buffer_publisher import execute_graphql, schedule_buffer_post, load_config
from schedule_handbooks_to_buffer import HANDBOOK_SCHEDULE, RAW_BASE, log_activity

def delete_buffer_post(post_id):
    mutation = f"""
    mutation {{
      deletePost(input: {{ id: "{post_id}" }}) {{
        ... on DeletePostPayload {{
          __typename
        }}
        ... on MutationError {{
          message
        }}
      }}
    }}
    """
    res = execute_graphql(mutation)
    print(f"[*] Deleted Buffer post {post_id}: {res}")
    return res

def main():
    print("=" * 70)
    print("🔄 RE-BALANCING BUFFER QUEUE FOR DECEMBER 2026 HANDBOOKS")
    print("=" * 70)

    # 1. Delete the 2 far-future January 2027 slots
    jan_post_1 = "6afc4f3e55207cffaeebcc57" # Jan 20, 2027
    jan_post_2 = "6afc4f3dbdb250961b9550a5" # Jan 13, 2027

    print("\n[1] Freeing 2 far-future January 2027 slots to make room for December Handbooks...")
    delete_buffer_post(jan_post_1)
    delete_buffer_post(jan_post_2)

    # 2. Schedule Handbook 3 (Dec 19) and Handbook 4 (Dec 26)
    for item in HANDBOOK_SCHEDULE:
        if item["id_key"] in ["handbook_03", "handbook_04"]:
            title = item["title"]
            due_at = item["due_at"]
            doc_url = f"{RAW_BASE}/{item['pdf_name']}"
            thumb_url = f"{RAW_BASE}/{item['cover_name']}"
            doc_title = item["doc_title"]
            
            print(f"\n[2] Scheduling: {title}")
            print(f"    Slot: {due_at} (Saturday 4:30 PM IST)")
            print(f"    PDF:  {doc_url}")
            
            res = schedule_buffer_post(
                post_text=item["text"],
                as_draft=False,
                document_url=doc_url,
                document_title=doc_title,
                thumbnail_url=thumb_url,
                due_at=due_at
            )
            
            if res and "id" in res:
                buf_id = res["id"]
                status = res.get("status", "scheduled")
                print(f"    [+] SUCCESS: Scheduled to Buffer! ID = {buf_id} (Status: {status})")
                log_activity(
                    "BUFFER_HANDBOOK_SCHEDULED",
                    f"Scheduled Tailored Handbook Post: {title}",
                    f"Buffer ID: {buf_id} | dueAt: {due_at} | PDF: {item['pdf_name']}"
                )
            else:
                print(f"    [-] Failed to schedule: {res}", file=sys.stderr)

    print("\n" + "=" * 70)
    print("✅ Finished re-balancing Buffer queue for December 2026 Handbooks!")
    print("=" * 70)

if __name__ == "__main__":
    main()
