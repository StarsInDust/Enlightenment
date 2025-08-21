import os
import re

# 🔧 Root directory containing year folders
root_dir = r"c:\xampp\htdocs\Enlightenment"


# ✅ Toggle to skip files that already have meta tags
skip_if_meta_exists = True

def generate_meta_tags(title, keywords, year):
    description = f"{title} tutorial ({year}) with clear steps and practical examples."
    return f"""
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://yourdomain.com/images/{title.lower().replace(' ', '-')}-preview.png">
    <meta property="og:url" content="https://yourdomain.com/{year}/{title.lower().replace(' ', '-')}.html">
    """

def inject_meta_tags(file_path, year):
    print(f"Processing: {file_path}")  # ✅ Good placement

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Diagnostic check for actual meta tag presence
    if skip_if_meta_exists and '<meta name="description"' in content:
        print(f"Skipped (already has meta): {file_path}")
    else:
        print(f"No meta tag found in: {file_path} — injecting now")

        return

    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(file_path))[0].replace('-', ' ').title()
    keywords = ', '.join(title.lower().split())
    meta_block = generate_meta_tags(title, keywords, year)

    if "<head>" in content:
        content = re.sub(r'(<head[^>]*>)', r'\1\n' + meta_block, content, count=1)
    else:
        content = f"<html>\n<head>\n{meta_block}\n</head>\n<body>\n{content}\n</body>\n</html>"

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Updated: {file_path}")

def batch_inject_all_years(root_dir):
    for folder_name in os.listdir(root_dir):
        folder_path = os.path.join(root_dir, folder_name)
        if os.path.isdir(folder_path) and folder_name.isdigit():
            year = folder_name
            for root, _, files in os.walk(folder_path):
                for file in files:
                    if file.endswith('.html'):
                        inject_meta_tags(os.path.join(root, file), year)

# 🚀 Run it
batch_inject_all_years(root_dir)
print("Meta tag injection across all years completed!")