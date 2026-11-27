#!/usr/bin/env python3
"""
generate_versatile_handbooks.py - Compiles a versatile suite of cutting-edge,
incremental architectural handbooks with pure single-color blue ballpoint pen
handwritten styling, 100% boundary safety, and ZERO personal undersigned references.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")

sys.path.insert(0, HERE)
from pdf_architect_engine import HandwrittenHandbookBuilder

def build_interview_handbook():
    print("[*] Generating 1. AI Engineer Mock Interview Field Manual (12 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="AI INTERVIEW & SRE EVALUATION",
        handbook_name="AI_Engineer_Mock_Interview_Handbook",
        theme_badge="MOCK REHEARSAL PLAYBOOK"
    )

    # 1. Cover
    b.add_cover(
        title="THE AI ENGINEER\nMOCK INTERVIEW FIELD MANUAL",
        subtitle="The Exact Questions & Staff+ Architecture Blueprints to Rehearse\nBefore Walking Into Any Enterprise AI or Systems Design Loop",
        curriculum=[
            "Warm-Up & Shipped AI Systems (Two Minutes Each)",
            "Fundamentals Under Pressure (Tokenization, Top-P, Reasoning Models)",
            "RAG Deep Dive & 500-Page Policy Pipelines (Chunking & Retrieval Flaws)",
            "Autonomous Agent Scenarios (Idempotency, Infinite Retries, Drift)",
            "Evaluation Challenges & Production Drift (Offline vs Online Divergence)",
            "Whiteboard System Design (Permissioned Q&A & Refund Agent Safeguards)",
            "Safety, Trust & Red-Teaming (Prompt Injections & Sensitive Log Hygiene)",
            "Behavioral Post-Mortems & The 4-Step Timed Rehearsal Protocol"
        ]
    )

    # Page 2: Warm-Up
    b._start_new_page("Round 1: Warm-Up Rehearsal (2 Min Each)")
    b.add_qa_card(
        question="Q: Tell me about yourself and the AI work you've actually shipped.",
        answer_paragraphs=[
            "THE 90-SECOND ARCHITECT PITCH:",
            "• Hook & Scope: Lead platform architecture focusing on enterprise AI execution harnesses, production RAG pipelines, and deterministic agent governance.",
            "• Concrete System Shipped: Architected a multi-tenant retrieval and inference gateway serving 4.5M monthly customer queries. Reduced p95 latency from 4.2s to 680ms while maintaining sub-10ms cache invalidation via Debezium CDC.",
            "• SRE Invariant: Treat foundation models as untrusted third-party dependencies with circuit breakers, token budgets, and rigid JSON schema validation at the system boundary."
        ],
        tag="WARM-UP • 2 MINS"
    )
    b.add_qa_card(
        question="Q: Explain RAG to a product manager who has never heard of it.",
        answer_paragraphs=[
            "THE ANALOGY CONTRACT:",
            "Imagine an open-book exam. A raw LLM is a brilliant student relying entirely on memory from books read two years ago. Sometimes they forget details or invent facts (hallucination).",
            "Retrieval-Augmented Generation (RAG) is giving that student an assistant who instantly pulls the exact 3 relevant company policy pages from the library right when a question is asked.",
            "VERDICT: The model doesn't guess private quarterly numbers; it reads directly from the fresh documents put in front of it."
        ],
        tag="EXECUTIVE COMMUNICATION"
    )

    # Page 3: RAG vs Fine-Tuning & Hallucinations
    b._start_new_page("Round 1 (Cont.): Core Dilemmas & Hallucinations")
    b.add_qa_card(
        question="Q: Prompting vs RAG vs Fine-Tuning: When is each the WRONG choice?",
        answer_paragraphs=[
            "• Prompting is WRONG when: Knowledge exceeds 128k context, updates daily, or requires multi-million token batch costs.",
            "• RAG is WRONG when: The model must learn a specialized syntax (e.g. proprietary DSL, assembly, COBOL) or adopt a distinct tone/style rather than reference factual data.",
            "• Fine-Tuning is WRONG when: Underlying data changes frequently (fine-tuning is frozen at training time) or when citations/attribution back to source paragraphs are required."
        ],
        tag="DECISION FRAMEWORK"
    )
    b.add_qa_card(
        question="Q: Why do models hallucinate, and what do you do about it in production?",
        answer_paragraphs=[
            "ROOT CAUSE: Autoregressive Next-Token Probability.",
            "Models do not have internal truth verification; they predict the mathematically most probable next token given the prompt context.",
            "PRODUCTION MITIGATION:",
            "1. Grounding Fences: Constrain prompts to answer ONLY from retrieved context.",
            "2. Structured Verification: Pass output through JSON schema validators.",
            "3. Hallucination Guardrails: Run an automated citation-checker that confirms every factual statement links to a specific sentence in the retrieved chunk."
        ],
        tag="SRE ROOT-CAUSE"
    )

    # Page 4: Fundamentals Under Pressure
    b._start_new_page("Round 2: Fundamentals Under Pressure")
    b.add_qa_card(
        question="Q: What happens from prompt dispatch to the first returned token?",
        answer_paragraphs=[
            "1. Client Gateway: TLS handshake, auth verification, token budgeting, and semantic cache lookup (SHA-256 + compound key).",
            "2. Tokenization: Byte-Pair Encoding (BPE) converts string text into token IDs.",
            "3. KV-Cache & Prefill: GPU loads token embeddings into Key-Value cache in a single parallelized forward pass.",
            "4. Autoregressive Decode: The model samples logits across vocabulary (via Temp/Top-P) and emits the first token (Time-to-First-Token, TTFT).",
            "5. SSE Stream: First token chunks over HTTP/2 Server-Sent Events to client."
        ],
        tag="INFERENCE INTERNALS"
    )
    b.add_qa_card(
        question="Q: Why does tokenization cause problems with numbers, code & non-English text?",
        answer_paragraphs=[
            "• Numbers: BPE splits '12345' arbitrarily into ['12', '345'] or ['1', '23', '45']. The model never sees mathematical values, only unrelated sub-word fragment IDs.",
            "• Code: Variable names (e.g. 'getUserAccountBalance') get fragmented into 4+ tokens, increasing token burn and syntax errors.",
            "• Non-English Text: Tokenizers trained heavily on English allocate single characters or multi-byte sequences to non-Latin scripts, causing 3x-5x token inflation and higher latency."
        ],
        tag="TOKENIZER DYNAMICS"
    )

    # Page 5: Sampling & Reasoning Models
    b._start_new_page("Round 2 (Cont.): Sampling Parameters & Reasoning Models")
    b.add_qa_card(
        question="Q: What do Temperature, Top-K, and Top-P each change?",
        answer_paragraphs=[
            "• Temperature (T): Scales raw logits before softmax. T=0 collapses distribution to argmax (deterministic). High T flattens probabilities (more creative/random).",
            "• Top-K: Hard truncate vocabulary to the K highest-probability tokens. Ignores the long-tail of low-probability words entirely.",
            "• Top-P (Nucleus Sampling): Dynamically accumulates tokens until cumulative probability hits P (e.g. 0.90). Adapts to sharp vs flat distributions dynamically."
        ],
        tag="PROBABILITY CONTROLS"
    )
    b.add_qa_card(
        question="Q: When to use a reasoning model (o1/R1) vs when is it wasted cost?",
        answer_paragraphs=[
            "• USE WHEN: Multi-step logic, code contract refactoring, mathematical proofs, complex dependency graphs, and planning multi-tool workflows.",
            "• WASTED COST WHEN: Routine text summarization, FAQ lookup, sentiment classification, entity extraction, or structured JSON reformatting.",
            "FINOPS INVARIANT: Using a 10x priced reasoning model for basic document search is a 90% budget burn to disguise lazy system prompt architecture."
        ],
        tag="FINOPS SELECTION"
    )

    # Page 6: RAG Deep Dive
    b._start_new_page("Round 3: Production RAG Deep Dive")
    b.add_qa_card(
        question="Q: Walk me through a RAG pipeline for a 500-page policy document.",
        answer_paragraphs=[
            "STEP 1: Hierarchical Document Parsing (Docling / Unstructured).",
            "Preserve table structures, header hierarchies (H1/H2/H3), and page boundaries. Never treat a 500-page PDF as flat OCR text.",
            "STEP 2: Recursive Markdown Chunking.",
            "Chunk size: 400-600 tokens with 10% overlap, strictly respecting section boundaries.",
            "STEP 3: Hybrid Retrieval (Dense Vector + BM25 Sparse).",
            "Query matches semantic intent AND exact policy codes (e.g. 'Section 14.2(b)').",
            "STEP 4: Cross-Encoder Reranking (Cohere / BGE-Reranker-Large).",
            "Rerank top 30 candidates down to top 5 most relevant passages before prompt injection."
        ],
        tag="PIPELINE BLUEPRINT"
    )
    b.add_qa_card(
        question="Q: Retrieval returns the right chunk but the answer is wrong. What do you check?",
        answer_paragraphs=[
            "1. Context Window Poisoning: Is the chunk buried in the middle of 20 other irrelevant chunks? (The 'Lost in the Middle' phenomenon).",
            "2. Negative Prompt Bias: Does the system prompt have conflicting directives (e.g. 'Be concise' overriding required clause disclaimers)?",
            "3. Chunk Fragmentation: Was the critical condition split across two adjacent chunks?",
            "4. Context Window Truncation: Check whether upstream gateway truncated the prompt."
        ],
        tag="DEBUGGING RUNBOOK"
    )

    # Page 7: Chunking & Hybrid Search
    b._start_new_page("Round 3 (Cont.): Chunk Size & Hybrid Search Perils")
    b.add_qa_card(
        question="Q: How do you choose chunk size, and how do you know it's wrong?",
        answer_paragraphs=[
            "• Too Small (e.g. 100 tokens): Loses sentence context, table rows, and conditional clauses. Evident when retrieval accuracy is high but model hallucinates explanations.",
            "• Too Large (e.g. 2000 tokens): Dilutes embedding specificity. The vector represents 5 different topics; cosine similarity drops on precise queries.",
            "HOW TO DETECT IN CI/CD:",
            "Run automated hit-rate@k and MRR (Mean Reciprocal Rank) on a golden test dataset. If hit-rate drops below 85%, adjust chunk boundaries."
        ],
        tag="CHUNKING METRICS"
    )
    b.add_qa_card(
        question="Q: When would hybrid search hurt you compared to vector-only?",
        answer_paragraphs=[
            "THE PERIL OF KEYWORD NOISE: Sparse BM25 searches match exact character strings without semantic understanding.",
            "If a user asks: 'Can I get a refund if the flight was canceled due to bad weather?', BM25 might pull chunks heavily featuring 'flight' and 'weather' that discuss baggage allowances rather than cancellation policies.",
            "THE FIX: Reciprocal Rank Fusion (RRF) with a tunable alpha parameter (0.7 vector / 0.3 keyword) to prevent keyword flooding."
        ],
        tag="RETRIEVAL PITFALL"
    )

    # Page 8: Autonomous Agents & Idempotency
    b._start_new_page("Round 4: Autonomous Agent Scenarios")
    b.add_qa_card(
        question="Q: Your agent calls the same tool 5 times in a row. What do you investigate?",
        answer_paragraphs=[
            "1. Uninformative Error Payloads: The tool returns a generic '500 Internal Error' or empty string. The model has no guidance on what to fix and tries again.",
            "2. Schema Mismatch: The model hallucinates parameter names that fail schema parsing without giving feedback to the context.",
            "3. Missing Completion Invariant: The prompt lacks a stop condition or success signal.",
            "SRE FIX: Implement a 3-strike circuit breaker and hard max_iterations = 4 cap."
        ],
        tag="AGENT DEBUGGING"
    )
    b.add_qa_card(
        question="Q: A tool call fails halfway through and retries. How to prevent duplicate side effects?",
        answer_paragraphs=[
            "THE ARCHITECT CONTRACT: Idempotency Keys.",
            "1. Client generates an immutable Idempotency-Key: SHA256(session_id + step_count + tool_params).",
            "2. Tool execution engine checks Redis before executing: IF key exists in 'PENDING' or 'COMPLETED' state, return existing response without re-executing.",
            "3. Two-Phase Commit for Financial Actions: Never allow an agent to trigger refunds or database mutations in a fire-and-forget loop."
        ],
        tag="IDEMPOTENCY INVARIANT"
    )

    # Page 9: Multi-Agent Topologies & Long Memory
    b._start_new_page("Round 4 (Cont.): Multi-Agent Cost & Memory Drift")
    b.add_qa_card(
        question="Q: When choose multi-agent over single agent, and what does it cost?",
        answer_paragraphs=[
            "• CHOOSE MULTI-AGENT WHEN: Specialized roles require isolated system prompts and strict tool segregation (e.g. Researcher -> Coder -> Verifier).",
            "• THE REAL COSTS:",
            "  1. Token Bloat: Multi-agent conversations pass whole dialogue histories, increasing token cost by 4x to 8x.",
            "  2. Latency Penalty: Serial agent hops add 3s-8s per round-trip.",
            "  3. Non-Deterministic Deadlocks: Agents can loop politely thanking each other without reaching completion."
        ],
        tag="MULTI-AGENT TRADE-OFF"
    )
    b.add_qa_card(
        question="Q: How do you keep an agent reliable over a long session with growing memory?",
        answer_paragraphs=[
            "1. Sliding Window + Structured Summarization: Evict raw messages past 10 turns and maintain a structured JSON 'State Ledger' of active entities.",
            "2. Episodic vs Working Memory: Store long-term facts in an external vector store, retrieving only upon explicit query.",
            "3. Monotonic Epoch Reset: If token drift exceeds 64k tokens, compact the scratchpad to preserve inference speed and prevent context saturation."
        ],
        tag="LONG-CONTEXT SRE"
    )

    # Page 10: Evaluation & Production Drift
    b._start_new_page("Round 5: Evals, Safety & Production Drift")
    b.add_qa_card(
        question="Q: LLM judge and human users disagree. Whose signal do you trust?",
        answer_paragraphs=[
            "VERDICT: Trust Human User Outcomes Every Time.",
            "LLM judges suffer from position bias, verbosity bias (favoring longer answers), and self-preference bias (ranking their own model family higher).",
            "THE SRE SIGNAL: Measure implicit user feedback: thumb-downs, copy-to-clipboard rates, session abandoned queries, and ticket escalations.",
            "Use disagreement samples to calibrate LLM judge prompts and few-shot rubric."
        ],
        tag="EVALUATION GOVERNANCE"
    )
    b.add_qa_card(
        question="Q: Offline eval passed but production quality dropped. What did you miss?",
        answer_paragraphs=[
            "THE 4 REAL-WORLD DIVERGENCES:",
            "1. Distribution Drift: Real users ask shorter, sloppier, typo-filled queries than curated test suites.",
            "2. Tool Dependency Latency: Production 3rd party APIs timed out under load, triggering fallback branches not tested in staging.",
            "3. Data Freshness Gap: Offline evals tested against a static snapshot; production documents were updated without re-indexing.",
            "4. Multi-Turn Context Contamination: Offline evals were single-turn; production users ask contextual follow-ups."
        ],
        tag="PRODUCTION DIVERGENCE"
    )

    # Page 11: System Design Whiteboard
    b._start_new_page("Round 6: 30-Min Whiteboard System Design")
    b.add_qa_card(
        question="Q: Design a Document Q&A System with Strict Multi-Tenant Data Permissions.",
        answer_paragraphs=[
            "1. Ingestion: Documents tagged with ACL metadata (Tenant ID, Department, Role Scope).",
            "2. Pre-Filtering at Query Time: Vector similarity MUST execute with metadata filters (WHERE tenant_id = ? AND role IN (?)). Never search global vector index.",
            "3. Post-Retrieval Validation: Independent auth gateway confirms user JWT token still possesses read permission on document ID before injecting into LLM context.",
            "4. Zero-Leak Audit Log: Every response logs user_id, doc_ids accessed, and cryptographic hash of retrieved text for SOC2/HIPAA compliance."
        ],
        tag="SYSTEM DESIGN 1"
    )
    b.add_qa_card(
        question="Q: Design a Customer Support Agent that can Issue Refunds with Safeguards.",
        answer_paragraphs=[
            "1. Tiered Financial Failsafe: Automated refunds allowed ONLY under $50. Greater amounts trigger human-in-the-loop escalation.",
            "2. Velocity Rate Limiting: Max 1 refund per user per 30 days; max $5,000 global daily budget.",
            "3. Deterministic State Machine: Decouple generative dialog from transactional tool invocation. The model extracts parameters; a typed Python harness verifies business logic before calling Stripe API."
        ],
        tag="SYSTEM DESIGN 2"
    )

    # Page 12: Rehearsal Protocol
    b._start_new_page("Round 7: How to Run the Mock Rehearsal Loop")
    b.add_qa_card(
        question="Q: The Senior Architect Practice Protocol: How to practice so you never fail.",
        answer_paragraphs=[
            "1. Set a Strict Timer: 2 minutes per concept question; 30 minutes for whiteboard system design. If you exceed 2 minutes on a concept, you failed the clarity test.",
            "2. Record Audio & Listen Back: Cringe early so you don't cringe in the loop. Listen for filler words ('basically', 'kind of', 'like'), vague hand-waving, and missing metrics.",
            "3. Rate Each Answer: Clear (ready), Shaky (knows concept but stumbled on numbers), Lost (blanked or guessed).",
            "4. The Redo Invariant: Redo every shaky and lost answer immediately until it rolls off your tongue with concrete architecture configs and numbers."
        ],
        tag="PRACTICE PROTOCOL"
    )
    b.add_invariant(
        title="PRODUCTION SRE DOCTRINE BEATS BUZZWORDS",
        rule_body="Interviews are not won by quoting papers. They are won by architects who describe failure modes, state boundaries, latency percentiles, and exact mitigation runbooks."
    )

    out_file = os.path.join(ASSETS_DIR, "AI_Engineer_Mock_Interview_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

def build_speculative_decoding_handbook():
    print("[*] Generating 2. Speculative Decoding & KV-Cache Paging Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="INFERENCE ACCELERATION & MEMORY SRE",
        handbook_name="Speculative_Decoding_KVCache_Handbook",
        theme_badge="GPU INFERENCE SPECIFICATION"
    )

    # Cover
    b.add_cover(
        title="SPECULATIVE DECODING\n& KV-CACHE PAGING FIELD MANUAL",
        subtitle="Accelerating 70B LLM Inference by 2.8x with 1B Draft Models\nand Eliminating GPU Memory Fragmentation via PagedAttention",
        curriculum=[
            "The Memory-Bound Bottleneck: Memory Bandwidth vs Arithmetic Intensity",
            "Speculative Decoding Mechanics: Draft K Tokens + Parallel Verification",
            "Acceptance Rate Dynamics: When Speculative Decoding Slows You Down",
            "KV-Cache Memory Bleed: Virtual Memory Paging with vLLM PagedAttention",
            "Continuous Batching & Chunked Prefill: Sub-50ms TTFT under 500 QPS",
            "Staff+ Systems Architect Production Inference SRE Verification Checklist"
        ]
    )

    # Page 2: Memory Bandwidth vs Compute
    b._start_new_page("Chapter 1: The Memory-Bound Inference Bottleneck")
    b.add_card(
        tag="GPU ARCHITECTURE AUDIT",
        title="Why is single-token autoregressive LLM decoding memory-bandwidth bound?",
        body_paragraphs=[
            "THE SYSTEM BOTTLENECK: Arithmetic Intensity < 1 FLOP/byte.",
            "In autoregressive generation, generating 1 token requires streaming all 140GB of weights (for a 70B FP16 model) from GPU HBM to SRAM for just one matrix-vector multiplication.",
            "• On an NVIDIA H100 (3.35 TB/s memory bandwidth), reading 140GB takes 41.7 milliseconds per token.",
            "• The Tensor Cores sit 96% idle while waiting on memory bus transfers.",
            "THE ARCHITECTURAL FIX: Speculative Decoding.",
            "Instead of reading 140GB per token, run a fast 1B draft model (which takes 1ms) to propose K candidate tokens, then verify ALL K tokens in a single parallel forward pass on the 70B model."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="SYSTEM INVARIANT: BATCHING OVER SERIAL LATENCY",
        rule_body="Never optimize GPU inference by increasing compute clock frequencies. Optimize memory bandwidth efficiency: process multiple tokens per memory load."
    )

    # Page 3: Draft Verification Math
    b._start_new_page("Chapter 2: Draft Proposal & Verification Mechanics")
    b.add_card(
        tag="SPECULATIVE ALGORITHM",
        title="How draft tokens are accepted without altering output distribution:",
        body_paragraphs=[
            "1. Draft Phase: A small draft model (e.g. LLaMA-1B) generates K=5 tokens sequentially in ~6ms.",
            "2. Target Verification Phase: The 70B target model evaluates all 5 tokens simultaneously in one forward pass (42ms).",
            "3. Modified Rejection Sampling: Accept token i if target_prob / draft_prob >= uniform_random(0,1).",
            "• Mathematically Proven: The output distribution is 100% identical to running the 70B model alone.",
            "• Speedup Factor: If acceptance rate alpha = 0.82, expected tokens per step = 4.1 tokens in 48ms (vs 1 token in 42ms) -> 3.5x effective throughput gain."
        ]
    )
    b.add_card(
        tag="FAILURE MODE",
        title="When does Speculative Decoding SLOW DOWN inference?",
        body_paragraphs=[
            "• Complex Reasoning / Math: If the draft model has low acceptance (alpha < 0.35), verifying rejected tokens adds overhead without generating forward progress.",
            "• High GPU Concurrency: If batch size > 32, GPUs transition from memory-bound to compute-bound; speculative verification causes compute saturation."
        ]
    )

    # Page 4: KV-Cache Fragmentation
    b._start_new_page("Chapter 3: PagedAttention & Eliminating KV Fragmentation")
    b.add_card(
        tag="KERNEL MEMORY ENGINE",
        title="Why standard KV-caches waste 60% of GPU VRAM:",
        body_paragraphs=[
            "THE PROBLEM: Contiguous Memory Pre-Allocation.",
            "Legacy frameworks allocate a contiguous memory chunk for max_sequence_length (e.g. 8,192 tokens) per request. If the user stops generating at 150 tokens, the remaining 98% of memory is locked and wasted (Internal Fragmentation).",
            "THE VLLM INNOVATION: PagedAttention.",
            "1. Inspired by OS Virtual Memory: PagedAttention divides the KV-cache into fixed-size physical blocks (e.g. 16 tokens).",
            "2. Block Table Mapping: Logical token positions are mapped dynamically to non-contiguous physical blocks via a block table.",
            "3. Zero Memory Waste: Memory is allocated on-demand as tokens generate. Waste is bounded to <4%."
        ]
    )
    b.add_invariant(
        title="INFERENCE CONCURRENCY INVARIANT",
        rule_body="GPU memory fragmentation is the primary ceiling on serving throughput. Eliminating fragmentation via PagedAttention increases serving capacity by 2.2x to 4x on identical hardware."
    )

    # Page 5: Continuous Batching & Chunked Prefill
    b._start_new_page("Chapter 4: Continuous Batching & Chunked Prefill")
    b.add_card(
        tag="SCHEDULER ARCHITECTURE",
        title="Eliminating Head-of-Line Blocking in LLM Inference Gateways:",
        body_paragraphs=[
            "1. Continuous (Iteration-Level) Batching:",
            "Instead of waiting for an entire batch to finish, the engine evicts completed sequences at every single iteration and injects new requests immediately into the active batch.",
            "2. Chunked Prefill (vLLM / TensorRT-LLM):",
            "Prefill (prompt processing) is compute-heavy; decode is memory-heavy. Running a 4,000-token prompt prefill freezes ongoing decode iterations for 800ms (Decode Latency Spike).",
            "Chunked prefill splits large prompts into 512-token chunks, interleaving them smoothly with ongoing decode steps."
        ]
    )
    b.add_card(
        tag="PRODUCTION LATENCY PROFILE",
        title="Serving Metrics Comparison (70B Model on 4x H100):",
        body_paragraphs=[
            "• Naive Static Batching: p99 Latency = 8,400ms | Concurrency = 12 streams.",
            "• Continuous Batching + Speculative Decoding: p99 Latency = 1,850ms | Concurrency = 54 streams."
        ]
    )

    # Page 6: Checklist
    b._start_new_page("Chapter 5: Production Inference SRE Verification Checklist")
    b.add_card(
        tag="PRODUCTION READINESS",
        title="The Senior Systems Architect Pre-Launch Inference Gateway Verification:",
        body_paragraphs=[
            "[✓] Speculative Draft Pair Validated: Draft model vocabulary aligns with target model.",
            "[✓] Acceptance Rate Monitored: Prometheus alert fires if acceptance drops < 60%.",
            "[✓] PagedAttention Active: Memory block size configured to 16/32 tokens.",
            "[✓] Chunked Prefill Enabled: Chunk size set to 512 tokens to suppress decode spikes.",
            "[✓] KV-Cache Offloading Failsafe: CPU RAM swap configured if GPU memory exceeds 92%.",
            "[✓] Latency SLOs Verified: TTFT < 80ms p95; Generation rate > 65 tokens/sec per stream.",
            "[✓] Negative ADR Documented: Architectural trade-offs of speculative vs quantized models recorded."
        ]
    )
    b.add_invariant(
        title="THE CORE INFERENCE DOCTRINE",
        rule_body="Inference efficiency is not about faster matrix multipliers; it is about keeping memory channels saturated while avoiding wasteful computation."
    )

    out_file = os.path.join(ASSETS_DIR, "Speculative_Decoding_and_KVCache_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

def build_multiregion_crdt_handbook():
    print("[*] Generating 3. Multi-Region Data Topologies & CRDTs Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="DISTRIBUTED DATA & HIGH AVAILABILITY",
        handbook_name="MultiRegion_Data_Topologies_CRDTs_Handbook",
        theme_badge="GLOBAL SYSTEMS BLUEPRINT"
    )

    # Cover
    b.add_cover(
        title="MULTI-REGION DATA TOPOLOGIES\n& CRDTs FIELD MANUAL",
        subtitle="Designing Active-Active Distributed Systems Across Continents\nWithout Split-Brain Partition Disasters or 200ms Consensus Taxes",
        curriculum=[
            "The Cross-Continent Latency Penalty: Speed of Light vs Raft Consensus",
            "Conflict-Free Replicated Data Types (CRDTs): State-Based vs Operation-Based",
            "Vector Clocks & Monotonic Version Vectors: Establishing Causal Order",
            "The Split-Brain Partition Nightmare: Fencing Off Zombie Primaries",
            "Read-Your-Writes Consistency: Monotonic Read Sessions & Local Caching",
            "Staff+ Systems Architect Global Active-Active Launch Checklist"
        ]
    )

    # Page 2: Speed of light & Consensus
    b._start_new_page("Chapter 1: The Physics of Cross-Continent Replication")
    b.add_card(
        tag="DISTRIBUTED SYSTEMS LAW",
        title="Why synchronous multi-region consensus (Raft/Paxos) destroys SLAs:",
        body_paragraphs=[
            "THE SPEED OF LIGHT BOUNDARY: 140ms Round-Trip.",
            "Network round-trip latency between Virginia (us-east-1) and Frankfurt (eu-central-1) is ~85ms. Round-trip to Singapore is ~190ms.",
            "THE SYSTEM FAILURE: Synchronous Raft Multi-Region Writes.",
            "If an application uses synchronous Raft consensus across 3 continents, every single database INSERT or UPDATE must wait for cross-ocean quorum confirmation.",
            "• p95 write latency spikes from 3ms to 240ms.",
            "• Upstream HTTP connection pools exhaust under high concurrency.",
            "• A transient undersea cable blip triggers cascading leader election storms."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="CAP THEOREM INVARIANT",
        rule_body="You cannot beat the speed of light. In a multi-region deployment, choose where to pay: pay in high write latency (CP) or pay in complex conflict resolution (AP)."
    )

    # Page 3: CRDTs
    b._start_new_page("Chapter 2: Conflict-Free Replicated Data Types (CRDTs)")
    b.add_card(
        tag="DATA STRUCTURE CONTRACT",
        title="How CRDTs achieve mathematical convergence without central coordination:",
        body_paragraphs=[
            "THE MATHEMATICAL GUARANTEE: Semilattice Join Property.",
            "CRDT operations are Commutative (A + B = B + A), Associative ((A + B) + C = A + (B + C)), and Idempotent (A + A = A).",
            "1. State-Based CRDTs (CvRDT): Nodes periodically gossip entire states. States merge via a deterministic join operator (LWW - Last-Write-Wins or PN-Counters).",
            "2. Operation-Based CRDTs (CmRDT): Nodes broadcast atomic operations over causally ordered message streams. Commutativity ensures identical final state regardless of packet arrival order.",
            "• Use Case: Shopping carts, collaborative document editing, active inventory counters, and multi-region user profiles."
        ]
    )
    b.add_card(
        tag="THE DANGEROUS PITFALL",
        title="The Last-Write-Wins (LWW) Clock Drift Trap:",
        body_paragraphs=[
            "Relying on wall-clock timestamps for LWW results in silent data loss if server clocks drift by even 25ms. Always use Hybrid Logical Clocks (HLC) or Vector Clocks to establish true causal precedence."
        ]
    )

    # Page 4: Split-Brain & Fencing
    b._start_new_page("Chapter 3: Split-Brain Isolation & Fencing Tokens")
    b.add_card(
        tag="DISASTER RECOVERY ARCHITECTURE",
        title="How to prevent split-brain dual-primary corruption during network partitions:",
        body_paragraphs=[
            "THE SCENARIO: Network Partition Across the Atlantic.",
            "US region cannot reach EU region. If both regions believe they are the active primary, both accept conflicting customer orders (Split-Brain Disaster).",
            "THE MITIGATION RUNBOOK:",
            "1. Quorum Witnesses in Region 3: Place a lightweight consensus witness in a 3rd independent region (e.g. Ireland). A partition must win 2-of-3 votes to accept writes.",
            "2. Monotonic Fencing Tokens: Every leader promotion increments an atomic generation counter. Storage backends reject any write carrying a stale epoch token.",
            "3. Auto-Demotion: If a primary loses quorum heartbeat for >3,000ms, immediately transition to Read-Only degraded mode."
        ]
    )
    b.add_invariant(
        title="FENCING INVARIANT",
        rule_body="Never rely on software self-resignation. Storage engines must enforce monotonic fencing tokens to reject zombie leader writes at the hardware layer."
    )

    # Page 5: Read-Your-Writes
    b._start_new_page("Chapter 4: Read-Your-Writes & Session Monotonicity")
    b.add_card(
        tag="CONSISTENCY ARCHITECTURE",
        title="Preventing customer-facing time travel anomalies:",
        body_paragraphs=[
            "THE ANOMALY: The Vanishing Update.",
            "A user in London posts a comment (written to local EU node). They refresh the page; the load balancer routes the read to a replica that has not yet received cross-region replication. The comment disappears.",
            "THE SRE MECHANISM: Monotonic Session Versioning.",
            "1. Write returns a Version Stamp (e.g. LSN = 458921).",
            "2. Client cookie / JWT stores min_required_lsn.",
            "3. Gateway verifies: Read request routes ONLY to a replica whose local replication LSN >= client_lsn.",
            "4. If local replica is lagging: Fast-forward read to origin primary or hold response for up to 30ms until replica catches up."
        ]
    )
    b.add_card(
        tag="CONSISTENCY LADDER",
        title="Latency vs Consistency Hierarchy:",
        body_paragraphs=[
            "• Strict Linearizable: 180ms p95 (Global consensus required).",
            "• Read-Your-Writes Session: 8ms p95 (Local replica with version gating).",
            "• Eventual Convergence (CRDT): 1.5ms p95 (Sub-millisecond local reads/writes)."
        ]
    )

    # Page 6: Checklist
    b._start_new_page("Chapter 5: Multi-Region Active-Active Launch Checklist")
    b.add_card(
        tag="GLOBAL SRE GATE",
        title="The Senior Systems Architect Pre-Launch Multi-Region Verification:",
        body_paragraphs=[
            "[✓] Quorum Oddity: Minimum 3 voting nodes / regions configured to prevent tie-breakers.",
            "[✓] HLC Implemented: Hybrid Logical Clocks synchronizing nodes with NTP bounded drift.",
            "[✓] Monotonic Fencing Tokens: All datastore writes validated against current generation token.",
            "[✓] Read-Your-Writes Gating: Session cookies carry minimum LSN version stamps.",
            "[✓] Chaos Partition Testing: Jepsen or Chaos Mesh partition tests executed in staging.",
            "[✓] Ingress Traffic Shifting: Route53 / Cloudflare Anycast healthcheck failover configured.",
            "[✓] Disaster Runbook: Documented procedure for manual region evacuation under 60 seconds."
        ]
    )
    b.add_invariant(
        title="GLOBAL RESILIENCE DOCTRINE",
        rule_body="A system is not truly distributed until it can withstand the complete loss of an entire cloud region without human intervention or data corruption."
    )

    out_file = os.path.join(ASSETS_DIR, "MultiRegion_Data_Topologies_CRDTs_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

def build_ebpf_observability_handbook():
    print("[*] Generating 4. Linux Kernel eBPF Observability Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="KERNEL OBSERVABILITY & JVM SRE",
        handbook_name="Linux_Kernel_eBPF_Observability_Handbook",
        theme_badge="KERNEL PERFORMANCE MANUAL"
    )

    # Cover
    b.add_cover(
        title="LINUX KERNEL eBPF\nOBSERVABILITY FIELD MANUAL",
        subtitle="Tracing TCP Socket Contention, Off-CPU Bottlenecks,\nand JVM Safepoint Freezes with Sub-1% Overhead",
        curriculum=[
            "The Profiler Observer Effect: Why jstack and ptrace Kill Latency",
            "eBPF Architecture: In-Kernel Verification, BPF Maps & Ring Buffers",
            "Diagnosing Socket Latency: Tracing tcp_v4_rcv & epoll_wait Contention",
            "Off-CPU Flame Graphs: Finding Where Threads Block on Mutexes and I/O",
            "JVM Safepoint Tracing: Uncovering STW Garbage Collection Pauses",
            "Senior Systems Architect Kernel Performance Runbook & Checklist"
        ]
    )

    # Page 2: Profiler Observer Effect
    b._start_new_page("Chapter 1: The Observer Effect of Userspace Profilers")
    b.add_card(
        tag="SRE INCIDENT ANALYSIS",
        title="Why userspace thread dumps (jstack/ptrace) crash production systems:",
        body_paragraphs=[
            "THE SYSTEM TRAP: Stop-the-World Safepoints.",
            "When a production service suffers a latency spike, engineers run 'jstack <pid>' or attach gdb/ptrace to capture thread states.",
            "• JVM thread dumps require bringing ALL active threads to a global safepoint.",
            "• Threads running long uncounted loops or awaiting network socket I/O cannot reach safepoints immediately.",
            "• The JVM halts all responding threads while waiting for the outliers, exacerbating a 200ms latency spike into a full 30-second customer timeout.",
            "THE EBPF REVOLUTION: Zero-Pause Kernel Tracing.",
            "eBPF runs sandboxed bytecode directly inside the Linux kernel on kprobes and tracepoints. It inspects kernel scheduler events and socket states with <0.5% CPU overhead without ever pausing userspace threads."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="OBSERVABILITY INVARIANT",
        rule_body="Never use diagnostic tools that alter the runtime behavior of the system they observe. If capturing diagnostics causes 504 timeouts, the telemetry harness has failed."
    )

    # Page 3: eBPF Internals
    b._start_new_page("Chapter 2: eBPF Verification & In-Kernel Maps")
    b.add_card(
        tag="KERNEL INTERNALS",
        title="How the eBPF Verifier guarantees 100% kernel safety:",
        body_paragraphs=[
            "1. The In-Kernel Verifier: Rejects any eBPF program with unbounded loops, uninitialized memory reads, or out-of-bounds pointer dereferences. It is mathematically impossible for an eBPF probe to crash the Linux kernel.",
            "2. JIT Compiler: Verified bytecode is compiled to native machine code for microsecond-level execution.",
            "3. BPF Ring Buffers: Lock-free per-CPU ring buffers stream telemetry data to userspace without acquiring mutex locks or allocating heap memory."
        ]
    )
    b.add_card(
        tag="KERNEL PROBE LOCATIONS",
        title="Critical Linux Kernel Tracepoints for SREs:",
        body_paragraphs=[
            "• sched:sched_switch: Tracks when threads yield CPU and why.",
            "• sock:inet_sock_set_state: Detects TCP socket state transitions (SYN, ESTABLISHED, CLOSE).",
            "• net:net_dev_queue: Measures network driver transmit queue backlog."
        ]
    )

    # Page 4: Socket Latency & TCP Contention
    b._start_new_page("Chapter 3: Tracing TCP Queue Latency & Socket Starvation")
    b.add_card(
        tag="NETWORK PERFORMANCE",
        title="Diagnosing hidden TCP latency behind high-traffic load balancers:",
        body_paragraphs=[
            "THE HIDDEN BOTTLENECK: TCP Listen Backlog Drops.",
            "If upstream NGINX or Envoy proxies receive a spike of incoming connections faster than the backend application worker can accept() them, connections sit queued in the TCP listen backlog.",
            "• To users, latency increases by 500ms.",
            "• In application APM (Datadog/NewRelic), transaction time looks fast because the timer doesn't start until accept() finishes.",
            "THE EBPF FIX: tcpconnect & tcplat probes.",
            "Attach eBPF probes to 'tcp_v4_connect' and 'tcp_finish_connect'. Measure the exact kernel socket handshake duration (RTT) and listen queue latency down to the microsecond."
        ]
    )
    b.add_invariant(
        title="KERNEL TELEMETRY INVARIANT",
        rule_body="Application APM sees only the code it executes. True latency begins the moment the first TCP SYN packet arrives at the network interface card."
    )

    # Page 5: Off-CPU Profiling & Safepoints
    b._start_new_page("Chapter 4: Off-CPU Flame Graphs & Safepoint Tracing")
    b.add_card(
        tag="PROFILING RUNBOOK",
        title="Finding why threads sleep instead of processing customer requests:",
        body_paragraphs=[
            "THE PARADOX: 20% CPU Utilization, yet p99 Latency = 4,000ms.",
            "Standard CPU profilers sample running threads. If a thread is blocked waiting on a mutex, disk I/O, or database connection, it is off-CPU and completely invisible to standard profilers.",
            "THE SRE MECHANISM: Off-CPU Tracing via eBPF.",
            "1. Record timestamp when thread leaves CPU on 'sched_switch'.",
            "2. Record timestamp when thread resumes CPU on next wake-up.",
            "3. Stack Delta: Aggregate stack traces by duration spent asleep.",
            "4. Result: Highlights the exact lock contention or socket read holding up worker threads."
        ]
    )
    b.add_card(
        tag="JVM GC LATENCY TRACING",
        title="Tracing Safepoint Pause Duration with USDT Probes:",
        body_paragraphs=[
            "• Attach eBPF to JVM USDT probes: hotspot:safepoint_begin and hotspot:safepoint_end.",
            "• Measures exact Stop-the-World pause duration without enabling verbose GC logging flags that degrade file I/O."
        ]
    )

    # Page 6: Checklist
    b._start_new_page("Chapter 5: Linux Kernel Observability Checklist")
    b.add_card(
        tag="SRE LAUNCH GATE",
        title="The Senior Systems Architect Kernel Telemetry Verification:",
        body_paragraphs=[
            "[✓] Kernel Version Compatible: Linux kernel >= 5.8 with BPF Type Format (BTF) enabled.",
            "[✓] Zero-Pause Telemetry: No production thread dumps executed via blocking jstack/ptrace.",
            "[✓] TCP Backlog Monitored: Alerts configured on 'ListenOverflows' and 'ListenDrops'.",
            "[✓] Off-CPU Profiling Configured: Automated off-CPU flame graphs generated during latency anomalies.",
            "[✓] JVM USDT Probes Enabled: '-XX:+ExtendedDTraceProbes' configured for zero-overhead safepoint tracing.",
            "[✓] Overhead Verified: Continuous eBPF daemon CPU consumption verified < 1.0% under peak load.",
            "[✓] Security Isolation: eBPF programs run with CAP_BPF / CAP_PERFMON; root execution disabled."
        ]
    )
    b.add_invariant(
        title="THE OBSERVABILITY DOCTRINE",
        rule_body="Observability is not about collecting billions of unstructured metrics; it is about having microsecond visibility into resource boundaries and queue contention."
    )

    out_file = os.path.join(ASSETS_DIR, "Linux_Kernel_eBPF_Observability_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

def build_edge_resumability_handbook():
    print("[*] Generating 5. Edge Platform Resumability & Sub-50ms LCP Handbook (6 Pages)...")
    b = HandwrittenHandbookBuilder(
        series_title="MODERN EDGE WEB & PERFORMANCE",
        handbook_name="Edge_Platform_Resumability_Handbook",
        theme_badge="EDGE RUNTIME ARCHITECTURE"
    )

    # Cover
    b.add_cover(
        title="EDGE PLATFORM RESUMABILITY\n& SUB-50ms LCP FIELD MANUAL",
        subtitle="Eliminating the JavaScript Hydration Tax Across Global CDNs\nwith Progressive Island Architectures and Resumable DOM Runtimes",
        curriculum=[
            "The Hydration Tax: Why Server-Side Rendering (SSR) Kills Total Blocking Time",
            "Resumability vs Re-Execution: How Resumable Runtimes Execute Zero Startup JS",
            "Progressive Island Architecture: Isolating Dynamic Micro-Modules",
            "HTTP/3 0-RTT & Early Hints: Pre-Warming Edge Caches in Sub-20ms",
            "Real User Monitoring (RUM): Reaching 100/100 Core Web Vitals at Scale",
            "Staff+ Systems Architect Modern Edge Platform Launch Gate"
        ]
    )

    # Page 2: Hydration Tax
    b._start_new_page("Chapter 1: The JavaScript Hydration Tax")
    b.add_card(
        tag="CORE WEB VITALS ROOT CAUSE",
        title="Why traditional React/Next.js SSR fails on low-end mobile devices:",
        body_paragraphs=[
            "THE PERFORMANCE TRAP: Double Execution.",
            "1. Server renders HTML string and sends it down the wire (Fast First Contentful Paint).",
            "2. The browser downloads 800KB of JavaScript bundles.",
            "3. The browser re-executes the entire component tree from top to bottom just to attach event listeners (Hydration).",
            "• During this 2.8-second window, the page LOOKS interactive, but clicking buttons does nothing (Uncanny Valley).",
            "• Mobile CPU core spikes to 100%, destroying Total Blocking Time (TBT) and Interaction to Next Paint (INP).",
            "THE ARCHITECTURAL FIX: Resumability.",
            "Resumable frameworks (Qwik, Vanilla Edge Blocks) serialize application state directly into HTML attributes. When a user clicks a button, the browser downloads only the 2KB click handler on-demand."
        ],
        is_warning=True
    )
    b.add_invariant(
        title="PERFORMANCE INVARIANT",
        rule_body="The fastest code is the code that never runs. Never download or execute JavaScript on page load for components that the user has not interacted with."
    )

    # Page 3: Resumability vs Re-Execution
    b._start_new_page("Chapter 2: Resumability Mechanics & Zero-JS Startup")
    b.add_card(
        tag="RUNTIME ARCHITECTURE",
        title="How Resumable Edge Runtimes eliminate startup parsing overhead:",
        body_paragraphs=[
            "1. HTML-Embedded State Serialization:",
            "Component state and closures are serialized directly into HTML DOM attributes (e.g. q:obj, q:key) during edge rendering.",
            "2. Global Delegated Event Listeners:",
            "Instead of attaching 500 event listeners to individual DOM elements, the runtime registers a single top-level event listener on the document root.",
            "3. Micro-Module Lazy Loading:",
            "When a user clicks: the global listener inspects the target DOM element, resolves the micro-chunk URL from the HTML attribute, and dynamically imports just that 1.2KB function.",
            "• Result: 0kB of JavaScript executed on page load. Immediate 100/100 Lighthouse score."
        ]
    )
    b.add_card(
        tag="METRIC PROFILE",
        title="Hydration vs Resumability Benchmarks:",
        body_paragraphs=[
            "• Traditional SSR + Hydration: JS Executed on Load = 1,420KB | TBT = 640ms | INP = 220ms.",
            "• Resumable Edge Architecture: JS Executed on Load = 0KB | TBT = 0ms | INP = 12ms."
        ]
    )

    # Page 4: Progressive Island Architecture
    b._start_new_page("Chapter 3: Progressive Island Architecture")
    b.add_card(
        tag="COMPONENT TOPOLOGY",
        title="Designing decentralized edge components with zero shared dependencies:",
        body_paragraphs=[
            "THE TOPOLOGY: Isolated Independent Islands.",
            "• The majority of a marketing, media, or e-commerce page is static content (Hero, Text, Product descriptions, Footers).",
            "• Dynamic functionality exists in isolated 'Islands' (Search autocomplete, Shopping cart, Interactive rating widget).",
            "THE SRE MECHANISM: Viewport Intersection Loading.",
            "• Islands below the fold are NOT loaded until they intersect with the user's viewport via IntersectionObserver:",
            "const observer = new IntersectionObserver((entries) => { entries.forEach(e => { if (e.isIntersecting) import('./island.js'); }); });",
            "• Critical Rendering Path remains 100% free of third-party script contention."
        ]
    )
    b.add_invariant(
        title="INGRESS INVARIANT",
        rule_body="Decouple component loading from global application bundles. If a marketing author adds a carousel component, it must not inflate the bundle size of the checkout flow."
    )

    # Page 5: HTTP/3 & Early Hints
    b._start_new_page("Chapter 4: HTTP/3 0-RTT & 103 Early Hints")
    b.add_card(
        tag="EDGE PROTOCOL ARCHITECTURE",
        title="Warming edge connections and browser caches in sub-20ms:",
        body_paragraphs=[
            "1. HTTP/3 QUIC 0-RTT Resumption:",
            "Eliminates TCP + TLS handshake round-trips for returning clients. The browser sends application data in the very first network packet.",
            "2. 103 Early Hints at the CDN Edge:",
            "While backend origin generates dynamic HTML (50ms), the edge CDN immediately emits HTTP status 103 with Link headers for critical LCP hero images and font files.",
            "• The browser begins fetching fonts and hero images 50ms before the HTML document finishes rendering.",
            "• LCP improves by 35% across high-latency mobile 4G networks."
        ]
    )
    b.add_card(
        tag="EDGE CACHING CONTRACT",
        title="Recommended Cache-Control Invariants for Edge Delivery:",
        body_paragraphs=[
            "• HTML Documents: Cache-Control: public, max-age=0, s-maxage=86400, stale-while-revalidate=60",
            "• Immutable Static Assets: Cache-Control: public, max-age=31536000, immutable"
        ]
    )

    # Page 6: Checklist
    b._start_new_page("Chapter 5: Edge Platform Reliability & Performance Checklist")
    b.add_card(
        tag="PRODUCTION READINESS",
        title="The Senior Systems Architect Pre-Launch Edge Platform Verification:",
        body_paragraphs=[
            "[✓] Zero-JS Critical Path: Initial viewport renders with 0kB blocking JavaScript.",
            "[✓] Sub-50ms LCP Monitored: Mobile p75 LCP under 800ms verified via Real User Monitoring.",
            "[✓] Progressive Island Loading: Below-the-fold modules gated by IntersectionObserver.",
            "[✓] 103 Early Hints Active: CDN emits Early Hints for hero assets and web fonts.",
            "[✓] HTTP/3 QUIC Enabled: UDP port 443 open with zero-RTT connection resumption.",
            "[✓] Cache Hit Ratio > 98%: Edge POP absorption shields origin database connection pools.",
            "[✓] Negative ADR Documented: Rationale for rejecting monolithic SPA frameworks recorded."
        ]
    )
    b.add_invariant(
        title="THE EDGE DOCTRINE",
        rule_body="The edge is not a CDN cache in front of a server; the edge is the application. Design for instant execution, zero hydration, and global resilience."
    )

    out_file = os.path.join(ASSETS_DIR, "Edge_Platform_Resumability_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

if __name__ == "__main__":
    f1 = build_interview_handbook()
    f2 = build_speculative_decoding_handbook()
    f3 = build_multiregion_crdt_handbook()
    f4 = build_ebpf_observability_handbook()
    f5 = build_edge_resumability_handbook()
    print("\n[+] Successfully compiled all 5 versatile, cutting-edge handbooks:")
    print(f"  1. {f1}")
    print(f"  2. {f2}")
    print(f"  3. {f3}")
    print(f"  4. {f4}")
    print(f"  5. {f5}")
