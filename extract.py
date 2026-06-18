import fitz
import os

collections = {
    "E:/Read/Books/Periyar/Anaimuthu Volumes/OCR-ed": "Anaimuthu's Periyar Collection",
    "E:/Read/Books/Periyar/Kudi Arasu/OCR-ed": "Kolathur Mani – Kudi Arasu Collection"
}

# Human-readable title mapping
title_map = {
    "anaimuthu-EVRT-Vol-1-Part-1---pp-0-122": "Thoughts of Periyar E.V.R. — Vol. 1, Part 1",
    "anaimuthu-EVRT-Vol-1-Part-2---pp-123-338": "Thoughts of Periyar E.V.R. — Vol. 1, Part 2",
    "anaimuthu-EVRT-Vol-1-Part-3---pp.-339-500": "Thoughts of Periyar E.V.R. — Vol. 1, Part 3",
    "anaimuthu-EVRT-Vol-1-Part-4---pp-501-645,-English-i-xxx": "Thoughts of Periyar E.V.R. — Vol. 1, Part 4",
    "anaimuthu-EVRT-Vol-2-Part-1---pp-646-900": "Thoughts of Periyar E.V.R. — Vol. 2, Part 1",
    "anaimuthu-EVRT-Vol-2-Part-2---pp-901-1045": "Thoughts of Periyar E.V.R. — Vol. 2, Part 2",
    "anaimuthu-EVRT-Vol-2-Part-3---pp-1046-1292,-English-i-viii": "Thoughts of Periyar E.V.R. — Vol. 2, Part 3",
    "anaimuthu-EVRT-Vol-3-Part-1---pp-1293-1634-ocr": "Thoughts of Periyar E.V.R. — Vol. 3, Part 1",
    "anaimuthu-EVRT-Vol-3-Part-2---pp-1635-1888-ocr": "Thoughts of Periyar E.V.R. — Vol. 3, Part 2",
    "anaimuthu-EVRT-Vol-3-Part-3---pp-1889-2076,-English-i-x-ocr": "Thoughts of Periyar E.V.R. — Vol. 3, Part 3",
    "kudi-arasu-1925-Preface-ocr": "Kudi Arasu — 1925 (Preface)",
    "kudi-arasu-1925-ocr": "Kudi Arasu — 1925",
    "kudi-arasu-1926-1-ocr": "Kudi Arasu — 1926, Part 1",
    "kudi-arasu-1926-2-ocr": "Kudi Arasu — 1926, Part 2",
    "kudi-arasu-1927-1-ocr": "Kudi Arasu — 1927, Part 1",
    "kudi-arasu-1927-2-ocr": "Kudi Arasu — 1927, Part 2",
    "kudi-arasu-1928-1-ocr": "Kudi Arasu — 1928, Part 1",
    "kudi-arasu-1928-2-ocr": "Kudi Arasu — 1928, Part 2",
    "kudi-arasu-1929-1-ocr": "Kudi Arasu — 1929, Part 1",
    "kudi-arasu-1929-2-ocr": "Kudi Arasu — 1929, Part 2",
    "kudi-arasu-1930-1-ocr": "Kudi Arasu — 1930, Part 1",
    "kudi-arasu-1930-2-ocr": "Kudi Arasu — 1930, Part 2",
    "kudi-arasu-1931-1-ocr": "Kudi Arasu — 1931, Part 1",
    "kudi-arasu-1931-2-ocr": "Kudi Arasu — 1931, Part 2",
    "kudi-arasu-1932-1-ocr": "Kudi Arasu — 1932, Part 1",
    "kudi-arasu-1932-2-ocr": "Kudi Arasu — 1932, Part 2",
    "kudi-arasu-1933-1-ocr": "Kudi Arasu — 1933, Part 1",
    "kudi-arasu-1933-2-ocr": "Kudi Arasu — 1933, Part 2",
    "kudi-arasu-1934-1-ocr": "Kudi Arasu — 1934, Part 1",
    "kudi-arasu-1934-2-ocr": "Kudi Arasu — 1934, Part 2",
    "kudi-arasu-1935-1-ocr": "Kudi Arasu — 1935, Part 1",
    "kudi-arasu-1935-2-ocr": "Kudi Arasu — 1935, Part 2",
    "kudi-arasu-1936-1-ocr": "Kudi Arasu — 1936, Part 1",
    "kudi-arasu-1936-2-ocr": "Kudi Arasu — 1936, Part 2",
    "kudi-arasu-1937-1-ocr": "Kudi Arasu — 1937, Part 1",
    "kudi-arasu-1937-2-ocr": "Kudi Arasu — 1937, Part 2",
    "kudi-arasu-1938-1-ocr": "Kudi Arasu — 1938, Part 1",
    "kudi-arasu-1938-2-ocr": "Kudi Arasu — 1938, Part 2",
    "kudi-arasu-Revolt": "Revolt: A Radical Weekly",
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
        key = out_filename.replace(".html", "")
        display_title = title_map.get(key, slug)
        out_path = os.path.join("docs", out_filename)

        safe_text = full_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script data-goatcounter="https://periyararchive.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<title>{display_title} — Periyar Archive</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&family=Noto+Serif:wght@400;700&display=swap" rel="stylesheet">
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{
    font-family: 'Noto Serif Tamil', 'Noto Serif', serif;
    background: #111;
    color: #ddd;
    line-height: 1.8;
  }}
  header {{
    background: #111;
    color: #fff;
    padding: 14px 30px;
    display: flex;
    align-items: center;
    gap: 20px;
    border-bottom: 2px solid #cc0000;
  }}
  header a {{
    color: #fff;
    text-decoration: none;
    font-size: 14px;
    font-family: sans-serif;
    border: 1px solid #555;
    padding: 4px 12px;
    border-radius: 3px;
    white-space: nowrap;
  }}
  header a:hover {{ border-color: #cc0000; color: #cc0000; }}
  header span {{
    font-size: 14px;
    color: #aaa;
    font-family: sans-serif;
  }}
  .doc-container {{
    max-width: 780px;
    margin: 40px auto;
    padding: 0 48px 80px;
  }}
  h1 {{
    font-size: 1.4em;
    margin-bottom: 6px;
    line-height: 1.4;
    color: #fff;
  }}
  .collection-label {{
    font-size: 0.85em;
    color: #777;
    font-family: sans-serif;
    margin-bottom: 30px;
    display: block;
  }}
  #content {{
    white-space: pre-wrap;
    font-size: 1.05em;
    line-height: 1.9;
    color: #ddd;
  }}
  .search-banner {{
    background: #1e1e1e;
    border-left: 3px solid #cc0000;
    padding: 10px 18px;
    margin-bottom: 24px;
    font-family: sans-serif;
    font-size: 14px;
    color: #aaa;
  }}
</style>
<script>
window.addEventListener("DOMContentLoaded", () => {{
  const params = new URLSearchParams(window.location.search);
  const term = decodeURIComponent(params.get("highlight") || "");

  // Build search box
  const searchBox = document.createElement("div");
  searchBox.className = "search-banner";
  searchBox.innerHTML = `
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      <input id="doc-search" type="text" placeholder="Search within this document..."
        style="flex:1;min-width:200px;padding:6px 10px;background:#2a2a2a;color:#eee;border:1px solid #444;border-radius:3px;font-size:14px;font-family:sans-serif;"
        value="${{term}}">
      <button onclick="searchInPage()" style="padding:6px 14px;background:#cc0000;color:#fff;border:none;border-radius:3px;cursor:pointer;font-size:14px;font-family:sans-serif;">Find</button>
      <span id="match-count" style="font-size:13px;color:#888;font-family:sans-serif;"></span>
    </div>`;
  document.querySelector(".doc-container").insertBefore(searchBox, document.querySelector(".doc-container").firstChild);

  // Search function
  window.searchInPage = function() {{
    const query = document.getElementById("doc-search").value.trim();
    if (!query) return;
    const content = document.getElementById("content");
    const text = content.innerHTML;
    // Remove previous highlights
    content.innerHTML = text.replace(/<mark class="doc-highlight">(.*?)<\/mark>/g, "$1");
    if (!query) return;
    const escaped = query.replace(/[.*+?^${{}}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(escaped, "gi");
    const newText = content.innerHTML.replace(regex, match => `<mark class="doc-highlight" style="background:#cc0000;color:#fff;border-radius:2px;padding:0 2px;">${{match}}</mark>`);
    content.innerHTML = newText;
    const first = content.querySelector(".doc-highlight");
    if (first) first.scrollIntoView({{behavior: "smooth", block: "center"}});
    const count = content.querySelectorAll(".doc-highlight").length;
    document.getElementById("match-count").textContent = count > 0 ? `${{count}} match${{count > 1 ? "es" : ""}}` : "No matches";
  }};

  // Trigger search on Enter key
  document.addEventListener("keydown", e => {{
    if (e.key === "Enter" && document.activeElement.id === "doc-search") searchInPage();
  }});

  // Auto-search if term came from search results
  if (term) searchInPage();
}});
</script>
</head>
<body>
<header>
  <a href="/">&#8592; Home</a>
  <span>Periyar Archive</span>
</header>
<div class="doc-container">
<h1>{display_title}</h1>
<span class="collection-label">{collection_name}</span>
<div id="content">{safe_text}</div>
</div>
</body>
</html>"""

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(html)

        index_links.append((out_filename, display_title, collection_name))
        print(f"  Done: {out_filename}")

# Write index page
with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script data-goatcounter="https://periyararchive.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<title>பெரியார் தேடகம் — Periyar Archive</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&family=Noto+Serif:wght@400;700&display=swap" rel="stylesheet">
<link href="/pagefind/pagefind-ui.css" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Noto Serif Tamil', 'Noto Serif', serif;
    background: #111;
    color: #eee;
  }
  header {
    background: #111;
    color: #fff;
    padding: 28px 30px;
    text-align: center;
    border-bottom: 2px solid #cc0000;
  }
  header h1 {
    font-size: 1.5em;
    font-weight: 700;
    letter-spacing: 0.01em;
  }
  header p {
    font-size: 0.85em;
    color: #aaa;
    margin-top: 6px;
    font-family: sans-serif;
  }
  .main {
    max-width: 780px;
    margin: 40px auto;
    padding: 0 24px;
  }
  .description {
    font-size: 0.95em;
    color: #aaa;
    line-height: 1.7;
    margin-bottom: 28px;
    font-family: sans-serif;
  }
  :root {
    --pagefind-ui-scale: 1;
    --pagefind-ui-primary: #cc0000;
    --pagefind-ui-text: #eee;
    --pagefind-ui-background: #1e1e1e;
    --pagefind-ui-border: #444;
    --pagefind-ui-tag: #222;
    --pagefind-ui-border-width: 1px;
    --pagefind-ui-border-radius: 3px;
    --pagefind-ui-font: sans-serif;
  }
  #search { margin-bottom: 20px; }
  .notes {
    font-family: sans-serif;
    font-size: 0.85em;
    color: #aaa;
    line-height: 1.6;
    margin-bottom: 8px;
  }
  .notes strong { color: #eee; }
  .contact {
    font-family: sans-serif;
    font-size: 0.85em;
    color: #aaa;
    margin-bottom: 32px;
  }
  .contact a { color: #aaa; text-decoration: underline; }
  .contact a:hover { color: #eee; }
  hr { border: none; border-top: 1px solid #333; margin-bottom: 24px; }
  #browse-heading {
    cursor: pointer;
    font-size: 1em;
    font-family: sans-serif;
    font-weight: 600;
    color: #eee;
    margin-bottom: 12px;
    user-select: none;
  }
  #browse-heading:hover { color: #cc0000; }
  #browse-list {
    list-style: none;
    font-family: sans-serif;
    font-size: 0.9em;
  }
  #browse-list li {
    padding: 6px 0;
    border-bottom: 1px solid #222;
  }
  #browse-list a { color: #ccc; text-decoration: none; }
  #browse-list a:hover { color: #cc0000; }
  #browse-list small { color: #666; }
</style>
</head>
<body>
<header>
  <h1>பெரியார் தேடகம் — Periyar Archive</h1>
  <p>A full-text searchable archive of Periyar E.V. Ramasamy's writings</p>
</header>
<div class="main">
  <p class="description" style="margin-top:28px;">Search across the collected volumes of Periyar's writings published by V Anaimuthu (1974 edition) and the Kudi Arasu and Revolt collections published by Kolathur Mani.</p>
  <div id="search"></div>
  <script src="/pagefind/pagefind-ui.js"></script>
  <script>
    window.addEventListener('DOMContentLoaded', () => {
      new PagefindUI({
        element: "#search",
        showImages: false,
        highlightParam: "highlight",
        translations: {
          placeholder: "Search",
          clear_search: "Clear",
          load_more: "Load more results",
          search_label: "Search this archive",
          filters_label: "Filters",
          zero_results: "No results for [SEARCH_TERM]",
          many_results: "[COUNT] results for [SEARCH_TERM]",
          one_result: "[COUNT] result for [SEARCH_TERM]",
          alt_search: "No results for [SEARCH_TERM]. Showing results for [DIFFERENT_TERM] instead",
          search_suggestion: "No results for [SEARCH_TERM]. Try one of the following searches:",
          searching: "Searching for [SEARCH_TERM]..."
        }
      });
    });
  </script>
  <p class="notes"><strong>Note for Tamil searches:</strong> The search may return words sharing similar characters. For example, a search for "மானம்" might also return results including "மேன்மை".</p>
  <p class="contact">For questions or feedback: <a href="mailto:ganeshwarbaarath@gmail.com">ganeshwarbaarath@gmail.com</a></p>
  <hr>
  <h2 id="browse-heading">&#9654; Browse Documents <small style="font-size:0.75em;font-weight:normal;color:#666;">click to expand</small></h2>
  <p style="font-family:sans-serif;font-size:0.9em;margin-bottom:16px;"><a href="https://theperiyarproject.wordpress.com/2022/09/17/a-periyar-reading-list/" target="_blank" style="color:#aaa;text-decoration:underline;">&#9654; For more on Periyar: A Periyar Reading List</a></p>
  <ul id="browse-list" style="display:none;">
""")
    for out_filename, display_title, collection_name in index_links:
        f.write(f'<li><a href="{out_filename}">{display_title}</a> <small>({collection_name})</small></li>\n')
    f.write("""</ul>
<script>
document.getElementById("browse-heading").addEventListener("click", function() {
  const list = document.getElementById("browse-list");
  const heading = document.getElementById("browse-heading");
  if (list.style.display === "none") {
    list.style.display = "block";
    heading.innerHTML = "&#9660; Browse Documents <small style=\\"font-size:0.75em;font-weight:normal;color:#666;\\">click to collapse</small>";
  } else {
    list.style.display = "none";
    heading.innerHTML = "&#9654; Browse Documents <small style=\\"font-size:0.75em;font-weight:normal;color:#666;\\">click to expand</small>";
  }
});
</script>
</div>
</body>
</html>""")

print("\nAll done. HTML files are in the docs/ folder.")
print(f"Total documents processed: {len(index_links)}")