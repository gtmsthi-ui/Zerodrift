#!/usr/bin/env python3
"""
generate_ai_interview_handbook.py - Generates the complete, multi-page,
authentic Blue Point Pen Handwritten Field Manual for:
"The AI Engineer Mock Interview Questions I'd Rehearse Before Any Interview"
100% boundary safe, zero text overlap, crisp handwritten layout.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
ASSETS_DIR = os.path.join(PROJECT_ROOT, "my_account", "assets")

sys.path.insert(0, HERE)
from pdf_architect_engine import HandwrittenHandbookBuilder

def build_interview_handbook():
    print("[*] Generating AI Engineer Mock Interview Field Manual (Blue Ballpoint Pen Style)...")
    b = HandwrittenHandbookBuilder(
        series_title="AI INTERVIEW FIELD MANUAL",
        handbook_name="AI_Engineer_Mock_Interview_Handbook",
        theme_badge="MOCK REHEARSAL PLAYBOOK"
    )

    # 1. Cover
    b.add_cover(
        title="THE AI ENGINEER\nMOCK INTERVIEW FIELD MANUAL",
        subtitle="The Exact Questions & Staff+ Architecture Blueprints I'd Rehearse\nBefore Walking Into Any Enterprise AI or Systems Design Loop",
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

    # 2. Page 2: Warm-Up
    b._start_new_page("Round 1: Warm-Up Rehearsal (2 Min Each)")
    b.add_qa_card(
        question="Q: Tell me about yourself and the AI work you've actually shipped.",
        answer_paragraphs=[
            "THE 90-SECOND ARCHITECT PITCH:",
            "• Hook & Scope: I lead platform architecture focusing on enterprise AI execution harnesses, production RAG pipelines, and deterministic agent governance.",
            "• Concrete System Shipped: Most recently, I architected a multi-tenant retrieval and inference gateway serving 4.5M monthly customer queries. We reduced p95 latency from 4.2s to 680ms while maintaining sub-10ms cache invalidation via Debezium CDC.",
            "• SRE Invariant: I treat foundation models as untrusted third-party dependencies with circuit breakers, token budgets, and rigid JSON schema validation at the system boundary."
        ],
        tag="WARM-UP • 2 MINS"
    )
    b.add_qa_card(
        question="Q: Explain RAG to a product manager who has never heard of it.",
        answer_paragraphs=[
            "THE ANALOGY CONTRACT:",
            "Imagine an open-book exam. A raw LLM is a brilliant student relying entirely on memory from books read two years ago. Sometimes they forget details or invent facts (hallucination).",
            "Retrieval-Augmented Generation (RAG) is giving that student an assistant who instantly pulls the exact 3 relevant company policy pages from the library right when a question is asked.",
            "VERDICT: The model doesn't guess our private quarterly numbers; it reads directly from the fresh documents we put in front of it."
        ],
        tag="EXECUTIVE COMMUNICATION"
    )

    # 3. Page 3: RAG vs Fine-Tuning & Hallucinations
    b._start_new_page("Round 1 (Cont.): Core Dilemmas & Hallucinations")
    b.add_qa_card(
        question="Q: Prompting vs RAG vs Fine-Tuning: When is each the WRONG choice?",
        answer_paragraphs=[
            "• Prompting is WRONG when: Knowledge exceeds 128k context, updates daily, or requires multi-million token batch costs.",
            "• RAG is WRONG when: You need the model to learn a specialized syntax (e.g. proprietary DSL, assembly, COBOL) or adopt a distinct tone/style rather than reference factual data.",
            "• Fine-Tuning is WRONG when: Your underlying data changes frequently (fine-tuning is frozen at training time) or when you need citations/attribution back to source paragraphs."
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

    # 4. Page 4: Fundamentals Under Pressure
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

    # 5. Page 5: Sampling & Reasoning Models
    b._start_new_page("Round 2 (Cont.): Sampling Parameters & Reasoning Models")
    b.add_qa_card(
        question="Q: What do Temperature, Top-K, and Top-P each change?",
        answer_paragraphs=[
            "• Temperature (T): Scales the raw logits before softmax. T=0 collapses distribution to argmax (deterministic). High T flattens probabilities (more creative/random).",
            "• Top-K: Hard truncate vocabulary to the K highest-probability tokens. Ignores the long-tail tail of low-probability words entirely.",
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

    # 6. Page 6: RAG Deep Dive
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

    # 7. Page 7: Chunking & Hybrid Search
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

    # 8. Page 8: Autonomous Agents & Idempotency
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

    # 9. Page 9: Multi-Agent Topologies & Long Memory
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

    # 10. Page 10: Evaluation & Production Drift
    b._start_new_page("Round 5: Evals, Safety & Production Drift")
    b.add_qa_card(
        question="Q: LLM judge and human users disagree. Whose signal do you trust?",
        answer_paragraphs=[
            "VERDICT: Trust Human User Outcomes Every Time.",
            "LLM judges suffer from position bias, verbosity bias (favoring longer answers), and self-preference bias (ranking their own model family higher).",
            "THE SRE SIGNAL: Measure implicit user feedback: thumb-downs, copy-to-clipboard rates, session abandoned queries, and ticket escalations.",
            "Use disagreement samples to calibrate your LLM judge prompts and few-shot rubric."
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

    # 11. Page 11: System Design Whiteboard
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

    # 12. Page 12: Rehearsal Protocol
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
        title="💡 THE CORE DOCTRINE: PRODUCTION SRE BEATS BUZZWORDS",
        rule_body="Interviews are not won by quoting papers. They are won by architects who describe failure modes, state boundaries, latency percentiles, and exact mitigation runbooks."
    )

    out_file = os.path.join(ASSETS_DIR, "AI_Engineer_Mock_Interview_Handwritten_Handbook.pdf")
    b.save_pdf(out_file)
    return out_file

if __name__ == "__main__":
    out = build_interview_handbook()
    print(f"\n[+] Successfully generated AI Engineer Mock Interview Handbook:\n    {out}")
