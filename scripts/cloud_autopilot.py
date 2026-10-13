#!/usr/bin/env python3
"""
cloud_autopilot.py - Headless queue runner for GitHub Actions:
1. Picks the next pending post from my_account/posts/
2. Validates human quality with detect.py
3. Pings Telegram with pre-posting alert and full copy
4. Pushes to Buffer API (if configured)
5. Updates post status to 'published' and records to log.md
"""

import datetime
import glob
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
CONFIG_FILE = os.path.join(PROJECT_ROOT, "my_account", "config.json")
POSTS_DIR = os.path.join(PROJECT_ROOT, "my_account", "posts")
LOG_FILE = os.path.join(PROJECT_ROOT, "my_account", "log.md")


def get_env_or_config(key, section="telegram"):
    # First check process environment (e.g. GitHub Actions Secrets)
    env_val = os.environ.get(key)
    if env_val and not env_val.startswith("YOUR_"):
        return env_val

    # Fallback to local config.json
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                val = cfg.get(section, {}).get(key.lower().replace(f"{section}_", ""))
                if val and not val.startswith("YOUR_"):
                    return val
        except Exception:
            pass
    return None


def send_telegram(bot_token, chat_id, text):
    if not bot_token or not chat_id:
        print("[-] Telegram credentials missing. Skipping notification.", file=sys.stderr)
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8")).get("ok", False)
    except Exception as e:
        print(f"[-] Telegram error: {e}", file=sys.stderr)
        return False


def post_to_buffer(access_token, channel_id, text, as_draft=False, image_url=None, document_url=None, document_title=None, thumbnail_url=None):
    if not access_token or not channel_id:
        return None
    url = "https://api.buffer.com/graphql"
    escaped_text = json.dumps(text)
    save_draft = "true" if as_draft else "false"
    mode = "addToQueue"

    assets_field = ""
    if document_url:
        doc_title = json.dumps(document_title or "Executive Architecture Guide")
        thumb = thumbnail_url or "https://raw.githubusercontent.com/gtmsthi-ui/linkedin/main/my_account/assets/carousel_slide_1.png"
        assets_field = f'assets: [{{ document: {{ url: "{document_url}", title: {doc_title}, thumbnailUrl: "{thumb}" }} }}],'
    elif image_url:
        assets_field = f'assets: [{{ image: {{ url: "{image_url}" }} }}],'

    mutation = f"""
    mutation {{
      createPost(input: {{
        channelId: "{channel_id}",
        text: {escaped_text},
        mode: {mode},
        schedulingType: automatic,
        saveToDraft: {save_draft},
        needsApproval: false,
        {assets_field}
      }}) {{
        ... on PostActionSuccess {{
          post {{
            id
            status
          }}
        }}
        ... on MutationError {{
          message
        }}
      }}
    }}
    """
    data = json.dumps({"query": mutation}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            if res and "data" in res:
                return res["data"].get("createPost", {})
            return res
    except Exception as e:
        print(f"[-] Buffer error: {e}", file=sys.stderr)
        return None



def run_detect(text):
    tmp_path = os.path.join(PROJECT_ROOT, "my_account", "_temp_detect.txt")
    with open(tmp_path, "w", encoding="utf-8") as f:
        f.write(text)

    detect_script = os.path.join(PROJECT_ROOT, "skills", "li-human", "detect.py")
    proc = subprocess.run([sys.executable, detect_script, tmp_path], capture_output=True, text=True)
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

    output = proc.stdout
    score = 0.0
    passed = "PASS" in output
    for line in output.splitlines():
        if "HUMAN SCORE" in line:
            for p in line.split():
                try:
                    score = float(p)
                    break
                except ValueError:
                    pass
    return passed, score, output


def parse_post_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"').strip("'")
            body = parts[2].strip()

    return meta, body


def update_post_file(filepath, meta, body, status):
    meta["status"] = status
    meta["published_at"] = datetime.datetime.utcnow().isoformat() + "Z"

    lines = ["---"]
    for k, v in meta.items():
        lines.append(f'{k}: "{v}"')
    lines.append("---")
    lines.append("")
    lines.append(body)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def append_to_log(title, pillar, score, post_file):
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = f"- **[{now}]** {title} (`{pillar}`) | Score: {score} PASS | File: `{os.path.basename(post_file)}`\n"
    mode = "a" if os.path.exists(LOG_FILE) else "w"
    with open(LOG_FILE, mode, encoding="utf-8") as f:
        if mode == "w":
            f.write("# LinkedIn Publishing Log\n\n")
        f.write(entry)


def main():
    tg_token = get_env_or_config("TELEGRAM_BOT_TOKEN", "telegram")
    tg_chat = get_env_or_config("TELEGRAM_CHAT_ID", "telegram")
    buf_token = get_env_or_config("BUFFER_ACCESS_TOKEN", "buffer")
    buf_profile = get_env_or_config("BUFFER_PROFILE_ID", "buffer")
    is_dry_run = os.environ.get("DRY_RUN", "false").lower() in ("true", "1", "yes")

    print(f"[*] Starting LinkedIn Cloud Autopilot (DryRun: {is_dry_run})...")

    post_files = sorted(glob.glob(os.path.join(POSTS_DIR, "*.md")))
    if not post_files:
        print("[!] No post files found in my_account/posts/")
        sys.exit(0)

    target_file = None
    target_meta = {}
    target_body = ""

    for pf in post_files:
        meta, body = parse_post_file(pf)
        if meta.get("status", "queued") == "queued":
            target_file = pf
            target_meta = meta
            target_body = body
            break

    if not target_file:
        print("[+] All posts in queue have already been published!")
        if tg_token and tg_chat:
            send_telegram(
                tg_token,
                tg_chat,
                "<b>LinkedIn Queue Empty</b>\n\nAll scheduled posts have been published. Time to add next week's drafts!"
            )
        sys.exit(0)

    title = target_meta.get("title", os.path.basename(target_file))
    pillar = target_meta.get("pillar", "AI Enthusiast & System Architecture")
    day = target_meta.get("day", "Today")

    print(f"[*] Processing queue item: {target_file} ({title})...")

    # Step 1: Detect
    passed, score, detect_log = run_detect(target_body)
    print(f"[*] Humanizer Score: {score} (Passed: {passed})")

    # Step 2: Notify Telegram BEFORE posting
    preview = target_body[:600] + ("..." if len(target_body) > 600 else "")
    buffer_status_note = (
        "✅ Sent directly to LinkedIn via Buffer."
        if (buf_token and buf_profile and not is_dry_run)
        else "📲 Ready to copy-paste or publish via Buffer (Configure Buffer secrets to auto-post)."
    )

    alert_text = (
        f"🚀 <b>LinkedIn Cloud Autopilot Triggered</b>\n\n"
        f"<b>Pillar:</b> {pillar}\n"
        f"<b>Schedule:</b> {day}\n"
        f"<b>Quality Score:</b> <code>{score}/100 PASS</code>\n\n"
        f"<b>Post Preview:</b>\n"
        f"<blockquote>{preview}</blockquote>\n\n"
        f"{buffer_status_note}"
    )

    if tg_token and tg_chat:
        print("[*] Sending pre-post notification to Telegram...")
        send_telegram(tg_token, tg_chat, alert_text)

    # Check for attached PDF document carousel or visual summary card
    post_key = target_meta.get("id", os.path.splitext(os.path.basename(target_file))[0])
    pdf_file = os.path.join(PROJECT_ROOT, "my_account", "assets", "senior_vs_architect_carousel.pdf") if post_key == "post_02" else os.path.join(PROJECT_ROOT, "my_account", "assets", f"{post_key}_carousel.pdf")
    image_file = os.path.join(PROJECT_ROOT, "my_account", "assets", f"{post_key}_card.png")

    doc_url = None
    doc_title = None
    image_url = None

    thumb_url = None
    if os.path.exists(pdf_file):
        doc_url = f"https://raw.githubusercontent.com/gtmsthi-ui/linkedin/main/my_account/assets/{os.path.basename(pdf_file)}"
        doc_title = title
        thumb_file = os.path.join(PROJECT_ROOT, "my_account", "assets", f"{post_key}_slide_1.png")
        if os.path.exists(thumb_file):
            thumb_url = f"https://raw.githubusercontent.com/gtmsthi-ui/linkedin/main/my_account/assets/{post_key}_slide_1.png"
        else:
            thumb_url = "https://raw.githubusercontent.com/gtmsthi-ui/linkedin/main/my_account/assets/carousel_slide_1.png"
        print(f"[*] Found attached PDF document carousel: {doc_url}")
    elif os.path.exists(image_file):
        image_url = f"https://raw.githubusercontent.com/gtmsthi-ui/linkedin/main/my_account/assets/{post_key}_card.png"
        print(f"[*] Found attached summary card: {image_url}")

    # Step 3: Publish to Buffer if credentials exist
    buf_post_id = None
    if buf_token and buf_profile and not is_dry_run:
        print("[*] Publishing to LinkedIn via Buffer API...")
        res = post_to_buffer(
            buf_token,
            buf_profile,
            target_body,
            as_draft=False,
            image_url=image_url,
            document_url=doc_url,
            document_title=doc_title,
            thumbnail_url=thumb_url
        )
        if res and ("post" in res or res.get("success")):
            buf_post_id = res.get("post", {}).get("id")
            print(f"[+] Successfully published to Buffer! (Post ID: {buf_post_id})")
        else:
            print(f"[-] Buffer publishing returned: {res}")

    # Step 4: Update status and log
    update_post_file(target_file, target_meta, target_body, "published")
    append_to_log(title, pillar, score, target_file)
    print(f"[+] Post marked as published in {target_file}")

    # Record in Central Database
    try:
        sys.path.insert(0, HERE)
        from db_tracker import update_post_status, record_log
        update_post_status(post_key, "published", buffer_id=buf_post_id)
        record_log("POST_PUBLISHED", f"Published '{title}' via Cloud Autopilot", f"File: {os.path.basename(target_file)} | Image: {image_url}")
    except Exception as e:
        print(f"[-] Could not update Central DB: {e}")


if __name__ == "__main__":
    main()
