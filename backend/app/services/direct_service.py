"""
Direct Service - Lógica de desmatamento SEM usar Azure Agent
Modo padrão para desenvolvimento e economia de custos
"""
from typing import Dict, Optional
import logging
from datetime import datetime

from app.config import settings
from app.services import mock_data

logger = logging.getLogger(__name__)


class DirectService:
    """
    Serviço que implementa as 3 ações diretamente
    SEM dependência do Azure Agent
    """
    
    def __init__(self):
        self.use_mock = settings.MOCK_DATA
        logger.info(f"DirectService inicializado (mock_data={self.use_mock})")
    
    async def get_state_deforestation(
        self,
        state: str,
        year: Optional[int] = None
    ) -> Dict:
        """
        Ação 1: Consultar desmatamento por estado
        
        Args:
            state: Nome ou sigla do estado
            year: Ano (se None, usa ano atual)
        
        Returns:
            Dados de desmatamento do estado
        """
        logger.info(f"DirectService.get_state_deforestation: state={state}, year={year}")
        
        # Usar ano atual se não especificado
        if year is None:
            year = datetime.now().year
        
        try:
            if self.use_mock:
                # Usar dados mockados
                data = mock_data.get_state_data(state, year)
                logger.info(f"Dados retornados (mock): {state} - {year}")
                return data
            else:
                # TODO: Integrar com API real do INPE
                # data = await self.inpe_service.fetch_state_data(state, year)
                raise NotImplementedError("Integração com API real ainda não implementada")
        
        except ValueError as e:
            logger.error(f"Erro de validação: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar dados: {e}")
            raise
    
    async def compare_deforestation(
        self,
        state: str,
        year_start: int,
        year_end: int
    ) -> Dict:
        """
        Ação 2: Comparar desmatamento entre períodos
        
        Args:
            state: Nome do estado ou "Brasil" para agregado
            year_start: Ano inicial
            year_end: Ano final
        
        Returns:
            Dados de comparação temporal
        """
        logger.info(
            f"DirectService.compare_deforestation: "
            f"state={state}, years={year_start}-{year_end}"
        )
        
        try:
            if self.use_mock:
                data = mock_data.get_comparison_data(state, year_start, year_end)
                logger.info(f"Comparação retornada (mock): {state} {year_start}-{year_end}")
                return data
            else:
                # TODO: Integrar com API real
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
        limit: int = 10
    ) -> Dict:
        """
        Ação 3: Ranking de estados por desmatamento
        
        Args:
            year: Ano da consulta
            order: Ordem ("desc" ou "asc")
            limit: Número de estados
        
        Returns:
            Ranking de estados
        """
        logger.info(
            f"DirectService.get_states_ranking: "
            f"year={year}, order={order}, limit={limit}"
        )
        
        try:
            if self.use_mock:
                data = mock_data.get_ranking_data(year, order, limit)
                logger.info(f"Ranking retornado (mock): {year} top {limit}")
                return data
            else:
                # TODO: Integrar com API real
                raise NotImplementedError("Integração com API real ainda não implementada")
        
        except ValueError as e:
            logger.error(f"Erro de validação: {e}")
            raise
        except Exception as e:
            logger.error(f"Erro ao buscar ranking: {e}")
            raise
    
    async def get_available_states(self) -> Dict:
        """
        Retorna lista de estados disponíveis
        
        Returns:
            Lista de estados
        """
        logger.info("DirectService.get_available_states")
        
        try:
            states = mock_data.get_available_states()
            return {
                "states": states,
                "total": len(states),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao buscar estados: {e}")
            raise
    
    async def get_available_years(self) -> Dict:
        """
        Retorna lista de anos disponíveis
        
        Returns:
            Lista de anos
        """
        logger.info("DirectService.get_available_years")
        
        try:
            years = mock_data.get_available_years()
            return {
                "years": years,
                "total": len(years),
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Erro ao buscar anos: {e}")
            raise