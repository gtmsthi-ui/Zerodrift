#!/usr/bin/env python3
"""
auto_reply_monitor.py - Autonomous Reply & Notification Monitor:
1. Monitors https://www.linkedin.com/notifications/ for:
   - Comments on your own posts ("commented on your post")
   - Replies to your comments on other people's posts ("replied to your comment")
2. Navigates into the exact thread
3. Triages the comment (LEAD vs SUBSTANCE vs PEER)
4. Drafts a tailored Senior Architect reply (humanized, zero slop)
5. Types and submits with natural human keystroke cadence
6. Sends an instant receipt to your phone on Telegram
7. Strictly prevents infinite reply loops or spam
"""

import argparse
import asyncio
import datetime
import json
import os
import random
import re
import sys
import urllib.parse
import urllib.request
from playwright.async_api import async_playwright

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
USER_DATA_DIR = os.path.join(PROJECT_ROOT, "my_account", "browser_session")
CONFIG_FILE = os.path.join(PROJECT_ROOT, "my_account", "config.json")
ENGAGEMENT_LOG = os.path.join(PROJECT_ROOT, "my_account", "engagement_log.md")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def send_telegram(text):
    cfg = load_config()
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
        print(f"[-] Telegram alert failed: {e}", file=sys.stderr)


def get_replied_ids():
    if not os.path.exists(ENGAGEMENT_LOG):
        return set()
    replied = set()
    with open(ENGAGEMENT_LOG, "r", encoding="utf-8") as f:
        for line in f:
            m = re.search(r"Thread-ID:\s*([^\s]+)", line)
            if m:
                replied.add(m.group(1).strip())
    return replied


def log_reply(thread_id, commenter, their_text, my_reply, event_type):
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


def generate_contextual_reply(comment_text, commenter_name, is_reply_to_my_comment=False):
    lower = comment_text.lower()
    first_name = commenter_name.split()[0] if commenter_name else ""
    salutation = f"@{first_name} " if first_name else ""

    # If it's a direct lead inquiry (asking how, cost, architecture help)
    if any(k in lower for k in ["how do you", "template", "pricing", "cost", "work together", "can you share", "guide"]):
        return (
            f"{salutation}Good question. In our pipeline, we decoupled schema validation "
            f"from the downstream ingestion layer, which cut payload errors by 85%. "
            f"Happy to share the sanitized ADR or architecture layout if it helps your team."
        )

    # If technical disagreement or deep nuance
    if any(k in lower for k in ["disagree", "trade-off", "depends", "however", "latency", "bottleneck", "overhead"]):
        return (
            f"{salutation}Spot on point. That trade-off holds true until your request volume doubles, "
            f"at which point network serialization becomes the dominant cost. "
            f"Appreciate the thoughtful nuance."
        )

    # General continuation / peer response
    if is_reply_to_my_comment:
        return (
            f"{salutation}Exactly. The architectural mistake people make is optimizing for "
            f"theoretical throughput before knowing where the real production bottleneck sits. "
            f"Glad we're aligned here."
        )

    # Short thoughtful reply
    return (
        f"{salutation}Appreciate the comment. That aligns with what we've seen across "
        f"multiple distributed systems migrations. Thanks for jumping in."
    )


async def human_type(element, text):
    for char in text:
        await element.type(char, delay=random.randint(35, 90))
        if char in ".!?,":
            await asyncio.sleep(random.uniform(0.2, 0.5))


async def run_reply_monitor(dry_run=False, max_replies=4):
    replied_ids = get_replied_ids()
    print(f"[*] Starting Autonomous Reply Monitor (Max: {max_replies} replies)...")

    os.makedirs(USER_DATA_DIR, exist_ok=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = await browser.new_page()

        print("[*] Navigating to LinkedIn Notifications...")
        await page.goto("https://www.linkedin.com/notifications/", wait_until="domcontentloaded")
        await asyncio.sleep(4)

        cookies = await browser.cookies()
        has_li_at = any(c.get("name") == "li_at" for c in cookies)
        if not has_li_at or "login" in page.url or "checkpoint" in page.url or "authwall" in page.url:
            print("[-] Not logged in: LinkedIn authentication cookie ('li_at') is missing.")
            print("[!] Please run: python scripts/linkedin_engage.py --login")
            print("[!] Log in inside the Chromium window that pops up until your feed loads.")
            await browser.close()
            return

        # Scan notifications
        notif_cards = await page.query_selector_all(".nt-card, article.nt-card")
        print(f"[*] Scanning {len(notif_cards)} notifications...")

        reply_count = 0

        for idx, card in enumerate(notif_cards[:15]):
            if reply_count >= max_replies:
                break

            card_text = await card.inner_text()
            clean_brief = re.sub(r"\s+", " ", card_text)[:90]
            print(f"  [Notif {idx+1}] {clean_brief}...")
            lower_text = card_text.lower()

            is_comment_on_my_post = "commented on your post" in lower_text
            is_reply_to_my_comment = "replied to your comment" in lower_text

            if not (is_comment_on_my_post or is_reply_to_my_comment):
                continue

            # Thread ID from hash of notification snippet
            clean_snippet = re.sub(r"\s+", " ", card_text)[:60]
            thread_id = str(abs(hash(clean_snippet)))

            if thread_id in replied_ids:
                continue

            event_type = "Replied to comment on your post" if is_comment_on_my_post else "Replied to comment thread"
            print(f"\n[+] Actionable interaction detected: {clean_snippet}...")

            # Click notification to open thread
            await card.click()
            await asyncio.sleep(random.uniform(4.0, 6.0))

            # Look for reply button on the latest comment
            reply_buttons = await page.query_selector_all("button[aria-label*='Reply'], button:has-text('Reply')")
            if not reply_buttons:
                print("[-] Could not find Reply button in thread.")
                await page.goto("https://www.linkedin.com/notifications/")
                await asyncio.sleep(3)
                continue

            # Click the first or target reply button
            target_reply_btn = reply_buttons[0]
            await target_reply_btn.click()
            await asyncio.sleep(random.uniform(1.5, 2.5))

            # Locate reply text editor
            editor = await page.query_selector(".comments-comment-box__editor p, .editor-content p, div[role='textbox']")
            if not editor:
                print("[-] Reply editor box not found.")
                continue

            # Extract commenter name if available
            commenter_elem = await page.query_selector(".comments-post-meta__name-text, .update-components-actor__name")
            commenter_name = await commenter_elem.inner_text() if commenter_elem else "Peer"
            commenter_clean = commenter_name.split("\n")[0].strip()

            # Generate smart Architect reply
            reply_text = generate_contextual_reply(
                card_text,
                commenter_clean,
                is_reply_to_my_comment=is_reply_to_my_comment
            )

            print(f"[*] Generated Reply to @{commenter_clean}: \"{reply_text}\"")

            await editor.click()
            await asyncio.sleep(1)
            print("[*] Typing reply with human cadence...")
            await human_type(editor, reply_text)
            await asyncio.sleep(random.uniform(2.0, 3.5))

            if not dry_run:
                submit_btn = await page.query_selector(".comments-comment-box__submit-button, button:has-text('Post')")
                if submit_btn:
                    await submit_btn.click()
                    print(f"[+] Reply submitted successfully on LinkedIn!")
                    log_reply(thread_id, commenter_clean, card_text, reply_text, event_type)
                    replied_ids.add(thread_id)
                    reply_count += 1

                    # Send Telegram Alert
                    tg_msg = (
                        f"💬 <b>Autonomous LinkedIn Reply Posted</b>\n\n"
                        f"<b>Type:</b> {event_type}\n"
                        f"<b>To:</b> @{commenter_clean}\n\n"
                        f"<b>Your Reply:</b>\n"
                        f"<blockquote>{reply_text}</blockquote>\n\n"
                        f"<i>Thread successfully handled & logged.</i>"
                    )
                    send_telegram(tg_msg)

                    cooldown = random.randint(20, 35)
                    print(f"[*] Cooling down for {cooldown}s...")
                    await asyncio.sleep(cooldown)
            else:
                print("[*] [Dry-Run] Reply typed but not submitted.")
                reply_count += 1

            # Navigate back to notifications for next check
            await page.goto("https://www.linkedin.com/notifications/")
            await asyncio.sleep(random.uniform(3.0, 5.0))

        print(f"\n[+] Reply Monitor finished. Processed {reply_count} reply interaction(s).")
        await asyncio.sleep(2)
        await browser.close()


def main():
    parser = argparse.ArgumentParser(description="Autonomous LinkedIn Reply Monitor.")
    parser.add_argument("--dry-run", action="store_true", help="Preview typing without submitting")
    parser.add_argument("--max", type=int, default=4, help="Max replies per session (default: 4)")
    args = parser.parse_args()

    asyncio.run(run_reply_monitor(dry_run=args.dry_run, max_replies=args.max))


if __name__ == "__main__":
    main()
