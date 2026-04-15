#!/usr/bin/env python3
"""
Download and scrape GEBCO documentation.

Strategy:
  - GEBCO does NOT publish separate PDF manuals per grid version.
    Documentation is embedded inside each data zip file.
  - The only standalone PDF document is the IHO-IOC GEBCO Cook Book.
  - Per-grid technical documentation (specs, methodology, terms of use)
    is scraped from the official GEBCO web pages and saved as Markdown.

Output: docs/gebco_docs/
"""

import os
import urllib.request
import re

OUT_DIR = os.path.join(os.path.dirname(__file__), "gebco_docs")
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; gebco-doc-downloader)"}

# ─── 1. PDF Downloads ──────────────────────────────────────────────────────

PDFS = {
    # The IHO-IOC GEBCO Cook Book — the main reference manual
    # for bathymetric grid construction methodology
    "IHO-IOC_GEBCO_CookBook_2019.pdf":
        "https://www.star.nesdis.noaa.gov/socd/lsa/GEBCO_Cookbook/documents/CookBook_20191031.pdf",
}

print("=" * 60)
print("GEBCO Documentation Downloader")
print("=" * 60)
print("\n[1/2] Downloading PDFs...\n")

pdf_ok, pdf_fail = 0, 0
for name, url in PDFS.items():
    dest = os.path.join(OUT_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 10000:
        print(f"  SKIP  {name}")
        continue
    print(f"  GET   {name} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
            data = r.read()
            f.write(data)
        print(f"OK ({len(data)//1024} KB)")
        pdf_ok += 1
    except Exception as e:
        print(f"FAILED — {e}")
        pdf_fail += 1

# ─── 2. Scrape grid pages as Markdown ─────────────────────────────────────

GRID_PAGES = {
    "GEBCO_2025_grid_docs.md":
        "https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2025-grid",
    "GEBCO_2024_grid_docs.md":
        "https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2024-grid",
    "GEBCO_2023_grid_docs.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/gebco2023-grid",
    "GEBCO_2022_grid_docs.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/gebco-2022",
    "GEBCO_2021_grid_docs.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/gebco-2021",
    "GEBCO_2020_grid_docs.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/gebco-2020",
    "GEBCO_2019_grid_docs.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/gebco-2019",
    "GEBCO_Arctic_IBCAO_docs.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/arctic-ocean",
    "GEBCO_Southern_IBCSO_docs.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/southern-ocean",
    "GEBCO_CookBook_page.md":
        "https://www.gebco.net/data-products/gebco-cook-book",
    "GEBCO_gridded_bathymetry_overview.md":
        "https://www.gebco.net/data-products/gridded-bathymetry-data/",
}

print("\n[2/2] Scraping grid documentation pages as Markdown...\n")

def extract_main_content(html_bytes):
    """Simple HTML-to-text extractor that preserves structure."""
    try:
        text = html_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""

    # Remove script and style blocks
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<nav[^>]*>.*?</nav>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<header[^>]*>.*?</header>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<footer[^>]*>.*?</footer>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Convert headings
    text = re.sub(r"<h1[^>]*>(.*?)</h1>", r"\n# \1\n", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<h4[^>]*>(.*?)</h4>", r"\n#### \1\n", text, flags=re.DOTALL | re.IGNORECASE)

    # Convert links
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", text, flags=re.DOTALL | re.IGNORECASE)

    # Convert list items
    text = re.sub(r"<li[^>]*>(.*?)</li>", r"\n- \1", text, flags=re.DOTALL | re.IGNORECASE)

    # Convert paragraphs and divs to newlines
    text = re.sub(r"<p[^>]*>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"<div[^>]*>", "\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</div>", "", text, flags=re.IGNORECASE)

    # Remove remaining HTML tags
    text = re.sub(r"<[^>]+>", "", text)

    # Clean up HTML entities
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace(
        "&gt;", ">").replace("&nbsp;", " ").replace("&copy;", "©").replace(
        "&#39;", "'").replace("&quot;", '"')

    # Collapse excessive whitespace/blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    lines = [l.strip() for l in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


scrape_ok, scrape_fail = 0, 0
for filename, url in GRID_PAGES.items():
    dest = os.path.join(OUT_DIR, filename)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"  SKIP  {filename}")
        continue
    print(f"  GET   {url} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
        content = extract_main_content(raw)
        header = f"# GEBCO Documentation\n\nSource: {url}\n\n---\n\n"
        with open(dest, "w", encoding="utf-8") as f:
            f.write(header + content)
        print(f"OK ({len(content)//1024} KB text)")
        scrape_ok += 1
    except Exception as e:
        print(f"FAILED — {e}")
        scrape_fail += 1

print(f"\n{'=' * 60}")
print(f"PDFs:   Downloaded {pdf_ok} | Failed {pdf_fail}")
print(f"Pages:  Scraped {scrape_ok} | Failed {scrape_fail}")
print(f"\nSaved to: {OUT_DIR}")
print(f"\nFiles created:")
for f in sorted(os.listdir(OUT_DIR)):
    sz = os.path.getsize(os.path.join(OUT_DIR, f))
    print(f"  {f:50s} ({sz//1024} KB)")
