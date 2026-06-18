import os

corrected_dir = "corrected"

old_code = 'content.innerHTML = content.innerHTML.replace(/<mark class="doc-highlight">(.*?)<\\/mark>/g, "$1");'

new_code = """const marks = content.querySelectorAll('mark.doc-highlight');
    marks.forEach(mark => {
        const parent = mark.parentNode;
        parent.replaceChild(document.createTextNode(mark.textContent), mark);
        parent.normalize();
    });"""

count = 0
if os.path.exists(corrected_dir):
    for filename in os.listdir(corrected_dir):
        if filename.endswith(".html"):
            filepath = os.path.join(corrected_dir, filename)
            
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
                
            if old_code in content:
                content = content.replace(old_code, new_code)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                print(f"Fixed: {filename}")
                count += 1

print(f"\nDone! Fixed {count} files.")