#!/usr/bin/env python3
"""Refresh license texts from the exact npm package versions included in dist/vendor."""
from pathlib import Path
import urllib.request
from concurrent.futures import ThreadPoolExecutor
ROOT = Path(__file__).resolve().parents[1]
PACKAGES = {
    'marked': ('15.0.12', 'LICENSE.md'),
    'dompurify': ('3.3.0', 'LICENSE'),
    'katex': ('0.16.22', 'LICENSE'),
    'pdfjs-dist': ('3.11.174', 'LICENSE'),
    'mammoth': ('1.9.0', 'LICENSE'),
    'mermaid': ('10.9.3', 'LICENSE'),
}
def fetch(item):
    package, (version, filename) = item
    url = f'https://cdn.jsdelivr.net/npm/{package}@{version}/{filename}'
    body = urllib.request.urlopen(url, timeout=45).read()
    dest = ROOT / 'dist/vendor/licenses' / (package + '.txt')
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(body)
    return package, url, len(body)
if __name__ == '__main__':
    with ThreadPoolExecutor(max_workers=6) as pool:
        for package, url, size in pool.map(fetch, PACKAGES.items()):
            print(package, size, url)
