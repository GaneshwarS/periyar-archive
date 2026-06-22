import os
import re
import time
import anthropic
import sys

# --- CONFIGURATION ---
# Securely fetch the API key from the environment to prevent Git exposure
API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
    print("Please run the following command in Git Bash before running this script:")
    print("export ANTHROPIC_API_KEY='your_actual_api_key_here'")
    sys.exit(1)

DOCS_DIR = "corrected"
CHUNK_SIZE = 4000  # Smaller chunks to guarantee Claude doesn't drop text

client = anthropic.Anthropic(api_key=API_KEY)

# Extremely aggressive prompt to prevent Haiku from summarizing
SYSTEM_PROMPT = """Fix OCR errors in Tamil/English text ONLY. DO NOT summarize. DO NOT delete any paragraphs, sentences, or words. You must output the exact same text length, only correcting spelling and punctuation. If you delete text, you fail. Output corrected text only, no commentary."""

def correct_chunk(text):
    """Sends a single chunk to the API."""
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Please correct the OCR errors in this text:\n\n{text}"
            }
        ]
    )
    return response.content[0].text

def get_chunks(text):
    """Splits text into safe sizes without breaking paragraphs."""
    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) > CHUNK_SIZE:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = para
        else:
            current_chunk += "\n\n" + para if current_chunk else para
            
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def process_file(filepath, filename):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        
    # The regex pattern to find the red markers
    pattern = r"<div style='border-left: 4px solid red; padding-left: 10px;'>\s*<!-- RESTORED DROPPED TEXT -->\s*(.*?)\s*<!-- END RESTORED TEXT -->\s*</div>"
    
    blocks_processed = 0
    
    while True:
        # Search for the first red block in the document
        match = re.search(pattern, text, flags=re.DOTALL)
        if not match:
            break # No more red markers found in this file!
            
        full_match_string = match.group(0)
        inner_text = match.group(1).strip()
        
        chunks = get_chunks(inner_text)
        print(f"  Found dropped text block. Splitting into {len(chunks)} chunks for safety...")
        
        corrected_pieces = []
        api_failed = False
        
        for i, chunk in enumerate(chunks):
            print(f"    -> Correcting chunk {i+1}/{len(chunks)}...")
            try:
                corrected_text = correct_chunk(chunk)
                corrected_pieces.append(corrected_text)
                time.sleep(1) # Gentle rate limiting
            except Exception as e:
                print(f"    [!] ERROR on chunk {i+1}: {e}")
                print(f"    [!] Saving partial progress and stopping this file to prevent data loss.")
                api_failed = True
                break
                
        if api_failed:
            # THE FAIL-SAFE: Combine successful chunks, and wrap the remaining uncorrected chunks back in red
            remaining_uncorrected = "\n\n".join(chunks[i:])
            safe_replacement = ""
            
            if corrected_pieces:
                safe_replacement += "\n\n".join(corrected_pieces) + "\n\n"
                
            safe_replacement += f"<div style='border-left: 4px solid red; padding-left: 10px;'>\n<!-- RESTORED DROPPED TEXT -->\n{remaining_uncorrected}\n<!-- END RESTORED TEXT -->\n</div>"
            
            text = text.replace(full_match_string, safe_replacement, 1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            return # Stop processing this file entirely so the user can check the error
            
        else:
            # 100% Success for this block! Replace the whole red box with clean text.
            text = text.replace(full_match_string, "\n\n".join(corrected_pieces), 1)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(text)
            blocks_processed += 1
            print(f"  ✓ Block complete and progress saved to disk!")

    if blocks_processed > 0:
        print(f"Finished {filename}: Cleaned and corrected {blocks_processed} restored blocks.")

# --- MAIN RUNNER ---
print("Scanning for documents with restored text markers...\n")

target_files = sorted([f for f in os.listdir(DOCS_DIR) if f.endswith('.html') and f.startswith('anaimuthu')])

for filename in target_files:
    filepath = os.path.join(DOCS_DIR, filename)
    
    # Quick check if the file actually needs processing before loading it
    with open(filepath, 'r', encoding='utf-8') as f:
        if "<!-- RESTORED DROPPED TEXT -->" not in f.read():
            continue
            
    print(f"\nProcessing: {filename}")
    process_file(filepath, filename)

print("\n\nAll targeted corrections complete! Your files in corrected/ are clean.")