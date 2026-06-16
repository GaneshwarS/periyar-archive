import os

docs_dir = "docs"

for filename in os.listdir(docs_dir):
    if filename == "index.html" or not filename.endswith(".html"):
        continue
    filepath = os.path.join(docs_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    # Fix the path regardless of what's there now
    content = content.replace(
        '<script src="pagefind/pagefind-highlight.js"></script>',
        '<script src="/pagefind/pagefind-highlight.js"></script>'
    )
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {filename}")

print("Done.")