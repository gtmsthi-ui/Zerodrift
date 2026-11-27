---
title: "Prompting vs RAG vs Fine-Tuning: When is Each the Wrong Choice?"
pillar: "Production AI & Harness Architecture"
slot: "2026-12-01T03:00:00.000Z"
status: "scheduled"
buffer_post_id: "6b096a08e94385a8fd9cfb61"
---

Most engineering teams can explain what Prompting, RAG, and Fine-Tuning do. Very few can articulate when each is the WRONG choice.

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

#AIEngineering #MachineLearning #SystemDesign #SoftwareArchitecture #RAG #LLMOps #CloudArchitecture #SRE
