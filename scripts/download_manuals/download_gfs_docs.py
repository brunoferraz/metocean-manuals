#!/usr/bin/env python3
"""
Download GFS technical documentation from NCEP/NOAA/EMC.
Sources:
  - EMC GFS Documentation page (FV3-based, v15/v16)
  - EMC Legacy Spectral GFS Documentation
  - NCEP Office Notes related to GFS
  - NWS Service Change Notices / TINs
  - GFSv15/v16 MEG evaluation PDFs

Output: docs/gfs_docs/
"""

import os
import urllib.request
import urllib.error

OUT_DIR = os.path.join(os.path.dirname(__file__), "gfs_docs")
os.makedirs(OUT_DIR, exist_ok=True)

BASE_EMC = "https://www.emc.ncep.noaa.gov"
BASE_NWS = "https://www.weather.gov"

DOCS = {
    # ── NWS Service Change Notices ─────────────────────────────────────────
    "SCN_GFSv15_2019.pdf":
        "https://www.weather.gov/media/notification/scn19-40gfs_v15_1.pdf",
    "SCN_GFSv16_2021_science.pdf":
        "https://www.weather.gov/media/notification/scn_21-20_gfsv16.0_aaa_update.pdf",
    "SCN_GFSv16_2021_timing.pdf":
        "https://www.weather.gov/media/notification/pdf2/scn21-21model_timing_gfs_v16.pdf",
    # ── NWS Technical Implementation Notices (TINs) ────────────────────────
    "TIN_GFS_2010.pdf":
        "https://www.weather.gov/media/notification/tins/tin10-15gfs.pdf",
    "TIN_GFS_2012_hybrid.pdf":
        "https://www.weather.gov/media/notification/tins/tin12-22gfs_hybridaab.pdf",
    "TIN_GFS_2014.pdf":
        "https://www.weather.gov/media/notification/tins/tin14-46gfs_cca.pdf",
    "TIN_GFS_2016_gdas.pdf":
        "https://www.weather.gov/media/notification/tins/tin16-11gfs_gdasaaa.pdf",
    "SCN_GFS_2017_upgrade.pdf":
        "https://www.weather.noaa.gov/media/notification/tins/scn17-67gfsupgrade.pdf",
    # ── EMC/NCEP Office Notes (GFS-specific) ──────────────────────────────
    "ON441_solar_radiation.pdf":
        "https://www.emc.ncep.noaa.gov/officenotes/newernotes/on441.pdf",
    "ON442_GFS_atmospheric_model.pdf":
        "https://www.emc.ncep.noaa.gov/officenotes/newernotes/on442.pdf",
    "ON461_sigma_pressure_coordinate.pdf":
        "https://www.emc.ncep.noaa.gov/officenotes/newernotes/on461.pdf",
    "ON462_semi_lagrangian_equations.pdf":
        "https://www.emc.ncep.noaa.gov/officenotes/newernotes/on462.pdf",
    "ON477_deep_atmospheric_nonhydrostatic.pdf":
        "https://www.emc.ncep.noaa.gov/officenotes/newernotes/on477.pdf",
    # ── GFS Post-processor ────────────────────────────────────────────────
    "ncepupp_postprocessor.pdf":
        "https://www.emc.ncep.noaa.gov/GFS/docs/ncepupp.pdf",
    # ── GFSv15 Implementation Documents (PDFs) ────────────────────────────
    "GFSv15_CCB_presentation.pdf":
        "https://www.emc.ncep.noaa.gov/users/Alicia.Bentley/fv3gfs/updates/EMC_CCB_FV3GFS_9-24-18.pdf",
    "GFSv15_OD_brief.pdf":
        "https://www.emc.ncep.noaa.gov/emc/docs/FV3GFS_OD_Briefs_10-01-18_4-1-2019.pdf",
    # ── GFSv16 Implementation Documents (PDFs) ────────────────────────────
    "GFSv16_CCB_presentation.pdf":
        "https://www.emc.ncep.noaa.gov/users/meg/gfsv16/pptx/CCB_9-30-20_GFSv16_Full.pdf",
    "GFSv16_wave_evaluation.pdf":
        "https://www.emc.ncep.noaa.gov/users/meg/gfsv16/pptx/MEG_10-01-20_GFSv16_Wave_Evaluation.pdf",
    "GFSv16_SOO_evaluation.pdf":
        "https://www.emc.ncep.noaa.gov/users/meg/gfsv16/pptx/MEG_9-17-20_GFSv16_SOO_Team_Evaluation.pdf",
    # ── GFS Physics Documentation (UFS/CCPP online docs not PDFs,
    #    but the FV3GFS brief PDFs are downloadable) ────────────────────────
    "FV3GFS_OD_brief.pdf":
        "https://www.emc.ncep.noaa.gov/emc/docs/FV3GFS_OD_Briefs_10-01-18_4-1-2019.pdf",
    # ── NCEP Office Note 424 (Orography) ──────────────────────────────────
    "ON424_global_orography.pdf":
        "https://www.emc.ncep.noaa.gov/officenotes/newernotes/on424.pdf",

}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; gfs-doc-downloader)"}

success, skipped, failed = 0, 0, 0
failed_list = []

for name, url in DOCS.items():
    dest = os.path.join(OUT_DIR, name)
    if os.path.exists(dest) and os.path.getsize(dest) > 1000:
        print(f"  SKIP  {name}")
        skipped += 1
        continue
    print(f"  GET   {name} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            data = r.read()
            f.write(data)
        size_kb = len(data) // 1024
        print(f"OK ({size_kb} KB)")
        success += 1
    except Exception as e:
        print(f"FAILED — {e}")
        failed_list.append((name, url, str(e)))
        failed += 1

print(f"\n{'='*60}")
print(f"Total: {len(DOCS)} | Downloaded: {success} | Skipped: {skipped} | Failed: {failed}")
if failed_list:
    print("\nFailed files:")
    for name, url, err in failed_list:
        print(f"  - {name}: {err}")
print(f"\nSaved to: {OUT_DIR}")
