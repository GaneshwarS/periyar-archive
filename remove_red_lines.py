import os
import re

# --- CONFIGURATION ---
SOURCE_DIR = "final_merged"
TARGET_DIR = "corrected"

def clean_archive():
    print("Starting raw text extraction (No AI involved)...\n")
    
    # Create the target folder if it doesn't exist
    os.makedirs(TARGET_DIR, exist_ok=True)
    target_files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith('.html')])
    
    # Regex patterns to find the red boxes and grab the text inside them
    # Pattern 1 looks for the standard tag
    pattern_standard = r"<div style='border-left: 4px solid red; padding-left: 10px;'>\s*<!-- RESTORED DROPPED TEXT -->\s*(.*?)\s*<!-- END RESTORED TEXT -->\s*</div>"
    
    # Pattern 2 looks for the "skipped" tag we added earlier to Anaimuthu Volume 1 Part 4
    pattern_skipped = r"<div style='border-left: 4px solid red; padding-left: 10px;'>\s*<!-- SKIPPED BY AI -->\s*(.*?)\s*<!-- END RESTORED TEXT -->\s*</div>"
    
    files_processed = 0

    for filename in target_files:
        source_path = os.path.join(SOURCE_DIR, filename)
        target_path = os.path.join(TARGET_DIR, filename)
        
        # Read the original safe file
        with open(source_path, 'r', encoding='utf-8') as f:
            text = f.read()
        
        # re.sub with r'\1' replaces the entire red box with ONLY the text captured inside it
        clean_text = re.sub(pattern_standard, r'\1', text, flags=re.DOTALL)
        clean_text = re.sub(pattern_skipped, r'\1', clean_text, flags=re.DOTALL)
        
        # Save the cleaned text to the target directory
        with open(target_path, 'w', encoding='utf-8') as f:
            f.write(clean_text)
            
        files_processed += 1
        print(f"  ✓ Cleaned and copied: {filename}")
        
    print(f"\nAll {files_processed} files successfully processed!")
    print("Your text is safely merged in the 'corrected' folder with all red lines removed.")

if __name__ == "__main__":
    clean_archive()