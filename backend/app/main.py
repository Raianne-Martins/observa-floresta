"""
Observa Floresta - Backend API
Sistema de monitoramento de desmatamento na Amazônia
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.routers import deforestation, health

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Observa Floresta API",
    description="API para monitoramento de desmatamento",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(deforestation.router, prefix="/api", tags=["Desmatamento"])


@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar a aplicação"""
    logger.info("🌳 Observa Floresta API iniciando...")
    logger.info(f"Modo: {'Azure Agent' if settings.USE_AZURE_AGENT else 'Direct Logic'}")
    logger.info(f"Mock Data: {settings.MOCK_DATA}")
    logger.info(f"Ambiente: {settings.ENVIRONMENT}")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado ao desligar a aplicação"""
    logger.info("🌳 Observa Floresta API encerrando...")


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "🌳 Observa Floresta API",
        "version": "1.0.0",
        "docs": "/docs",
        "mode": "Azure Agent" if settings.USE_AZURE_AGENT else "Direct Logic",
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )
