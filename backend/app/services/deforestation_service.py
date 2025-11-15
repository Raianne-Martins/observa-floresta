"""
Deforestation Service - Orchestrator
Decide qual engine usar (Azure Agent ou Direct)
"""
from typing import Dict, Optional
import logging

from app.config import settings
from app.services.direct_service import DirectService
# from app.agent.azure_agent import AzureAgent  # Importar quando criar

logger = logging.getLogger(__name__)


class DeforestationService:
    """
    Orquestrador que decide qual engine usar
    Transparente para quem chama
    """
    
    def __init__(self):
        if settings.USE_AZURE_AGENT:
            logger.info("Usando Azure Agent Mode")
            # TODO: Implementar quando criar o Azure Agent
            # self.engine = AzureAgent()
            raise NotImplementedError(
                "Azure Agent Mode ainda não implementado. "
                "Use USE_AZURE_AGENT=false no .env"
            )
        else:
            logger.info("Usando Direct Mode")
            self.engine = DirectService()
    
    async def get_state_deforestation(
        self,
        state: str,
        year: Optional[int] = None
    ) -> Dict:
        """Ação 1: Dados por estado"""
        return await self.engine.get_state_deforestation(state, year)
    
    async def compare_deforestation(
        self,
        state: str,
        year_start: int,
        year_end: int
    ) -> Dict:
        """Ação 2: Comparação temporal"""
        return await self.engine.compare_deforestation(state, year_start, year_end)
    
    async def get_states_ranking(
        self,
        year: int,
        order: str = "desc",
        limit: int = 10
    ) -> Dict:
        """Ação 3: Ranking de estados"""
        return await self.engine.get_states_ranking(year, order, limit)
    
    async def get_available_states(self) -> Dict:
        """Lista de estados disponíveis"""
        return await self.engine.get_available_states()
    
    async def get_available_years(self) -> Dict:
        """Lista de anos disponíveis"""
        return await self.engine.get_available_years()


# Singleton instance
_service_instance: Optional[DeforestationService] = None


def get_deforestation_service() -> DeforestationService:
    """
    Dependency Injection para FastAPI
    
    Returns:
        Instância do DeforestationService
    """
    global _service_instance
    if _service_instance is None:
        _service_instance = DeforestationService()
    return _service_instance
