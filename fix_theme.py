import os

dirs = ["docs", "corrected"]

style_block = """<style>
  body { background: #111 !important; color: #ddd !important; }
  h1 { color: #fff !important; }
  .collection-label { color: #777 !important; }
  #content { color: #ddd !important; }
  a { color: #ccc !important; }
</style>"""

for folder in dirs:
    for filename in os.listdir(folder):
        if filename == "index.html" or not filename.endswith(".html"):
            continue
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if "background: #111" in content or "background:#111" in content:
            print(f"Already themed: {filename}")
            continue
        content = content.replace("</head>", style_block + "\n</head>")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filename}")

print("Done.")