"""
Router de health check e status
"""
from fastapi import APIRouter
from datetime import datetime
from app.config import settings

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    
    Returns:
        Status da aplicação e configurações
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "mode": "azure_agent" if settings.USE_AZURE_AGENT else "direct_logic",
        "mock_data": settings.MOCK_DATA,
        "version": "1.0.0"
    }


@router.get("/config")
async def get_config():
    """
    Retorna configurações públicas (não sensíveis)
    
    Returns:
        Configurações da aplicação
    """
    return {
        "environment": settings.ENVIRONMENT,
        "use_azure_agent": settings.USE_AZURE_AGENT,
        "mock_data": settings.MOCK_DATA,
        "cache_enabled": settings.ENABLE_CACHE,
        "cache_ttl": settings.CACHE_TTL,
        "cors_origins": settings.cors_origins_list
    }