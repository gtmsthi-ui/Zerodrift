---
id: "post_09b"
title: "Why Naive AEM Dispatcher Invalidation Kills TTFB: The 3-Layer Cache Hierarchy"
day: "Wednesday 8:30 AM"
pillar: "AEM & Enterprise Web Architecture"
hook_formula: "#1 Contrarian Thesis"
status: "published"
score: "77.6"
scheduled_at: "2026-10-28T03:00:00.000Z"
buffer_post_id: "6adefb4ce4fd2be3e658cc18"
image_url: "https://raw.githubusercontent.com/gtmsthi-ui/Zerodrift/main/my_account/assets/post_09b_card.png"
published_at: "2026-10-28T03:00:00.000Z"
---

Flushing an entire AEM Dispatcher cache every time someone hits publish is the fastest way I know to kill a website.

We learned this the hard way five years back on an enterprise commerce rollout.
Every weekday at 2:00 PM sharp, our Time to First Byte jumped from 45ms to 3.8 seconds.
Brutal.
Our infra leads blamed sudden visitor spikes, while our marketing team blamed our large hero images.
They were all looking in the wrong place.

The real culprit?
Someone left statfileslevel set to 0.
When an editor updated one bio on /content/corporate/about-us, our replication agent touched the root .stat file.
In less than a second, our Dispatcher invalidated cached HTML across 14 language sites and 45,000 URLs.
Forty-five thousand live user requests bypassed Apache and hit our 4 publish JVMs at once.
CPU pinned at 98%.
Dead.
The whole cluster choked.

If you run enterprise AEM at scale, you can't treat cache invalidation like a sledgehammer. You've got to protect your publish tier.

Here's how we fixed our caching architecture to lock in a 96% hit ratio:

1. Tune statfileslevel to match your tree
Don't leave statfileslevel at 0 or 1.
If your repository path is /content/brand/country/language, set statfileslevel to 4.
When we publish /content/brand/us/en/news/article-1, only files in that exact en folder invalidate, while our UK, German, and Japanese pages stay warm. Simple.

2. Put stale-while-revalidate at the CDN edge
You shouldn't let incoming visitors wait on an origin re-render.
We set up Fastly with stale-while-revalidate=86400.
When our cache clears, the CDN serves the existing page to visitors while one single background thread fetches fresh HTML from AEM.
Nobody feels the rebuild lag.

3. Strip campaign tags before cache lookup
Marketers attach tracking parameters like ?utm_source or ?gclid to everything.
Default Dispatcher rules see those query strings and treat them as unique uncached pages.
We rewrote our Dispatcher filters to discard marketing params before checking cache on disk.

What that gave us:
- Cache hit ratio rose from 61% to 96.8%
- We cut peak publish cluster CPU down to 18%
- Global p95 TTFB stayed under 65ms during our largest Black Friday launch

Good web architecture isn't about paying for bigger cloud servers. It's about making sure your origin barely knows visitors exist.

I've sketched out our exact Dispatcher invalidation hierarchy in the visual below.

Read our complete web architecture guide at The Pragmatic Architect: https://gtmsthi-ui.github.io/Zerodrift/

What's the nastiest cache invalidation bug you've had to solve in AEM?

#AdobeExperienceManager #WebPerformance