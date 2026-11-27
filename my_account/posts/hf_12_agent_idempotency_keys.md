---
title: "A Tool Call Fails Halfway and Gets Retried: Preventing Duplicate Side Effects"
pillar: "Production AI & Harness Architecture"
status: "queued"
---

An autonomous agent executes a tool call to issue a $120 customer refund.

The payment gateway processes the refund, but before returning the HTTP 200 response to your agent harness, a network blip occurs. The connection drops.

The agent's retry logic fires. It retries the tool call. The customer receives two refunds ($240).

In non-deterministic agent workflows, un-safeguarded retries lead directly to financial loss and database corruption.

Here is the Senior Architect Idempotency Blueprint:

1️⃣ Cryptographic Idempotency Keys:
The agent harness (not the LLM) generates a deterministic idempotency key for every state mutation:
`Idempotency-Key: SHA256(session_id + agent_turn_index + tool_name + sorted_parameters)`

2️⃣ Atomic Redis State Machine:
Before executing any side-effect tool (Stripe refund, database UPDATE, email dispatch), the harness attempts an atomic `SET key "PENDING" NX EX 300` in Redis.
• If key already exists in 'PENDING': Hold request; do not re-execute.
• If key exists in 'COMPLETED': Immediately return the cached response without touching downstream APIs.

3️⃣ Two-Phase Commit for Financial Actions:
Never let an LLM call transactional APIs in a single fire-and-forget shot.
• Phase 1: Tool generates a typed `TransferProposal`.
• Phase 2: A deterministic verification rule verifies wallet limits, velocity caps, and executes the transfer with the idempotency key.

Treat generative models as untrusted parameter extractors. Never give them unchecked transactional execution authority.

How do you guarantee idempotency across your autonomous agent tool integrations?

#SystemDesign #FinOps #SoftwareEngineering #Architecture #Fintech #AutonomousAgents #SRE
