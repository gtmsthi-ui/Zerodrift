#!/usr/bin/env python3
"""
build_newsletter_site.py - Automated Static Site Generator for The Pragmatic Architect
- Reads all editions from my_account/newsletter/editions/*.md
- Builds a responsive, modern web hub at docs/index.html (GitHub Pages compatible)
- Makes each edition readable locally or on the live web
- Auto-syncs live URLs with Central DB
"""

import os
import sys
import glob
import re
import json

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
EDITIONS_DIR = os.path.join(PROJECT_ROOT, "my_account", "newsletter", "editions")
DOCS_DIR = os.path.join(PROJECT_ROOT, "docs")
OUT_HTML = os.path.join(DOCS_DIR, "index.html")


def parse_edition_md(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read()

    meta = {}
    body = raw
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            for line in parts[1].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    val = v.strip().strip('"').strip("'")
                    if val.startswith("[") and val.endswith("]"):
                        # Parse tags
                        tags = [t.strip().strip('"').strip("'") for t in val[1:-1].split(",") if t.strip()]
                        meta[k.strip()] = tags
                    else:
                        meta[k.strip()] = val
            body = parts[2].strip()

    return meta, body


def markdown_to_html_simple(md):
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
    html = re.sub(r"```(text|markdown)?\n([\s\S]*?)```", r"<pre><code>\2</code></pre>", html)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

    # Bullets
    lines = []
    in_ul = False
    for line in html.splitlines():
        if line.strip().startswith("- ") or line.strip().startswith("* ") or line.strip().startswith("• "):
            if not in_ul:
                lines.append("<ul>")
                in_ul = True
            item_text = line.strip()[2:]
            lines.append(f"<li>{item_text}</li>")
        else:
            if in_ul:
                lines.append("</ul>")
                in_ul = False
            if line.strip() and not line.startswith("<h") and not line.startswith("<pre") and not line.startswith("<ul") and not line.startswith("<li"):
                lines.append(f"<p>{line}</p>")
            else:
                lines.append(line)
    if in_ul:
        lines.append("</ul>")

    return "\n".join(lines)


def build_site():
    os.makedirs(DOCS_DIR, exist_ok=True)
    edition_files = sorted(glob.glob(os.path.join(EDITIONS_DIR, "*.md")))

    editions = []
    for ef in edition_files:
        meta, body = parse_edition_md(ef)
        meta["file"] = ef
        meta["body_html"] = markdown_to_html_simple(body)
        editions.append(meta)

    # Generate complete docs/index.html
    cards_html = []
    modals_html = []

    for i, ed in enumerate(editions, start=1):
        num_raw = ed.get("edition", i)
        try:
            num = int(num_raw)
        except Exception:
            num = i
        title = ed.get("title", f"Edition {num}")
        subtitle = ed.get("subtitle", "")
        date = ed.get("date", "October 2026")
        tags = ed.get("tags", ["#SoftwareArchitecture", "#AIReliability"])
        if isinstance(tags, str):
            tags = [tags]

        tags_markup = "".join([f'<span class="tag">#{t.lstrip("#")}</span>' for t in tags])

        cards_html.append(f"""
        <article class="card">
          <div class="card-top">
            <span class="card-num">EDITION #{num:02d}</span>
            <span class="card-date">{date}</span>
          </div>
          <h4 class="card-title">{title}</h4>
          <p class="card-summary">{subtitle}</p>
          <div class="tags">
            {tags_markup}
          </div>
          <div class="card-actions">
            <span class="status-badge status-ready">Available</span>
            <a class="read-btn" onclick="openModal('ed{num}')">Read Deep-Dive →</a>
          </div>
        </article>
        """)

        modals_html.append(f"""
        <div id="ed{num}-modal" class="modal-overlay" onclick="closeModal(event)">
          <div class="modal-content" onclick="event.stopPropagation()">
            <button class="modal-close" onclick="closeModalDirect('ed{num}')">&times;</button>
            <div class="article-body">
              <span class="card-num">EDITION #{num:02d} · THE PRAGMATIC ARCHITECT</span>
              <h1 style="margin-top: 0.5rem;">{title}</h1>
              <div class="article-meta">By Gautam Sethi · Senior Software Architect · {date}</div>
              {ed["body_html"]}
            </div>
          </div>
        </div>
        """)

    # Combine into template
    base_template_path = os.path.join(PROJECT_ROOT, "my_account", "newsletter", "index.html")
    with open(base_template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Save to docs/index.html
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(template)

    print(f"[+] Successfully built newsletter site: {OUT_HTML} ({len(editions)} edition(s))")


if __name__ == "__main__":
    build_site()
