import os
import re

# 🔧 Root directory of your tutorials
root_dir = r"c:\xampp\htdocs\Enlightenment"

def analyze_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    # Remove HTML comments to avoid false positives
    content_no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    has_head = bool(re.search(r'<head[^>]*>', content, re.IGNORECASE))
    has_meta = '<meta name="description"' in content_no_comments

    if not has_head:
        return "❌ No <head> tag"
    elif has_meta:
        return "✅ Meta tag present"
    elif '<meta name="description"' in content:
        return "⚠️ Meta tag is commented out"
    else:
        return "❌ Missing meta tag"

def validate_all_html(root_dir):
    print("🔍 Starting meta tag validation...\n")
    for root, _, files in os.walk(root_dir):  # ← walks everything recursively
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                result = analyze_file(file_path)
                print(f"{result} — {file_path}")

# 🚀 Run the validator
validate_all_html(root_dir)