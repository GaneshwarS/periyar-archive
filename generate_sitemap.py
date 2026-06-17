import os

docs_dir = "docs"
base_url = "https://periyararchive.in"

urls = []
for filename in sorted(os.listdir(docs_dir)):
    if not filename.endswith(".html"):
        continue
    if filename.startswith("google"):
        continue
    url = f"{base_url}/{filename}"
    urls.append(url)

with open("docs/sitemap.xml", "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for url in urls:
        f.write(f'  <url><loc>{url}</loc></url>\n')
    f.write('</urlset>\n')

print(f"Done. Sitemap created with {len(urls)} URLs.")