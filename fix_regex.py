import os

for folder in ["docs", "corrected"]:
    for filename in os.listdir(folder):
        if not filename.endswith(".html") or filename in ["index.html", "about.html"]:
            continue
        filepath = os.path.join(folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        if '`(${escaped})`' in content:
            content = content.replace(
                'const regex = new RegExp(`(${escaped})`, "gi");',
                'const regex = new RegExp("(" + escaped + ")", "gi");'
            )
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {filepath}")
        elif 'new RegExp(escaped' in content:
            content = content.replace(
                'const regex = new RegExp(escaped, "gi");',
                'const regex = new RegExp("(" + escaped + ")", "gi");'
            )
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Fixed: {filepath}")
        else:
            print(f"Already correct: {filename}")

print("Done.")