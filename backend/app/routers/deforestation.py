"""
Router de Desmatamento
Endpoints para as 3 ações principais do Observa Floresta
"""
from fastapi import APIRouter, HTTPException, Depends, Query, status
from typing import Optional
import logging
from datetime import datetime

from app.services.deforestation_service import (
    DeforestationService,
    get_deforestation_service
)
from app.models.requests import (
    StateDeforestationRequest,
    ComparisonRequest,
    RankingRequest
)
from app.models.responses import (
    StateDeforestationResponse,
    ComparisonResponse,
    RankingResponse,
    StatesListResponse,
    YearsListResponse,
    ErrorResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()


# ==========================================
# Ação 1: Consultar Desmatamento por Estado
# ==========================================

@router.post(
    "/deforestation/state",
    response_model=StateDeforestationResponse,
    summary="Consultar desmatamento por estado",
    description="Retorna dados de desmatamento de um estado específico em um ano",
    tags=["Ações Principais"]
)
async def get_state_deforestation_post(
    request: StateDeforestationRequest,
    service: DeforestationService = Depends(get_deforestation_service)
):
    """Ação 1: Consultar Desmatamento por Estado"""
    try:
        logger.info(f"POST /deforestation/state: {request.state}, {request.year}")
        result = await service.get_state_deforestation(
            state=request.state,
            year=request.year
        )
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in get_state_deforestation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar dados de desmatamento"
        )


@router.get(
    "/deforestation/state/{state}",
    response_model=StateDeforestationResponse,
    summary="Consultar desmatamento por estado (GET)",
    description="Versão GET do endpoint de consulta por estado",
    tags=["Ações Principais"]
)
async def get_state_deforestation_get(
    state: str,
    year: Optional[int] = Query(None, ge=2020, le=2024),
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    Ação 1: Consultar Desmatamento por Estado (GET)
    
    Aceita:
    - Siglas: PA, AM, RS, etc
    - Nomes completos: Pará, Amazonas, etc
    - Nomes sem acento: Para, Amazonas, etc
    """
    try:
        logger.info(f"GET /deforestation/state/{state}?year={year}")
        result = await service.get_state_deforestation(
            state=state,
            year=year
        )
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in get_state_deforestation_get: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar dados de desmatamento"
        )


# ==========================================
# Ação 2: Comparar Desmatamento Temporal
# ==========================================

@router.post(
    "/deforestation/compare",
    response_model=ComparisonResponse,
    summary="Comparar desmatamento entre períodos",
    description="Compara desmatamento de um estado, bioma ou Brasil entre dois anos",
    tags=["Ações Principais"]
)
async def compare_deforestation_post(
    request: ComparisonRequest,
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    Ação 2: Comparar Desmatamento Temporal
    
    Agora suporta:
    - Estados específicos (ex: "Pará")
    - Biomas (ex: "Cerrado", "Amazônia")
    - Brasil inteiro (use "Brasil")
    """
    try:
        logger.info(
            f"POST /deforestation/compare: {request.state_or_biome}, "
            f"{request.year_start}-{request.year_end}"
        )
        result = await service.compare_deforestation(
            state_or_biome=request.state_or_biome,
            year_start=request.year_start,
            year_end=request.year_end
        )
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in compare_deforestation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao comparar dados de desmatamento"
        )


@router.get(
    "/deforestation/compare/{state_or_biome}",
    response_model=ComparisonResponse,
    summary="Comparar desmatamento entre períodos (GET)",
    description="Versão GET - suporta estado, bioma ou Brasil",
    tags=["Ações Principais"]
)
async def compare_deforestation_get(
    state_or_biome: str,
    year_start: int = Query(..., ge=2020, le=2024, description="Ano inicial"),
    year_end: int = Query(..., ge=2020, le=2024, description="Ano final"),
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    Ação 2: Comparar Desmatamento Temporal (GET)
    
    ⚠️ IMPORTANTE: NÃO inclua texto extra no path parameter!
    
    ✅ CORRETO:
    - GET /api/deforestation/compare/Amazonas?year_start=2020&year_end=2024
    - GET /api/deforestation/compare/PA?year_start=2020&year_end=2024
    - GET /api/deforestation/compare/Cerrado?year_start=2020&year_end=2024
    - GET /api/deforestation/compare/Brasil?year_start=2020&year_end=2024
    
    ❌ ERRADO:
    - GET /api/deforestation/compare/Amazonas entre?year_start=2020
    
    Aceita:
    - Estados: Siglas (PA, AM) ou nomes completos/sem acento
    - Biomas: Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa, Pantanal
    - Brasil: "Brasil" ou "Brazil"
    """
    try:
        # Validação básica
        if year_end <= year_start:
            raise ValueError("year_end deve ser maior que year_start")
        
        logger.info(
            f"GET /deforestation/compare/{state_or_biome} "
            f"?year_start={year_start}&year_end={year_end}"
        )
        
        result = await service.compare_deforestation(
            state_or_biome=state_or_biome,
            year_start=year_start,
            year_end=year_end
        )
        return result
        
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in compare_deforestation_get: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao comparar dados de desmatamento"
        )


# ==========================================
# Ação 3: Ranking de Estados
# ==========================================

@router.post(
    "/deforestation/ranking",
    response_model=RankingResponse,
    summary="Ranking de estados por desmatamento",
    description="Lista estados ordenados por área desmatada (com filtro de bioma opcional)",
    tags=["Ações Principais"]
)
async def get_states_ranking_post(
    request: RankingRequest,
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    Ação 3: Ranking de Estados
    
    Agora com filtro opcional de bioma:
    - biome: null (todos os estados)
    - biome: "Amazônia" (apenas estados da Amazônia)
    """
    try:
        logger.info(
            f"POST /deforestation/ranking: year={request.year}, "
            f"order={request.order}, limit={request.limit}, biome={request.biome}"
        )
        result = await service.get_states_ranking(
            year=request.year,
            order=request.order,
            limit=request.limit,
            biome=request.biome
        )
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in get_states_ranking: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar ranking de desmatamento"
        )


@router.get(
    "/deforestation/ranking/{year}",
    response_model=RankingResponse,
    summary="Ranking de estados por desmatamento (GET)",
    description="Versão GET com filtro opcional de bioma",
    tags=["Ações Principais"]
)
async def get_states_ranking_get(
    year: int,
    order: str = Query("desc", regex="^(desc|asc)$", description="Ordem: desc ou asc"),
    limit: int = Query(10, ge=1, le=30, description="Limite de resultados"),
    biome: Optional[str] = Query(None, description="Filtrar por bioma"),
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    Ação 3: Ranking de Estados (GET)
    
    **Exemplos:**
    - GET /api/deforestation/ranking/2024 (todos os estados)
    - GET /api/deforestation/ranking/2024?biome=Cerrado (apenas Cerrado)
    - GET /api/deforestation/ranking/2024?biome=Amazônia&order=desc&limit=5 (top 5 da Amazônia)
    - GET /api/deforestation/ranking/2024?order=asc&limit=5 (5 estados com MENOR desmatamento)
    """
    try:
        logger.info(
            f"GET /deforestation/ranking/{year}"
            f"?order={order}&limit={limit}&biome={biome}"
        )
        result = await service.get_states_ranking(
            year=year,
            order=order,
            limit=limit,
            biome=biome
        )
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in get_states_ranking_get: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar ranking de desmatamento"
        )


# ==========================================
# Endpoints Auxiliares
# ==========================================

@router.get(
    "/deforestation/states",
    summary="Listar estados disponíveis",
    description="Retorna lista de estados (com filtro opcional de bioma)",
    tags=["Auxiliares"]
)
async def get_available_states(
    biome: Optional[str] = Query(None, description="Filtrar por bioma (ex: Amazônia, Cerrado)"),
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    **Lista de Estados Disponíveis**
    
    Retorna todos os estados brasileiros, opcionalmente filtrados por bioma.
    
    **Exemplos:**
    - GET /api/deforestation/states (todos os 27 estados)
    - GET /api/deforestation/states?biome=Amazônia (apenas estados da Amazônia)
    - GET /api/deforestation/states?biome=Cerrado (apenas estados do Cerrado)
    """
    try:
        logger.info(f"GET /deforestation/states?biome={biome}")
        result = await service.get_available_states(biome)
        return result
    except Exception as e:
        logger.error(f"Error in get_available_states: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar lista de estados"
        )


@router.get(
    "/deforestation/years",
    response_model=YearsListResponse,
    summary="Listar anos disponíveis",
    description="Retorna lista de anos com dados disponíveis",
    tags=["Auxiliares"]
)
async def get_available_years(
    service: DeforestationService = Depends(get_deforestation_service)
):
    """**Lista de Anos Disponíveis**"""
    try:
        logger.info("GET /deforestation/years")
        result = await service.get_available_years()
        return result
    except Exception as e:
        logger.error(f"Error in get_available_years: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar lista de anos"
        )


@router.get(
    "/deforestation/biomes",
    summary="Listar biomas disponíveis",
    description="Retorna lista de todos os biomas brasileiros",
    tags=["Auxiliares"]
)
async def get_available_biomes(
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    **Lista de Biomas Disponíveis**
    
    Retorna os 6 biomas brasileiros:
    - Amazônia
    - Cerrado
    - Mata Atlântica
    - Caatinga
    - Pampa
    - Pantanal
    """
    try:
        logger.info("GET /deforestation/biomes")
        result = await service.get_available_biomes()
        return result
    except Exception as e:
        logger.error(f"Error in get_available_biomes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao buscar lista de biomas"
        )


# ==========================================
# NOVO: Comparação de Biomas
# ==========================================

@router.get(
    "/deforestation/biomes/compare/{year}",
    summary="Comparar todos os biomas",
    description="Compara degradação entre todos os biomas brasileiros em um ano",
    tags=["Ações Principais"]
)
async def compare_biomes(
    year: int,
    service: DeforestationService = Depends(get_deforestation_service)
):
    """
    **Comparação de Biomas**
    
    Retorna dados comparativos de todos os 6 biomas brasileiros em um ano específico.
    Útil para visualizar qual bioma teve maior degradação.
    
    **Exemplo:**
    ```
    GET /api/deforestation/biomes/compare/2024
    ```
    
    **Retorna:**
    - Área degradada de cada bioma (km²)
    - Percentual do total nacional
    - Número de estados em cada bioma
    """
    try:
        logger.info(f"GET /deforestation/biomes/compare/{year}")
        result = await service.get_biome_comparison(year)
        return result
    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error in compare_biomes: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao comparar biomas"
        )


# ==========================================
# Endpoint de Teste Rápido
# ==========================================

@router.get(
    "/deforestation",
    summary="Endpoint de teste",
    description="Retorna informações sobre os endpoints disponíveis",
    tags=["Auxiliares"]
)
async def deforestation_info():
    """**Informações sobre os Endpoints**"""
    return {
        "message": "🌳 Observa Floresta - API de Desmatamento (TODOS OS BIOMAS)",
        "version": "2.0.1",
        "coverage": {
            "states": 27,
            "biomes": 6,
            "years": "2020-2024"
        },
        "actions": [
            {
                "name": "Ação 1: Consultar por Estado",
                "endpoints": [
                    "POST /api/deforestation/state",
                    "GET /api/deforestation/state/{state}"
                ],
                "description": "Dados de desmatamento de um estado específico",
                "examples": [
                    "GET /api/deforestation/state/PA?year=2024",
                    "GET /api/deforestation/state/Pará?year=2024",
                    "GET /api/deforestation/state/Para?year=2024"
                ]
            },
            {
                "name": "Ação 2: Comparação Temporal",
                "endpoints": [
                    "POST /api/deforestation/compare",
                    "GET /api/deforestation/compare/{state_or_biome}"
                ],
                "description": "Compara desmatamento entre períodos (estado, bioma ou Brasil)",
                "examples": [
                    "GET /api/deforestation/compare/Pará?year_start=2020&year_end=2024",
                    "GET /api/deforestation/compare/Cerrado?year_start=2020&year_end=2024",
                    "GET /api/deforestation/compare/Brasil?year_start=2020&year_end=2024"
                ]
            },
            {
                "name": "Ação 3: Ranking de Estados",
                "endpoints": [
                    "POST /api/deforestation/ranking",
                    "GET /api/deforestation/ranking/{year}"
                ],
                "description": "Lista estados ordenados por desmatamento (com filtro de bioma)",
                "examples": [
                    "GET /api/deforestation/ranking/2024",
                    "GET /api/deforestation/ranking/2024?biome=Amazônia&limit=5",
                    "GET /api/deforestation/ranking/2024?order=asc&limit=5"
                ]
            },
            {
                "name": "NOVO: Comparação de Biomas",
                "endpoints": [
                    "GET /api/deforestation/biomes/compare/{year}"
                ],
                "description": "Compara todos os 6 biomas brasileiros",
                "examples": [
                    "GET /api/deforestation/biomes/compare/2024"
                ]
            }
        ],
        "auxiliary": [
            {
                "name": "Estados Disponíveis",
                "endpoint": "GET /api/deforestation/states?biome={biome}",
                "description": "Lista estados (com filtro opcional de bioma)"
            },
            {
                "name": "Biomas Disponíveis",
                "endpoint": "GET /api/deforestation/biomes",
                "description": "Lista os 6 biomas brasileiros"
            },
            {
                "name": "Anos Disponíveis",
                "endpoint": "GET /api/deforestation/years",
                "description": "Lista anos com dados disponíveis"
            }
        ],
        "biomes": [
            "Amazônia",
            "Cerrado",
            "Mata Atlântica",
            "Caatinga",
            "Pampa",
            "Pantanal"
        ],
        "tips": {
            "estados": "Use siglas (PA, AM) ou nomes completos/sem acento",
            "urls": "NÃO inclua texto extra no path: use /compare/Amazonas (não /compare/Amazonas entre)",
            "biomas": "Use nomes corretos: Amazônia, Cerrado, etc",
            "brasil": "Para dados nacionais, use: /compare/Brasil"
        },
        "docs": "/docs"
    }