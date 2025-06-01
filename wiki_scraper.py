import re
import asyncio
import httpx
from bs4 import BeautifulSoup

WIKI_BASE_URL = "https://en.wikipedia.org"
MAX_CONCURRENT_REQUESTS = 5

# Shared semaphore for concurrency control
tasks_semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

async def fetch_article(client: httpx.AsyncClient, title: str) -> str:
    """Fetch HTML content for a single Wikipedia article."""
    url = f"{WIKI_BASE_URL}/wiki/{title}"
    async with tasks_semaphore:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def parse_text_and_links(html: str) -> tuple[str, list[str]]:
    """Extract plain text and list of linked article titles."""
    soup = BeautifulSoup(html, 'html.parser')
    content = soup.find(id='mw-content-text')
    if not content:
        return "", []

    text = "".join(p.get_text() for p in content.find_all('p'))
    links = [
        a['href'].split('/wiki/')[1]
        for a in content.find_all('a', href=True)
        if a['href'].startswith('/wiki/') and ':' not in a['href']
    ]
    return text, links


def tokenize(text: str) -> list[str]:
    """Split text into lowercase words using simple regex."""
    return re.findall(r"\b[a-zA-Z']+\b", text.lower())

async def traverse_articles_async(start_title: str, max_depth: int) -> list[str]:
    """
    Traverse Wikipedia articles asynchronously up to max_depth.
    Uses a queue-based BFS to simplify flow and avoid deep recursion.
    """
    visited = set([start_title])
    queue = [(start_title, 0)]
    words = []

    async with httpx.AsyncClient(timeout=10) as client:
        while queue:
            title, depth = queue.pop(0)
            try:
                html = await fetch_article(client, title)
            except (httpx.HTTPError, httpx.RequestError):
                continue

            text, links = parse_text_and_links(html)
            words.extend(tokenize(text))

            if depth < max_depth:
                for link in links:
                    if link not in visited:
                        visited.add(link)
                        queue.append((link, depth + 1))
    return words
