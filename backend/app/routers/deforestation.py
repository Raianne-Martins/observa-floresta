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
    """Ação 1: Consultar Desmatamento por Estado (GET)"""
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
    description="Compara desmatamento de um estado entre dois anos",
    tags=["Ações Principais"]
)
async def compare_deforestation_post(
    request: ComparisonRequest,
    service: DeforestationService = Depends(get_deforestation_service)
):
    """Ação 2: Comparar Desmatamento Temporal"""
    try:
        logger.info(
            f"POST /deforestation/compare: {request.state}, "
            f"{request.year_start}-{request.year_end}"
        )
        result = await service.compare_deforestation(
            state=request.state,
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
    "/deforestation/compare/{state}",
    response_model=ComparisonResponse,
    summary="Comparar desmatamento entre períodos (GET)",
    description="Versão GET do endpoint de comparação temporal",
    tags=["Ações Principais"]
)
async def compare_deforestation_get(
    state: str,
    year_start: int = Query(..., ge=2020, le=2024),
    year_end: int = Query(..., ge=2020, le=2024),
    service: DeforestationService = Depends(get_deforestation_service)
):
    """Ação 2: Comparar Desmatamento Temporal (GET)"""
    try:
        if year_end <= year_start:
            raise ValueError("year_end deve ser maior que year_start")
        
        logger.info(
            f"GET /deforestation/compare/{state}"
            f"?year_start={year_start}&year_end={year_end}"
        )
        result = await service.compare_deforestation(
            state=state,
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
        logger.error(f"Error in compare_deforestation_get: {e}")
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
    description="Lista estados ordenados por área desmatada",
    tags=["Ações Principais"]
)
async def get_states_ranking_post(
    request: RankingRequest,
    service: DeforestationService = Depends(get_deforestation_service)
):
    """Ação 3: Ranking de Estados"""
    try:
        logger.info(
            f"POST /deforestation/ranking: year={request.year}, "
            f"order={request.order}, limit={request.limit}"
        )
        result = await service.get_states_ranking(
            year=request.year,
            order=request.order,
            limit=request.limit
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
    description="Versão GET do endpoint de ranking",
    tags=["Ações Principais"]
)
async def get_states_ranking_get(
    year: int,
    order: str = Query("desc", regex="^(desc|asc)$"),
    limit: int = Query(10, ge=1, le=20),
    service: DeforestationService = Depends(get_deforestation_service)
):
    """Ação 3: Ranking de Estados (GET)"""
    try:
        logger.info(
            f"GET /deforestation/ranking/{year}"
            f"?order={order}&limit={limit}"
        )
        result = await service.get_states_ranking(
            year=year,
            order=order,
            limit=limit
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
    response_model=StatesListResponse,
    summary="Listar estados disponíveis",
    description="Retorna lista de estados da Amazônia Legal",
    tags=["Auxiliares"]
)
async def get_available_states(
    service: DeforestationService = Depends(get_deforestation_service)
):
    """Lista de Estados Disponíveis"""
    try:
        logger.info("GET /deforestation/states")
        result = await service.get_available_states()
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
    """Lista de Anos Disponíveis"""
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
    """Informações sobre os Endpoints"""
    return {
        "message": "🌳 Observa Floresta - API de Desmatamento",
        "version": "1.0.0",
        "actions": [
            {
                "name": "Ação 1: Consultar por Estado",
                "endpoints": [
                    "POST /api/deforestation/state",
                    "GET /api/deforestation/state/{state}"
                ],
                "description": "Dados de desmatamento de um estado específico"
            },
            {
                "name": "Ação 2: Comparação Temporal",
                "endpoints": [
                    "POST /api/deforestation/compare",
                    "GET /api/deforestation/compare/{state}"
                ],
                "description": "Compara desmatamento entre períodos"
            },
            {
                "name": "Ação 3: Ranking de Estados",
                "endpoints": [
                    "POST /api/deforestation/ranking",
                    "GET /api/deforestation/ranking/{year}"
                ],
                "description": "Lista estados ordenados por desmatamento"
            }
        ],
        "auxiliary": [
            {
                "name": "Estados Disponíveis",
                "endpoint": "GET /api/deforestation/states",
                "description": "Lista estados da Amazônia Legal"
            },
            {
                "name": "Anos Disponíveis",
                "endpoint": "GET /api/deforestation/years",
                "description": "Lista anos com dados disponíveis"
            }
        ],
        "docs": "/docs"
    }
