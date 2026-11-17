#!/usr/bin/env python3
"""
li_reply_monitor.py - LinkedIn Comment Reply Monitor using linkedin-api library

Uses the linkedin-api library's session bootstrap (Android UA → /uas/authenticate)
to get a valid JSESSIONID, then injects the li_at cookie from config.json.
No username/password needed. No Playwright/browser. No bot detection.

Usage:
  python scripts/li_reply_monitor.py --dry-run        # Preview replies without posting
  python scripts/li_reply_monitor.py                  # Post replies live
  python scripts/li_reply_monitor.py --max 15         # Override cap (default 10)
  python scripts/li_reply_monitor.py --post-count 20  # How many posts to scan (default 10)
"""

import argparse
import datetime
import json
import os
import random
import re
import sys
import time

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import requests
from linkedin_api.client import Client
from linkedin_api import Linkedin

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "my_account", "config.json")
ENGAGEMENT_LOG = os.path.join(PROJECT_ROOT, "my_account", "engagement_log.md")
PROFILE_ID = "gautam-sethi-1b944324"

# ─────────────────────────────────────────────
# Config helpers
# ─────────────────────────────────────────────

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


# ─────────────────────────────────────────────
# Auth: bootstrap session with Android UA, inject li_at
# ─────────────────────────────────────────────

def build_linkedin_client(li_at: str) -> Client:
    """
    Build a linkedin-api Client object authenticated with an existing li_at cookie.

    Steps (mirrors what Client._do_authentication_request does internally):
      1. GET /uas/authenticate with Android headers → get fresh JSESSIONID
      2. Inject our li_at into the session
      3. Set csrf-token from JSESSIONID
    """
    client = Client()

    # Step 1: Bootstrap session cookies from LinkedIn (gets JSESSIONID)
    print("[*] Bootstrapping session via LinkedIn Android auth endpoint...")
    bootstrap_cookies = client._request_session_cookies()
    client._set_session_cookies(bootstrap_cookies)

    # Step 2: Inject real li_at cookie (overwrites the unauthenticated one)
    client.session.cookies.set("li_at", li_at, domain=".linkedin.com")

    # Step 3: CSRF token is already set from JSESSIONID in step 1
    print(f"[*] Session ready. JSESSIONID = {client.session.cookies.get('JSESSIONID', 'none')[:30]}...")
    return client


def build_linkedin_api(client: Client) -> Linkedin:
    """Wrap the authenticated client in a Linkedin API object."""
    api = Linkedin.__new__(Linkedin)
    api.client = client
    api.logger = client.logger
    api._MAX_POST_COUNT = 100
    api._MAX_UPDATE_COUNT = 100
    api._MAX_SEARCH_COUNT = 49
    api._DEFAULT_SEARCH_TYPES = []
    # Fetch metadata (needed for some calls)
    try:
        client._fetch_metadata()
    except Exception as e:
        print(f"[!] Metadata fetch note: {e}")
    return api


# ─────────────────────────────────────────────
# Engagement log
# ─────────────────────────────────────────────

def get_replied_ids() -> set:
    if not os.path.exists(ENGAGEMENT_LOG):
        return set()
    replied = set()
    with open(ENGAGEMENT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"Thread-ID:\s*(\S+)", line)
            if m:
                replied.add(m.group(1).strip())
    return replied


def log_reply(thread_id: str, commenter: str, their_text: str, my_reply: str, bucket: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"- [{now}] [{bucket}] Reply to @{commenter}:\n"
        f"  Thread-ID: {thread_id}\n"
        f"  Their comment: \"{their_text[:120]}...\"\n"
        f"  Your reply: \"{my_reply}\"\n\n"
    )
    mode = "a" if os.path.exists(ENGAGEMENT_LOG) else "w"
    with open(ENGAGEMENT_LOG, mode, encoding="utf-8") as f:
        if mode == "w":
            f.write("# Autonomous LinkedIn Engagement Log\n\n")
        f.write(entry)


# ─────────────────────────────────────────────
# Telegram
# ─────────────────────────────────────────────

def send_telegram(text: str, cfg: dict):
    token = cfg.get("telegram", {}).get("bot_token")
    chat_id = cfg.get("telegram", {}).get("chat_id")
    if not token or not chat_id:
        return
    try:
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True},
            timeout=15,
        )
    except Exception as e:
        print(f"  [-] Telegram failed: {e}")


# ─────────────────────────────────────────────
# Triage & reply generation (from voice.md)
# ─────────────────────────────────────────────

def triage(text: str) -> str:
    lower = text.lower()
    if any(k in lower for k in ["dm me", "check out my", "i help ", "book a call", "free consultation", "click here", "reach out to me"]):
        return "NOISE"
    if any(k in lower for k in ["how do you", "how did you", "can you share", "template", "would love to", "could you help", "any resources", "where can i", "how to", "how can"]):
        return "LEAD"
    if any(k in lower for k in ["disagree", "however,", "trade-off", "tradeoff", "depends on", "latency", "bottleneck", "overhead", "alternatively", "what about", "have you considered", "actually,", "but what"]):
        return "SUBSTANCE"
    if any(k in lower for k in ["we've", "we have", "in our team", "at my company", "from experience", "i've seen", "i've built", "similar thing", "in our case", "at our org"]):
        return "PEER"
    return "SUPPORT"


def generate_reply(comment_text: str, commenter_name: str, bucket: str) -> str:
    first = commenter_name.split()[0] if commenter_name else ""
    sal = f"{first}, " if first else ""
    lower = comment_text.lower()

    if bucket == "LEAD":
        if any(k in lower for k in ["template", "share", "send", "resource"]):
            return (
                f"{sal}happy to share the structure. "
                "The part that made the biggest difference for us was separating schema validation "
                "from downstream ingestion — once decoupled, payload errors dropped significantly. "
                "Send a connection request and I'll pass it across."
            )
        return (
            f"{sal}the short answer: start at the execution boundary, not the model. "
            "Define a strict input/output schema first, then wrap the LLM call in a retry harness "
            "with deterministic fallback. Most teams skip that step and pay for it in production."
        )

    if bucket == "SUBSTANCE":
        if any(k in lower for k in ["disagree", "actually", "but"]):
            return (
                f"{sal}fair point — that holds true at lower scale. "
                "The calculus shifts once you're under sustained load; "
                "at that point serialization overhead becomes the dominant cost, not the logic layer. "
                "Appreciate the pushback."
            )
        return (
            f"{sal}exactly right. "
            "Most teams don't hit that trade-off until they're already in production, "
            "which is the worst time to learn it. "
            "The part that surprises people is how fast network round-trips dwarf compute costs at scale."
        )

    if bucket == "PEER":
        return (
            f"{sal}that matches what we've seen across multiple migrations. "
            "Teams that move fastest have already internalized the infra cost "
            "before writing the first line of orchestration code. Good to know it's consistent across orgs."
        )

    if bucket == "SUPPORT":
        short = [
            f"Thanks {first}. Glad it landed." if first else "Appreciate it — glad it landed.",
            f"Thanks {first}. More on this soon." if first else "Thanks. More to come on this.",
            f"Appreciate it, {first}." if first else "Appreciate the kind words.",
        ]
        return random.choice(short)

    return ""  # NOISE — no reply


# ─────────────────────────────────────────────
# Post reply via Voyager API directly
# ─────────────────────────────────────────────

def post_comment_reply(client: Client, post_urn: str, comment_urn: str, reply_text: str) -> bool:
    """Post a reply to a comment using the authenticated client session."""
    url = f"{client.API_BASE_URL}/feed/comments"
    payload = {
        "actor": f"urn:li:member:{PROFILE_ID}",
        "message": {"attributes": [], "text": reply_text},
        "parentCommentUrn": comment_urn,
        "updateKey": post_urn,
    }
    try:
        resp = client.session.post(url, json=payload, timeout=20)
        return resp.status_code in (200, 201)
    except Exception as e:
        print(f"  [-] Post reply error: {e}")
        return False


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def run(dry_run: bool = False, max_replies: int = 10, post_count: int = 10):
    cfg = load_config()
    li_at = cfg.get("linkedin", {}).get("li_at", "")
    if not li_at:
        print("[-] No li_at in config.json. Grab it from Chrome DevTools > Application > Cookies > linkedin.com")
        sys.exit(1)

    replied_ids = get_replied_ids()

    print("=" * 60)
    print(f"  LinkedIn Reply Monitor  |  {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Scanning last {post_count} posts  |  Max replies: {max_replies}")
    print("=" * 60)

    # Auth
    client = build_linkedin_client(li_at)
    api = build_linkedin_api(client)

    # Fetch posts
    print(f"\n[*] Fetching posts for @{PROFILE_ID}...")
    try:
        posts = api.get_profile_posts(public_id=PROFILE_ID, post_count=post_count)
    except Exception as e:
        print(f"[-] Failed to fetch posts: {e}")
        print("[!] If you see a CHALLENGE error, your li_at cookie may be expired.")
        print("[!] Grab a fresh one: Chrome > F12 > Application > Cookies > linkedin.com > li_at")
        sys.exit(1)

    print(f"[+] Found {len(posts)} posts.\n")

    reply_count = 0
    triage_counts = {"LEAD": 0, "SUBSTANCE": 0, "PEER": 0, "SUPPORT": 0, "NOISE": 0, "SKIPPED": 0}

    for post in posts:
        if reply_count >= max_replies:
            break

        # Extract post URN (activity ID)
        urn = ""
        entity_urn = post.get("updateMetadata", {}).get("urn", "") or post.get("entityUrn", "")
        if "activity:" in entity_urn:
            urn = entity_urn.split("activity:")[-1].split(",")[0].rstrip(")")
        if not urn:
            continue

        print(f"[Post] activity:{urn}")

        # Fetch comments
        try:
            comments = api.get_post_comments(post_urn=urn, comment_count=50)
        except Exception as e:
            print(f"  [-] Could not fetch comments: {e}")
            continue

        # Filter out empty
        comments = [c for c in comments if c and c.get("commentV2", {}).get("text", {}).get("text", "")]
        print(f"  {len(comments)} comment(s) found.")

        for comment in comments:
            if reply_count >= max_replies:
                break

            # Extract text and author
            text = comment.get("commentV2", {}).get("text", {}).get("text", "")
            if not text:
                text = comment.get("comment", {}).get("values", [{}])[0].get("value", {}).get("com.linkedin.voyager.feed.render.CommentComponent", {}).get("commentV2", {}).get("text", {}).get("text", "")
            if not text:
                continue

            author_obj = comment.get("commenter", {}).get("com.linkedin.voyager.feed.MemberActor", {})
            author_name = author_obj.get("name", {}).get("text", "") or "Peer"
            author_name = author_name.split("\n")[0].strip()

            comment_urn = comment.get("entityUrn", "")
            thread_id = str(abs(hash(comment_urn or text[:60])))

            # Skip own comments
            if any(k in author_name.lower() for k in ["gautam", "sethi"]):
                continue

            # Skip already replied
            if thread_id in replied_ids:
                triage_counts["SKIPPED"] += 1
                continue

            bucket = triage(text)
            triage_counts[bucket] += 1

            print(f"\n  @{author_name} [{bucket}]")
            print(f"  \"{text[:120]}{'...' if len(text) > 120 else ''}\"")

            if bucket == "NOISE":
                print("  → Skipping (NOISE).")
                continue

            reply = generate_reply(text, author_name, bucket)
            print(f"  → Reply: \"{reply}\"")

            if not dry_run:
                post_urn_full = f"urn:li:activity:{urn}"
                success = post_comment_reply(client, post_urn_full, comment_urn, reply)
                if success:
                    print(f"  [+] Posted ✓")
                    log_reply(thread_id, author_name, text, reply, bucket)
                    replied_ids.add(thread_id)
                    reply_count += 1
                    send_telegram(
                        f"💬 <b>Reply Posted</b>\n\n"
                        f"<b>[{bucket}]</b> → @{author_name}\n\n"
                        f"<i>{text[:200]}</i>\n\n"
                        f"<blockquote>{reply}</blockquote>",
                        cfg
                    )
                    cooldown = random.randint(12, 28)
                    print(f"  [cooldown {cooldown}s]")
                    time.sleep(cooldown)
                else:
                    print(f"  [-] Failed to post reply.")
            else:
                print("  → [dry-run] Would post above.")
                replied_ids.add(thread_id)
                reply_count += 1

    print("\n" + "=" * 60)
    print(f"  Done. Replies: {reply_count}  |  Triage: {triage_counts}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="LinkedIn Reply Monitor (linkedin-api, no browser).")
    parser.add_argument("--dry-run", action="store_true", help="Preview without posting")
    parser.add_argument("--max", type=int, default=10, help="Max replies per run")
    parser.add_argument("--post-count", type=int, default=10, help="Number of recent posts to scan")
    args = parser.parse_args()
    run(dry_run=args.dry_run, max_replies=args.max, post_count=args.post_count)


if __name__ == "__main__":
    main()

