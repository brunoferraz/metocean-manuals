#!/usr/bin/env python3
"""
Download ECMWF IFS Documentation PDFs.

Strategy:
  - The ECMWF elibrary embeds the real PDF URL in each page's HTML.
  - We scrape each elibrary page to extract the PDF href, then download it.
  - Focus: CY49R1 (latest, all 8 parts) + CY48R1 (previous cycle, all 8 parts)
    + wave model docs for older cycles (relevant for ocean/wave applications)
    + supplementary docs (Forecast User Guide page, ERA5 documentation)

Links discovered from: https://www.ecmwf.int/en/publications/ifs-documentation

Output: docs/ecmwf_docs/
"""

import os
import re
import time
import urllib.request
import urllib.error

OUT_DIR = os.path.join(os.path.dirname(__file__), "ecmwf_docs")
os.makedirs(OUT_DIR, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

# ─── IFS Documentation elibrary slugs ────────────────────────────────────
# Format: "output_filename": "elibrary_id-slug"
# CY49R1 — current operational cycle (Nov 2024)

IFS_ELIBRARY = {

    # ── CY49R1 (2024) — all 8 parts ───────────────────────────────────────
    "IFS_CY49R1_Part-I_Observations.pdf":
        "81623-ifs-documentation-cy49r1-part-i-observations",
    "IFS_CY49R1_Part-II_Data-Assimilation.pdf":
        "81624-ifs-documentation-cy49r1-part-ii-data-assimilation",
    "IFS_CY49R1_Part-III_Dynamics.pdf":
        "81625-ifs-documentation-cy49r1-part-iii-dynamics-and-numerical-procedures",
    "IFS_CY49R1_Part-IV_Physical-Processes.pdf":
        "81626-ifs-documentation-cy49r1-part-iv-physical-processes",
    "IFS_CY49R1_Part-V_EPS.pdf":
        "81627-ifs-documentation-cy49r1-part-v-ensemble-prediction-system",
    "IFS_CY49R1_Part-VI_Technical-Procedures.pdf":
        "81628-ifs-documentation-cy49r1-part-vi-technical-and-computational-procedures",
    "IFS_CY49R1_Part-VII_Wave-Model.pdf":
        "81629-ifs-documentation-cy49r1-part-vii-ecmwf-wave-model",
    "IFS_CY49R1_Part-VIII_Atmospheric-Composition.pdf":
        "81630-ifs-documentation-cy49r1-part-viii-atmospheric-composition",

    # ── CY48R1 (2023) — all 8 parts ───────────────────────────────────────
    "IFS_CY48R1_Part-I_Observations.pdf":
        "81367-ifs-documentation-cy48r1-part-i-observations",
    "IFS_CY48R1_Part-II_Data-Assimilation.pdf":
        "81368-ifs-documentation-cy48r1-part-ii-data-assimilation",
    "IFS_CY48R1_Part-III_Dynamics.pdf":
        "81369-ifs-documentation-cy48r1-part-iii-dynamics-and-numerical-procedures",
    "IFS_CY48R1_Part-IV_Physical-Processes.pdf":
        "81370-ifs-documentation-cy48r1-part-iv-physical-processes",
    "IFS_CY48R1_Part-V_EPS.pdf":
        "81371-ifs-documentation-cy48r1-part-v-ensemble-prediction-system",
    "IFS_CY48R1_Part-VI_Technical-Procedures.pdf":
        "81372-ifs-documentation-cy48r1-part-vi-technical-and-computational-procedures",
    "IFS_CY48R1_Part-VII_Wave-Model.pdf":
        "81373-ifs-documentation-cy48r1-part-vii-ecmwf-wave-model",
    "IFS_CY48R1_Part-VIII_Atmospheric-Composition.pdf":
        "81374-ifs-documentation-cy48r1-part-viii-atmospheric-composition",

    # ── CY47R3 (2021) — Wave model (important for ocean apps) ─────────────
    "IFS_CY47R3_Part-IV_Physical-Processes.pdf":
        "81271-ifs-documentation-cy47r3-part-iv-physical-processes",
    "IFS_CY47R3_Part-VII_Wave-Model.pdf":
        "81274-ifs-documentation-cy47r3-part-vii-ecmwf-wave-model",

    # ── CY47R1 (2020) ─────────────────────────────────────────────────────
    "IFS_CY47R1_Part-IV_Physical-Processes.pdf":
        "81189-ifs-documentation-cy47r1-part-iv-physical-processes",
    "IFS_CY47R1_Part-VII_Wave-Model.pdf":
        "81192-ifs-documentation-cy47r1-part-vii-ecmwf-wave-model",

    # ── CY46R1 (2019) ─────────────────────────────────────────────────────
    "IFS_CY46R1_Part-IV_Physical-Processes.pdf":
        "81141-ifs-documentation-cy46r1-part-iv-physical-processes",
    "IFS_CY46R1_Part-VII_Wave-Model.pdf":
        "81144-ifs-documentation-cy46r1-part-vii-ecmwf-wave-model",

    # ── CY45R1 (2018) ─────────────────────────────────────────────────────
    "IFS_CY45R1_Part-IV_Physical-Processes.pdf":
        "80895-ifs-documentation-cy45r1-part-iv-physical-processes",
    "IFS_CY45R1_Part-VII_Wave-Model.pdf":
        "80898-ifs-documentation-cy45r1-part-vii-ecmwf-wave-model",
}

# ─── Web pages to scrape as Markdown ─────────────────────────────────────

PAGES = {
    "ECMWF_IFS_documentation_index.md":
        "https://www.ecmwf.int/en/publications/ifs-documentation",
    "ECMWF_ERA5_documentation.md":
        "https://confluence.ecmwf.int/display/CKB/ERA5%3A+data+documentation",
    "ECMWF_open_data.md":
        "https://www.ecmwf.int/en/forecasts/datasets/open-data",
    "ECMWF_forecast_datasets.md":
        "https://www.ecmwf.int/en/forecasts/datasets",
    "ECMWF_wave_products.md":
        "https://www.ecmwf.int/en/forecasts/datasets/catalogue-ecmwf-real-time-products",
}


def fetch_pdf_url_from_elibrary(slug):
    """Fetch the elibrary page and extract the direct PDF URL."""
    url = f"https://www.ecmwf.int/en/elibrary/{slug}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            html = r.read().decode("utf-8", errors="replace")
        # Look for PDF links in href attributes
        pdfs = re.findall(
            r'href="(https://www\.ecmwf\.int/sites/default/files/elibrary/[^"]+\.pdf[^"]*)"',
            html
        )
        if not pdfs:
            pdfs2 = re.findall(
                r'href="(/sites/default/files/elibrary/[^"]+\.pdf[^"]*)"',
                html
            )
            pdfs = [f"https://www.ecmwf.int{p}" for p in pdfs2]
        return pdfs[0] if pdfs else None
    except Exception as e:
        return None


def download_file(url, dest):
    """Download a file to dest. Returns (size_bytes, error)."""
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        if len(data) < 5000:
            return 0, f"Too small ({len(data)} bytes)"
        with open(dest, "wb") as f:
            f.write(data)
        return len(data), None
    except Exception as e:
        return 0, str(e)


def extract_content(html_bytes):
    """Minimal HTML → readable text converter."""
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
    text = re.sub(r"<p[^>]*>", "\n\n", text, flags=re.IGNORECASE)
    text = re.sub(r"</p>",     "\n",   text, flags=re.IGNORECASE)
    text = re.sub(r"<br\s*/?>","\n",   text, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>",  "",     text)
    text = text.replace("&amp;","&").replace("&lt;","<").replace("&gt;",">") \
               .replace("&nbsp;"," ").replace("&copy;","©") \
               .replace("&#39;","'").replace("&quot;",'"')
    text = re.sub(r"[ \t]+", " ", text)
    lines = [l.strip() for l in text.split("\n")]
    text  = "\n".join(lines)
    text  = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ─── Main ─────────────────────────────────────────────────────────────────

print("=" * 65)
print("ECMWF IFS Documentation Downloader")
print("=" * 65)

# ── Phase 1: Discover PDF URLs and Download ───────────────────────────────
print(f"\n[1/2] Discovering and downloading {len(IFS_ELIBRARY)} IFS docs...\n")

pdf_ok = pdf_skip = pdf_fail = 0
failed = []

for fname, slug in IFS_ELIBRARY.items():
    dest = os.path.join(OUT_DIR, fname)

    if os.path.exists(dest) and os.path.getsize(dest) > 50_000:
        print(f"  SKIP  {fname}")
        pdf_skip += 1
        continue

    print(f"  FIND  {fname} ...", end=" ", flush=True)
    pdf_url = fetch_pdf_url_from_elibrary(slug)
    if not pdf_url:
        print(f"PDF URL not found in elibrary page")
        failed.append((fname, f"https://www.ecmwf.int/en/elibrary/{slug}", "No PDF URL"))
        pdf_fail += 1
        time.sleep(0.5)
        continue

    print(f"→ GET ...", end=" ", flush=True)
    size, err = download_file(pdf_url, dest)
    if err:
        print(f"FAILED — {err}")
        failed.append((fname, pdf_url, err))
        pdf_fail += 1
    else:
        print(f"OK ({size//1024//1024} MB)" if size > 1_000_000 else f"OK ({size//1024} KB)")
        pdf_ok += 1
    time.sleep(0.3)  # polite delay between requests

# ── Phase 2: Scrape supplementary pages ──────────────────────────────────
print(f"\n[2/2] Scraping {len(PAGES)} supplementary pages as Markdown...\n")

pg_ok = pg_fail = 0
for fname, url in PAGES.items():
    dest = os.path.join(OUT_DIR, fname)
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        print(f"  SKIP  {fname}")
        continue
    print(f"  GET   {url[:65]} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read()
        content = extract_content(raw)
        with open(dest, "w", encoding="utf-8") as f:
            f.write(f"# ECMWF Documentation\n\nSource: {url}\n\n---\n\n{content}")
        print(f"OK ({len(content)//1024} KB)")
        pg_ok += 1
    except Exception as e:
        print(f"FAILED — {e}")
        pg_fail += 1

# ── Summary ────────────────────────────────────────────────────────────────
print(f"\n{'=' * 65}")
print(f"PDFs:   Downloaded {pdf_ok} | Skipped {pdf_skip} | Failed {pdf_fail}")
print(f"Pages:  Scraped {pg_ok} | Failed {pg_fail}")
if failed:
    print("\nFailed items:")
    for n, u, e in failed:
        print(f"  - {n}: {e}")

print(f"\nOutput: {OUT_DIR}")
print(f"\nFiles:")
for f in sorted(os.listdir(OUT_DIR)):
    sz = os.path.getsize(os.path.join(OUT_DIR, f))
    print(f"  {f:60s} ({sz//1024:>6} KB)")
