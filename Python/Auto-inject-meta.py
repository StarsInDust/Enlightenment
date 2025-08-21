import os
import re

# 🔧 Set your tutorial folder path
directory = r"c:\xampp\htdocs\Enlightenment\2025"

def generate_meta_tags(title, keywords):
    """Create a meta tag block based on title and keywords."""
    description = f"{title} tutorial with clear steps and practical examples."
    return f"""
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="https://yourdomain.com/images/{title.lower().replace(' ', '-')}-preview.png">
    <meta property="og:url" content="https://yourdomain.com/tutorials/{title.lower().replace(' ', '-')}.html">
    """

def inject_meta_tags(file_path):
    """Inject meta tags into the <head> of an HTML file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Extract title from <h1> or filename
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    title = title_match.group(1).strip() if title_match else os.path.splitext(os.path.basename(file_path))[0].replace('-', ' ').title()

    # Generate keywords (basic version)
    keywords = ', '.join(title.lower().split())

    # Create meta tag block
    meta_block = generate_meta_tags(title, keywords)

    # Inject into <head>
    if "<head>" in content:
        content = re.sub(r'(<head[^>]*>)', r'\1\n' + meta_block, content, count=1)
    else:
        # If no <head>, wrap content with basic HTML structure
        content = f"<html>\n<head>\n{meta_block}\n</head>\n<body>\n{content}\n</body>\n</html>"

    # Save updated file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Updated meta tags in: {file_path}")

def batch_inject(directory):
    """Process all HTML files in the directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                inject_meta_tags(os.path.join(root, file))

# 🚀 Run the batch injection
batch_inject(directory)
print("Meta tag injection completed!")