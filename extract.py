import fitz
import os

collections = {
    "E:/Read/Books/Periyar/Anaimuthu Volumes/OCR-ed": "Anaimuthu's Periyar Collection",
    "E:/Read/Books/Periyar/Kudi Arasu/OCR-ed": "Kolathur Mani – Kudi Arasu Collection"
}

title_map = {
    "anaimuthu-EVRT-Vol-1-Part-1---pp-0-122": "Thoughts of Periyar E.V.R. — Vol. 1, Part 1",
    "anaimuthu-EVRT-Vol-1-Part-2---pp-123-338": "Thoughts of Periyar E.V.R. — Vol. 1, Part 2",
    "kudi-arasu-1925-ocr": "Kudi Arasu — 1925",
    "kudi-arasu-Revolt": "Revolt: A Radical Weekly",
}

os.makedirs("docs", exist_ok=True)
index_links = []

# --- SAFE IN-PAGE SEARCH SCRIPT (NOW WITH TRANSLITERATION) ---
doc_search_script = """
window.addEventListener("DOMContentLoaded", () => {
  const params = new URLSearchParams(window.location.search);
  const term = decodeURIComponent(params.get("highlight") || "");

  // 1. Build the Search UI with the Toggle Button
  const searchBox = document.createElement("div");
  searchBox.className = "search-banner";
  searchBox.innerHTML = `
    <div style="display:flex; justify-content: flex-end; margin-bottom: 8px;">
      <button id="doc-toggle-btn" style="background: transparent; color: #cc0000; border: 1px solid #cc0000; padding: 4px 12px; border-radius: 3px; font-family: sans-serif; font-size: 12px; cursor: pointer; transition: 0.2s;">Keyboard: <strong>தமிழ் (ON)</strong></button>
    </div>
    <div style="display:flex;gap:8px;align-items:center;flex-wrap:wrap;">
      <input id="doc-search" type="text" placeholder="Search: press space for Tamil transliteration..."
        style="flex:1;min-width:200px;padding:6px 10px;background:#2a2a2a;color:#eee;border:1px solid #444;border-radius:3px;font-size:14px;font-family:sans-serif;"
        value="${term}">
      <button id="doc-search-btn" style="padding:6px 14px;background:#cc0000;color:#fff;border:none;border-radius:3px;cursor:pointer;font-size:14px;font-family:sans-serif;">Find</button>
      <span id="match-count" style="font-size:13px;color:#888;font-family:sans-serif;"></span>
    </div>`;
  document.querySelector(".doc-container").insertBefore(searchBox, document.querySelector(".doc-container").firstChild);

  const searchInput = document.getElementById("doc-search");
  const toggleBtn = document.getElementById("doc-toggle-btn");
  const content = document.getElementById("content");

  // 2. Transliteration Logic for In-Page Search
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

  // 3. Highlight Search Execution
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

    const escaped = query.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");
    const regex = new RegExp(`(${escaped})(?![^<]*>)`, "gi");
    content.innerHTML = content.innerHTML.replace(regex, `<mark class="doc-highlight" style="background:#cc0000;color:#fff;border-radius:2px;padding:0 2px;">$1</mark>`);

    const first = content.querySelector(".doc-highlight");
    if (first) first.scrollIntoView({behavior: "smooth", block: "center"});

    const count = content.querySelectorAll(".doc-highlight").length;
    document.getElementById("match-count").textContent = count > 0 ? count + " matches" : "No matches";
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
                            if b[0] < mid_x: left_col.append(b)
                            else: right_col.append(b)
                    
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
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&family=Noto+Serif:wght@400;700&display=swap" rel="stylesheet">
<style>
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
<header><a href="/">&#8592; Home</a><span>Periyar Archive</span></header>
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

with open("docs/index.html", "w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>பெரியார் தேடகம் — Periyar Archive</title>
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
  :root { --pagefind-ui-scale: 1; --pagefind-ui-primary: #cc0000; --pagefind-ui-text: #eee; --pagefind-ui-background: #1e1e1e; --pagefind-ui-border: #444; --pagefind-ui-tag: #222; --pagefind-ui-border-radius: 3px; --pagefind-ui-font: sans-serif; }
  #search { margin-bottom: 20px; }
  .notes { font-family: sans-serif; font-size: 0.85em; color: #aaa; line-height: 1.6; margin-bottom: 8px; }
</style>
</head>
<body>
<header>
  <h1>பெரியார் தேடகம் — Periyar Archive</h1>
  <p style="margin-bottom: 14px;">A full-text searchable archive of Periyar E.V. Ramasamy's writings</p>
  <a href="about.html" style="color: #fff; text-decoration: none; font-size: 13px; font-family: sans-serif; border: 1px solid #555; padding: 5px 14px; border-radius: 3px; display: inline-block;">About the Archive</a>
</header>
<div class="main">
  <p class="description" style="margin-top:28px;">Search across the collected volumes of Periyar's writings.</p>
  <div id="search"></div>
  
  <script src="/pagefind/pagefind-ui.js"></script>
  <script>
    window.addEventListener('DOMContentLoaded', () => {
      // Initialize Pagefind with custom English placeholder
      new PagefindUI({ 
        element: "#search", 
        showImages: false,
        translations: {
          placeholder: "Search: press space for Tamil transliteration..."
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
            toggleBtn.style.cssText = 'background: transparent; color: #cc0000; border: 1px solid #cc0000; padding: 4px 12px; border-radius: 3px; font-family: sans-serif; font-size: 12px; cursor: pointer; transition: 0.2s;';
            
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
</div>
</body>
</html>""")

print("Done generating fresh docs.")