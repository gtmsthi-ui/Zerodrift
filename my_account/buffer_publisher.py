#!/usr/bin/env python3
"""
buffer_publisher.py - Integrates with Buffer's GraphQL API (2025/2026) to schedule or draft posts to LinkedIn.
Zero external dependencies (uses standard library urllib).
"""

import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(HERE, "config.json")
GRAPHQL_URL = "https://api.buffer.com/graphql"


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def execute_graphql(query, variables=None, access_token=None):
    if not access_token:
        cfg = load_config()
        if cfg and "buffer" in cfg:
            access_token = cfg["buffer"].get("access_token")

    if not access_token or access_token.startswith("YOUR_"):
        print("[-] Error: Buffer access_token not configured in my_account/config.json", file=sys.stderr)
        return None

    payload = {"query": query}
    if variables:
        payload["variables"] = variables

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        GRAPHQL_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"[-] HTTP Error {e.code}: {e.read().decode('utf-8')}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[-] Buffer request failed: {e}", file=sys.stderr)
        return None


def get_profiles(access_token=None):
    """Fetches connected channels using GraphQL."""
    cfg = load_config()
    org_id = cfg.get("buffer", {}).get("organization_id")
    if not org_id:
        # First query account organizations
        res = execute_graphql("""
        query {
          account {
            organizations {
              id
              name
            }
          }
        }
        """, access_token=access_token)
        orgs = res.get("data", {}).get("account", {}).get("organizations", [])
        if orgs:
            org_id = orgs[0]["id"]

    if not org_id:
        print("[-] Could not determine organization ID.", file=sys.stderr)
        return []

    q = f"""
    query {{
      channels(input: {{ organizationId: "{org_id}" }}) {{
        id
        name
        service
      }}
    }}
    """
    res = execute_graphql(q, access_token=access_token)
    return res.get("data", {}).get("channels", []) if res else []


def schedule_buffer_post(post_text, channel_id=None, as_draft=True, share_now=False, access_token=None):
    """
    Creates a post or draft on the specified LinkedIn channel.
    as_draft=True saves it into Buffer as a draft for review/scheduling.
    share_now=True publishes immediately.
    """
    cfg = load_config()
    if not channel_id and cfg and "buffer" in cfg:
        channel_id = cfg["buffer"].get("profile_id")
    if not access_token and cfg and "buffer" in cfg:
        access_token = cfg["buffer"].get("access_token")

    if not channel_id or channel_id.startswith("YOUR_"):
        print("[-] Error: Buffer profile_id/channel_id not configured in config.json", file=sys.stderr)
        return None

    mode = "shareNow" if share_now else "addToQueue"
    save_draft = "true" if as_draft else "false"

    # Escape JSON text cleanly
    escaped_text = json.dumps(post_text)

    mutation = f"""
    mutation {{
      createPost(input: {{
        channelId: "{channel_id}",
        text: {escaped_text},
        mode: {mode},
        schedulingType: automatic,
        saveToDraft: {save_draft},
        needsApproval: false
      }}) {{
        ... on PostActionSuccess {{
          post {{
            id
            text
            status
          }}
        }}
        ... on MutationError {{
          message
        }}
      }}
    }}
    """

    res = execute_graphql(mutation, access_token=access_token)
    if res and "data" in res:
        post_data = res["data"].get("createPost", {})
        if "post" in post_data:
            state = post_data["post"].get("state", "draft/queued")
            print(f"[+] Successfully pushed post to Buffer! (State: {state})")
            return post_data["post"]
        elif "message" in post_data:
            print(f"[-] Buffer mutation error: {post_data['message']}", file=sys.stderr)
            return None
    print(f"[-] Buffer response: {res}", file=sys.stderr)
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--profiles":
        print("[*] Fetching connected channels from Buffer GraphQL API...")
        channels = get_profiles()
        if channels:
            print(f"[+] Found {len(channels)} channel(s):")
            for c in channels:
                print(f"  - {c.get('service').upper()} ({c.get('name')}): ID = {c.get('id')}")
        else:
            print("[-] No channels found.")
    else:
        print("Usage: python buffer_publisher.py --profiles")
