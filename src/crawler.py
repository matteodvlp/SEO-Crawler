from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")


def is_internal_link(base_url, link):
    base_domain = urlparse(base_url).netloc
    link_domain = urlparse(link).netloc
    return base_domain == link_domain


def extract_internal_links(base_url, soup):
    links = set()

    for tag in soup.find_all("a", href=True):
        absolute_url = urljoin(base_url, tag["href"])
        absolute_url = normalize_url(absolute_url)

        if is_internal_link(base_url, absolute_url):
            links.add(absolute_url)

    return links


def crawl_site(start_url, max_pages=10):
    visited = set()
    to_visit = [normalize_url(start_url)]
    pages = []

    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)

        if url in visited:
            continue

        try:
            response = requests.get(
                url,
                headers={"User-Agent": "SEOAuditBot/1.0"},
                timeout=10
            )
            response.raise_for_status()
        except requests.RequestException:
            continue

        visited.add(url)

        soup = BeautifulSoup(response.text, "html.parser")
        pages.append({
            "url": url,
            "soup": soup
        })

        internal_links = extract_internal_links(url, soup)

        for link in internal_links:
            if link not in visited and link not in to_visit:
                to_visit.append(link)

    return pages