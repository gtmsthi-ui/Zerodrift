---
id: "post_07"
title: "Unit Tests Don't Work on Probabilistic Systems: The CI/CD Eval Pipeline That Does"
day: "Friday 8:30 AM"
pillar: "Practical AI & System Architecture"
hook_formula: "#2 Contrarian Thesis"
status: "queued"
score: 77.8
---

You can't test an LLM pipeline with assert output == expected.

Yet thousands of engineering teams I talk with still try to jam probabilistic models into traditional deterministic unit test suites.

The result? Either flaky tests that break every CI run, or watered-down assertions that let massive semantic hallucinations slip into production.

Here's the 3-tier eval architecture we use in our CI/CD pipelines to catch regressions before they hit customer traffic:

1. Golden Dataset Schema Gates
We maintain a version-controlled dataset of 300 real customer queries with strict ground-truth constraints.
Every PR validates that output conforms strictly to JSON schemas, latency stays within p95 SLA (sub-800ms), and token counts don't drift by more than 10%.
If token bloat spikes on a PR, our build automatically blocks the merge.

2. Out-of-Band Semantic Assertion Workers
We don't run slow evaluators synchronously inside the build pipeline.
Instead, our test workers spin up asynchronous containers that run semantic similarity embeddings against golden reference vectors.
It costs us $0.15 per CI build and finishes in under two minutes.

3. Shadow Traffic Canary Verification
Before any model upgrade or prompt refactor goes live to all users, it receives 5% of shadow production traffic.
Our observability layer compares semantic drift and user feedback in real time against the control cluster.
If drift exceeds 2.5%, the canary terminates instantly.

The real engineering results: we caught 14 silent prompt regressions before staging, reduced flaky build failures from 18% to zero, and kept model response determinism at 99.4%.

Probabilistic systems require statistical verification, not binary assertions.

I put together the complete CI/CD eval pipeline workflow in the visual summary below.

You can also read the breakdown in ZeroDrift Systems: https://gtmsthi-ui.github.io/Zerodrift/

How is your engineering team testing LLM prompt changes before merging PRs?

#DevOps #SoftwareEngineering #CloudArchitecture #SystemDesign
