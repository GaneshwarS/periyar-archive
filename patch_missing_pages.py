import os
import difflib
import re

# --- FOLDER SETUP ---
backup_dir = "ocr_backup"      
corrected_dir = "docs"    
output_dir = "final_merged"    

os.makedirs(output_dir, exist_ok=True)

# Automatically find all HTML files in the backup directory
target_files = [f for f in os.listdir(backup_dir) if f.endswith('.html')]

def clean_word(w):
    """Strips punctuation and lowercases for highly accurate word matching"""
    return re.sub(r'[^\w]', '', w.lower())

for filename in target_files:
    backup_path = os.path.join(backup_dir, filename)
    corrected_path = os.path.join(corrected_dir, filename)
    output_path = os.path.join(output_dir, filename)
    
    if not os.path.exists(corrected_path):
        print(f"Skipping {filename} - No corrected file found in '{corrected_dir}'.")
        continue
        
    print(f"\nProcessing: {filename}")
    print("Aligning documents at the word-level... (This may take 5-15 seconds)")
    
    with open(backup_path, 'r', encoding='utf-8') as f:
        b_text = f.read()
    with open(corrected_path, 'r', encoding='utf-8') as f:
        c_text = f.read()
        
    # Extract all words and their exact character positions in the original strings
    b_matches = list(re.finditer(r'\S+', b_text))
    c_matches = list(re.finditer(r'\S+', c_text))
    
    # Create clean lists of words for the matching algorithm
    b_words = [clean_word(m.group()) for m in b_matches]
    c_words = [clean_word(m.group()) for m in c_matches]
    
    # Use SequenceMatcher to find contiguous blocks of identical words
    # autojunk=False ensures it doesn't ignore common words, making it ultra-precise
    sm = difflib.SequenceMatcher(None, b_words, c_words, autojunk=False)
    blocks = sm.get_matching_blocks()
    
    final_string = ""
    last_b_word_idx = 0
    last_c_word_idx = 0
    patched_count = 0
    
    for block in blocks:
        match_b_start, match_c_start, match_len = block
        
        # 1. Append Claude's gap (Corrections, summaries, or spacing before the match)
        if match_c_start > last_c_word_idx:
            c_gap_start = c_matches[last_c_word_idx - 1].end() if last_c_word_idx > 0 else 0
            c_gap_end = c_matches[match_c_start].start()
            if c_gap_end > c_gap_start:
                final_string += c_text[c_gap_start:c_gap_end]
                
        # 2. Check for a Dropped Page in Backup
        b_gap_words = match_b_start - last_b_word_idx
        c_gap_words = match_c_start - last_c_word_idx
        
        # If Claude skipped more than 20 words that existed in the backup
        if b_gap_words > 20 and (b_gap_words - c_gap_words > 15):
            b_gap_start = b_matches[last_b_word_idx - 1].end() if last_b_word_idx > 0 else 0
            b_gap_end = b_matches[match_b_start].start()
            
            dropped_text = b_text[b_gap_start:b_gap_end].strip()
            
            # Wrap the rescued text in clear markers so you can find it easily
            final_string += f"\n\n<div style='border-left: 4px solid red; padding-left: 10px;'>\n"
            final_string += f"<!-- RESTORED DROPPED TEXT -->\n{dropped_text}\n<!-- END RESTORED TEXT -->\n"
            final_string += f"</div>\n\n"
            patched_count += 1
            
        # 3. Append the Matched Claude Text
        if match_len > 0:
            match_start_char = c_matches[match_c_start].start()
            match_end_idx = match_c_start + match_len
            match_end_char = c_matches[match_end_idx - 1].end()
            
            # If this is the very first match, we need to handle the preceding whitespace carefully
            if last_c_word_idx == 0 and match_c_start == 0:
                match_start_char = 0
                
            final_string += c_text[match_start_char:match_end_char]
            
        last_b_word_idx = match_b_start + match_len
        last_c_word_idx = match_c_start + match_len
        
    # Append any remaining text Claude added at the very end
    if last_c_word_idx < len(c_matches):
        c_gap_start = c_matches[last_c_word_idx - 1].end() if last_c_word_idx > 0 else 0
        final_string += c_text[c_gap_start:]
        
    # Final cleanup to prevent excessive blank lines
    final_string = re.sub(r'\n{4,}', '\n\n', final_string)
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_string)
        
    print(f"  -> Successfully detected and patched {patched_count} massive text drops!")

print("\nDone! All files processed successfully. Check the 'final_merged' folder.")