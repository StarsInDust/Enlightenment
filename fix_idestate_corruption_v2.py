import os
import re

# Define the root directory of your website
root_dir = r"C:\xampp\htdocs\Enlightenment"

print("=" * 70)
print("IDESTATE CORRUPTION CLEANUP SCRIPT")
print("=" * 70)
print(f"\nScanning directory: {root_dir}")
print("\nLooking for corrupted files...\n")

cleaned_count = 0
total_html_files = 0
corrupted_files = []

# Walk through all files
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if file.endswith('.html'):
            total_html_files += 1
            file_path = os.path.join(root, file)
            
            try:
                # Read the file
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check if corrupted
                if '# IDESTATE CONTEXT' in content or 'IDESTATE CONTEXT' in content:
                    print(f"FOUND CORRUPTION: {file}")
                    corrupted_files.append(file_path)
                    
                    # Find where the corruption starts
                    start_pos = content.find('# IDESTATE CONTEXT')
                    if start_pos == -1:
                        start_pos = content.find('IDESTATE CONTEXT')
                    
                    # Remove everything from corruption to the next HTML tag
                    if start_pos != -1:
                        # Find the next DOCTYPE or html tag
                        next_tag = content.find('<!DOCTYPE', start_pos)
                        if next_tag == -1:
                            next_tag = content.find('<html', start_pos)
                        if next_tag == -1:
                            next_tag = content.find('</head>', start_pos)
                        
                        if next_tag != -1:
                            # Remove the corrupted section
                            cleaned_content = content[:start_pos] + content[next_tag:]
                        else:
                            # Just remove from corruption to end
                            cleaned_content = content[:start_pos]
                        
                        # Write back
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(cleaned_content)
                        
                        cleaned_count += 1
                        print(f"  -> CLEANED!\n")
            
            except Exception as e:
                print(f"ERROR reading {file}: {e}\n")

print("=" * 70)
print(f"RESULTS:")
print(f"  Total HTML files scanned: {total_html_files}")
print(f"  Corrupted files found: {len(corrupted_files)}")
print(f"  Files cleaned: {cleaned_count}")
print("=" * 70)

if cleaned_count > 0:
    print("\nCLEANED FILES:")
    for f in corrupted_files:
        print(f"  - {f}")
    print("\nSUCCESS! Files have been cleaned.")
    print("You can now try committing to Git.")
else:
    print("\nNo corrupted files found.")

print("\nPress Enter to exit...")
input()