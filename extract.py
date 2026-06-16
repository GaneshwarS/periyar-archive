import fitz
import os

collections = {
    "E:/Read/Books/Periyar/Anaimuthu Volumes/OCR-ed": "Anaimuthu's Periyar Collection",
    "E:/Read/Books/Periyar/Kudi Arasu/OCR-ed": "Kolathur Mani – Kudi Arasu Collection"
}

os.makedirs("docs", exist_ok=True)

index_links = []

for folder_path, collection_name in collections.items():
    if not os.path.exists(folder_path):
        print(f"WARNING: Could not find folder: {folder_path}")
        continue
    for filename in sorted(os.listdir(folder_path)):
        if not filename.lower().endswith(".pdf"):
            continue
        filepath = os.path.join(folder_path, filename)
        print(f"Processing: {filename}")
        try:
            doc = fitz.open(filepath)
            full_text = ""
            for page in doc:
                full_text += page.get_text() + "\n\n"
            doc.close()
        except Exception as e:
            print(f"  ERROR reading {filename}: {e}")
            continue

        slug = filename.replace(".pdf", "").replace(" ", "-")
        collection_slug = "anaimuthu" if "Anaimuthu" in collection_name else "kudi-arasu"
        out_filename = f"{collection_slug}-{slug}.html"
        out_path = os.path.join("docs", out_filename)

        # Escape any characters that would break HTML
        safe_text = full_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<title>{slug} — {collection_name}</title>
</head>
<body>
<h1>{slug}</h1>
<p><em>Collection: {collection_name}</em></p>
<div id="content">
<div id="content" style="white-space: pre-wrap; font-family: sans-serif;">{safe_text}</div>
</div>
</body>
</html>"""

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        index_links.append((out_filename, slug, collection_name))
        print(f"  Done: {out_filename}")

# Write index page
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<title>பெரியார் தேடகம் — Periyar Archive</title>
<link href="/pagefind/pagefind-ui.css" rel="stylesheet">
<style>
  body { font-family: sans-serif; max-width: 860px; margin: 40px auto; padding: 0 20px; }
  h1 { font-size: 1.6em; }
  #search { margin: 30px 0; }
</style>
</head>
<body>
<h1>பெரியார் தேடகம் — Periyar Archive</h1>
<p>Search across Anaimuthu's collected volumes and the Kolathur Mani Kudi Arasu collection.</p>
<div id="search"></div>
<script src="/pagefind/pagefind-ui.js"></script>
<script>
  window.addEventListener('DOMContentLoaded', () => {
    new PagefindUI({ element: "#search", showImages: false });
  });
</script>
<hr>
<h2>Browse Documents</h2>
<ul>
""")
    for out_filename, slug, collection_name in index_links:
        f.write(f'<li><a href="{out_filename}">{slug}</a> <small>({collection_name})</small></li>\n')
    f.write("</ul>\n</body>\n</html>")

print("\nAll done. HTML files are in the docs/ folder.")
print(f"Total documents processed: {len(index_links)}")