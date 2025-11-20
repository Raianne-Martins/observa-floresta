"""
Direct Service - Lógica de desmatamento SEM usar Azure Agent
"""
from typing import Dict, Optional
import logging
from datetime import datetime

from app.config import settings

logger = logging.getLogger(__name__)


class DirectService:
    """
    Serviço que implementa as ações diretamente
    SEM dependência do Azure Agent
    """
    
    def __init__(self):
        self.use_mock = settings.MOCK_DATA
        logger.info(f"DirectService inicializado (mock_data={self.use_mock})")
        
        if self.use_mock:
            from app.services import mock_data_brazil as mock_data
            self.mock_data = mock_data
    
    async def get_state_deforestation(
        self,
        state: str,
        year: Optional[int] = None
    ) -> Dict:
        """Ação 1: Consultar desmatamento por estado"""
        logger.info(f"DirectService.get_state_deforestation: state={state}, year={year}")
        
        if year is None:
            year = datetime.now().year
        
        try:
            if self.use_mock:
                data = self.mock_data.get_state_data(state, year)
                logger.info(f"Dados retornados (mock): {state} - {year}")
                return data
            else:
                raise NotImplementedError("Integração com API real ainda não implementada")
        
        except ValueError as e:
            logger.error(f"Erro de validação: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar dados: {e}")
            raise
    
    async def compare_deforestation(
        self,
        state_or_biome: str,
        year_start: int,
        year_end: int
    ) -> Dict:
        """Ação 2: Comparar desmatamento entre períodos (estado ou bioma)"""
        logger.info(
            f"DirectService.compare_deforestation: "
            f"entity={state_or_biome}, years={year_start}-{year_end}"
        )
        
        try:
            if self.use_mock:
                data = self.mock_data.get_comparison_data(state_or_biome, year_start, year_end)
                logger.info(f"Comparação retornada (mock): {state_or_biome} {year_start}-{year_end}")
                return data
            else:
                raise NotImplementedError("Integração com API real ainda não implementada")
        
        except ValueError as e:
            logger.error(f"Erro de validação: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao comparar dados: {e}")
            raise
    
    async def get_states_ranking(
        self,
        year: int,
        order: str = "desc",
        limit: int = 10,
        biome: Optional[str] = None
    ) -> Dict:
        """Ação 3: Ranking de estados por desmatamento (com filtro de bioma)"""
        logger.info(
            f"DirectService.get_states_ranking: "
            f"year={year}, order={order}, limit={limit}, biome={biome}"
        )
        
        try:
            if self.use_mock:
                data = self.mock_data.get_ranking_data(year, order, limit, biome)
                logger.info(f"Ranking retornado (mock): {year} top {limit}")
                return data
            else:
                raise NotImplementedError("Integração com API real ainda não implementada")
        
        except ValueError as e:
            logger.error(f"Erro de validação: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar ranking: {e}")
            raise
    
    async def get_biome_comparison(self, year: int) -> Dict:
        """NOVA: Comparar todos os biomas"""
        logger.info(f"DirectService.get_biome_comparison: year={year}")
        
        try:
            if self.use_mock:
                data = self.mock_data.get_biome_comparison(year)
                logger.info(f"Comparação de biomas retornada: {year}")
                return data
            else:
                raise NotImplementedError("Integração com API real ainda não implementada")
        
        except ValueError as e:
            logger.error(f"Erro de validação: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao comparar biomas: {e}")
            raise
    
    async def get_available_states(self, biome: Optional[str] = None) -> Dict:
        """Retorna lista de estados disponíveis (com filtro de bioma)"""
        logger.info(f"DirectService.get_available_states: biome={biome}")
        
        try:
            states = self.mock_data.get_available_states(biome)
            return states
        except Exception as e:
            logger.error(f"Erro ao buscar estados: {e}")
            raise
    
    async def get_available_years(self) -> Dict:
        """Retorna lista de anos disponíveis"""
        logger.info("DirectService.get_available_years")
        
        try:
            years = self.mock_data.get_available_years()
            return years
        except Exception as e:
            logger.error(f"Erro ao buscar anos: {e}")
            raise
    
    async def get_available_biomes(self) -> Dict:
        """NOVA: Retorna lista de biomas disponíveis"""
        logger.info("DirectService.get_available_biomes")
        
        try:
            biomes = self.mock_data.get_available_biomes()
            return {
                "biomes": biomes,
                "total": len(biomes),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao buscar biomas: {e}")
            raise