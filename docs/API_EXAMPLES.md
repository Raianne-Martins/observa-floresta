# 📚 Exemplos de Uso da API - Observa Floresta

## Base URL
```
http://localhost:8000/api
```

---

## 🌳 Ação 1: Consultar Desmatamento por Estado

### POST /deforestation/state

**Request:**
```bash
curl -X POST "http://localhost:8000/api/deforestation/state" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Pará",
    "year": 2024
  }'
```

**Response:**
```json
{
  "state": "Pará",
  "state_code": "PA",
  "year": 2024,
  "area_km2": 3245.8,
  "percentage_of_total": 38.64,
  "biome": "Amazônia",
  "comparison_previous_year": {
    "year": 2023,
    "area_km2": 3862.4,
    "change_km2": -616.6,
    "change_percentage": -15.96
  },
  "data_source": "MOCK_DATA",
  "timestamp": "2024-11-14T..."
}
```

### GET /deforestation/state/{state}

**Request:**
```bash
curl "http://localhost:8000/api/deforestation/state/MT?year=2024"
```

---

## 📊 Ação 2: Comparação Temporal

### POST /deforestation/compare

**Request:**
```bash
curl -X POST "http://localhost:8000/api/deforestation/compare" \
  -H "Content-Type: application/json" \
  -d '{
    "state": "Amazonas",
    "year_start": 2020,
    "year_end": 2024
  }'
```

**Response:**
```json
{
  "state": "Amazonas",
  "state_code": "AM",
  "biome": "Amazônia",
  "year_start": 2020,
  "year_end": 2024,
  "data": [
    {"year": 2020, "area_km2": 1454.1},
    {"year": 2021, "area_km2": 2221.7},
    {"year": 2022, "area_km2": 1761.7},
    {"year": 2023, "area_km2": 1591.5},
    {"year": 2024, "area_km2": 1423.8}
  ],
  "total_change_km2": -30.3,
  "percentage_change": -2.08,
  "trend": "stable",
  "data_source": "MOCK_DATA",
  "timestamp": "2024-11-14T..."
}
```

### GET /deforestation/compare/{state}

**Request (Brasil agregado):**
```bash
curl "http://localhost:8000/api/deforestation/compare/Brasil?year_start=2020&year_end=2024"
```

---

## 🏆 Ação 3: Ranking de Estados

### POST /deforestation/ranking

**Request:**
```bash
curl -X POST "http://localhost:8000/api/deforestation/ranking" \
  -H "Content-Type: application/json" \
  -d '{
    "year": 2024,
    "order": "desc",
    "limit": 5
  }'
```

**Response:**
```json
{
  "year": 2024,
  "total_brazil_km2": 8399.0,
  "order": "desc",
  "ranking": [
    {
      "position": 1,
      "state": "Pará",
      "state_code": "PA",
      "area_km2": 3245.8,
      "percentage_of_total": 38.64,
      "biome": "Amazônia"
    },
    {
      "position": 2,
      "state": "Amazonas",
      "state_code": "AM",
      "area_km2": 1423.8,
      "percentage_of_total": 16.95,
      "biome": "Amazônia"
    },
    ...
  ],
  "data_source": "MOCK_DATA",
  "timestamp": "2024-11-14T..."
}
```

### GET /deforestation/ranking/{year}

**Request (menor para maior):**
```bash
curl "http://localhost:8000/api/deforestation/ranking/2024?order=asc&limit=3"
```

---

## 📋 Endpoints Auxiliares

### Listar Estados Disponíveis
```bash
curl "http://localhost:8000/api/deforestation/states"
```

### Listar Anos Disponíveis
```bash
curl "http://localhost:8000/api/deforestation/years"
```

---

## 🔍 Exemplos de Queries Naturais

Estas consultas poderão ser feitas via chat no frontend:

| Query Natural | Endpoint Correspondente |
|---------------|-------------------------|
| "Qual o desmatamento no Pará em 2024?" | `GET /state/Pará?year=2024` |
| "Compare Amazonas de 2020 a 2024" | `GET /compare/Amazonas?year_start=2020&year_end=2024` |
| "Quais os 5 estados que mais desmataram?" | `GET /ranking/2024?order=desc&limit=5` |
| "Mostre o ranking de menor desmatamento" | `GET /ranking/2024?order=asc` |
| "Como está o Brasil?" | `GET /compare/Brasil?year_start=2020&year_end=2024` |

