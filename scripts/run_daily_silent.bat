@echo off
cd /d "D:\Visual-studio-project\linkedin-skill"
python scripts\linkedin_manager.py --all >> my_account\daily_cron.log 2>&1
