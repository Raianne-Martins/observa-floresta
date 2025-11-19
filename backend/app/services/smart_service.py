"""
Smart Data Service - VERSÃO OTIMIZADA
Multi-estratégia com fallback inteligente
"""
import logging
from typing import Dict, Optional, List
from datetime import datetime

from app.config import settings
from app.services.inpe_client import INPEClientOptimized
from app.services import mock_data_brazil

logger = logging.getLogger(__name__)

class SmartDataServiceOptimized:
    """
    Serviço inteligente com múltiplas estratégias de fallback:
    1. API Real (multi-estratégia)
    2. Mock data (se API falhar completamente)
    """
    
    def __init__(self):
        self.use_real_api = not settings.MOCK_DATA
        self.inpe_client = None
        
        print("\n" + "="*60)
        print("📦 SMART DATA SERVICE - OPTIMIZED")
        print("="*60)
        
        if self.use_real_api:
            print("🌐 Modo: REAL API (multi-estratégia) + fallback mock")
            print(f"📍 INPE Base URL: {settings.INPE_API_BASE_URL}")
            logger.info("🌐 Smart Service: Modo REAL API otimizado")
            self.inpe_client = INPEClientOptimized(settings.INPE_API_BASE_URL)
            logger.info(f"   📡 INPE Client (optimized) inicializado")
        else:
            print("📦 Modo: MOCK DATA apenas")
            logger.info("📦 Smart Service: Modo MOCK DATA")
        
        print("="*60 + "\n")
    
    async def get_state_data(
        self, 
        state: str, 
        year: int, 
        dataset: str = "prodes_amazon"
    ) -> Dict:
        """
        Busca dados de estado com fallback automático
        """
        logger.info(f"🔍 Request: {state}/{year}")
        
        if not self.use_real_api:
            logger.info("📦 Using MOCK (forced)")
            return self._get_mock_state_data(state, year)
        

        try:
            logger.info("🌐 Trying REAL API...")
            real_data = await self.inpe_client.get_state_deforestation(
                state, year, dataset
            )
            
            if real_data is not None:
                area = real_data.get("area_km2", 0)
                logger.info(f"✅ API SUCCESS: {area:.2f} km²")
                real_data["data_source"] = "real_api"
                return real_data
            
            logger.warning("⚠️ API returned None")
            
        except Exception as e:
            logger.error(f"❌ API error: {e}", exc_info=True)
        

        logger.warning(f"📦 FALLBACK to MOCK for {state}/{year}")
        return self._get_mock_state_data(state, year)
    
    async def compare_data(
        self,
        state_or_biome: str,
        year_start: int,
        year_end: int,
        dataset: str = "prodes_amazon"
    ) -> Dict:
        """
        Comparação temporal otimizada
        """
        logger.info(f"📊 Compare: {state_or_biome} ({year_start}-{year_end})")
        
        if not self.use_real_api:
            return self._get_mock_comparison(state_or_biome, year_start, year_end)
        
        try:
            logger.info("🌐 Trying REAL API comparison...")
            
            series_data = []
            for year in range(year_start, year_end + 1):
                data = await self.inpe_client.get_state_deforestation(
                    state_or_biome, year, dataset, _fetch_previous=False
                )
                if data:
                    series_data.append({
                        "year": year,
                        "area_km2": data["area_km2"]
                    })
            
            if series_data and len(series_data) > 0:
                logger.info(f"✅ API comparison: {len(series_data)} years")
                
                first_area = series_data[0]["area_km2"]
                last_area = series_data[-1]["area_km2"]
                total_change = last_area - first_area
                percentage_change = (total_change / first_area * 100) if first_area > 0 else 0
                
                trend = "increasing" if total_change > 0 else (
                    "decreasing" if total_change < 0 else "stable"
                )
                
                # Resolver nome do estado
                from app.services.inpe_client import resolve_state
                resolved = resolve_state(state_or_biome)
                
                result = {
                    "state": resolved["name"] if resolved else state_or_biome,
                    "state_code": resolved["uf"] if resolved else None,
                    "year_start": year_start,
                    "year_end": year_end,
                    "data": series_data,
                    "total_change_km2": round(total_change, 2),
                    "percentage_change": round(percentage_change, 2),
                    "trend": trend,
                    "biome": series_data[0].get("biome") if series_data else None,
                    "data_source": "real_api",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                return result
            
            logger.warning("⚠️ No data from API")
            
        except Exception as e:
            logger.error(f"❌ Comparison error: {e}", exc_info=True)
        
        # Fallback
        logger.warning(f"📦 FALLBACK to MOCK comparison")
        return self._get_mock_comparison(state_or_biome, year_start, year_end)
    
    async def get_ranking(
        self,
        year: int,
        order: str = "desc",
        limit: int = 10,
        biome: Optional[str] = None,
        dataset: str = "prodes_amazon"
    ) -> Dict:
        """
        Ranking otimizado com queries paralelas
        """
        logger.info(f"🏆 Ranking: {year}")
        
        if not self.use_real_api:
            return self._get_mock_ranking(year, order, limit, biome)
        
        try:
            logger.info("🌐 Trying REAL API ranking...")
            
            real_ranking = await self.inpe_client.get_ranking(
                year, order, limit, biome, dataset
            )
            
            if real_ranking and real_ranking.get("ranking"):
                logger.info(f"✅ API ranking: {len(real_ranking['ranking'])} states")
                real_ranking["data_source"] = "real_api"
                return real_ranking
            
            logger.warning("⚠️ No ranking data from API")
            
        except Exception as e:
            logger.error(f"❌ Ranking error: {e}", exc_info=True)
        
        # Fallback
        logger.warning(f"📦 FALLBACK to MOCK ranking")
        return self._get_mock_ranking(year, order, limit, biome)
    
    # ============================================================
    # MOCK HELPERS
    # ============================================================
    
    def _get_mock_state_data(self, state: str, year: int) -> Dict:
        """Helper para buscar dados mock"""
        result = mock_data_brazil.get_state_data(state, year)
        result['data_source'] = 'mock'
        return result
    
    def _get_mock_comparison(
        self, 
        state_or_biome: str, 
        year_start: int, 
        year_end: int
    ) -> Dict:
        """Helper para comparação mock"""
        result = mock_data_brazil.get_comparison_data(
            state_or_biome, year_start, year_end
        )
        result["data_source"] = "mock"
        return result
    
    def _get_mock_ranking(
        self, 
        year: int, 
        order: str, 
        limit: int, 
        biome: Optional[str]
    ) -> Dict:
        """Helper para ranking mock"""
        result = mock_data_brazil.get_ranking_data(year, order, limit, biome)
        result["data_source"] = "mock"
        return result
    
    async def get_available_states(self, biome: Optional[str] = None) -> Dict:
        """Lista estados disponíveis"""
        return mock_data_brazil.get_available_states(biome)
    
    async def get_available_biomes(self) -> List[str]:
        """Lista biomas disponíveis"""
        return mock_data_brazil.get_available_biomes()
    
    async def get_available_years(self) -> Dict:
        """Lista anos disponíveis"""
        return mock_data_brazil.get_available_years()
    
    async def get_biome_comparison(self, year: int) -> Dict:
        """Comparação de biomas"""
        return mock_data_brazil.get_biome_comparison(year)
    
    async def close(self):
        """Fecha conexões"""
        if self.inpe_client:
            await self.inpe_client.close()