#!/usr/bin/env python3
"""
generate_tailored_handbooks.py - Compiles dedicated, multi-page, descriptive
handwritten handbooks for specific LinkedIn posts using the safe layout engine.
Guarantees 100% boundary safety with zero text clipping.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")

sys.path.insert(0, HERE)
from pdf_architect_engine import HandwrittenHandbookBuilder

def build_database_handbook():
    print("[*] Generating Zero-Downtime Database Architecture Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="DATABASE SYSTEMS SRE",
        handbook_name="Zero_Downtime_Database_Architecture_Handbook",
        accent_color=(5, 150, 105), # Emerald Green
        theme_badge="HIGH-THROUGHPUT DATASTORE MANUAL"
    )

    # 1. Cover
    b.add_cover(
        title="ZERO-DOWNTIME\nDATABASE EVOLUTION\nFIELD MANUAL",
        subtitle="The 3-Phase Expand/Contract Pattern on 80M+ Row Tables\nWithout Table Locks, Replication Lag, or Outages",
        curriculum=[
            "Why ALTER TABLE Causes Cascading 504 Gateway Outages",
            "Phase 1 (Expand): Dual-Writing with Feature Flags & Shadow Columns",
            "Phase 2 (Backfill): Throttled Idempotent Workers & Zero WAL Lag",
            "Phase 3 (Contract): Complete Lock-Free Cutover & Column Deprecation",
            "Zero-Downtime Indexing via CREATE INDEX CONCURRENTLY & Lock Timeouts",
            "Senior Systems Architect 8-Point Production Migration Checklist"
        ]
    )

    # 2. Page 2: Failure Mode
    b._start_new_page("Chapter 1: The Anatomy of Table Lock Starvation")
    b.add_card(
        tag="SRE ROOT-CAUSE ANALYSIS",
        title="Why does running ALTER TABLE cause cascading 504 gateway failures?",
        body_paragraphs=[
            "ROOT CAUSE: The Exclusive Metadata Lock Queue.",
            "Running ALTER TABLE on PostgreSQL or MySQL requires an ACCESS EXCLUSIVE lock. Even though adding a nullable column is metadata-only in modern versions, the command cannot acquire the lock until every prior in-flight SELECT, INSERT, or UPDATE transaction finishes.",
            "FAILURE: The Cascading Starvation Wave.",
            "• While ALTER TABLE waits in the queue, it blocks all subsequent read/write requests from acquiring locks.",
            "• Database connection pools (HikariCP, PgBouncer) saturate to 100% in under 30 seconds.",
            "• Upstream API gateways run out of available threads and throw 504 Gateway Timeouts to live customers.",
            "• Within 2 minutes, checkout and authentication are completely down."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="💡 PRODUCTION INVARIANT: STATEMENT & LOCK TIMEOUTS",
        rule_body="Never execute a DDL command without setting an explicit lock_timeout (e.g. 2000ms) and statement_timeout. If the lock cannot be acquired within 2 seconds, fail immediately rather than holding the entire connection pool hostage."
    )

    # 3. Page 3: Expand Phase
    b._start_new_page("Chapter 2: Phase 1 — The Expand Architecture")
    b.add_card(
        tag="MIGRATION BLUEPRINT: EXPAND",
        title="How to evolve high-throughput schemas safely without table locks:",
        body_paragraphs=[
            "STEP 1: Add New Nullable Column with Zero Default Constraint.",
            "In Postgres: ALTER TABLE payments ADD COLUMN amount_cents_v2 bigint;",
            "Never specify a non-null constraint or complex default value during column creation, as writing defaults across 80M rows triggers hours of table rewriting.",
            "STEP 2: Deploy Dual-Writing Application Logic.",
            "• Application write operations write to BOTH legacy 'amount' and new 'amount_cents_v2' columns inside a single database transaction.",
            "• Application reads continue reading exclusively from the old column.",
            "• Dual-writing guarantees that all new incoming transactions are automatically consistent in the new format from millisecond zero."
        ]
    )
    b.add_card(
        tag="CODE CONTRACT",
        title="Application Dual-Write Pattern in Code:",
        body_paragraphs=[
            "paymentRecord.setAmount(cents / 100.0); // Legacy column",
            "paymentRecord.setAmountCentsV2(cents); // New optimized column",
            "paymentRepository.save(paymentRecord);",
            "• The application never assumes backfill is finished during Phase 1.",
            "• Feature flags control rollout percentages with instant rollback safety."
        ]
    )

    # 4. Page 4: Backfill Phase
    b._start_new_page("Chapter 3: Phase 2 — Throttled Backfilling")
    b.add_card(
        tag="DATA ENGINE BLUEPRINT",
        title="How to backfill 80 million historical rows with sub-10ms replica lag:",
        body_paragraphs=[
            "THE PERIL: Unconstrained Bulk UPDATEs Destroy Replicas.",
            "Running 'UPDATE payments SET amount_cents_v2 = amount * 100;' generates millions of Write-Ahead Log (WAL) bytes, overwhelming replication pipelines and crashing read-replicas.",
            "THE SRE FIX: Chunked Idempotent Keyspace Traversal.",
            "1. Iterate by primary key in fixed micro-batches: WHERE id BETWEEN ? AND ? ORDER BY id LIMIT 2000;",
            "2. Throttled Sleep: Inject a 50ms pause between micro-batches to allow disk I/O and replication threads to flush.",
            "3. WAL Lag Monitor: If streaming replication lag exceeds 50ms on any read-replica, pause the worker until lag returns to <10ms.",
            "4. Idempotency Invariant: 'WHERE amount_cents_v2 IS NULL' prevents re-processing rows and allows resuming on worker crash."
        ]
    )
    b.add_invariant(
        title="💡 ARCHITECT INVARIANT: READ-REPLICA HEALTH OVER SPEED",
        rule_body="Backfill velocity is disposable; replica freshness is non-negotiable. It is always better for a migration backfill to take 8 hours at 0% customer impact than 8 minutes with 200ms of lag on production read pools."
    )

    # 5. Page 5: Contract Phase & Indexing
    b._start_new_page("Chapter 4: Phase 3 — The Contract Phase")
    b.add_card(
        tag="FINAL CUTOVER BLUEPRINT",
        title="Zero-downtime read cutover and cleanup contracts:",
        body_paragraphs=[
            "STEP 3: Switch Reads to New Column via Gradual Canary Rollout.",
            "Flip the feature flag: 5% -> 25% -> 100% of read traffic reads from 'amount_cents_v2'. Because dual-writing is active and backfill is 100% complete, reads see identical data.",
            "STEP 4: Remove Legacy Writing Logic.",
            "Deploy code release where dual-write is removed. Writes now target ONLY 'amount_cents_v2'.",
            "STEP 5: Drop Legacy Column Safely.",
            "ALTER TABLE payments DROP COLUMN amount; (Executed during low-traffic window with lock_timeout set to 2s)."
        ]
    )
    b.add_card(
        tag="INDEXING HYGIENE",
        title="How to index high-cardinality foreign keys with zero table locks:",
        body_paragraphs=[
            "• Always use CREATE INDEX CONCURRENTLY on PostgreSQL.",
            "• Concurrent indexing takes share locks, allowing continuous live SELECT, INSERT, and UPDATE queries while the b-tree builds.",
            "• If concurrent build fails due to transient deadlock: inspect 'pg_class' for invalid indexes and run DROP INDEX CONCURRENTLY before retrying."
        ]
    )

    # 6. Page 6: Checklist
    b._start_new_page("Chapter 5: The Database SRE 8-Point Checklist")
    b.add_card(
        tag="PRODUCTION READINESS CONTRACT",
        title="The Senior Systems Architect Pre-Migration Verification Gate:",
        body_paragraphs=[
            "[✓] Lock Timeout Configured: All migration DDL runs with 'SET lock_timeout = 2000ms;'.",
            "[✓] Dual-Writing Verified: New records write to both columns in staging before backfill.",
            "[✓] Micro-Batch Throttling: Backfill iterates by ID in 2,000-row chunks with sleep intervals.",
            "[✓] WAL Replica Lag Monitored: Workers pause if replica lag exceeds 50ms.",
            "[✓] Concurrent Indexing: All secondary indexes built with CONCURRENTLY.",
            "[✓] Backward Compatibility: Previous code release can run against new schema without crashing.",
            "[✓] Rollback Strategy Verified: Feature flags allow 1-click fallback to old column.",
            "[✓] Negative ADR Documented: Explicit record of why in-place ALTER was rejected."
        ]
    )
    b.add_invariant(
        title="💡 THE CORE DOCTRINE: MIGRATION IS DISTRIBUTED STATE",
        rule_body="Treat database changes as distributed state machines. If a migration requires engineering scheduled downtime, the architecture has failed."
    )

    out_file = os.path.join(ASSETS_DIR, "Zero_Downtime_Database_Architecture_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

def build_semantic_caching_handbook():
    print("[*] Generating Safe Semantic Caching in Production Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="ENTERPRISE AI ARCHITECTURE",
        handbook_name="Safe_Semantic_Caching_Production_Handbook",
        accent_color=(37, 99, 235), # Deep Blue
        theme_badge="AI SRE FIELD MANUAL"
    )

    # 1. Cover
    b.add_cover(
        title="SAFE SEMANTIC CACHING\nIN PRODUCTION SYSTEMS",
        subtitle="Preventing Cross-Tenant Leaks, The 500ms Invalidation Trap,\nand High-Recall Hallucinations in LLM Inference Gateways",
        curriculum=[
            "Why Cosine Similarity (0.88) Breaks Down in Multi-Tenant Production",
            "The 500ms Stale Invalidation Race Condition & In-Flight Query Drift",
            "The Partitioned Compound Key Blueprint: SHA256(Tenant + Role + Epoch)",
            "Event-Driven Invalidation: Sub-50ms Cache Eviction via Debezium CDC",
            "Dynamic Similarity Thresholds: 0.96+ for Factual vs 0.86 for Chat",
            "Senior Systems Architect Pre-Production AI Gateway Verification Checklist"
        ]
    )

    # 2. Page 2: Cosine Collapse
    b._start_new_page("Chapter 1: The Failure Modes of Flat Vector Caching")
    b.add_card(
        tag="SECURITY & ACCURACY AUDIT",
        title="Why does naive semantic caching fail under enterprise load?",
        body_paragraphs=[
            "FAILURE 1: Cross-Tenant Context Contamination.",
            "Teams deploy an open-source vector database (Redis Vector, Qdrant, Pinecone) in front of OpenAI or Claude. They compute embeddings on incoming user prompts and cache the LLM response.",
            "If Tenant B asks: 'What is our corporate refund threshold?', the vector similarity score matches Tenant A's previous prompt with 0.89 cosine distance.",
            "Tenant B receives Tenant A's private, confidential refund policies. In a SOC2/HIPAA environment, this is a catastrophic data breach.",
            "FAILURE 2: The Numerical Blind Spot of Vector Distance.",
            "Vector embeddings excel at semantic topic matching, but fail on exact numerical variations. 'Transfer $50,000 to Account X' and 'Transfer $50 to Account X' have a 0.97 cosine similarity. Serving a cached response causes financial corruption."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="💡 PRODUCTION INVARIANT: ISOLATE BEFORE YOU EMBED",
        rule_body="Never evaluate vector distances across tenant or security boundaries. Vector similarity must ONLY operate within strictly pre-filtered, tenant-isolated logical partitions."
    )

    # 3. Page 3: 500ms Trap
    b._start_new_page("Chapter 2: The 500ms Invalidation Race")
    b.add_card(
        tag="DISTRIBUTED SYSTEMS INCIDENT",
        title="The Stale Invalidation Window in High-Concurrency Gateways:",
        body_paragraphs=[
            "THE INCIDENT SCENARIO:",
            "1. At 14:00:00.000, an admin updates pricing policy in the primary database.",
            "2. Vector re-indexing pipelines (embeddings generation, vector chunk upsert) take between 500ms and 5,000ms to complete.",
            "3. During this 500ms window, 200 concurrent user requests hit the inference gateway.",
            "4. The gateway evaluates incoming queries against the un-updated vector cache and returns stale, hallucinated pricing.",
            "THE SRE MITIGATION: Monotonic Document Epoch Tagging.",
            "• Every document version maintains an atomic, monotonic epoch counter in Redis.",
            "• The inference gateway verifies that the cached vector embedding's epoch matches the current document epoch in under 1ms.",
            "• In-flight queries assessing against older epochs get fenced off immediately and fail-open to fresh retrieval."
        ]
    )

    # 4. Page 4: Compound Keys & Dynamic Gates
    b._start_new_page("Chapter 3: The Compound Partition Key Architecture")
    b.add_card(
        tag="GATEWAY BLUEPRINT",
        title="How to architect zero-leak multi-tenant semantic caching:",
        body_paragraphs=[
            "1. Partitioned Compound Cache Keys:",
            "Key = SHA256(tenant_id + user_role_hierarchy + doc_epoch) + query_vector",
            "This mathematically guarantees that queries from Tenant B can NEVER match cache entries created by Tenant A, regardless of prompt phrasing.",
            "2. Tiered Dynamic Similarity Gates:",
            "• Tier 1 (Numerical, Pricing, Legal): Cosine Threshold >= 0.97 (Near exact).",
            "• Tier 2 (Product Features, FAQ Retrieval): Cosine Threshold >= 0.93.",
            "• Tier 3 (Conversational Dialogue, Chit-Chat): Cosine Threshold >= 0.86.",
            "3. Hard Token Budget Failsafe: Cache misses route to small language models (8B SLMs) first before escalating to 400B models."
        ]
    )
    b.add_invariant(
        title="💡 ARCHITECT INVARIANT: TIERED THRESHOLDS",
        rule_body="Flat 0.88 cosine similarity thresholds are indefensible in mission-critical software. Always tie your semantic distance threshold to the domain criticality of the query."
    )

    # 5. Page 5: Event-Driven CDC
    b._start_new_page("Chapter 4: Event-Driven CDC Invalidation")
    b.add_card(
        tag="DATA PIPELINE ARCHITECTURE",
        title="Sub-50ms cache invalidation via Debezium and Kafka:",
        body_paragraphs=[
            "1. Change Data Capture (CDC): Debezium monitors PostgreSQL transaction logs (WAL).",
            "2. Atomic Change Event: When a document or policy table commits an UPDATE, Debezium emits an immutable CDC event to Kafka in <15ms.",
            "3. Gateway Consumer: The API gateway cache worker consumes the event and increments the document epoch in Redis via atomic EVAL script in <5ms.",
            "4. Immediate Invalidation: Next incoming query evaluates against the new epoch; stale vector cache hits are invalidated instantly without waiting for vector embeddings to finish re-indexing."
        ]
    )
    b.add_card(
        tag="LATENCY PROFILE",
        title="End-to-End Invalidation Latency Comparison:",
        body_paragraphs=[
            "• Naive Periodic Polling: 30,000ms – 60,000ms (High stale hallucination risk).",
            "• Batch Vector Upsert: 5,000ms – 10,000ms (Dangerous in-flight window).",
            "• Event-Driven CDC Epoch Invalidation: 22ms p99 (Zero stale cache hits)."
        ]
    )

    # 6. Page 6: Checklist
    b._start_new_page("Chapter 5: Production AI Gateway Verification Checklist")
    b.add_card(
        tag="SRE LAUNCH GATE",
        title="The Senior Systems Architect Semantic Caching Production Checklist:",
        body_paragraphs=[
            "[✓] Multi-Tenant Key Salting: All vector queries hashed with tenant ID & role scope.",
            "[✓] Monotonic Epoch Fencing: Document updates increment Redis epoch in <50ms.",
            "[✓] Tiered Similarity Gates: Factual endpoints configured with >= 0.96 threshold.",
            "[✓] Exact String Fast-Path: SHA256 exact match checked in Redis before vector embedding.",
            "[✓] Fail-Open Design: Vector store downtime routes directly to primary inference.",
            "[✓] Zero Cross-Tenant Leak Audits: Automated red-team penetration tests passing in CI.",
            "[✓] Token FinOps Metrics: Cache hit rate, p95 gateway latency, and saved tokens exported to Grafana."
        ]
    )
    b.add_invariant(
        title="💡 THE CORE DOCTRINE: CACHE SPEED MUST NOT COMPROMISE TRUTH",
        rule_body="Saving $0.02 in LLM token inference is worthless if you serve an unvetted cached hallucination to a customer. Correctness precedes latency optimization."
    )

    out_file = os.path.join(ASSETS_DIR, "Safe_Semantic_Caching_Production_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

def build_mcp_handbook():
    print("[*] Generating Model Context Protocol (MCP) in Production Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="PRODUCTION AI HARNESS SRE",
        handbook_name="Model_Context_Protocol_Production_Handbook",
        accent_color=(124, 58, 237), # Royal Violet / Indigo
        theme_badge="ENTERPRISE MCP FIELD MANUAL"
    )

    # 1. Cover
    b.add_cover(
        title="MODEL CONTEXT PROTOCOL (MCP)\nENTERPRISE PRODUCTION MANUAL",
        subtitle="Out-of-Process Sandboxing, stdio vs SSE Topologies,\nAsync Circuit Breakers, and Least-Privilege Tool Execution",
        curriculum=[
            "Why In-Process LLM Tool Execution Causes Memory Bleeds & Process Crashes",
            "Protocol Topologies: stdio Local Pipes vs SSE Remote Microservices",
            "Out-of-Process Isolation: gVisor / Docker Sandboxes & Memory Bounds",
            "Preventing Cascading Deadlocks: Async Circuit Breakers & Timeout Ladders",
            "Tool Schema Contracts: Strict JSON Schema Validation & Input Sanitization",
            "Senior Systems Architect Pre-Production MCP Verification Checklist"
        ]
    )

    # 2. Page 2: In-Process Peril
    b._start_new_page("Chapter 1: The Peril of In-Process Tool Calling")
    b.add_card(
        tag="SECURITY & STABILITY ROOT CAUSE",
        title="Why does running LLM tools in the main process crash enterprise platforms?",
        body_paragraphs=[
            "THE SYSTEM FAILURE: Shared Memory Corruption & Process Lock.",
            "When engineers bind tools directly into the application process (e.g. running LangChain or LlamaIndex tool functions inside the web server), un-sandboxed tools inherit full OS process privileges.",
            "A single hanging SQL query, memory-leaking PDF parser, or unhandled C-extension segfault takes down the entire parent application worker.",
            "THE SECURITY BREACH: Indirect Prompt Injection to Shell Execution.",
            "If an LLM hallucinates shell command arguments or ingests a malicious web document containing jailbreak injection, an in-process tool runner executes malicious shellcode with the web server's full IAM service account privileges.",
            "THE ARCHITECTURAL FIX: Model Context Protocol (MCP).",
            "MCP enforces strict separation of concerns: the model context client communicates with tool servers exclusively via structured JSON-RPC over isolated stdio pipes or network SSE."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="💡 PRODUCTION INVARIANT: ZERO IN-PROCESS CODE EXECUTION",
        rule_body="Never execute tool implementations inside the primary LLM inference host. Every external tool must run in an isolated, sandboxed subprocess with bounded memory and read-only root filesystems."
    )

    # 3. Page 3: stdio vs SSE
    b._start_new_page("Chapter 2: Protocol Architecture — stdio vs SSE")
    b.add_card(
        tag="TOPOLOGY COMPARISON",
        title="Architectural Trade-Offs: Local stdio vs Distributed SSE:",
        body_paragraphs=[
            "TOPOLOGY A: stdio (Standard Input / Output Pipes).",
            "• Use Case: Local agent execution, developer desktop IDEs, single-host container pods.",
            "• Communication: Raw stdin/stdout JSON-RPC streams. Zero network overhead, sub-millisecond invocation latency.",
            "• Security: Sandboxed via Linux namespace, cgroups (CPU/RAM caps), and read-only host mounts.",
            "TOPOLOGY B: SSE (Server-Sent Events over HTTP/2).",
            "• Use Case: Enterprise multi-agent fleets, shared centralized database tools, microservices.",
            "• Communication: HTTP POST for client requests, HTTP streaming (SSE) for server events.",
            "• Architecture: Allows independent horizontal auto-scaling of tool clusters behind load balancers with mTLS authentication."
        ]
    )
    b.add_card(
        tag="TOPOLOGY SELECTION CONTRACT",
        title="The Architect Rule of Thumb for Protocol Selection:",
        body_paragraphs=[
            "• If the tool requires local host environment access (git, file reads): Use stdio in a locked container.",
            "• If the tool manages shared state (Postgres query runner, Salesforce CRM, Jira API): Use SSE with OAuth2 Bearer token propagation."
        ]
    )

    # 4. Page 4: Circuit Breakers & Timeouts
    b._start_new_page("Chapter 3: Circuit Breakers & Timeout Ladders")
    b.add_card(
        tag="DISTRIBUTED SYSTEMS RESILIENCY",
        title="How to prevent multi-agent deadlocks and runaway token spending:",
        body_paragraphs=[
            "THE HAZARD: The Recursive Tool Retry Black Hole.",
            "When an MCP tool returns an error, LLMs tend to generate identical tool calls repeatedly. In an unconstrained loop, this consumes $500 in API tokens and hangs the user thread indefinitely.",
            "THE SRE MECHANISM: The 3-Tier Timeout & Circuit Breaker Ladder.",
            "1. Tool Execution Timeout: Hard kill at 3,000ms. If an MCP server tool exceeds 3 seconds, SIGKILL the worker process and return an explicit JSON error frame.",
            "2. Circuit Breaker (Hystrix Pattern): If an MCP server fails 3 consecutive invocations, trip the breaker to OPEN state for 30s. Instantly short-circuit subsequent calls with fallback cached results.",
            "3. Max Tool Recursion Cap: Enforce a strict max_tool_iterations = 4. If step count exceeds 4 without final answer, abort with graceful user degradation."
        ]
    )
    b.add_invariant(
        title="💡 ARCHITECT INVARIANT: BOUNDED EXECUTION CONTRACTS",
        rule_body="Every MCP tool call must have a strict wall-clock deadline and a deterministic fallback state. Treat tool servers as untrusted 3rd-party dependencies."
    )

    # 5. Page 5: Schema Validation & Security
    b._start_new_page("Chapter 4: Schema Contracts & Injection Shielding")
    b.add_card(
        tag="SECURITY DEFENSE-IN-DEPTH",
        title="Hardening the MCP Gateway against malicious input payloads:",
        body_paragraphs=[
            "1. Strict JSON Schema Validation at the Harness Boundary:",
            "Never pass raw LLM JSON directly to the underlying tool function. Validate incoming tool arguments against rigid JSON Schema (Draft 7/2020-12) with additionalProperties: false.",
            "2. Shell Argument Sanitization:",
            "Disallow raw bash execution. Use parameterized argv arrays without shell interpolation (execve rather than /bin/sh -c).",
            "3. Output Token Truncation:",
            "If an MCP tool returns a 10MB database dump, feeding it into the LLM context causes massive latency spikes and context overflow. Enforce a 4,000-token output truncation ceiling."
        ]
    )
    b.add_card(
        tag="AUDIT TRAIL CONTRACT",
        title="Immutable Tool Audit Ledger:",
        body_paragraphs=[
            "• Every MCP tool invocation must log: timestamp, caller_agent_id, tool_name, SHA256(input_params), execution_latency_ms, and exit_code.",
            "• Stream tool audit logs directly to SIEM (Splunk, Elastic) for automated compliance monitoring."
        ]
    )

    # 6. Page 6: Checklist
    b._start_new_page("Chapter 5: Enterprise MCP Production Readiness Checklist")
    b.add_card(
        tag="SRE VERIFICATION GATE",
        title="The Senior Systems Architect Pre-Production MCP Verification Gate:",
        body_paragraphs=[
            "[✓] Process Sandboxing: stdio tools run in isolated containers with read-only root filesystems.",
            "[✓] Hard Execution Timeouts: Sub-process SIGKILL configured at 3,000ms threshold.",
            "[✓] Circuit Breaker Active: Tripped after 3 consecutive failures; 30s cool-off window.",
            "[✓] Parameterized Invocation: Zero string interpolation in system shell commands.",
            "[✓] Token Truncation Ceiling: Tool output payloads bounded to max 4KB / 4,000 tokens.",
            "[✓] Least-Privilege IAM: Dedicated read-only service accounts used for datastore tools.",
            "[✓] Healthcheck & Heartbeats: Ping/Pong liveness checks configured on SSE network endpoints.",
            "[✓] Negative ADR Documented: Architectural trade-offs of in-process vs out-of-process logged."
        ]
    )
    b.add_invariant(
        title="💡 THE CORE DOCTRINE: THE HARNESS IS THE FIREWALL",
        rule_body="The model generates intent; the MCP harness enforces physical reality. Never trust generated parameters without programmatic boundary validation."
    )

    out_file = os.path.join(ASSETS_DIR, "Model_Context_Protocol_Production_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

def build_aem_reliability_handbook():
    print("[*] Generating AEM Enterprise Web Reliability Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="EDGE PLATFORMS & CDN SRE",
        handbook_name="AEM_Enterprise_Web_Reliability_Handbook",
        accent_color=(220, 38, 38), # Crimson / Sunset Red
        theme_badge="EDGE CDN & DISPATCHER MANUAL"
    )

    # 1. Cover
    b.add_cover(
        title="AEM EDGE RELIABILITY\n& DISPATCHER CACHING MANUAL",
        subtitle="Sub-100ms LCP, /statfileslevel Invalidation Architecture,\nOrigin Shielding, and High-Performance Vanilla Edge Blocks",
        curriculum=[
            "The /statfileslevel 0 Catastrophe: How 1 Typo Wipes Millions of Cached Assets",
            "The 3-Layer Edge Invalidation Architecture: Level 2+ Tree Scoping",
            "Dispatcher Origin Shielding: /gracePeriod 2 & Thundering Herd Suppression",
            "The Death of Monolithic Clientlibs: High-Performance Vanilla Block Modules",
            "Real User Monitoring (RUM) & Edge Delivery Services (EDS) Optimization",
            "Senior Systems Architect Edge Platform Reliability Checklist"
        ]
    )

    # 2. Page 2: Statfileslevel 0 Disaster
    b._start_new_page("Chapter 1: The Anatomy of Dispatcher Cache Wipeout")
    b.add_card(
        tag="CDN INCIDENT POST-MORTEM",
        title="Why setting /statfileslevel 0 crashes enterprise web platforms:",
        body_paragraphs=[
            "THE CONFIGURATION FLAW: /statfileslevel 0.",
            "In AEM Dispatcher, the .stat file records the timestamp of the most recent content publication. When /statfileslevel is set to 0, there is only ONE single .stat file at the webroot (/content).",
            "THE CATASTROPHE: Global Root Invalidation.",
            "• An author changes one comma in a footer on /content/es/blog/post-1.",
            "• Replication flushes the root .stat file at /content.",
            "• Dispatcher immediately considers ALL 500,000 cached HTML files across English, German, French, and Japanese sites as STALE.",
            "• 15,000 requests/sec bypass the Dispatcher cache and hit backend publish instances simultaneously.",
            "• JVM thread pools saturate in 10 seconds, heap memory spikes to 100%, and authors face total outage."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="💡 PRODUCTION INVARIANT: NEVER USE /statfileslevel < 2",
        rule_body="Always configure /statfileslevel 2 or 3. Never allow global root invalidation. Ensure content tree changes only touch their localized language subtree."
    )

    # 3. Page 3: 3-Layer Invalidation
    b._start_new_page("Chapter 2: The 3-Layer Tree Invalidation Architecture")
    b.add_card(
        tag="EDGE CACHE BLUEPRINT",
        title="How to configure surgical tree-scoped invalidation:",
        body_paragraphs=[
            "1. Tree-Scoped .stat Files (/statfileslevel 3):",
            "Docroot path: /content/corporate/us/en/products/page.html",
            "• Level 0: /content/.stat",
            "• Level 1: /content/corporate/.stat",
            "• Level 2: /content/corporate/us/.stat",
            "• Level 3: /content/corporate/us/en/.stat",
            "Publishing an English product update touches ONLY the /us/en/.stat file. German, French, and Asian docroots remain 100% cached at 99.8% hit ratio.",
            "2. Surgical Flush Agent Headers:",
            "Configure CQ-Action: Activate and CQ-Path: /content/corporate/us/en/products.",
            "Never send wildcard root flushes (*.html)."
        ]
    )
    b.add_card(
        tag="DISPATCHER CONFIG CONTRACT",
        title="Recommended dispatcher.any Caching Invariants:",
        body_paragraphs=[
            "/statfileslevel \"3\"",
            "/allowAuthorized \"0\"",
            "/serveStaleOnError \"1\"",
            "• Prevents unauthenticated cache leaks for protected member portals.",
            "• Enables instant failover to stale cache if backend publish nodes restart."
        ]
    )

    # 4. Page 4: Grace Period & Origin Shielding
    b._start_new_page("Chapter 3: /gracePeriod 2 & Thundering Herd Defense")
    b.add_card(
        tag="ORIGIN SHIELDING ARCHITECTURE",
        title="Eliminating cache stampedes during major marketing campaigns:",
        body_paragraphs=[
            "THE THUNDERING HERD RISK:",
            "When a high-traffic homepage is invalidated during a live campaign, 1,000 concurrent requests arrive in the same 100ms window before the first request finishes rendering on publish.",
            "All 1,000 requests strike the origin simultaneously (Cache Stampede).",
            "THE SRE MECHANISM: /gracePeriod 2.",
            "• /gracePeriod 2 instructs Dispatcher to continue serving the existing cached file for 2 seconds after the .stat file timestamp update.",
            "• The first incoming request triggers a background origin fetch to rebuild cache.",
            "• The other 999 concurrent requests are served immediately from disk in 1.2ms without touching backend JVM threads.",
            "• Result: Zero origin load spikes during continuous content publishing."
        ]
    )
    b.add_invariant(
        title="💡 ARCHITECT INVARIANT: ORIGIN SHIELDING IS MANDATORY",
        rule_body="Deploy a dedicated Origin Shielding CDN layer (Cloudflare / Fastly) in front of Dispatcher. Collapse concurrent cache misses at the edge POP before they cross the WAN boundary."
    )

    # 5. Page 5: Vanilla Blocks vs Clientlibs
    b._start_new_page("Chapter 4: The Death of Monolithic Clientlibs")
    b.add_card(
        tag="MODERN EDGE WEB PLATFORM",
        title="Moving from 1.8MB legacy clientlibs to high-performance vanilla blocks:",
        body_paragraphs=[
            "THE LEGACY TRAP: Monolithic Clientlibs.",
            "Legacy AEM sites bundle 20+ component scripts into a monolithic clientlib.min.js (1.8MB). The browser parses scripts for carousels, forms, and modals before rendering the hero image.",
            "LCP suffers severely (3.8s+ on mobile 4G), destroying Core Web Vitals.",
            "THE EDGE MODERNIZATION: Vanilla Block Architecture (EDS).",
            "1. Zero Render-Blocking JS: Initial HTML contains clean semantic DOM markup directly from markdown / spreadsheet.",
            "2. Dynamic Module Import: JavaScript blocks load only when intersected via IntersectionObserver:",
            "import(`./blocks/${blockName}/${blockName}.js`).then(m => m.default(el));",
            "3. Result: 100% Core Web Vitals score, Sub-100ms LCP, and 0kB unused CSS."
        ]
    )
    b.add_card(
        tag="PERFORMANCE COMPARISON",
        title="Real User Monitoring (RUM) Metrics:",
        body_paragraphs=[
            "• Legacy Clientlib Architecture: LCP = 3.4s | CLS = 0.18 | Lighthouse = 42",
            "• Modern Edge Vanilla Block: LCP = 0.6s | CLS = 0.00 | Lighthouse = 100"
        ]
    )

    # 6. Page 6: Checklist
    b._start_new_page("Chapter 5: Edge Platform Reliability Checklist")
    b.add_card(
        tag="SRE LAUNCH GATE",
        title="The Senior Systems Architect Pre-Launch Edge Checklist:",
        body_paragraphs=[
            "[✓] Statfileslevel Depth: /statfileslevel set to 2 or 3 across all virtual hosts.",
            "[✓] Grace Period Configured: /gracePeriod \"2\" enabled to squash cache stampedes.",
            "[✓] Origin Shielding Active: CDN collapsed forwarding prevents duplicate origin hits.",
            "[✓] ServeStaleOnError Enabled: Fail-safe mode serves cached content if origin 503s.",
            "[✓] Zero Monolithic Clientlibs: Heavy scripts loaded dynamically via IntersectionObserver.",
            "[✓] Cache Hit Ratio Monitored: Alerting configured if edge hit ratio drops below 96%.",
            "[✓] Sub-100ms LCP Verified: Mobile p75 LCP under 1.2s verified via RUM analytics.",
            "[✓] Negative ADR Documented: Rationale for rejecting monolithic clientlibs recorded."
        ]
    )
    b.add_invariant(
        title="💡 THE CORE DOCTRINE: THE EDGE IS THE ONLY APPLICATION",
        rule_body="If an end-user request reaches an origin JVM application server, the caching topology has broken down. Design the edge to absorb 99.5% of all traffic."
    )

    out_file = os.path.join(ASSETS_DIR, "AEM_Enterprise_Web_Reliability_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

if __name__ == "__main__":
    f1 = build_database_handbook()
    f2 = build_semantic_caching_handbook()
    f3 = build_mcp_handbook()
    f4 = build_aem_reliability_handbook()
    print("\n[+] Successfully compiled all 4 custom-themed, descriptive handbooks:")
    print(f"  1. {f1}")
    print(f"  2. {f2}")
    print(f"  3. {f3}")
    print(f"  4. {f4}")
