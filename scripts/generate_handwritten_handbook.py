#!/usr/bin/env python3
"""
generate_handwritten_handbook.py - Generates an authentic, high-resolution (1080x1440)
multi-page handwritten architectural handbook in GoodNotes / engineering notebook style,
compiling all pages into a swipeable PDF for LinkedIn document carousels.
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1440
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "my_account", "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

# Fonts
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 44)
FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 30)
FONT_H2 = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 32)
FONT_BODY = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 25)
FONT_SMALL = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 20)
FONT_COVER_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeprb.ttf", 56)
FONT_COVER_SUB = ImageFont.truetype("C:/Windows/Fonts/Inkfree.ttf", 34)

BG_COLOR = (252, 251, 248) # Warm cream notebook paper
DOT_COLOR = (215, 212, 202, 140)

def create_base_canvas(page_num, total_pages, title_header):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img, "RGBA")

    # Draw dot grid
    for x in range(60, WIDTH - 60, 40):
        for y in range(80, HEIGHT - 80, 40):
            draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=DOT_COLOR)

    # Top Margin line
    draw.line([(60, 70), (WIDTH - 60, 70)], fill=(225, 29, 72, 200), width=2)
    draw.text((60, 38), f"THE PRAGMATIC ARCHITECT • {title_header.upper()}", font=FONT_SMALL, fill=(100, 116, 139))
    draw.text((WIDTH - 200, 38), f"PAGE {page_num:02d} / {total_pages:02d}", font=FONT_SMALL, fill=(100, 116, 139))

    # Bottom Footer
    draw.line([(60, HEIGHT - 75), (WIDTH - 60, HEIGHT - 75)], fill=(203, 213, 225, 200), width=1)
    draw.text((60, HEIGHT - 60), "Gautam Sethi • AI Enthusiast & Systems Architect", font=FONT_SMALL, fill=(51, 65, 85))
    draw.text((WIDTH - 250, HEIGHT - 60), "Save & Repost ♻️", font=FONT_SMALL, fill=(10, 102, 194))

    return img, draw

def render_cover():
    img = Image.new("RGB", (WIDTH, HEIGHT), (248, 250, 252))
    draw = ImageDraw.Draw(img, "RGBA")

    # Grid
    for x in range(50, WIDTH - 50, 36):
        for y in range(60, HEIGHT - 60, 36):
            draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(203, 213, 225, 160))

    # Double border
    draw.rounded_rectangle([(40, 40), (WIDTH - 40, HEIGHT - 40)], radius=16, outline=(15, 23, 42), width=4)
    draw.rounded_rectangle([(48, 48), (WIDTH - 48, HEIGHT - 48)], radius=12, outline=(10, 102, 194), width=2)

    # Top badge
    draw.rounded_rectangle([(WIDTH//2 - 240, 120), (WIDTH//2 + 240, 175)], radius=10, fill=(10, 102, 194))
    draw.text((WIDTH//2 - 210, 132), "THE PRAGMATIC ARCHITECT • FIELD MANUAL", font=FONT_BODY, fill=(255, 255, 255))

    # Main Title
    draw.rectangle([(80, 240), (WIDTH - 80, 440)], fill=(254, 240, 138, 160)) # yellow highlighter
    draw.text((100, 250), "PRODUCTION AI &\nDISTRIBUTED SYSTEMS\nHANDBOOK", font=FONT_COVER_TITLE, fill=(15, 23, 42), spacing=12)

    draw.text((100, 470), "100 System Design Questions, Real-World SRE Failure Modes,\nand Deterministic Architectural Contracts", font=FONT_COVER_SUB, fill=(51, 65, 85), spacing=8)

    # Blueprint Contents Box
    y = 600
    draw.rounded_rectangle([(80, y), (WIDTH - 80, y + 540)], radius=14, fill=(255, 255, 255, 230), outline=(51, 65, 85), width=2)
    draw.text((110, y + 25), "📖 COMPLETE ARCHITECTURAL CURRICULUM:", font=FONT_H2, fill=(10, 102, 194))

    topics = [
        "1. Model Context Protocol (MCP) in Production Sandboxes",
        "2. Multi-Agent State Orchestration & Breaking Recursive Loops",
        "3. Safe Semantic Caching & The 500ms Invalidation Race",
        "4. Production RAG Architecture & Fallback Finite State Machines",
        "5. Zero-Downtime Database Architecture (Expand / Contract Pattern)",
        "6. AEM Edge Delivery Services (EDS) & Sub-50ms LCP Pipelines",
        "7. AEM Dispatcher Caching & The /statfileslevel 0 Catastrophe",
        "8. Linux Kernel eBPF Telemetry for JVM GC Pauses & Safepoints",
        "9. Multi-Region Active-Active Topologies & CRDT Conflict Resolution",
        "10. Staff+ Technical Governance & Executable CI/CD Fitness Functions"
    ]
    draw.text((110, y + 80), "\n".join(topics), font=FONT_BODY, fill=(30, 41, 59), spacing=14)

    # Author Sign-off
    draw.text((100, HEIGHT - 160), "Handwritten Field Notes by Gautam Sethi", font=FONT_SUBTITLE, fill=(15, 23, 42))
    draw.text((100, HEIGHT - 115), "AI Enthusiast • Ex-Enterprise Systems Lead", font=FONT_BODY, fill=(100, 116, 139))
    draw.text((WIDTH - 300, HEIGHT - 140), "SWIPE ➡️", font=FONT_COVER_SUB, fill=(10, 102, 194))

    return img

def render_content_page(page_num, total_pages, chapter_title, sub_hook, q1_title, q1_body, q2_title, q2_body, rule_title, rule_body):
    img, draw = create_base_canvas(page_num, total_pages, chapter_title.split(":")[0])

    # Title with highlight
    draw.rectangle([(55, 95), (WIDTH - 60, 160)], fill=(254, 240, 138, 140))
    draw.text((65, 102), chapter_title, font=FONT_TITLE, fill=(15, 23, 42))
    draw.text((65, 172), sub_hook, font=FONT_SUBTITLE, fill=(71, 85, 105))

    # Q1 Box
    y = 230
    draw.rounded_rectangle([(60, y), (WIDTH - 60, y + 330)], radius=12, fill=(255, 255, 255, 220), outline=(59, 130, 246, 220), width=2)
    draw.rounded_rectangle([(80, y - 14), (320, y + 16)], radius=6, fill=(37, 99, 235))
    draw.text((95, y - 12), "Q1: ARCHITECTURAL QUESTION", font=FONT_SMALL, fill=(255, 255, 255))
    draw.text((80, y + 26), q1_title, font=FONT_H2, fill=(30, 58, 138))
    draw.text((80, y + 78), q1_body, font=FONT_BODY, fill=(30, 41, 59), spacing=7)

    # Q2 Box
    y = 600
    draw.rounded_rectangle([(60, y), (WIDTH - 60, y + 410)], radius=12, fill=(248, 250, 252, 230), outline=(16, 185, 129, 220), width=2)
    draw.rounded_rectangle([(80, y - 14), (360, y + 16)], radius=6, fill=(5, 150, 105))
    draw.text((95, y - 12), "Q2: PRODUCTION FAILURE MODE & SRE FIX", font=FONT_SMALL, fill=(255, 255, 255))
    draw.text((80, y + 26), q2_title, font=FONT_H2, fill=(6, 78, 59))
    draw.text((80, y + 78), q2_body, font=FONT_BODY, fill=(30, 41, 59), spacing=7)

    # Senior Architect Invariant
    y = 1050
    draw.rounded_rectangle([(60, y), (WIDTH - 60, y + 175)], radius=12, fill=(254, 243, 199, 190), outline=(217, 119, 6), width=2)
    draw.text((80, y + 18), rule_title, font=FONT_H2, fill=(180, 83, 9))
    draw.text((80, y + 66), rule_body, font=FONT_BODY, fill=(120, 53, 15), spacing=6)

    return img

def build_full_handbook():
    print("[*] Generating 11-Page Handwritten Systems Architect Handbook...")
    pages = []

    # Cover
    pages.append(render_cover())

    # Page 2: MCP
    pages.append(render_content_page(
        page_num=2, total_pages=11,
        chapter_title="01: Model Context Protocol (MCP) in Production",
        sub_hook="Standardizing Enterprise AI Tool Ingestion & Out-of-Process Sandboxing",
        q1_title="Why is Model Context Protocol replacing custom LLM tool wrappers?",
        q1_body="1. Out-of-Process Isolation: Tools run in independent sandboxed processes (stdio/SSE)\n   protecting core API processes from unvetted code execution.\n2. Dynamic JSON-RPC 2.0 Negotiation: Agents dynamically query server capabilities,\n   eliminating bespoke parameter mapping glue code.\n3. Central Governance: Security teams enforce rate limits, auth scopes, and audit logging\n   at the gateway proxy without altering agent prompts.",
        q2_title="What is the primary failure mode of MCP under concurrency?",
        q2_body="FAILURE: Synchronous socket hangs. If a tool blocks on a slow DB query, the agent\nturn stalls and downstream HTTP clients throw 504 Gateway Timeouts.\n\nSRE FIX: The Asynchronous Job Ticket Pattern:\n• Tool returns an immediate jobId if execution exceeds 800ms.\n• Agent yields turn and receives an event-driven callback when the worker finishes.\n• Hard circuit breaker: Maximum 3 retries before fail-open fallback.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: PRINCIPLE OF LEAST PRIVILEGE",
        rule_body="Never grant an autonomous LLM write-tokens directly to live production tables.\nAll mutating actions must stage an immutable draft and await human-in-the-loop\nor deterministic policy assertion approval before execution."
    ))

    # Page 3: Multi-Agent FSMs
    pages.append(render_content_page(
        page_num=3, total_pages=11,
        chapter_title="02: Multi-Agent State Orchestration",
        sub_hook="Governing Multi-Agent Swarms as Deterministic Finite State Machines",
        q1_title="Why do conversational multi-agent loops fail in enterprise staging?",
        q1_body="1. The Polite Hallucination Loop: Two agents pass conversational summaries back\n   and forth without mutating state, burning $45+ in tokens in minutes.\n2. Context Poisoning: By turn 15, system rules get pushed out of the attention window.\n3. Distributed Deadlocks: Agent A blocks waiting on Agent B while B waits on A.",
        q2_title="How do Staff Architects structure reliable multi-agent workflows?",
        q2_body="THE ACTOR MODEL + DETERMINISTIC FSM BLUEPRINT:\n• Central Typed State Ledger: Agents do NOT communicate via free-form text.\n  They emit structured JSON state transitions validated against JSON Schema.\n• Ephemeral Sandboxes: Each agent gets a freshly pruned context window.\n• Bounded Test-Time Compute: Hard 8-hop circuit breakers to terminate loops.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: BOUNDED EXECUTION",
        rule_body="Autonomy without state machines is enterprise debt. Every multi-agent system\nmust have a deterministic Directed Acyclic Graph (DAG) with hard token budgets\nand an un-bypassable terminal exit state."
    ))

    # Page 4: Semantic Caching
    pages.append(render_content_page(
        page_num=4, total_pages=11,
        chapter_title="03: Safe Semantic Caching in Production",
        sub_hook="Preventing Cross-Tenant Leaks and High-Recall Invalidation Failures",
        q1_title="What is the 500ms Invalidation Trap in LLM Semantic Caching?",
        q1_body="When source documents update, vector databases take 500ms–5s to re-index.\nIn-flight queries during that window match stale embeddings, serving cached hallucinations.\n\nFurthermore, flat cosine similarity thresholds (0.88) allow semantically close\nqueries from Tenant B to retrieve proprietary pricing cached by Tenant A.",
        q2_title="What is the production architecture for safe semantic caching?",
        q2_body="1. Partitioned Compound Cache Keys:\n   Key = SHA256(tenant_id + user_role + doc_epoch) + query_embedding\n2. Dynamic Similarity Thresholds: 0.96+ for numerical/regulatory data; 0.88 for chat.\n3. Event-Driven CDC Invalidation: Debezium captures database updates and pushes\n   atomic epoch bumps via Kafka in <50ms, instantly fencing stale cache lines.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: ISOLATE BEFORE YOU EMBED",
        rule_body="Never compute semantic similarity across tenant boundaries. Vector distance\nmust only be evaluated within pre-filtered, tenant-isolated logical partitions."
    ))

    # Page 5: Zero-Downtime DB
    pages.append(render_content_page(
        page_num=5, total_pages=11,
        chapter_title="04: Zero-Downtime Database Architecture",
        sub_hook="Safe Schema Evolution on 80M+ Row Tables via Expand/Contract",
        q1_title="Why does running ALTER TABLE cause production outages?",
        q1_body="Running ALTER TABLE on tables with 80M+ rows requests an exclusive metadata lock.\nWhile waiting for in-flight transactions to finish, all subsequent read/write\nqueries queue up behind it. Connection pools exhaust in seconds. Upstream gateways\nthrow 504 Timeouts and the platform suffers a complete cascading collapse.",
        q2_title="What are the 3 phases of the Expand/Contract Pattern?",
        q2_body="• PHASE 1 (Expand): Add new nullable column/table. Deploy code that dual-writes\n  to both old and new columns, reading from the old.\n• PHASE 2 (Backfill): Run throttled, idempotent background workers with zero WAL\n  replica lag (<10ms). Then flip feature flag to read from new column.\n• PHASE 3 (Contract): Remove old column writing code. Drop legacy column safely.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: NEVER MUTATE IN-PLACE",
        rule_body="Database evolution is a multi-step distributed state transition. A migration that\nrequires scheduled downtime is architectural technical debt masquerading as maintenance."
    ))

    # Page 6: AEM Dispatcher Invalidation
    pages.append(render_content_page(
        page_num=6, total_pages=11,
        chapter_title="05: AEM Dispatcher Cache Invalidation",
        sub_hook="Protecting Publisher JVMs from Thundering Herds & /statfileslevel Disasters",
        q1_title="Why is /statfileslevel 0 the most dangerous setting in enterprise AEM?",
        q1_body="When /statfileslevel is set to 0, publishing a 1-character typo on /content/us/en\ntouches the root .stat file. The Dispatcher treats every cached HTML file across all\n14 language sites as invalidated. 45,000 live requests bypass Apache and flood the 4\npublisher JVMs simultaneously. CPU hits 98% and the cluster chokes.",
        q2_title="How do you architect resilient multi-tenant Dispatcher farms?",
        q2_body="1. Match /statfileslevel to Tenant Depth: E.g., /content/brand/country/lang -> level 3.\n   Publishing /us/en only flushes the /us branch; EMEA and APAC stay warm.\n2. Enforce /gracePeriod 2: Allows Dispatcher to continue serving stale cache for 2 seconds\n   while the publisher renders the new HTML, eliminating the thundering herd.\n3. AST Verification: Scan farm files in pre-commit hooks to block statfileslevel 0.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: ORIGIN SHIELDING",
        rule_body="Treat origin publish tiers as fragile databases. The Dispatcher exists to protect\nthe JVM from the internet. Every cache miss is an architectural vulnerability."
    ))

    # Page 7: AEM Edge Delivery Services (EDS)
    pages.append(render_content_page(
        page_num=7, total_pages=11,
        chapter_title="06: High-Performance Vanilla Block Architecture",
        sub_hook="The Death of Monolithic Clientlibs & Sub-50ms LCP on Edge CDNs",
        q1_title="Why are monolithic clientlibs obsolete on modern web platforms?",
        q1_body="Bundling 40 CSS and 80 JS files into a single 1.8MB clientlib forces mobile browsers\nto parse hundreds of kilobytes of code before rendering the hero section. 78% of the\ncode belongs to components not even present on the page. Core Web Vitals plummet.",
        q2_title="How does Decentralized Vanilla Block architecture achieve 99+ CWV?",
        q2_body="1. Semantic HTML First: Edge CDNs serve raw HTML in <50ms without server rendering.\n2. Viewport-Based Lazy Hydration: Blocks load their isolated 2KB script ONLY when\n   entering the viewport via IntersectionObserver.\n3. Zero Heavy Framework Overhead: Pure vanilla JavaScript eliminates React/jQuery\n   re-hydration blocking time, driving Total Blocking Time (TBT) to <15ms.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: NO PAYLOAD MONOPOLIES",
        rule_body="A 1-character change in a component footer should never invalidate the CDN cache\nof your entire global web platform. Decentralize bundles down to the block level."
    ))

    # Page 8: eBPF JVM Observability
    pages.append(render_content_page(
        page_num=8, total_pages=11,
        chapter_title="07: Zero-Overhead JVM Observability via eBPF",
        sub_hook="Tracing Safepoint Latency & Socket Contention at the Linux Kernel Boundary",
        q1_title="Why do Java thread dumps (jstack) make production incidents worse?",
        q1_body="Triggering jstack forces the JVM into a global safepoint. If one thread is locked\nin uninterruptible kernel I/O, every request thread freezes waiting for the safepoint.\nAPM bytecode instrumentation disrupts JIT compiler inlining and adds up to 12% CPU tax.",
        q2_title="How does eBPF kernel tracing solve the Observer Effect?",
        q2_body="eBPF probes run directly inside the Linux kernel sandbox with <1% overhead:\n• Off-CPU Analysis: Traces exact nanoseconds threads spend waiting on epoll queues.\n• True Time-to-Safepoint (TTSP): Measures exact latency without JVM freeze.\n• Zero Application Modifications: Attaches to tracepoints without restarting the JVM.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: TRACE AT THE BOUNDARY",
        rule_body="When diagnosing high-throughput production incidents, userspace profilers perturb\nthe system they observe. Observe from the Linux kernel boundary."
    ))

    # Page 9: Multi-Region CRDTs
    pages.append(render_content_page(
        page_num=9, total_pages=11,
        chapter_title="08: Multi-Region Active-Active Topologies",
        sub_hook="Eliminating Cross-Continent Latency & Split-Brain Disasters via CRDTs",
        q1_title="What is the speed-of-light problem in multi-region cloud databases?",
        q1_body="Speed-of-light propagation through fiber optics across the Atlantic takes ~70ms roundtrip.\nIf transactions require synchronous multi-region Raft/Paxos consensus, writes take\n150ms+. During network partitions, naive failover causes catastrophic split-brain states.",
        q2_title="What are the 3 tiers of global active-active replication?",
        q2_body="• Tier 1 (Read Replicas): Sub-10ms local reads; all writes route back to US Master.\n• Tier 2 (Partitioned by Tenant): 100% local reads/writes; zero cross-region contention.\n• Tier 3 (Multi-Master CRDTs): Concurrent writes in both regions; conflicts resolved\n  mathematically using State-Based or Operation-Based Conflict-Free Replicated Data Types.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: BOUND YOUR CONSENSUS",
        rule_body="You cannot defeat the laws of physics. Either partition your data to keep consensus\nlocal, or embrace mathematically provable eventual consistency using CRDTs."
    ))

    # Page 10: Staff+ Governance
    pages.append(render_content_page(
        page_num=10, total_pages=11,
        chapter_title="09: Architecture Review Board (ARB) Anti-Patterns",
        sub_hook="Replacing 80-Page Slide Committees with Automated CI/CD Code Contracts",
        q1_title="Why do traditional Architecture Review Boards fail to prevent tech debt?",
        q1_body="Gatekeeping committees review pristine 80-page slide decks instead of executable code.\nApprovals take 3 months, but the moment code lands in staging, teams still commit\nblocking database migrations, memory leaks, and unvetted dependencies.",
        q2_title="How do Staff+ architects automate technical governance?",
        q2_body="1. Git-Backed Architecture Decision Records (ADRs): Version-controlled RFCs.\n2. Executable Fitness Functions: Architectural rules enforced directly in GitHub Actions:\n   - AST scanners checking component proxy hygiene.\n   - Linter rules checking maximum dependency payload sizes.\n   - Database migration locks verified before PR merge.",
        rule_title="💡 SENIOR ARCHITECT INVARIANT: ARCHITECTURE AS CODE",
        rule_body="If an architectural standard cannot be expressed as an automated test in CI/CD,\nit is merely an opinion that will be discarded under the pressure of a deadline."
    ))

    # Page 11: Summary Checklist
    pages.append(render_content_page(
        page_num=11, total_pages=11,
        chapter_title="10: The Senior Systems Architect Final Checklist",
        sub_hook="10 Production Invariants for High-Scale Enterprise Platforms",
        q1_title="The Core Production SRE Invariants:",
        q1_body="[✓] Tools Sandboxed: All agent tool executions run in isolated out-of-process containers.\n[✓] Finite State Machines: All autonomous workflows have hard token & hop ceilings.\n[✓] Monotonic Epochs: Semantic caches verify doc epoch before serving hits.\n[✓] Expand/Contract: Zero table-lock ALTER TABLE operations on live datastores.\n[✓] Origin Shielding: /statfileslevel matches tenant hierarchy with /gracePeriod 2.",
        q2_title="The Operational & Career Invariants:",
        q2_body="[✓] Sub-50ms LCP: Ingest modules via IntersectionObserver upon viewport intersection.\n[✓] eBPF Observability: Profile safepoints and socket queues at kernel boundary.\n[✓] CRDT Consensus: Bounded consistency domains across active-active cloud regions.\n[✓] Automated Governance: Architectural fitness functions enforced in CI/CD pipelines.\n[✓] Negative ADRs: Documenting explicitly what we chose NOT to build.",
        rule_title="💡 SAVE THIS FIELD MANUAL FOR YOUR ARCHITECTURE REVIEWS",
        rule_body="Bookmark this post to reference during system design reviews, tech lead interviews,\nand enterprise cloud migration planning."
    ))

    # Save all pages as PNG images and as a single consolidated PDF
    pdf_path = os.path.join(ASSETS_DIR, "The_Pragmatic_Architect_Handwritten_Handbook.pdf")
    pages[0].save(pdf_path, save_all=True, append_images=pages[1:], resolution=150.0)
    print(f"[+] Successfully compiled 11-page PDF: {pdf_path}")

    for idx, p in enumerate(pages, 1):
        p_path = os.path.join(ASSETS_DIR, f"handbook_page_{idx:02d}.png")
        p.save(p_path)

    print(f"[+] Successfully saved {len(pages)} high-resolution slide PNGs into {ASSETS_DIR}")
    return pdf_path

if __name__ == "__main__":
    build_full_handbook()
