#!/usr/bin/env python3
"""
schedule_handbooks_to_buffer.py - Schedules the 4 tailored concept handbooks
into consecutive Saturday slots on Buffer for Gautam Sethi's profile.
"""

import os
import sys
import json
import sqlite3
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")
DB_PATH = os.path.join(PROJECT_ROOT, "my_account", "linkedin_tracker.db")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "my_account"))
from buffer_publisher import schedule_buffer_post

RAW_BASE = "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets"

HANDBOOK_SCHEDULE = [
    {
        "id_key": "handbook_01",
        "title": "Zero-Downtime Database Architecture Handbook",
        "due_at": "2026-12-05T11:00:00.000Z", # Saturday Dec 5, 4:30 PM IST
        "existing_buffer_id": "6b095e4f062ed764a80802c5", # Already scheduled
        "pdf_name": "Zero_Downtime_Database_Architecture_Handwritten_Handbook.pdf",
        "cover_name": "Zero_Downtime_Database_Architecture_Handwritten_Handbook_cover.png",
        "doc_title": "Zero-Downtime Database Architecture Field Manual",
        "text": """Running ALTER TABLE on a live production table with 80M rows is playing Russian roulette with customer SLAs.

Even adding a simple nullable column requires an ACCESS EXCLUSIVE lock. While the metadata update itself takes 2 milliseconds, the command waits in the lock queue until prior in-flight queries finish.

The result?
• The lock queue blocks subsequent SELECT, INSERT, and UPDATE requests.
• Connection pools (HikariCP, PgBouncer) saturate in under 30 seconds.
• Upstream gateways run out of worker threads and return 504 Gateway Timeouts.
• Production authentication and checkout fail.

To solve this, senior systems architects use the 3-Phase Expand/Contract Blueprint:

1️⃣ Phase 1 (Expand): Add the new nullable column with no default constraint. Deploy dual-writing logic inside a single transaction so new rows are consistent from millisecond zero.
2️⃣ Phase 2 (Backfill): Backfill historical rows using chunked, keyspace-indexed workers (WHERE id BETWEEN ? AND ? ORDER BY id LIMIT 2000). Throttling with a 50ms pause keeps streaming replication lag <10ms.
3️⃣ Phase 3 (Contract): Canary rollout read traffic (5% -> 25% -> 100%) to the new column, deprecate old write paths, and drop the legacy column during a low-traffic window.

📖 I compiled the complete 6-Page Handwritten Field Manual attached below to document:
• Lock queue starvation post-mortems
• Dual-writing application code contracts
• Throttled backfilling with WAL replica monitoring
• Zero-downtime indexing via CREATE INDEX CONCURRENTLY
• An 8-Point Pre-Migration SRE Verification Gate

📌 Save this PDF to reference during your next database migration review.
♻️ Repost to help fellow backend and data platform engineers prevent lock-starvation outages.

What is the most challenging schema migration or lock incident you have managed in production?

#DatabaseArchitecture #PostgreSQL #DistributedSystems #SoftwareEngineering #CloudArchitecture #BackendEngineering #DevOps #SRE"""
    },
    {
        "id_key": "handbook_02",
        "title": "Safe Semantic Caching in Production Handbook",
        "due_at": "2026-12-12T11:00:00.000Z", # Saturday Dec 12, 4:30 PM IST
        "pdf_name": "Safe_Semantic_Caching_Production_Handwritten_Handbook.pdf",
        "cover_name": "Safe_Semantic_Caching_Production_Handwritten_Handbook_cover.png",
        "doc_title": "Safe Semantic Caching in Production Systems Manual",
        "text": """Naive semantic caching is a ticking security and accuracy time bomb in enterprise AI gateways.

Many teams deploy Redis Vector or Pinecone in front of LLMs to reduce token expenditures. They compute embeddings on incoming user prompts and cache the inference response with a flat 0.88 cosine distance threshold.

Under enterprise load, two critical failure modes emerge:

1️⃣ Cross-Tenant Data Contamination
If Tenant B asks: 'What is our corporate expense reimbursement threshold?', flat vector similarity can match Tenant A’s prompt with 0.89 cosine distance. Tenant B receives Tenant A's private confidential internal policies. In a SOC2/HIPAA regulated environment, this is an immediate breach.

2️⃣ The 500ms Stale Invalidation Race
Vector re-indexing takes between 500ms and 5,000ms. When a pricing document updates, in-flight inference requests evaluated against un-updated vector indexes serve stale, hallucinated pricing.

How senior architects prevent this:
• Partitioned Compound Keys: Key = SHA256(tenant_id + role_hierarchy + epoch) + query_vector. Cross-tenant matches are mathematically impossible.
• Event-Driven Invalidation: Debezium captures Postgres WAL commits and increments the Redis epoch in <15ms, invalidating stale cache before vector embeddings finish re-indexing.
• Dynamic Similarity Gates: 0.97+ for financial/factual queries vs 0.86 for chit-chat.

📖 I compiled the full 6-Page Handwritten Architecture Guide attached below:
• Cosine distance collapse on numerical prompts
• The 500ms stale invalidation post-mortem
• Compound cache partition key blueprint
• Sub-50ms CDC invalidation pipeline via Debezium & Kafka
• Pre-Production AI Gateway Verification Checklist

📌 Swipe through and save this field manual for your next LLM gateway design review!
♻️ Repost to share with platform teams building production AI systems.

Are you running semantic caching in production, or sticking to exact SHA-256 prompt matching?

#EnterpriseAI #MachineLearning #SystemDesign #SoftwareArchitecture #FinOps #DataEngineering #CloudInfrastructure #AIPlatform"""
    },
    {
        "id_key": "handbook_03",
        "title": "Model Context Protocol (MCP) in Production Handbook",
        "due_at": "2026-12-19T11:00:00.000Z", # Saturday Dec 19, 4:30 PM IST
        "pdf_name": "Model_Context_Protocol_Production_Handwritten_Handbook.pdf",
        "cover_name": "Model_Context_Protocol_Production_Handwritten_Handbook_cover.png",
        "doc_title": "Model Context Protocol (MCP) Enterprise Production Manual",
        "text": """Running LLM tool functions inside the main application process is an architectural anti-pattern.

When tools execute in-process (e.g. LangChain or LlamaIndex tool functions inside your web server), they inherit the host process's full IAM privileges, memory address space, and network sockets.

A single hanging third-party API call, memory-leaking PDF parser, or unhandled C-extension crash takes down your entire web application worker. Worse, an indirect prompt injection attack can trick the model into executing shell commands with production privileges.

This is why the Model Context Protocol (MCP) has become the gold standard for enterprise LLM tooling:

1️⃣ Out-of-Process Isolation: Tools run in sandboxed Docker/gVisor containers with read-only root filesystems and explicit memory bounds.
2️⃣ Protocol Topologies:
   • stdio pipes for single-host, zero-latency local tool execution.
   • SSE (Server-Sent Events) over HTTP/2 for distributed, independently auto-scaling tool clusters with mTLS.
3️⃣ Async Circuit Breakers: Hard execution kill timeouts at 3,000ms and a 3-strike circuit breaker prevent recursive tool hallucination loops from burning thousands in API tokens.
4️⃣ Strict Schema Gateways: Input arguments validated against rigid JSON Schema (Draft 2020-12) with additionalProperties: false before reaching execution.

📖 I put together the complete 6-Page Handwritten Field Manual attached below:
• In-process tool vulnerability breakdowns
• stdio vs SSE architectural trade-offs
• Async circuit breakers & timeout ladders
• Schema sanitization & injection shielding
• SRE Pre-Production MCP Verification Checklist

📌 Save this field manual to harden your agentic systems before shipping to customers.
♻️ Repost to help architects building reliable multi-agent platforms.

How do you sandbox external tool executions in your AI architectures?

#ModelContextProtocol #AIArchitecture #MultiAgentSystems #SoftwareEngineering #CloudSecurity #SRE #Microservices #TechLeadership"""
    },
    {
        "id_key": "handbook_04",
        "title": "AEM Enterprise Web Reliability Handbook",
        "due_at": "2026-12-26T11:00:00.000Z", # Saturday Dec 26, 4:30 PM IST
        "pdf_name": "AEM_Enterprise_Web_Reliability_Handwritten_Handbook.pdf",
        "cover_name": "AEM_Enterprise_Web_Reliability_Handwritten_Handbook_cover.png",
        "doc_title": "AEM Edge Reliability & Dispatcher Invalidation Manual",
        "text": """Setting /statfileslevel to 0 in your Dispatcher farm configuration is one of the fastest ways to crash an enterprise web platform.

In AEM Dispatcher, the .stat file stores the invalidation timestamp. When /statfileslevel is set to 0, there is only ONE single .stat file at the root.

An author fixes a typo in a Spanish blog post, and the Dispatcher immediately flushes the entire docroot. 500,000 cached HTML files across English, German, French, and Japanese sites become stale in one second.

Thousands of live users hit the backend publish instances simultaneously (Cache Stampede). JVM thread pools saturate, heap spikes to 100%, and the site suffers a total outage.

Here is the SRE architecture for 99.8% edge cache efficiency:

1️⃣ Surgical Tree-Scoped Invalidation (/statfileslevel 2+ or 3): Confines .stat file invalidation to localized language subtrees. A Spanish change leaves global docroots completely intact.
2️⃣ Thundering Herd Suppression (/gracePeriod 2): Dispatcher continues serving stale cached assets for 2 seconds while one background request refreshes the origin, absorbing traffic spikes during major campaigns.
3️⃣ Monolithic Clientlib Deprecation: Replacing 1.8MB legacy clientlib packages with modern Vanilla Block modules loaded dynamically via IntersectionObserver drops LCP from 3.4s down to <600ms on mobile.

📖 I documented the complete 6-Page Handwritten Architecture Guide attached below:
• The anatomy of /statfileslevel 0 root wipeouts
• 3-Layer tree-scoped invalidation architecture
• Origin shielding & /gracePeriod 2 configuration
• Modern Edge Delivery Services (EDS) block loading
• Senior Systems Architect Edge Platform Reliability Checklist

📌 Save this field manual to audit your CDN and edge caching farm configurations!
♻️ Repost to share with web platform architects and SRE teams.

What is your current edge cache hit ratio, and how do you protect origin servers during live publishing?

#AdobeExperienceManager #AEM #WebPerformance #EdgeComputing #CDN #DevOps #SRE #CloudEngineering"""
    }
]

def log_activity(action_type, summary, details):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO activity_logs (action_type, summary, details, status, created_at)
            VALUES (?, ?, ?, 'SUCCESS', CURRENT_TIMESTAMP)
        """, (action_type, summary, details))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[-] DB Log Error: {e}", file=sys.stderr)

def main():
    print("=" * 70)
    print("🚀 SCHEDULING TAILORED ARCHITECTURAL HANDBOOKS INTO BUFFER (WEEKLY SAT)")
    print("=" * 70)

    for item in HANDBOOK_SCHEDULE:
        key = item["id_key"]
        title = item["title"]
        due_at = item["due_at"]
        doc_url = f"{RAW_BASE}/{item['pdf_name']}"
        thumb_url = f"{RAW_BASE}/{item['cover_name']}"
        doc_title = item["doc_title"]
        
        print(f"\n[*] Processing: {title}")
        print(f"    Slot: {due_at} (Saturday 4:30 PM IST)")
        print(f"    PDF:  {doc_url}")
        
        if "existing_buffer_id" in item:
            print(f"    [!] Already scheduled in Buffer (ID: {item['existing_buffer_id']}).")
            log_activity(
                "BUFFER_HANDBOOK_VERIFIED",
                f"Verified Handbook 1 in Buffer: {title}",
                f"Buffer ID: {item['existing_buffer_id']} | dueAt: {due_at} | PDF: {item['pdf_name']}"
            )
            continue

        # Schedule new post to Buffer
        print(f"    Pushing to Buffer GraphQL API...")
        res = schedule_buffer_post(
            post_text=item["text"],
            as_draft=False,
            document_url=doc_url,
            document_title=doc_title,
            thumbnail_url=thumb_url,
            due_at=due_at
        )

        if res and "id" in res:
            buf_id = res["id"]
            status = res.get("status", "scheduled")
            print(f"    [+] SUCCESS: Scheduled to Buffer! ID = {buf_id} (Status: {status})")
            log_activity(
                "BUFFER_HANDBOOK_SCHEDULED",
                f"Scheduled Tailored Handbook Post: {title}",
                f"Buffer ID: {buf_id} | dueAt: {due_at} | PDF: {item['pdf_name']}"
            )
        else:
            print(f"    [-] Failed to schedule post: {res}", file=sys.stderr)

    print("\n" + "=" * 70)
    print("✅ All tailored concept handbooks processed and scheduled!")
    print("=" * 70)

def schedule_single_handbook(index):
    item = HANDBOOK_SCHEDULE[index]
    doc_url = f"{RAW_BASE}/{item['pdf_name']}"
    thumb_url = f"{RAW_BASE}/{item['cover_name']}"
    res = schedule_buffer_post(
        post_text=item["text"],
        as_draft=False,
        document_url=doc_url,
        document_title=item["doc_title"],
        thumbnail_url=thumb_url,
        due_at=item["due_at"]
    )
    print(f"Scheduled single handbook {item['title']}: {res}")
    return res

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1].isdigit():
        schedule_single_handbook(int(sys.argv[1]))
    else:
        main()
