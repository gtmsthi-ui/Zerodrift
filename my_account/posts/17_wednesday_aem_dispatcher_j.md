---
id: "post_17_wednesday_aem_dispatcher_j"
title: "Is Your AEM Dispatcher Leaking Repository Trees via Wildcard .json Selectors?"
day: "Wednesday 8:30 AM"
pillar: "Enterprise Web Security & JCR Hygiene"
hook_formula: "The Permissive Wildcard Exploit"
status: "scheduled"
score: "85.0"
scheduled_at: "2026-11-25T03:00:00.000Z"
solution_tool: "AEM Health Inspector (Rule DSP-03)"
live_demo_url: "https://gtmsthi-ui.github.io/Zerodrift/aem_systems_embed.html"
buffer_post_id: "6ae04f324c0869d0f8d78478"
---

A single '/0003 { /type "allow" /glob "*.json" }' in your Dispatcher filter section opens your entire JCR repository to data traversal.

Default Sling servlets provide rich JSON representations of any node (.1.json, .infinity.json, .tidy.json).
When teams leave permissive *.json rules open to support SPA frontends or search components, attackers use path traversal to dump /home/users, author metadata, and internal component dialog properties.

Enterprise architecture rule:
Deny *.json by default.
Expose ONLY vetted .model.json selectors for headless Core Components, and explicitly deny default Sling JSON servlets.

Here is how we architected the mitigation in our enterprise reliability toolkit:

1. Block all wildcard *.json globs in your /filter rules.

2. Explicitly allow only vetted .model.json selectors for headless and SPA consumers.

3. Use our live scanner to audit your Dispatcher filter rules against JCR traversal exploits.

---

💡 You can test this live in your browser right now on our zero-dependency engineering lab:
👉 Live Interactive Tool: https://gtmsthi-ui.github.io/Zerodrift/aem_systems_embed.html (Switch to AEM Health Inspector (Rule DSP-03))
👉 GitHub Repository: https://github.com/gtmsthi-ui/aem-reliability-toolkit

Have you encountered this invalidation or caching bottleneck on your sites? What /statfileslevel does your team use?

#AEM #AdobeExperienceManager #AEMCloudService #EnterpriseArchitecture #WebPerformance #SoftwareEngineering