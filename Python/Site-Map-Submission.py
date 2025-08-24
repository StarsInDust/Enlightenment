import requests
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Your sitemap URL
sitemap_url = "https://starsindust.github.io/Enlightenment/sitemap.xml"

# Submit to Bing
bing_ping = f"https://www.bing.com/webmaster/ping.aspx?siteMap={sitemap_url}"
bing_response = requests.get(bing_ping)
print("Bing response:", bing_response.status_code)

# Submit to Google (requires credentials setup)
SCOPES = ['https://www.googleapis.com/auth/webmasters']
credentials = ServiceAccountCredentials.from_json_keyfile_name('your-credentials.json', SCOPES)
webmasters_service = build('webmasters', 'v3', credentials=credentials)

site_url = "https://starsindust.github.io/Enlightenment/"
response = webmasters_service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
print("Google response:", response)