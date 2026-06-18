import os

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

for folder in ["docs", "corrected"]:
    for filename in os.listdir(folder):
        if filename == "index.html" or not filename.endswith(".html"):
            continue
        key = filename.replace(".html", "")
        if key not in title_map:
            print(f"No title mapping for: {filename}")
            continue
        display_title = title_map[key]
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # Replace <h1> content
        import re
        content = re.sub(r'<h1[^>]*>.*?</h1>', f'<h1>{display_title}</h1>', content, flags=re.DOTALL)
        # Replace <title> content
        content = re.sub(r'<title>.*?</title>', f'<title>{display_title} — Periyar Archive</title>', content, flags=re.DOTALL)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filename}")

print("Done.")