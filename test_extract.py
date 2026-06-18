import fitz
import os

pdf_path = "E:\Read\Books\Periyar\Anaimuthu Volumes\OCR-ed\EVRT Vol 1 Part 1 - pp 0-122.pdf"

doc = fitz.open(pdf_path)
full_text = ""

for page in doc:
    blocks = page.get_text("blocks")
    blocks = sorted(blocks, key=lambda b: (b[1], b[0]))  # sort by y then x position
    for block in blocks:
        block_text = block[4].strip()
        if block_text:
            full_text += block_text + "\n\n"

doc.close()

safe_text = full_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

html = f"""<!DOCTYPE html>
<html lang="ta">
<head>
<meta charset="UTF-8">
<title>Test Extract — Vol. 1, Part 1</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Serif+Tamil:wght@400;700&family=Noto+Serif:wght@400;700&display=swap" rel="stylesheet">
<style>
  body {{ font-family: 'Noto Serif Tamil', 'Noto Serif', serif; background: #111; color: #ddd; max-width: 780px; margin: 40px auto; padding: 0 48px 80px; line-height: 1.9; }}
</style>
</head>
<body>
<h1>Test: Thoughts of Periyar E.V.R. — Vol. 1, Part 1</h1>
<p style="color:#777;font-family:sans-serif;margin-bottom:30px;">Block mode extraction test</p>
<div id="content" style="white-space: pre-wrap;">{safe_text}</div>
</body>
</html>"""

with open("test_output.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Done. Open test_output.html in your browser to compare.")