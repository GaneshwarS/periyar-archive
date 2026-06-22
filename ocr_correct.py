import os
import re
import time
import anthropic

# --- CONFIGURATION ---
API_KEY = "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"  
DOCS_DIR = "docs"
BACKUP_DIR = "ocr_backup"
CHUNK_SIZE = 20000  # characters per API call

client = anthropic.Anthropic(api_key=API_KEY)

SYSTEM_PROMPT = """Fix OCR errors in Tamil/English text: correct wrong characters, join broken lines into proper paragraphs, fix punctuation. Preserve meaning, proper nouns, and intentional paragraph breaks. Output corrected text only, no commentary."""

def correct_chunk(text, chunk_num, total_chunks, filename):
    print(f"  Correcting chunk {chunk_num}/{total_chunks}...")
    try:
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
    except Exception as e:
        print(f"  ERROR on chunk {chunk_num}: {e}")
        return text  # Return original if error

def process_file(filepath, filename):
    print(f"\nProcessing: {filename}")
    
    with open(filepath, "r", encoding="utf-8") as f:
        html = f.read()
    
    # Extract text content between content div tags
    start_marker = '<div id="content">'
    end_marker = '</div>\n</div>\n</body>'
    
    start = html.find(start_marker)
    end = html.find(end_marker)
    
    if start == -1 or end == -1:
        print(f"  Could not find content markers in {filename}, skipping.")
        return
    
    content_start = start + len(start_marker)
    original_content = html[content_start:end]
    
    # Split into chunks at paragraph boundaries
    paragraphs = original_content.split("\n\n")
    chunks = []
    current_chunk = ""
    
    for para in paragraphs:
        if len(current_chunk) + len(para) > CHUNK_SIZE:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para
        else:
            current_chunk += "\n\n" + para if current_chunk else para
    
    if current_chunk:
        chunks.append(current_chunk)
    
    print(f"  Split into {len(chunks)} chunks")
    
    # Process each chunk
    corrected_chunks = []
    for i, chunk in enumerate(chunks):
        corrected = correct_chunk(chunk, i+1, len(chunks), filename)
        corrected_chunks.append(corrected)
        time.sleep(1)  # Rate limiting
    
    corrected_content = "\n\n".join(corrected_chunks)
    
    # Reassemble HTML
    new_html = html[:content_start] + corrected_content + html[end:]
    
    # Save backup
    backup_path = os.path.join(BACKUP_DIR, filename)
    with open(backup_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    # Save corrected file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_html)
    
    print(f"  Done: {filename}")

# --- MAIN ---
os.makedirs(BACKUP_DIR, exist_ok=True)

# Install anthropic if needed
try:
    import anthropic
except ImportError:
    os.system("pip install anthropic --break-system-packages")
    import anthropic

# Get list of files to process
files = [f for f in sorted(os.listdir(DOCS_DIR)) 
         if f.endswith(".html") 
         and f != "index.html" 
         and f != "about.html"
         and f.startswith("anaimuthu")
         and f not in os.listdir(BACKUP_DIR)]

print(f"Found {len(files)} files to process")
print("Starting OCR correction...\n")

for filename in files:
    filepath = os.path.join(DOCS_DIR, filename)
    process_file(filepath, filename)
    time.sleep(2)  # Pause between files

print("\n\nAll done! Corrected files are in docs/")
print("Original files backed up in ocr_backup/")
print("\nNext steps:")
print("1. Check a few files to verify quality")
print("2. Run: pagefind --site docs")
print("3. Run: git add . && git commit -m 'OCR corrections' && git push origin main")