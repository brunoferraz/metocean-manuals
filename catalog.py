"""
catalog.py — Modelo de dados universal para catálogo de produtos oceanográficos.

Problema central:
    Cada provider (CMEMS, NOAA, ECMWF, GEBCO, ...) organiza seus dados de forma
    diferente: "products", "dataset_ids", "collections", "experiments". Cada modelo
    nomeia variáveis de modo distinto (thetao vs temperature vs temp vs TEMP).
    Resoluções, grids, coordenadas verticais e métodos de acesso variam.

Solução:
    Um schema normalizado com 3 camadas:
    
    1. CATALOG LAYER — o que existe no mundo (fontes, produtos, variáveis)
    2. MAPPING LAYER — tradução entre nomes locais e padrões CF
    3. DOMAIN LAYER — o que eu quero (já existe no seu _base.yaml)

    A chave de unificação é o CF standard_name: qualquer variável de qualquer
    fonte é mapeada para um conceito físico padronizado.

Hierarquia do catálogo:

    Provider
    └── ProductLine
        └── Dataset
            ├── Variable[]
            ├── Grid
            ├── TemporalSpec
            ├── VerticalSpec
            └── AccessMethod[]

Uso:
    # Carregar catálogo
    catalog = load_catalog("catalog/")
    
    # Buscar todos os datasets que oferecem temperatura
    matches = catalog.find_datasets(cf_standard_name="sea_water_potential_temperature")
    
    # Buscar datasets com cobertura no South Atlantic
    matches = catalog.find_datasets(covers_bbox={"lon_min": -70, "lon_max": 20, ...})
    
    # Comparar variáveis equivalentes entre fontes
    equiv = catalog.find_equivalences("sea_surface_wave_significant_height")
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# =============================================================================
# ENUMS — taxonomia fixa
# =============================================================================

class ProductType(str, Enum):
    """Classificação temporal/funcional do produto."""
    FORECAST = "forecast"
    ANALYSIS = "analysis"           # best estimate com assimilação
    REANALYSIS = "reanalysis"       # reanálise histórica
    HINDCAST = "hindcast"           # simulação histórica sem assimilação
    OBSERVATION = "observation"     # dados observados (boias, satélite, HF radar)
    STATIC = "static"              # dados estáticos (batimetria, máscaras)
    CLIMATOLOGY = "climatology"     # médias climatológicas


class GridType(str, Enum):
    REGULAR_LATLON = "regular_latlon"
    CURVILINEAR = "curvilinear"
    UNSTRUCTURED = "unstructured"      # ICON, FESOM, MPAS
    ICOSAHEDRAL = "icosahedral"        # ICON específico
    POLAR_STEREOGRAPHIC = "polar_stereographic"  # IBCAO
    ROTATED_POLE = "rotated_pole"
    TRIPOLAR = "tripolar"              # ORCA grids (NEMO global)


class VerticalType(str, Enum):
    Z_LEVELS = "z_levels"           # profundidades fixas em metros
    Z_STAR = "z_star"               # z-star (NEMO, HYCOM)
    SIGMA = "sigma"                 # terrain-following (ROMS)
    HYBRID = "hybrid"               # hybrid sigma-z
    PRESSURE = "pressure"           # níveis de pressão (atmosférico)
    SURFACE_ONLY = "surface_only"   # sem dimensão vertical
    SEAFLOOR_ONLY = "seafloor_only" # batimetria
    ISOPYCNAL = "isopycnal"         # coordenadas isopicnais (HYCOM)
    GEOPOTENTIAL = "geopotential"   # níveis geopotenciais


class DataFormat(str, Enum):
    NETCDF3 = "netcdf3"
    NETCDF4 = "netcdf4"
    GRIB1 = "grib1"
    GRIB2 = "grib2"
    GEOTIFF = "geotiff"
    ZARR = "zarr"
    COG = "cog"                     # Cloud Optimized GeoTiff
    HDF5 = "hdf5"
    TUV = "tuv"                     # CODAR SeaSonde
    CSV = "csv"


class TransportProtocol(str, Enum):
    OPENDAP = "opendap"
    HTTP = "http"
    FTP = "ftp"
    S3 = "s3"
    AZURE_BLOB = "azure_blob"
    GCS = "gcs"                     # Google Cloud Storage
    CDS_API = "cds_api"             # Copernicus CDS
    CMEMS_API = "cmems_api"         # copernicusmarine toolbox
    ERDDAP = "erddap"
    THREDDS = "thredds"


class VariableCategory(str, Enum):
    """Categoria física da variável — agrupa conceitos relacionados."""
    OCEAN_PHYSICS = "ocean_physics"       # T, S, correntes, SSH, MLD
    WAVE = "wave"                         # Hs, Tp, direção, Stokes drift
    ATMOSPHERE = "atmosphere"             # vento, pressão, radiação
    BATHYMETRY = "bathymetry"             # profundidade do fundo
    ICE = "ice"                           # gelo marinho
    BIOGEOCHEMISTRY = "biogeochemistry"   # O2, pH, clorofila, nutrientes
    SEDIMENT = "sediment"                 # transporte de sedimentos
    OBSERVATION_QC = "observation_qc"     # flags de qualidade


class PhysicalQuantity(str, Enum):
    """
    Grandeza física base — o que está sendo medido, antes de qualquer
    qualificação termodinâmica. Agrupa variáveis que são "a mesma coisa"
    em formas termodinâmicas diferentes.
    """
    TEMPERATURE = "temperature"
    SALINITY = "salinity"
    DENSITY = "density"
    PRESSURE = "pressure"
    VELOCITY = "velocity"
    SEA_LEVEL = "sea_level"
    WAVE_HEIGHT = "wave_height"
    WAVE_PERIOD = "wave_period"
    WAVE_DIRECTION = "wave_direction"
    DEPTH = "depth"
    ICE_FRACTION = "ice_fraction"
    ICE_THICKNESS = "ice_thickness"
    WIND = "wind"
    MIXED_LAYER = "mixed_layer"
    VORTICITY = "vorticity"
    HEAT_FLUX = "heat_flux"
    RADIATION = "radiation"
    OTHER = "other"


class ThermodynamicForm(str, Enum):
    """
    Forma termodinâmica da variável.
    
    Distingue entre a medição direta (in_situ) e quantidades derivadas
    que corrigem para efeitos de pressão/composição.
    
    Impacto prático: misturar formas numa comparação ou assimilação
    introduz erros. θ e T divergem ~0.5°C a 5000m de profundidade.
    σ₀ e σ₂ podem inverter a estratificação em águas profundas.
    SP e SA diferem ~0.5% dependendo da composição iônica.
    """
    IN_SITU = "in_situ"                  # medição direta no local
    POTENTIAL = "potential"               # corrigido para pressão de referência
    CONSERVATIVE = "conservative"         # TEOS-10 conservative temperature (Θ)
    VIRTUAL = "virtual"                   # temperatura virtual (atmosfera, corrige umidade)
    EQUIVALENT_POTENTIAL = "equivalent_potential"  # θe (atmosfera, inclui calor latente)
    ABSOLUTE = "absolute"                 # salinidade absoluta SA (TEOS-10)
    PRACTICAL = "practical"               # salinidade prática SP (PSS-78)
    PREFORMED = "preformed"               # salinidade preformada S*
    NEUTRAL = "neutral"                   # densidade neutra γⁿ
    NOT_APPLICABLE = "not_applicable"     # para variáveis sem distinção (onda, vento, etc.)


class ThermodynamicFramework(str, Enum):
    """
    Framework termodinâmico usado para calcular propriedades da água do mar.
    
    EOS-80: equação de estado clássica. Usa temperatura potencial (θ)
            e salinidade prática (SP). Maioria dos modelos operacionais.
    TEOS-10: padrão IOC/IAPSO desde 2010. Usa temperatura conservativa (Θ)
             e salinidade absoluta (SA). Termodinamicamente consistente.
    
    A diferença importa: modelos NEMO podem rodar em EOS-80 ou TEOS-10
    dependendo da configuração. HYCOM usa EOS-80. MOM6 suporta ambos.
    """
    EOS80 = "eos80"
    TEOS10 = "teos10"
    UNKNOWN = "unknown"


@dataclass
class ReferenceState:
    """
    Condições de referência para variáveis potenciais/derivadas.
    
    Exemplos:
        θ  → reference_pressure_dbar=0 (temperatura potencial ref. superfície)
        σ₂ → reference_pressure_dbar=2000 (densidade potencial ref. 2000 dbar)
        σ₀ → reference_pressure_dbar=0
        θe → inclui pressão de referência + condensação
    
    Para variáveis in_situ ou não-termodinâmicas: None.
    """
    reference_pressure_dbar: float | None = None   # pressão de referência em dbar
    reference_depth_m: float | None = None          # profundidade de referência (≈ dbar)
    framework: ThermodynamicFramework = ThermodynamicFramework.UNKNOWN
    notes: str | None = None


# =============================================================================
# BUILDING BLOCKS — componentes reutilizáveis
# =============================================================================

@dataclass
class BoundingBox:
    lon_min: float
    lon_max: float
    lat_min: float
    lat_max: float

    def contains(self, other: "BoundingBox") -> bool:
        return (
            self.lon_min <= other.lon_min
            and self.lon_max >= other.lon_max
            and self.lat_min <= other.lat_min
            and self.lat_max >= other.lat_max
        )

    def intersects(self, other: "BoundingBox") -> bool:
        return not (
            self.lon_max < other.lon_min
            or self.lon_min > other.lon_max
            or self.lat_max < other.lat_min
            or self.lat_min > other.lat_max
        )


@dataclass
class Grid:
    """Especificação espacial do grid."""
    grid_type: GridType
    horizontal_resolution: str          # "0.083deg", "2.5km", "100m", "R2B6"
    horizontal_resolution_m: float | None = None  # resolução em metros (para comparação)
    crs: str = "EPSG:4326"              # sistema de coordenadas
    nx: int | None = None               # pontos em x
    ny: int | None = None               # pontos em y
    coverage: BoundingBox | None = None
    notes: str | None = None


@dataclass
class VerticalSpec:
    """Especificação da coordenada vertical."""
    vertical_type: VerticalType
    n_levels: int | None = None
    levels: list[float] | None = None   # valores dos níveis (metros, sigma, hPa)
    depth_min: float | None = None      # profundidade mínima em metros
    depth_max: float | None = None      # profundidade máxima em metros
    unit: str = "meters"                # meters, sigma, hPa


@dataclass
class TemporalSpec:
    """Especificação temporal do dataset."""
    product_type: ProductType
    temporal_resolution: str | None = None   # "PT1H", "P1D", "P1M", "PT15M", "static"
    update_frequency: str | None = None      # "daily", "twice_daily", "weekly", "static"
    forecast_length_hours: int | None = None
    archive_years: int | None = None         # anos de arquivo disponíveis
    start_date: str | None = None            # "1979-01-01" (para reanálises)
    end_date: str | None = None              # "present" ou data fixa
    reference_time: str | None = None        # "00Z", "12Z" (para ciclos de forecast)


@dataclass
class AccessMethod:
    """Como acessar os dados."""
    protocol: TransportProtocol
    endpoint: str | None = None          # URL base, OPeNDAP endpoint, etc.
    format: DataFormat = DataFormat.NETCDF4
    auth_required: bool = False
    auth_method: str | None = None       # "api_key", "sas_token", "aad", "cds_key"
    notes: str | None = None
    # Para mapeamento direto com o downloader existente:
    downloader_class: str | None = None  # "CopernicusDownloader", "HycomDownloader", etc.


# =============================================================================
# VARIABLE — a peça central da unificação
# =============================================================================

@dataclass
class Variable:
    """
    Uma variável física oferecida por um dataset.
    
    O cf_standard_name é a chave de unificação entre fontes diferentes.
    O native_name é como a variável aparece no arquivo original.
    
    Campos termodinâmicos permitem distinguir entre formas da mesma
    grandeza (in_situ vs potencial vs conservativa), evitando erros
    silenciosos em comparações e assimilação.
    """
    # Identidade
    native_name: str                     # nome no arquivo: "thetao", "VHM0", "temperature"
    cf_standard_name: str | None = None  # CF convention: "sea_water_potential_temperature"
    long_name: str | None = None         # "Sea water potential temperature"
    
    # Física
    unit: str | None = None              # "K", "m", "m/s", "g/kg", "degree"
    category: VariableCategory | None = None
    
    # Termodinâmica — distingue formas da mesma grandeza
    physical_quantity: PhysicalQuantity | None = None   # a grandeza base (TEMPERATURE, SALINITY, ...)
    thermodynamic_form: ThermodynamicForm = ThermodynamicForm.NOT_APPLICABLE
    reference_state: ReferenceState | None = None       # condições de referência (pressão, framework)
    
    # Dimensionalidade
    is_3d: bool = False                  # True se varia com profundidade
    is_vector_component: bool = False    # True para u, v (componentes de vetor)
    vector_pair: str | None = None       # nome da outra componente ("vo" se esta é "uo")
    
    # Faixa de valores esperados (para QC automático)
    valid_min: float | None = None
    valid_max: float | None = None
    
    # Metadados extras
    fill_value: float | str | None = None
    notes: str | None = None

    def is_compatible_with(self, other: "Variable") -> "VariableCompatibility":
        """
        Verifica compatibilidade termodinâmica com outra variável.
        
        Retorna um VariableCompatibility indicando se são diretamente
        comparáveis, se precisam de conversão, ou se são incompatíveis.
        """
        # Grandezas diferentes → incompatível
        if (
            self.physical_quantity
            and other.physical_quantity
            and self.physical_quantity != other.physical_quantity
        ):
            return VariableCompatibility(
                compatible=False,
                needs_conversion=False,
                reason=f"Different quantities: {self.physical_quantity.value} vs {other.physical_quantity.value}",
            )

        # Mesma forma termodinâmica → compatível direto
        if self.thermodynamic_form == other.thermodynamic_form:
            # Mas verificar referência (σ₀ vs σ₂ são ambos "potential" mas refs diferentes)
            if (
                self.reference_state
                and other.reference_state
                and self.reference_state.reference_pressure_dbar != other.reference_state.reference_pressure_dbar
            ):
                return VariableCompatibility(
                    compatible=False,
                    needs_conversion=True,
                    reason=(
                        f"Same form ({self.thermodynamic_form.value}) but different reference: "
                        f"{self.reference_state.reference_pressure_dbar} vs "
                        f"{other.reference_state.reference_pressure_dbar} dbar"
                    ),
                    conversion_notes="Requires recalculation at common reference pressure",
                )
            return VariableCompatibility(compatible=True, needs_conversion=False)

        # Formas diferentes da mesma grandeza → precisa conversão
        if self.thermodynamic_form != ThermodynamicForm.NOT_APPLICABLE:
            return VariableCompatibility(
                compatible=False,
                needs_conversion=True,
                reason=(
                    f"{self.thermodynamic_form.value} vs {other.thermodynamic_form.value}"
                ),
                conversion_notes=_suggest_conversion(self, other),
            )

        return VariableCompatibility(compatible=True, needs_conversion=False)


@dataclass
class VariableCompatibility:
    """Resultado da verificação de compatibilidade entre duas variáveis."""
    compatible: bool                     # True se podem ser comparadas diretamente
    needs_conversion: bool = False       # True se precisam de conversão
    reason: str | None = None
    conversion_notes: str | None = None  # sugestão de como converter
    conversion_function: str | None = None  # ex: "gsw.pt_from_t" (GSW toolbox)


def _suggest_conversion(a: Variable, b: Variable) -> str | None:
    """Sugere método de conversão entre formas termodinâmicas."""
    forms = {a.thermodynamic_form, b.thermodynamic_form}
    qty = a.physical_quantity or b.physical_quantity

    if qty == PhysicalQuantity.TEMPERATURE:
        if forms == {ThermodynamicForm.IN_SITU, ThermodynamicForm.POTENTIAL}:
            return "gsw.pt_from_t(SA, t, p, p_ref) or gsw.t_from_CT(SA, CT, p). Requires pressure profile."
        if forms == {ThermodynamicForm.POTENTIAL, ThermodynamicForm.CONSERVATIVE}:
            return "gsw.CT_from_pt(SA, pt) — TEOS-10. Requires absolute salinity."
        if forms == {ThermodynamicForm.IN_SITU, ThermodynamicForm.CONSERVATIVE}:
            return "gsw.CT_from_t(SA, t, p) — TEOS-10. Requires pressure and absolute salinity."

    if qty == PhysicalQuantity.SALINITY:
        if forms == {ThermodynamicForm.PRACTICAL, ThermodynamicForm.ABSOLUTE}:
            return "gsw.SA_from_SP(SP, p, lon, lat) — TEOS-10. Requires position and pressure."

    if qty == PhysicalQuantity.DENSITY:
        if ThermodynamicForm.POTENTIAL in forms:
            return "Recalculate at common reference pressure using gsw.rho(SA, CT, p_ref)."

    return None


# =============================================================================
# HIERARCHY — Provider → ProductLine → Dataset
# =============================================================================

@dataclass
class Dataset:
    """
    Um dataset específico dentro de um produto.
    
    Exemplo CMEMS: cmems_mod_blk_phy-temp_anfc_2.5km_P1D-m
    Exemplo HYCOM: GLBy0.08/expt_93.0
    Exemplo GEBCO: GEBCO_2025.nc
    """
    dataset_id: str                      # identificador único do dataset
    name: str | None = None              # nome legível
    description: str | None = None
    
    # Conteúdo
    variables: list[Variable] = field(default_factory=list)
    
    # Specs
    grid: Grid | None = None
    vertical: VerticalSpec | None = None
    temporal: TemporalSpec | None = None
    
    # Acesso
    access: list[AccessMethod] = field(default_factory=list)
    
    # Tamanho típico
    typical_file_size_mb: float | None = None
    
    def cf_names(self) -> set[str]:
        """Retorna todos os CF standard_names deste dataset."""
        return {v.cf_standard_name for v in self.variables if v.cf_standard_name}

    def native_names(self) -> set[str]:
        return {v.native_name for v in self.variables}

    def variables_by_category(self, cat: VariableCategory) -> list[Variable]:
        return [v for v in self.variables if v.category == cat]


@dataclass
class ProductLine:
    """
    Uma linha de produto oferecida por um provider.
    
    Exemplo CMEMS: BLKSEA_ANALYSISFORECAST_PHY_007_001
    Exemplo NOAA: GFS Wave
    Exemplo GEBCO: GEBCO_2025
    """
    product_id: str                      # identificador do produto
    name: str | None = None
    description: str | None = None
    
    # Modelo numérico subjacente
    model_name: str | None = None        # "NEMO v4.2.2", "WAM 4.7", "WW3 v6.07.1"
    model_version: str | None = None
    
    # Classificação
    product_types: list[ProductType] = field(default_factory=list)
    categories: list[VariableCategory] = field(default_factory=list)
    
    # Região
    region: str | None = None            # "Baltic Sea", "Global", "Black Sea"
    coverage: BoundingBox | None = None
    
    # Datasets que compõem este produto
    datasets: list[Dataset] = field(default_factory=list)
    
    # Documentação
    pum_url: str | None = None           # URL do Product User Manual
    quid_url: str | None = None          # URL do Quality Information Document
    
    # Versão e datas
    version: str | None = None
    last_updated: str | None = None
    
    def all_variables(self) -> list[Variable]:
        """Todas as variáveis únicas de todos os datasets."""
        seen = set()
        result = []
        for ds in self.datasets:
            for v in ds.variables:
                key = (v.native_name, v.cf_standard_name)
                if key not in seen:
                    seen.add(key)
                    result.append(v)
        return result

    def all_cf_names(self) -> set[str]:
        names = set()
        for ds in self.datasets:
            names |= ds.cf_names()
        return names


@dataclass
class Provider:
    """
    Uma organização que fornece dados.
    
    Exemplo: Copernicus Marine Service, NOAA/NCEP, ECMWF, GEBCO
    """
    provider_id: str                     # "cmems", "noaa", "ecmwf", "gebco"
    name: str
    url: str | None = None
    description: str | None = None
    
    product_lines: list[ProductLine] = field(default_factory=list)


# =============================================================================
# VARIABLE REGISTRY — o dicionário universal de variáveis
# =============================================================================

@dataclass
class CanonicalVariable:
    """
    Uma variável canônica no registro global.
    
    Mapeia um conceito físico para todos os nomes que ele assume
    em diferentes fontes. É a Rosetta Stone do sistema.
    
    Inclui informação termodinâmica para distinguir formas da mesma
    grandeza e detectar incompatibilidades.
    """
    cf_standard_name: str                # chave primária
    long_name: str
    canonical_unit: str
    category: VariableCategory
    is_3d: bool = False
    is_vector_component: bool = False
    
    # Termodinâmica
    physical_quantity: PhysicalQuantity = PhysicalQuantity.OTHER
    thermodynamic_form: ThermodynamicForm = ThermodynamicForm.NOT_APPLICABLE
    reference_pressure_dbar: float | None = None  # para variáveis potenciais
    framework: ThermodynamicFramework = ThermodynamicFramework.UNKNOWN
    
    # Relações com outras formas da mesma grandeza
    related_cf_names: list[str] = field(default_factory=list)
    # ex: sea_water_potential_temperature.related = [sea_water_temperature, sea_water_conservative_temperature]
    
    # Todos os aliases conhecidos (nome → provider)
    aliases: dict[str, list[str]] = field(default_factory=dict)


# Registro pré-populado com as variáveis mais comuns
VARIABLE_REGISTRY: dict[str, CanonicalVariable] = {

    # ══════════════════════════════════════════════════════════════════
    # TEMPERATURA — 3 formas termodinâmicas distintas
    # ══════════════════════════════════════════════════════════════════

    "sea_water_temperature": CanonicalVariable(
        cf_standard_name="sea_water_temperature",
        long_name="Sea water in-situ temperature",
        canonical_unit="°C",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.TEMPERATURE,
        thermodynamic_form=ThermodynamicForm.IN_SITU,
        related_cf_names=[
            "sea_water_potential_temperature",
            "sea_water_conservative_temperature",
        ],
        aliases={
            "temperature": ["hycom_insitu"],  # HYCOM pode exportar in-situ dependendo da config
        },
    ),
    "sea_water_potential_temperature": CanonicalVariable(
        cf_standard_name="sea_water_potential_temperature",
        long_name="Sea water potential temperature",
        canonical_unit="°C",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.TEMPERATURE,
        thermodynamic_form=ThermodynamicForm.POTENTIAL,
        reference_pressure_dbar=0,
        framework=ThermodynamicFramework.EOS80,
        related_cf_names=[
            "sea_water_temperature",
            "sea_water_conservative_temperature",
        ],
        aliases={
            "thetao": ["cmems"],
            "temperature": ["hycom"],         # HYCOM GLBv0.08 exporta θ por padrão
            "temp": ["roms", "cronos"],
            "TEMP": ["blksea_file"],
            "to": ["icon_o"],                 # ICON-O output
        },
    ),
    "sea_water_conservative_temperature": CanonicalVariable(
        cf_standard_name="sea_water_conservative_temperature",
        long_name="Sea water conservative temperature (TEOS-10)",
        canonical_unit="°C",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.TEMPERATURE,
        thermodynamic_form=ThermodynamicForm.CONSERVATIVE,
        framework=ThermodynamicFramework.TEOS10,
        related_cf_names=[
            "sea_water_temperature",
            "sea_water_potential_temperature",
        ],
        aliases={
            "bigthetao": ["cmems_teos10"],    # CMEMS se/quando migrar para TEOS-10
            "CT": ["gsw"],                     # nomenclatura GSW toolbox
        },
    ),
    "sea_water_potential_temperature_at_sea_floor": CanonicalVariable(
        cf_standard_name="sea_water_potential_temperature_at_sea_floor",
        long_name="Sea floor potential temperature",
        canonical_unit="°C",
        category=VariableCategory.OCEAN_PHYSICS,
        physical_quantity=PhysicalQuantity.TEMPERATURE,
        thermodynamic_form=ThermodynamicForm.POTENTIAL,
        reference_pressure_dbar=0,
        aliases={
            "bottomT": ["cmems"],
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # SALINIDADE — 2 formas: prática (PSS-78) vs absoluta (TEOS-10)
    # ══════════════════════════════════════════════════════════════════

    "sea_water_practical_salinity": CanonicalVariable(
        cf_standard_name="sea_water_practical_salinity",
        long_name="Sea water practical salinity (PSS-78)",
        canonical_unit="1",               # adimensional no PSS-78 (historicamente psu)
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.SALINITY,
        thermodynamic_form=ThermodynamicForm.PRACTICAL,
        framework=ThermodynamicFramework.EOS80,
        related_cf_names=["sea_water_absolute_salinity"],
        aliases={
            "so": ["cmems"],               # CMEMS usa practical salinity
            "salinity": ["hycom"],
            "salt": ["roms", "cronos"],
            "PSAL": ["blksea_file"],
        },
    ),
    "sea_water_absolute_salinity": CanonicalVariable(
        cf_standard_name="sea_water_absolute_salinity",
        long_name="Sea water absolute salinity (TEOS-10)",
        canonical_unit="g/kg",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.SALINITY,
        thermodynamic_form=ThermodynamicForm.ABSOLUTE,
        framework=ThermodynamicFramework.TEOS10,
        related_cf_names=["sea_water_practical_salinity"],
        aliases={
            "SA": ["gsw"],
            "so_abs": ["cmems_teos10"],
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # DENSIDADE — in-situ, potencial σ₀, σ₂, neutra
    # ══════════════════════════════════════════════════════════════════

    "sea_water_density": CanonicalVariable(
        cf_standard_name="sea_water_density",
        long_name="Sea water in-situ density",
        canonical_unit="kg/m³",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.DENSITY,
        thermodynamic_form=ThermodynamicForm.IN_SITU,
        related_cf_names=[
            "sea_water_potential_density",
            "sea_water_sigma_theta",
        ],
        aliases={
            "rho": ["icon_o", "nemo"],
        },
    ),
    "sea_water_sigma_theta": CanonicalVariable(
        cf_standard_name="sea_water_sigma_theta",
        long_name="Potential density anomaly σ₀ (ref 0 dbar)",
        canonical_unit="kg/m³",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.DENSITY,
        thermodynamic_form=ThermodynamicForm.POTENTIAL,
        reference_pressure_dbar=0,
        related_cf_names=["sea_water_density", "sea_water_sigma_t"],
        aliases={
            "rhopot": ["icon_o", "nemo"],
            "sigma0": ["hycom", "roms"],
        },
    ),
    "sea_water_potential_density_2000dbar": CanonicalVariable(
        cf_standard_name="sea_water_potential_density_referenced_to_2000dbar",
        long_name="Potential density σ₂ (ref 2000 dbar)",
        canonical_unit="kg/m³",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.DENSITY,
        thermodynamic_form=ThermodynamicForm.POTENTIAL,
        reference_pressure_dbar=2000,
        related_cf_names=["sea_water_sigma_theta"],
        aliases={
            "sigma2": ["hycom_isopycnal"],    # HYCOM em modo isopicnal usa σ₂
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # PRESSÃO
    # ══════════════════════════════════════════════════════════════════

    "sea_water_pressure": CanonicalVariable(
        cf_standard_name="sea_water_pressure",
        long_name="Sea water pressure",
        canonical_unit="dbar",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        physical_quantity=PhysicalQuantity.PRESSURE,
        thermodynamic_form=ThermodynamicForm.IN_SITU,
        aliases={
            "pressure": ["ctd"],
        },
    ),
    "air_pressure_at_mean_sea_level": CanonicalVariable(
        cf_standard_name="air_pressure_at_mean_sea_level",
        long_name="Mean sea level pressure",
        canonical_unit="Pa",
        category=VariableCategory.ATMOSPHERE,
        physical_quantity=PhysicalQuantity.PRESSURE,
        thermodynamic_form=ThermodynamicForm.NOT_APPLICABLE,
        aliases={
            "msl": ["era5", "ecmwf"],
            "PRMSL": ["gfs_grib"],
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # CORRENTES — sem ambiguidade termodinâmica, mas vector pairing
    # ══════════════════════════════════════════════════════════════════

    "eastward_sea_water_velocity": CanonicalVariable(
        cf_standard_name="eastward_sea_water_velocity",
        long_name="Eastward sea water velocity",
        canonical_unit="m/s",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        is_vector_component=True,
        physical_quantity=PhysicalQuantity.VELOCITY,
        aliases={
            "uo": ["cmems"],
            "water_u": ["hycom"],
            "u": ["roms", "cronos", "icon_o"],
        },
    ),
    "northward_sea_water_velocity": CanonicalVariable(
        cf_standard_name="northward_sea_water_velocity",
        long_name="Northward sea water velocity",
        canonical_unit="m/s",
        category=VariableCategory.OCEAN_PHYSICS,
        is_3d=True,
        is_vector_component=True,
        physical_quantity=PhysicalQuantity.VELOCITY,
        aliases={
            "vo": ["cmems"],
            "water_v": ["hycom"],
            "v": ["roms", "cronos", "icon_o"],
        },
    ),
    "sea_surface_height_above_geoid": CanonicalVariable(
        cf_standard_name="sea_surface_height_above_geoid",
        long_name="Sea surface height above geoid",
        canonical_unit="m",
        category=VariableCategory.OCEAN_PHYSICS,
        physical_quantity=PhysicalQuantity.SEA_LEVEL,
        aliases={
            "zos": ["cmems"],
            "ssh": ["hycom"],
            "zeta": ["roms", "cronos"],
            "ASLV": ["blksea_file"],
        },
    ),
    "ocean_mixed_layer_thickness_defined_by_sigma_theta": CanonicalVariable(
        cf_standard_name="ocean_mixed_layer_thickness_defined_by_sigma_theta",
        long_name="Ocean mixed layer thickness",
        canonical_unit="m",
        category=VariableCategory.OCEAN_PHYSICS,
        physical_quantity=PhysicalQuantity.MIXED_LAYER,
        aliases={
            "mlotst": ["cmems"],
            "AMXL": ["blksea_file"],
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # ONDAS
    # ══════════════════════════════════════════════════════════════════

    "sea_surface_wave_significant_height": CanonicalVariable(
        cf_standard_name="sea_surface_wave_significant_height",
        long_name="Significant wave height",
        canonical_unit="m",
        category=VariableCategory.WAVE,
        physical_quantity=PhysicalQuantity.WAVE_HEIGHT,
        aliases={
            "VHM0": ["cmems_wav", "baltic_wav"],
            "hs": ["icon_waves", "ww3"],
            "swh": ["era5", "ecmwf"],
            "HTSGW": ["gfs_wave"],
        },
    ),
    "sea_surface_wave_period_at_variance_spectral_density_maximum": CanonicalVariable(
        cf_standard_name="sea_surface_wave_period_at_variance_spectral_density_maximum",
        long_name="Peak wave period",
        canonical_unit="s",
        category=VariableCategory.WAVE,
        physical_quantity=PhysicalQuantity.WAVE_PERIOD,
        aliases={
            "VTPK": ["cmems_wav", "baltic_wav"],
            "tpp": ["icon_waves"],
            "tp": ["era5"],
            "PERPW": ["gfs_wave"],
        },
    ),
    "sea_surface_wave_from_direction": CanonicalVariable(
        cf_standard_name="sea_surface_wave_from_direction",
        long_name="Mean wave direction",
        canonical_unit="degree",
        category=VariableCategory.WAVE,
        physical_quantity=PhysicalQuantity.WAVE_DIRECTION,
        aliases={
            "VMDR": ["cmems_wav", "baltic_wav"],
            "hs_dir": ["icon_waves"],
            "mwd": ["era5"],
        },
    ),
    "sea_surface_wave_stokes_drift_x_velocity": CanonicalVariable(
        cf_standard_name="sea_surface_wave_stokes_drift_x_velocity",
        long_name="Stokes drift U",
        canonical_unit="m/s",
        category=VariableCategory.WAVE,
        is_vector_component=True,
        physical_quantity=PhysicalQuantity.VELOCITY,
        aliases={
            "VSDX": ["cmems_wav", "baltic_wav"],
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # ATMOSFERA
    # ══════════════════════════════════════════════════════════════════

    "eastward_wind": CanonicalVariable(
        cf_standard_name="eastward_wind",
        long_name="10m U wind component",
        canonical_unit="m/s",
        category=VariableCategory.ATMOSPHERE,
        is_vector_component=True,
        physical_quantity=PhysicalQuantity.WIND,
        aliases={
            "u10": ["era5", "ecmwf"],
            "wind_u": ["gfs"],
            "UGRD": ["gfs_grib"],
        },
    ),
    "northward_wind": CanonicalVariable(
        cf_standard_name="northward_wind",
        long_name="10m V wind component",
        canonical_unit="m/s",
        category=VariableCategory.ATMOSPHERE,
        is_vector_component=True,
        physical_quantity=PhysicalQuantity.WIND,
        aliases={
            "v10": ["era5", "ecmwf"],
            "wind_v": ["gfs"],
            "VGRD": ["gfs_grib"],
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # BATIMETRIA
    # ══════════════════════════════════════════════════════════════════

    "sea_floor_depth_below_geoid": CanonicalVariable(
        cf_standard_name="sea_floor_depth_below_geoid",
        long_name="Sea floor depth below geoid",
        canonical_unit="m",
        category=VariableCategory.BATHYMETRY,
        physical_quantity=PhysicalQuantity.DEPTH,
        aliases={
            "deptho": ["cmems"],
            "elevation": ["gebco", "sdb"],
            "depth": ["sdb_composite"],
        },
    ),

    # ══════════════════════════════════════════════════════════════════
    # GELO
    # ══════════════════════════════════════════════════════════════════

    "sea_ice_area_fraction": CanonicalVariable(
        cf_standard_name="sea_ice_area_fraction",
        long_name="Sea ice area fraction",
        canonical_unit="1",
        category=VariableCategory.ICE,
        physical_quantity=PhysicalQuantity.ICE_FRACTION,
        aliases={"siconc": ["cmems"], "aice": ["hycom"]},
    ),
    "sea_ice_thickness": CanonicalVariable(
        cf_standard_name="sea_ice_thickness",
        long_name="Sea ice thickness",
        canonical_unit="m",
        category=VariableCategory.ICE,
        physical_quantity=PhysicalQuantity.ICE_THICKNESS,
        aliases={"sithick": ["cmems"], "hi": ["hycom"]},
    ),

    # ══════════════════════════════════════════════════════════════════
    # OBSERVAÇÃO (CODAR)
    # ══════════════════════════════════════════════════════════════════

    "surface_eastward_sea_water_velocity": CanonicalVariable(
        cf_standard_name="surface_eastward_sea_water_velocity",
        long_name="Surface eastward current (HF radar)",
        canonical_unit="m/s",
        category=VariableCategory.OCEAN_PHYSICS,
        is_vector_component=True,
        physical_quantity=PhysicalQuantity.VELOCITY,
        aliases={"u_surface": ["codar"], "EWCT": ["codar_tuv"]},
    ),
    "surface_northward_sea_water_velocity": CanonicalVariable(
        cf_standard_name="surface_northward_sea_water_velocity",
        long_name="Surface northward current (HF radar)",
        canonical_unit="m/s",
        category=VariableCategory.OCEAN_PHYSICS,
        is_vector_component=True,
        physical_quantity=PhysicalQuantity.VELOCITY,
        aliases={"v_surface": ["codar"], "NSCT": ["codar_tuv"]},
    ),
}


# =============================================================================
# CATALOG — o agregador
# =============================================================================

@dataclass
class Catalog:
    """
    Catálogo completo de fontes de dados.
    
    Agrega providers e oferece buscas cruzadas.
    """
    providers: list[Provider] = field(default_factory=list)
    variable_registry: dict[str, CanonicalVariable] = field(
        default_factory=lambda: dict(VARIABLE_REGISTRY)
    )

    def all_datasets(self) -> list[tuple[str, str, Dataset]]:
        """Retorna (provider_id, product_id, dataset) para todos os datasets."""
        result = []
        for prov in self.providers:
            for pl in prov.product_lines:
                for ds in pl.datasets:
                    result.append((prov.provider_id, pl.product_id, ds))
        return result

    def find_datasets(
        self,
        *,
        cf_standard_name: str | None = None,
        native_name: str | None = None,
        category: VariableCategory | None = None,
        product_type: ProductType | None = None,
        covers_bbox: BoundingBox | None = None,
        provider_id: str | None = None,
    ) -> list[tuple[str, str, Dataset]]:
        """Busca datasets que atendem aos critérios."""
        results = []
        for prov_id, prod_id, ds in self.all_datasets():
            if provider_id and prov_id != provider_id:
                continue
            if product_type and ds.temporal and ds.temporal.product_type != product_type:
                continue
            if covers_bbox and ds.grid and ds.grid.coverage:
                if not ds.grid.coverage.intersects(covers_bbox):
                    continue
            if cf_standard_name and cf_standard_name not in ds.cf_names():
                continue
            if native_name and native_name not in ds.native_names():
                continue
            if category:
                if not any(v.category == category for v in ds.variables):
                    continue
            results.append((prov_id, prod_id, ds))
        return results

    def find_equivalences(self, cf_standard_name: str) -> dict[str, list[str]]:
        """
        Dado um CF standard_name, retorna {native_name: [providers]} 
        mostrando todos os aliases conhecidos.
        """
        canon = self.variable_registry.get(cf_standard_name)
        if not canon:
            return {}
        return dict(canon.aliases)

    def resolve_native_to_cf(self, native_name: str) -> str | None:
        """Dado um nome nativo (ex: 'thetao'), retorna o CF standard_name."""
        for cf_name, canon in self.variable_registry.items():
            if native_name in canon.aliases:
                return cf_name
        return None

    def compare_products(
        self, product_id_a: str, product_id_b: str
    ) -> dict[str, Any]:
        """
        Compara dois produtos: variáveis em comum, exclusivas, 
        diferenças de resolução, etc.
        """
        pl_a = pl_b = None
        for prov in self.providers:
            for pl in prov.product_lines:
                if pl.product_id == product_id_a:
                    pl_a = pl
                if pl.product_id == product_id_b:
                    pl_b = pl

        if not pl_a or not pl_b:
            return {"error": "Product not found"}

        cf_a = pl_a.all_cf_names()
        cf_b = pl_b.all_cf_names()

        return {
            "product_a": product_id_a,
            "product_b": product_id_b,
            "common_cf_names": sorted(cf_a & cf_b),
            "only_in_a": sorted(cf_a - cf_b),
            "only_in_b": sorted(cf_b - cf_a),
            "a_variables_total": len(pl_a.all_variables()),
            "b_variables_total": len(pl_b.all_variables()),
        }

    def summary(self) -> dict[str, Any]:
        """Resumo estatístico do catálogo."""
        all_ds = self.all_datasets()
        all_cf = set()
        cats = {}
        types = {}
        for _, _, ds in all_ds:
            all_cf |= ds.cf_names()
            for v in ds.variables:
                if v.category:
                    cats[v.category.value] = cats.get(v.category.value, 0) + 1
                if ds.temporal:
                    t = ds.temporal.product_type.value
                    types[t] = types.get(t, 0) + 1

        return {
            "providers": len(self.providers),
            "product_lines": sum(len(p.product_lines) for p in self.providers),
            "datasets": len(all_ds),
            "unique_cf_variables": len(all_cf),
            "registry_size": len(self.variable_registry),
            "by_category": cats,
            "by_product_type": types,
        }


# =============================================================================
# SERIALIZAÇÃO YAML — ida e volta
# =============================================================================

def catalog_to_yaml_dict(catalog: Catalog) -> dict:
    """Serializa catálogo para dict compatível com YAML."""
    import dataclasses

    def _to_dict(obj):
        if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
            return {k: _to_dict(v) for k, v in dataclasses.asdict(obj).items() if v is not None}
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, list):
            return [_to_dict(i) for i in obj]
        if isinstance(obj, dict):
            return {k: _to_dict(v) for k, v in obj.items()}
        if isinstance(obj, set):
            return sorted(obj)
        return obj

    return _to_dict(catalog)


def save_catalog_yaml(catalog: Catalog, path: str) -> None:
    """Salva catálogo em arquivo YAML."""
    import yaml
    data = catalog_to_yaml_dict(catalog)
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "AccessMethod",
    "BoundingBox",
    "CanonicalVariable",
    "Catalog",
    "DataFormat",
    "Dataset",
    "Grid",
    "GridType",
    "PhysicalQuantity",
    "ProductLine",
    "ProductType",
    "Provider",
    "ReferenceState",
    "TemporalSpec",
    "ThermodynamicForm",
    "ThermodynamicFramework",
    "TransportProtocol",
    "Variable",
    "VariableCategory",
    "VariableCompatibility",
    "VerticalSpec",
    "VerticalType",
    "VARIABLE_REGISTRY",
    "catalog_to_yaml_dict",
    "save_catalog_yaml",
]