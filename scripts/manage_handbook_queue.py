#!/usr/bin/env python3
"""
manage_handbook_queue.py - Inspects the current queue, manages slots,
and ensures all handbook carousels are queued or drafted in Buffer.
"""

import os
import sys
import json
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)

sys.path.insert(0, os.path.join(PROJECT_ROOT, "my_account"))
from buffer_publisher import execute_graphql, get_buffer_posts, schedule_buffer_post, load_config

def delete_post(post_id):
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
    print(f"Delete {post_id} -> {res}")
    return res

def list_posts():
    cfg = load_config()
    org_id = cfg.get("buffer", {}).get("organization_id")
    q = f"""
    query {{
      posts(input: {{ organizationId: "{org_id}", filter: {{ status: scheduled }} }}) {{
        edges {{
          node {{
            id
            status
            dueAt
            text
          }}
        }}
      }}
    }}
    """
    res = execute_graphql(q)
    edges = res.get("data", {}).get("posts", {}).get("edges", []) if res else []
    print(f"Total posts returned: {len(edges)}")
    scheduled = [e["node"] for e in edges if e["node"].get("status") == "scheduled"]
    print(f"Total scheduled posts: {len(scheduled)}")
    for p in scheduled:
        print(f"  {p.get('id')} | {p.get('dueAt')} | {p.get('text', '')[:50].replace(chr(10), ' ')}")
    return [e["node"] for e in edges]

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--delete":
        delete_post(sys.argv[2])
    else:
        list_posts()
