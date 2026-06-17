import os

docs_dir = "docs"

home_button = '''<div style="margin-bottom:15px;">
<a href="/" style="text-decoration:none;background:#f0f0f0;padding:6px 14px;border-radius:4px;font-family:sans-serif;font-size:14px;">&#8592; Home</a>
</div>'''

count = 0
for filename in os.listdir(docs_dir):
    if filename == "index.html" or not filename.endswith(".html"):
        continue
    filepath = os.path.join(docs_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if "&#8592; Home" in content:
        print(f"Already has home button: {filename}")
        continue
    content = content.replace("<body>", "<body>\n" + home_button)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1
    print(f"Updated: {filename}")

print(f"\nDone. Added home button to {count} files.")