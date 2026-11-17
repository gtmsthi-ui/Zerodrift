import re

with open("content.js", "r", encoding="utf-8") as f:
    js = f.read()

with open("overlay.css", "r", encoding="utf-8") as f:
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

with open("bookmarklet.txt", "w", encoding="utf-8") as f:
    f.write(bookmarklet)

print("Bookmarklet generated successfully! Length:", len(bookmarklet))

