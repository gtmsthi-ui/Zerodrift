@echo off
REM ============================================================================
REM run_local_autopilot.bat - Local Execution Engine for LinkedIn & Buffer
REM Runs zero cloud minutes, zero cost, directly against your local machine.
REM ============================================================================

echo ============================================================================
echo  [LOCAL AUTOPILOT] SYNCHRONIZING BUFFER QUEUE & ARCHITECTURE PORTFOLIO
echo ============================================================================

cd /d "D:\Visual-studio-project\linkedin-skill"

REM 1. Verify Newsletter Guardrails
echo [*] Step 1: Running Newsletter Guardrail Check...
python scripts/newsletter_autopilot.py

REM 2. Prepare & Replenish Buffer Queue (Threshold: 3, Target: 4)
echo [*] Step 2: Checking Buffer Queue Stock & Synthesizing Cards...
python scripts/online_queue_autopilot.py --prepare --threshold=3 --target=4

REM 3. Rebuild Grounded RAG Corpus for Live Studio
echo [*] Step 3: Rebuilding Grounded RAG Corpus (67 Docs)...
python scripts/build_rag_corpus.py

REM 4. Sync & Schedule with Buffer API
echo [*] Step 4: Pushing Scheduled Posts to Buffer...
python scripts/online_queue_autopilot.py --sync-and-schedule

REM 5. Sync Website Hub
echo [*] Step 5: Updating ZeroDrift Publications Hub...
python scripts/sync_site_publications.py

echo ============================================================================
echo  [DONE] Local Autopilot Pass Complete! All posts queued to Buffer.
echo ============================================================================
pause

