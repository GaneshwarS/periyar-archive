import os

# Define the three folders
folders = {
    "Original": "ocr_backup",
    "API Corrected": "docs", # Or "corrected" if that's where your API files are currently sitting
    "Final Merged": "final_merged"
}

# Get all HTML files from the backup directory that start with 'anaimuthu'
target_files = sorted([f for f in os.listdir(folders["Original"]) if f.endswith('.html') and f.startswith('anaimuthu')])

def get_char_count(filepath):
    """Returns the character count of a file, or 'N/A' if missing."""
    if not os.path.exists(filepath):
        return "N/A"
    with open(filepath, 'r', encoding='utf-8') as f:
        return len(f.read())

# Print the table header
print(f"\n{'Filename':<60} | {'Original':<10} | {'API':<10} | {'Merged':<10}")
print("-" * 98)

# Print the counts for each file
for filename in target_files:
    counts = {}
    for label, folder in folders.items():
        filepath = os.path.join(folder, filename)
        counts[label] = get_char_count(filepath)
    
    # Format the numbers with commas for readability (if they are integers)
    orig_str = f"{counts['Original']:,}" if isinstance(counts['Original'], int) else counts['Original']
    api_str = f"{counts['API Corrected']:,}" if isinstance(counts['API Corrected'], int) else counts['API Corrected']
    merged_str = f"{counts['Final Merged']:,}" if isinstance(counts['Final Merged'], int) else counts['Final Merged']
    
    print(f"{filename:<60} | {orig_str:<10} | {api_str:<10} | {merged_str:<10}")

print("\n")