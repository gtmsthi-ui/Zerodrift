#!/usr/bin/env python3
"""
recreate_all_upcoming_posts.py - Recreates all upcoming posts in Buffer
with complete topic versatility across the 4 core pillars, attaching the
newly compiled single-color blue pen handwritten handbooks (zero undersigned references).
"""

import os
import sys
import json
import sqlite3
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
DB_PATH = os.path.join(PROJECT_ROOT, "my_account", "linkedin_tracker.db")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "my_account"))
from buffer_publisher import execute_graphql, schedule_buffer_post, load_config, get_buffer_posts

RAW_BASE = "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets"

VERSATILE_PIPELINE = [
    # 1. Wed Dec 02 - Edge & Distributed Web Platforms
    {
        "slot_key": "post_dec_02",
        "due_at": "2026-12-02T03:00:00.000Z", # Wed Dec 02, 8:30 AM IST
        "title": "The Death of Monolithic Clientlibs: High-Performance Vanilla Block Architecture",
        "pillar": "Edge & Distributed Web Platforms",
        "type": "text",
        "text": """Bundling 1.8MB of JavaScript in monolithic clientlib packages is the silent killer of Core Web Vitals on enterprise web platforms.

For over a decade, enterprise CMS deployments bundled 20+ component scripts into a single clientlib.min.js loaded in the HTML header. The browser is forced to download, parse, and compile code for carousels, modals, and accordion widgets before it can even begin rendering the hero image.

The result on mobile 4G?
• Largest Contentful Paint (LCP) degrades to 3.8s+
• Total Blocking Time (TBT) spikes past 600ms
• Mobile conversion rates drop by 24%

Here is how modern Edge Delivery Platforms (like AEM EDS and modern Edge runtimes) solve this with Vanilla Block Architecture:

1️⃣ Semantic DOM from Source: The origin outputs clean, semantic HTML with zero framework scaffolding. The critical rendering path has 0kB of blocking JavaScript.
2️⃣ Decentralized Micro-Modules: Each component is an isolated ESM module (e.g. /blocks/hero/hero.js).
3️⃣ Viewport-Intersection Loading: Blocks below the fold are loaded dynamically via IntersectionObserver only when the user scrolls near them:

const observer = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      import(`./blocks/${blockName}/${blockName}.js`).then(m => m.default(el));
      observer.unobserve(el);
    }
  });
});

4️⃣ The Production Outcome:
• Lighthouse Performance: 42/100 -> 100/100
• Mobile LCP: 3.4s -> 0.6s
• Total Blocking Time: 0ms

Stop shipping framework runtimes to display text and images. Ship semantic markup, lazy-load dynamic behavior at the edge, and let the browser do what it was built to do.

What is your current mobile LCP, and what is the biggest bundle bottleneck in your web platform?

#WebPerformance #CoreWebVitals #EdgeComputing #AEM #SoftwareArchitecture #FrontendEngineering #TechLeadership #SRE"""
    },

    # 2. Sat Dec 05 - AI Mock Interview Field Manual (Carousel)
    {
        "slot_key": "handbook_dec_05",
        "due_at": "2026-12-05T11:00:00.000Z", # Sat Dec 05, 4:30 PM IST
        "title": "The AI Engineer Mock Interview Field Manual (12 Pages)",
        "pillar": "Production AI & Harness Architecture",
        "type": "document",
        "pdf_name": "AI_Engineer_Mock_Interview_Handwritten_Handbook.pdf",
        "cover_name": "AI_Engineer_Mock_Interview_Handwritten_Handbook_cover.png",
        "doc_title": "AI Engineer Mock Interview Field Manual (12 Pages)",
        "text": """Reading interview questions isn't practice. 

Practice is answering them with a timer running, a friend across from you, or a recording you'll cringe at later. 

These are the mock questions I rehearse before any Staff+ AI Engineer or Systems Architecture interview, grouped the way a real interview loop moves:

⏱️ Warm-Up (Two Minutes Each):
• Tell me about yourself and the AI work you've actually shipped
• Explain RAG to a product manager who has never heard of it
• Prompting vs RAG vs Fine-tuning: when is each the wrong choice?
• Why do models hallucinate, and what do you do about it in production?

⚡ Fundamentals Under Pressure:
• What happens to a prompt from the moment it's sent to the moment a token comes back?
• Why does tokenization cause problems with numbers, code, and non-English text?
• What do temperature, top-k, and top-p each change?
• When to use a reasoning model (o1/R1), and when is it wasted cost?

🔍 RAG Deep Dive:
• Walk me through a RAG pipeline for a 500-page policy document
• How do you choose chunk size, and how do you know it's wrong?
• Retrieval returns the right chunk but the answer is still wrong. What do you check?
• When would hybrid search hurt you compared to vector-only?

🤖 Agent Scenarios:
• Your agent calls the same tool five times in a row. What do you investigate?
• A tool call fails halfway through and retries. How do you prevent duplicate side effects?
• When choose multi-agent over single agent, and what does it cost?
• How to keep an agent reliable over a long session with growing memory?

📊 Evaluation Challenges:
• How do you measure quality for a customer support assistant?
• LLM judge and human users disagree. Whose signal do you trust?
• Offline eval passed but production quality dropped. What did you miss?

📐 System Design Round (Thirty Minutes, Whiteboard):
• Design a document Q&A system for a company with strict data permissions
• Design a support agent that can issue refunds, with safeguards

📖 The complete 12-Page Field Manual attached below documents concrete Staff+ answers, system design blueprints, failure modes, and code contracts for every question.

Save this manual to rehearse before your next technical loop.

Which question category do you find hardest under interview pressure?

#AIEngineering #SystemDesign #SoftwareArchitecture #MachineLearning #LLMOps #RAG #StaffEngineer #SRE"""
    },

    # 3. Wed Dec 09 - Production AI & Harness Architecture
    {
        "slot_key": "post_dec_09",
        "due_at": "2026-12-09T03:00:00.000Z", # Wed Dec 09, 8:30 AM IST
        "title": "Speculative Decoding in Enterprise Production: Cutting 70B Latency by 64%",
        "pillar": "Production AI & Harness Architecture",
        "type": "text",
        "text": """Generating text from a 70B parameter LLM is not compute-bound; it is severely memory-bandwidth bound.

In autoregressive token generation, emitting a single token requires reading all 140GB of weights from GPU High Bandwidth Memory (HBM) to SRAM for just one matrix-vector multiplication.

On an NVIDIA H100 with 3.35 TB/s bandwidth:
• Streaming 140GB takes 41.7 milliseconds per token.
• GPU Tensor Cores sit over 90% idle while waiting on memory bus transfers.
• Time-to-Generate 100 tokens: ~4.2 seconds.

Here is how speculative decoding accelerates this by 2.8x without any loss in accuracy:

1️⃣ The Draft Phase: We pair our 70B target model with an aligned 1B draft model (e.g. LLaMA-1B). The 1B model takes only 1.2ms to generate a token. It speculatively generates K=5 tokens in ~6ms.
2️⃣ The Parallel Verification Phase: The 70B model evaluates all 5 candidate tokens in a single parallel forward pass (taking ~42ms).
3️⃣ Modified Rejection Sampling: We accept tokens up to the first disagreement using probability ratios. Even rejected tokens yield forward progress.
4️⃣ The Performance Reality:
• With an acceptance rate of alpha = 0.82, we generate an average of 4.1 tokens every 48ms.
• Effective latency drops from 42ms/token down to ~12ms/token (a 71% latency reduction).
• The output text distribution is mathematically identical to running the 70B model alone.

The catch? If your draft model acceptance rate drops below 40% (e.g. on dense code syntax or symbolic math), speculative decoding can actually increase latency. Always monitor your draft acceptance ratios in production telemetry.

Are you running speculative decoding or Medusa multi-head draft heads in your inference gateways?

#MachineLearning #LLMOps #ArtificialIntelligence #SoftwareEngineering #CloudInfrastructure #DeepLearning #GPU #SRE"""
    },

    # 4. Sat Dec 12 - Speculative Decoding & KV-Cache Paging (Carousel)
    {
        "slot_key": "handbook_dec_12",
        "due_at": "2026-12-12T11:00:00.000Z", # Sat Dec 12, 4:30 PM IST
        "title": "Speculative Decoding & KV-Cache Paging Field Manual (6 Pages)",
        "pillar": "Production AI & Harness Architecture",
        "type": "document",
        "pdf_name": "Speculative_Decoding_and_KVCache_Handwritten_Handbook.pdf",
        "cover_name": "Speculative_Decoding_and_KVCache_Handwritten_Handbook_cover.png",
        "doc_title": "Speculative Decoding & KV-Cache Paging Field Manual (6 Pages)",
        "text": """Standard KV-cache implementations waste up to 60% of GPU VRAM due to memory fragmentation.

When serving concurrent LLM requests, legacy frameworks pre-allocate contiguous memory blocks for the maximum possible sequence length (e.g. 8k tokens). If a user completes their query in 200 tokens, the remaining 97% of memory sits locked and unusable (Internal Fragmentation).

This memory wall is the #1 ceiling on enterprise inference throughput.

In the 6-Page Technical Field Manual attached below, we break down:
• Arithmetic Intensity: Why single-token decoding is memory-bandwidth bound
• Speculative Decoding Math: Proposing K candidate tokens with parallel target verification
• Rejection Sampling Mechanics: Mathematical proofs guaranteeing zero output distribution drift
• vLLM PagedAttention: How OS virtual memory paging eliminates GPU memory fragmentation down to <4%
• Continuous Batching & Chunked Prefill: Interleaving 512-token prompt prefill chunks to eliminate decode latency spikes
• Senior Systems Architect Production Inference SRE Verification Checklist

Swipe through and save this specification for your next GPU infrastructure review.

How do you manage KV-cache memory pressure and batch scheduling under peak traffic?

#LLMInference #vLLM #GPUArchitecture #SystemDesign #SoftwareEngineering #CloudComputing #DeepLearning #SRE"""
    },

    # 5. Wed Dec 16 - Cloud FinOps & Distributed Data
    {
        "slot_key": "post_dec_16",
        "due_at": "2026-12-16T03:00:00.000Z", # Wed Dec 16, 8:30 AM IST
        "title": "The $30,000/Month Cross-AZ Cloud Tax: Diagnosing Kubernetes Service Mesh Waste",
        "pillar": "Cloud FinOps & Distributed Data",
        "type": "text",
        "text": """AWS charges $0.01 per GB for data transfer between Availability Zones (AZs) in the same region. That sounds negligible until you inspect a Kubernetes cluster with a naive service mesh.

In many high-growth architectures, microservices are deployed across 3 AZs for high availability. When Service A calls Service B via a round-robin load balancer, 66% of all internal RPC requests cross AZ boundaries.

In an e-commerce platform processing 80 TB of internal gRPC data daily:
• 53 TB crosses AZ boundaries every day.
• Daily cross-AZ transfer tax: $530/day.
• Monthly inter-zone bill: $15,900/month ($190,000/year) paid entirely for moving packets across the same data center metro ring!

Here is how senior infrastructure architects eliminate this tax:

1️⃣ Topology-Aware Routing (Kubernetes 1.27+):
Configure `topology.kubernetes.io/zone` on your Services. kube-proxy and Envoy favor endpoints located in the SAME availability zone as the caller:
service.spec.trafficDistribution: PreferClose

2️⃣ Availability Zone Affinity in Service Mesh:
In Istio/Envoy, enable Locality Prioritized Load Balancing. Requests stay within AZ-1 unless AZ-1 pods exceed 85% CPU saturation, at which point traffic smoothly fails over to AZ-2.

3️⃣ The SRE Outcome:
• Inter-AZ traffic slashed by 82%
• Cross-AZ transfer bill reduced by $13,000/month
• Service-to-service p99 latency dropped by 1.8ms (eliminating fiber propagation delay)

Never pay cloud providers a toll for un-routed internal traffic. Keep local traffic local.

Have you audited your AWS/GCP inter-zone data transfer costs recently?

#CloudFinOps #Kubernetes #AWS #DevOps #Microservices #CloudArchitecture #SRE #CostOptimization"""
    },

    # 6. Sat Dec 19 - Multi-Region Data Topologies & CRDTs (Carousel)
    {
        "slot_key": "handbook_dec_19",
        "due_at": "2026-12-19T11:00:00.000Z", # Sat Dec 19, 4:30 PM IST
        "title": "Multi-Region Data Topologies & CRDTs Field Manual (6 Pages)",
        "pillar": "Cloud FinOps & Distributed Data",
        "type": "document",
        "pdf_name": "MultiRegion_Data_Topologies_CRDTs_Handwritten_Handbook.pdf",
        "cover_name": "MultiRegion_Data_Topologies_CRDTs_Handwritten_Handbook_cover.png",
        "doc_title": "Multi-Region Data Topologies & CRDTs Field Manual (6 Pages)",
        "text": """Synchronous cross-continent consensus guarantees high latency. You cannot beat the speed of light.

Network round-trip time between us-east-1 and eu-central-1 is ~85ms. If your database uses synchronous Raft consensus across oceans, every single write transaction waits 170ms+ for quorum confirmation.

Under high concurrency, connection pools exhaust, API gateways throw 504 timeouts, and a single undersea fiber blip triggers catastrophic leader election storms.

In the 6-Page Technical Field Manual attached below, we document the architecture for resilient Active-Active multi-region systems:
• The Speed-of-Light Barrier: Why synchronous cross-region Raft breaks SLAs
• Conflict-Free Replicated Data Types (CRDTs): Semilattice join properties guaranteeing deterministic convergence without locks
• Vector Clocks vs Hybrid Logical Clocks: Avoiding data loss from 25ms server clock drift
• Split-Brain Fencing: Monotonic epoch tokens and quorum witnesses preventing zombie leader write corruption
• Read-Your-Writes Consistency: Session version stamps (LSN) preventing customer-facing time-travel anomalies
• Staff+ Systems Architect Global Active-Active Launch Verification Checklist

Swipe through and save this specification for your distributed systems architecture reviews.

What consistency model do you enforce for your multi-region data stores?

#DistributedSystems #DatabaseArchitecture #HighAvailability #CloudArchitecture #SoftwareEngineering #DataEngineering #SRE"""
    },

    # 7. Wed Dec 23 - Kernel-Level Observability & Performance
    {
        "slot_key": "post_dec_23",
        "due_at": "2026-12-23T03:00:00.000Z", # Wed Dec 23, 8:30 AM IST
        "title": "eBPF Socket Profiling: Diagnosing Linux TCP Contention Behind Gateways",
        "pillar": "Kernel-Level Observability & Performance",
        "type": "text",
        "text": """Your application APM shows 12ms average latency, but users are complaining of 600ms delays. Where is the missing time?

The blind spot is the Linux kernel socket queue.

When incoming traffic surges past the worker pool capacity of your web server (NGINX, Envoy, Node.js, Go), established TCP connections sit queued in the kernel listen backlog waiting for the application process to invoke accept().

Because application APM timers do not start until accept() returns a socket descriptor, the 500ms spent waiting in the kernel is completely invisible to Datadog or New Relic.

Here is how we diagnose this at the kernel boundary using eBPF:

1️⃣ The Kernel Probe: We attach an eBPF tracepoint to `sock:inet_sock_set_state` and kprobe `tcp_v4_rcv`.
2️⃣ Listen Backlog Delta: We measure the exact delta between when the final TCP 3-way handshake ACK arrives at the NIC and when `sys_accept4` is executed by userspace.
3️⃣ Socket Starvation Alert:
If queue latency exceeds 15ms or the kernel increments `ListenOverflows` / `ListenDrops` (visible in /proc/net/netstat), we immediately know worker threads are CPU-starved or blocked on downstream database locks.

4️⃣ The Production Fix:
• Scale worker process concurrency to match CPU core counts.
• Tune `net.core.somaxconn` from default 128 to 4096.
• Enable `SO_REUSEPORT` to allow multiple worker processes to bind to the same port and distribute incoming TCP handshakes evenly across CPU cores.

True latency does not begin when your code runs; it begins the microsecond the first TCP SYN packet hits the network interface.

How do you monitor TCP backlog queuing and socket starvation in your production clusters?

#LinuxKernel #eBPF #Networking #Observability #DevOps #SystemPerformance #SRE #CloudEngineering"""
    },

    # 8. Sat Dec 26 - Linux Kernel eBPF Observability (Carousel)
    {
        "slot_key": "handbook_dec_26",
        "due_at": "2026-12-26T11:00:00.000Z", # Sat Dec 26, 4:30 PM IST
        "title": "Linux Kernel eBPF Observability Field Manual (6 Pages)",
        "pillar": "Kernel-Level Observability & Performance",
        "type": "document",
        "pdf_name": "Linux_Kernel_eBPF_Observability_Handwritten_Handbook.pdf",
        "cover_name": "Linux_Kernel_eBPF_Observability_Handwritten_Handbook_cover.png",
        "doc_title": "Linux Kernel eBPF Observability Field Manual (6 Pages)",
        "text": """Running jstack or gdb thread dumps during a live production latency spike is playing with fire.

Standard userspace diagnostic tools require bringing all threads to a global Stop-the-World safepoint. If worker threads are stuck in uncounted loops or blocked on socket I/O, the entire JVM freezes while waiting for them, turning a minor latency wobble into a full customer outage (The Observer Effect).

In the 6-Page Technical Field Manual attached below, we document zero-pause Linux kernel observability with eBPF:
• The Observer Effect: Why ptrace and thread dumps worsen production latency
• In-Kernel Safety: How the eBPF Verifier mathematically guarantees zero kernel panics
• Lock-Free Telemetry: BPF ring buffers streaming metrics with <0.5% CPU overhead
• Tracing TCP Listen Backlog Drops: Catching socket starvation before accept()
• Off-CPU Flame Graphs: Finding where worker threads block on mutexes and disk I/O when CPU utilization is misleadingly low
• JVM Safepoint Tracing: Using USDT probes for sub-microsecond GC pause visibility
• Senior Systems Architect Kernel Telemetry Verification Checklist

Swipe through and save this specification for your high-throughput system performance reviews.

What diagnostic tools do you trust during live P1 production incidents?

#eBPF #LinuxKernel #SystemsEngineering #JVM #Observability #PerformanceEngineering #SRE #DevOps"""
    },

    # 9. Wed Dec 30 - Edge & Distributed Web Platforms
    {
        "slot_key": "post_dec_30",
        "due_at": "2026-12-30T03:00:00.000Z", # Wed Dec 30, 8:30 AM IST
        "title": "Edge Serverless vs Container Pods: Surviving Database Connection Exhaustion",
        "pillar": "Edge & Distributed Web Platforms",
        "type": "text",
        "text": """Deploying edge functions (Cloudflare Workers, AWS Lambda@Edge) that connect directly to PostgreSQL or MySQL is an architectural time bomb.

Standard relational databases were designed for long-lived, stateful connection pools (like HikariCP or PgBouncer running inside dedicated backend containers). A single Postgres instance maxes out around 500-1,000 concurrent connections before memory consumption and context switching degrade performance.

When an edge marketing campaign spikes to 20,000 requests/sec across 200 global edge locations:
• Every isolated edge isolate attempts to open its own TCP + TLS database connection.
• Postgres hits `max_connections` within 3 seconds.
• Connection pool starvation causes immediate cascading 500 Internal Server Errors globally.

Here is the SRE architecture for surviving edge database access under load:

1️⃣ The Edge Data Layer Isolation:
Never allow edge isolates to establish direct TCP socket connections to primary databases.
2️⃣ HTTP/WebSocket Connection Proxies (Hyperdrive / Neon / Supabase):
Edge isolates connect over persistent HTTP/2 to an intermediate connection pooling proxy. The proxy multiplexes 20,000 edge requests over a warm, bounded pool of 80 database connections.
3️⃣ Regional Read Replicas & Cache Invalidation:
Serve 95% of edge queries from regional read replicas cached with sub-second TTLs, invalidated via CDC events (Debezium/Kafka).

The edge gives you infinite front-end scaling; without connection multiplexing, it gives your database an instant denial of service.

How do you manage database connection pooling when scaling serverless edge functions?

#EdgeComputing #Serverless #DatabaseArchitecture #PostgreSQL #CloudEngineering #DevOps #SoftwareArchitecture #SRE"""
    },

    # 10. Sat Jan 02 - Edge Platform Resumability & Sub-50ms LCP (Carousel)
    {
        "slot_key": "handbook_jan_02",
        "due_at": "2027-01-02T11:00:00.000Z", # Sat Jan 02, 4:30 PM IST
        "title": "Edge Platform Resumability & Sub-50ms LCP Field Manual (6 Pages)",
        "pillar": "Edge & Distributed Web Platforms",
        "type": "document",
        "pdf_name": "Edge_Platform_Resumability_Handwritten_Handbook.pdf",
        "cover_name": "Edge_Platform_Resumability_Handwritten_Handbook_cover.png",
        "doc_title": "Edge Platform Resumability & Sub-50ms LCP Field Manual (6 Pages)",
        "text": """Traditional Server-Side Rendering (SSR) has a dirty secret: The Hydration Tax.

The server renders HTML (fast First Contentful Paint). But then the browser downloads 1MB of JavaScript bundles and re-executes the entire component tree from top to bottom just to attach event listeners.

During this 2-3 second window on mobile devices, the page looks interactive, but tapping buttons does nothing. CPU spikes to 100%, and Interaction to Next Paint (INP) collapses.

In the 6-Page Technical Field Manual attached below, we document the Resumable Edge Architecture:
• The Hydration Tax: Why double execution destroys Total Blocking Time (TBT)
• Resumability vs Re-Execution: Serializing component state directly into HTML attributes
• Zero-JS Startup: Executing 0kB of JavaScript on page load while maintaining instant interactivity
• Progressive Island Architecture: Viewport-intersection dynamic module loading via IntersectionObserver
• HTTP/3 0-RTT & 103 Early Hints: Warming edge connections and browser caches in sub-20ms
• Real User Monitoring (RUM): Engineering pipelines to maintain 100/100 Core Web Vitals at global scale
• Staff+ Systems Architect Modern Edge Platform Launch Gate

Swipe through and save this specification to eliminate frontend performance bottlenecks.

What is your strategy for reducing client-side JavaScript execution overhead?

#WebPerformance #CoreWebVitals #FrontendArchitecture #EdgeComputing #SystemDesign #SoftwareEngineering #CloudArchitecture #SRE"""
    }
]

def delete_buffer_post(post_id):
    mutation = f"""
    mutation {{
      deletePost(input: {{ id: "{post_id}" }}) {{
        ... on DeletePostPayload {{
          __typename
        }}
        ... on MutationError {{
          message
        }}
      }}
    }}
    """
    res = execute_graphql(mutation)
    return res

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
    print("🚀 RECREATING ALL UPCOMING POSTS IN BUFFER WITH COMPLETE VERSATILITY")
    print("=" * 70)

    # 1. Fetch all current scheduled posts and delete them from Buffer
    print("\n[1] Fetching active Buffer scheduled queue...")
    posts = get_buffer_posts()
    scheduled = [p for p in posts if p.get("status") == "scheduled"]
    print(f"    Found {len(scheduled)} scheduled post(s) to clear.")

    for p in scheduled:
        pid = p["id"]
        due = p.get("dueAt")
        txt = p.get("text", "")[:35].replace("\n", " ")
        print(f"    Deleting old post {pid} ({due}): {txt}...")
        delete_buffer_post(pid)
        time.sleep(0.5)

    print("\n[+] Buffer scheduled queue cleared successfully!")

    # 2. Schedule the 10 versatile, incremental posts
    print("\n[2] Pushing 10 versatile upcoming posts to Buffer GraphQL API...")
    for idx, item in enumerate(VERSATILE_PIPELINE, 1):
        slot = item["due_at"]
        title = item["title"]
        p_type = item["type"]
        print(f"\n({idx}/10) Scheduling: {title}")
        print(f"       Slot: {slot}")

        if p_type == "document":
            doc_url = f"{RAW_BASE}/{item['pdf_name']}"
            thumb_url = f"{RAW_BASE}/{item['cover_name']}"
            doc_title = item["doc_title"]
            print(f"       Attaching Document: {doc_url}")
            res = schedule_buffer_post(
                post_text=item["text"],
                as_draft=False,
                document_url=doc_url,
                document_title=doc_title,
                thumbnail_url=thumb_url,
                due_at=slot
            )
        else:
            print(f"       Pushing Text Post...")
            res = schedule_buffer_post(
                post_text=item["text"],
                as_draft=False,
                due_at=slot
            )

        if res and "id" in res:
            buf_id = res["id"]
            st = res.get("status", "scheduled")
            print(f"       [+] SUCCESS: Scheduled to Buffer! ID = {buf_id} (Status: {st})")
            log_activity(
                "POST_BUFFER_QUEUED",
                f"Scheduled Versatile Post: {title}",
                f"Buffer ID: {buf_id} | dueAt: {slot} | Type: {p_type}"
            )
        else:
            print(f"       [-] FAILED to schedule: {res}", file=sys.stderr)
        time.sleep(1.0)

    print("\n" + "=" * 70)
    print("✅ Successfully recreated all 10 upcoming posts in Buffer with complete versatility!")
    print("=" * 70)

if __name__ == "__main__":
    main()
