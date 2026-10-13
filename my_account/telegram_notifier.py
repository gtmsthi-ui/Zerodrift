#!/usr/bin/env python3
"""
telegram_notifier.py - Sends LinkedIn draft notifications and schedule alerts to your phone via Telegram.
Zero external dependencies (uses standard library urllib).
"""

import json
import os
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(HERE, "config.json")


def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def send_telegram_message(message_text, bot_token=None, chat_id=None):
    if not bot_token or not chat_id:
        cfg = load_config()
        if not cfg or "telegram" not in cfg:
            print("[-] Error: No config.json found or telegram credentials missing.", file=sys.stderr)
            return False
        bot_token = bot_token or cfg["telegram"].get("bot_token")
        chat_id = chat_id or cfg["telegram"].get("chat_id")

    if not bot_token or bot_token.startswith("YOUR_"):
        print("[-] Error: Telegram bot token not configured in my_account/config.json", file=sys.stderr)
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message_text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"}
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("ok"):
                print("[+] Telegram alert successfully sent!")
                return True
            else:
                print(f"[-] Telegram API error: {result}", file=sys.stderr)
                return False
    except Exception as e:
        print(f"[-] Failed to send Telegram message: {e}", file=sys.stderr)
        return False


def format_post_alert(post_text, scheduled_time, pillar, human_score=None):
    preview = post_text.strip()
    if len(preview) > 600:
        preview = preview[:597] + "..."

    score_str = f"<b>{human_score}/100 PASS</b>" if human_score else "Checked"

    msg = (
        f"<b>LinkedIn Post Ready & Scheduled</b>\n\n"
        f"<b>Pillar:</b> {pillar}\n"
        f"<b>Scheduled Time:</b> {scheduled_time}\n"
        f"<b>AI Humanizer Score:</b> {score_str}\n\n"
        f"<b>Post Preview:</b>\n"
        f"<blockquote>{preview}</blockquote>\n\n"
        f"<i>Check Buffer to modify or confirm publishing!</i>"
    )
    return msg


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("[*] Testing Telegram notification...")
        test_msg = (
            "<b>Antigravity LinkedIn Bot Connected!</b>\n\n"
            "Your notifications and schedule reminders will be sent to this chat."
        )
        send_telegram_message(test_msg)
    else:
        print("Usage: python telegram_notifier.py --test")
