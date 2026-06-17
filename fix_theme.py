import os

dirs = ["docs", "corrected"]

old_body = "background: #fff;\n    color: #111;"
new_body = "background: #111;\n    color: #ddd;"

old_banner = 'background:#fff3cd;padding:12px 20px;border-bottom:1px solid #ccc;font-family:sans-serif;font-size:15px;'
new_banner = 'background:#1e1e1e;border-left:3px solid #cc0000;padding:10px 18px;font-family:sans-serif;font-size:14px;color:#aaa;'

old_home = 'text-decoration:none;background:#f0f0f0;padding:6px 14px;border-radius:4px;font-family:sans-serif;font-size:14px;'
new_home = 'text-decoration:none;background:#222;color:#fff;padding:6px 14px;border-radius:4px;font-family:sans-serif;font-size:14px;'

for folder in dirs:
    for filename in os.listdir(folder):
        if filename == "index.html" or not filename.endswith(".html"):
            continue
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace(old_body, new_body)
        content = content.replace(old_banner, new_banner)
        content = content.replace(old_home, new_home)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated: {filepath}")

print("Done.")