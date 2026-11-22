import os
import re
import html

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "content.js"), "r", encoding="utf-8") as f:
    js = f.read()

# Minification:
# 1. Remove single-line comments that are alone on a line
lines = []
for line in js.splitlines():
    stripped = line.strip()
    if stripped.startswith("//") and not stripped.startswith("//#"):
        continue
    lines.append(line)

cleaned = "\n".join(lines)

# 2. Compress multi-line string templates and excessive whitespace
# To preserve backtick strings safely, replace double newlines with single spaces
compacted = re.sub(r'\n\s*', ' ', cleaned)

bookmarklet_code = f"javascript:(function(){{{compacted}}})();"

# Save pure raw bookmarklet text
with open(os.path.join(HERE, "bookmarklet.txt"), "w", encoding="utf-8") as f:
    f.write(bookmarklet_code)

escaped_code = html.escape(bookmarklet_code)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>LinkedIn Architect Studio (Auto-Reply & Newsletter Hub)</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      max-width: 820px;
      margin: 36px auto;
      line-height: 1.6;
      color: #1f2328;
      padding: 0 24px;
      background: #f6f8fa;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #d0d7de;
      border-radius: 12px;
      padding: 24px;
      margin-bottom: 24px;
      box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }}
    h2 {{ margin-top: 0; color: #0a66c2; }}
    .badge {{
      display: inline-block;
      padding: 14px 28px;
      background: linear-gradient(135deg, #0a66c2 0%, #004182 100%);
      color: #ffffff !important;
      font-weight: 600;
      text-decoration: none;
      border-radius: 28px;
      box-shadow: 0 4px 14px rgba(10,102,194,0.35);
      font-size: 15px;
      cursor: move;
    }}
    .badge:hover {{ transform: translateY(-1px); }}
    textarea {{
      width: 100%;
      height: 110px;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 11px;
      background: #0d1117;
      color: #58a6ff;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 12px;
      resize: vertical;
      box-sizing: border-box;
    }}
    .btn {{
      padding: 10px 18px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      border: none;
      font-size: 13px;
    }}
    .btn-primary {{ background: #238636; color: #ffffff; }}
    .btn-primary:hover {{ background: #2ea043; }}
    .step {{ border-left: 4px solid #0a66c2; padding-left: 14px; margin: 20px 0; }}
  </style>
</head>
<body>
  <div class="card">
    <h2>⚡ Architect Auto-Reply & Studio Hub (v6.6)</h2>
    <p>This studio runs directly inside your Chrome browser on LinkedIn to scan comments, generate high-signal senior architect replies, auto-inject into the comment box, and 1-click publish newsletter editions.</p>

    <div class="step">
      <b>Method 1: Direct Bookmarklet (Drag or Copy)</b>
      <p style="margin: 8px 0;">Make sure your Bookmarks Bar is visible in Chrome (<code>Ctrl + Shift + B</code>), then drag this button to your bar:</p>
      <div style="margin: 14px 0;">
        <a class="badge" href="{escaped_code}">⚡ Architect Auto-Reply</a>
      </div>
      <p style="font-size: 12px; color: #57606a;">Or click below to copy the code manually into a bookmark URL:</p>
      <button class="btn btn-primary" onclick="copyCode()">📋 Copy Bookmarklet Code</button>
      <span id="copy-msg" style="margin-left: 12px; font-weight: 600; color: #238636; display: none;">✅ Copied to clipboard!</span>
      <div style="margin-top: 10px;">
        <textarea id="raw-code" readonly>{escaped_code}</textarea>
      </div>
    </div>

    <div class="step">
      <b>Method 2 (100% Fail-Safe): Load as Permanent Chrome Extension</b>
      <p style="margin: 8px 0;">If LinkedIn's strict page security (CSP) blocks bookmark clicks on your browser, load it as an unpacked extension once:</p>
      <ol style="margin: 6px 0 0 18px; padding: 0;">
        <li>Open Chrome and navigate to: <code>chrome://extensions</code></li>
        <li>Enable <b>Developer mode</b> (toggle in top-right).</li>
        <li>Click <b>Load unpacked</b> (top-left).</li>
        <li>Select this folder: <code>d:\\Visual-studio-project\\linkedin-skill\\chrome-extension</code></li>
        <li>Open any LinkedIn post or comment page — the <b>⚡ Architect Studio</b> floating button will immediately appear at bottom right!</li>
      </ol>
    </div>
  </div>

  <script>
    function copyCode() {{
      const el = document.getElementById('raw-code');
      el.select();
      navigator.clipboard.writeText(el.value).then(() => {{
        const msg = document.getElementById('copy-msg');
        msg.style.display = 'inline';
        setTimeout(() => {{ msg.style.display = 'none'; }}, 3000);
      }});
    }}
  </script>
</body>
</html>
"""

with open(os.path.join(HERE, "bookmarklet.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Generated clean Direct-Execution Bookmarklet! Length: {len(bookmarklet_code)} chars.")
