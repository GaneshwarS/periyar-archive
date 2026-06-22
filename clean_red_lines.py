import os
import re

# We target the files in your corrected folder
corrected_dir = "corrected"
target_files = [f for f in os.listdir(corrected_dir) if f.endswith('.html') and f.startswith('anaimuthu')]

count_cleaned = 0

for filename in target_files:
    filepath = os.path.join(corrected_dir, filename)
    
    if not os.path.exists(filepath):
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # This Regex perfectly targets the red wrapper and the comments, 
    # extracting ONLY the text inside (Group 1), completely ignoring spacing issues.
    pattern = r"<div style='border-left: 4px solid red; padding-left: 10px;'>\s*<!-- RESTORED DROPPED TEXT -->\s*(.*?)\s*<!-- END RESTORED TEXT -->\s*</div>"
    
    # Check if there's anything to clean
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, r"\1", text, flags=re.DOTALL)
        count_cleaned += 1
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

print(f"Successfully removed red HTML wrappers from {count_cleaned} files in the 'corrected/' folder!")