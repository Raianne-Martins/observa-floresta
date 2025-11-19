"""
Direct Service - VERSÃO CORRIGIDA
Aceita tanto texto natural quanto inputs simples (estado + ano)
"""
from typing import Dict, Optional
import logging
from datetime import datetime
from fastapi import HTTPException, status

from app.services.smart_service import SmartDataServiceOptimized as SmartDataService
from app.services import mock_data_brazil

logger = logging.getLogger(__name__)


class DirectService:
    """
    Serviço que usa SmartDataService
    (com fallback automático para mock)
    """
    
    def __init__(self):
        logger.info("="*60)
        logger.info("🔧 DirectService inicializando...")
        logger.info("="*60)
        
        self.smart_service = SmartDataService()
        self.use_mock = not self.smart_service.use_real_api
        
        if self.use_mock:
            logger.warning("⚠️  MODO MOCK ATIVADO - Dados reais não serão buscados")
        else:
            logger.info("✅ MODO API REAL - Buscando dados do INPE")
    
    async def get_state_deforestation(
        self,
        state: str,
        year: Optional[int] = None
    ) -> Dict:
        """
        Ação 1: Consultar desmatamento por estado
        
        Aceita:
        - Input simples: state="PA", year=2024
        - Input simples: state="Pará", year=2024
        - Texto natural: state="desmatamento no Pará em 2024"
        """
        # Se ano não fornecido, usar ano atual
        if year is None:
            year = datetime.now().year
        
        logger.info(f"🌳 DirectService.get_state_deforestation: {state}, {year}")
        
        try:
            result = await self.smart_service.get_state_data(state, year)
            
            if result and 'data_source' in result:
                source = result['data_source']
                if source == 'real_api':
                    logger.info(f"   ✅ Dados REAIS obtidos da API para {state}/{year}")
                elif source == 'mock':
                    logger.warning(f"   📦 Fallback para MOCK (API falhou ou indisponível)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar dados: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar dados de desmatamento: {str(e)}"
            )
    
    async def compare_deforestation(
        self,
        state_or_biome: str,
        year_start: int,
        year_end: int
    ) -> Dict:
        """
        Ação 2: Comparar desmatamento entre períodos
        
        Aceita:
        - state_or_biome="PA", year_start=2020, year_end=2024
        - state_or_biome="Pará", year_start=2020, year_end=2024
        - state_or_biome="Amazônia", year_start=2020, year_end=2024
        """
        logger.info(f"📊 DirectService.compare_deforestation: {state_or_biome}, {year_start}-{year_end}")
        
        # Validação básica
        if year_end <= year_start:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="year_end deve ser maior que year_start"
            )
        
        try:
            result = await self.smart_service.compare_data(
                state_or_biome, year_start, year_end
            )
            
            if result and 'data_source' in result:
                source = result['data_source']
                if source == 'real_api':
                    logger.info(f"   ✅ Comparação REAL obtida da API para {state_or_biome}")
                elif source == 'mock':
                    logger.warning(f"   📦 Fallback para MOCK (API falhou ou indisponível)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao comparar dados: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao comparar dados: {str(e)}"
            )
    
    async def get_states_ranking(
        self,
        year: int,
        order: str = "desc",
        limit: int = 10,
        biome: Optional[str] = None
    ) -> Dict:
        """Ação 3: Ranking de estados"""
        logger.info(f"🏆 DirectService.get_states_ranking: {year}, {order}, {limit}, {biome}")
        
        try:
            result = await self.smart_service.get_ranking(year, order, limit, biome)
            
            if result and 'data_source' in result:
                source = result['data_source']
                if source == 'real_api':
                    logger.info(f"   ✅ Ranking REAL obtido da API para {year}")
                elif source == 'mock':
                    logger.warning(f"   📦 Fallback para MOCK (API falhou ou indisponível)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro ao buscar ranking: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar ranking: {str(e)}"
            )
    
    async def get_biome_comparison(self, year: int) -> Dict:
        """Comparar todos os biomas"""
        logger.info(f"🌿 DirectService.get_biome_comparison: {year}")
        
        try:
            result = await self.smart_service.get_biome_comparison(year)
            return result
            
        except Exception as e:
            logger.error(f"❌ Erro em get_biome_comparison: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao comparar biomas: {str(e)}"
            )
    
    async def get_available_states(self, biome: Optional[str] = None) -> Dict:
        """Lista estados disponíveis"""
        return await self.smart_service.get_available_states(biome)
    
    async def get_available_years(self) -> Dict:
        """Lista anos disponíveis"""
        return await self.smart_service.get_available_years()
    
    async def get_available_biomes(self) -> Dict:
        """Lista biomas disponíveis"""
        result = await self.smart_service.get_available_biomes()
        # Converter list para dict com timestamp
        return {
            "biomes": result,
            "total": len(result),
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def close(self):
        """Limpa recursos"""
        logger.info("🔌 DirectService.close() - limpando recursos...")
        await self.smart_service.close()
        logger.info("✅ Recursos limpos")