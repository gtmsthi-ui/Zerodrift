---
title: "System Design: Document Q&A with Strict Multi-Tenant Data Permissions"
pillar: "Production AI & Harness Architecture"
status: "queued"
---

Designing an enterprise document Q&A assistant is 20% vector search and 80% security authorization plumbing.

If an engineering manager asks: 'What were the performance ratings for my department?', vector similarity will happily match confidential HR compensation spreadsheets across the global company corpus if you don't enforce security boundaries.

Here is the Senior Architect Whiteboard Blueprint for Zero-Leak Document Q&A:

1️⃣ Metadata Tagging at Ingestion:
Every document chunk inherits cryptographic access control metadata:
`ACL: { organization_id: "org_44", department: "eng", security_clearance: "level_2", allowed_groups: ["eng_managers"] }`

2️⃣ Pre-Query Filter Enforcement (Non-Negotiable):
Never search an open vector index and filter results afterward.
The query vector MUST be executed with strict metadata predicates:
`WHERE organization_id = ? AND allowed_groups IN (?)`
If a user does not have clearance for executive compensation, those vectors do not mathematically exist in the search space.

3️⃣ Independent Auth Verification Gateway:
Before retrieved chunks are injected into the LLM prompt, an out-of-band authorization service verifies the user's current JWT session against the primary identity provider (Okta/Entra ID) to ensure permissions were not revoked 5 minutes ago.

4️⃣ Cryptographic Response Audit Ledger:
Every generated answer logs:
`{ user_id: "u_102", doc_chunk_ids_accessed: ["chk_991", "chk_992"], SHA256(retrieved_context) }`
Directly streamed to immutable SIEM storage for SOC2/HIPAA compliance.

In enterprise software, search accuracy is worthless without rigorous identity governance.

How do you enforce role-based access control (RBAC) across your vector databases?

#SystemDesign #CyberSecurity #DataPrivacy #RAG #EnterpriseArchitecture #CloudSecurity #SRE
