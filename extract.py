import fitz
import os

collections = {
    "E:/Read/Books/Periyar/Anaimuthu Volumes/OCR-ed": "Anaimuthu's Periyar Collection",
    "E:/Read/Books/Periyar/Kudi Arasu/OCR-ed": "Kolathur Mani – Kudi Arasu Collection"
}

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

doc_search_script = """
window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const term = decodeURIComponent(params.get("highlight") || "");

  const searchBox = document.createElement("div");
  searchBox.className = "search-banner";
  searchBox.innerHTML = `
    <div style="display:flex; justify-content: flex-end; margin-bottom: 8px;">
      <button id="doc-toggle-btn" style="background: transparent; color: #cc0000; border: 1px solid #cc0000; padding: 4px 12px; border-radius: 3px; font-family: sans-serif; font-size: 12px; cursor: pointer;">Keyboard: <strong>தமிழ் (ON)</strong></button>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      <input id="doc-search" type="text" placeholder="Search within this document..."
        style="flex:1;min-width:200px;padding:6px 10px;background:#2a2a2a;color:#eee;border:1px solid #444;border-radius:3px;font-size:14px;font-family:sans-serif;"
        value="${term}">
      <button id="doc-search-btn" style="padding:6px 14px;background:#cc0000;color:#fff;border:none;border-radius:3px;cursor:pointer;font-size:14px;font-family:sans-serif;">Find</button>
      <span id="match-count" style="font-size:13px;color:#888;font-family:sans-serif;"></span>
    </div>`;
  document.querySelector(".doc-container").insertBefore(searchBox, document.querySelector(".doc-container").firstChild);

  const searchInput = document.getElementById("doc-search");
  const toggleBtn = document.getElementById("doc-toggle-btn");
  const content = document.getElementById("content");

  let isTamil = true;
  toggleBtn.addEventListener('click', (e) => {
    e.preventDefault();
    isTamil = !isTamil;
    toggleBtn.innerHTML = isTamil ? 'Keyboard: <strong>தமிழ் (ON)</strong>' : 'Keyboard: <strong>English (ON)</strong>';
    toggleBtn.style.color = isTamil ? '#cc0000' : '#aaa';
    toggleBtn.style.borderColor = isTamil ? '#cc0000' : '#555';
    searchInput.focus();
  });

  async function transliterate(text) {
    if (!text.trim() || !/[a-zA-Z]/.test(text)) return text;
    try {
      const url = `https://inputtools.google.com/request?text=${encodeURIComponent(text)}&itc=ta-t-i0-und&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=jsapi`;
      const response = await fetch(url);
      const data = await response.json();
      if (data && data[0] === 'SUCCESS') {
        return data[1][0][1][0];
      }
    } catch (e) {
      console.error("Transliteration blocked:", e);
    }
    return text;
  }

  searchInput.addEventListener('keyup', async (e) => {
    if (!isTamil) return;
    if (e.key === ' ' || e.key === 'Enter') {
      const words = searchInput.value.split(' ');
      const targetIndex = e.key === ' ' ? words.length - 2 : words.length - 1;
      const wordToTranslate = words[targetIndex];
      if (wordToTranslate && /[a-zA-Z]/.test(wordToTranslate)) {
        const tamilWord = await transliterate(wordToTranslate);
        words[targetIndex] = tamilWord;
        searchInput.value = words.join(' ');
      }
    }
  });

  window.searchInPage = function() {
    const query = searchInput.value.trim();
    const marks = content.querySelectorAll('mark.doc-highlight');
    marks.forEach(mark => {
      const parent = mark.parentNode;
      parent.replaceChild(document.createTextNode(mark.textContent), mark);
      parent.normalize();
    });
    if (!query) {
      document.getElementById("match-count").textContent = "";
      return;
    }
    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
    const regex = new RegExp(`(${escaped})`, "gi");
    content.innerHTML = content.innerHTML.replace(regex, `<mark class="doc-highlight" style="background:#cc0000;color:#fff;border-radius:2px;padding:0 2px;">$1</mark>`);
    const first = content.querySelector(".doc-highlight");
    if (first) first.scrollIntoView({behavior: "smooth", block: "center"});
    const count = content.querySelectorAll(".doc-highlight").length;
    document.getElementById("match-count").textContent = count > 0 ? count + (count > 1 ? " matches" : " match") : "No matches";
  };

  document.getElementById("doc-search-btn").addEventListener("click", searchInPage);
  document.addEventListener("keydown", e => {
    if (e.key === "Enter" && document.activeElement.id === "doc-search") searchInPage();
  });

  if (term) searchInPage();
});
"""

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
            if "Anaimuthu" in collection_name or "Revolt" in filename:
                for page in doc:
                    blocks = page.get_text("blocks")
                    blocks = sorted(blocks, key=lambda b: (b[1], b[0]))
                    for block in blocks:
                        block_text = block[4].strip()
                        if block_text:
                            full_text += block_text + "\n\n"
            else:
                for page in doc:
                    blocks = page.get_text("blocks")
                    mid_x = page.rect.width / 2
                    left_col, right_col = [], []
                    for b in blocks:
                        if b[6] == 0:
                            if b[0] < mid_x:
                                left_col.append(b)
                            else:
                                right_col.append(b)
                    left_col.sort(key=lambda b: b[1])
                    right_col.sort(key=lambda b: b[1])
                    for block in (left_col + right_col):
                        clean_text = block[4].strip().replace("\n", " ")
                        if clean_text:
                            full_text += clean_text + "\n\n"
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

<meta property="og:title" content="{display_title} — Periyar Archive" />
<meta property="og:description" content="A full-text searchable archive of Periyar E.V. Ramasamy's writings." />
<meta property="og:image" content="https://periyararchive.in/thumbnail.jpg" />
<meta property="og:url" content="https://periyararchive.in/" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{display_title} — Periyar Archive" />
<meta name="twitter:description" content="A full-text searchable archive of Periyar E.V. Ramasamy's writings." />
<meta name="twitter:image" content="https://periyararchive.in/thumbnail.jpg" />

<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&family=Noto+Serif:wght@400;700&display=swap" rel="stylesheet"><style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Noto Serif Tamil', 'Noto Serif', serif; background: #111; color: #ddd; line-height: 1.8; }}
  header {{ background: #111; color: #fff; padding: 14px 30px; display: flex; align-items: center; gap: 20px; border-bottom: 2px solid #cc0000; }}
  header a {{ color: #fff; text-decoration: none; font-size: 14px; font-family: sans-serif; border: 1px solid #555; padding: 4px 12px; border-radius: 3px; white-space: nowrap; }}
  header a:hover {{ border-color: #cc0000; color: #cc0000; }}
  header span {{ font-size: 14px; color: #aaa; font-family: sans-serif; }}
  .doc-container {{ max-width: 780px; margin: 40px auto; padding: 0 48px 80px; }}
  h1 {{ font-size: 1.4em; margin-bottom: 6px; line-height: 1.4; color: #fff; }}
  .collection-label {{ font-size: 0.85em; color: #777; font-family: sans-serif; margin-bottom: 30px; display: block; }}
  #content {{ white-space: pre-wrap; font-size: 1.05em; line-height: 1.9; color: #ddd; }}
  .search-banner {{ background: #1e1e1e; border-left: 3px solid #cc0000; padding: 10px 18px; margin-bottom: 24px; font-family: sans-serif; font-size: 14px; color: #aaa; }}
</style>
<script>{doc_search_script}</script>
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

<meta property="og:title" content="பெரியார் தேடகம் — Periyar Archive" />
<meta property="og:description" content="A full-text searchable archive of Periyar E.V. Ramasamy's writings." />
<meta property="og:image" content="https://periyararchive.in/thumbnail.jpg" />
<meta property="og:url" content="https://periyararchive.in/" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="பெரியார் தேடகம் — Periyar Archive" />
<meta name="twitter:description" content="A full-text searchable archive of Periyar E.V. Ramasamy's writings." />
<meta name="twitter:image" content="https://periyararchive.in/thumbnail.jpg" />

<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&family=Noto+Serif:wght@400;700&display=swap" rel="stylesheet">
<link href="/pagefind/pagefind-ui.css" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Noto Serif Tamil', 'Noto Serif', serif; background: #111; color: #eee; }
  header { background: #111; color: #fff; padding: 28px 30px; text-align: center; border-bottom: 2px solid #cc0000; }
  header h1 { font-size: 1.5em; font-weight: 700; letter-spacing: 0.01em; }
  header p { font-size: 0.85em; color: #aaa; margin-top: 6px; font-family: sans-serif; }
  .main { max-width: 780px; margin: 40px auto; padding: 0 24px; }
  .description { font-size: 0.95em; color: #aaa; line-height: 1.7; margin-bottom: 28px; font-family: sans-serif; }
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
  .notes { font-family: sans-serif; font-size: 0.85em; color: #aaa; line-height: 1.6; margin-bottom: 8px; }
  .notes strong { color: #eee; }
  .contact { font-family: sans-serif; font-size: 0.85em; color: #aaa; margin-bottom: 32px; }
  .contact a { color: #aaa; text-decoration: underline; }
  .contact a:hover { color: #eee; }
  hr { border: none; border-top: 1px solid #333; margin-bottom: 24px; }
  #browse-heading { cursor: pointer; font-size: 1em; font-family: sans-serif; font-weight: 600; color: #eee; margin-bottom: 12px; user-select: none; }
  #browse-heading:hover { color: #cc0000; }
  #browse-list { list-style: none; font-family: sans-serif; font-size: 0.9em; }
  #browse-list li { padding: 6px 0; border-bottom: 1px solid #222; }
  #browse-list a { color: #ccc; text-decoration: none; }
  #browse-list a:hover { color: #cc0000; }
  #browse-list small { color: #666; }
</style>
</head>
<body>
<header>
  <h1>பெரியார் தேடகம் — Periyar Archive</h1>
  <p style="margin-bottom: 14px;">A full-text searchable archive of Periyar E.V. Ramasamy's writings</p>
  <a href="about.html" style="color: #fff; text-decoration: none; font-size: 13px; font-family: sans-serif; border: 1px solid #555; padding: 5px 14px; border-radius: 3px; display: inline-block;">About the Archive</a>
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

      const isDesktop = window.innerWidth > 768 && !(/Mobi|Android/i.test(navigator.userAgent));
      if (isDesktop) {
        const checkExist = setInterval(function() {
          const searchInput = document.querySelector('.pagefind-ui__search-input');
          if (searchInput) {
            clearInterval(checkExist);

            const toggleContainer = document.createElement('div');
            toggleContainer.style.cssText = 'display: flex; justify-content: flex-end; margin-bottom: 8px;';
            const toggleBtn = document.createElement('button');
            toggleBtn.innerHTML = 'Keyboard: <strong>தமிழ் (ON)</strong>';
            toggleBtn.style.cssText = 'background: transparent; color: #cc0000; border: 1px solid #cc0000; padding: 4px 12px; border-radius: 3px; font-family: sans-serif; font-size: 12px; cursor: pointer;';
            toggleContainer.appendChild(toggleBtn);
            const searchDiv = document.getElementById('search');
            searchDiv.parentNode.insertBefore(toggleContainer, searchDiv);

            let isTamil = true;
            toggleBtn.addEventListener('click', (e) => {
              e.preventDefault();
              isTamil = !isTamil;
              toggleBtn.innerHTML = isTamil ? 'Keyboard: <strong>தமிழ் (ON)</strong>' : 'Keyboard: <strong>English (ON)</strong>';
              toggleBtn.style.color = isTamil ? '#cc0000' : '#aaa';
              toggleBtn.style.borderColor = isTamil ? '#cc0000' : '#555';
              searchInput.focus();
            });

            async function transliterate(text) {
              if (!text.trim() || !/[a-zA-Z]/.test(text)) return text;
              try {
                const url = `https://inputtools.google.com/request?text=${encodeURIComponent(text)}&itc=ta-t-i0-und&num=1&cp=0&cs=1&ie=utf-8&oe=utf-8&app=jsapi`;
                const response = await fetch(url);
                const data = await response.json();
                if (data && data[0] === 'SUCCESS') {
                  return data[1][0][1][0];
                }
              } catch (e) {
                console.error("Transliteration blocked:", e);
              }
              return text;
            }

            searchInput.addEventListener('keyup', async (e) => {
              if (!isTamil) return;
              if (e.key === ' ' || e.key === 'Enter') {
                const words = searchInput.value.split(' ');
                const targetIndex = e.key === ' ' ? words.length - 2 : words.length - 1;
                const wordToTranslate = words[targetIndex];
                if (wordToTranslate && /[a-zA-Z]/.test(wordToTranslate)) {
                  const tamilWord = await transliterate(wordToTranslate);
                  words[targetIndex] = tamilWord;
                  searchInput.value = words.join(' ');
                  searchInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
              }
            });
          }
        }, 100);
      }
    });
  </script>
  <p class="notes"><strong>Note for Tamil searches:</strong> The search may return words sharing similar characters. For example, a search for "மானம்" might also return results including "மேன்மை".</p>
  <p class="contact">For questions or feedback: <a href="mailto:contact@periyararchive.in">contact@periyararchive.in</a></p>
  <hr>
  <p style="font-family:sans-serif;font-size:0.9em;margin-bottom:16px;"><a href="https://theperiyarproject.wordpress.com/2022/09/17/a-periyar-reading-list/" target="_blank" style="color:#aaa;text-decoration:underline;">&#9654; For more on Periyar: A Periyar Reading List</a></p>
  <h2 id="browse-heading">&#9654; Browse Documents <small style="font-size:0.75em;font-weight:normal;color:#666;">click to expand</small></h2>
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

# --- GENERATE ABOUT PAGE ---
about_html = """<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script data-goatcounter="https://periyararchive.goatcounter.com/count" async src="//gc.zgo.at/count.js"></script>
<title>About — Periyar Archive</title>

<meta property="og:title" content="About — Periyar Archive" />
<meta property="og:description" content="A full-text searchable archive of Periyar E.V. Ramasamy's writings." />
<meta property="og:image" content="https://periyararchive.in/thumbnail.jpg" />
<meta property="og:url" content="https://periyararchive.in/about.html" />
<meta property="og:type" content="website" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="About — Periyar Archive" />
<meta name="twitter:description" content="A full-text searchable archive of Periyar E.V. Ramasamy's writings." />
<meta name="twitter:image" content="https://periyararchive.in/thumbnail.jpg" />

<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&family=Noto+Serif:wght@400;700&display=swap" rel="stylesheet">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: 'Noto Serif Tamil', 'Noto Serif', serif; background: #111; color: #ddd; line-height: 1.8; }
  header { background: #111; color: #fff; padding: 14px 30px; display: flex; align-items: center; gap: 20px; border-bottom: 2px solid #cc0000; }
  header a { color: #fff; text-decoration: none; font-size: 14px; font-family: sans-serif; border: 1px solid #555; padding: 4px 12px; border-radius: 3px; white-space: nowrap; }
  header a:hover { border-color: #cc0000; color: #cc0000; }
  header span { font-size: 14px; color: #aaa; font-family: sans-serif; }
  .doc-container { max-width: 780px; margin: 40px auto; padding: 0 48px 80px; }
  h1 { font-size: 1.8em; margin-bottom: 24px; color: #fff; }
  h2 { font-size: 1.3em; margin-top: 36px; margin-bottom: 16px; color: #fff; border-bottom: 1px solid #333; padding-bottom: 6px; }
  p { margin-bottom: 18px; font-size: 1.05em; line-height: 1.9; }
  ul { margin-bottom: 18px; padding-left: 24px; font-size: 1.05em; line-height: 1.9; }
  li { margin-bottom: 12px; }
  blockquote { background: #1e1e1e; border-left: 3px solid #cc0000; padding: 14px 18px; margin-bottom: 24px; font-size: 0.95em; color: #ccc; }
  a { color: #cc0000; text-decoration: none; }
  a:hover { text-decoration: underline; }
</style>
</head>
<body>
<header>
  <a href="/">&#8592; Home</a>
  <span>Periyar Archive</span>
</header>
<div class="doc-container">
  <h1>About Periyar Archive</h1>
  <p>The Periyar Archive (periyararchive.in) is a comprehensive, open-access digital database dedicated to the writings, speeches, and editorial work of E.V. Ramasamy 'Periyar'. Designed for researchers, historians, and the general public, this platform provides full-text searchability across publicly available compilations of Periyar's writings and speeches.</p>
  <p>While the novelty and radicality of Periyar's approaches to caste, gender, religion, nation, and culture have often been recognised by anti-caste scholars and activists around the world, there has been a significant barrier to accessing his primary texts. This archive aims to dismantle that barrier by digitising more than 13,500 pages of his public writings and speeches into a single database, indexing over 3,50,000 unique search terms for exhaustive textual analysis.</p>

  <h2>The Collections &amp; Provenance</h2>
  <p>This searchable database stands on the shoulders of the scholars, activists, and organisations who painstakingly compiled, edited, and digitised Periyar's original print publications. The archive currently indexes the following major collections:</p>
  <ul>
    <li><strong>The V. Anaimuthu Volumes (1974 Edition):</strong> This magisterial compilation organised Periyar's thoughts across various social and political themes into three volumes and ten parts. It was put together by the extraordinary labour of V Anaimuthu and his Sinthanaiyalar Kazhagam. In 2011, under the presidency of Ku. Ma. Subramanian, the organisation generously permitted these volumes to be uploaded for free online public access. This collection has now been expanded into 20 parts, though they remain to be digitised.</li>
    <li><strong>The Kudi Arasu Collection (27 Volumes):</strong> Originally published as the flagship weekly of the Self-Respect Movement, Kudi Arasu ran as a weekly between 1925 and 1949. In addition to serving as the ideological repository of the Self-Respect Movement during its heyday, it also published the first Tamil translations of Marx and Engels's <em>Communist Manifesto</em>, Bhagat Singh's <em>Why I am an Atheist</em>, Lenin's essays on religion (serialised and later published as <em>Leninum Mathamum</em>), and Babasaheb Ambedkar's <em>Annihilation of Caste</em>. Periyar's writings in Kudi Arasu between 1925 and 1938 (alongside Puratchi and Pagutharivu, published when Kudi Arasu was banned in 1934) were compiled and edited into 27 volumes in 2008 by Kolathur Mani for the Periyar Dravidar Kazhagam (PDK). He now leads the Dravidar Viduthalai Kazhagam (DVK).</li>
    <li><strong>The Revolt Collection:</strong> The Self-Respect Movement's first English-language weekly was published by Periyar for over two years between 1928 and 1930, at a time when very few Tamilians, and fewer still Tamil non-Brahmins, could read or write English. Articles published in the weekly were compiled and edited for the PDK by noted scholars V. Geetha and S.V. Rajadurai.</li>
  </ul>
  <p>Both these compilations were published by Kolathur Mani, who made the digital files freely available online to ensure Periyar's legacy remained unrestricted by copyright and accessible to all. This archive aggregates those very files to preserve them and make them fully searchable.</p>

  <h2>Methodology &amp; Usage</h2>
  <p>To transform these historical print compilations into a modern research tool, the archive employs a multi-stage digital pipeline:</p>
  <ul>
    <li><strong>Optical Character Recognition (OCR):</strong> Because the source volumes were preserved as image-only documents, they were systematically processed via OCR text-recognition tools to construct searchable text layers.</li>
    <li><strong>Indexing &amp; Search:</strong> Full-text extraction and search capability are powered by Pagefind, an open-source static search engine. This infrastructure allows for high-speed, client-side keyword discovery across thousands of pages without requiring heavy server-side processing.</li>
  </ul>
  <blockquote><strong>Note on Scan and Search Accuracy:</strong> Because the database relies on automated OCR of historical typography, some character recognition, line break and page break errors may persist. Furthermore, as Pagefind is not optimised for Tamil's agglutinative morphology (joint letters), the search results might be more expansive than required, especially for short search terms. The archive recognises these limitations and is continuously in search of ways to address them.</blockquote>

  <h2>Curation &amp; Contact</h2>
  <p>The Periyar Archive is an independent digital humanities project curated and maintained by Ganeshwar, a researcher working on Periyar's political thought. It is a completely non-commercial endeavour built solely to facilitate historical research and public education. It is not monetised in any way and does not collect any third-party user data.</p>
  <p>For questions, feedback, or to report archival errors, please reach out at: <a href="mailto:contact@periyararchive.in">contact@periyararchive.in</a></p>
</div>
</body>
</html>"""

with open("docs/about.html", "w", encoding="utf-8") as f:
    f.write(about_html)

print("  Done: about.html generated")