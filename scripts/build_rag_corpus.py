import glob
import json
import re

docs = []
files = sorted(glob.glob("my_account/posts/*.md") + glob.glob("my_account/newsletter/editions/*.md"))

for p in files:
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()

    filename = p.replace("\\", "/").split("/")[-1]
    title_m = re.search(r'title:\s*["\']?(.*?)["\']?$', text, re.MULTILINE)
    title = title_m.group(1) if title_m else filename

    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].strip()

    # Split by section headers or large paragraphs
    sections = re.split(r'\n(?=## |\n\n)', body)
    for i, sec in enumerate(sections):
        clean = sec.strip()
        if len(clean) < 60:
            continue
        header_m = re.search(r'^##\s+(.*)$', clean, re.MULTILINE)
        sec_name = header_m.group(1) if header_m else f"{title[:40]} (Part {i+1})"
        
        # Remove markdown symbols
        clean_text = re.sub(r'#+\s*', '', clean)
        clean_text = re.sub(r'[*_`]', '', clean_text)
        clean_text = ' '.join(clean_text.split())
        
        if len(clean_text) > 40:
            docs.append({
                "file": filename,
                "section": sec_name[:65],
                "content": clean_text[:450],
                "line": (i + 1) * 12
            })

print(f"Total extracted documents: {len(docs)}")
with open("scripts/rag_corpus.json", "w", encoding="utf-8") as out:
    json.dump(docs, out, indent=2, ensure_ascii=False)

