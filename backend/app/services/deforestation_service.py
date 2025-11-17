"""
Deforestation Service - Orchestrator
Decide qual engine usar (Azure Agent ou Direct)
"""
from typing import Dict, Optional
import logging

from app.config import settings
from app.services.direct_service import DirectService

logger = logging.getLogger(__name__)


class DeforestationService:
    """Orquestrador que decide qual engine usar"""
    
    def __init__(self):
        if settings.USE_AZURE_AGENT:
            logger.info("🔵 Usando Azure Agent Mode")
            from app.agent.azure_agent import AzureAgent
            self.engine = AzureAgent()
        else:
            logger.info("🟢 Usando Direct Mode")
            self.engine = DirectService()
    
    async def get_state_deforestation(self, state: str, year: Optional[int] = None) -> Dict:
        return await self.engine.get_state_deforestation(state, year)
    
    async def compare_deforestation(self, state_or_biome: str, year_start: int, year_end: int) -> Dict:
        return await self.engine.compare_deforestation(state_or_biome, year_start, year_end)
    
    async def get_states_ranking(self, year: int, order: str = "desc", limit: int = 10, biome: Optional[str] = None) -> Dict:
        return await self.engine.get_states_ranking(year, order, limit, biome)
    
    async def get_biome_comparison(self, year: int) -> Dict:
        return await self.engine.get_biome_comparison(year)
    
    async def get_available_states(self, biome: Optional[str] = None) -> Dict:
        return await self.engine.get_available_states(biome)
    
    async def get_available_years(self) -> Dict:
        return await self.engine.get_available_years()
    
    async def get_available_biomes(self) -> Dict:
        return await self.engine.get_available_biomes()


_service_instance: Optional[DeforestationService] = None


def get_deforestation_service() -> DeforestationService:
    global _service_instance
    if _service_instance is None:
        _service_instance = DeforestationService()
    return _service_instance
