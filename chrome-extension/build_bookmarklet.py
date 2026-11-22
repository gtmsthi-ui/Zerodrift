import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "content.js"), "r", encoding="utf-8") as f:
    js = f.read()

with open(os.path.join(HERE, "overlay.css"), "r", encoding="utf-8") as f:
    css = f.read().replace("\n", " ").replace('"', '\\"')

inject_css = f'''
if (!document.getElementById("li-architect-css")) {{
  const style = document.createElement("style");
  style.id = "li-architect-css";
  style.textContent = "{css}";
  document.head.appendChild(style);
}}
'''

full_code = inject_css + "\n" + js
# Remove single-line comments that might break when minified
cleaned_js = re.sub(r'//.*?\n', '\n', full_code)
bookmarklet = "javascript:(function(){" + cleaned_js.replace("\n", " ") + "})();"

with open(os.path.join(HERE, "bookmarklet.txt"), "w", encoding="utf-8") as f:
    f.write(bookmarklet)

# Also update bookmarklet.html to embed the exact raw code into the button link!
html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>LinkedIn Architect Auto-Reply Bookmarklet</title>
  <style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 750px; margin: 40px auto; line-height: 1.6; color: #1f2328; padding: 0 20px; }}
    .badge {{ display: inline-block; padding: 14px 28px; background: #0a66c2; color: #fff; font-weight: 600; text-decoration: none; border-radius: 28px; box-shadow: 0 4px 12px rgba(10,102,194,0.3); font-size: 16px; cursor: move; }}
    .badge:hover {{ background: #004182; }}
    pre {{ background: #0d1117; color: #58a6ff; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 12px; max-height: 200px; }}
    .step {{ background: #f6f8fa; border-left: 4px solid #0a66c2; padding: 14px 18px; margin: 18px 0; border-radius: 0 8px 8px 0; }}
    .copy-btn {{ background: #238636; color: #fff; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600; cursor: pointer; }}
    .copy-btn:hover {{ background: #2ea043; }}
  </style>
</head>
<body>
  <h2>⚡ LinkedIn Architect Auto-Reply (v5.4 Multi-Method Injector)</h2>
  <p>To use this directly inside your normal Chrome browser window without installing any unpacked extensions:</p>
  
  <div class="step">
    <b>Step 1:</b> Make sure your Bookmarks Bar is visible in Chrome (press <code>Ctrl + Shift + B</code>).
  </div>
  
  <div class="step">
    <b>Step 2:</b> Drag this blue button directly onto your Chrome Bookmarks Bar:
    <div style="margin: 20px 0;">
      <a class="badge" href="{bookmarklet}">⚡ Architect Auto-Reply</a>
    </div>
    <i>Alternatively, right-click your bookmarks bar &rarr; "Add page" &rarr; Name: <code>Architect Auto-Reply</code> &rarr; URL: paste the raw code from the box below.</i>
  </div>

  <div class="step">
    <b>Raw Bookmarklet Code (Self-Contained):</b><br>
    <button class="copy-btn" onclick="navigator.clipboard.writeText(document.getElementById('raw-code').innerText); alert('Copied bookmarklet code to clipboard!');">📋 Copy Raw Bookmarklet Code</button>
    <pre id="raw-code">{bookmarklet}</pre>
  </div>

  <div class="step">
    <b>Step 3:</b> Whenever you are on <a href="https://www.linkedin.com/feed/" target="_blank">LinkedIn</a>, click the bookmark! The floating HUD will immediately appear at the bottom right with your comment replies and newsletter publishing hub.
  </div>
</body>
</html>
'''

with open(os.path.join(HERE, "bookmarklet.html"), "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Bookmarklet generated successfully! Length: {len(bookmarklet)} characters.")
