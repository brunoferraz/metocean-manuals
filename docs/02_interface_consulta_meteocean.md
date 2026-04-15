# 📘 Interface de Consulta Estruturada — Sistema Meteocean

## 1. Objetivo

Permitir que o usuário formule consultas como:

- temperatura em lat/lon, profundidade e data
- vento e corrente em um período
- comparação entre forecast e reanalysis
- comparação com dados próprios

E obter:

- provider
- produto/modelo
- variáveis
- tipo de produto
- resolução
- método de acesso
- (opcional) link/curl

---

## 2. Estrutura da Interface

### Bloco A — Tipo de consulta

- Obter dados em local/período
- Obter múltiplas variáveis
- Comparar forecast vs reanalysis
- Comparar com dados próprios
- Explorar datasets

---

### Bloco B — Variáveis

Categorias:

- Oceanografia: Temperatura, Salinidade, Correntes, Nível do mar
- Atmosfera: Vento, Pressão, Temperatura do ar
- Ondas
- Batimetria

Expansões automáticas:
- Correntes → u + v
- Vento → u + v

---

### Bloco C — Localização

Modos:
- Ponto (lat/lon)
- Área (bbox)

---

### Bloco D — Tempo e Profundidade

Tempo:
- data única ou intervalo
- resolução: horário, diário, mensal

Profundidade:
- superfície
- valor único
- faixa
- coluna completa

---

### Bloco E — Finalidade

- visualização
- análise
- validação
- comparação
- modelagem

---

## 3. Tipos de Consulta

### 3.1 Consulta simples
Seleciona datasets compatíveis com:
- variável
- espaço
- tempo
- profundidade

---

### 3.2 Multivariável
Define:
- usar mesma fonte
- combinar fontes

---

### 3.3 Forecast vs Reanalysis
Retorna:
- par compatível
- análise de compatibilidade

---

### 3.4 Comparação com dados próprios
Entrada:
- variáveis
- unidade
- tipo
- cobertura

Saída:
- dataset de referência
- conversões necessárias

---

## 4. Estrutura de Request

```json
{
  "query_type": "compare_forecast_vs_reanalysis",
  "variables": ["temperature", "currents"],
  "spatial": {"lat": -22.9, "lon": -43.2},
  "temporal": {"start": "2026-04-01", "end": "2026-04-07"},
  "vertical": {"depth": 100}
}
```

---

## 5. Estrutura de Response

```json
{
  "recommendations": [
    {
      "provider": "cmems",
      "product": "ARCTIC_ANALYSISFORECAST_PHY_002_001",
      "variables": ["thetao", "uo", "vo"],
      "type": ["forecast", "analysis"]
    }
  ],
  "warnings": ["conversion required"]
}
```

---

## 6. Layout da Interface

- Painel esquerdo: formulário
- Painel direito: resultados
- Painel inferior: diagnóstico

---

## 7. Regras de UX

- Não usar nomes técnicos na entrada
- Expandir variáveis automaticamente
- Mostrar incertezas
- Separar recomendação de execução

---

## 8. MVP

Implementar apenas:
- consulta simples
- multivariável
- comparação forecast vs reanalysis

---

## 9. Conclusão

Interface estruturada permite:

- eliminar dependência de LLM no núcleo
- garantir consistência científica
- transformar o sistema em motor determinístico

LLM pode ser usado apenas para explicação.
