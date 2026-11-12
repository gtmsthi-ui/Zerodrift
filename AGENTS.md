# Architectural Governance & Content Supply Chain Rules

## 1. Strict Deduplication & Anti-Overlap Policy
- **Never Re-Suggest or Overwrite Published Work:** Before generating, drafting, or proposing any LinkedIn post or newsletter edition, the agent must check:
  1. Frontmatter flag (`status: "published"`)
  2. The central SQLite database (`my_account/linkedin_tracker.db` in `newsletter_editions` and `posts` tables)
  3. SHA-256 content and title hash matches.
- If an edition is already published, it must be locked with a hard block (`🔴 [ALREADY PUBLISHED]`).

## 2. Portfolio Pillar Diversity (No Topic Monopolies)
All content must cycle deterministically through the 4 core pillars to ensure a balanced engineering portfolio:
1. **Edge & Distributed Web Platforms:** AEM Edge Delivery Services (EDS), sub-100ms LCP, vanilla block rendering, zero-downtime cache invalidation (`/statfileslevel 2+`, `/gracePeriod 2`).
2. **Production AI & Harness Architecture:** Model Context Protocol (MCP) servers, out-of-process sandboxing, safe multi-tenant semantic caching, CDC-driven Redis invalidation, prompt injection defenses.
3. **Kernel-Level Observability & Performance:** eBPF kprobes, Linux TCP socket queue latency (`epoll_wait`), zero-overhead JVM GC pause tracing.
4. **Cloud FinOps & Distributed Data:** Multi-region cache shielding, eliminating cross-AZ data transfer taxes, 3-Phase Expand/Contract database migrations.

## 3. Writing Style & Tone (The Pragmatic Architect)
- **Zero Buzzwords:** Never use empty filler words ("delve", "leverage", "game-changer", "tapestry", "seamless", "revolutionize").
- **Concrete Systems Rigor:** Always cite specific file configurations, HTTP status codes, latency percentiles (p99), and exact failure modes.
- **SRE & Production Invariants:** Treat the model and external services as untrusted dependencies with circuit breakers, timeouts, and negative ADR evaluations.

## 4. Live Studio Integrity (aem_systems_embed.html)
- **Interactive Tools Must Be Live:** All tools (AEM Inspector, Grounded RAG, Content Pipeline) must execute real runtime logic.
- **AST Scanner Standard:** The AEM Inspector must scan on live keystrokes across all 12 SRE rules from `aem-reliability-toolkit`.
- **Refusal Protocol:** The Grounded RAG engine must refuse consumer and non-technical queries (food, lifestyle) with an explicit refusal directive.
- **RAG Grounding:** Every technical answer must cite primary file paths and line numbers from the 67-document knowledge corpus.
