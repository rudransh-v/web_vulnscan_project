import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def is_same_domain(base_url, link_url):
    return urlparse(base_url).netloc == urlparse(link_url).netloc


def crawl(start_url, max_depth=2):
    visited = set()
    to_visit = [(start_url, 0)]
    discovered_pages = []
    discovered_forms = []

    while to_visit:
        url, depth = to_visit.pop(0)

        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=5)
        except requests.RequestException as e:
            print(f"Could not reach {url}: {e}")
            continue

        if response.status_code != 200:
            continue

        discovered_pages.append(url)
        soup = BeautifulSoup(response.text, "html.parser")

        for form in soup.find_all("form"):
            form_info = {
                "page": url,
                "action": form.get("action"),
                "method": form.get("method", "get"),
                "inputs": [inp.get("name") for inp in form.find_all("input")]
            }
            discovered_forms.append(form_info)

        for link in soup.find_all("a", href=True):
            full_url = urljoin(url, link["href"])
            if is_same_domain(start_url, full_url) and full_url not in visited:
                to_visit.append((full_url, depth + 1))

    return discovered_pages, discovered_forms


if __name__ == "__main__":
    target = "http://localhost/DVWA/"
    pages, forms = crawl(target)

    print(f"\nFound {len(pages)} pages:")
    for p in pages:
        print(" -", p)

    print(f"\nFound {len(forms)} forms:")
    for f in forms:
        print(" -", f)