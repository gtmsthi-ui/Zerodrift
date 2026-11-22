import os
import re
import json
import base64
import html

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "content.js"), "r", encoding="utf-8") as f:
    js = f.read()

with open(os.path.join(HERE, "overlay.css"), "r", encoding="utf-8") as f:
    css = f.read()

# Build full client payload with CSS injection
css_json = json.dumps(css)
full_script = f"""
if (!document.getElementById("li-architect-css")) {{
  const style = document.createElement("style");
  style.id = "li-architect-css";
  style.textContent = {css_json};
  document.head.appendChild(style);
}}
{js}
"""

# Base64 encode the UTF-8 payload to prevent ANY HTML-stripping, quote breaks, or newline truncation
b64_payload = base64.b64encode(full_script.encode("utf-8")).decode("ascii")

bookmarklet_code = f'javascript:(function(){{try{{const c=decodeURIComponent(escape(atob("{b64_payload}")));const s=document.createElement("script");s.textContent=c;document.body.appendChild(s);s.remove();}}catch(e){{console.error(e);alert("Architect Studio Error: "+e.message);}}}})();'

# Save clean plain text version
with open(os.path.join(HERE, "bookmarklet.txt"), "w", encoding="utf-8") as f:
    f.write(bookmarklet_code)

# Build HTML with a readonly textarea to guarantee that copy/paste NEVER strips HTML tags
escaped_code = html.escape(bookmarklet_code)

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>LinkedIn Architect Studio (Auto-Reply & Newsletter)</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      max-width: 800px;
      margin: 40px auto;
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
      box-shadow: 0 3px 12px rgba(0,0,0,0.04);
    }}
    h2 {{ margin-top: 0; color: #0a66c2; display: flex; align-items: center; gap: 8px; }}
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
    .badge:hover {{ transform: translateY(-1px); box-shadow: 0 6px 18px rgba(10,102,194,0.45); }}
    textarea {{
      width: 100%;
      height: 100px;
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
    .step {{ border-left: 4px solid #0a66c2; padding-left: 14px; margin: 16px 0; }}
  </style>
</head>
<body>
  <div class="card">
    <h2>⚡ Architect Auto-Reply & Studio Hub (v6.5)</h2>
    <p>Use this directly on LinkedIn to scan comments, draft high-signal architectural replies, auto-inject into the comment box, or 1-click publish newsletter editions.</p>

    <div class="step">
      <b>Method 1 (Recommended): 1-Click Drag to Bookmarks Bar</b>
      <p style="margin: 8px 0;">Make sure your Chrome Bookmarks Bar is visible (<code>Ctrl + Shift + B</code>), then drag this button directly to your bar:</p>
      <div style="margin: 16px 0;">
        <a class="badge" href="{escaped_code}">⚡ Architect Auto-Reply</a>
      </div>
    </div>

    <div class="step">
      <b>Method 2: Manual Copy & Paste into Bookmark URL</b>
      <p style="margin: 8px 0;">If dragging doesn't work, click the button below to copy the code, right-click your bookmarks bar &rarr; <i>Add Page</i> &rarr; Name: <code>Architect Auto-Reply</code> &rarr; Paste into <i>URL</i>.</p>
      <button class="btn btn-primary" onclick="copyCode()">📋 Copy Bookmarklet Code</button>
      <span id="copy-msg" style="margin-left: 12px; font-weight: 600; color: #238636; display: none;">✅ Copied to clipboard!</span>
      <div style="margin-top: 12px;">
        <textarea id="raw-code" readonly>{escaped_code}</textarea>
      </div>
    </div>

    <div class="step">
      <b>Method 3 (Permanent): Load as Chrome Extension</b>
      <p style="margin: 8px 0;">To have the button automatically appear on every LinkedIn page without clicking a bookmark:</p>
      <ol style="margin: 6px 0 0 18px; padding: 0;">
        <li>Open Chrome and navigate to: <code>chrome://extensions</code></li>
        <li>Enable <b>Developer mode</b> (toggle in top right).</li>
        <li>Click <b>Load unpacked</b> and select the folder: <code>d:\\Visual-studio-project\\linkedin-skill\\chrome-extension</code></li>
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

print(f"Successfully generated clean Base64 Bookmarklet! Length: {len(bookmarklet_code)} chars.")
