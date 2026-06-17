import os
import shutil

corrected_dir = "corrected"
docs_dir = "docs"

if not os.path.exists(corrected_dir):
    print("No corrected/ folder found. Nothing to restore.")
else:
    files = [f for f in os.listdir(corrected_dir) if f.endswith(".html") and f != "index.html"]
    if not files:
        print("No corrected HTML files found.")
    else:
        for filename in files:
            src = os.path.join(corrected_dir, filename)
            dst = os.path.join(docs_dir, filename)
            shutil.copy2(src, dst)
            print(f"Restored: {filename}")
        print(f"\nDone. {len(files)} files restored from corrected/ to docs/")