@echo off
title LinkedIn Autonomous Engagement Assistant
cd /d "%~dp0"
echo ======================================================================
echo           LINKEDIN AUTONOMOUS ENGAGEMENT ASSISTANT
echo ======================================================================
echo.
echo [1/2] Browsing Feed & Leaving 2 High-Value Architecture Comments...
echo [2/2] Scanning Notifications for Inbound Comments & Replies...
echo.
python scripts\linkedin_manager.py --all
echo.
echo ======================================================================
echo Routine Complete! Check Telegram on your phone for full receipts.
echo ======================================================================
pause
