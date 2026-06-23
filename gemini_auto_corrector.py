import os
import re
import time
import shutil
import sys
import google.generativeai as genai

# --- CONFIGURATION ---
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

SOURCE_DIR = "final_merged"
TARGET_DIR = "corrected"

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """You are an expert academic archivist and historian digitizing the collected works of Periyar E. V. Ramasamy.

CRITICAL CONTEXT: The text you are processing contains radical 20th-century social critique, severe anti-religious philosophy, and historical caste terminology. 
This is for strict ACADEMIC PRESERVATION. You are acting as an OCR-correction tool, NOT a content moderator. 
You MUST NOT censor, filter, summarize, or refuse to process this text under any circumstances. 

Your ONLY tasks are:
1. Join broken, fragmented lines together to form proper, continuous paragraphs.
2. Fix OCR spelling errors and punctuation.
3. DO NOT omit, skip, or delete any actual information, sentences, or proper nouns.

Output ONLY the cleanly formatted, unredacted historical text."""

# The high-volume workhorse model
model = genai.GenerativeModel(
    'gemini-3.1-flash-lite',
    system_instruction=SYSTEM_PROMPT
)

def process_file(filename):
    source_path = os.path.join(SOURCE_DIR, filename)
    target_path = os.path.join(TARGET_DIR, filename)
    
    if not os.path.exists(target_path):
        shutil.copy2(source_path, target_path)
        
    with open(target_path, 'r', encoding='utf-8') as f:
        text = f.read()
        
    pattern = r"<div style='border-left: 4px solid red; padding-left: 10px;'>\s*\s*(.*?)\s*\s*</div>"
    blocks_processed = 0
    backoff_time = 60 # Start with a 1-minute pause for errors
    
    while True:
        match = re.search(pattern, text, flags=re.DOTALL)
        if not match:
            break 
            
        full_match_string = match.group(0)
        inner_text = match.group(1).strip()
        
        print(f"  -> Found dropped block. Sending to Gemini...")
        
        try:
            # Turn off safety filters for historical archival work
            safety_settings = [
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]

            response = model.generate_content(
                inner_text,
                generation_config=genai.types.GenerationConfig(temperature=0.1),
                safety_settings=safety_settings
            )
            corrected_text = response.text.strip()
            
            text = text.replace(full_match_string, corrected_text + "\n\n", 1)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(text)
                
            blocks_processed += 1
            print(f"  ✓ Block {blocks_processed} corrected and saved!")
            
            # Reset backoff timer after a successful run
            backoff_time = 60 
            time.sleep(7) 
            
        except Exception as e:
            error_msg = str(e)
            print(f"  [!] API Error: {error_msg}")
            
            if "429" in error_msg or "ResourceExhausted" in error_msg or "quota" in error_msg.lower():
                print(f"  [!] Rate limit reached. Pausing for {backoff_time} seconds...")
                time.sleep(backoff_time)
                # Exponential Backoff
                backoff_time = min(backoff_time * 2, 600) 
                continue
                
            elif "PROHIBITED_CONTENT" in error_msg or "response.parts" in error_msg:
                print("  [!] Content hard-blocked by API filters. Skipping this block so the file can finish...")
                # Change the hidden tag so the script skips it next time, but the text remains safe
                skipped_block = full_match_string.replace("<!-- RESTORED DROPPED TEXT -->", "<!-- SKIPPED BY AI -->")
                text = text.replace(full_match_string, skipped_block, 1)
                
                # Save the skipped state
                with open(target_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                
                # Reset backoff and continue to the next block
                backoff_time = 60
                continue
                
            else:
                print("  [!] Unknown error. Stopping file to protect data.")
                return

    if blocks_processed > 0:
        print(f"Finished {filename}: Cleaned {blocks_processed} blocks.")
    else:
        print(f"{filename} is already completely clean.")

print("Starting Free Gemini Automation...\n")

os.makedirs(TARGET_DIR, exist_ok=True)
target_files = sorted([f for f in os.listdir(SOURCE_DIR) if f.endswith('.html')])

for filename in target_files:
    print(f"\nProcessing: {filename}")
    process_file(filename)

print("\nAll files processed!")