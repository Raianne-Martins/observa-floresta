"""
Observa Floresta - Backend API
Sistema de monitoramento de desmatamento na Amazônia
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys

from app.config import settings
from app.routers import deforestation, health

# ==========================================
# CONFIGURAÇÃO DE LOGGING MELHORADA
# ==========================================

# Configurar formato de log
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=log_format,
    handlers=[
        logging.StreamHandler(sys.stdout)  # Força saída no terminal
    ]
)

# Logger específico da aplicação
logger = logging.getLogger(__name__)

#debugging
logging.basicConfig(level=logging.DEBUG)

# Garantir que logs dos nossos módulos apareçam
logging.getLogger("app").setLevel(logging.INFO)
logging.getLogger("app.services").setLevel(logging.INFO)
logging.getLogger("app.agent").setLevel(logging.INFO)

# Criar aplicação FastAPI
app = FastAPI(
    title="Observa Floresta API",
    description="API para monitoramento de desmatamento na Amazônia Legal",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(deforestation.router, prefix="/api", tags=["Desmatamento"])


@app.on_event("startup")
async def startup_event():
    """Evento executado ao iniciar a aplicação"""
    print("\n" + "="*60)
    print("🌳 OBSERVA FLORESTA API INICIANDO...")
    print("="*60)
    
    logger.info(f"Modo Agent: {'Azure OpenAI' if settings.USE_AZURE_AGENT else 'Direct Logic'}")
    logger.info(f"Dados: {'Mock Data' if settings.MOCK_DATA else 'Real API com Fallback'}")
    logger.info(f"Ambiente: {settings.ENVIRONMENT}")
    
    print("="*60 + "\n")


@app.on_event("shutdown")
async def shutdown_event():
    """Evento executado ao desligar a aplicação"""
    logger.info("🌳 Observa Floresta API encerrando...")


@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "🌳 Observa Floresta API",
        "version": "2.0.0",
        "docs": "/docs",
        "mode": "Azure Agent" if settings.USE_AZURE_AGENT else "Direct Logic",
        "data_mode": "Mock Data" if settings.MOCK_DATA else "Real API + Fallback",
        "status": "online"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level="info"
    )