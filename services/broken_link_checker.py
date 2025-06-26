import asyncio
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin

class LinkChecker:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.broken_links = []

    async def fetch_html(self, session, url):
        try:
            async with session.get(url, timeout=10) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            print(f"[ERROR] Failed to fetch HTML from {url}: {e}")
            return ""

    def extract_links(self, base_url, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Remove header, footer, nav, aside
        for tag in soup.select("header, footer, nav, aside"):
            tag.decompose()

        links = set()
        for tag in soup.find_all('a', href=True):
            href = tag['href']
            full_url = urljoin(base_url, href)
            if full_url.startswith('http'):
                links.add(full_url)

        return links

    async def check_link(self, session, url):
        try:
            async with session.head(url, allow_redirects=True, timeout=10) as response:
                if response.status >= 400:
                    print(f"[BROKEN] {url} - Status: {response.status}")
                    return (url, response.status)
                else:
                    print(f"[OK]     {url} - Status: {response.status}")
                    return None
        except Exception as e:
            print(f"[ERROR]  {url} - Exception: {e}")
            return (url, str(e))

    async def run(self):
        async with aiohttp.ClientSession() as session:
            html = await self.fetch_html(session, self.base_url)
            if not html:
                return

            links = self.extract_links(self.base_url, html)
            print(f"\nFound {len(links)} unique HTTP links.\n")

            tasks = [self.check_link(session, link) for link in links]
            results = await asyncio.gather(*tasks)

            self.broken_links = [res for res in results if res]

            print(f"\n🛑 Found {len(self.broken_links)} broken link(s).")
            for url, status in self.broken_links:
                print(f"- {url} --> {status}")

            return self.broken_links