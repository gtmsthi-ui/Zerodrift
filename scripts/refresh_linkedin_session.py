#!/usr/bin/env python3
"""
refresh_linkedin_session.py - LinkedIn Session Cookie Refresher

Opens a fresh Chromium window (does NOT use the locked browser_session dir)
so you can log in manually. After login, captures the li_at and JSESSIONID
cookies and saves them directly into my_account/config.json.

Usage:
    python scripts/refresh_linkedin_session.py

Chrome/Chromium does NOT need to be closed first - this uses a fresh temp dir.
"""

import asyncio
import json
import os
import sys
import tempfile

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

try:
    from playwright.async_api import async_playwright
except ImportError:
    print("[-] Playwright not installed. Run: pip install playwright && playwright install chromium")
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "my_account", "config.json")


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print(f"[+] Config saved to {CONFIG_FILE}")


async def refresh_session():
    print("=" * 60)
    print("  LinkedIn Session Cookie Refresher")
    print("=" * 60)
    print()
    print("[*] Opening a FRESH Chromium window (separate from your regular Chrome).")
    print("[*] Log into LinkedIn normally. The script will capture your session.")
    print()

    # Use a fresh temp directory to avoid conflicting with any running Chrome
    tmp_dir = tempfile.mkdtemp(prefix="li_session_refresh_")
    print(f"[*] Using temp profile dir: {tmp_dir}")

    async with async_playwright() as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=tmp_dir,
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
                "--start-maximized",
            ],
            no_viewport=True,
        )

        page = await browser.new_page()
        await page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded")

        print("[*] Browser window is open. Please:")
        print("    1. Enter your LinkedIn email and password")
        print("    2. Complete any 2FA/verification if prompted")
        print("    3. Wait for your LinkedIn feed to load")
        print()
        print("[*] Waiting up to 5 minutes for login...")

        li_at = None
        jsessionid = None

        for _ in range(150):  # 150 x 2s = 5 minutes
            await asyncio.sleep(2)
            try:
                current_url = page.url
                cookies = await browser.cookies()
                cookie_map = {c["name"]: c["value"] for c in cookies}

                li_at = cookie_map.get("li_at")
                jsessionid = cookie_map.get("JSESSIONID")

                if li_at and (
                    "feed" in current_url
                    or "mynetwork" in current_url
                    or "messaging" in current_url
                    or "notifications" in current_url
                    or current_url.rstrip("/") == "https://www.linkedin.com"
                ):
                    print(f"\n[+] Login successful! LinkedIn session cookies captured.")
                    break
            except Exception:
                pass

        await asyncio.sleep(2)
        await browser.close()

        # Clean up temp dir
        try:
            import shutil
            shutil.rmtree(tmp_dir, ignore_errors=True)
        except Exception:
            pass

        if not li_at:
            print("\n[-] Login timed out or li_at cookie not found.")
            print("[!] Please try again and make sure your feed fully loads before 5 minutes.")
            return False

        # Save to config.json
        cfg = load_config()
        if "linkedin" not in cfg:
            cfg["linkedin"] = {}
        cfg["linkedin"]["li_at"] = li_at
        if jsessionid:
            cfg["linkedin"]["jsessionid"] = jsessionid
        save_config(cfg)

        print()
        print("=" * 60)
        print("  Session Refreshed Successfully!")
        print("=" * 60)
        print()
        print("[+] li_at cookie saved to my_account/config.json")
        if jsessionid:
            print("[+] JSESSIONID cookie saved to my_account/config.json")
        print()
        print("[*] You can now run the reply monitor:")
        print("    python scripts/auto_reply_monitor.py")
        print("    python scripts/auto_reply_monitor.py --dry-run  (to preview only)")
        return True


def main():
    asyncio.run(refresh_session())


if __name__ == "__main__":
    main()

