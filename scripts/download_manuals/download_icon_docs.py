#!/usr/bin/env python3
"""
Download ICON (ICOsahedral Nonhydrostatic) model documentation.
Sources:
  - Reports on ICON — DWD/MPI-M technical series (ISSN 2628-4898)
  - ICON Tutorial (DWD, DOI-referenced PDF)
  - DWD Database Reference for ICON and ICON-EPS
  - EMVORADO Radar forward operator User's Guide (COSMO/ICON)
  - docs.icon-model.org pages scraped as Markdown

Output: docs/icon_docs/
"""

import os
import re
import urllib.request
import urllib.error

OUT_DIR = os.path.join(os.path.dirname(__file__), "icon_docs")
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; icon-doc-downloader)"}
BASE_DWD = "https://www.dwd.de/SharedDocs/downloads/DE/modelldokumentationen/nwv/icon"
BASE_REP = "https://www.dwd.de/EN/ourservices/reports_on_icon/pdf_einzelbaende"


# ─── 1. PDFs ──────────────────────────────────────────────────────────────

# Reports on ICON — numbered PDFs (YYYY_NN format).
# Known from page scrape + archive: 2019_01..03, 2020_04..05, 2021_06..08,
# 2022_09..10, 2024_11.  We probe sequentially to catch any new ones.
REPORT_IDS = [
    "2019_01", "2019_02", "2019_03",
    "2020_04", "2020_05",
    "2021_06", "2021_07", "2021_08",
    "2022_09", "2022_10",
    "2024_11",
]

PDFS = {
    # ── ICON Tutorial (official DOI redirect to DWD PDF) ──────────────────
    "ICON_Tutorial_2025.pdf":
        "https://www.dwd.de/SharedDocs/downloads/DE/modelldokumentationen/nwv/icon/icon_tutorial2025.pdf?__blob=publicationFile",
    # ── DWD Database Reference for ICON (variable definitions, GRIB2 keys) ─
    "ICON_DWD_Database_Reference_current.pdf":
        "https://www.dwd.de/SharedDocs/downloads/DE/modelldokumentationen/nwv/icon/icon_dbbeschr_aktuell.pdf?__blob=publicationFile",
    # ── EMVORADO User's Guide (radar operator used in ICON) ───────────────
    "EMVORADO_UserGuide.pdf":
        "https://www.cosmo-model.org/content/model/documentation/core/emvorado_userguide.pdf",
}

# Build all Report PDFs
for rid in REPORT_IDS:
    year, num = rid.split("_")
    fname = f"Reports_on_ICON_{rid}.pdf"
    url = f"{BASE_REP}/{rid}.pdf?__blob=publicationFile"
    PDFS[fname] = url


# ─── 2. Web pages to scrape as Markdown ──────────────────────────────────

PAGES = {
    "ICON_docs_overview.md":
        "https://docs.icon-model.org/",
    "ICON_literature.md":
        "https://docs.icon-model.org/literature/literature.html",
    "ICON_atmosphere.md":
        "https://docs.icon-model.org/atmosphere/atmosphere.html",
    "ICON_ocean.md":
        "https://docs.icon-model.org/ocean/ocean.html",
    "ICON_waves.md":
        "https://docs.icon-model.org/waves/waves.html",
    "ICON_land.md":
        "https://docs.icon-model.org/land/land.html",
    "ICON_quickstart.md":
        "https://docs.icon-model.org/buildrun/buildrun_quickstart.html",
    "ICON_DWD_reports_page.md":
        "https://www.dwd.de/EN/ourservices/reports_on_icon/reports_on_icon.html",
}


def extract_content(html_bytes):
    """Minimal HTML → clean text converter."""
    try:
        text = html_bytes.decode("utf-8", errors="replace")
    except Exception:
        return ""
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>",  "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<nav[^>]*>.*?</nav>",       "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<header[^>]*>.*?</header>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<footer[^>]*>.*?</footer>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<h1[^>]*>(.*?)</h1>", r"\n# \1\n",    text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<h2[^>]*>(.*?)</h2>", r"\n## \1\n",   text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<h3[^>]*>(.*?)</h3>", r"\n### \1\n",  text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<h4[^>]*>(.*?)</h4>", r"\n#### \1\n", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r"[\2](\1)", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<li[^>]*>(.*?)</li>", r"\n- \1", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<p[^>]*>",  "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>",      "\n",   text, flags=re.IGNORECASE)
    text = re.sub(r"<br\s*/?>", "\n",   text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>",   "",     text)
    text = text.replace("&amp;", "&").replace("&lt;", "<").replace(
        "&gt;", ">").replace("&nbsp;", " ").replace("&copy;", "©").replace(
        "&#39;", "'").replace("&quot;", '"')
    text = re.sub(r"[ \t]+", " ", text)
    lines = [l.strip() for l in text.split("\n")]
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ─── Main ─────────────────────────────────────────────────────────────────

print("=" * 65)
print("ICON Documentation Downloader")
print("=" * 65)

# ── Download PDFs ──────────────────────────────────────────────────────────
print(f"\n[1/2] Downloading PDFs ({len(PDFS)} targets)...\n")

pdf_ok = pdf_skip = pdf_fail = 0
failed_pdfs = []

for name, url in PDFS.items():
    dest = os.path.join(OUT_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"  SKIP  {name}")
        pdf_skip += 1
        continue
    print(f"  GET   {name} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        if len(data) < 1000:
            raise ValueError(f"Too small ({len(data)} bytes)")
        with open(dest, "wb") as f:
            f.write(data)
        print(f"OK ({len(data)//1024} KB)")
        pdf_ok += 1
    except Exception as e:
        print(f"FAILED — {e}")
        pdf_fail += 1
        failed_pdfs.append((name, url, str(e)))

# ── Scrape web pages ───────────────────────────────────────────────────────
print(f"\n[2/2] Scraping documentation pages ({len(PAGES)} targets)...\n")

page_ok = page_skip = page_fail = 0

for name, url in PAGES.items():
    dest = os.path.join(OUT_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"  SKIP  {name}")
        page_skip += 1
        continue
    print(f"  GET   {url} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
        content = extract_content(raw)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(f"# ICON Documentation\n\nSource: {url}\n\n---\n\n{content}")
        print(f"OK ({len(content)//1024} KB text)")
        page_ok += 1
    except Exception as e:
        print(f"FAILED — {e}")
        page_fail += 1

# ── Summary ────────────────────────────────────────────────────────────────
print(f"\n{'=' * 65}")
print(f"PDFs:   Downloaded {pdf_ok} | Skipped {pdf_skip} | Failed {pdf_fail}")
print(f"Pages:  Scraped {page_ok}   | Skipped {page_skip}  | Failed {page_fail}")
if failed_pdfs:
    print("\nFailed PDFs:")
    for n, u, e in failed_pdfs:
        print(f"  - {n}: {e}")

total = pdf_ok + page_ok
print(f"\nTotal files saved: {total}")
print(f"Output: {OUT_DIR}\n")

for f in sorted(os.listdir(OUT_DIR)):
    sz = os.path.getsize(os.path.join(OUT_DIR, f))
    print(f"  {f:55s} ({sz//1024:>5} KB)")
