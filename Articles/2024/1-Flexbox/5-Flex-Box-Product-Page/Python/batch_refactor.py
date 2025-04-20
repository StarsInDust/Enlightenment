import os
import re

# Define the directory containing your HTML files
directory = r"c:\xampp\htdocs\Enlightenment"

# Define the replacements
replacements = {
    'class="MsoToc1"': 'class="tableOfContents"',  # Replace MsoToc1 with tableOfContents
    r'<p class="MsoNormal">&nbsp;</p>': '',        # Remove empty <p> tags
}

def refactor_html(file_path):
    """Refactor a single HTML file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Apply replacements
    for old, new in replacements.items():
        content = re.sub(old, new, content)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def batch_refactor(directory):
    """Batch refactor all HTML files in the directory."""
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                print(f"Refactoring: {file_path}")
                refactor_html(file_path)

# Run the batch refactoring
batch_refactor(directory)
print("Batch refactoring completed!")