# LinkedIn Automation & Telegram Setup Guide

This setup connects your LinkedIn content pipeline to:
1. **Buffer API:** Safely queues and schedules your posts directly to LinkedIn (100% compliant with LinkedIn's partner API, zero ban risk).
2. **Telegram Bot:** Pings your phone with post previews, scheduled timings, and reminders.

---

## Step 1: Set up your Telegram Bot (Takes 2 minutes)

1. Open Telegram and search for `@BotFather`.
2. Send `/newbot`, choose a name (e.g. `MyLinkedInArchitectBot`), and get your **HTTP API Token**.
3. Start a conversation with your new bot (click Start).
4. Search for `@userinfobot` on Telegram and send `/start` to see your **Id** (this is your `chat_id`).

---

## Step 2: Set up Buffer API (Free Plan Supported)

1. Go to [buffer.com](https://buffer.com) and create a free account.
2. Connect your **LinkedIn Profile**.
3. Create a Buffer developer token:
   - Go to [buffer.com/developers/apps/create](https://buffer.com/developers/apps/create) (or Access Tokens under your Buffer dashboard).
   - Generate your `access_token`.
4. Run this command to discover your connected LinkedIn Profile ID:
   ```bash
   python my_account/buffer_publisher.py --profiles
   ```

---

## Step 3: Configure `my_account/config.json`

Copy `my_account/config.example.json` to `my_account/config.json` and fill in your values:

```json
{
  "telegram": {
    "bot_token": "YOUR_TELEGRAM_BOT_TOKEN",
    "chat_id": "YOUR_TELEGRAM_CHAT_ID"
  },
  "buffer": {
    "access_token": "YOUR_BUFFER_ACCESS_TOKEN",
    "profile_id": "YOUR_BUFFER_LINKEDIN_PROFILE_ID"
  }
}
```

---

## Step 4: Test Your Setup

1. **Test Telegram:**
   ```bash
   python my_account/telegram_notifier.py --test
   ```
   *(You should immediately get a ping on your phone!)*

2. **Test Post Pipeline (Dry Run):**
   ```bash
   python my_account/publish_pipeline.py my_account/draft_01.txt --dry-run
   ```

3. **Publish & Schedule for Real:**
   ```bash
   python my_account/publish_pipeline.py my_account/draft_01.txt --pillar "Practical AI" --time "Tuesday 8:15 AM"
   ```
