# CDW Data Pipeline — Especificação Técnica

**Versão:** 0.1  
**Data:** 2026-04-09  
**Projeto:** Cube Deep Water — Módulo de Aquisição, Harmonização e Preparação de Dados

---

## 1. Objetivo

Pipeline Python para download, harmonização e preparação de dados oceanográficos multi-fonte. Produz uma base unificada pronta para consumo pelo sistema de visualização 3D Cube Deep Water (poc-trame).

**Dois modos de operação:**

- **Carga inicial (full load):** download completo do período configurado
- **Atualização incremental (daily):** execução diária que baixa apenas o delta desde a última atualização

**Requisito adicional:** capacidade de gerar datasets recortados por **domínio nomeado** (região geográfica ou evento histórico), cada um com bbox, período, profundidades e fontes configuráveis.

---

## 2. Fontes de Dados

### 2.1 Classificação por tipo de produto

Cada fonte fornece um ou mais **tipos de produto**. A distinção forecast vs. reanalysis afeta a organização dos dados, a frequência de atualização e a política de retenção.

| Fonte | Tipo(s) de produto | Resolução temporal | Resolução espacial | Grade |
|---|---|---|---|---|
| **HYCOM** | `forecast`, `analysis` | 3h | 0.08° | Regular lat/lon |
| **CMEMS** | `forecast`, `reanalysis` | 1h–diário | 1/12° (~0.083°) | Regular lat/lon |
| **ROMS** | `forecast`, `hindcast` | variável (output do modelo) | curvilinear | Curvilinear (Arakawa C) |
| **GFS** | `forecast` | 1h (F001–F120), 3h (F120+) | 0.25° | Regular lat/lon |
| **ERA5** | `reanalysis` | 1h (superfície), 6h (pressão) | 0.25° (atmo), 0.5° (ondas) | Regular lat/lon |
| **CODAR** | `observation` | 1h | ~6 km (HF-radar) | Irregular (pontos) |
| **Boias** | `observation` | desconhecido | pontual | Ponto fixo |
| **Fundeios** | `observation` | desconhecido | pontual | Ponto fixo (perfil vertical) |
| **GEBCO** | `static` | — | 15 arc-sec (~450m) | Regular lat/lon |

### 2.2 Datasets por fonte e tipo de produto

**HYCOM (ESPC-D-V02)**

| Produto | Dataset | Variáveis |
|---|---|---|
| `analysis` | Saída de análise (nowcast) | temperature, salinity, water_u, water_v, ssh |
| `forecast` | Previsão 8 dias | mesmas variáveis |

- Coordenada vertical: 40 níveis Z fixos (0–5000 m)
- Longitude: 0–360 (converter para ±180)
- Época temporal: horas desde 2000-01-01
- Dados compactados: int16 com scale_factor + add_offset
- Acesso: OPeNDAP / NCSS (TDS HYCOM)

**CMEMS (Copernicus Marine)**

| Produto | Dataset | Variáveis |
|---|---|---|
| `forecast` | GLOBAL_ANALYSISFORECAST_PHY_001_024 | thetao, so, uo, vo, zos |
| `reanalysis` | GLOBAL_MULTIYEAR_PHY_001_030 | mesmas variáveis |

- Coordenada vertical: 50 níveis Z (0.49–5728 m)
- Longitude: −180/+180 (nativa — sem conversão necessária)
- Época temporal: horas desde 1950-01-01
- Fill values: três sentinelas (9.97e+36, 1.0e+20, −9999)
- Temperatura: potencial (referência para comparações)
- Acesso: Copernicus Marine API (copernicusmarine toolbox)

**ROMS**

| Produto | Dataset | Variáveis |
|---|---|---|
| `forecast` | Rodada operacional (ex: Cronos) | u, v, w, temp, salt, zeta |
| `hindcast` | Rodada histórica / reprocessamento | mesmas variáveis |

- Coordenada vertical: N níveis sigma (S-coordinate, terrain-following)
- Conversão S→Z obrigatória (Vtransform 1 ou 2)
- Grade curvilinear: eta_rho × xi_rho (Arakawa C-grid)
- u/v em sub-grades deslocadas → interpolação para rho-grid
- Retenção mínima: 30 dias (análise de mesoescala)
- Acesso: SFTP/HTTP/OPeNDAP (depende do operador)

**GFS (NOAA)**

| Produto | Dataset | Variáveis |
|---|---|---|
| `forecast` | GFS 0.25° (ciclos 00/06/12/18Z) | UGRD (u10), VGRD (v10), PRMSL |

- Longitude: 0–360 (converter para ±180)
- Temperatura: Kelvin (converter para °C)
- Pressão: Pascal (converter para hPa)
- valid_time = reference_time + forecast_step (reconstruir)
- Variáveis de fluxo: acumuladas desde inicialização (diferenciar steps)
- Acesso: NOAA AWS (s3://noaa-gfs-bdp-pds/)

**ERA5 (ECMWF)**

| Produto | Dataset | Variáveis |
|---|---|---|
| `reanalysis` | reanalysis-era5-single-levels | u10, v10, msl, sst, swh |

- Longitude: 0–360 (converter para ±180)
- Temperatura: Kelvin (converter para °C)
- Pressão: Pascal (converter para hPa)
- Épocas duplas: 1900-01-01 (legado) vs 1970-01-01 (novo CDS)
- Máscara terra-mar: fracionária (aplicar limiar < 0.5)
- Grade de ondas: separada 0.5° (requer reinterpolação para 0.25° se combinada com atmo)
- Acesso: CDS API (cdsapi)

**CODAR (HF-Radar)**

| Produto | Dataset | Variáveis |
|---|---|---|
| `observation` | Totais RDJS | u_surface, v_surface |

- Grade irregular (pontos espalhados ~6 km)
- Formato: .tuv (tabular, texto)
- QC flags embutidos
- Acesso: Azure Blob Storage

**Boias**

| Produto | Dataset | Variáveis |
|---|---|---|
| `observation` | a definir | a definir |

- Séries temporais em ponto fixo

**Fundeios (Moorings)**

| Produto | Dataset | Variáveis |
|---|---|---|
| `observation` | a definir | a definir |

- Perfis verticais em ponto fixo: dimensões (time, depth)

**GEBCO**

| Produto | Dataset | Variáveis |
|---|---|---|
| `static` | GEBCO 2024 grid | elevation |

- Elevação com sinal invertido (oceano = negativo → converter para profundidade positiva)
- Download manual, recorte por bbox
- Acesso: https://download.gebco.net/

---

## 3. Conversões Críticas por Fonte

Referência completa das transformações que cada harmonizer deve aplicar.

### 3.1 Unidades físicas

| Conversão | Fontes | Implementação |
|---|---|---|
| Temperatura: <br> K → °C (−273.15) | ERA5, GFS | `converters/temperature.py` |
| Pressão: <br> Pa → hPa (÷100) | ERA5, GFS | `converters/pressure.py` |
| Batimetria: <br> inverter sinal | GEBCO | `converters/depth.py` |
| Temperatura:  <br>  in-situ → potencial (TEOS-10) | HYCOM ↔ CMEMS | `converters/temperature.py` |

### 3.2 Coordenadas espaciais

| Conversão | Fontes | Implementação |
|---|---|---|
| Longitude: <br>  0–360 → ±180 | GFS, HYCOM, ERA5 | `converters/longitude.py` |
| Grade de ondas: <br>  reinterpolação 0.5° → 0.25° | ERA5 | `harmonizers/era5.py` |
| S-coordinate → Z métrico (Vtransform 1/2) | ROMS | `converters/depth.py` |
| u/v sub-grade → rho-grid (Arakawa C) | ROMS | `harmonizers/roms.py` |

### 3.3 Coordenadas temporais

| Conversão | Fontes | Implementação |
|---|---|---|
| Época: horas desde 1950-01-01 | CMEMS | `converters/time.py` |
| Época: horas desde 2000-01-01 | HYCOM | `converters/time.py` |
| Épocas duplas: 1900 vs 1970 | ERA5 | `converters/time.py` |
| valid_time = ref_time + forecast_step | GFS | `converters/time.py` |
| Fluxos acumulados: diferenciar steps | GFS | `harmonizers/gfs.py` |

### 3.4 Máscaras e valores ausentes

| Conversão | Fontes | Implementação |
|---|---|---|
| Descompactar int16 (scale × factor + offset) | HYCOM | `converters/masks.py` |
| Tratar 3 fill values (9.97e+36, 1.0e+20, −9999) | CMEMS | `converters/masks.py` |
| Máscara terra-mar fracionária → limiar | ERA5 | `converters/masks.py` |

---

## 4. Configuração de Domínio

Cada domínio é definido por um arquivo YAML em `domains/`. Domínios podem representar regiões geográficas permanentes ou eventos históricos delimitados no tempo.

### 4.1 Esquema do domain.yaml

```yaml
# domains/{nome}.yaml
inherit: _base.yaml              # herda defaults

name: "Nome legível do domínio"
description: "Descrição opcional"

# --- Recorte espacial ---
bbox:
  lon_min: -42.5
  lon_max: -39.0
  lat_min: -24.5
  lat_max: -21.0

# --- Recorte vertical ---
depth:
  unit: meters                   # meters | sigma
  min: 0
  max: 3000

# --- Recorte temporal ---
time:
  mode: rolling                  # rolling | fixed
  rolling_days: 30               # para mode=rolling: últimos N dias
  # start: "2004-03-24"          # para mode=fixed: data início
  # end: "2004-03-30"            # para mode=fixed: data fim

# --- Política de retenção ---
retention:
  default_days: 45               # dias a manter por padrão
  roms: 60                       # override por fonte
  buoys: 180
  moorings: 365

# --- Fontes habilitadas ---
sources:
  hycom:
    enabled: true
    products: [analysis, forecast]       # quais tipos de produto baixar
    variables: [temperature, salinity, water_u, water_v, ssh]

  cmems:
    enabled: true
    products: [forecast, reanalysis]
    variables: [thetao, so, uo, vo, zos]

  roms:
    enabled: true
    products: [forecast]
    provider: cronos
    url: "sftp://modelo.server/output/his/"
    file_pattern: "cronos_his_{date:%Y-%m-%d}.nc"
    variables: [u, v, w, temp, salt, zeta]
    min_retention_days: 30
    depth:
      unit: sigma
      min: 0
      max: -1

  gfs:
    enabled: true
    products: [forecast]
    variables: [wind_u, wind_v]
    depth:
      unit: meters
      min: 0
      max: 0

  era5:
    enabled: true
    products: [reanalysis]
    variables: [u10, v10, msl]
    depth:
      unit: meters
      min: 0
      max: 0

  codar:
    enabled: true
    products: [observation]
    depth:
      unit: meters
      min: 0
      max: 0

  buoys:
    enabled: true
    products: [observation]
    stations:
      - id: vitoria
        name: "Boia de Vitória"
        lat: -20.19
        lon: -38.55
        provider: pnboia
      - id: cabo_frio
        name: "Boia Cabo Frio"
        lat: -23.63
        lon: -42.18
        provider: pnboia
    variables: [sst, pressure, wind_speed, wind_dir, wave_height]
    depth:
      unit: meters
      min: 0
      max: 0

  moorings:
    enabled: true
    products: [observation]
    deployments:
      - id: adcp_campos_2026
        name: "ADCP Campos P-51"
        lat: -22.35
        lon: -40.10
        depth: 1200
        provider: local
        path: "moorings/adcp_campos_2026.nc"
    variables: [u, v, temperature, salinity, pressure]

  gebco:
    enabled: true
    products: [static]
    depth: null

# --- Projeção para CDW ---
origin_lat: -22.75
origin_lon: -40.75
```

### 4.2 Herança via _base.yaml

```yaml
# domains/_base.yaml
depth:
  unit: meters
  min: 0
  max: 5000

time:
  mode: rolling
  rolling_days: 30

retention:
  default_days: 45

sources:
  hycom:
    enabled: false
    products: [analysis, forecast]
    variables: [temperature, salinity, water_u, water_v, ssh]
  cmems:
    enabled: false
    products: [forecast, reanalysis]
    variables: [thetao, so, uo, vo, zos]
  roms:
    enabled: false
    products: [forecast]
    variables: [u, v, w, temp, salt, zeta]
    min_retention_days: 30
    depth:
      unit: sigma
      min: 0
      max: -1
  gfs:
    enabled: false
    products: [forecast]
    variables: [wind_u, wind_v]
    depth:
      unit: meters
      min: 0
      max: 0
  era5:
    enabled: false
    products: [reanalysis]
    variables: [u10, v10, msl]
    depth:
      unit: meters
      min: 0
      max: 0
  codar:
    enabled: false
    products: [observation]
    depth:
      unit: meters
      min: 0
      max: 0
  buoys:
    enabled: false
    products: [observation]
    depth:
      unit: meters
      min: 0
      max: 0
  moorings:
    enabled: false
    products: [observation]
  gebco:
    enabled: false
    products: [static]
    depth: null
```

### 4.3 Exemplos de domínios

**Região permanente — monitoramento operacional:**

```yaml
# domains/bacia_campos.yaml
inherit: _base.yaml
name: "Bacia de Campos"
bbox: { lon_min: -42.5, lon_max: -39.0, lat_min: -24.5, lat_max: -21.0 }
depth: { unit: meters, min: 0, max: 3000 }
time: { mode: rolling, rolling_days: 30 }
sources:
  hycom: { enabled: true }
  cmems: { enabled: true }
  roms: { enabled: true, provider: cronos, url: "sftp://..." }
  gfs: { enabled: true }
  codar: { enabled: true }
  buoys: { enabled: true, stations: [...] }
  moorings: { enabled: true, deployments: [...] }
  gebco: { enabled: true }
origin_lat: -22.75
origin_lon: -40.75
```

**Evento histórico — análise pontual:**

```yaml
# domains/catarina_2004.yaml
inherit: _base.yaml
name: "Furacão Catarina — Março 2004"
description: "Ciclone tropical no Atlântico Sul"
bbox: { lon_min: -52.0, lon_max: -38.0, lat_min: -32.0, lat_max: -24.0 }
depth: { unit: meters, min: 0, max: 500 }
time: { mode: fixed, start: "2004-03-20", end: "2004-04-01" }
sources:
  era5: { enabled: true, variables: [u10, v10, msl, sst, swh] }
  cmems: { enabled: true, products: [reanalysis] }   # só reanálise para evento passado
  gebco: { enabled: true }
origin_lat: -28.0
origin_lon: -45.0
```

**Região ampla — vista geral:**

```yaml
# domains/margem_equatorial.yaml
inherit: _base.yaml
name: "Margem Equatorial Brasileira"
bbox: { lon_min: -52.0, lon_max: -30.0, lat_min: -5.0, lat_max: 5.0 }
depth: { unit: meters, min: 0, max: 5000 }
time: { mode: rolling, rolling_days: 30 }
sources:
  hycom: { enabled: true }
  cmems: { enabled: true }
  gfs: { enabled: true }
  era5: { enabled: true }
  gebco: { enabled: true }
origin_lat: 0.0
origin_lon: -41.0
```

---

## 5. Estrutura de Pastas

```
cube-data-pipeline/
│
├── domains/                              # configuração de domínios
│   ├── _base.yaml                        # defaults herdados por todos
│   ├── campos_basin.yaml
│   ├── equatorial_margin.yaml
│   ├── catarina_2004.yaml
│   └── full_south_atlantic.yaml
│
├── downloaders/                          # aquisição de dados brutos
│   ├── base.py                           # BaseDownloader(domain, source_config)
│   ├── hycom.py                          # OPeNDAP / NCSS
│   ├── cmems.py                          # Copernicus Marine API
│   ├── roms.py                           # SFTP / HTTP / OPeNDAP
│   ├── gfs.py                            # NOAA AWS
│   ├── era5.py                           # CDS API
│   ├── codar.py                          # Azure Blob
│   ├── buoys.py                          # PNBOIA, PIRATA, SIMCOSTA
│   ├── moorings.py                       # arquivos locais (registra/valida)
│   └── gebco.py                          # estático, recorte por bbox
│
├── harmonizers/                          # conversão e normalização
│   ├── base.py                           # BaseHarmonizer — interface + log
│   ├── hycom.py                          # lon, epoch 2000, scale/offset, temp in-situ
│   ├── cmems.py                          # epoch 1950, fill values, temp potencial
│   ├── roms.py                           # S→Z, u/v→rho, grade curvilinear
│   ├── gfs.py                            # lon, K→°C, Pa→hPa, valid_time
│   ├── era5.py                           # lon, K→°C, épocas duplas, lsm
│   ├── codar.py                          # .tuv→xarray, QC flags
│   ├── buoys.py                          # unificar formatos, QC, interpolação
│   ├── moorings.py                       # perfis verticais, bins ADCP
│   ├── gebco.py                          # inversão sinal
│   └── converters/                       # funções puras reutilizáveis
│       ├── longitude.py                  # wrap_180(), wrap_360()
│       ├── temperature.py                # kelvin_to_celsius(), insitu_to_potential()
│       ├── pressure.py                   # pa_to_hpa()
│       ├── time.py                       # normalize_epoch(), gfs_valid_time()
│       ├── depth.py                      # elevation_to_depth(), s_to_z()
│       ├── masks.py                      # fill_values(), land_sea_mask()
│       └── point_data.py                 # dedup, QC flags, bin averaging
│
├── store/                                # persistência da base unificada
│   ├── writer.py                         # grava harmonizado (formato TBD)
│   ├── catalog.py                        # índice: domain × source × product × var × período
│   ├── schemas.py                        # validação CF: dims, ranges, unidades
│   ├── inventory.py                      # cobertura temporal, gaps
│   └── retention.py                      # política de retenção por fonte/domain
│
├── exporters/                            # preparação para renderização CDW
│   ├── base.py                           # BaseExporter
│   ├── vtk_rectilinear.py               # grade regular → .vtr (HYCOM, CMEMS, GFS, ERA5, GEBCO)
│   ├── vtk_structured.py                # grade curvilinear → .vts (ROMS)
│   ├── vtk_polydata.py                  # pontos irregulares → .vtp (CODAR, boias, fundeios)
│   ├── pvd_writer.py                    # .pvd com timesteps
│   └── cdw_project.py                   # gera .cdw apontando para VTK exportado
│
├── pipeline/                             # orquestração
│   ├── runner.py                         # download → harmonize → store → export
│   ├── modes.py                          # FULL_LOAD | INCREMENTAL | REPROCESS | BACKFILL
│   ├── scheduler.py                      # cron / watchdog para modo diário
│   └── cli.py                            # interface de linha de comando
│
├── data/                                 # gitignore — tudo gerado
│   └── {domain}/                         # ex: campos_basin/
│       ├── raw/                          # downloads brutos, intocados
│       │   ├── hycom/
│       │   │   ├── forecast/
│       │   │   └── analysis/
│       │   ├── cmems/
│       │   │   ├── forecast/
│       │   │   └── reanalysis/
│       │   ├── roms/
│       │   │   ├── forecast/
│       │   │   └── hindcast/
│       │   ├── gfs/
│       │   │   └── forecast/
│       │   ├── era5/
│       │   │   └── reanalysis/
│       │   ├── codar/
│       │   │   └── observation/
│       │   ├── buoys/
│       │   │   └── observation/
│       │   ├── moorings/
│       │   │   └── observation/
│       │   └── gebco/
│       │       └── static/
│       │
│       ├── harmonized/                   # pós-conversão, coordenadas unificadas
│       │   ├── ocean_3d/                 # HYCOM + CMEMS (grade regular, níveis Z)
│       │   │   ├── forecast/
│       │   │   └── reanalysis/
│       │   ├── ocean_3d_roms/            # ROMS (grade curvilinear, pós S→Z)
│       │   │   ├── forecast/
│       │   │   └── hindcast/
│       │   ├── wind/                     # GFS + ERA5
│       │   │   ├── forecast/
│       │   │   └── reanalysis/
│       │   ├── surface_currents/         # CODAR
│       │   │   └── observation/
│       │   ├── observations/             # boias + fundeios
│       │   │   └── observation/
│       │   └── bathymetry/               # GEBCO
│       │       └── static/
│       │
│       ├── vtk/                          # pronto para CDW consumir
│       │   ├── forecast/
│       │   │   ├── hycom_3d.pvd
│       │   │   ├── cmems_3d.pvd
│       │   │   ├── roms_3d.pvd
│       │   │   ├── gfs_wind.pvd
│       │   │   └── timesteps/
│       │   ├── reanalysis/
│       │   │   ├── cmems_3d.pvd
│       │   │   ├── era5_wind.pvd
│       │   │   └── timesteps/
│       │   ├── hindcast/
│       │   │   ├── roms_3d.pvd
│       │   │   └── timesteps/
│       │   ├── analysis/
│       │   │   ├── hycom_3d.pvd
│       │   │   └── timesteps/
│       │   ├── observation/
│       │   │   ├── codar_surface.pvd
│       │   │   ├── buoys.pvd
│       │   │   ├── moorings.pvd
│       │   │   └── timesteps/
│       │   └── static/
│       │       └── gebco_bathy.vtr
│       │
│       └── projects/                     # .cdw gerados automaticamente
│           ├── campos_basin_forecast.cdw
│           ├── campos_basin_reanalysis.cdw
│           └── campos_basin_full.cdw     # todas as camadas combinadas
│
├── docs/
│   ├── cdw_conversoes.md
│   ├── cdw_variable_cross_reference.md
│   ├── architecture.md
│   └── sources/
│       ├── hycom_api_reference.md
│       ├── copernicus_api_reference.md
│       ├── gfs_api_reference.md
│       ├── era5_api_reference.md
│       └── codar_api_reference.md
│
├── tests/
│   ├── test_converters/
│   ├── test_harmonizers/
│   ├── test_exporters/
│   └── fixtures/                         # NetCDF sintéticos pequenos
│
├── pyproject.toml
├── requirements.txt
└── Makefile
```

---

## 6. Organização de Dados: forecast vs. reanalysis

### 6.1 Princípio

O eixo **product_type** (forecast, reanalysis, analysis, hindcast, observation, static) é um nível de organização dentro de cada fonte e dentro dos dados harmonizados. A mesma variável física (ex: temperatura oceânica) pode existir tanto como forecast do HYCOM quanto como reanalysis do CMEMS, e ambos são preservados separadamente.

### 6.2 Tipos de produto

| product_type | Significado | Fontes | Atualização |
|---|---|---|---|
| `forecast` | Previsão a partir de agora | HYCOM, CMEMS, ROMS, GFS | Diária (ciclos operacionais) |
| `analysis` | Nowcast / assimilação de dados | HYCOM | Diária |
| `reanalysis` | Re-processamento histórico com dados assimilados | CMEMS, ERA5 | ~5 dias de atraso |
| `hindcast` | Rodada ROMS com forçantes históricas | ROMS | Sob demanda |
| `observation` | Medição direta (in-situ ou remota) | CODAR, boias, fundeios | Tempo real ou near-real-time |
| `static` | Dado estático, sem dimensão temporal | GEBCO | Atualização anual |

### 6.3 Implicações na organização

**raw/**: separado por `{source}/{product_type}/` — permite reter análise e forecast do mesmo modelo simultaneamente.

**harmonized/**: separado por domínio físico e product_type — `ocean_3d/forecast/`, `ocean_3d/reanalysis/`. Isso permite que o CDW carregue, por exemplo, apenas a camada de reanalysis para validação contra observações.

**vtk/**: separado por product_type — cada tipo gera seus próprios .pvd e timesteps. O exportador `cdw_project.py` gera .cdw separados para cada combinação útil (forecast-only, reanalysis-only, observações, ou all-layers).

### 6.4 Cenários de uso

| Cenário | Fontes/produtos carregados |
|---|---|
| Briefing operacional | ROMS forecast + GFS forecast + CODAR obs + boias obs |
| Validação de modelo | ROMS forecast + CMEMS reanalysis + boias obs + fundeios obs |
| Análise de evento histórico | CMEMS reanalysis + ERA5 reanalysis + GEBCO |
| Monitoramento costeiro | CODAR obs + boias obs + GFS forecast + GEBCO |

---

## 7. CLI e Modos de Execução

### 7.1 Comandos

```bash
# Carga completa de um domínio
cdw-data run campos_basin --mode full

# Atualização incremental (diária)
cdw-data run campos_basin --mode incremental

# Reprocessar harmonização sem re-download
cdw-data run campos_basin --mode reprocess

# Backfill: preencher lacunas em período específico
cdw-data run campos_basin --mode backfill --start 2026-03-01 --end 2026-03-15

# Status / inventário
cdw-data status campos_basin
cdw-data status campos_basin --source hycom --product forecast

# Exportar VTK a partir de dados já harmonizados
cdw-data export campos_basin

# Listar domínios configurados
cdw-data domains

# Scheduler: executar modo incremental diariamente
cdw-data schedule campos_basin --cron "0 6 * * *"
```

### 7.2 Modos de execução

| Modo | Download | Harmonize | Store | Export | Quando usar |
|---|---|---|---|---|---|
| `FULL_LOAD` | todo o período | tudo | tudo | tudo | Primeira vez, novo domínio |
| `INCREMENTAL` | só delta | só novos | append | atualiza .pvd | Diário |
| `REPROCESS` | não | tudo | reescreve | tudo | Mudou lógica de harmonização |
| `BACKFILL` | período específico | só período | merge | atualiza .pvd | Preencher gaps |

---

## 8. Pipeline de Execução

Fluxo para cada fonte habilitada dentro de um domínio:

```
1. Ler domain config (bbox, depth, time, sources)
2. Para cada source habilitada:
   a. Para cada product_type habilitado:
      i.   DOWNLOAD: baixar dados brutos → data/{domain}/raw/{source}/{product}/
      ii.  HARMONIZE: aplicar conversões da fonte → dados normalizados
      iii. STORE: gravar em data/{domain}/harmonized/{physical_domain}/{product}/
      iv.  EXPORT: converter para VTK → data/{domain}/vtk/{product}/
3. Gerar .cdw combinados → data/{domain}/projects/
4. Atualizar catálogo e inventário
5. Aplicar política de retenção (apagar dados fora da janela)
```

| etapa | path | descrição |
|---|---|---|
| DOWNLOAD | data/`domain`/raw/`source`/`product`/ | Baixar dados brutos da fonte |
| HARMONIZE | data/`domain`/harmonized/`physical_domain`/`product`/ | Aplicar conversões e normalizações |
| STORE | data/`domain`/harmonized/`physical_domain`/`product`/ | Armazenar dados harmonizados |
| EXPORT | data/`domain`/vtk/`product`/ | Converter para VTK |
| PROJECT | data/`domain`/projects/ | Gerar .cdw combinados |
| CATALOG | data/`domain`/catalog/ | Atualizar catálogo e inventário |
| RETENTION | data/`domain`/ | Aplicar política de retenção (apagar dados fora da janela) |


### 8.1 Contrato de harmonização

Todo dado harmonizado deve satisfazer:

| Propriedade | Valor |
|---|---|
| Longitude | −180 a +180 |
| Latitude | ordem S→N |
| Profundidade | metros, positivo para baixo (exceto sigma quando `depth.unit: sigma`) |
| Tempo | `datetime64[ns]` UTC, com `calendar: gregoriano` |
| Temperatura | °C |
| Salinidade | PSU |
| Correntes | m/s |
| Pressão | hPa |
| Fill value | NaN (float) ou masked array |
| Metadados | CF attributes preservados: `standard_name`, `units`, `source`, `product_type` |

---

## 9. Decisões em Aberto

| # | Decisão | Opções | Impacto |
|---|---|---|---|
| 1 | Formato do `harmonized/` | Zarr / NetCDF / Parquet | Performance de I/O, lazy loading |
| 2 | Nível de paralelismo dos downloads | Sequencial / asyncio / multiprocessing | Tempo de carga inicial |
| 3 | Como lidar com overlap temporal forecast/analysis | Sobrescrever / manter ambos / flag preferência | Espaço em disco, complexidade |
| 4 | Frequência de limpeza por retenção | Junto com incremental / job separado | Complexidade do scheduler |
| 5 | Provider de boias (PNBOIA API) | Scraping / API oficial / download manual | Robustez do downloader |
| 6 | Deploy do scheduler | Cron local / systemd timer / Docker + cron | Portabilidade |