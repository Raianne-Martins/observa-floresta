"""
Routers do Observa Floresta
"""
from app.routers import health
from app.routers import deforestation

__all__ = [
    "health",
    "deforestation"
]

# Importar outros routers conforme forem criados
# from app.routers import deforestation
