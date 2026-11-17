#!/usr/bin/env python3
"""
api_reply_monitor.py - LinkedIn Comment Reply Monitor via Voyager API

Uses LinkedIn's internal Voyager API with the li_at session cookie.
No browser automation needed — no bot detection, no redirect loops.

Steps:
  1. Fetches your recent posts via Voyager API
  2. Fetches comments on each post
  3. Triages each comment (LEAD / SUBSTANCE / PEER / SUPPORT / NOISE)
  4. Drafts a contextual reply in your voice
  5. Posts the reply via API (or dry-run: prints only)
  6. Sends a Telegram receipt per reply

Usage:
  python scripts/api_reply_monitor.py              # Live mode (posts replies)
  python scripts/api_reply_monitor.py --dry-run    # Preview only
  python scripts/api_reply_monitor.py --max 10     # Override reply cap (default 10)
"""

import argparse
import datetime
import json
import os
import random
import re
import sys
import time
import urllib.parse
import urllib.request

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "my_account", "config.json")
ENGAGEMENT_LOG = os.path.join(PROJECT_ROOT, "my_account", "engagement_log.md")

VOYAGER_BASE = "https://www.linkedin.com/voyager/api"
PROFILE_ID = "gautam-sethi-1b944324"

# ─────────────────────────────────────────────
# Config & session helpers
# ─────────────────────────────────────────────

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def build_headers(li_at: str, csrf_token: str = "") -> dict:
    """Build LinkedIn Voyager API request headers."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
        "Accept": "application/vnd.linkedin.normalized+json+2.1",
        "Accept-Language": "en-US,en;q=0.9",
        "x-li-lang": "en_US",
        "x-li-track": json.dumps({
            "clientVersion": "1.13.16",
            "mpVersion": "1.13.16",
            "osName": "web",
            "timezoneOffset": 5.5,
            "timezone": "Asia/Kolkata",
            "deviceFormFactor": "DESKTOP",
            "mpName": "voyager-web",
            "displayDensity": 1.5,
            "displayWidth": 1920,
            "displayHeight": 1080
        }),
        "Cookie": f"li_at={li_at}",
        "Referer": "https://www.linkedin.com/feed/",
    }
    if csrf_token:
        headers["csrf-token"] = csrf_token
    return headers


def voyager_get(path: str, params: dict, headers: dict) -> dict:
    """Make a GET request to the LinkedIn Voyager API."""
    qs = urllib.parse.urlencode(params)
    url = f"{VOYAGER_BASE}/{path}?{qs}" if qs else f"{VOYAGER_BASE}/{path}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        print(f"  [-] HTTP {e.code} on {path}: {body}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"  [-] Request failed on {path}: {e}", file=sys.stderr)
        return {}


def voyager_post(path: str, payload: dict, headers: dict) -> dict:
    """Make a POST request to the LinkedIn Voyager API."""
    url = f"{VOYAGER_BASE}/{path}"
    data = json.dumps(payload).encode("utf-8")
    post_headers = {**headers, "Content-Type": "application/json"}
    req = urllib.request.Request(url, data=data, headers=post_headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read()
            return json.loads(raw.decode("utf-8")) if raw else {}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:300]
        print(f"  [-] HTTP {e.code} on POST {path}: {body}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"  [-] POST failed on {path}: {e}", file=sys.stderr)
        return {}


# ─────────────────────────────────────────────
# Engagement log helpers
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


def log_reply(thread_id: str, commenter: str, their_text: str, my_reply: str, event_type: str):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = (
        f"- [{now}] {event_type} to @{commenter}:\n"
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
# Telegram notification
# ─────────────────────────────────────────────

def send_telegram(text: str, cfg: dict):
    token = cfg.get("telegram", {}).get("bot_token")
    chat_id = cfg.get("telegram", {}).get("chat_id")
    if not token or not chat_id:
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=15)
    except Exception as e:
        print(f"  [-] Telegram alert failed: {e}", file=sys.stderr)


# ─────────────────────────────────────────────
# Comment triage & reply generation
# ─────────────────────────────────────────────

def triage_comment(text: str) -> str:
    """Sort comment into LEAD / SUBSTANCE / PEER / SUPPORT / NOISE."""
    lower = text.lower()
    # NOISE: pitches, spam
    if any(k in lower for k in ["dm me", "check out my", "i help", "book a call", "free consultation", "click here"]):
        return "NOISE"
    # LEAD: asking how, requesting help/template
    if any(k in lower for k in ["how do you", "how did you", "can you share", "template", "would love to", "could you", "any resources", "where can i"]):
        return "LEAD"
    # SUBSTANCE: technical pushback or deep engagement
    if any(k in lower for k in ["disagree", "however", "trade-off", "tradeoff", "depends on", "latency", "bottleneck", "overhead", "alternatively", "what about", "have you considered", "actually"]):
        return "SUBSTANCE"
    # PEER: name-drops their experience or adds a data point
    if any(k in lower for k in ["we've", "we have", "in our team", "at my company", "from experience", "i've seen", "i've built", "similar thing"]):
        return "PEER"
    # SUPPORT: short affirmation
    return "SUPPORT"


def generate_reply(comment_text: str, commenter_name: str, bucket: str) -> str:
    """
    Generate a contextual reply in Gautam's voice:
    - Senior Architect / AI practitioner tone
    - Concrete, no buzzwords, short paragraphs
    - Addresses the actual point raised
    """
    first = commenter_name.split()[0] if commenter_name else ""
    sal = f"{first} — " if first else ""
    lower = comment_text.lower()

    if bucket == "LEAD":
        if "template" in lower or "share" in lower:
            return (
                f"{sal}happy to share the structure we use. "
                "The key is separating schema validation from ingestion — "
                "once you decouple those, payload errors drop significantly. "
                "Send me a connection request and I'll pass it across."
            )
        if "how" in lower:
            return (
                f"{sal}the short answer: start with the execution boundary, not the model. "
                "Define a strict input/output schema first, then wrap the LLM call in a retry harness "
                "with deterministic fallback. Most teams skip that and pay for it in production reliability."
            )
        return (
            f"{sal}good question. "
            "The pattern that worked for us was treating the LLM as an untrusted microservice "
            "with bounded retries and schema-gated outputs. Happy to go deeper if useful."
        )

    if bucket == "SUBSTANCE":
        if "disagree" in lower or "actually" in lower:
            return (
                f"{sal}fair point — and I'd concede that holds true at lower scale. "
                "The calculus shifts once you're handling sustained load, "
                "at which point the serialization overhead becomes the dominant cost, not the logic. "
                "Appreciate the pushback, keeps the thinking honest."
            )
        return (
            f"{sal}exactly right. "
            "That trade-off is real and most teams don't hit it until they're already in production. "
            "The part that surprises people is how fast network round-trips dwarf compute costs. "
            "Good nuance."
        )

    if bucket == "PEER":
        return (
            f"{sal}solid — and that matches what we've seen across multiple migrations. "
            "The teams that move fastest are usually the ones who've already internalized the "
            "infra cost before writing the first line of orchestration code. "
            "Good to know it's consistent across orgs."
        )

    if bucket == "SUPPORT":
        # Short 3–8 word replies for support comments
        short_replies = [
            f"Thanks {first}. Glad it landed.",
            f"Appreciate it, {first}.",
            f"Thanks {first} — more to come.",
            f"Thanks {first}. Glad it's useful.",
        ]
        return random.choice(short_replies) if first else "Appreciate it — more to come."

    # NOISE — no reply
    return ""


# ─────────────────────────────────────────────
# LinkedIn Voyager API: fetch posts & comments
# ─────────────────────────────────────────────

def get_my_recent_posts(headers: dict) -> list:
    """Fetch recent posts from the user's profile via Voyager."""
    print(f"[*] Fetching recent posts for profile: {PROFILE_ID} ...")
    data = voyager_get(
        f"identity/profiles/{PROFILE_ID}/posts",
        params={"count": 10, "start": 0},
        headers=headers,
    )
    posts = []

    # Try paging data
    elements = data.get("data", {}).get("data", {}).get("identityDashProfileComponentsByPage", {}).get("elements", [])

    # Fallback: look in top-level elements
    if not elements:
        elements = data.get("elements", [])

    # Fallback: try feed endpoint
    if not elements:
        print("[*] Trying feed/updatesV2 endpoint...")
        data = voyager_get(
            "feed/updatesV2",
            params={
                "profileId": PROFILE_ID,
                "q": "memberShareFeed",
                "moduleKey": "member-shares:phone",
                "count": 10,
                "start": 0,
            },
            headers=headers,
        )
        elements = data.get("elements", [])

    for elem in elements:
        urn = elem.get("updateKey") or elem.get("entityUrn", "")
        if urn:
            posts.append({"urn": urn, "raw": elem})

    print(f"[*] Found {len(posts)} recent post(s).")
    return posts


def get_comments_for_post(update_urn: str, headers: dict) -> list:
    """Fetch comments on a given post URN."""
    encoded = urllib.parse.quote(update_urn, safe="")
    data = voyager_get(
        "feed/comments",
        params={
            "updateKey": update_urn,
            "count": 50,
            "start": 0,
            "q": "comments",
        },
        headers=headers,
    )
    elements = data.get("elements", [])
    comments = []
    for el in elements:
        text = el.get("commentary", {}).get("text", {}).get("text", "") or el.get("message", {}).get("text", "")
        actor = el.get("actor", {})
        name_obj = actor.get("name", {})
        name = name_obj.get("text", "") if isinstance(name_obj, dict) else str(name_obj)
        comment_urn = el.get("entityUrn", "")
        if text:
            comments.append({
                "urn": comment_urn,
                "text": text.strip(),
                "author": name.strip(),
            })
    return comments


def post_reply(parent_update_urn: str, parent_comment_urn: str, reply_text: str, headers: dict) -> bool:
    """Post a reply to a comment via Voyager API."""
    payload = {
        "actor": f"urn:li:member:{PROFILE_ID}",
        "message": {"attributes": [], "text": reply_text},
        "parentCommentUrn": parent_comment_urn,
        "updateKey": parent_update_urn,
    }
    result = voyager_post("feed/comments", payload, headers)
    return bool(result)


# ─────────────────────────────────────────────
# Main monitor loop
# ─────────────────────────────────────────────

def run_monitor(dry_run: bool = False, max_replies: int = 10):
    cfg = load_config()
    li_at = cfg.get("linkedin", {}).get("li_at") or os.environ.get("LINKEDIN_LI_AT", "")
    if not li_at:
        print("[-] No li_at cookie found in my_account/config.json. Cannot proceed.")
        sys.exit(1)

    # Extract CSRF token from JSESSIONID (LinkedIn uses it as the csrf-token)
    jsessionid = cfg.get("linkedin", {}).get("jsessionid", "")
    csrf = jsessionid.replace('"', "") if jsessionid else ""

    headers = build_headers(li_at, csrf)
    replied_ids = get_replied_ids()

    print("=" * 60)
    print(f"  LinkedIn API Reply Monitor  |  {'DRY RUN' if dry_run else 'LIVE'}")
    print(f"  Max replies: {max_replies}")
    print("=" * 60)

    posts = get_my_recent_posts(headers)
    if not posts:
        print("[!] No posts found. LinkedIn API may need a valid CSRF token.")
        print("[!] Try grabbing JSESSIONID from Chrome DevTools and adding it to config.json:")
        print('    "linkedin": { "li_at": "...", "jsessionid": "ajax:XXXX..." }')
        return

    reply_count = 0
    triage_summary = {"LEAD": 0, "SUBSTANCE": 0, "PEER": 0, "SUPPORT": 0, "NOISE": 0}

    for post in posts:
        if reply_count >= max_replies:
            break
        urn = post["urn"]
        print(f"\n[+] Post URN: {urn}")
        comments = get_comments_for_post(urn, headers)
        print(f"    {len(comments)} comment(s) found.")

        for comment in comments:
            if reply_count >= max_replies:
                break

            thread_id = str(abs(hash(comment["urn"] or comment["text"][:60])))
            if thread_id in replied_ids:
                print(f"    [skip] Already replied to @{comment['author']}")
                continue

            # Skip own comments
            author_lower = comment["author"].lower()
            if "gautam" in author_lower or "sethi" in author_lower:
                continue

            bucket = triage_comment(comment["text"])
            triage_summary[bucket] += 1

            print(f"\n    Comment by @{comment['author']} [{bucket}]:")
            print(f"    \"{comment['text'][:120]}...\"" if len(comment["text"]) > 120 else f"    \"{comment['text']}\"")

            if bucket == "NOISE":
                print("    [skip] NOISE — no reply.")
                continue

            reply_text = generate_reply(comment["text"], comment["author"], bucket)
            print(f"    Draft reply: \"{reply_text}\"")

            if not dry_run:
                success = post_reply(urn, comment["urn"], reply_text, headers)
                if success:
                    print(f"    [+] Reply posted to @{comment['author']}!")
                    log_reply(thread_id, comment["author"], comment["text"], reply_text, f"API reply [{bucket}]")
                    replied_ids.add(thread_id)
                    reply_count += 1
                    send_telegram(
                        f"💬 <b>LinkedIn Reply Posted</b>\n\n"
                        f"<b>Bucket:</b> {bucket}\n"
                        f"<b>To:</b> @{comment['author']}\n\n"
                        f"<b>Their comment:</b>\n<i>{comment['text'][:200]}</i>\n\n"
                        f"<b>Your reply:</b>\n<blockquote>{reply_text}</blockquote>",
                        cfg,
                    )
                    cooldown = random.randint(12, 25)
                    print(f"    [*] Cooling down {cooldown}s...")
                    time.sleep(cooldown)
                else:
                    print(f"    [-] Failed to post reply to @{comment['author']}.")
            else:
                print("    [dry-run] Would post above reply.")
                replied_ids.add(thread_id)
                reply_count += 1

    print("\n" + "=" * 60)
    print(f"  Done. Replies processed: {reply_count}")
    print(f"  Triage breakdown: {triage_summary}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="LinkedIn API Reply Monitor (no browser needed).")
    parser.add_argument("--dry-run", action="store_true", help="Draft replies without posting")
    parser.add_argument("--max", type=int, default=10, help="Max replies per run (default: 10)")
    args = parser.parse_args()
    run_monitor(dry_run=args.dry_run, max_replies=args.max)


if __name__ == "__main__":
    main()

