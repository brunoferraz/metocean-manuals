# 📘 Wireframe — Interface de Consulta Meteocean

## 1. Visão Geral

Layout principal dividido em três áreas:

```
┌───────────────────────────────────────────────┐
│ HEADER                                        │
├───────────────┬───────────────────────────────┤
│ FORMULÁRIO    │ RESULTADOS                    │
│               │                               │
├───────────────┴───────────────────────────────┤
│ DIAGNÓSTICO (colapsável)                      │
└───────────────────────────────────────────────┘
```

---

## 2. Header

```
🌊 Meteocean Data Assistant
[Nova Consulta] [Histórico] [Configurações]
```

---

## 3. Painel Esquerdo — Formulário

### Tipo de Consulta
- Dados em local/período
- Multivariável
- Forecast vs Reanalysis
- Comparar com meus dados

### Variáveis
- Temperatura
- Correntes
- Vento

Expansões automáticas:
- Correntes → u + v
- Vento → u + v

---

### Localização
- Ponto (lat/lon)
- Área (bbox)

---

### Tempo
- Data inicial / final
- Resolução (melhor disponível, diário, horário)

---

### Profundidade
- Superfície
- Valor único
- Faixa

---

### Preferências
- Provider opcional
- Permitir múltiplas fontes
- Compatibilidade estrita

---

### Objetivo
- Visualização
- Validação
- Comparação
- Modelagem

---

## 4. Painel Direito — Resultados

### Recomendação Principal

- Provider: CMEMS
- Produto: ARCTIC_ANALYSISFORECAST_PHY_002_001
- Tipo: forecast / analysis
- Variáveis: thetao, uo, vo
- Acesso: netcdf4 / API

---

### Alternativas
- ERA5
- HYCOM

---

### Alertas Técnicos

- Diferença entre temperatura potencial e in-situ
- Conversão necessária
- Diferença de unidade (Pa vs hPa)

---

### Explicação

Texto explicando:
- por que foi escolhido
- limitações
- compatibilidade

---

## 5. Painel Inferior — Diagnóstico

- Variáveis resolvidas
- Filtros aplicados
- Datasets descartados
- Motivos

---

## 6. Fluxo de Uso

1. Usuário preenche formulário
2. Clica em buscar
3. Sistema:
   - interpreta query
   - busca no catálogo
   - valida compatibilidade
   - retorna recomendação

---

## 7. Regras de UX

- Não usar nomes técnicos na entrada
- Expandir variáveis automaticamente
- Mostrar conflitos antes da resposta
- Separar recomendação de execução

---

## 8. MVP

Implementar inicialmente:

- Consulta simples
- Forecast vs Reanalysis
- Campos básicos:
  - variável
  - localização
  - tempo
  - profundidade

---

## 9. Conclusão

A interface estruturada:

- elimina ambiguidade
- reduz necessidade de LLM
- permite lógica determinística
- melhora confiabilidade científica

Transforma o sistema em uma ferramenta técnica de decisão.
