# metocean-manuals

Toolkit Python para catalogação e harmonização de fontes de dados meteorológico-oceanográficos (metocean). Parte do projeto **Cube Deep Water (CDW)** — pipeline de aquisição, harmonização e preparação de dados para visualização 3D.

---

## Visão geral

O problema central é que cada provedor organiza e nomeia seus dados de forma diferente:

- **HYCOM** exporta `water_temp` em °C (temperatura in-situ), com longitude 0–360
- **CMEMS** exporta `thetao` em °C (temperatura potencial), com longitude −180/+180
- **ERA5** exporta temperatura em Kelvin, pressão em Pascal, longitude 0–360
- **GEBCO** exporta `elevation` (oceano = valor negativo), enquanto modelos usam profundidade positiva

Este repositório resolve isso em dois níveis:

1. **Documentação técnica** (`docs/`) — referência cruzada de variáveis, conversões críticas e especificações de cada fonte
2. **Schema normalizado** (`catalog.py`) + **extração automática** (`doc_triage.py`) — modelo de dados com anotação termodinâmica completa e builder que usa LLM para popular o catálogo a partir de documentação

---

## Estrutura

```
metocean-manuals/
├── catalog.py              # Modelo de dados universal (Provider → ProductLine → Dataset → Variable)
├── doc_triage.py           # Extrai metadados de documentação via LLM e gera catálogo
└── docs/
    ├── 00-tech_specs_goal.md         # Especificação técnica do pipeline CDW
    ├── cdw_variable_cross_reference.md  # Tabela mestra de variáveis em 5 fontes
    ├── cdw_conversoes.md             # 14 conversões críticas documentadas
    ├── download_<fonte>_docs.py      # Scrapers de documentação por fonte
    ├── copernicus_docs/              # PUM e QUID do CMEMS
    ├── ecmwf_docs/                   # Documentação ERA5, IFS, ECMWF open data
    ├── era5_docs/
    ├── gebco_docs/                   # Grids 2019–2025, IBCAO, IBCSO
    ├── gfs_docs/
    ├── hycom_docs/
    └── icon_docs/                    # Modelo icosaédrico DWD (atmosfera, oceano, ondas)
```

---

## Fontes suportadas

| Fonte | Tipo | Resolução | Variáveis-chave |
|---|---|---|---|
| **CMEMS** | forecast, reanalysis | 1/12° | thetao, so, uo, vo, zos, siconc |
| **HYCOM** | analysis, forecast | 0.08° | water_temp, salinity, water_u/v, surf_el |
| **GFS** | forecast | 0.25° | TMP, UGRD, VGRD, PRMSL, ICEC |
| **ERA5** | reanalysis | 0.25° / 0.5° | t2m, u10, v10, msl, swh, sst |
| **GEBCO** | static (batimetria) | 15 arc-sec | elevation |
| **ICON** | forecast | R2B6–R2B9 | atmosfera, oceano, ondas |
| **ROMS** | forecast, hindcast | curvilínear | configurável por domínio |

---

## catalog.py — Modelo de dados

Hierarquia de 3 camadas:

```
Provider
└── ProductLine
    └── Dataset
        ├── Variable[]     ← com anotação termodinâmica completa
        ├── Grid
        ├── TemporalSpec
        ├── VerticalSpec
        └── AccessMethod[]
```

### Anotação termodinâmica de variáveis

A chave de unificação é o **CF standard_name**. Além disso, cada `Variable` carrega:

- `physical_quantity` — grandeza base (TEMPERATURE, SALINITY, WAVE_HEIGHT, ...)
- `thermodynamic_form` — forma termodinâmica (in_situ, potential, conservative, practical, absolute, ...)
- `reference_state` — pressão de referência e framework (EOS-80 ou TEOS-10)

Isso permite detectar incompatibilidades silenciosas — por exemplo, `thetao` (CMEMS, temperatura potencial EOS-80) vs `water_temp` (HYCOM, temperatura in-situ) são a mesma grandeza mas formas distintas; a mistura direta introduz erro de ~0.5°C a 5000 m.

O método `Variable.is_compatible_with()` retorna um `VariableCompatibility` indicando se a conversão é possível e qual função usar (ex: `gsw.pt_from_t`, `gsw.SA_from_SP`).

### VARIABLE_REGISTRY

Dicionário pré-populado de variáveis canônicas com todos os aliases conhecidos por fonte:

```python
from catalog import VARIABLE_REGISTRY

canon = VARIABLE_REGISTRY["sea_water_potential_temperature"]
# canon.aliases → {"thetao": ["cmems"], "theta": ["nemo"], ...}
```

---

## doc_triage.py — Extração automática de metadados

Varre documentos (`md`, `pdf`, `txt`, `rst`) em um diretório, extrai um preview de texto e chama um LLM para preencher o schema do `catalog.py`.

### Fluxo de execução

A cada execução o script passa pelas etapas abaixo. Cada etapa só processa o que ainda não foi feito — pode ser interrompida e retomada sem retrabalho.

```
1. Discover     — lista todos os arquivos suportados na pasta indicada
2. Reconcile    — compara com o checkpoint salvo:
                    • arquivos novos ou modificados → entram na fila
                    • arquivos removidos do disco   → aviso (mantidos no inventário)
3. Checklist    — imprime status de cada arquivo antes de começar:
                    [x] extraído  [x] LLM  |  [ ] pendente  |  [!] erro
4. Extração     — extrai preview de texto apenas dos arquivos ainda não extraídos
                  salva catalog_inventory.json (checkpoint pós-extração)
5. LLM          — classifica apenas os arquivos extraídos sem catalog_entry ainda
6. Checklist    — atualiza status após cada fase
7. Correlação   — cruza variáveis entre fontes e detecta incompatibilidades
8. Save final   — grava catalog_inventory.json, .yaml e correlation_report.txt
```

**Exemplo de saída do checklist:**

```
────────────────────────────────────────────────────────────
  Arquivo                           Extração  LLM
────────────────────────────────────────────────────────────
  ERA5__data_documentation.md       [x]       [x]
  ECMWF_IFS_documentation_index.md  [x]       [x]
  GEBCO_2024_grid_docs.md           [x]       [ ]
  ICON_ocean.md                     [ ]       [ ]
────────────────────────────────────────────────────────────
  Total: 4  |  Extraídos: 3/4  |  LLM: 2/4
```

```bash
# 1ª execução: extração + LLM
python doc_triage.py -i ./docs --backend ollama --model qwen2.5:14b

# Diretório de saída customizado
python doc_triage.py -i ./docs --backend ollama --output-dir ./results

# Interrompida? Rode o mesmo comando — retoma de onde parou
python doc_triage.py -i ./docs --backend ollama --model qwen2.5:14b

# Só extração de texto, sem LLM
python doc_triage.py -i ./docs --no-llm

# Limitar documentos processados
python doc_triage.py -i ./docs --backend ollama --model qwen2.5:14b --max-docs 10

# Com Anthropic
python doc_triage.py -i ./docs --backend anthropic
```

### Saídas

Todos os arquivos são gravados no diretório `--output-dir` (padrão: `./output`), criado automaticamente se não existir.

| Arquivo | Conteúdo |
|---|---|
| `catalog_inventory.json` | Metadados extraídos por documento |
| `catalog_inventory.yaml` | Entradas no formato `catalog.py` |
| `catalog_inventory_correlation.txt` | Relatório de correlação cruzada entre fontes |

Checkpoints por documento (auditoria e retomada):

- `documents/<doc_id>.json` — estado consolidado mais recente do documento
- `documents/extracted/<doc_id>.json` — snapshot após a etapa de extração
- `documents/llm/<doc_id>.json` — snapshot após a etapa de classificação LLM

### Relatório de correlação

O relatório agrupa variáveis pelo CF standard_name e identifica:

- **Variáveis com múltiplas fontes** — candidatas a fallback automático
- **Incompatibilidades termodinâmicas** — formas distintas da mesma grandeza que precisam de conversão antes da comparação
- **Variáveis sem fallback** — encontradas em apenas uma fonte
- **Variáveis não resolvidas** — sem CF name reconhecido

---

## Conversões críticas

Documentadas em [docs/cdw_conversoes.md](docs/cdw_conversoes.md). As mais importantes:

| Conversão | Fontes afetadas | Operação |
|---|---|---|
| Temperatura K → °C | ERA5, GFS | `t - 273.15` |
| Pressão Pa → hPa | ERA5, GFS | `p / 100` |
| Longitude 0–360 → ±180 | GFS, HYCOM, ERA5 | `((lon + 180) % 360) - 180` |
| Elevação → profundidade | GEBCO | `depth = -elevation` |
| Época temporal CMEMS | CMEMS | horas desde 1950-01-01 |
| Época temporal HYCOM | HYCOM | horas desde 2000-01-01 |

---

## Dependências

```bash
pip install pyyaml pypdf pdfplumber   # extração de texto
pip install anthropic                  # opcional: backend Anthropic
# Ollama: https://ollama.com (modelo recomendado: qwen2.5:14b)
```

---

## Contexto

Este repositório é a camada de documentação e catalogação do pipeline CDW. Os módulos de download (`download_<fonte>_docs.py`) rasparão a documentação oficial de cada provedor para manter o catálogo atualizado.
