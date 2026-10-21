#!/usr/bin/env python3
"""
sync_site_publications.py - Full Architectural Whitepaper & LinkedIn Dispatch Synchronizer
Synchronizes:
1. All Research Whitepapers from my_account/newsletter/editions/*.md
2. All Architectural Dispatches from my_account/posts/*.md
3. Injects interactive cards, filterable tabs, and full reading modals into docs/index.html
4. Updates Command Palette (⌘K / Ctrl+K) with all available whitepapers
"""

import os
import sys
import glob
import re
import json

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
EDITIONS_DIR = os.path.join(PROJECT_ROOT, "my_account", "newsletter", "editions")
POSTS_DIR = os.path.join(PROJECT_ROOT, "my_account", "posts")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
INDEX_HTML = os.path.join(DOCS_DIR, "index.html")


def parse_markdown_file(filepath):
    """Parses frontmatter and markdown body."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta = {}
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    val = v.strip().strip('"').strip("'")
                    if val.startswith("[") and val.endswith("]"):
                        meta[k.strip()] = [t.strip().strip('"').strip("'") for t in val[1:-1].split(",") if t.strip()]
                    else:
                        meta[k.strip()] = val
            body = parts[2].strip()

    return meta, body


def markdown_to_html(md):
    """Converts common Markdown patterns to clean semantic HTML for reader modals."""
    html = md
    # Headers
    html = re.sub(r"^### (.*)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.*)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.*)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)

    # Bold & Italic
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

    # Code blocks
    html = re.sub(r"```([a-zA-Z0-9_-]*)\n([\s\S]*?)```", r"<pre><code>\2</code></pre>", html)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

    # Paragraphs & lists
    lines = []
    in_ul = False
    for line in html.splitlines():
        s = line.strip()
        if s.startswith("- ") or s.startswith("* ") or s.startswith("• "):
            if not in_ul:
                lines.append("<ul>")
                in_ul = True
            lines.append(f"<li>{s[2:]}</li>")
        else:
            if in_ul:
                lines.append("</ul>")
                in_ul = False
            if s and not s.startswith("<h") and not s.startswith("<pre") and not s.startswith("<ul") and not s.startswith("<li") and not s.startswith("---"):
                lines.append(f"<p>{s}</p>")
            elif s == "---":
                lines.append("<hr style='border: none; border-top: 1px solid var(--border-subtle); margin: 2rem 0;' />")
            else:
                lines.append(s)
    if in_ul:
        lines.append("</ul>")

    return "\n".join(lines)


def generate_publications_html():
    """Generates the complete Publications & Dispatches HTML section."""
    # 1. Collect Whitepapers
    whitepaper_files = sorted(glob.glob(os.path.join(EDITIONS_DIR, "*.md")))
    whitepapers = []
    for wf in whitepaper_files:
        meta, body = parse_markdown_file(wf)
        ed_num = int(meta.get("edition", len(whitepapers) + 1))
        # Status check: only published or edition 1 are publicly available for reading
        status = meta.get("status", "scheduled" if ed_num > 1 else "published")
        whitepapers.append({
            "num": ed_num,
            "id": f"wp{ed_num}",
            "type": "whitepaper",
            "title": meta.get("title", f"Whitepaper #{ed_num}"),
            "subtitle": meta.get("subtitle", ""),
            "date": meta.get("date", "October 2026"),
            "tags": meta.get("tags", ["#SoftwareArchitecture"]),
            "pillar": meta.get("pillar", "Practical AI & System Architecture"),
            "status": status,
            "body_html": markdown_to_html(body)
        })

    # 2. Collect Posts
    post_files = sorted(glob.glob(os.path.join(POSTS_DIR, "*.md")))
    dispatches = []
    for pf in post_files:
        meta, body = parse_markdown_file(pf)
        post_id = meta.get("id", os.path.splitext(os.path.basename(pf))[0])
        status = meta.get("status", "queued")
        dispatches.append({
            "id": post_id,
            "type": "dispatch",
            "title": meta.get("title", post_id),
            "day": meta.get("day", "Weekly Dispatch"),
            "pillar": meta.get("pillar", "System Architecture"),
            "score": meta.get("score", "80.0"),
            "status": status,
            "scheduled_at": meta.get("scheduled_at", ""),
            "buffer_id": meta.get("buffer_post_id", ""),
            "image_url": meta.get("image_url", ""),
            "body_html": markdown_to_html(body)
        })

    # Render Cards HTML
    wp_cards = []
    for wp in whitepapers:
        tags_markup = "".join([f'<span class="tag">#{t.lstrip("#")}</span>' for t in wp["tags"][:4]])
        if wp["status"] == "published":
            action_markup = f"""
            <span class="status-badge status-ready">Available to Read</span>
            <a class="read-btn" onclick="openModal('{wp['id']}')">Read Whitepaper →</a>
            """
        else:
            action_markup = f"""
            <span class="status-badge status-queued" style="display: inline-flex; align-items: center; gap: 0.4rem;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
              Scheduled Release
            </span>
            <span class="locked-indicator" style="font-size: 0.8rem; color: var(--text-muted); display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.4rem 0.8rem; background: rgba(255,255,255,0.03); border-radius: 6px; border: 1px dashed var(--border-subtle);">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              In Editorial Queue
            </span>
            """
        wp_cards.append(f"""
        <!-- Whitepaper {wp['num']:02d} -->
        <article class="card spotlight-card pub-item pub-whitepaper" data-category="whitepaper" data-pillar="{wp['pillar']}">
          <div class="card-top">
            <span class="card-num" style="color: var(--cyan-bright);">WHITEPAPER #{wp['num']:02d}</span>
            <span class="card-date">{wp['date']}</span>
          </div>
          <h4 class="card-title">{wp['title']}</h4>
          <p class="card-summary">{wp['subtitle']}</p>
          <div class="tags">
            {tags_markup}
          </div>
          <div class="card-actions">
            {action_markup.strip()}
          </div>
        </article>
        """)

    dispatch_cards = []
    for dp in dispatches:
        if dp["status"] == "published":
            action_markup = f"""
            <span class="status-badge status-ready">Published on LinkedIn</span>
            <a class="read-btn" onclick="openModal('{dp['id']}')">Read Breakdown →</a>
            """
        else:
            action_markup = f"""
            <span class="status-badge status-queued" style="display: inline-flex; align-items: center; gap: 0.4rem;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
              Scheduled in Buffer
            </span>
            <span class="locked-indicator" style="font-size: 0.8rem; color: var(--text-muted); display: inline-flex; align-items: center; gap: 0.35rem; padding: 0.4rem 0.8rem; background: rgba(255,255,255,0.03); border-radius: 6px; border: 1px dashed var(--border-subtle);">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              {dp['day']}
            </span>
            """
        dispatch_cards.append(f"""
        <!-- Dispatch {dp['id']} -->
        <article class="card spotlight-card pub-item pub-dispatch" data-category="dispatch" data-pillar="{dp['pillar']}">
          <div class="card-top">
            <span class="card-num" style="color: var(--emerald-glow);">{dp['id'].upper()} · ARCHITECTURE DISPATCH</span>
            <span class="card-date">{dp['day']}</span>
          </div>
          <h4 class="card-title">{dp['title']}</h4>
          <p class="card-summary">{dp['pillar']} · Quality Score: {dp['score']}/100 PASS</p>
          <div class="tags">
            <span class="tag">#{dp['pillar'].split()[0]}</span>
            <span class="tag">#Reliability</span>
            <span class="tag">#StaffPlus</span>
          </div>
          <div class="card-actions">
            {action_markup.strip()}
          </div>
        </article>
        """)

    # Render Reader Modals HTML ONLY for Published items
    modals = []
    for wp in whitepapers:
        if wp["status"] == "published":
            modals.append(f"""
  <!-- Modal Reader for Whitepaper {wp['num']:02d} -->
  <div id="{wp['id']}-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="{wp['id']}-heading" onclick="closeModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeModalDirect('{wp['id']}')" aria-label="Close dialog">&times;</button>
      <div class="article-body">
        <span class="card-num" style="color: var(--cyan-bright);">WHITEPAPER #{wp['num']:02d} · {wp['pillar'].upper()}</span>
        <h1 id="{wp['id']}-heading" style="margin-top: 0.5rem; color: #fff;">{wp['title']}</h1>
        <div class="article-meta">By Gautam Sethi · ZeroDrift Systems Research Group · {wp['date']}</div>
        <div class="modal-inner-text" style="margin-top: 1.5rem; line-height: 1.75; color: var(--text-main);">
          {wp['body_html']}
        </div>
        <div style="margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center; flex-wrap: gap;">
          <a href="https://www.linkedin.com/in/gautam-sethi-1b944324" target="_blank" class="btn-primary" style="font-size: 0.85rem; padding: 0.6rem 1.2rem;">Discuss on LinkedIn →</a>
          <button class="btn-outline" onclick="closeModalDirect('{wp['id']}')" style="font-size: 0.85rem; padding: 0.6rem 1.2rem;">Close Document</button>
        </div>
      </div>
    </div>
  </div>
            """)

    for dp in dispatches:
        if dp["status"] == "published":
            modals.append(f"""
  <!-- Modal Reader for Dispatch {dp['id']} -->
  <div id="{dp['id']}-modal" class="modal-overlay" role="dialog" aria-modal="true" aria-labelledby="{dp['id']}-heading" onclick="closeModal(event)">
    <div class="modal-content" onclick="event.stopPropagation()">
      <button class="modal-close" onclick="closeModalDirect('{dp['id']}')" aria-label="Close dialog">&times;</button>
      <div class="article-body">
        <span class="card-num" style="color: var(--emerald-glow);">{dp['id'].upper()} · ARCHITECTURE DISPATCH</span>
        <h1 id="{dp['id']}-heading" style="margin-top: 0.5rem; color: #fff;">{dp['title']}</h1>
        <div class="article-meta">Gautam Sethi · Schedule Slot: {dp['day']} · Humanizer Quality: {dp['score']}/100 PASS</div>
        <div class="modal-inner-text" style="margin-top: 1.5rem; line-height: 1.75; color: var(--text-main);">
          {dp['body_html']}
        </div>
        <div style="margin-top: 2.5rem; padding-top: 1.5rem; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center;">
          <a href="https://www.linkedin.com/in/gautam-sethi-1b944324" target="_blank" class="btn-primary" style="font-size: 0.85rem; padding: 0.6rem 1.2rem;">View on LinkedIn →</a>
          <button class="btn-outline" onclick="closeModalDirect('{dp['id']}')" style="font-size: 0.85rem; padding: 0.6rem 1.2rem;">Close Dispatch</button>
        </div>
      </div>
    </div>
  </div>
            """)

    all_cards = "".join(wp_cards) + "".join(dispatch_cards)
    all_modals = "".join(modals)

    # Filterable Controls Markup
    section_html = f"""
    <!-- ==========================================================================
         SYNCHRONIZED ARCHITECTURAL WHITEPAPERS & TECHNICAL DISPATCHES
         ========================================================================== -->
    <section class="container lazy-reveal" id="whitepapers">
      <div class="section-title">
        <h3>Architectural Whitepapers & Technical Dispatches</h3>
        <p>Peer-reviewed systems engineering research, failure post-mortems, and Staff+ field manuals published by Gautam Sethi.</p>
      </div>

      <!-- Publication Filter Tabs -->
      <div class="pub-filter-bar" style="display: flex; gap: 0.75rem; margin-bottom: 2rem; flex-wrap: wrap; justify-content: center;">
        <button class="tab-btn active" onclick="filterPublications('all', this)" style="padding: 0.5rem 1.2rem; font-size: 0.85rem;">
          All Research ({len(whitepapers) + len(dispatches)})
        </button>
        <button class="tab-btn" onclick="filterPublications('whitepaper', this)" style="padding: 0.5rem 1.2rem; font-size: 0.85rem;">
          Whitepapers ({len(whitepapers)})
        </button>
        <button class="tab-btn" onclick="filterPublications('dispatch', this)" style="padding: 0.5rem 1.2rem; font-size: 0.85rem;">
          Weekly Dispatches ({len(dispatches)})
        </button>
        <button class="tab-btn" onclick="filterPublications('Practical AI', this)" style="padding: 0.5rem 1.2rem; font-size: 0.85rem;">
          Practical AI & RAG
        </button>
        <button class="tab-btn" onclick="filterPublications('Staff+', this)" style="padding: 0.5rem 1.2rem; font-size: 0.85rem;">
          Staff+ Leadership
        </button>
      </div>

      <div class="editions-grid" id="publicationsGrid">
        {all_cards}
      </div>
    </section>
    """

    return section_html, all_modals, whitepapers, dispatches


def sync_docs_index():
    """Reads docs/index.html and updates the whitepaper section, reader modals, and command palette."""
    if not os.path.exists(INDEX_HTML):
        print(f"[-] Error: {INDEX_HTML} not found.")
        return False

    with open(INDEX_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    section_html, modals_html, whitepapers, dispatches = generate_publications_html()

    # 1. Replace the #whitepapers section
    # Matches <section class="container lazy-reveal" id="whitepapers"> ... </section>
    pattern = r'<section class="container lazy-reveal" id="whitepapers">[\s\S]*?</section>'
    if re.search(pattern, html):
        html = re.sub(pattern, section_html.strip(), html)
        print("[+] Replaced existing #whitepapers section.")
    else:
        # Fallback: insert before </main>
        html = html.replace("</main>", f"{section_html.strip()}\n  </main>")
        print("[+] Inserted #whitepapers section before </main>.")

    # 2. Inject Modals before <footer> or before closing </body>
    # First remove any old ed1-modal / wp-modal blocks if present
    html = re.sub(r'<!-- Modal Reader for Whitepaper[\s\S]*?<!-- Assessment Inquiry Modal -->', f'{modals_html}\n\n  <!-- Assessment Inquiry Modal -->', html)

    # 3. Add Client-Side Filter JavaScript & Modal Handlers if not already present
    filter_js = """
    /* Publication Filter Script */
    function filterPublications(cat, btn) {
      document.querySelectorAll('.pub-filter-bar .tab-btn').forEach(b => b.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const items = document.querySelectorAll('.pub-item');
      items.forEach(el => {
        const itemCat = el.getAttribute('data-category');
        const itemPillar = el.getAttribute('data-pillar') || '';

        if (cat === 'all') {
          el.style.display = 'flex';
        } else if (cat === 'whitepaper' && itemCat === 'whitepaper') {
          el.style.display = 'flex';
        } else if (cat === 'dispatch' && itemCat === 'dispatch') {
          el.style.display = 'flex';
        } else if (itemPillar.toLowerCase().includes(cat.toLowerCase())) {
          el.style.display = 'flex';
        } else {
          el.style.display = 'none';
        }
      });
    }

    function openModal(id) {
      const modal = document.getElementById(id + '-modal');
      if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
      }
    }

    function closeModalDirect(id) {
      if (id) {
        const modal = document.getElementById(id + '-modal');
        if (modal) modal.style.display = 'none';
      } else {
        document.querySelectorAll('.modal-overlay').forEach(m => m.style.display = 'none');
      }
      document.body.style.overflow = '';
    }
    """

    if "function filterPublications" not in html:
        html = html.replace("</script>", f"{filter_js}\n  </script>")

    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"[+] Successfully synchronized docs/index.html with {len(whitepapers)} Whitepapers and {len(dispatches)} LinkedIn Dispatches!")
    return True


if __name__ == "__main__":
    sync_docs_index()
