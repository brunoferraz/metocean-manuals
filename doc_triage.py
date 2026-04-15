#!/usr/bin/env python3
"""
=============================================================================
doc_triage.py — Document Triage → Catalog Builder
=============================================================================
Extrai metadados de documentos oceanográficos e popula estruturas do
catalog.py, incluindo formas termodinâmicas e correlação entre fontes.

Uso:
    # Com Ollama local (gratuito)
    python doc_triage.py -i /docs --backend ollama --model qwen2.5:14b

    # Diretório de saída customizado
    python doc_triage.py -i /docs --backend ollama --output-dir ./results

    # Com Anthropic
    python doc_triage.py -i /docs --backend anthropic

    # Só extração local sem LLM
    python doc_triage.py -i /docs --no-llm

Saídas (em --output-dir, padrão: ./output):
    catalog_inventory.json              — metadados extraídos por documento
    catalog_inventory.yaml              — catálogo no formato catalog.py
    catalog_inventory_correlation.txt   — variáveis cruzadas entre documentos
=============================================================================
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import argparse
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

# ---------------------------------------------------------------------------
# Importar catalog.py (deve estar no mesmo diretório ou no PYTHONPATH)
# ---------------------------------------------------------------------------
_this_dir = Path(__file__).resolve().parent
if str(_this_dir) not in sys.path:
    sys.path.insert(0, str(_this_dir))

from catalog import VARIABLE_REGISTRY

# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("triage")

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
MAX_PREVIEW_CHARS = 5000
MAX_PDF_PAGES = 5
LLM_MODEL = "qwen2.5:14b"
SUPPORTED_EXT = {".pdf", ".md", ".txt", ".markdown", ".rst"}


# ---------------------------------------------------------------------------
# TEXT EXTRACTION
# ---------------------------------------------------------------------------

def extract_preview(filepath: Path) -> dict[str, Any]:
    info = {
        "file_size_mb": round(filepath.stat().st_size / (1024 * 1024), 2),
        "pages": None,
        "text": "",
        "method": None,
        "error": None,
    }

    if filepath.suffix.lower() == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(str(filepath))
            info["pages"] = len(reader.pages)
            parts = []
            for i in range(min(MAX_PDF_PAGES, len(reader.pages))):
                t = reader.pages[i].extract_text() or ""
                parts.append(t)
            info["text"] = "\n".join(parts)[:MAX_PREVIEW_CHARS]
            info["method"] = "pypdf"

            if len(info["text"].strip()) < 100:
                try:
                    import pdfplumber
                    with pdfplumber.open(str(filepath)) as pdf:
                        parts = [p.extract_text() or "" for p in pdf.pages[:MAX_PDF_PAGES]]
                    info["text"] = "\n".join(parts)[:MAX_PREVIEW_CHARS]
                    info["method"] = "pdfplumber"
                except Exception:
                    pass
        except Exception as e:
            info["error"] = str(e)
    else:
        try:
            content = filepath.read_text(encoding="utf-8", errors="replace")
            info["text"] = content[:MAX_PREVIEW_CHARS]
            info["pages"] = max(1, len(content) // 3000)
            info["method"] = "text"
        except Exception as e:
            info["error"] = str(e)

    return info


# ---------------------------------------------------------------------------
# DISCOVER
# ---------------------------------------------------------------------------

def _file_hash(fp: Path, root: Path) -> str:
    """ID estável por documento, resistente a colisões.

    Combina caminho relativo + conteúdo completo e gera SHA-1 curto.
    """
    h = hashlib.sha1()
    rel = fp.relative_to(root).as_posix().encode("utf-8", errors="replace")
    h.update(rel)
    h.update(b"\0")
    with fp.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _legacy_file_hash(fp: Path) -> str:
    """Hash legado usado em versões antigas (md5 dos primeiros 8KB)."""
    with fp.open("rb") as f:
        return hashlib.md5(f.read(8192)).hexdigest()[:12]


def discover_files(input_dir: Path) -> list[dict[str, Any]]:
    """Lista todos os arquivos suportados e retorna metadados mínimos (sem extração de texto)."""
    files = sorted(f for f in input_dir.rglob("*") if f.suffix.lower() in SUPPORTED_EXT)
    return [
        {
            "doc_id": _file_hash(fp, input_dir),
            "legacy_doc_id": _legacy_file_hash(fp),
            "filename": fp.name,
            "filepath": str(fp),
            "extension": fp.suffix.lower(),
            "file_size_mb": round(fp.stat().st_size / (1024 * 1024), 2),
            "pages": None,
            "text_preview": "",
            "extraction_method": None,
            "extraction_error": None,
            "catalog_entry": None,
            "classification_error": None,
        }
        for fp in files
    ]


def reconcile(
    discovered: list[dict], saved: list[dict] | None
) -> tuple[list[dict], list[str], list[str]]:
    """Mescla arquivos descobertos com o checkpoint salvo.

    Retorna:
        docs       — lista final (ordem: descobertos, sem removidos)
        added      — filenames novos
        removed    — filenames presentes no checkpoint mas não no disco
    """
    saved_by_id: dict[str, dict] = {d["doc_id"]: d for d in (saved or [])}
    saved_by_path: dict[str, dict] = {d["filepath"]: d for d in (saved or [])}
    disc_paths = {d["filepath"] for d in discovered}

    removed = [
        d["filename"] for d in (saved or [])
        if d["filepath"] not in disc_paths
    ]

    docs: list[dict] = []
    added: list[str] = []
    migrated = 0
    for d in discovered:
        prev = saved_by_id.get(d["doc_id"]) or saved_by_path.get(d["filepath"])
        if prev:
            # Match direto pelo novo doc_id.
            same_doc = prev.get("doc_id") == d["doc_id"]

            # Migração: mesmo arquivo (filepath) com doc_id legado.
            same_legacy = (
                prev.get("filepath") == d["filepath"]
                and prev.get("doc_id") == d.get("legacy_doc_id")
            )

            if same_doc or same_legacy:
                # Arquivo não mudou — aproveitar tudo do checkpoint
                d.update({
                    "pages": prev.get("pages"),
                    "text_preview": prev.get("text_preview", ""),
                    "extraction_method": prev.get("extraction_method"),
                    "extraction_error": prev.get("extraction_error"),
                    "catalog_entry": prev.get("catalog_entry"),
                    "classification_error": prev.get("classification_error"),
                })
                if same_legacy:
                    migrated += 1
            else:
                # Arquivo modificado — reextrair e reclassificar
                added.append(d["filename"] + " (modified)")
        else:
            added.append(d["filename"])
        docs.append(d)

    if migrated:
        log.info("  Legacy checkpoint migration: %d document(s) reused", migrated)

    return docs, added, removed


# ---------------------------------------------------------------------------
# CHECKLIST
# ---------------------------------------------------------------------------

def print_checklist(docs: list[dict]) -> None:
    """Imprime tabela de status: extração de texto e classificação LLM."""
    TICK = "[x]"
    CROSS = "[ ]"
    ERR = "[!]"

    col_w = max((len(d["filename"]) for d in docs), default=20)
    header = f"  {'Arquivo':<{col_w}}  Extração  LLM"
    print("\n" + "─" * len(header))
    print(header)
    print("─" * len(header))

    for d in docs:
        # Extração
        if d.get("extraction_error"):
            ext_mark = ERR
        elif d.get("extraction_method"):
            ext_mark = TICK
        else:
            ext_mark = CROSS

        # LLM
        if d.get("classification_error"):
            llm_mark = ERR
        elif d.get("catalog_entry"):
            llm_mark = TICK
        else:
            llm_mark = CROSS

        print(f"  {d['filename']:<{col_w}}  {ext_mark:<9} {llm_mark}")

    n_ext = sum(1 for d in docs if d.get("extraction_method"))
    n_llm = sum(1 for d in docs if d.get("catalog_entry"))
    print("─" * len(header))
    print(f"  Total: {len(docs)}  |  Extraídos: {n_ext}/{len(docs)}  |  LLM: {n_llm}/{len(docs)}\n")


def scan_documents(
    docs: list[dict],
    doc_out_dir: Path | None = None,
    inventory_path: str | None = None,
) -> None:
    """Extrai texto dos documentos pendentes e salva checkpoint por documento.

    Modifica ``docs`` in-place e persiste progresso continuamente.
    """
    pending = [d for d in docs if not d.get("extraction_method") and not d.get("extraction_error")]
    if not pending:
        log.info("Text extraction: all files already extracted.")
        return

    log.info("Extracting text from %d file(s)...", len(pending))
    for i, d in enumerate(pending):
        fp = Path(d["filepath"])
        log.info("[%d/%d] Extracting: %s", i + 1, len(pending), fp.name)
        ext = extract_preview(fp)
        d["pages"] = ext["pages"]
        d["text_preview"] = ext["text"]
        d["extraction_method"] = ext["method"]
        d["extraction_error"] = ext["error"]

        if doc_out_dir is not None:
            save_doc_checkpoint(d, doc_out_dir, stage="extracted")
        if inventory_path is not None:
            save_inventory(docs, inventory_path)


# ---------------------------------------------------------------------------
# LLM PROMPT — aligned to catalog.py schema
# ---------------------------------------------------------------------------

PROMPT_TEMPLATE = '''You are an expert in operational oceanography and CF metadata conventions.

Analyze this document and extract structured metadata compatible with the schema below.

<document>
Filename: {filename}
Size: {file_size_mb} MB | Pages: {pages}

{text_preview}
</document>

Respond ONLY with valid JSON (no markdown, no ```). Schema:

{{
  "doc_type": "PUM | model_documentation | evaluation_report | scientific_paper | dataset_description | technical_note | other",
  "relevance_score": 0.0 to 1.0,
  "summary": "2-3 sentences describing the document",

  "provider": {{
    "provider_id": "cmems | noaa | ecmwf | gebco | dwd | cmcc | fmi | null",
    "name": "full name or null"
  }},

  "product_line": {{
    "product_id": "e.g. BLKSEA_ANALYSISFORECAST_PHY_007_001 or null",
    "name": "human readable name or null",
    "model_name": "e.g. NEMO v4.2.2 | WAM 4.7 | WW3 | ICON-O | HYCOM | null",
    "region": "Global | Baltic | Black Sea | Arctic | Atlantic | null",
    "product_types": ["forecast", "analysis", "reanalysis", "hindcast", "observation", "static", "climatology"],
    "categories": ["ocean_physics", "wave", "atmosphere", "bathymetry", "ice", "biogeochemistry"]
  }},

  "datasets": [
    {{
      "dataset_id": "e.g. cmems_mod_blk_phy-temp_anfc_2.5km_P1D-m or null",
      "temporal_resolution": "PT15M | PT1H | P1D | P1M | static | null",
      "update_frequency": "daily | twice_daily | weekly | monthly | static | null",
      "forecast_length_hours": null or integer
    }}
  ],

  "variables": [
    {{
      "native_name": "name in file (e.g. thetao, VHM0, u10)",
      "cf_standard_name": "full CF standard name or null",
      "long_name": "description or null",
      "unit": "unit (m, degC, psu, m/s, degree, g/kg, Pa, 1)",
      "physical_quantity": "temperature | salinity | density | pressure | velocity | sea_level | wave_height | wave_period | wave_direction | depth | ice_fraction | ice_thickness | wind | mixed_layer | vorticity | other",
      "thermodynamic_form": "in_situ | potential | conservative | practical | absolute | neutral | not_applicable",
      "framework": "eos80 | teos10 | unknown",
      "reference_pressure_dbar": null or float (e.g. 0 for theta, 2000 for sigma2),
      "category": "ocean_physics | wave | atmosphere | bathymetry | ice | biogeochemistry | observation_qc",
      "is_3d": true/false,
      "is_vector_component": true/false,
      "vector_pair": "name of paired component or null (e.g. vo if this is uo)"
    }}
  ],

  "grid": {{
    "grid_type": "regular_latlon | curvilinear | unstructured | icosahedral | tripolar | polar_stereographic | null",
    "horizontal_resolution": "e.g. 2.5km, 0.083deg, 100m, R2B6 or null",
    "crs": "EPSG:4326 or other or null",
    "coverage": {{
      "lon_min": null, "lon_max": null, "lat_min": null, "lat_max": null
    }}
  }},

  "vertical": {{
    "vertical_type": "z_levels | z_star | sigma | hybrid | pressure | surface_only | seafloor_only | isopycnal | null",
    "n_levels": null or integer,
    "depth_min_m": null or float,
    "depth_max_m": null or float
  }},

  "access": [
    {{
      "protocol": "opendap | http | cmems_api | cds_api | azure_blob | erddap | thredds | null",
      "format": "netcdf3 | netcdf4 | grib2 | geotiff | zarr | tuv | null",
      "auth_required": true/false
    }}
  ]
}}

CRITICAL thermodynamic rules for variables:
- thetao, temperature (ocean models output) → thermodynamic_form: potential, framework: eos80, reference_pressure_dbar: 0
- conservative temperature (TEOS-10 Theta) → thermodynamic_form: conservative, framework: teos10
- practical salinity (so, salinity, salt, PSU) → thermodynamic_form: practical, framework: eos80
- absolute salinity (SA, g/kg) → thermodynamic_form: absolute, framework: teos10
- sigma0 / rhopot / sigma_theta → thermodynamic_form: potential (density), reference_pressure_dbar: 0
- sigma2 → thermodynamic_form: potential (density), reference_pressure_dbar: 2000
- in-situ density (rho) → thermodynamic_form: in_situ
- Waves, wind, SSH, bathymetry, ice → thermodynamic_form: not_applicable
- List ALL variables mentioned in the document (max 30).'''


# ---------------------------------------------------------------------------
# LLM BACKENDS
# ---------------------------------------------------------------------------

def _build_prompt(doc: dict) -> str:
    return PROMPT_TEMPLATE.format(
        filename=doc["filename"],
        file_size_mb=doc["file_size_mb"],
        pages=doc["pages"],
        text_preview=doc["text_preview"][:MAX_PREVIEW_CHARS],
    )


def _parse_json_response(raw: str) -> dict | None:
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text[3:]
    if text.endswith("```"):
        text = text.rsplit("```", 1)[0]
    start = text.find("{")
    end = text.rfind("}") + 1
    if start >= 0 and end > start:
        text = text[start:end]
    # Tentativa leve de saneamento para erros comuns de vírgula/trailing commas.
    cleaned = text.strip()
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return json.loads(cleaned)


def _build_json_repair_prompt(original_prompt: str, raw_response: str) -> str:
    return (
        "You previously returned invalid JSON for the schema below. "
        "Fix it and return ONLY valid JSON. Do not add commentary.\n\n"
        "<schema_and_context>\n"
        f"{original_prompt}\n"
        "</schema_and_context>\n\n"
        "<invalid_json>\n"
        f"{raw_response}\n"
        "</invalid_json>\n"
    )


def classify_anthropic(doc: dict, client, model: str) -> None:
    prompt = _build_prompt(doc)
    doc["classification_error"] = None
    try:
        resp = client.messages.create(
            model=model, max_tokens=3000, temperature=0.0,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text
        try:
            doc["catalog_entry"] = _parse_json_response(raw)
            doc["_tokens_in"] = resp.usage.input_tokens
            doc["_tokens_out"] = resp.usage.output_tokens
            return
        except json.JSONDecodeError:
            repair_prompt = _build_json_repair_prompt(prompt, raw)
            repaired = client.messages.create(
                model=model, max_tokens=3000, temperature=0.0,
                messages=[{"role": "user", "content": repair_prompt}],
            )
            raw2 = repaired.content[0].text
            doc["catalog_entry"] = _parse_json_response(raw2)
            doc["_tokens_in"] = (resp.usage.input_tokens or 0) + (repaired.usage.input_tokens or 0)
            doc["_tokens_out"] = (resp.usage.output_tokens or 0) + (repaired.usage.output_tokens or 0)
    except json.JSONDecodeError as e:
        doc["classification_error"] = f"JSON parse: {e}"
    except Exception as e:
        doc["classification_error"] = str(e)


def classify_ollama(doc: dict, model: str, url: str) -> None:
    import urllib.request
    prompt = _build_prompt(doc)
    doc["classification_error"] = None
    try:
        total_in = 0
        total_out = 0
        total_eval_s = 0.0

        payload = json.dumps({
            "model": model, "prompt": prompt,
            "stream": False, "options": {"temperature": 0.0, "num_predict": 3000},
        }).encode()
        req = urllib.request.Request(
            f"{url}/api/generate", data=payload,
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=180) as resp:
            result = json.loads(resp.read().decode())

        raw = result.get("response", "")
        total_in += result.get("prompt_eval_count", 0) or 0
        total_out += result.get("eval_count", 0) or 0
        total_eval_s += (result.get("eval_duration", 0) or 0) / 1e9

        try:
            doc["catalog_entry"] = _parse_json_response(raw)
        except json.JSONDecodeError:
            repair_prompt = _build_json_repair_prompt(prompt, raw)
            payload2 = json.dumps({
                "model": model, "prompt": repair_prompt,
                "stream": False, "options": {"temperature": 0.0, "num_predict": 3000},
            }).encode()
            req2 = urllib.request.Request(
                f"{url}/api/generate", data=payload2,
                headers={"Content-Type": "application/json"},
            )
            with urllib.request.urlopen(req2, timeout=180) as resp2:
                result2 = json.loads(resp2.read().decode())
            raw2 = result2.get("response", "")
            total_in += result2.get("prompt_eval_count", 0) or 0
            total_out += result2.get("eval_count", 0) or 0
            total_eval_s += (result2.get("eval_duration", 0) or 0) / 1e9
            doc["catalog_entry"] = _parse_json_response(raw2)

        doc["_tokens_in"] = total_in
        doc["_tokens_out"] = total_out
        doc["_eval_s"] = round(total_eval_s, 2)
    except json.JSONDecodeError as e:
        doc["classification_error"] = f"JSON parse: {e}"
    except Exception as e:
        doc["classification_error"] = str(e)


def classify_all(
    docs: list[dict],
    backend: str,
    model: str,
    ollama_url: str = "http://localhost:11434",
    doc_out_dir: Path | None = None,
    inventory_path: str | None = None,
    full_docs: list[dict] | None = None,
) -> None:
    client = None
    if backend == "anthropic":
        from anthropic import Anthropic
        client = Anthropic()

    for i, doc in enumerate(docs):
        log.info("[%d/%d] Classifying: %s", i + 1, len(docs), doc["filename"])
        if backend == "anthropic":
            classify_anthropic(doc, client, model)
        elif backend == "ollama":
            classify_ollama(doc, model, ollama_url)

        entry = doc.get("catalog_entry")
        if entry:
            n_vars = len(entry.get("variables") or [])
            score = entry.get("relevance_score", "?")
            log.info("  -> %s | %d vars | score=%s",
                     entry.get("doc_type", "?"), n_vars, score)
        elif doc.get("classification_error"):
            log.warning("  error: %s", doc["classification_error"])

        if doc_out_dir is not None:
            save_doc_checkpoint(doc, doc_out_dir, stage="llm")
        if inventory_path is not None:
            save_inventory(full_docs or docs, inventory_path)


# ---------------------------------------------------------------------------
# CORRELATION ENGINE
# ---------------------------------------------------------------------------

@dataclass
class VariableOccurrence:
    doc_filename: str
    native_name: str
    cf_standard_name: str | None
    physical_quantity: str | None
    thermodynamic_form: str | None
    framework: str | None
    reference_pressure_dbar: float | None
    unit: str | None
    category: str | None
    product_id: str | None
    provider_id: str | None


def _resolve_cf_from_registry(native_name: str) -> str | None:
    for cf_name, canon in VARIABLE_REGISTRY.items():
        if native_name in canon.aliases:
            return cf_name
    return None


def build_occurrence_table(docs: list[dict]) -> list[VariableOccurrence]:
    occurrences = []
    for doc in docs:
        entry = doc.get("catalog_entry")
        if not entry:
            continue

        product_id = (entry.get("product_line") or {}).get("product_id")
        provider_id = (entry.get("provider") or {}).get("provider_id")

        for v in (entry.get("variables") or []):
            native = v.get("native_name", "")
            cf = v.get("cf_standard_name")
            if not cf:
                cf = _resolve_cf_from_registry(native)

            occurrences.append(VariableOccurrence(
                doc_filename=doc["filename"],
                native_name=native,
                cf_standard_name=cf,
                physical_quantity=v.get("physical_quantity"),
                thermodynamic_form=v.get("thermodynamic_form"),
                framework=v.get("framework"),
                reference_pressure_dbar=v.get("reference_pressure_dbar"),
                unit=v.get("unit"),
                category=v.get("category"),
                product_id=product_id,
                provider_id=provider_id,
            ))

    return occurrences


def build_correlation_report(occurrences: list[VariableOccurrence]) -> str:
    lines = []
    lines.append("=" * 75)
    lines.append("CORRELATION REPORT")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total occurrences: {len(occurrences)}")
    lines.append("=" * 75)

    by_cf: dict[str, list[VariableOccurrence]] = {}
    unresolved: list[VariableOccurrence] = []
    for occ in occurrences:
        if occ.cf_standard_name:
            by_cf.setdefault(occ.cf_standard_name, []).append(occ)
        else:
            unresolved.append(occ)

    # --- Multi-source: fallback candidates ---
    lines.append(f"\n{'─'*75}")
    lines.append("VARIABLES WITH MULTIPLE SOURCES (fallback candidates)")
    lines.append(f"{'─'*75}")

    multi = {k: v for k, v in by_cf.items() if len({o.doc_filename for o in v}) > 1}
    for cf_name in sorted(multi):
        occs = multi[cf_name]
        canon = VARIABLE_REGISTRY.get(cf_name)
        label = canon.long_name if canon else cf_name

        lines.append(f"\n  {cf_name}")
        lines.append(f"  {label}")

        forms_seen = set()
        for occ in occs:
            form = occ.thermodynamic_form or "?"
            fw = occ.framework or "?"
            ref = f" ref={occ.reference_pressure_dbar}dbar" if occ.reference_pressure_dbar is not None else ""
            forms_seen.add((form, fw, occ.reference_pressure_dbar))
            lines.append(
                f"    {(occ.native_name or '?'):20s} [{occ.unit or '?':6s}] "
                f"form={form:15s} fw={fw:8s}{ref}"
                f"  <- {occ.doc_filename}"
            )

        if len(forms_seen) > 1:
            forms_list = [f"{f[0]}({f[1]})" + (f" ref={f[2]}" if f[2] is not None else "") for f in forms_seen]
            lines.append(f"    WARNING: DIFFERENT FORMS: {', '.join(forms_list)}")
            lines.append(f"    -> Conversion required for direct comparison")
        else:
            lines.append(f"    OK: Compatible — direct fallback possible")

    # --- Single source ---
    lines.append(f"\n{'─'*75}")
    lines.append("VARIABLES WITH SINGLE SOURCE (no fallback in corpus)")
    lines.append(f"{'─'*75}")

    single = {k: v for k, v in by_cf.items() if len({o.doc_filename for o in v}) == 1}
    for cf_name in sorted(single):
        occ = single[cf_name][0]
        canon = VARIABLE_REGISTRY.get(cf_name)
        known = canon.aliases if canon else {}
        alt = sorted(f"{a}@{','.join(p)}" for a, p in known.items())

        lines.append(f"  {(occ.native_name or '?'):20s} -> {cf_name}  <- {occ.doc_filename}")
        if alt:
            lines.append(f"    Known aliases in registry: {', '.join(alt)}")

    # --- Unresolved ---
    if unresolved:
        lines.append(f"\n{'─'*75}")
        lines.append(f"UNRESOLVED VARIABLES ({len(unresolved)})")
        lines.append(f"{'─'*75}")
        for occ in unresolved:
            lines.append(f"  {(occ.native_name or '?'):20s} [{occ.unit or '?'}] <- {occ.doc_filename}")

    # --- Thermodynamic families ---
    lines.append(f"\n{'─'*75}")
    lines.append("THERMODYNAMIC FAMILIES FOUND")
    lines.append(f"{'─'*75}")

    qty_groups: dict[str, set[str]] = {}
    for occ in occurrences:
        q = occ.physical_quantity or "other"
        f = occ.thermodynamic_form
        if f and f != "not_applicable":
            qty_groups.setdefault(q, set()).add(f)

    for q in sorted(qty_groups):
        lines.append(f"  {q}: {', '.join(sorted(qty_groups[q]))}")

    # --- Stats ---
    lines.append(f"\n{'─'*75}")
    lines.append("SUMMARY")
    lines.append(f"{'─'*75}")
    lines.append(f"  Unique CF standard_names: {len(by_cf)}")
    lines.append(f"  Multi-source (fallback OK): {len(multi)}")
    lines.append(f"  Single-source: {len(single)}")
    lines.append(f"  Unresolved: {len(unresolved)}")

    n_issues = sum(
        1 for v in multi.values()
        if len({(o.thermodynamic_form, o.framework, o.reference_pressure_dbar) for o in v}) > 1
    )
    lines.append(f"  Thermodynamic incompatibilities: {n_issues}")

    lines.append("\n" + "=" * 75)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CHECKPOINT / RESUME
# ---------------------------------------------------------------------------

def load_inventory(path: str) -> list[dict[str, Any]] | None:
    """Carrega inventário salvo de uma execução anterior."""
    p = Path(path)
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as f:
        docs = json.load(f)
    for d in docs:
        d.setdefault("text_preview", "")
    log.info("Loaded %d docs from checkpoint: %s", len(docs), path)
    return docs


def _doc_checkpoint_path(doc: dict, doc_out_dir: Path) -> Path:
    return doc_out_dir / f"{doc['doc_id']}.json"


def _doc_stage_checkpoint_path(doc: dict, doc_out_dir: Path, stage: str) -> Path:
    return doc_out_dir / stage / f"{doc['doc_id']}.json"


def save_doc_checkpoint(doc: dict, doc_out_dir: Path, stage: str | None = None) -> None:
    """Salva checkpoint individual consolidado e, opcionalmente, por estágio."""
    doc_out_dir.mkdir(parents=True, exist_ok=True)
    payload = {k: v for k, v in doc.items()}
    path = _doc_checkpoint_path(doc, doc_out_dir)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2, default=str)

    if stage:
        stage_path = _doc_stage_checkpoint_path(doc, doc_out_dir, stage)
        stage_path.parent.mkdir(parents=True, exist_ok=True)
        with stage_path.open("w", encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False, indent=2, default=str)


def load_doc_checkpoint(doc: dict, doc_out_dir: Path) -> dict[str, Any] | None:
    path = _doc_checkpoint_path(doc, doc_out_dir)
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def hydrate_from_doc_checkpoints(docs: list[dict], doc_out_dir: Path) -> None:
    """Reaproveita progresso salvo por documento quando disponível."""
    hit = 0
    for d in docs:
        prev = load_doc_checkpoint(d, doc_out_dir)
        if not prev:
            continue
        if prev.get("doc_id") != d.get("doc_id"):
            continue
        d.update({
            "pages": prev.get("pages"),
            "text_preview": prev.get("text_preview", ""),
            "extraction_method": prev.get("extraction_method"),
            "extraction_error": prev.get("extraction_error"),
            "catalog_entry": prev.get("catalog_entry"),
            "classification_error": prev.get("classification_error"),
        })
        hit += 1
    if hit:
        log.info("Loaded %d document checkpoints from %s", hit, doc_out_dir)


def ensure_doc_checkpoints(docs: list[dict], doc_out_dir: Path) -> None:
    """Garante arquivo checkpoint individual para todos os documentos da execução."""
    for d in docs:
        save_doc_checkpoint(d, doc_out_dir)


def apply_unified_equivalences(docs: list[dict]) -> dict[str, Any]:
    """Ajusta entradas com equivalências conhecidas e retorna índice unificado."""
    equivalence_index: dict[str, dict[str, Any]] = {}
    fixed_cf = 0
    for doc in docs:
        entry = doc.get("catalog_entry")
        if not entry:
            continue
        variables = entry.get("variables") or []
        for v in variables:
            native = v.get("native_name")
            cf = v.get("cf_standard_name")
            # LLM may return a list; take the first element
            if isinstance(cf, list):
                cf = cf[0] if cf else None
                v["cf_standard_name"] = cf
            if not cf and native:
                cf = _resolve_cf_from_registry(native)
                if cf:
                    v["cf_standard_name"] = cf
                    fixed_cf += 1

            if not cf:
                continue
            if not isinstance(cf, str):
                cf = str(cf)
                v["cf_standard_name"] = cf
            canon = VARIABLE_REGISTRY.get(cf)
            if canon:
                v.setdefault("category", canon.category.value)
                v.setdefault("physical_quantity", canon.physical_quantity.value)
                v.setdefault("thermodynamic_form", canon.thermodynamic_form.value)
                v.setdefault("framework", canon.framework.value)
                if canon.reference_pressure_dbar is not None:
                    v.setdefault("reference_pressure_dbar", canon.reference_pressure_dbar)

            item = equivalence_index.setdefault(
                cf,
                {
                    "cf_standard_name": cf,
                    "native_names": set(),
                    "source_files": set(),
                    "forms": set(),
                },
            )
            if native:
                item["native_names"].add(native)
            item["source_files"].add(doc["filename"])
            form = v.get("thermodynamic_form") or "unknown"
            fw = v.get("framework") or "unknown"
            ref = v.get("reference_pressure_dbar")
            if ref is None:
                item["forms"].add(f"{form}({fw})")
            else:
                item["forms"].add(f"{form}({fw}) ref={ref}")

    unified = {
        "resolved_cf_count": fixed_cf,
        "equivalences": {
            cf: {
                "cf_standard_name": data["cf_standard_name"],
                "native_names": sorted(data["native_names"]),
                "source_files": sorted(data["source_files"]),
                "forms": sorted(data["forms"]),
            }
            for cf, data in sorted(equivalence_index.items())
        },
    }
    log.info("Unified catalog adjustments: %d CF names resolved from aliases", fixed_cf)
    return unified


# ---------------------------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------------------------

def save_inventory(docs: list[dict], path: str) -> None:
    clean = [
        {k: v for k, v in d.items() if k not in {"text_preview", "legacy_doc_id"}}
        for d in docs
    ]
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean, f, ensure_ascii=False, indent=2, default=str)
    log.info("Inventory: %s", path)


def save_catalog_yaml(docs: list[dict], path: str, unified: dict[str, Any] | None = None) -> None:
    entries = []
    for doc in docs:
        entry = doc.get("catalog_entry")
        if not entry:
            continue
        entry["_source_file"] = doc["filename"]
        entries.append(entry)

    payload: dict[str, Any] = {"extracted_entries": entries}
    if unified is not None:
        payload["unified_catalog"] = unified

    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(payload, f,
                  default_flow_style=False, allow_unicode=True, sort_keys=False)
    log.info("Catalog YAML: %s", path)


# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

def _update_model(name: str) -> None:
    global LLM_MODEL
    LLM_MODEL = name


def main() -> int:
    parser = argparse.ArgumentParser(description="Doc triage -> catalog builder")
    parser.add_argument("--input-dir", "-i", required=True)
    parser.add_argument("--output-dir", "-o", default="./output",
                        help="Diretório de saída para todos os arquivos gerados (padrão: ./output)")
    parser.add_argument("--no-llm", action="store_true")
    parser.add_argument("--max-docs", type=int, default=None)
    parser.add_argument("--backend", choices=["anthropic", "ollama"], default="ollama")
    parser.add_argument("--model", default=LLM_MODEL)
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--log-level", default="INFO")

    args = parser.parse_args()
    logging.getLogger().setLevel(getattr(logging, args.log_level.upper(), logging.INFO))

    if args.model != LLM_MODEL:
        _update_model(args.model)
    elif args.backend == "ollama" and "claude" in LLM_MODEL:
        _update_model("qwen2.5:14b")

    log.info("=" * 60)
    log.info("Doc Triage -> Catalog Builder")
    log.info("=" * 60)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    doc_ckpt_dir = out_dir / "documents"
    doc_ckpt_dir.mkdir(parents=True, exist_ok=True)
    (doc_ckpt_dir / "extracted").mkdir(parents=True, exist_ok=True)
    (doc_ckpt_dir / "llm").mkdir(parents=True, exist_ok=True)
    inventory_path = str(out_dir / "catalog_inventory.json")
    yaml_path      = str(out_dir / "catalog_inventory.yaml")
    report_path    = str(out_dir / "catalog_inventory_correlation.txt")
    log.info("Output dir: %s", out_dir.resolve())
    log.info("Doc checkpoints: %s", doc_ckpt_dir.resolve())

    # 1. Discover — lista todos os arquivos na pasta
    all_files = discover_files(Path(args.input_dir))
    if args.max_docs:
        all_files = all_files[:args.max_docs]
    if not all_files:
        log.warning("No documents found in %s", args.input_dir)
        return 1

    # 2. Reconcile com checkpoint
    saved = load_inventory(inventory_path)
    docs, added, removed = reconcile(all_files, saved)
    hydrate_from_doc_checkpoints(docs, doc_ckpt_dir)

    if saved:
        if added:
            log.info("  New/modified files: %s", ", ".join(added))
        if removed:
            log.warning("  Removed files (not present in this run): %s", ", ".join(removed))

    ensure_doc_checkpoints(docs, doc_ckpt_dir)

    # 3. Checklist de status
    print_checklist(docs)

    # 4. Extração de texto — só arquivos pendentes
    scan_documents(docs, doc_out_dir=doc_ckpt_dir, inventory_path=inventory_path)
    # Salvar após extração para não perder trabalho em caso de interrupção
    save_inventory(docs, inventory_path)
    print_checklist(docs)

    # 5. Classify — only unclassified docs
    pending_llm = [
        d for d in docs
        if d.get("extraction_method")
        and d.get("catalog_entry") is None
        and not d.get("extraction_error")
    ]
    if not args.no_llm:
        if pending_llm:
            log.info("\nClassifying %d docs with %s (%s)", len(pending_llm), args.backend, LLM_MODEL)
            classify_all(
                pending_llm,
                args.backend,
                LLM_MODEL,
                args.ollama_url,
                doc_out_dir=doc_ckpt_dir,
                inventory_path=inventory_path,
                full_docs=docs,
            )
        else:
            log.info("\nAll docs already classified — skipping LLM step.")

    # 6. Checklist final
    print_checklist(docs)

    # 7. Correlate
    unified = apply_unified_equivalences(docs)
    log.info("Building correlation table...")
    occurrences = build_occurrence_table(docs)
    report = build_correlation_report(occurrences)
    print("\n" + report)

    # 8. Save final
    save_inventory(docs, inventory_path)
    save_catalog_yaml(docs, yaml_path, unified=unified)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    log.info("Correlation report: %s", report_path)

    log.info("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())