---
title: "From Prompt to First Token: The GPU & Gateway Lifecycle"
pillar: "Production AI & Harness Architecture"
slot: "2026-12-03T03:00:00.000Z"
status: "scheduled"
buffer_post_id: "6b096fa2e94385a8fd9f2ed1"
---

In Staff+ engineering interviews, asking 'What happens from the moment a user clicks Submit to the moment the first token arrives?' separates engineers who wrap APIs from architects who understand physical systems.

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

#GPU #LLMOps #MachineLearning #SystemDesign #SoftwareEngineering #CloudArchitecture #DeepLearning #SRE
