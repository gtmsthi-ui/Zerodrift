---
title: "Your Agent Calls the Same Tool 5 Times in a Row: The 3-Strike Circuit Breaker"
pillar: "Production AI & Harness Architecture"
status: "queued"
---

When an autonomous agent calls the same tool 5 times in a row without making forward progress, it is not thinking deeply. It is stuck in an infinite hallucination loop burning $50/hour in API tokens.

Why does this happen in production?

1️⃣ The Vague Error Payload Trap:
The tool encounters an error (e.g. database timeout or validation failure) and returns a generic string like `Error: 500` or `{}`. The model has no actionable feedback on what parameter failed, so it repeats the exact same tool call with identical parameters.

2️⃣ Phantom Parameter Hallucination:
The model invents a parameter that isn't in your schema (e.g. `user_id` instead of `account_id`). The execution harness rejects it, but unless the validation error is fed back to the model as an explicit system prompt correction, it keeps retrying.

3️⃣ Missing Completion Invariant:
The model accomplishes the task, but the system prompt lacks an explicit termination trigger (e.g. 'Emit FINISH when data is saved'). The model loops asking for more data.

The Senior Systems Architect SRE Mitigation:
• The 3-Strike Hystrix Breaker: If an agent calls the same tool with identical or failing parameters 3 times, trip the circuit breaker.
• Hard Iteration Ceiling: Enforce `max_tool_iterations = 4` at the gateway harness.
• Structured Feedback Frames: Never return raw HTTP errors to the model. Return a structured error JSON:
`{"status": "error", "failed_parameter": "date_range", "correction_hint": "Format must be YYYY-MM-DD"}`

How do you break recursive tool loops in your multi-agent platforms?

#AIEngineering #AutonomousAgents #SoftwareArchitecture #SystemDesign #LLMOps #Python #SRE
