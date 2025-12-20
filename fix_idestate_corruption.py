import os
import re

# Define the root directory of your website
root_dir = r"C:\xampp\htdocs\Enlightenment"

# The corrupted text pattern to remove
corrupted_pattern = r'# IDESTATE CONTEXT.*?(?=<!DOCTYPE|<html|$)'

def clean_file(file_path):
    """Remove IDESTATE corruption from a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if the file contains the corrupted text
        if '# IDESTATE CONTEXT' in content:
            # Remove the corrupted section
            cleaned_content = re.sub(corrupted_pattern, '', content, flags=re.DOTALL)
            
            # Write the cleaned content back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            return True  # File was cleaned
        return False  # File didn't need cleaning
    
    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")
        return False

def scan_and_clean(root_dir):
    """Scan all HTML files and clean them."""
    print("🔍 Scanning for corrupted files...\n")
    
    cleaned_count = 0
    total_html_files = 0
    
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.html'):
                total_html_files += 1
                file_path = os.path.join(root, file)
                
                if clean_file(file_path):
                    cleaned_count += 1
                    print(f"✅ CLEANED: {file_path}")
    
    print(f"\n{'='*60}")
    print(f"📊 SUMMARY:")
    print(f"   Total HTML files scanned: {total_html_files}")
    print(f"   Files cleaned: {cleaned_count}")
    print(f"{'='*60}")
    
    if cleaned_count > 0:
        print("\n✨ Success! Your files have been cleaned.")
        print("   You can now try committing to Git again.")
    else:
        print("\n✨ No corrupted files found!")

# Run the cleanup
if __name__ == "__main__":
    print("🛠️  IDESTATE Corruption Cleanup Script")
    print("="*60)
    scan_and_clean(root_dir)
    input("\nPress Enter to exit...")