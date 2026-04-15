# Referência cruzada de variáveis oceanográficas em cinco fontes de dados globais

**As cinco fontes de dados oceânicos globais mais utilizadas — CMEMS, GFS, HYCOM, ERA5 e GEBCO — diferem significativamente em nomenclatura de variáveis, unidades, convenções de coordenadas e estrutura de grade.** A construção de uma camada de harmonização exige o mapeamento cuidadoso de pelo menos 14 regras críticas de conversão: Kelvin para Celsius nas temperaturas do ERA5/GFS, Pascal para hectopascal na pressão, rotação de longitude 0–360 para ±180° no GFS/HYCOM/ERA5, e inversão de sinal de profundidade no GEBCO. Este documento referencia cada nome de variável, unidade, convenção de coordenadas e armadilha conhecida nas nove categorias de variáveis oceanográficas, fornecendo a especificação completa necessária para um pipeline de integração multi-fonte.

---

## Tabela mestra de referência cruzada de variáveis

A tabela abaixo mapeia cada variável física em todas as cinco fontes. Células vazias indicam que a variável não está disponível naquela fonte.

| Categoria | CMEMS | GFS | HYCOM | ERA5 | GEBCO |
|---|---|---|---|---|---|
| **Temperatura (3D)** | `thetao` <br> °C <br> temp. potencial <br> 50 níveis | — | `water_temp` <br> °C <br> temp. in-situ <br> 40 níveis | — | — |
| **TSM (superfície)** | `thetao` <br> em depth=0.49m <br> °C | `TMP` na superfície <br> K (temp. de pele) | `sst` (arquivo ice) ou `water_temp` em depth=0 <br> °C | `sst` <br> K (condição de contorno prescrita) | — |
| **Corrente zonal (3D)** | `uo` <br> m/s <br> 50 níveis | — | `water_u` <br> m/s <br> 40 níveis | — | — |
| **Corrente meridional (3D)** | `vo` <br> m/s <br> 50 níveis | — | `water_v` <br> m/s <br> 40 níveis | — | — |
| **Salinidade (3D)** | `so` <br> 1e-3 (PSU) <br> 50 níveis | — | `salinity` <br> PSU <br> 40 níveis | — | — |
| **Elevação da superfície do mar** | `zos` <br> m (sem marés/IB) | — | `surf_el` <br> m (anomalia SSH do modelo) | — | — |
| **Batimetria** | `deptho` (arquivo estático) <br> m | — | — | — | `elevation` <br> m (negativo=oceano) |
| **Concentração de gelo marinho** | `siconc` <br> fração (0–1) | `ICEC` <br> fração (0–1) | `sic` <br> fração (0–1) | `siconc` <br> fração (0–1) | — |
| **Espessura de gelo marinho** | `sithick` <br> m | `ICETK` <br> m | `sih` <br> m | — | — |
| **Profundidade da camada de mistura** | `mlotst` <br> m | — | `mixed_layer_thickness` <br> m (apenas GOFS 3.1) | — | — |
| **Vento U a 10m** | — | `UGRD` a 10m <br> m/s | — | `u10` <br> m/s | — |
| **Vento V a 10m** | — | `VGRD` a 10m <br> m/s | — | `v10` <br> m/s | — |
| **Pressão ao nível do mar** | — | `PRMSL` <br> Pa | — | `msl` <br> Pa | — |
| **Altura significativa de onda** | — | — | — | `swh` <br> m (grade 0.5°) | — |

---

## Geometria de grade e convenções de coordenadas

Entender as diferenças de coordenadas é a fonte mais comum de bugs em integrações. A tabela abaixo captura cada convenção que precisa ser reconciliada.

| Propriedade | CMEMS | GFS | HYCOM | ERA5 | GEBCO |
|---|---|---|---|---|---|
| **Resolução espacial** | 1/12° (~0.083°) | 0.25° / 0.50° / 1.0° | 0.08° lon × 0.04° lat | 0.25° (atmo) / 0.5° (ondas) | 15 arc-sec (~0.004°) |
| **Dimensões da grade** | 4320 × 2041 | 1440 × 721 (0.25°) | 4500 × 4251 | 1440 × 721 (0.25°) | 86400 × 43200 |
| **Faixa de longitude** | **−180 a +180** | **0 a 360** | **0 a 360** | **0 a 360** (padrão) | **−180 a +180** |
| **Faixa de latitude** | −80 a 90 | −90 a 90 | −80 a 90 | −90 a 90 | −90 a 90 |
| **Convenção de profundidade** | positiva para baixo (0.49–5728 m) | N/A (atmosférico) | positiva para baixo (0–5000 m) | N/A (atmosférico) | elevação: positiva para cima |
| **Níveis de profundidade** | 50 níveis Z | — | 40 níveis Z | — | — |
| **Tipo de grade** | Lat/lon regular (de ORCA12) | Lat/lon regular | Lat/lon regular (de curvilínea) | Lat/lon regular (de Gaussiana reduzida) | Lat/lon regular, pixel-center |
| **Registro da grade** | Centro da célula | Ponto de grade | Centro da célula | Ponto de grade | Centro do pixel |
| **Ordem de varredura** | S→N, W→E | N→S, W→E | S→N, W→E | N→S, W→E | S→N, W→E |

**A longitude é a conversão de maior prioridade.** CMEMS e GEBCO usam −180/+180; GFS, HYCOM e ERA5 usam 0/360 por padrão. Qualquer camada de harmonização deve implementar `lon = ((lon + 180) % 360) - 180` ou seu inverso. Falhar nisso faz os dados aparecerem deslocados por metade do globo ou produz subconjuntos preenchidos com NaN ao solicitar longitudes negativas de fontes 0–360.

---

## Resolução temporal e épocas de referência de tempo

Cada fonte usa uma época diferente para sua coordenada temporal, criando bugs silenciosos ao mesclar datasets sem conversão explícita.

| Propriedade | CMEMS | GFS | HYCOM | ERA5 | GEBCO |
|---|---|---|---|---|---|
| **Resolução temporal** | Horária (superfície) / 6h / Diária / Mensal | 1h (F001–F120), 3h (F120–F384) | 3-horária (3D), 1-horária (SSH/ice no ESPC-D-V02) | Horária | Estático |
| **Unidades de tempo** | horas desde **1950-01-01** | reference_time + forecast_step | horas desde **2000-01-01** | horas desde **1900-01-01** (legado) ou **1970-01-01** (novo CDS) | N/A |
| **Calendário** | Gregoriano | Gregoriano | Gregoriano | Gregoriano proléptico | N/A |
| **Tipo de tempo** | Blend análise/previsão | Previsão (ciclos 00/06/12/18Z) | Análise + previsão | Reanálise (análises + previsões curtas) | N/A |
| **Cadência de atualização** | Diária ~12 UTC | A cada 6 horas | Diária (análise); previsões de 8 dias | ~5 dias atrás do tempo real | Lançamento anual |

O GFS apresenta um desafio temporal único: variáveis de fluxo (calor latente, radiação, precipitação) são acumuladas desde o tempo de inicialização, não instantâneas. Extrair fluxos de intervalos específicos requer diferenciar passos consecutivos de previsão: `fluxo(t1→t2) = [fluxo(0→t2) × t2 − fluxo(0→t1) × t1] / (t2 − t1)`. O ERA5 tem um problema similar com suas variáveis de tipo previsão (precipitação, evaporação, radiação), que acumulam a partir das origens de previsão 06Z e 18Z.

---

## Conversões de unidades necessárias para harmonização

As unidades de temperatura e pressão são os dois pontos de conversão mais perigosos. Esquecer uma conversão Kelvin→Celsius introduz um **desvio de 273.15**; esquecer uma conversão Pascal→hectopascal introduz um **erro de fator 100**.

| Variável | CMEMS | GFS | HYCOM | ERA5 | Unidade alvo |
|---|---|---|---|---|---|
| **Temperatura** | °C ✓ | **K** (−273.15) | °C ✓ | **K** (−273.15) | °C |
| **Salinidade** | 1e-3 (PSU) | — | PSU | — | PSU |
| **Correntes** | m/s | — | m/s | — | m/s |
| **SSH** | m | — | m | — | m |
| **Vento** | — | m/s | — | m/s | m/s |
| **Pressão** | — | **Pa** (÷100) | — | **Pa** (÷100) | hPa |
| **Conc. gelo marinho** | 0–1 | 0–1 | 0–1 | 0–1 | 0–1 |
| **Batimetria** | m (positivo para baixo) | — | — | — | m (elevação, neg=oceano) |

Além da simples conversão de escala, **o tipo de temperatura difere entre CMEMS e HYCOM**. O CMEMS fornece **temperatura potencial** (`sea_water_potential_temperature`), enquanto o HYCOM fornece **temperatura in-situ** (`sea_water_temperature`). Na superfície, a diferença é desprezível (<0.001°C), mas a **4000 m de profundidade a diferença chega a ~0.35°C** devido aos efeitos de compressão adiabática. Para intercomparações no oceano profundo, a conversão via biblioteca TEOS-10 Gibbs SeaWater é essencial.

A TSM do ERA5 merece atenção especial: é uma **condição de contorno prescrita** interpolada de análises observacionais (HadISST2 historicamente, OSTIA operacionalmente), não uma previsão do modelo. O valor atualiza apenas uma vez por dia apesar de estar tecnicamente disponível em resolução horária. A temperatura de superfície do GFS (`TMP:surface`) sobre o oceano representa a **temperatura de pele** do esquema NSST, que inclui aquecimento diurno e correções de cool-skin — tornando-a fisicamente diferente tanto da TSM bulk do ERA5 quanto da temperatura a ~0.5 m de profundidade do CMEMS.

---

## Estruturas de níveis verticais comparadas

CMEMS e HYCOM fornecem campos oceânicos 3D de profundidade completa, mas diferem em número de níveis, espaçamento e profundidade mais rasa disponível.

| Profundidade (m) | Nível CMEMS | Nível HYCOM | Observações |
|---|---|---|---|
| 0.0 | — | ✓ (nível 1) | CMEMS não tem superfície verdadeira; mais raso = 0.49 m |
| 0.49 | ✓ (nível 1) | — | TSM do CMEMS é na verdade a ~0.5 m de profundidade |
| 2.0 | — | ✓ (nível 2) | HYCOM tem resolução de 2 m perto da superfície |
| 5.08 | ✓ (nível 5) | — | |
| 10.0 | — | ✓ (nível 6) | |
| 50.0 | ✓ (nível 15) | ✓ (nível 15) | Ambas as fontes têm um nível perto de 50 m |
| 100.0 | ✓ (nível 20) | ✓ (nível 20) | Boa concordância em 100 m |
| 500.0 | — | ✓ (nível 28) | CMEMS mais próximo: 541 m |
| 1000.0 | — | ✓ (nível 33) | CMEMS mais próximo: 1062 m |
| 2000.0 | — | ✓ (nível 36) | CMEMS mais próximo: 1941 m |
| 5000.0 | — | ✓ (nível 40) | CMEMS mais próximo: 5275 m |
| 5728.0 | ✓ (nível 50) | — | Nível mais profundo do CMEMS |

O CMEMS usa **50 níveis Z não uniformes** com 22 níveis concentrados nos 100 m superiores, proporcionando excelente resolução próxima à superfície (0.49, 1.54, 2.65, 3.82 m...). O HYCOM usa **40 níveis Z** com espaçamento mais grosseiro perto da superfície (0, 2, 4, 6, 8, 10 m), mas se estende até 5000 m. A interpolação vertical entre fontes requer tratamento cuidadoso das diferentes estruturas de níveis, particularmente perto da superfície onde o CMEMS não tem nível em 0 m.

---

## Máscaras de terra e convenções de fill value

Cada fonte trata valores ausentes/terra de forma diferente — uma fonte frequente de corrupção silenciosa de dados.

| Fonte | Fill value | Variável de máscara | Convenção |
|---|---|---|---|
| **CMEMS** | `9.96921e+36` (maioria) <br> `1.0e+20` (SMOC) <br> `−9999` (MOL) | `mask` em arquivo estático (1=mar, 0=terra) | Múltiplos fill values entre datasets |
| **GFS** | Bitmap GRIB2 (ausente=indefinido) | Variável `LAND` <br> (0=mar, 1=terra) | Máscara binária |
| **HYCOM** | `−30000` (int16 compactado) | Implícita via fill value | _FillValue aplicado antes de descompactar |
| **ERA5** | `_FillValue` <br> NetCDF com scale/offset | `lsm` <br> (fracionária 0.0–1.0) | Máscara terra-mar **fracionária**, não binária |
| **GEBCO** | Nenhum <br> (cobertura global) | Grade TID: <br> código 0 = terra | Sinal da elevação distingue terra (>0) de oceano (<0) |

A máscara terra-mar fracionária (com tons de cinza [0.0,1.0] bom para anti-alias mas talvez não faça sentido físico) do ERA5 é uma armadilha particularmente sutil. Ao contrário de máscaras binárias, células de grade costeiras carregam valores como 0.3 ou 0.7, significando que valores de TSM nessas células representam uma mistura. Para extração estritamente oceânica, aplique um limiar (tipicamente `lsm < 0.5`). O CMEMS agrava o problema usando **três fill values diferentes** entre suas famílias de datasets — o código deve verificar _FillValue por variável, sem assumir um valor sentinela único.

---

## Identificadores de dataset por produto e padrões de acesso

Para acesso programático, estes são os IDs exatos de dataset e URLs de acesso necessários.

**CMEMS** (Produto: GLOBAL_ANALYSISFORECAST_PHY_001_024, DOI: 10.48670/moi-00016):

| Dimensões | Variáveis | variavel dataset | tempo de atualização | resolucao  | ID do dataset |
|---|---|---|---|---|---|
| 3D | Temperatura | `thetao` | Diária ~12 UTC | 0.083° | `cmems_mod_glo_phy-anfc_0.083deg_P1D-m` |
| 3D | Correntes | `uo`, `vo` | Diária ~12 UTC | 0.083° | `cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m` |
| 3D | Salinidade | `so` | Diária ~12 UTC | 0.083° | `cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m` |
| Superfície | T, S, u, v, SSH | `thetao`, `so`, `uo`, `vo`, `zos` | Horária | 0.083° | `cmems_mod_glo_phy-anfc_0.083deg_PT1H-m` |
| 2D | SSH, MLD, gelo | `zos`, `mlotst`, `siconc` | Diária ~12 UTC | 0.083° | `cmems_mod_glo_phy-anfc_0.083deg_P1D-m` |
| 2D | T/S fundo | `thetao`, `so` em nível mais profundo | Diária ~12 UTC | 0.083° | `cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m` <br> `cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m` |

- Temperatura 3D diária: `cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m`
- Correntes 3D diárias: `cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m`
- Salinidade 3D diária: `cmems_mod_glo_phy-so_anfc_0.083deg_P1D-m`
- Superfície horária (T, S, u, v, SSH): `cmems_mod_glo_phy_anfc_0.083deg_PT1H-m`
- 2D diário (SSH, MLD, gelo, T/S fundo): `cmems_mod_glo_phy_anfc_0.083deg_P1D-m`

**GFS** (NCEP, 0.25°):
- Filtro GRIB NOMADS: `https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl`
- Padrão de arquivo: `gfs.tCCz.pgrb2.0p25.fFFF`
- Espelho AWS: `s3://noaa-gfs-bdp-pds/`

**HYCOM** (ESPC-D-V02, operacional desde ago/2024):
- Base OPeNDAP: `https://tds.hycom.org/thredds/dodsC/ESPC-D-V02/`
- Subdiretórios: `ssh/`, `t3z/YYYY`, `s3z/YYYY`, `u3z/YYYY`, `v3z/YYYY`, `ice/`
- GOFS 3.1 legado: `https://tds.hycom.org/thredds/dodsC/GLBy0.08/expt_93.0`

**ERA5** (ECMWF CDS):
- Dataset CDS: `reanalysis-era5-single-levels`
- Nomes de variáveis API usam nomes longos com underscore: `sea_surface_temperature`, `10m_u_component_of_wind`, `mean_sea_level_pressure`

**GEBCO** (grade 2024):
- App de download: `https://download.gebco.net/`
- DOI: 10.5285/1c44ce99-0a0d-5f4f-e063-7086abc0ea0f

---

## Mapeamento CF Standard Name entre fontes

Os nomes padrão CF fornecem o elo canônico entre variáveis com nomes diferentes. Nem todas as fontes seguem convenções CF igualmente bem.

| Grandeza física | CF Standard Name | CMEMS | GFS | HYCOM | ERA5 |
|---|---|---|---|---|---|
| Temperatura oceânica | `sea_water_potential_temperature` | `thetao` ✓ | — | — | — |
| Temperatura oceânica | `sea_water_temperature` | — | — | `water_temp` ✓ | — |
| TSM | `sea_surface_temperature` | — | (`WTMP`, raro) | — | `sst` ✓ |
| Temp. pele superfície | `surface_temperature` | — | `TMP:sfc` | — | `skt` |
| Corrente zonal | `eastward_sea_water_velocity` | `uo` ✓ | — | `water_u` ✓ | — |
| Corrente meridional | `northward_sea_water_velocity` | `vo` ✓ | — | `water_v` ✓ | — |
| Salinidade | `sea_water_salinity` | `so` ✓ | — | `salinity` ✓ | — |
| SSH | `sea_surface_height_above_geoid` | `zos` ✓ | — | — | — |
| SSH | `sea_surface_elevation` | — | — | `surf_el` ✓ | — |
| Vento zonal | `eastward_wind` | — | `UGRD` ✓ | — | `u10` (aprox.) |
| Vento meridional | `northward_wind` | — | `VGRD` ✓ | — | `v10` (aprox.) |
| PNMM | `air_pressure_at_mean_sea_level` | — | `PRMSL` ✓ | — | `msl` ✓ |
| Fração gelo marinho | `sea_ice_area_fraction` | `siconc` ✓ | `ICEC` ✓ | `sic` ✓ | `siconc` ✓ |
| Prof. camada mistura | `ocean_mixed_layer_thickness_defined_by_sigma_theta` | `mlotst` ✓ | — | — | — |
| Batimetria | `height_above_mean_sea_level` | — | — | — | — |

Note que o SSH do CMEMS (`zos`) usa o standard name `sea_surface_height_above_geoid` enquanto o SSH do HYCOM (`surf_el`) usa `sea_surface_elevation` — estas representam grandezas físicas ligeiramente diferentes. **O `zos` do CMEMS exclui marés, efeitos de pressão atmosférica e mudanças estéricas médias globais**, enquanto o `surf_el` do HYCOM é uma anomalia de SSH relativa à própria média do modelo. A comparação direta requer entender o que cada modelo inclui em sua definição de SSH.

---

## Cuidados para conversão e harmonização de variáveis

Com base na análise completa de referência cruzada, estas são as transformações exatas que uma camada de harmonização deve implementar, ordenadas pela severidade das consequências se esquecidas:

1. **Temperatura ERA5/GFS: subtrair 273.15** para converter K → °C
2. **Pressão ERA5/GFS: dividir por 100** para converter Pa → hPa
3. **Longitude GFS/HYCOM/ERA5: aplicar `((lon + 180) % 360) − 180`** para convenção −180/+180
4. **Elevação GEBCO: multiplicar por −1** para obter profundidade positiva para baixo (modelos oceânicos)
5. **Tempo CMEMS: converter de horas desde 1950-01-01** (época única)
6. **Tempo HYCOM: converter de horas desde 2000-01-01** (época única)
7. **Tempo ERA5: tratar épocas duplas** (1900-01-01 legado vs. 1970-01-01 novo CDS)
8. **Tempo GFS: reconstruir valid_time = reference_time + forecast_step**
9. **Dados compactados HYCOM: descompactar com `valor = compactado × scale_factor + add_offset`** antes da análise
10. **Fill values CMEMS: tratar três sentinelas diferentes** (9.97e+36, 1.0e+20, −9999)
11. **Máscara terra-mar ERA5: aplicar limiar em valores fracionários** (lsm < 0.5 = oceano)
12. **Tipo de temperatura: converter in-situ HYCOM → potencial** (ou vice-versa) via TEOS-10 para comparações em profundidade
13. **Grade de ondas ERA5: tratar grade separada de 0.5°** vs. grade atmosférica de 0.25°
14. **Acúmulos de fluxo GFS: diferenciar passos consecutivos** para obter valores de intervalo específico

---

## Escopo futuro: mapeamento de variáveis meteorológicas e de ondas

Este documento cobre o domínio de **oceanografia física**. As seguintes categorias de variáveis devem ser mapeadas em fases futuras:

### Meteorologia (Fase B.2 — futuro)

| Categoria | Fontes relevantes | Complexidade |
|---|---|---|
| Vento em múltiplos níveis (superfície, 850, 500, 250 hPa) | GFS, ERA5 | Média — mesmas fontes, níveis de pressão diferentes |
| Temperatura do ar em níveis de pressão | GFS, ERA5 | Média — mesmos 14 gotchas de unidades/coordenadas |
| Precipitação (total, convectiva, grande escala) | GFS, ERA5 | Alta — variáveis acumuladas, diferença de step necessária |
| Radiação (solar, infravermelha, líquida, descendente) | GFS, ERA5 | Alta — acumulações com origens de previsão diferentes |
| Umidade (específica, relativa, ponto de orvalho) | GFS, ERA5 | Média — unidades consistentes, mas definições de nível variam |
| Cobertura de nuvens | GFS, ERA5 | Baixa — fração 0–1 em ambas as fontes |
| CAPE / CIN | GFS, ERA5 | Baixa — J/kg em ambas, mas definições de camada diferem |
| Altura da camada limite | ERA5 | Baixa — fonte única |

### Ondas Oceânicas (Fase B.3 — futuro)

| Categoria | Fontes relevantes | Complexidade |
|---|---|---|
| Altura significativa (Hs combinada, wind waves, swell) | ERA5 (WAM), GFS (WAVEWATCH III), CMEMS (ondas) | Alta — modelos de ondas diferentes, partição swell/wind wave diverge |
| Período (médio, de pico, zero-crossing) | ERA5, GFS, CMEMS | Alta — definições de período de pico variam entre modelos |
| Direção (média, de pico, swell, wind waves) | ERA5, GFS, CMEMS | Média — convenções meteorológica vs. oceanográfica (de onde vem vs. para onde vai) |
| Espectro direcional | ERA5 (complete) | Alta — disponível apenas via sintaxe MARS, grade 0.5° |

---

## Conclusão

As cinco fontes se dividem naturalmente em três categorias funcionais: **modelos de estado do oceano** (CMEMS, HYCOM) fornecem temperatura 3D, salinidade, correntes e SSH; **reanálises/previsões atmosféricas** (ERA5, GFS) fornecem campos de forçante de superfície como vento, pressão, TSM e gelo marinho; e o **GEBCO** fornece a base batimétrica estática. Nenhuma fonte isolada cobre todas as nove categorias de variáveis, tornando a integração multi-fonte inevitável para aplicações oceânicas abrangentes.

Os pontos de integração mais traiçoeiros não são as conversões óbvias de unidade, mas as diferenças físicas sutis: CMEMS armazena temperatura potencial enquanto HYCOM armazena temperatura in-situ; a TSM do ERA5 é uma condição de contorno observacional com atualização diária enquanto a do GFS é uma temperatura de pele diurna; o `zos` do CMEMS exclui marés e barômetro invertido enquanto o `surf_el` do HYCOM inclui física diferente. Uma camada de harmonização robusta deve codificar não apenas transformações de coordenadas e unidades, mas também flags de metadados indicando qual grandeza física cada variável realmente representa — porque conceitos com nomes idênticos como "temperatura da superfície do mar" significam coisas mensuravelmente diferentes entre essas cinco fontes.