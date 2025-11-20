"""
Dados mockados completos - TODOS os biomas brasileiros
Baseados em dados aproximados de desmatamento/degradação
"""
from typing import Dict, List, Optional
from datetime import datetime

# ==========================================
# DEFINIÇÕES DE BIOMAS E ESTADOS
# ==========================================

BIOMES = [
    "Amazônia",
    "Cerrado", 
    "Mata Atlântica",
    "Caatinga",
    "Pampa",
    "Pantanal"
]

# Estados brasileiros com seus biomas predominantes
STATES_BY_BIOME = {
    "Amazônia": ["Acre", "Amapá", "Amazonas", "Pará", "Rondônia", "Roraima", "Tocantins", "Mato Grosso", "Maranhão"],
    "Cerrado": ["Goiás", "Tocantins", "Mato Grosso", "Mato Grosso do Sul", "Minas Gerais", "Bahia", "Maranhão", "Piauí", "São Paulo", "Paraná", "Distrito Federal"],
    "Mata Atlântica": ["Rio Grande do Sul", "Santa Catarina", "Paraná", "São Paulo", "Rio de Janeiro", "Espírito Santo", "Minas Gerais", "Bahia", "Sergipe", "Alagoas", "Pernambuco", "Paraíba", "Rio Grande do Norte", "Ceará", "Piauí", "Goiás", "Mato Grosso do Sul"],
    "Caatinga": ["Bahia", "Ceará", "Paraíba", "Pernambuco", "Piauí", "Rio Grande do Norte", "Alagoas", "Sergipe", "Maranhão", "Minas Gerais"],
    "Pampa": ["Rio Grande do Sul"],
    "Pantanal": ["Mato Grosso", "Mato Grosso do Sul"]
}

# Todos os estados brasileiros
ALL_STATES = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapá",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceará",
    "DF": "Distrito Federal",
    "ES": "Espírito Santo",
    "GO": "Goiás",
    "MA": "Maranhão",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Pará",
    "PB": "Paraíba",
    "PR": "Paraná",
    "PE": "Pernambuco",
    "PI": "Piauí",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondônia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "São Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}

STATE_CODES = {v: k for k, v in ALL_STATES.items()}

# Bioma predominante por estado
STATE_PRIMARY_BIOME = {
    "Acre": "Amazônia",
    "Alagoas": "Caatinga",
    "Amapá": "Amazônia",
    "Amazonas": "Amazônia",
    "Bahia": "Caatinga",
    "Ceará": "Caatinga",
    "Distrito Federal": "Cerrado",
    "Espírito Santo": "Mata Atlântica",
    "Goiás": "Cerrado",
    "Maranhão": "Amazônia",
    "Mato Grosso": "Amazônia",
    "Mato Grosso do Sul": "Cerrado",
    "Minas Gerais": "Cerrado",
    "Pará": "Amazônia",
    "Paraíba": "Caatinga",
    "Paraná": "Mata Atlântica",
    "Pernambuco": "Caatinga",
    "Piauí": "Cerrado",
    "Rio de Janeiro": "Mata Atlântica",
    "Rio Grande do Norte": "Caatinga",
    "Rio Grande do Sul": "Pampa",
    "Rondônia": "Amazônia",
    "Roraima": "Amazônia",
    "Santa Catarina": "Mata Atlântica",
    "São Paulo": "Mata Atlântica",
    "Sergipe": "Caatinga",
    "Tocantins": "Cerrado"
}

# ==========================================
# DADOS DE DESMATAMENTO/DEGRADAÇÃO POR ESTADO
# ==========================================

# Dados aproximados de degradação ambiental (km²) por ano
DEGRADATION_DATA: Dict[str, Dict[int, float]] = {
    # AMAZÔNIA (dados já existentes)
    "Pará": {2020: 5075.6, 2021: 4974.2, 2022: 4258.7, 2023: 3862.4, 2024: 3245.8},
    "Mato Grosso": {2020: 1781.5, 2021: 1508.9, 2022: 1673.1, 2023: 1439.6, 2024: 1245.3},
    "Amazonas": {2020: 1454.1, 2021: 2221.7, 2022: 1761.7, 2023: 1591.5, 2024: 1423.8},
    "Rondônia": {2020: 1247.5, 2021: 1249.8, 2022: 1387.4, 2023: 1089.7, 2024: 967.4},
    "Acre": {2020: 634.2, 2021: 872.7, 2022: 1015.3, 2023: 789.3, 2024: 654.7},
    "Maranhão": {2020: 267.6, 2021: 271.3, 2022: 485.6, 2023: 387.2, 2024: 312.5},
    "Roraima": {2020: 290.2, 2021: 1016.6, 2022: 649.9, 2023: 498.3, 2024: 423.6},
    "Tocantins": {2020: 94.3, 2021: 102.9, 2022: 127.4, 2023: 98.7, 2024: 87.3},
    "Amapá": {2020: 31.7, 2021: 54.3, 2022: 58.9, 2023: 45.2, 2024: 38.6},
    
    # CERRADO
    "Goiás": {2020: 456.3, 2021: 423.1, 2022: 398.7, 2023: 412.5, 2024: 387.9},
    "Mato Grosso do Sul": {2020: 378.4, 2021: 345.2, 2022: 367.8, 2023: 334.6, 2024: 298.3},
    "Minas Gerais": {2020: 289.1, 2021: 312.4, 2022: 267.9, 2023: 245.8, 2024: 223.4},
    "Bahia": {2020: 234.6, 2021: 256.8, 2022: 278.3, 2023: 198.7, 2024: 187.2},
    "Piauí": {2020: 178.3, 2021: 192.4, 2022: 165.7, 2023: 156.9, 2024: 143.5},
    "Distrito Federal": {2020: 12.4, 2021: 9.8, 2022: 11.2, 2023: 8.9, 2024: 7.3},
    
    # MATA ATLÂNTICA
    "São Paulo": {2020: 123.4, 2021: 115.7, 2022: 109.3, 2023: 98.6, 2024: 89.2},
    "Paraná": {2020: 98.7, 2021: 87.3, 2022: 92.1, 2023: 79.4, 2024: 73.8},
    "Santa Catarina": {2020: 76.3, 2021: 69.8, 2022: 72.4, 2023: 64.2, 2024: 58.9},
    "Rio Grande do Sul": {2020: 87.1, 2021: 79.6, 2022: 83.2, 2023: 71.8, 2024: 67.3},
    "Rio de Janeiro": {2020: 54.3, 2021: 48.9, 2022: 52.1, 2023: 43.7, 2024: 39.8},
    "Espírito Santo": {2020: 43.2, 2021: 38.7, 2022: 41.3, 2023: 35.6, 2024: 32.1},
    
    # CAATINGA
    "Ceará": {2020: 145.6, 2021: 132.8, 2022: 139.4, 2023: 121.3, 2024: 112.7},
    "Pernambuco": {2020: 112.3, 2021: 98.7, 2022: 104.5, 2023: 93.2, 2024: 87.6},
    "Paraíba": {2020: 89.4, 2021: 82.1, 2022: 87.3, 2023: 76.8, 2024: 71.2},
    "Rio Grande do Norte": {2020: 67.8, 2021: 61.3, 2022: 64.9, 2023: 57.4, 2024: 53.1},
    "Alagoas": {2020: 45.3, 2021: 41.7, 2022: 43.8, 2023: 38.9, 2024: 36.2},
    "Sergipe": {2020: 34.7, 2021: 31.2, 2022: 33.4, 2023: 29.1, 2024: 27.3},
    
    # PANTANAL (já incluído em MT e MS acima, mas com dados específicos)
    
    # PAMPA (já incluído em RS acima)
}


BRAZIL_TOTAL: Dict[int, float] = {
    2020: sum(data.get(2020, 0) for data in DEGRADATION_DATA.values()),
    2021: sum(data.get(2021, 0) for data in DEGRADATION_DATA.values()),
    2022: sum(data.get(2022, 0) for data in DEGRADATION_DATA.values()),
    2023: sum(data.get(2023, 0) for data in DEGRADATION_DATA.values()),
    2024: sum(data.get(2024, 0) for data in DEGRADATION_DATA.values()),
}


BIOME_TOTALS: Dict[str, Dict[int, float]] = {}
for biome in BIOMES:
    BIOME_TOTALS[biome] = {}
    for year in [2020, 2021, 2022, 2023, 2024]:
        total = 0
        for state in STATES_BY_BIOME.get(biome, []):
            total += DEGRADATION_DATA.get(state, {}).get(year, 0)
        BIOME_TOTALS[biome][year] = total


# ==========================================
# FUNÇÕES DE CONSULTA
# ==========================================

def get_state_data(state: str, year: int) -> Dict:
    """Retorna dados de um estado específico"""
    state_name = normalize_state_name(state)
    
    if state_name not in DEGRADATION_DATA:
        raise ValueError(f"Estado '{state}' não encontrado")
    
    if year not in DEGRADATION_DATA[state_name]:
        raise ValueError(f"Ano {year} não disponível. Anos: 2020-2024")
    
    area_km2 = DEGRADATION_DATA[state_name][year]
    total_brazil = BRAZIL_TOTAL[year]
    percentage = (area_km2 / total_brazil) * 100
    
    previous_year = year - 1
    previous_area = DEGRADATION_DATA[state_name].get(previous_year, 0)
    
    if previous_area > 0:
        change_km2 = area_km2 - previous_area
        change_percentage = ((area_km2 - previous_area) / previous_area) * 100
    else:
        change_km2 = 0
        change_percentage = 0
    
    return {
        "state": state_name,
        "state_code": STATE_CODES[state_name],
        "year": year,
        "area_km2": round(area_km2, 2),
        "percentage_of_total": round(percentage, 2),
        "biome": STATE_PRIMARY_BIOME[state_name],
        "comparison_previous_year": {
            "year": previous_year,
            "area_km2": round(previous_area, 2) if previous_area > 0 else None,
            "change_km2": round(change_km2, 2),
            "change_percentage": round(change_percentage, 2)
        },
        "data_source": "MOCK_DATA_BRAZIL",
        "timestamp": datetime.utcnow().isoformat()
    }


def get_comparison_data(state_or_biome: str, year_start: int, year_end: int) -> Dict:
    """Compara dados entre períodos (estado ou bioma)"""
    if year_start >= year_end:
        raise ValueError("Ano inicial deve ser menor que ano final")
    
    if state_or_biome.upper() in ["BRASIL", "BRAZIL"]:
        data_points = []
        for year in range(year_start, year_end + 1):
            if year in BRAZIL_TOTAL:
                data_points.append({
                    "year": year,
                    "area_km2": round(BRAZIL_TOTAL[year], 2)
                })
        
        entity_name = "Brasil"
        entity_code = "BR"
        biome = "Todos os biomas"
    
    elif state_or_biome.title() in BIOMES or state_or_biome.upper() in [b.upper() for b in BIOMES]:
        biome_name = next((b for b in BIOMES if b.upper() == state_or_biome.upper()), state_or_biome.title())
        
        data_points = []
        for year in range(year_start, year_end + 1):
            if year in BIOME_TOTALS.get(biome_name, {}):
                data_points.append({
                    "year": year,
                    "area_km2": round(BIOME_TOTALS[biome_name][year], 2)
                })
        
        entity_name = biome_name
        entity_code = biome_name[:3].upper()
        biome = biome_name
    
    else:
        state_name = normalize_state_name(state_or_biome)
        
        if state_name not in DEGRADATION_DATA:
            raise ValueError(f"Estado ou bioma '{state_or_biome}' não encontrado")
        
        data_points = []
        for year in range(year_start, year_end + 1):
            if year in DEGRADATION_DATA[state_name]:
                data_points.append({
                    "year": year,
                    "area_km2": round(DEGRADATION_DATA[state_name][year], 2)
                })
        
        entity_name = state_name
        entity_code = STATE_CODES[state_name]
        biome = STATE_PRIMARY_BIOME[state_name]
    
    if not data_points:
        raise ValueError(f"Sem dados para o período {year_start}-{year_end}")
    
    first_value = data_points[0]["area_km2"]
    last_value = data_points[-1]["area_km2"]
    total_change_km2 = last_value - first_value
    percentage_change = ((last_value - first_value) / first_value) * 100
    
    if percentage_change > 5:
        trend = "increasing"
    elif percentage_change < -5:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        "state": entity_name,
        "state_code": entity_code,
        "biome": biome,
        "year_start": year_start,
        "year_end": year_end,
        "data": data_points,
        "total_change_km2": round(total_change_km2, 2),
        "percentage_change": round(percentage_change, 2),
        "trend": trend,
        "data_source": "MOCK_DATA_BRAZIL",
        "timestamp": datetime.utcnow().isoformat()
    }


def get_ranking_data(year: int, order: str = "desc", limit: int = 10, biome: Optional[str] = None) -> Dict:
    """Retorna ranking de estados"""
    if year not in BRAZIL_TOTAL:
        raise ValueError(f"Ano {year} não disponível. Anos: 2020-2024")
    
    states_data = []
    states_to_include = DEGRADATION_DATA.keys()
    
    if biome:
        biome_title = next((b for b in BIOMES if b.upper() == biome.upper()), None)
        if biome_title:
            states_to_include = [s for s in states_to_include if s in STATES_BY_BIOME.get(biome_title, [])]
    
    for state_name in states_to_include:
        if year in DEGRADATION_DATA[state_name]:
            area_km2 = DEGRADATION_DATA[state_name][year]
            percentage = (area_km2 / BRAZIL_TOTAL[year]) * 100
            
            states_data.append({
                "state": state_name,
                "state_code": STATE_CODES[state_name],
                "area_km2": round(area_km2, 2),
                "percentage_of_total": round(percentage, 2),
                "biome": STATE_PRIMARY_BIOME[state_name]
            })
    
    reverse = (order.lower() == "desc")
    states_data.sort(key=lambda x: x["area_km2"], reverse=reverse)
    
    ranking = []
    for i, state_data in enumerate(states_data[:limit], 1):
        ranking.append({
            "position": i,
            **state_data
        })
    
    return {
        "year": year,
        "total_brazil_km2": round(BRAZIL_TOTAL[year], 2),
        "order": order,
        "biome_filter": biome,
        "ranking": ranking,
        "data_source": "MOCK_DATA_BRAZIL",
        "timestamp": datetime.utcnow().isoformat()
    }


def get_biome_comparison(year: int) -> Dict:
    """Compara todos os biomas em um ano específico"""
    if year not in BRAZIL_TOTAL:
        raise ValueError(f"Ano {year} não disponível")
    
    biome_data = []
    for biome in BIOMES:
        total = BIOME_TOTALS[biome][year]
        percentage = (total / BRAZIL_TOTAL[year]) * 100
        
        biome_data.append({
            "biome": biome,
            "area_km2": round(total, 2),
            "percentage_of_total": round(percentage, 2),
            "num_states": len(STATES_BY_BIOME[biome])
        })
    
    biome_data.sort(key=lambda x: x["area_km2"], reverse=True)
    
    return {
        "year": year,
        "total_brazil_km2": round(BRAZIL_TOTAL[year], 2),
        "biomes": biome_data,
        "data_source": "MOCK_DATA_BRAZIL",
        "timestamp": datetime.utcnow().isoformat()
    }


def get_available_biomes() -> List[str]:
    """Retorna lista de biomas disponíveis"""
    return BIOMES.copy()


def get_available_states(biome: Optional[str] = None) -> Dict:
    """Retorna lista de estados disponíveis"""
    if biome:
        biome_title = next((b for b in BIOMES if b.upper() == biome.upper()), None)
        if not biome_title:
            raise ValueError(f"Bioma '{biome}' não encontrado")
        
        states = [
            {
                "name": state,
                "code": STATE_CODES[state],
                "biome": STATE_PRIMARY_BIOME[state]
            }
            for state in STATES_BY_BIOME[biome_title]
        ]
    else:
        states = [
            {
                "name": state,
                "code": STATE_CODES[state],
                "biome": STATE_PRIMARY_BIOME[state]
            }
            for state in sorted(ALL_STATES.values())
        ]
    
    return {
        "states": states,
        "total": len(states),
        "biome_filter": biome,
        "timestamp": datetime.utcnow().isoformat()
    }


def get_available_years() -> Dict:
    """Retorna lista de anos disponíveis"""
    years = sorted(BRAZIL_TOTAL.keys())
    return {
        "years": years,
        "total": len(years),
        "timestamp": datetime.utcnow().isoformat()
    }


def normalize_state_name(state: str) -> str:
    """Normaliza nome ou sigla do estado"""
    state = state.strip()
    
    if len(state) == 2:
        state = state.upper()
        if state in ALL_STATES:
            return ALL_STATES[state]
 
    for code, name in ALL_STATES.items():
        if name.lower() == state.lower():
            return name
    
 
    state_lower = state.lower()
    for name in ALL_STATES.values():
        if state_lower in name.lower() or name.lower() in state_lower:
            return name
    
    raise ValueError(f"Estado '{state}' não reconhecido")