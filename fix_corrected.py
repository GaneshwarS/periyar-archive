import os
import re

corrected_dir = "corrected"

for filename in os.listdir(corrected_dir):
    if not filename.endswith(".html") or filename in ["index.html", "about.html"]:
        continue
    filepath = os.path.join(corrected_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find the content div
    content_start = content.find('<div id="content">')
    if content_start == -1:
        print(f"No content div found in {filename}")
        continue
    
    # Find the first </div> after content start
    content_end = content.find('</div>', content_start + 18)
    if content_end == -1:
        print(f"No closing div found in {filename}")
        continue
    
    # Keep only up to and including the closing content div
    truncated = content[:content_end + 6]
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(truncated)
    print(f"Fixed: {filename}")

print("Done.")