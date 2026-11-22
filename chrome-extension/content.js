// LinkedIn Architect Auto-Reply & Studio Hub (v6.6 Direct DOM Injection)
(() => {
  console.log("[Architect Studio] Initializing...");

  // If already open, toggle visibility
  const existingPanel = document.getElementById("li-architect-panel");
  if (existingPanel) {
    existingPanel.style.display = (existingPanel.style.display === "none") ? "flex" : "none";
    showToast(existingPanel.style.display === "flex" ? "⚡ Architect Studio Opened" : "Architect Studio Minimized");
    return;
  }

  // Helper: Visual Toast Notification (Confirms instantly on screen)
  function showToast(msg, bg = "#0a66c2") {
    let t = document.getElementById("li-architect-toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "li-architect-toast";
      document.body.appendChild(t);
    }
    t.style.cssText = `position:fixed; top:24px; right:24px; background:${bg}; color:#ffffff; padding:12px 22px; border-radius:8px; z-index:2147483647; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; font-size:13px; font-weight:600; box-shadow:0 6px 20px rgba(0,0,0,0.35); pointer-events:none; transition:opacity 0.3s ease;`;
    t.innerText = msg;
    t.style.opacity = "1";
    setTimeout(() => { if (t) t.style.opacity = "0"; }, 3000);
  }

  showToast("⚡ Architect Studio Launched!", "#238636");

  // 1. Floating trigger button (Positioned above LinkedIn messaging drawer)
  const triggerBtn = document.createElement("button");
  triggerBtn.id = "li-architect-btn";
  triggerBtn.innerHTML = `⚡ <span>Architect Studio</span>`;
  triggerBtn.style.cssText = `position:fixed; bottom:95px; right:24px; z-index:2147483647; background:linear-gradient(135deg, #0a66c2 0%, #004182 100%); color:#ffffff; border:1px solid rgba(255,255,255,0.3); padding:10px 18px; border-radius:28px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; font-size:13px; font-weight:600; box-shadow:0 6px 22px rgba(0,0,0,0.35); cursor:pointer; display:flex; align-items:center; gap:8px;`;
  document.body.appendChild(triggerBtn);

  // 2. Pre-configured newsletter editions (The Pragmatic Architect)
  const NEWSLETTER_EDITIONS = [
    { issue: 1, title: "The Model Race Is Over. The Enterprise Harness Race Just Began", subtitle: "A Senior Architect's Guide to Building Deterministic, SRE-Grade AI Workflows Without Token Bloat", lead: "In enterprise software, the foundation model was never the hard part. The real battle for AI reliability has officially moved from raw models to the Enterprise Execution Harness." },
    { issue: 2, title: "Zero-Downtime Database Architecture: The 3-Phase Expand/Contract Blueprint", subtitle: "Safe Schema Evolution on High-Throughput Production Datastores Without Table Locks", lead: "Running ALTER TABLE on a live table with 80M rows is playing Russian roulette with customer SLAs. This guide details the Expand/Contract Pattern for zero-downtime database evolution." },
    { issue: 3, title: "Production RAG Failures & Fallback State Machines", subtitle: "Why Vector Similarity Breaks in Enterprise Staging and How to Box Hallucinations", lead: "Vector embeddings alone do not solve enterprise retrieval. Architects decouple retrieval from generative synthesis using bounded state machines with strict JSON schema verification." },
    { issue: 4, title: "FinOps for Autonomous AI Pipelines: The 3 Financial Gates", subtitle: "Token Budgets, Tiered Model Ladders, and Gateway Throttling Before Your CFO Pages You", lead: "Routing routine data extraction to a 400B model is paying a 30x tax to disguise lazy systems architecture. Establish a Model Ladder to cut token expenditures by 78%." },
    { issue: 6, title: "Safe Semantic Caching in Production: The 500ms Invalidation Trap", subtitle: "Preventing Cross-Tenant Leaks and High-Recall Invalidation Failures in LLM Gateways", lead: "Naive semantic caching introduces silent data contamination across tenants. Safe semantic caching requires monotonic epoch tagging inside compound partition keys." },
    { issue: 11, title: "Multi-Agent State Orchestration: Preventing Deadlocks & Hallucinated Loops", subtitle: "Governing Autonomous Agents as Deterministic Finite State Machines Using the Actor Model", lead: "Connecting multiple agents in an open conversational loop burns thousands of API dollars in recursive hallucination. Reliable multi-agent platforms require typed state ledgers and bounded compute." },
    { issue: 12, title: "The Death of Monolithic Clientlibs: High-Performance Vanilla Block Architecture", subtitle: "Decentralized Component Loading for Sub-50ms LCP on Modern Edge Web Platforms", lead: "Bundling 1.8MB of JavaScript in legacy clientlib packages kills Core Web Vitals. Modern edge platforms load micro-modules dynamically via IntersectionObserver upon viewport intersection." },
    { issue: 13, title: "Zero-Overhead JVM Observability: Tracing Safepoint Latency with eBPF", subtitle: "Diagnosing GC Pauses and Socket Contention at the Linux Kernel Boundary Without Profiler Overhead", lead: "Userspace JVM thread dumps (jstack) freeze production workloads at safepoints. Tracing at the Linux kernel boundary with eBPF kprobes provides microsecond-level off-CPU visibility with sub-1% CPU impact." },
    { issue: 14, title: "Multi-Region Distributed Data Topologies: Eliminating Split-Brain Partition Risks", subtitle: "An Architectural Blueprint for Global Active-Active Replication and Conflict-Free CRDTs", lead: "Synchronous cross-continent consensus guarantees high latency. Designing resilient global systems requires clear consistency boundaries, monotonic epoch tagging, and CRDTs." },
    { issue: 15, title: "The Architecture Review Board Anti-Patterns: Moving to Automated Code Contracts", subtitle: "How Staff+ Architects Replace 80-Page Slides with Executable CI/CD Architectural Verification", lead: "Gatekeeping review boards provide the illusion of control while technical debt accumulates. High-velocity engineering teams encode architectural fitness functions directly into CI/CD pipelines." }
  ];

  // 3. Control HUD Panel (Inline styling for 100% guaranteed rendering)
  const panel = document.createElement("div");
  panel.id = "li-architect-panel";
  panel.style.cssText = `position:fixed; bottom:155px; right:24px; width:450px; max-width:calc(100vw - 48px); max-height:560px; background:#1b1f23; color:#e6edf3; border:1px solid #30363d; border-radius:12px; box-shadow:0 14px 40px rgba(0,0,0,0.5); z-index:2147483647; display:flex; flex-direction:column; overflow:hidden; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;`;

  panel.innerHTML = `
    <div style="padding:12px 16px; background:#161b22; border-bottom:1px solid #30363d; display:flex; justify-content:space-between; align-items:center;">
      <h3 style="margin:0; font-size:14px; font-weight:600; color:#f0f6fc; display:flex; align-items:center; gap:8px;">
        ⚡ Architect Studio (Replies & Newsletter)
      </h3>
      <button id="li-close-btn" style="background:none; border:none; color:#8b949e; font-size:20px; cursor:pointer; line-height:1; padding:2px 6px;">&times;</button>
    </div>
    <div style="padding:14px; overflow-y:auto; flex:1;">
      <div style="font-size:11px; color:#8b949e; margin-bottom:10px;">
        Senior Systems Architect Assistant: Automated Comment Triage, Live Window Replies & 1-Click Publishing.
      </div>
      <div style="display:flex; gap:8px; margin-bottom:12px;">
        <button id="li-tab-replies" style="flex:1; padding:8px 10px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; border:none; background:#238636; color:#ffffff;">💬 Auto-Reply HUD</button>
        <button id="li-tab-news" style="flex:1; padding:8px 10px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; border:1px solid #30363d; background:#21262d; color:#c9d1d9;">📰 Newsletter Hub</button>
      </div>

      <div id="li-replies-view">
        <div style="display:flex; gap:8px; margin-bottom:10px;">
          <button id="li-scan-btn" style="flex:1; padding:8px 10px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; border:none; background:#0a66c2; color:#ffffff;">🔍 Scan & Draft All Replies</button>
          <button id="li-sample-btn" style="flex:1; padding:8px 10px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; border:1px solid #30363d; background:#21262d; color:#c9d1d9;">🧪 Test / Sample Replies</button>
        </div>
      </div>

      <div id="li-news-view" style="display:none;"></div>

      <div id="li-log" style="background:#0d1117; border:1px solid #30363d; border-radius:8px; padding:12px; font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:11px; line-height:1.5; min-height:220px; max-height:300px; overflow-y:auto; white-space:pre-wrap; word-break:break-word;">
Ready.
• Click "🔍 Scan & Draft All Replies" on any post with comments.
• Click "🧪 Test / Sample Replies" to view immediate pre-generated replies in this window!
• Click "📰 Newsletter Hub" to access editions of The Pragmatic Architect.
      </div>
    </div>
  `;
  document.body.appendChild(panel);

  triggerBtn.addEventListener("click", () => {
    panel.style.display = (panel.style.display === "none") ? "flex" : "none";
  });
  document.getElementById("li-close-btn").addEventListener("click", () => {
    panel.style.display = "none";
  });

  const logBox = document.getElementById("li-log");
  const repliesView = document.getElementById("li-replies-view");
  const newsView = document.getElementById("li-news-view");
  const tabReplies = document.getElementById("li-tab-replies");
  const tabNews = document.getElementById("li-tab-news");

  function log(msg, color = "") {
    const el = document.createElement("div");
    el.style.marginBottom = "6px";
    if (color) el.style.color = color;
    el.innerText = msg;
    logBox.appendChild(el);
    logBox.scrollTop = logBox.scrollHeight;
  }

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  // --- TAB TOGGLE ---
  tabReplies.addEventListener("click", () => {
    repliesView.style.display = "block";
    newsView.style.display = "none";
    tabReplies.style.background = "#238636";
    tabReplies.style.color = "#ffffff";
    tabNews.style.background = "#21262d";
    tabNews.style.color = "#c9d1d9";
  });

  tabNews.addEventListener("click", () => {
    repliesView.style.display = "none";
    newsView.style.display = "block";
    tabNews.style.background = "#238636";
    tabNews.style.color = "#ffffff";
    tabReplies.style.background = "#21262d";
    tabReplies.style.color = "#c9d1d9";
    showNewsletterHub();
  });

  // --- ARCHITECTURAL TRIAGE & GENERATOR ---
  function triage(text) {
    const l = text.toLowerCase();
    if (/dm me|check out my|book a call|free consult|reach out to me|promo/i.test(l)) return "NOISE";
    if (/how do you|how did you|can you share|template|could you|how to|how can|pricing|guide|resource/i.test(l)) return "LEAD";
    if (/disagree|however,|trade-off|tradeoff|latency|bottleneck|overhead|have you considered|actually,|counterpoint|context engineering|harness/i.test(l)) return "SUBSTANCE";
    if (/we've|we have|in our team|at my company|from experience|i've seen|built|in production/i.test(l)) return "PEER";
    return "SUPPORT";
  }

  function generateReply(text, authorName, bucket) {
    const first = (authorName || "").split(" ")[0].trim();
    const sal = first ? `${first}, ` : "";
    const lower = text.toLowerCase();

    // 1. Topic: Context Engineering / Execution Harness
    if (/context engineering|harness|dial-up|left this behind|took it a step further|eval|prompt/i.test(lower)) {
      return (
        `${sal}spot on point. Context engineering was the first step, but treating LLMs like conversational chat endpoints ` +
        `rather than untrusted microservices is why so many staging environments collapse under production load.\n\n` +
        `Execution harnesses with strict schema gates, bounded execution budgets, and immutable audit traces are what make ` +
        `the system deterministic. Really appreciate the sharp insight.`
      );
    }

    // 2. Topic: Semantic Caching / Invalidation / In-flight queries
    if (/in-flight|invalidation|stress test|500ms|compound keys|leak|caching|cache/i.test(lower)) {
      return (
        `${sal}sharp question — in-flight query races during that 500ms window are where naive invalidation breaks down.\n\n` +
        `The fix we implemented is monotonic document epoch tagging inside the compound key (tenant + role + doc_version). ` +
        `When a doc update commits, Kafka pushes an atomic epoch bump to the gateway in <50ms. In-flight requests evaluating against the older epoch ` +
        `get fenced off at the gateway layer and fail-open directly to raw retrieval rather than serving stale cache hits.\n\n` +
        `You're spot on about flat thresholds being indefensible in multi-tenant systems. Appreciate the deep pushback.`
      );
    }

    // 3. Topic: AEM Dispatcher / Caching / Performance
    if (/dispatcher|statfileslevel|graceperiod|aem|clientlibs|core web vitals|lcp/i.test(lower)) {
      return (
        `${sal}exact problem teams encounter. Setting /statfileslevel to 0 wipes the entire docroot tree on every minor publication, ` +
        `causing cache thrashing and publisher starvation. Elevating to level 2 with a 2-second gracePeriod prevents publisher thundering herds. ` +
        `Appreciate the practical systems perspective.`
      );
    }

    // 4. Topic: LEAD / Templates
    if (bucket === "LEAD") {
      if (/template|share|send|guide/i.test(lower)) {
        return `${sal}happy to share the structure. The part that made the biggest difference for us was decoupling schema validation from the ingestion layer — payload errors dropped significantly. Send a connection request and I'll pass it across.`;
      }
      return `${sal}the short answer: start at the execution boundary, not the model. Define a strict input/output schema first, then wrap the LLM call in a retry harness with deterministic fallback. Most teams skip that and pay for it in production.`;
    }

    // 5. Topic: Technical Pushback / Substance
    if (bucket === "SUBSTANCE") {
      return `${sal}fair point — that holds true at lower scale. The calculus shifts under sustained enterprise load; at that point serialization overhead and variance become the dominant costs, not the logic layer. Appreciate the pushback.`;
    }

    // 6. Topic: Peer Experience
    if (bucket === "PEER") {
      return `${sal}that matches what we've seen across multiple migrations. Teams that move fastest have already internalized the infra cost before writing the first line of orchestration code. Good to know it's consistent across orgs.`;
    }

    const options = [
      `Thanks ${first || "Dan"} — glad it resonated with your experience.`,
      `Appreciate it, ${first || "friend"} — more architectural breakdowns coming on this.`,
      `Thanks ${first || ""}. Glad it landed well.`
    ];
    return options[Math.floor(Math.random() * options.length)];
  }

  // Multi-method text injector for ProseMirror
  async function injectTextIntoProseMirror(editor, text) {
    editor.focus();
    await sleep(150);

    // Technique 1: ClipboardEvent paste
    try {
      const dt = new DataTransfer();
      dt.setData("text/plain", text);
      editor.dispatchEvent(new ClipboardEvent("paste", { clipboardData: dt, bubbles: true, cancelable: true }));
    } catch (e) {}

    await sleep(150);

    // Technique 2: InputEvent with insertText & execCommand
    let curText = (editor.innerText || "").trim();
    if (!curText || curText.length < 5) {
      try {
        const sel = window.getSelection();
        const range = document.createRange();
        const p = editor.querySelector("p") || editor;
        range.selectNodeContents(p);
        sel.removeAllRanges();
        sel.addRange(range);

        editor.dispatchEvent(new InputEvent("beforeinput", { bubbles: true, cancelable: true, inputType: "insertText", data: text }));
        document.execCommand("insertText", false, text);
        editor.dispatchEvent(new InputEvent("input", { bubbles: true, inputType: "insertText", data: text }));
      } catch (e) {}
    }

    await sleep(150);

    // Technique 3: Direct Paragraph insertion fallback
    curText = (editor.innerText || "").trim();
    if (!curText || curText.length < 5) {
      try {
        let p = editor.querySelector("p");
        if (!p) {
          p = document.createElement("p");
          editor.appendChild(p);
        }
        p.textContent = text;
        editor.dispatchEvent(new Event("input", { bubbles: true }));
        editor.dispatchEvent(new Event("change", { bubbles: true }));
      } catch (e) {}
    }

    // Always copy to system clipboard
    try {
      await navigator.clipboard.writeText(text);
    } catch (e) {}
  }

  // --- RENDER REPLIES DIRECTLY IN THE HUD WINDOW ---
  function renderRepliesInWindow(items) {
    logBox.innerHTML = "";
    log(`⚡ ARCHITECT AUTO-REPLY DRAFTS (${items.length} FOUND)`, "#58a6ff");
    log(`Replies generated below with 1-click Copy & Live Auto-Inject:\n`, "#8b949e");

    items.forEach((item, idx) => {
      const card = document.createElement("div");
      card.style.cssText = "background:#161b22; border:1px solid #30363d; border-radius:8px; padding:12px; margin-bottom:14px;";

      card.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
          <span style="font-weight:600; color:#58a6ff; font-size:12px;">#${idx + 1} @${item.author}</span>
          <span style="background:#21262d; border:1px solid #30363d; border-radius:4px; padding:2px 6px; font-size:10px; color:#7ee787;">${item.bucket}</span>
        </div>
        <div style="font-size:11px; color:#8b949e; background:#0d1117; padding:8px; border-radius:4px; margin-bottom:8px; font-style:italic;">
          "${item.text.slice(0, 140)}${item.text.length > 140 ? "..." : ""}"
        </div>
        <div style="font-size:11px; font-weight:600; color:#c9d1d9; margin-bottom:4px;">Proposed Senior Architect Reply:</div>
        <textarea id="reply-box-${idx}" style="width:100%; height:85px; background:#0d1117; color:#e6edf3; border:1px solid #30363d; border-radius:6px; padding:8px; font-size:11px; font-family:sans-serif; resize:vertical; box-sizing:border-box;">${item.reply}</textarea>
        <div style="display:flex; gap:8px; margin-top:8px;">
          <button id="copy-btn-${idx}" style="flex:1; padding:6px 10px; border-radius:6px; font-size:11px; font-weight:600; cursor:pointer; border:1px solid #30363d; background:#21262d; color:#c9d1d9;">📋 Copy Reply</button>
          <button id="inject-btn-${idx}" style="flex:1; padding:6px 10px; border-radius:6px; font-size:11px; font-weight:600; cursor:pointer; border:none; background:#238636; color:#ffffff;">🚀 Auto-Inject & Post</button>
        </div>
        <div id="status-${idx}" style="font-size:11px; margin-top:4px; color:#8b949e;"></div>
      `;
      logBox.appendChild(card);

      setTimeout(() => {
        const copyBtn = document.getElementById(`copy-btn-${idx}`);
        const injectBtn = document.getElementById(`inject-btn-${idx}`);
        const replyTextarea = document.getElementById(`reply-box-${idx}`);
        const statusEl = document.getElementById(`status-${idx}`);

        if (copyBtn) {
          copyBtn.addEventListener("click", async () => {
            const val = replyTextarea.value;
            try {
              await navigator.clipboard.writeText(val);
              statusEl.innerText = "✅ Copied to clipboard! Press Ctrl+V in comment box.";
              statusEl.style.color = "#3fb950";
            } catch (e) {
              prompt("Copy this reply:", val);
            }
          });
        }

        if (injectBtn) {
          injectBtn.addEventListener("click", async () => {
            const val = replyTextarea.value;
            statusEl.innerText = "⏳ Opening editor and injecting text...";
            statusEl.style.color = "#58a6ff";

            try {
              if (item.replyBtn) {
                item.replyBtn.scrollIntoView({ behavior: "smooth", block: "center" });
                item.replyBtn.click();
                await sleep(800);
              }

              const editor = (item.cBox && item.cBox.querySelector("div[role='textbox'], [contenteditable='true'], .comments-comment-box__editor p, .editor-content p")) ||
                             document.querySelector(".comments-comment-box div[role='textbox'], [contenteditable='true']:focus, div[role='textbox']:focus") ||
                             Array.from(document.querySelectorAll("[contenteditable='true']")).pop();

              if (editor) {
                await injectTextIntoProseMirror(editor, val);
                statusEl.innerText = "✅ Injected! Unlocking Submit button...";

                const box = editor.closest(".comments-comment-box") || (item.cBox || document);
                const submitBtn = box.querySelector("button[type='submit'], button.comments-comment-box__submit-button") ||
                                  Array.from(box.querySelectorAll("button")).find(b => {
                                    const t = (b.innerText || "").trim().toLowerCase();
                                    return t === "reply" || t === "post";
                                  });

                if (submitBtn) {
                  submitBtn.removeAttribute("disabled");
                  submitBtn.classList.remove("artdeco-button--disabled");
                  await sleep(400);
                  submitBtn.click();
                  statusEl.innerText = "🎉 Successfully posted live reply!";
                  statusEl.style.color = "#3fb950";
                } else {
                  statusEl.innerText = "✅ Injected & copied to clipboard! Click Reply manually if needed.";
                  statusEl.style.color = "#7ee787";
                }
              } else {
                await navigator.clipboard.writeText(val);
                statusEl.innerText = "📋 Editor not in DOM; reply copied to clipboard. Press Ctrl+V!";
                statusEl.style.color = "#e3b341";
              }
            } catch (err) {
              statusEl.innerText = "[-] " + err.message;
              statusEl.style.color = "#f85149";
            }
          });
        }
      }, 50);
    });
  }

  // --- SAMPLE / TEST MODE ---
  document.getElementById("li-sample-btn").addEventListener("click", () => {
    const sampleComments = [
      {
        author: "Absar Ahmed",
        text: "Semantic caching sounds great in theory, but what about in-flight queries during that 500ms invalidation window? Doesn't that risk cross-tenant data leak?",
        bucket: "SUBSTANCE",
        reply: generateReply("Semantic caching in-flight queries 500ms invalidation window cross-tenant data leak", "Absar Ahmed", "SUBSTANCE")
      },
      {
        author: "Dan Malloy",
        text: "We left prompt engineering behind and went straight to context engineering. That was the dial-up era of AI.",
        bucket: "PEER",
        reply: generateReply("context engineering dial-up era of AI", "Dan Malloy", "PEER")
      },
      {
        author: "Sarah Jenkins",
        text: "Could you share the template for your zero-downtime database expand/contract migrations?",
        bucket: "LEAD",
        reply: generateReply("could you share the template for zero-downtime database expand/contract migrations?", "Sarah Jenkins", "LEAD")
      }
    ];

    renderRepliesInWindow(sampleComments);
  });

  // --- LIVE SCANNER ---
  document.getElementById("li-scan-btn").addEventListener("click", async () => {
    logBox.innerHTML = "";
    log("[⚡] Scanning active page for LinkedIn comments...", "#58a6ff");

    // 1. Expand collapsed replies
    const expandButtons = Array.from(document.querySelectorAll(
      "button[aria-label*='repl' i], button.comments-comment-item__load-more-comments-button, button[aria-label*='previous comments' i], button[aria-label*='more comments' i]"
    ));

    for (const eb of expandButtons) {
      try { eb.click(); await sleep(250); } catch (e) {}
    }

    // 2. Locate comment containers
    const commentItems = Array.from(document.querySelectorAll(
      "article.comments-comment-item, li.comments-comment-item, div.comments-comment-item, [data-view-name*='comment'], .comments-reply-item, article[class*='comment']"
    ));

    const parsed = [];
    const seen = new Set();

    for (const item of commentItems) {
      const authLink = item.querySelector("a[href*='/in/'], [class*='actor__name'], .comments-post-meta__name-text");
      const authorName = authLink ? authLink.innerText.split("\n")[0].trim() : "Colleague";

      if (/gautam|sethi/i.test(authorName)) continue;

      const textEl = item.querySelector("span[dir='ltr'], div[dir='ltr'], .comments-comment-item__main-content, .update-components-text, p");
      const text = textEl ? textEl.innerText.trim() : "";

      if (!text || text.length < 5) continue;
      const key = `${authorName}:${text.slice(0, 30)}`.toLowerCase();
      if (seen.has(key)) continue;
      seen.add(key);

      const bucket = triage(text);
      const reply = generateReply(text, authorName, bucket);

      const replyBtn = item.querySelector("button[aria-label*='Reply' i], button.comments-comment-social-bar__reply-action-button, button:has-text('Reply')") ||
                       Array.from(item.querySelectorAll("button")).find(b => {
                         const al = (b.getAttribute("aria-label") || b.innerText || "").toLowerCase();
                         return al.includes("reply") || al.includes("répondre");
                       });

      parsed.push({ cBox: item, replyBtn, author: authorName, text, bucket, reply });
    }

    if (parsed.length === 0) {
      const allProfileLinks = Array.from(document.querySelectorAll("a[href*='/in/']"));
      const otherAuthorLinks = allProfileLinks.filter(a => {
        const href = a.href.toLowerCase();
        const txt = (a.innerText || "").trim();
        return !href.includes("gautam-sethi") && txt.length > 2 && !txt.includes("Follow") && !txt.includes("3rd+") && !txt.includes("Connect");
      });

      for (const a of otherAuthorLinks) {
        const cBox = a.closest("article, li, div.artdeco-card, [class*='comment']") || a.parentElement.parentElement;
        const textEl = cBox.querySelector("span[dir='ltr'], div[dir='ltr'], p");
        const commentText = textEl ? textEl.innerText.trim() : "";
        if (!commentText || commentText.length < 8) continue;
        const authorName = a.innerText.split("\n")[0].trim();
        const key = `${authorName}:${commentText.slice(0, 30)}`.toLowerCase();
        if (seen.has(key)) continue;
        seen.add(key);

        const bucket = triage(commentText);
        const reply = generateReply(commentText, authorName, bucket);
        const replyBtn = cBox.querySelector("button[aria-label*='Reply' i], button");

        parsed.push({ cBox, replyBtn, author: authorName, text: commentText, bucket, reply });
      }
    }

    if (parsed.length > 0) {
      renderRepliesInWindow(parsed);
    } else {
      logBox.innerHTML = "";
      log(`[-] No comments detected in the currently visible viewport.`, "#f85149");
      log(`\nHow to fix:`, "#58a6ff");
      log(`1. Scroll down to a post on LinkedIn that has comments visible.`);
      log(`2. Click '🔍 Scan & Draft All Replies' again.`);
      log(`3. Or click '🧪 Test / Sample Replies' below to view instant pre-generated replies in this window!`, "#8b949e");

      const testBtn = document.createElement("button");
      testBtn.style.cssText = "margin-top:12px; padding:8px 12px; border-radius:6px; font-size:12px; font-weight:600; cursor:pointer; border:none; background:#238636; color:#ffffff;";
      testBtn.innerText = "🧪 Load Pre-Engineered Replies Now";
      testBtn.addEventListener("click", () => document.getElementById("li-sample-btn").click());
      logBox.appendChild(testBtn);
    }
  });

  // --- NEWSLETTER HUB LOGIC ---
  function showNewsletterHub() {
    newsView.innerHTML = `
      <div style="font-size:12px; color:#58a6ff; font-weight:600; margin-bottom:8px;">
        📰 The Pragmatic Architect — 1-Click Publishing Hub
      </div>
      <div style="font-size:11px; color:#8b949e; margin-bottom:12px;">
        Select any edition below to copy its complete publishing package and launch the LinkedIn Article Editor.
      </div>
    `;

    NEWSLETTER_EDITIONS.forEach((ed) => {
      const item = document.createElement("div");
      item.style.cssText = "margin-bottom:10px; padding:10px; background:#161b22; border:1px solid #30363d; border-radius:6px;";
      item.innerHTML = `
        <div style="font-weight:600; color:#58a6ff; font-size:12px;">Issue #${ed.issue}: ${ed.title}</div>
        <div style="color:#8b949e; font-size:11px; margin:3px 0;">${ed.subtitle}</div>
        <button id="copy-issue-${ed.issue}" style="margin-top:6px; padding:4px 10px; font-size:11px; font-weight:600; border-radius:4px; cursor:pointer; border:none; background:#238636; color:#ffffff;">
          📋 Copy Package & Open Editor
        </button>
      `;
      newsView.appendChild(item);

      setTimeout(() => {
        const btn = document.getElementById(`copy-issue-${ed.issue}`);
        if (btn) {
          btn.addEventListener("click", async () => {
            const launchPost = `The latest issue of The Pragmatic Architect is live.\n\nHeadline: ${ed.title}\n\nIn mission-critical enterprise systems, superficial patterns collapse the moment they face real customer SLA requirements.\n\nIn this deep-dive edition, I broke down the complete architectural blueprint:\n• The core failure modes teams overlook in staging\n• The step-by-step production-safe transition topology\n• Exact verification gates and observability traces before merging code\n\nRead the full article and subscribe here:\nhttps://www.linkedin.com/newsletters/the-pragmatic-architect-7515757942990737408/\n\n#SoftwareArchitecture #DistributedSystems #EngineeringLeadership #SystemsDesign #TechCareers`;

            const fullPackage = `HEADLINE:\n${ed.title}\n\nSUBTITLE:\n${ed.subtitle}\nBy Gautam Sethi · AI Enthusiast\n\nFEED LAUNCH POST:\n${launchPost}\n\n` + "=".repeat(60) + `\nARTICLE BODY:\n` + "=".repeat(60) + `\n\n# ${ed.title}\n\n*By Gautam Sethi · AI Enthusiast*\n\n---\n\n${ed.lead}`;

            try {
              await navigator.clipboard.writeText(fullPackage);
              alert(`✅ Issue #${ed.issue} Publishing Package copied to your clipboard!\n\nOpening the LinkedIn Article Editor now.`);
            } catch (e) {
              prompt("Copy this package:", fullPackage);
            }
            window.open("https://www.linkedin.com/article/edit/", "_blank");
          });
        }
      }, 50);
    });
  }
})();
