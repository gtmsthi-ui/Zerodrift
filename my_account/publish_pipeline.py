#!/usr/bin/env python3
"""
publish_pipeline.py - Complete workflow:
1. Validates & scores draft with detect.py
2. Schedules post via Buffer API
3. Sends Telegram push notification with full preview & schedule timings
"""

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)

from buffer_publisher import schedule_buffer_post
from telegram_notifier import format_post_alert, send_telegram_message


def run_humanizer_check(draft_path):
    detect_script = os.path.join(PROJECT_ROOT, "skills", "li-human", "detect.py")
    cmd = [sys.executable, detect_script, draft_path]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    
    # Check output for HUMAN SCORE and PASS/REVIEW
    output = proc.stdout
    score = None
    passed = False
    
    for line in output.splitlines():
        if "HUMAN SCORE" in line:
            parts = line.split()
            for p in parts:
                try:
                    score = float(p)
                    break
                except ValueError:
                    continue
            if "PASS" in line:
                passed = True
                
    return passed, score, output


def main():
    parser = argparse.ArgumentParser(description="Validate, schedule, and notify LinkedIn post.")
    parser.add_argument("draft", help="Path to draft text file")
    parser.add_argument("--pillar", default="Practical AI & System Architecture", help="Content pillar name")
    parser.add_argument("--time", default="Tuesday 8:15 AM", help="Scheduled posting time description")
    parser.add_argument("--epoch", type=int, default=None, help="Optional Unix timestamp for Buffer scheduling")
    parser.add_argument("--dry-run", action="store_true", help="Validate and send Telegram alert without calling Buffer")

    args = parser.parse_args()

    if not os.path.exists(args.draft):
        print(f"[-] Draft file not found: {args.draft}", file=sys.stderr)
        sys.exit(1)

    with open(args.draft, "r", encoding="utf-8") as f:
        draft_content = f.read()

    print(f"[*] Step 1: Running detect.py on {args.draft}...")
    passed, score, detect_output = run_humanizer_check(args.draft)

    print(detect_output)

    if not passed and not args.dry_run:
        print("[-] Post did not pass human detection (needs score >= 70). Halting publish.", file=sys.stderr)
        sys.exit(1)

    # Step 2: Buffer
    if args.dry_run:
        print("[*] Dry run mode: Skipping Buffer API call.")
    else:
        print("[*] Step 2: Pushing to Buffer queue...")
        res = schedule_buffer_post(draft_content, scheduled_at=args.epoch)
        if not res:
            print("[-] Buffer scheduling failed. Halting.", file=sys.stderr)
            sys.exit(1)

    # Step 3: Telegram notification
    print("[*] Step 3: Sending Telegram confirmation alert...")
    alert_msg = format_post_alert(
        post_text=draft_content,
        scheduled_time=args.time,
        pillar=args.pillar,
        human_score=score
    )
    send_telegram_message(alert_msg)
    print("[+] Pipeline complete!")


if __name__ == "__main__":
    main()
