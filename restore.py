import os

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
            corr_path = os.path.join(corrected_dir, filename)
            doc_path = os.path.join(docs_dir, filename)

            if not os.path.exists(doc_path):
                continue

            # Read your manual typo corrections
            with open(corr_path, "r", encoding="utf-8") as f:
                corr_html = f.read()

            # Read the fresh, perfectly coded layout
            with open(doc_path, "r", encoding="utf-8") as f:
                doc_html = f.read()

            # Isolate the exact text block from both files
            corr_start = corr_html.find('<div id="content">')
            doc_start = doc_html.find('<div id="content">')

            if corr_start != -1 and doc_start != -1:
                # Grab your typo-corrected text block
                content_to_keep = corr_html[corr_start + 18 : corr_html.find('</div>', corr_start + 18)]
                
                # Stitch your text into the perfect layout
                new_doc = doc_html[:doc_start + 18] + content_to_keep + "\n</div>\n</div>\n</body>\n</html>"

                # Save it to docs/
                with open(doc_path, "w", encoding="utf-8") as f:
                    f.write(new_doc)
                print(f"Merged typo fixes into fresh layout: {filename}")

        print(f"\nDone. Typo fixes securely merged without breaking code.")