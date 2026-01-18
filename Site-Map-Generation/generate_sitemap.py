import os
from datetime import datetime

# === CONFIGURATION ===
site_folder = "C:/xampp/htdocs/Enlightenment"  # Adjust if needed
base_url = "https://starsindust.github.io/Enlightenment"
output_folder = "./sitemapBackup"  # Optional subfolder to store generated sitemaps

# === TIMESTAMP ===
today = datetime.today().strftime("%Y-%m-%d")
output_filename = f"sitemap-{today}.xml"
output_path = os.path.join(output_folder, output_filename)

# === Ensure output folder exists ===
os.makedirs(output_folder, exist_ok=True)

# === Collect URLs ===
sitemap_entries = []

for root, dirs, files in os.walk(site_folder):
    for file in files:
        if file.endswith(".html"):
            rel_path = os.path.relpath(os.path.join(root, file), site_folder)
            url = f"{base_url}/{rel_path.replace(os.sep, '/')}"
            sitemap_entries.append(f"  <url>\n    <loc>{url}</loc>\n  </url>")

# === Build XML ===
sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{chr(10).join(sitemap_entries)}
</urlset>
"""

# === Save File ===
# Save timestamped backup
with open(output_path, "w", encoding="utf-8") as f:
    f.write(sitemap)

# Save main sitemap.xml to site root
main_sitemap_path = os.path.join(site_folder, "sitemap.xml")
with open(main_sitemap_path, "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Sitemap generated: {output_path}")
print(f"Main sitemap updated: {main_sitemap_path}")