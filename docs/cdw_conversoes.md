# Conversões críticas para trabalhar com múltiplos datasets oceânicos e meteorológicos

---

* **1. Temperatura ERA5/GFS:**
    - K → °C (subtrair 273.15)

    Essas duas fontes fornecem temperatura em Kelvin. Sem conversão, os valores ficam ~273° acima do correto.

* **2. Pressão ERA5/GFS:** 
    - Pa → hPa (dividir por 100)

    A pressão vem em Pascal, mas o padrão oceanográfico/meteorológico é hectopascal. Erro de fator 100.

* **3. Longitude GFS/HYCOM/ERA5:** 

    - 0–360 → −180/+180

    Essas fontes usam longitude 0–360, enquanto CMEMS e GEBCO usam −180/+180. Sem conversão, dados aparecem deslocados meio globo ou retornam NaN.

* **4. Elevação GEBCO:** 
    - multiplicar por −1

    O GEBCO usa elevação (oceano = negativo). Modelos oceânicos usam profundidade positiva para baixo. Sem inversão, a batimetria fica com sinal trocado.

* **5. Tempo CMEMS:** 
    
    - horas desde 1950-01-01

    Época temporal própria. Sem conversão explícita, as datas ficam erradas silenciosamente.

* **6. Tempo HYCOM:**
    - horas desde 2000-01-01

    Outra época temporal distinta. Mesmo problema da regra anterior.

* **7. Tempo ERA5:**

    - épocas duplas (1900-01-01 legado vs. 1970-01-01 novo CDS)

    Dependendo da versão da API, a época muda. Misturar as duas corrompe a série temporal.

* **8. Tempo GFS:**

    - valid_time = reference_time + forecast_step

    O GFS não armazena um timestamp direto — é preciso somar o horário de inicialização ao passo de previsão para obter o tempo real.

* **9. Dados compactados HYCOM:**

    - descompactar com scale_factor e add_offset

    Os dados vêm como int16 compactado. Sem aplicar `valor = compactado × scale + offset`, os valores são lixo numérico.

* **10. Fill values CMEMS:**

    - tratar três sentinelas diferentes (9.97e+36, 1.0e+20, −9999)

    O CMEMS não usa um único valor de ausência — cada família de dataset pode ter um diferente. Assumir um só contamina os dados com valores gigantes ou negativos.

* **11. Máscara terra-mar ERA5:**

    - aplicar limiar nos valores fracionários

    A máscara do ERA5 não é binária (0 ou 1), mas fracionária (ex: 0.3 em células costeiras). Sem limiar (ex: `lsm < 0.5`), dados costeiros misturam terra e oceano.

* **12. Tipo de temperatura:**

    - in-situ (HYCOM) vs. potencial (CMEMS) via TEOS-10

    Na superfície a diferença é desprezível, mas a 4000 m chega a ~0.35°C. Para comparações em profundidade, é obrigatório converter usando a biblioteca Gibbs SeaWater.

* **13. Grade de ondas ERA5:**

    - grade separada de 0.5° vs. atmosférica de 0.25°

    A altura significativa de onda vem numa grade diferente do vento e pressão. Misturar sem reinterpolação gera incompatibilidade espacial.

* **14. Acúmulos de fluxo GFS:**
    - diferenciar passos consecutivos

    Variáveis de fluxo do GFS (radiação, precipitação) são acumuladas desde a inicialização, não instantâneas. Para obter o valor de um intervalo específico, é preciso subtrair passos consecutivos.



## Conversões agrupadas por tipo

---

### Unidades físicas

| # | Conversão | Fontes afetadas | Por quê |
|---|---|---|---|
| 1 | Temperatura: <br> K → °C (−273.15) | ERA5, GFS | Desvio de 273.15 nos valores |
| 2 | Pressão: <br> Pa → hPa (÷100) | ERA5, GFS | Erro de fator 100 |
| 4 | Batimetria: <br> inverter sinal | GEBCO | Oceano vem negativo; modelos usam profundidade positiva para baixo |
| 12 | Temperatura: <br> in-situ → potencial (TEOS-10) | HYCOM ↔ CMEMS | Diferença de até 0.35°C a 4000 m |

### Coordenadas espaciais

| # | Conversão | Fontes afetadas | Por quê |
|---|---|---|---|
| 3 | Longitude: <br> 0–360 → −180/+180 | GFS, HYCOM, ERA5 | Dados deslocados meio globo ou NaN em longitudes negativas |
| 13 | Grade de ondas separada <br> (0.5° vs 0.25°) | ERA5 | Onda e atmosfera vivem em grades diferentes; requer reinterpolação |

### Coordenadas temporais

| # | Conversão | Fontes afetadas | Por quê |
|---|---|---|---|
| 5 | Época: <br> horas desde 1950-01-01 | CMEMS | Época própria; datas erradas silenciosamente |
| 6 | Época: <br> horas desde 2000-01-01 | HYCOM | Época própria; datas erradas silenciosamente |
| 7 | Épocas duplas: <br> 1900 vs 1970 | ERA5 | Versão da API muda a referência; corrompe séries |
| 8 | valid_time = ref_time + forecast_step | GFS | Não há timestamp direto; precisa reconstruir |
| 14 | Fluxos acumulados: <br> diferenciar steps | GFS | Valores são acumulados desde a inicialização, não instantâneos |

### Máscaras e valores ausentes

| # | Conversão | Fontes afetadas | Por quê |
|---|---|---|---|
| 9 | Escala e offset: <br> Descompactar int16 com scale/offset | HYCOM | Sem aplicar, valores são lixo numérico |
| 10 | Valores nulos: <br> Três fill values diferentes | CMEMS | Assumir um só contamina dados com sentinelas gigantes |
| 11 | Máscara terra-mar fracionária → limiar | ERA5 | Sem limiar, células costeiras misturam terra e oceano |

---

## Mesmas conversões agrupadas por fonte (grid)

### GFS

| grid | resolução | longitude | latitude |
|---|---|---|---|
| `GFS` | 0.25° | 0–360 | N→S |

| # | Conversão | |
|---|---|---|
| 1 | Temperatura | K → °C |
| 2 | Pressão | Pa → hPa |
| 3 | Longitude | 0–360 → −180/+180 |
| 8 | Reconstruir valid_time | |
| 14 | Diferenciar acúmulos de fluxo | |

### ERA5
| grid | resolução | longitude | latitude |
|---|---|---|---|
| `ERA5` | 0.25° atmo / 0.5° ondas | 0–360 | N→S |

| # | Conversão | |
|---|---|---|   
| 1 | Temperatura | K → °C |
| 2 | Pressão | Pa → hPa |
| 3 | Longitude | 0–360 → −180/+180 |
| 7 | Tratar épocas duplas | 1900 vs 1970 |
| 11 | Limiar na máscara terra-mar fracionária | |
| 13 | Reinterpolação grade ondas | 0.5° → 0.25° |

### HYCOM
| grid | resolução | longitude | latitude |
|---|---|---|---|
| `HYCOM` | 0.08° | 0–360 | S→N |

| # | Conversão | |
|---|---|---|
| 3 | Longitude | 0–360 → −180/+180 |
| 6 | Época temporal desde 2000-01-01 | |
| 9 | Descompactar int16 (scale + offset) | |
| 12 | Temperatura in-situ → potencial (TEOS-10) | |

### CMEMS
| grid | resolução | longitude | latitude |
|---|---|---|---|
| `CMEMS` | 1/12° | −180/+180 | S→N |

| # | Conversão | |
|---|---|---|
| 5 | Época temporal desde 1950-01-01 | |
| 10 | Tratar três fill values distintos | |
| 12 | Já é temperatura potencial (referência para conversão) | |

### GEBCO
| grid | resolução | longitude | latitude |
|---|---|---|---|
| `GEBCO` | 15 arc-sec | −180/+180 | S→N |

| # | Conversão | |
|---|---|---|
| 4 | Inverter sinal da elevação para profundidade positiva | |