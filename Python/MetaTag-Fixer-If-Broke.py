import os
import re

root_dir = r"c:\xampp\htdocs\Enlightenment"
default_description = "Learn web design fundamentals in this tutorial."

def fix_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()

    original = content
    content_no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    has_head = bool(re.search(r'<head[^>]*>', content, re.IGNORECASE))
    has_meta = '<meta name="description"' in content_no_comments

    if not has_head:
        # Insert full <head> section before <body>
        head_block = f"""<head>
    <meta charset="UTF-8">
    <meta name="description" content="{default_description}">
    <title>Untitled</title>
</head>"""
        content = re.sub(r'<body[^>]*>', head_block + r'\n<body', content, flags=re.IGNORECASE)
        status = "🧱 Added <head> with meta"
    elif not has_meta:
        # Insert meta tag inside existing <head>
        content = re.sub(r'(<head[^>]*>)', r'\1\n    <meta name="description" content="' + default_description + '">', content, flags=re.IGNORECASE)
        status = "🔧 Inserted meta tag"
    else:
        status = "✅ Already has meta tag"

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

    return status

def fix_all_html(root_dir):
    print("🛠️ Starting meta tag fixer...\n")
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                result = fix_file(file_path)
                print(f"{result} — {file_path}")

# 🚀 Run the fixer
fix_all_html(root_dir)