"""
Dados mockados para desenvolvimento
Baseados em dados reais de desmatamento da Amazônia Legal
"""
from typing import Dict, List
from datetime import datetime

# Estados da Amazônia Legal
AMAZONIA_LEGAL_STATES = [
    "Acre", "Amapá", "Amazonas", "Pará", "Rondônia", 
    "Roraima", "Tocantins", "Mato Grosso", "Maranhão"
]

# Siglas dos estados
STATE_CODES = {
    "Acre": "AC",
    "Amapá": "AP",
    "Amazonas": "AM",
    "Pará": "PA",
    "Rondônia": "RO",
    "Roraima": "RR",
    "Tocantins": "TO",
    "Mato Grosso": "MT",
    "Maranhão": "MA"
}

# Biomas por estado
STATE_BIOMES = {
    "Acre": "Amazônia",
    "Amapá": "Amazônia",
    "Amazonas": "Amazônia",
    "Pará": "Amazônia",
    "Rondônia": "Amazônia",
    "Roraima": "Amazônia",
    "Tocantins": "Cerrado/Amazônia",
    "Mato Grosso": "Amazônia/Cerrado/Pantanal",
    "Maranhão": "Amazônia/Cerrado"
}

# Dados de desmatamento por estado e ano (em km²)
# Valores aproximados baseados em dados históricos do INPE
DEFORESTATION_DATA: Dict[str, Dict[int, float]] = {
    "Pará": {
        2020: 5075.6,
        2021: 4974.2,
        2022: 4258.7,
        2023: 3862.4,
        2024: 3245.8
    },
    "Mato Grosso": {
        2020: 1781.5,
        2021: 1508.9,
        2022: 1673.1,
        2023: 1439.6,
        2024: 1245.3
    },
    "Amazonas": {
        2020: 1454.1,
        2021: 2221.7,
        2022: 1761.7,
        2023: 1591.5,
        2024: 1423.8
    },
    "Rondônia": {
        2020: 1247.5,
        2021: 1249.8,
        2022: 1387.4,
        2023: 1089.7,
        2024: 967.4
    },
    "Acre": {
        2020: 634.2,
        2021: 872.7,
        2022: 1015.3,
        2023: 789.3,
        2024: 654.7
    },
    "Maranhão": {
        2020: 267.6,
        2021: 271.3,
        2022: 485.6,
        2023: 387.2,
        2024: 312.5
    },
    "Roraima": {
        2020: 290.2,
        2021: 1016.6,
        2022: 649.9,
        2023: 498.3,
        2024: 423.6
    },
    "Tocantins": {
        2020: 94.3,
        2021: 102.9,
        2022: 127.4,
        2023: 98.7,
        2024: 87.3
    },
    "Amapá": {
        2020: 31.7,
        2021: 54.3,
        2022: 58.9,
        2023: 45.2,
        2024: 38.6
    }
}

# Total Brasil por ano
BRAZIL_TOTAL: Dict[int, float] = {
    2020: 10851.0,
    2021: 13272.4,
    2022: 11418.0,
    2023: 9801.9,
    2024: 8399.0
}


def get_state_data(state: str, year: int) -> Dict:
    """
    Retorna dados de desmatamento para um estado específico
    
    Args:
        state: Nome do estado ou sigla (ex: "Pará" ou "PA")
        year: Ano da consulta
    
    Returns:
        Dados de desmatamento do estado
    """
    # Normalizar nome do estado
    state_name = normalize_state_name(state)
    
    if state_name not in DEFORESTATION_DATA:
        raise ValueError(f"Estado '{state}' não encontrado na Amazônia Legal")
    
    if year not in DEFORESTATION_DATA[state_name]:
        raise ValueError(f"Ano {year} não disponível. Anos disponíveis: 2020-2024")
    
    area_km2 = DEFORESTATION_DATA[state_name][year]
    total_brazil = BRAZIL_TOTAL[year]
    percentage = (area_km2 / total_brazil) * 100
    
    # Calcular comparação com ano anterior
    previous_year = year - 1
    previous_area = DEFORESTATION_DATA[state_name].get(previous_year, 0)
    
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
        "biome": STATE_BIOMES[state_name],
        "comparison_previous_year": {
            "year": previous_year,
            "area_km2": round(previous_area, 2) if previous_area > 0 else None,
            "change_km2": round(change_km2, 2),
            "change_percentage": round(change_percentage, 2)
        },
        "data_source": "MOCK_DATA",
        "timestamp": datetime.utcnow().isoformat()
    }


def get_comparison_data(state: str, year_start: int, year_end: int) -> Dict:
    """
    Compara desmatamento entre dois períodos
    
    Args:
        state: Nome do estado ou "Brasil" para agregado
        year_start: Ano inicial
        year_end: Ano final
    
    Returns:
        Dados de comparação temporal
    """
    if year_start >= year_end:
        raise ValueError("Ano inicial deve ser menor que ano final")
    
    if state.upper() == "BRASIL" or state.upper() == "BRAZIL":
        # Dados agregados do Brasil
        data_points = []
        for year in range(year_start, year_end + 1):
            if year in BRAZIL_TOTAL:
                data_points.append({
                    "year": year,
                    "area_km2": round(BRAZIL_TOTAL[year], 2)
                })
        
        state_name = "Brasil"
        state_code = "BR"
        biome = "Amazônia Legal"
    else:
        # Dados de estado específico
        state_name = normalize_state_name(state)
        
        if state_name not in DEFORESTATION_DATA:
            raise ValueError(f"Estado '{state}' não encontrado")
        
        data_points = []
        for year in range(year_start, year_end + 1):
            if year in DEFORESTATION_DATA[state_name]:
                data_points.append({
                    "year": year,
                    "area_km2": round(DEFORESTATION_DATA[state_name][year], 2)
                })
        
        state_code = STATE_CODES[state_name]
        biome = STATE_BIOMES[state_name]
    
    if not data_points:
        raise ValueError(f"Sem dados disponíveis para o período {year_start}-{year_end}")
    
    # Calcular mudanças
    first_value = data_points[0]["area_km2"]
    last_value = data_points[-1]["area_km2"]
    total_change_km2 = last_value - first_value
    percentage_change = ((last_value - first_value) / first_value) * 100
    
    # Determinar tendência
    if percentage_change > 5:
        trend = "increasing"
    elif percentage_change < -5:
        trend = "decreasing"
    else:
        trend = "stable"
    
    return {
        "state": state_name,
        "state_code": state_code,
        "biome": biome,
        "year_start": year_start,
        "year_end": year_end,
        "data": data_points,
        "total_change_km2": round(total_change_km2, 2),
        "percentage_change": round(percentage_change, 2),
        "trend": trend,
        "data_source": "MOCK_DATA",
        "timestamp": datetime.utcnow().isoformat()
    }


def get_ranking_data(year: int, order: str = "desc", limit: int = 10) -> Dict:
    """
    Retorna ranking de estados por desmatamento
    
    Args:
        year: Ano da consulta
        order: Ordem ("desc" = maior para menor, "asc" = menor para maior)
        limit: Número de estados no ranking
    
    Returns:
        Ranking de estados
    """
    if year not in BRAZIL_TOTAL:
        raise ValueError(f"Ano {year} não disponível. Anos disponíveis: 2020-2024")
    
    # Coletar dados de todos os estados
    states_data = []
    for state_name, years_data in DEFORESTATION_DATA.items():
        if year in years_data:
            area_km2 = years_data[year]
            percentage = (area_km2 / BRAZIL_TOTAL[year]) * 100
            
            states_data.append({
                "state": state_name,
                "state_code": STATE_CODES[state_name],
                "area_km2": round(area_km2, 2),
                "percentage_of_total": round(percentage, 2),
                "biome": STATE_BIOMES[state_name]
            })
    
    # Ordenar
    reverse = (order.lower() == "desc")
    states_data.sort(key=lambda x: x["area_km2"], reverse=reverse)
    
    # Adicionar posição
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
        "ranking": ranking,
        "data_source": "MOCK_DATA",
        "timestamp": datetime.utcnow().isoformat()
    }


def normalize_state_name(state: str) -> str:
    """
    Normaliza nome ou sigla do estado
    
    Args:
        state: Nome ou sigla do estado
    
    Returns:
        Nome completo do estado
    """
    state = state.strip()
    
    # Se for sigla
    if len(state) == 2:
        state = state.upper()
        for name, code in STATE_CODES.items():
            if code == state:
                return name
    
    # Se for nome (case insensitive)
    for name in AMAZONIA_LEGAL_STATES:
        if name.lower() == state.lower():
            return name
    
    # Tentar match parcial
    state_lower = state.lower()
    for name in AMAZONIA_LEGAL_STATES:
        if state_lower in name.lower() or name.lower() in state_lower:
            return name
    
    raise ValueError(f"Estado '{state}' não reconhecido")


def get_available_states() -> List[Dict[str, str]]:
    """
    Retorna lista de estados disponíveis
    
    Returns:
        Lista de estados com códigos
    """
    return [
        {
            "name": state,
            "code": STATE_CODES[state],
            "biome": STATE_BIOMES[state]
        }
        for state in AMAZONIA_LEGAL_STATES
    ]


def get_available_years() -> List[int]:
    """
    Retorna lista de anos disponíveis
    
    Returns:
        Lista de anos
    """
    return sorted(BRAZIL_TOTAL.keys())