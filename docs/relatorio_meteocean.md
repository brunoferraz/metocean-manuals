# 📘 Relatório Técnico — Sistema de Recomendação e Validação de Dados Meteoceanográficos

## 1. Contexto e Motivação

O objetivo do sistema é permitir que um usuário formule perguntas operacionais como:

- “Preciso da temperatura em lat/lon, profundidade e data específica”
- “Preciso de vento e corrente em um período”
- “Quero comparar forecast com reanálise”
- “Dado um dataset, qual reanálise compatível devo usar?”

E obter como resposta:

- quais dados baixar
- provider
- produto/modelo
- variáveis
- tipo (forecast, analysis, reanalysis)
- resolução temporal/espacial
- método de acesso
- (opcional) link ou comando de download

---

## 2. Diagnóstico

O sistema já possui:

- Parsing de documentos técnicos
- Extração estruturada com LLM
- Normalização semântica
- Inventário estruturado (catalog_inventory)
- Correlação entre fontes

---

## 3. Insight Central

O sistema é:

**Sistema de recomendação + validação científica de dados meteoceanográficos**

---

## 4. Problema Atual

Falta:

**Camada de consulta (query layer)**

---

## 5. Arquitetura Proposta

```
[User Query]
     ↓
interpretation
     ↓
catalog lookup
     ↓
compatibility check
     ↓
ranking
     ↓
response
```

---

## 6. Funções Necessárias

- interpret_request()
- resolve_variables()
- find_candidate_datasets()
- check_compatibility()
- rank_and_explain()

---

## 7. Tipos de Consulta

- Consulta simples
- Multivariável
- Forecast vs Reanalysis
- Comparação com dado existente

---

## 8. Saída Esperada

Exemplo:

Provider: CMEMS  
Produto: ARCTIC_ANALYSISFORECAST_PHY_002_001  
Variáveis: thetao, so, uo, vo  
Tipo: forecast/analysis  

Observações:
- Conversão necessária entre formas termodinâmicas
- Normalização de unidades

---

## 9. Papel do LLM

- Interpretação (opcional)
- Explicação
- Organização da resposta

---

## 10. Conclusão

O sistema já resolve a parte mais difícil.

O próximo passo é implementar:

**Motor de recomendação de datasets**
