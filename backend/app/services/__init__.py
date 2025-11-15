"""
Services do Observa Floresta
"""
from app.services.deforestation_service import (
    DeforestationService,
    get_deforestation_service
)
from app.services.direct_service import DirectService

__all__ = [
    "DeforestationService",
    "get_deforestation_service",
    "DirectService"
]
