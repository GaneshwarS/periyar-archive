import os
import anthropic

API_KEY = "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"
client = anthropic.Anthropic(api_key=API_KEY)

# Test on just the Revolt file (English, easy to verify)
with open("docs/kudi-arasu-1931-1-ocr.html", "r", encoding="utf-8") as f:
    html = f.read()

start_marker = '<div id="content">'
end_marker = '</div>\n</div>\n</body>'
start = html.find(start_marker)
end = html.find(end_marker)
content = html[start + len(start_marker):end]

# Just test the first 3000 characters
test_chunk = content[60000:70000]

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=4096,
    system="""You are a specialist in correcting OCR errors in Tamil and English text. 
Fix wrong characters, unnecessary line breaks, and broken paragraph structure.
Preserve meaning exactly. Output only corrected text, no commentary.""",
    messages=[{"role": "user", "content": f"Correct OCR errors:\n\n{test_chunk}"}]
)

print("ORIGINAL:")
print(test_chunk[:500])
print("\nCORRECTED:")
print(response.content[0].text[:500])