#!/usr/bin/env python3
"""
fetch_comments_via_browser.py

Uses Playwright's real Chromium (correct TLS fingerprint, no profile lock)
to authenticate with the li_at cookie, then calls LinkedIn's Voyager API
from within the browser using page.evaluate() — bypassing all bot detection.

Outputs a JSON file: my_account/pending_comments.json
"""
import asyncio
import json
import os
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "my_account", "config.json")
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "my_account", "pending_comments.json")

from playwright.async_api import async_playwright


def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


async def fetch_comments():
    cfg = load_config()
    li_at = cfg["linkedin"]["li_at"]
    jsessionid = cfg["linkedin"].get("jsessionid", "")
    csrf = jsessionid.replace('"', "")

    print("[*] Launching Chromium (fresh context, no profile lock)...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-blink-features=AutomationControlled"]
        )
        ctx = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/131.0.0.0 Safari/537.36"
            )
        )

        # Inject cookies
        cookies = [
            {"name": "li_at", "value": li_at, "domain": ".linkedin.com", "path": "/", "secure": True, "httpOnly": True},
        ]
        if jsessionid:
            cookies.append({"name": "JSESSIONID", "value": f'"{jsessionid}"', "domain": ".linkedin.com", "path": "/", "secure": True})
        await ctx.add_cookies(cookies)

        page = await ctx.new_page()

        # Navigate to feed first (establishes session)
        print("[*] Loading LinkedIn feed to establish session...")
        await page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=30000)
        await asyncio.sleep(3)

        if "login" in page.url or "authwall" in page.url:
            print("[-] Session invalid — li_at cookie may be expired.")
            await browser.close()
            return

        print(f"[+] Session confirmed. URL: {page.url}")

        # Now call Voyager API from within the browser (bypasses TLS fingerprinting)
        print("[*] Fetching recent posts via Voyager API (in-browser fetch)...")
        posts_data = await page.evaluate("""
            async () => {
                const resp = await fetch('/voyager/api/feed/updatesV2?q=memberShareFeed&count=10&start=0', {
                    headers: {
                        'Accept': 'application/vnd.linkedin.normalized+json+2.1',
                        'x-li-lang': 'en_US',
                        'x-restli-protocol-version': '2.0.0',
                    },
                    credentials: 'include'
                });
                if (!resp.ok) return {error: resp.status, url: resp.url};
                return await resp.json();
            }
        """)

        if isinstance(posts_data, dict) and posts_data.get("error"):
            print(f"[-] Feed API error: {posts_data}")
            # Try alternative endpoint
            print("[*] Trying alternative endpoint...")
            posts_data = await page.evaluate("""
                async () => {
                    const resp = await fetch('/voyager/api/identity/profiles/gautam-sethi-1b944324/updates?count=10&start=0', {
                        headers: {
                            'Accept': 'application/vnd.linkedin.normalized+json+2.1',
                            'x-li-lang': 'en_US',
                        },
                        credentials: 'include'
                    });
                    if (!resp.ok) return {error: resp.status};
                    return await resp.json();
                }
            """)

        elements = posts_data.get("elements", []) if isinstance(posts_data, dict) else []
        print(f"[*] Posts found: {len(elements)}")

        if not elements:
            print("[*] Trying to scrape post URNs directly from profile page...")
            await page.goto(
                "https://www.linkedin.com/in/gautam-sethi-1b944324/recent-activity/all/",
                wait_until="domcontentloaded", timeout=30000
            )
            await asyncio.sleep(4)

            # Scrape activity URNs from page DOM
            urns = await page.evaluate("""
                () => {
                    const items = document.querySelectorAll('[data-urn], [data-id]');
                    const found = [];
                    items.forEach(el => {
                        const u = el.getAttribute('data-urn') || el.getAttribute('data-id');
                        if (u && u.includes('activity')) found.push(u);
                    });
                    return [...new Set(found)].slice(0, 10);
                }
            """)
            print(f"[*] Scraped {len(urns)} activity URNs from DOM")
            elements = [{"updateKey": u} for u in urns]

        # Now fetch comments for each post
        all_comments = []
        for elem in elements[:10]:
            urn = elem.get("updateKey") or elem.get("entityUrn", "")
            if not urn:
                continue
            encoded_urn = urn.replace(":", "%3A").replace(",", "%2C")
            print(f"[*] Fetching comments for: {urn[:60]}...")

            comments_data = await page.evaluate(f"""
                async () => {{
                    const resp = await fetch('/voyager/api/feed/comments?updateKey={encoded_urn}&count=50&start=0&q=comments', {{
                        headers: {{
                            'Accept': 'application/vnd.linkedin.normalized+json+2.1',
                            'x-li-lang': 'en_US',
                        }},
                        credentials: 'include'
                    }});
                    if (!resp.ok) return {{error: resp.status}};
                    return await resp.json();
                }}
            """)

            comment_elems = comments_data.get("elements", []) if isinstance(comments_data, dict) else []
            for c in comment_elems:
                text = ""
                msg = c.get("commentary") or c.get("message") or {}
                if isinstance(msg, dict):
                    text = msg.get("text", {}).get("text", "") or msg.get("text", "")
                actor = c.get("actor", {})
                name_obj = actor.get("name", {})
                name = name_obj.get("text", "") if isinstance(name_obj, dict) else str(name_obj)
                c_urn = c.get("entityUrn", "")
                if text and text.strip():
                    all_comments.append({
                        "post_urn": urn,
                        "comment_urn": c_urn,
                        "author": name.strip(),
                        "text": text.strip(),
                    })
                    print(f"  → @{name.strip()}: \"{text.strip()[:80]}\"")

        await browser.close()

        print(f"\n[+] Total comments fetched: {len(all_comments)}")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_comments, f, indent=2, ensure_ascii=False)
        print(f"[+] Saved to {OUTPUT_FILE}")
        return all_comments


def main():
    asyncio.run(fetch_comments())


if __name__ == "__main__":
    main()

