#!/usr/bin/env python3
"""
realign_to_3_posts_per_week.py - Re-aligns the 10 Buffer slots to the optimal
3-posts/week schedule (Tuesday, Thursday, Saturday) to maximize algorithmic dwell time,
prevent audience fatigue, and minimize cloud execution minutes.
"""

import os
import sys
import json
import sqlite3
import time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
DB_PATH = os.path.join(PROJECT_ROOT, "my_account", "linkedin_tracker.db")
POSTS_DIR = os.path.join(PROJECT_ROOT, "my_account", "posts")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "my_account"))
from buffer_publisher import execute_graphql, schedule_buffer_post, get_buffer_posts

RAW_BASE = "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets"

THREE_PER_WEEK_PIPELINE = [
    # Week 1
    {
        "slot_key": "pw3_01_tue_dec_01",
        "file": "pw3_01_prompting_vs_rag_vs_finetuning.md",
        "due_at": "2026-12-01T03:00:00.000Z", # Tue Dec 01, 8:30 AM IST
        "title": "Prompting vs RAG vs Fine-Tuning: When is Each the Wrong Choice?",
        "pillar": "Production AI & Harness Architecture",
        "type": "text",
        "text": """Most engineering teams can explain what Prompting, RAG, and Fine-Tuning do. Very few can articulate when each is the WRONG choice.

In production architecture reviews, choosing the wrong paradigm is a 6-figure mistake. Here is the negative evaluation framework:

1️⃣ Prompting is the WRONG choice when:
• Your knowledge base exceeds 128k tokens or updates frequently. Stuffing 80 pages of documentation into every prompt inflates p95 latency to 6s+ and burns thousands in daily token costs.
• You require deterministic JSON outputs for mission-critical automation without schema enforcement.

2️⃣ RAG is the WRONG choice when:
• You need the model to learn a specialized syntax, domain dialect, or proprietary programming language (e.g. legacy COBOL, custom DSL, or internal assembly). RAG provides external facts; it does not alter the model's fundamental reasoning grammar.
• You need the model to adopt a consistent persona, voice, or deterministic stylistic constraint across millions of short interactions.

3️⃣ Fine-Tuning is the WRONG choice when:
• Your underlying data changes weekly or daily. Fine-tuned weights are frozen at training time. Re-training a 70B model to update product pricing is architectural malpractice.
• You require verifiable citations back to primary source clauses. Fine-tuned models hallucinate citations that look plausible but point to non-existent document paragraphs.
• You are attempting to fix factual hallucinations. Fine-tuning teaches style and formatting, not factual grounding.

The Architect Rule of Thumb:
• Want to change style, tone, or syntax? -> Fine-Tune.
• Want to provide fresh, verifiable, secure facts? -> RAG.
• Want quick experimentation on a small context window? -> Prompting.

What is the biggest mismatch you have seen between business requirements and the chosen AI paradigm?

#AIEngineering #MachineLearning #SystemDesign #SoftwareArchitecture #RAG #LLMOps #CloudArchitecture #SRE"""
    },
    {
        "slot_key": "pw3_02_thu_dec_03",
        "file": "pw3_02_prompt_to_first_token_lifecycle.md",
        "due_at": "2026-12-03T03:00:00.000Z", # Thu Dec 03, 8:30 AM IST
        "title": "From Prompt to First Token: The GPU & Gateway Lifecycle",
        "pillar": "Production AI & Harness Architecture",
        "type": "text",
        "text": """In Staff+ engineering interviews, asking 'What happens from the moment a user clicks Submit to the moment the first token arrives?' separates engineers who wrap APIs from architects who understand physical systems.

Here is the exact lifecycle down to the GPU hardware:

1️⃣ Gateway & Transport (0ms – 15ms):
• The client initiates TLS 1.3 handshake.
• API Gateway validates JWT, checks tenant token quota in Redis, and evaluates the prompt against a SHA-256 semantic cache.
• Cache miss: Request streams to inference cluster over HTTP/2.

2️⃣ Tokenization & Embedding (15ms – 25ms):
• Byte-Pair Encoding (BPE) converts input string into a 1D tensor of integer Token IDs.
• Tokens pass through the Embedding Matrix: looking up high-dimensional vectors (e.g. 4096-dim for LLaMA-70B).

3️⃣ The Prefill Phase (Compute-Bound, 25ms – 120ms):
• GPU loads prompt embeddings into Tensor Cores.
• All prompt tokens are processed in a single, massive parallel matrix multiplication (GEMM).
• Key and Value vectors for all prompt tokens are computed and written to High Bandwidth Memory (HBM) as the initial KV-Cache.
• Time-to-First-Token (TTFT) is established here.

4️⃣ The Autoregressive Decode Phase (Memory-Bound, 120ms+):
• The model samples logits across its 128k vocabulary using Temperature, Top-K, and Top-P thresholds.
• Softmax yields token #1.
• Generating token #2 requires reading all model weights from HBM to SRAM again, appending token #1's KV tensor to the KV-cache.
• Emitted tokens stream over Server-Sent Events (SSE) back to the user.

Understanding this distinction is critical: Prefill is compute-bound (saturates Tensor Cores); Decode is memory-bandwidth bound (saturates HBM bus).

How do you monitor and optimize TTFT vs generation throughput in your serving clusters?

#GPU #LLMOps #MachineLearning #SystemDesign #SoftwareEngineering #CloudArchitecture #DeepLearning #SRE"""
    },
    {
        "slot_key": "pw3_03_sat_dec_05",
        "file": "pw3_03_ai_engineer_mock_interview_handbook.md",
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
• How do you choose chunk size, and how do you know it was wrong?
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

    # Week 2
    {
        "slot_key": "pw3_04_tue_dec_08",
        "file": "pw3_04_rag_500_page_policy_pipeline.md",
        "due_at": "2026-12-08T03:00:00.000Z", # Tue Dec 08, 8:30 AM IST
        "title": "Architecting a RAG Pipeline for a 500-Page Policy Document",
        "pillar": "Production AI & Harness Architecture",
        "type": "text",
        "text": """Treating a 500-page corporate policy document or legal contract as flat OCR text is why most enterprise RAG prototypes fail in staging.

In enterprise documents, the answer to 'What is our medical reimbursement limit?' depends entirely on section hierarchies, table rows, and nested conditional clauses (e.g. 'Unless Section 14.2 applies').

If a naive chunker cuts every 500 characters, it slices right through tables, divorcing numbers from their headers.

Here is the production architecture for high-accuracy policy RAG:

1️⃣ Hierarchical Document Parsing (Docling / Unstructured):
Extract documents into structural Abstract Syntax Trees (AST). Tables are preserved as Markdown tables; headers retain their H1 > H2 > H3 parentage.

2️⃣ Recursive Document-Aware Chunking:
Chunks are bounded between 400 and 600 tokens with 10% overlap, but chunk breaks are strictly forced at section boundaries. Every chunk's metadata is injected with its parent breadcrumb:
Metadata: `Policy: Benefits > Section: Medical > Subsection: Exclusions`

3️⃣ Hybrid Retrieval (Dense Vector + Sparse BM25):
Dense vectors capture semantic intent ('refund rules'); BM25 captures exact alphanumeric legal identifiers (e.g. 'Form 1040-ES', 'Clause 9.B').
Merge via Reciprocal Rank Fusion (RRF) with alpha = 0.7.

4️⃣ Cross-Encoder Reranking:
Send top 30 candidates through a cross-encoder model (Cohere Rerank / BGE-Reranker-Large) to score actual query-passage relevance, narrowing to top 5 candidates.

5️⃣ Citation Enforcement:
The prompt requires the model to output exact sentence-level references: [Doc: Benefits.pdf, Page 142, Clause 3]. Responses failing citation validation are rejected before reaching the user.

How does your RAG pipeline parse complex tables and structural hierarchies?

#RAG #MachineLearning #DataEngineering #InformationRetrieval #Python #SoftwareArchitecture #AIEngineering #SRE"""
    },
    {
        "slot_key": "pw3_05_thu_dec_10",
        "file": "pw3_05_rag_retrieval_right_chunk_wrong_answer.md",
        "due_at": "2026-12-10T03:00:00.000Z", # Thu Dec 10, 8:30 AM IST
        "title": "Retrieval Returned the Right Chunk, But the Answer is Wrong: The Runbook",
        "pillar": "Production AI & Harness Architecture",
        "type": "text",
        "text": """Your vector search pipeline executed flawlessly. The top retrieved chunk contains the exact verbatim answer to the user's question.

Yet the model's generated answer is completely wrong or claims: 'The provided documents do not contain this information.'

What broke?

Here is the 4-step Senior Systems Architect debugging runbook:

1️⃣ Context Window Poisoning ('Lost in the Middle'):
If you pass 15 retrieved chunks and the correct chunk is placed in positions 7 through 10, attention scores drop dramatically in long-context models. LLMs have high recall at the very beginning and very end of the prompt (Primacy & Recency bias), but suffer attention dilution in the middle.
-> THE FIX: Sort retrieved chunks so the highest-scoring reranked passages sit at the top and bottom of the context block.

2️⃣ Negative System Prompt Bias:
Inspect your system directives. Directives like 'Be extremely concise' or 'If not 100% certain, refuse to answer' often overpower factual retrieval. The model sees ambiguity in phrasing and chooses the refusal path.

3️⃣ Sentence Boundary Fragmentation:
The chunking algorithm split a critical sentence in half. Chunk A says: 'Refunds are granted within 30 days.' Chunk B says: '...unless the software license has been activated.' If only Chunk A was retrieved, the answer is dangerously incomplete.
-> THE FIX: Sentence-aware chunkers with 15% sliding window overlap.

4️⃣ Tokenization Truncation:
Check your upstream gateway logs. Did the context exceed the model's max prompt token budget, causing the gateway to silently truncate the end of the prompt where the chunk was placed?

Never debug RAG by simply tweaking embeddings. 60% of RAG failures happen after retrieval has already succeeded.

How do you diagnose post-retrieval synthesis failures in production?

#RAG #MachineLearning #DataEngineering #SystemDesign #SoftwareEngineering #LLMOps #AIArchitecture #SRE"""
    },
    {
        "slot_key": "pw3_06_sat_dec_12",
        "file": "pw3_06_speculative_decoding_kv_cache_handbook.md",
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

    # Week 3
    {
        "slot_key": "pw3_07_tue_dec_15",
        "file": "pw3_07_why_tokenization_breaks_numbers_and_code.md",
        "due_at": "2026-12-15T03:00:00.000Z", # Tue Dec 15, 8:30 AM IST
        "title": "Why Tokenization Breaks Numbers, Code, and Non-English Text",
        "pillar": "Production AI & Harness Architecture",
        "type": "text",
        "text": """Why can a 400B parameter model write poetry and pass the bar exam, but fail to reverse a 5-digit number or compare 9.11 and 9.9?

The root cause is almost never the model's weights. It is the tokenizer.

Modern LLMs do not read characters or numbers. They use Byte-Pair Encoding (BPE) trained on frequency statistics of natural English prose. This introduces three massive production hazards:

1️⃣ The Numerical Blind Spot:
In BPE, '12345' is not parsed as a single mathematical quantity. Depending on token frequency, it might be split into ['12', '345'] or ['1', '23', '45'].
When asked to perform addition or reverse digits, the model is manipulating arbitrary sub-word token IDs with no mathematical relationship. '9.11' might be tokenized as ['9', '.', '11'] (where '11' is a token) and '9.9' as ['9', '.', '9']. To the model, 11 > 9, causing it to confidently declare 9.11 is greater than 9.9.

2️⃣ Code Variable Fragmentation:
Idiomatic camelCase or snake_case identifiers (e.g. `processUserAccountTransactionId`) get shredded into 4 to 6 separate tokens. This consumes 4x more context window and increases the probability of hallucinated variable spelling in generated code.

3️⃣ The Non-Latin Tax:
Because tokenizers are trained on corpora that are 85%+ English, common words in Hindi, Japanese, Arabic, or German are not allocated unique tokens. A single word in Hindi can consume 6 to 9 byte-level tokens compared to 1 token for its English translation.
• 3x to 5x higher inference latency
• 3x to 5x higher token cost
• Context window effective capacity reduced by 70%

The SRE Invariant: Never allow an LLM to perform raw mathematical arithmetic or currency conversions in text. Offload numerical computation to deterministic Python tool calls via strict JSON schema execution.

How does your architecture handle multilingual token inflation and numerical calculations?

#AIEngineering #MachineLearning #LLM #Tokenization #SoftwareEngineering #Python #DataScience #SRE"""
    },
    {
        "slot_key": "pw3_08_thu_dec_17",
        "file": "pw3_08_when_hybrid_search_hurts_rag.md",
        "due_at": "2026-12-17T03:00:00.000Z", # Thu Dec 17, 8:30 AM IST
        "title": "When Hybrid Search Hurts You: The BM25 Keyword Noise Trap",
        "pillar": "Production AI & Harness Architecture",
        "type": "text",
        "text": """Hybrid search (combining dense vector embeddings with sparse BM25 keyword search) is widely recommended as best practice.

Yet in production, naive hybrid search frequently degrades accuracy compared to vector-only search.

Why? The Keyword Flooding Trap.

BM25 scores documents based on Term Frequency-Inverse Document Frequency (TF-IDF). It has zero semantic understanding; it rewards exact character string repetition.

Consider this user prompt:
'Can I get a refund if my business flight was canceled due to sudden winter snowstorms?'

• Dense Vector Search: Accurately maps the semantic concept to your policy sections on: `Trip Disruption`, `Carrier Cancellations`, and `Force Majeure Exceptions`.
• Sparse BM25 Search: Heavily weights the rare words 'winter', 'snowstorms', and 'flight'. It retrieves marketing press releases about winter holiday flight destinations and weather safety tips for pilots—none of which contain refund policies.

When Reciprocal Rank Fusion (RRF) merges these sets, the irrelevant keyword-heavy documents push the actual policy passages out of the top-5 context window.

How senior architects harden hybrid retrieval:
1️⃣ Semantic Density Gating: Check semantic similarity distance first. If vector similarity is > 0.92, discard BM25 candidates completely.
2️⃣ Tunable RRF Weights: Weight dense vectors at 0.75 and BM25 at 0.25 for conversational queries; flip weights only for exact SKU or code lookups.
3️⃣ Cross-Encoder Arbitration: Never pass raw hybrid search results to the LLM. Always pass them through a cross-encoder reranker to strip false keyword matches.

Tools are only as good as their arbitration logic.

How do you tune your dense-to-sparse fusion ratios under production traffic?

#Search #InformationRetrieval #RAG #MachineLearning #VectorSearch #Python #SoftwareArchitecture #SRE"""
    },
    {
        "slot_key": "pw3_09_sat_dec_19",
        "file": "pw3_09_multiregion_crdt_handbook.md",
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

    # Week 4
    {
        "slot_key": "pw3_10_tue_dec_22",
        "file": "pw3_10_speculative_decoding_enterprise_prod.md",
        "due_at": "2026-12-22T03:00:00.000Z", # Tue Dec 22, 8:30 AM IST
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

def save_markdown_post(p):
    os.makedirs(POSTS_DIR, exist_ok=True)
    fpath = os.path.join(POSTS_DIR, p["file"])
    
    doc_lines = ""
    if p["type"] == "document":
        doc_lines = f'document_pdf: "{p["pdf_name"]}"\ndocument_cover: "{p["cover_name"]}"\n'
        
    content = f"""---
title: "{p['title']}"
pillar: "{p['pillar']}"
slot: "{p['due_at']}"
status: "scheduled"
buffer_post_id: "{p.get('buffer_id', '')}"
{doc_lines}---

{p['text']}
"""
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)

def main():
    print("=" * 70)
    print("🚀 REALIGNING BUFFER QUEUE TO 3 POSTS PER WEEK (TUE, THU, SAT)")
    print("=" * 70)

    # 1. Clear current Buffer queue
    print("\n[1] Clearing existing scheduled queue...")
    posts = get_buffer_posts()
    scheduled = [p for p in posts if p.get("status") == "scheduled"]
    print(f"    Found {len(scheduled)} scheduled post(s) to realign.")

    for p in scheduled:
        pid = p["id"]
        due = p.get("dueAt")
        print(f"    Clearing slot {pid} ({due})...")
        delete_buffer_post(pid)
        time.sleep(0.5)

    print("[+] Queue cleared!")

    # 2. Push 10 posts spaced 3/week (Tue, Thu, Sat)
    print("\n[2] Scheduling 10 posts across 3.5 weeks (Tue, Thu, Sat)...")
    for idx, item in enumerate(THREE_PER_WEEK_PIPELINE, 1):
        slot = item["due_at"]
        title = item["title"]
        p_type = item["type"]
        print(f"\n({idx}/10) Scheduling: {title}")
        print(f"       Slot: {slot}")

        if p_type == "document":
            doc_url = f"{RAW_BASE}/{item['pdf_name']}"
            thumb_url = f"{RAW_BASE}/{item['cover_name']}"
            doc_title = item["doc_title"]
            res = schedule_buffer_post(
                post_text=item["text"],
                as_draft=False,
                document_url=doc_url,
                document_title=doc_title,
                thumbnail_url=thumb_url,
                due_at=slot
            )
        else:
            res = schedule_buffer_post(
                post_text=item["text"],
                as_draft=False,
                due_at=slot
            )

        if res and "id" in res:
            buf_id = res["id"]
            item["buffer_id"] = buf_id
            print(f"       [+] SUCCESS: Scheduled to Buffer! ID = {buf_id}")
        else:
            print(f"       [-] FAILED to schedule: {res}", file=sys.stderr)

        save_markdown_post(item)
        time.sleep(1.0)

    # Update database
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for p in THREE_PER_WEEK_PIPELINE:
        cur.execute("""
            INSERT OR REPLACE INTO posts (post_key, filename, title, pillar, day_slot, content, status, buffer_post_id, scheduled_at, updated_at)
            VALUES (?, ?, ?, ?, '3-Posts/Week Slot', ?, 'scheduled', ?, ?, CURRENT_TIMESTAMP)
        """, (p['slot_key'], p['file'], p['title'], p['pillar'], p['text'], p.get('buffer_id', ''), p['due_at']))
    conn.commit()
    conn.close()

    print("\n" + "=" * 70)
    print("✅ Buffer queue successfully realigned to 3 posts per week (Tue, Thu, Sat)!")
    print("=" * 70)

if __name__ == "__main__":
    main()
