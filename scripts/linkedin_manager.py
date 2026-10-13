#!/usr/bin/env python3
"""
linkedin_manager.py - Master Autonomous LinkedIn Executive Manager

Commands:
  1. Full Daily Routine (Feed comments + Inbound reply monitor):
     python scripts/linkedin_manager.py --all

  2. Autonomous Feed Engagement Only (2 high-value comments):
     python scripts/linkedin_manager.py --feed

  3. Autonomous Reply & Thread Monitor Only:
     python scripts/linkedin_manager.py --replies

  4. Publish Scheduled Post:
     python scripts/linkedin_manager.py --publish
"""

import argparse
import subprocess
import sys

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_feed():

    print("\n" + "=" * 60)
    print("🚀 [Step 1] Running Autonomous Feed Engagement (2 Comments/Day)...")
    print("=" * 60)
    subprocess.run([sys.executable, "scripts/auto_feed_browser.py"])


def run_replies():
    print("\n" + "=" * 60)
    print("💬 [Step 2] Running Autonomous Reply & Notification Monitor...")
    print("=" * 60)
    subprocess.run([sys.executable, "scripts/auto_reply_monitor.py"])


def run_publish():
    print("\n" + "=" * 60)
    print("📅 [Step 3] Publishing Next Scheduled Post from Queue...")
    print("=" * 60)
    subprocess.run([sys.executable, "scripts/cloud_autopilot.py"])


def run_status():
    subprocess.run([sys.executable, "scripts/db_tracker.py", "--summary"])


def main():
    parser = argparse.ArgumentParser(description="Master Autonomous LinkedIn Manager.")
    parser.add_argument("--all", action="store_true", help="Run full daily engagement routine (Feed + Replies)")
    parser.add_argument("--feed", action="store_true", help="Run autonomous feed commenting only")
    parser.add_argument("--replies", action="store_true", help="Run autonomous reply/thread monitor only")
    parser.add_argument("--publish", action="store_true", help="Publish next queued post")
    parser.add_argument("--status", action="store_true", help="Display Central Database status dashboard")

    args = parser.parse_args()

    if args.all:
        run_feed()
        run_replies()
    elif args.feed:
        run_feed()
    elif args.replies:
        run_replies()
    elif args.publish:
        run_publish()
    elif args.status:
        run_status()
    else:
        run_status()


if __name__ == "__main__":
    main()
