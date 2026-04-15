#!/usr/bin/env python3
"""
Download all HYCOM documentation PDFs from hycom.org/hycom/documentation
Output: docs/hycom_docs/
"""

import os
import urllib.request

OUT_DIR = os.path.join(os.path.dirname(__file__), "hycom_docs")
os.makedirs(OUT_DIR, exist_ok=True)

DOCS = {
    # ── User Manuals & Design ──────────────────────────────────────────────
    "hycom_users_guide_v2.1_draft.pdf":
        "https://www.hycom.org/attachments/063_hycom_users_guide.pdf",
    "hycom_users_manual_v2.0.01.pdf":
        "https://www.hycom.org/attachments/063_hycom_users_manual.pdf",
    "hycom_sdd_v2.2_metzger.pdf":
        "https://www.hycom.org/attachments/063_metzger1-2009.pdf",
    # ── Halliwell Docs ─────────────────────────────────────────────────────
    "halliwell_advdiff.pdf":
        "https://www.hycom.org/attachments/067_advdiff.pdf",
    "halliwell_boundary.pdf":
        "https://www.hycom.org/attachments/067_boundary.pdf",
    "halliwell_diapycnal.pdf":
        "https://www.hycom.org/attachments/067_diapycnal.pdf",
    "halliwell_float.pdf":
        "https://www.hycom.org/attachments/067_float.pdf",
    "halliwell_giss.pdf":
        "https://www.hycom.org/attachments/067_giss.pdf",
    "halliwell_hybrid.pdf":
        "https://www.hycom.org/attachments/067_hybrid.pdf",
    "halliwell_ice.pdf":
        "https://www.hycom.org/attachments/067_ice.pdf",
    "halliwell_kpp.pdf":
        "https://www.hycom.org/attachments/067_kpp.pdf",
    "halliwell_kta.pdf":
        "https://www.hycom.org/attachments/067_kta.pdf",
    "halliwell_ktb.pdf":
        "https://www.hycom.org/attachments/067_ktb.pdf",
    "halliwell_ktc.pdf":
        "https://www.hycom.org/attachments/067_ktc.pdf",
    "halliwell_mesh.pdf":
        "https://www.hycom.org/attachments/067_mesh.pdf",
    "halliwell_momentum.pdf":
        "https://www.hycom.org/attachments/067_momentum.pdf",
    "halliwell_mellor_yamada.pdf":
        "https://www.hycom.org/attachments/067_my.pdf",
    "halliwell_overview.pdf":
        "https://www.hycom.org/attachments/067_overview.pdf",
    "halliwell_pwp.pdf":
        "https://www.hycom.org/attachments/067_pwp.pdf",
    "halliwell_state.pdf":
        "https://www.hycom.org/attachments/067_state.pdf",
    "halliwell_surface.pdf":
        "https://www.hycom.org/attachments/067_surface.pdf",
    "halliwell_vdiff.pdf":
        "https://www.hycom.org/attachments/067_vdiff.pdf",
    "halliwell_vertical_vel.pdf":
        "https://www.hycom.org/attachments/067_vertical_vel.pdf",
    # ── Wallcraft Docs ─────────────────────────────────────────────────────
    "wallcraft_HYCOM_2.1.03_code.pdf":
        "https://www.hycom.org/attachments/066_HYCOM%202.1.03_code.pdf",
    "wallcraft_HYCOM_2.1.03_model_devel.pdf":
        "https://www.hycom.org/attachments/066_HYCOM%202.1.03_model_devel.pdf",
    "wallcraft_HYCOM_2.2_code_devel.pdf":
        "https://www.hycom.org/attachments/066_HYCOM%202.2_code_devel.pdf",
    "wallcraft_HYCOM_2.2_code_devel_2.pdf":
        "https://www.hycom.org/attachments/066_HYCOM%202.2_code_devel_2.pdf",
    "wallcraft_HYCOM_2.2_features.pdf":
        "https://www.hycom.org/attachments/066_HYCOM%202.2_features.pdf",
    "wallcraft_talk_COAPS_17a.pdf":
        "https://www.hycom.org/attachments/066_talk_COAPS_17a.pdf",
    "wallcraft_talk_hycom_09a.pdf":
        "https://www.hycom.org/attachments/066_talk_hycom_09a.pdf",
    "wallcraft_new_features_lom2011.pdf":
        "https://www.hycom.org/attachments/066_wallcraft_new-features-of-hycom_lom-2011.pdf",
    "wallcraft_new_features_lom2013.pdf":
        "https://www.hycom.org/attachments/066_wallcraft_new-features-of-hycom_lom-2013.pdf",
    "wallcraft_new_features_lom2015.pdf":
        "https://www.hycom.org/attachments/066_wallcraft_new-features-of-hycom_lom-2015.pdf",
    # ── Community ──────────────────────────────────────────────────────────
    "BB86_for_dummies.pdf":
        "https://www.hycom.org/attachments/349_BB86_for_dummies.pdf",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; hycom-doc-downloader)"}

success, skipped, failed = 0, 0, 0
for name, url in DOCS.items():
    dest = os.path.join(OUT_DIR, name)
    if os.path.exists(dest):
        print(f"  SKIP  {name}")
        skipped += 1
        continue
    print(f"  GET   {name} ...", end=" ", flush=True)
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
        size_kb = os.path.getsize(dest) // 1024
        print(f"OK ({size_kb} KB)")
        success += 1
    except Exception as e:
        print(f"FAILED — {e}")
        failed += 1

print(f"\n{'='*50}")
print(f"Total: {len(DOCS)} | Downloaded: {success} | Skipped: {skipped} | Failed: {failed}")
print(f"Saved to: {OUT_DIR}")
