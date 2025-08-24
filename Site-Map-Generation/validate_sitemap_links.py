import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

# === CONFIGURATION ===
sitemap_folder = "./sitemaps"
log_file = "sitemap_log.txt"

# === Find the latest sitemap file ===
sitemaps = sorted([f for f in os.listdir(sitemap_folder) if f.startswith("sitemap-") and f.endswith(".xml")])
if not sitemaps:
    print("No sitemap files found.")
    exit()

latest_sitemap = os.path.join(sitemap_folder, sitemaps[-1])
print(f"Validating: {latest_sitemap}")

# === Parse sitemap XML ===
tree = ET.parse(latest_sitemap)
root = tree.getroot()
namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
urls = [url.find("ns:loc", namespace).text for url in root.findall("ns:url", namespace)]

# === Validate URLs ===
broken_links = []
for url in urls:
    try:
        response = requests.head(url, timeout=10)
        if response.status_code >= 400:
            broken_links.append((url, response.status_code))
    except requests.RequestException as e:
        broken_links.append((url, str(e)))

# === Log results ===
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(log_file, "a", encoding="utf-8") as log:
    log.write(f"\n--- Validation Run: {timestamp} ---\n")
    log.write(f"Checked {len(urls)} URLs\n")
    if broken_links:
        log.write(f"Found {len(broken_links)} broken links:\n")
        for url, error in broken_links:
            log.write(f"  {url} → {error}\n")
    else:
        log.write("No broken links found.\n")

print(f"Validation complete. Results saved to {log_file}")