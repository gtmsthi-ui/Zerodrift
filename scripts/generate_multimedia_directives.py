#!/usr/bin/env python3
"""
generate_multimedia_directives.py - Generates 60-second video scripts with timed
visual directives, carousel storyboards, and pre-publication audit checklists
using the aem-reliability-toolkit generator engine.
"""

import os
import sys
import re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
TOOLKIT_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, "..", "aem-reliability-toolkit"))
EDITIONS_DIR = os.path.join(PROJECT_ROOT, "my_account", "newsletter", "editions")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "my_account", "multimedia_directives")

sys.path.insert(0, TOOLKIT_ROOT)

try:
    from aem_ai_engine.generator.parser import TechnicalDocumentParser
except ImportError:
    TechnicalDocumentParser = None


def generate_timed_video_script(edition_path):
    with open(edition_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Extract metadata
    title_m = re.search(r'title:\s*["\']?(.*?)["\']?$', text, re.MULTILINE)
    title = title_m.group(1) if title_m else "Enterprise Systems Architecture"
    
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()

    # Extract key technical hooks
    first_para = body.split("\n\n")[0] if "\n\n" in body else body[:200]
    first_para = re.sub(r'#+\s*', '', first_para).strip()

    slug = re.sub(r'[^a-zA-Z0-9_-]+', '-', title.lower()).strip('-')[:35]
    out_file = os.path.join(OUTPUT_DIR, f"{slug}_video_script.md")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    script_content = f"""# 🎬 60-Second Technical Video Script & Timed Visual Directives
# TOPIC: {title}
# SOURCE REPO: https://github.com/gtmsthi-ui/aem-reliability-toolkit
# FORMAT: 9:16 Vertical (LinkedIn / YouTube Shorts) or 16:9 Landscape
# CADENCE: 130-140 words per minute (High authority, calm, concrete delivery)

---

### [00:00 - 00:08] SCENE 1: THE HOOK (PATTERN FAILURE)
- **Camera / Visual Directive:**
  - *Shot:* Tight medium close-up, sharp studio lighting, dark slate background.
  - *On-Screen Graphic (Overlay at 00:02):* Red warning badge: `[PRODUCTION INCIDENT: 504 TIMEOUT / LEAK DETECTED]`.
  - *B-Roll / Cutaway (00:04):* Terminal screen showing Grafana error spike or starving connection pools.
- **Spoken Audio (Architect Voice):**
  > "The most expensive optimization in production systems is the one that looks flawless in staging. Here is the silent failure mode that destroys SLAs under concurrency..."

---

### [00:08 - 00:22] SCENE 2: THE ROOT CAUSE (CODE & CONCURRENCY)
- **Camera / Visual Directive:**
  - *Shot:* Screen-share split view (Left: Gautam on webcam; Right: Code / Config file).
  - *Visual Directive:* Zoom into the specific anti-pattern (e.g., flat `0.88` cosine similarity threshold or unvetted table lock). Highlight key lines with an amber glow.
  - *Text Overlay (Lower Third):* `Root Cause: Unpartitioned Namespaces & Race Conditions`.
- **Spoken Audio:**
  > "{first_para[:180]}... Most teams treat this as a configuration detail. In high-throughput distributed systems, it's a structural flaw."

---

### [00:22 - 00:42] SCENE 3: THE ARCHITECTURAL SOLUTION (THE TOPOLOGY)
- **Camera / Visual Directive:**
  - *Shot:* Full-screen high-contrast dark diagram transition.
  - *Visual Directive:* Animated step-by-step flowchart:
    - Step 1: Compound Cryptographic Tenant Hash (`SHA256(Tenant + Role)`).
    - Step 2: Event-driven CDC cache invalidation via Debezium + Redis.
    - Step 3: Hard physical vector namespace isolation.
  - *Audio Effect:* Subtle technical digital click on each node appearance.
- **Spoken Audio:**
  > "Here is the production-safe standard we built in the AEM Reliability Toolkit: We isolate tenant memory cryptographically, enforce dynamic similarity gates, and trigger event-driven cache purges within 50 milliseconds of any source data mutation."

---

### [00:42 - 00:52] SCENE 4: VERIFICATION & GO-LIVE GATES
- **Camera / Visual Directive:**
  - *Shot:* Fast terminal screencast running the automated Python audit CLI.
  - *Visual Directive:* Green passing checks scroll by: `[PASS] 0 Cross-Tenant Leaks | [PASS] Sub-10ms WAL Replica Lag | [PASS] Zero Table Locks`.
  - *On-Screen Stat Callout:* `62 Automated Test Gates | 100% Deterministic`.
- **Spoken Audio:**
  > "Before touching production, every pipeline must pass automated verification gates. No unvetted migrations, no guesswork, and zero un-isolated vector collections."

---

### [00:52 - 01:00] SCENE 5: CALL TO ACTION (PORTFOLIO & NEWSLETTER)
- **Camera / Visual Directive:**
  - *Shot:* Return to centered camera.
  - *Visual Directive:* Surface clickable UI cards and GitHub repo tag:
    - Top Pill: `The Pragmatic Architect Newsletter (Issue #6)`
    - Bottom URL: `https://github.com/gtmsthi-ui/aem-reliability-toolkit`
- **Spoken Audio:**
  > "I've published the complete 4-slide field manual and open-source verification scripts. Read the deep-dive in The Pragmatic Architect newsletter at the link below. What’s your biggest caching headache in production right now?"

---

### 📋 Technical Production Checklist
- [ ] Aspect Ratio: 1080x1920 (Vertical Reel) & 1920x1080 (Desktop LinkedIn).
- [ ] Caption Style: Bold white text with neon cyan highlights on keywords (`0.88 Threshold`, `Tenant Key`, `CDC`).
- [ ] Sound Design: Low-frequency subtle tech ambient synth pad; zero distracting beats.
- [ ] Companion Asset: Attach the 4-slide PDF field manual to the video's LinkedIn launch post.
"""

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(script_content)

    print(f"[+] Successfully generated 60-second video script with timed visual directives:")
    print(f"    File: {os.path.relpath(out_file, PROJECT_ROOT)}")
    return out_file


if __name__ == "__main__":
    target = os.path.join(EDITIONS_DIR, "06_safe_semantic_caching_production.md")
    if len(sys.argv) > 1:
        target = sys.argv[1]
    generate_timed_video_script(target)
