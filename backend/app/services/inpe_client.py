# inpe_client_optimized.py
import httpx
import logging
import unicodedata
import re
import asyncio
from typing import Any, Dict, List, Optional, Tuple
from shapely.geometry import shape, mapping, box
from shapely.ops import unary_union
from datetime import datetime

logger = logging.getLogger(__name__)

# ----------------------------
# Config / Layers
# ----------------------------
TERRABRASILIS_BASE = "https://terrabrasilis.dpi.inpe.br/geoserver/ows"

LAYER_CONFIG = {
    "prodes_amazon": {
       
        "deforestation": "prodes-amazon-nb:accumulated_deforestation_2007_biome",
        "states": "prodes-amazon-nb:states_amazon_biome",
    }
}

# Mapeamento de estados
STATE_MAP: Dict[str, str] = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
    "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins",
}

STATE_PRIMARY_BIOME: Dict[str, str] = {
    "Acre": "Amazônia", "Amazonas": "Amazônia", "Amapá": "Amazônia",
    "Maranhão": "Amazônia", "Mato Grosso": "Amazônia", "Pará": "Amazônia",
    "Rondônia": "Amazônia", "Roraima": "Amazônia", "Tocantins": "Cerrado",

}


def _normalize_for_key(s: Optional[str]) -> str:
    if not s:
        return ""
    s = s.strip().upper()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^A-Z0-9]", "", s)
    return s

STATE_NAME_TO_CODE: Dict[str, str] = {
    _normalize_for_key(name): code for code, name in STATE_MAP.items()
}

def resolve_state(user_input: Optional[str]) -> Optional[Dict[str, str]]:
    """
    Resolve input de usuário para estado
    
    Prioridade:
    1. Sigla exata (PA, AM, RO)
    2. Nome normalizado exato (PARA → Pará)
    3. Match parcial comum (Para → Pará, Parana → Paraná)
    4. Prefix match (se único)
    """
    if not user_input:
        return None
    
    raw = user_input.strip()
    

    if len(raw) == 2 and raw.isalpha():
        code = raw.upper()
        if code in STATE_MAP:
            logger.info(f"✅ Sigla: '{raw}' → {STATE_MAP[code]} ({code})")
            return {"name": STATE_MAP[code], "uf": code}
    

    key_norm = _normalize_for_key(raw)
    if key_norm in STATE_NAME_TO_CODE:
        code = STATE_NAME_TO_CODE[key_norm]
        logger.info(f"✅ Nome exato: '{raw}' → {STATE_MAP[code]} ({code})")
        return {"name": STATE_MAP[code], "uf": code}
    

    common_matches = {
        'PARA': 'PA',      
        'PARANA': 'PR',    
        'PARAIBA': 'PB',   
        'CEARA': 'CE',     
        'GOIAS': 'GO',    
        'MARANHAO': 'MA',  
        'PIAUI': 'PI',     
        'RONDONIA': 'RO',  
        'AMAPA': 'AP',     
    }
    
    if key_norm in common_matches:
        code = common_matches[key_norm]
        logger.info(f"✅ Match comum: '{raw}' → {STATE_MAP[code]} ({code})")
        return {"name": STATE_MAP[code], "uf": code}
    
    matches = [code for name_norm, code in STATE_NAME_TO_CODE.items() 
               if name_norm.startswith(key_norm)]
    
    if len(matches) == 1:
        code = matches[0]
        logger.info(f"✅ Prefix único: '{raw}' → {STATE_MAP[code]} ({code})")
        return {"name": STATE_MAP[code], "uf": code}
    
    if len(matches) > 1:
        if key_norm in common_matches:
            code = common_matches[key_norm]
            logger.info(f"✅ Assumindo: '{raw}' → {STATE_MAP[code]} ({code})")
            return {"name": STATE_MAP[code], "uf": code}
        
        logger.warning(f"⚠️ Ambíguo: '{raw}' → opções {matches}")
        logger.warning(f"💡 Sugestão: use 'PA' para Pará, 'PB' para Paraíba, 'PR' para Paraná")
        return None
    
    logger.warning(f"❌ Não reconhecido: '{raw}'")
    return None


class INPEClientOptimized:
    def __init__(self, base_url: str = TERRABRASILIS_BASE, timeout: float = 60.0):
        self.base_url = base_url.rstrip("?")
        self.client = httpx.AsyncClient(
            base_url=self.base_url, 
            timeout=timeout,
            headers={"Accept-Encoding": "gzip, deflate"}
        )
        self._cache: Dict[str, Any] = {}
        self._semaphore = asyncio.Semaphore(3)  # Reduzir concorrência
    
    async def _wfs_request(
        self, 
        type_name: str, 
        cql_filter: Optional[str] = None,
        property_name: Optional[str] = None,
        max_features: int = 5000,
        start_index: int = 0
    ) -> Optional[Dict[str, Any]]:
        """Request WFS com parâmetros otimizados"""
        params = {
            "service": "WFS",
            "version": "1.0.0",
            "request": "GetFeature",
            "typeName": type_name,
            "outputFormat": "application/json",
            "maxFeatures": max_features,
            "startIndex": start_index
        }
        
        if cql_filter:
            params["cql_filter"] = cql_filter
        
        if property_name:
            params["propertyName"] = property_name
        
        try:
            async with self._semaphore:
                logger.debug(f"WFS Request: {type_name}, filter={cql_filter}")
                resp = await self.client.get("", params=params)
                
                if resp.status_code != 200:
                    logger.error(f"WFS error status {resp.status_code}")
                    return None
                
                content_type = resp.headers.get("content-type", "")
                

                if "xml" in content_type:
                    logger.error(f"⚠️ GeoServer returned XML (error): {resp.text[:500]}")
                    

                    if "ServiceException" in resp.text:
                        import re
                        error_match = re.search(r'<ServiceException[^>]*>([^<]+)</ServiceException>', resp.text)
                        if error_match:
                            error_msg = error_match.group(1).strip()
                            logger.error(f"❌ GeoServer error: {error_msg}")
                    
                    return None
                
                if "json" in content_type:
                    return resp.json()
                    
                logger.error(f"Unexpected content-type: {content_type}")
                return None
                
        except Exception as e:
            logger.error(f"WFS request failed: {e}")
            return None
    
    async def _get_deforestation_by_uf(
        self, 
        uf: str, 
        year: int, 
        dataset: str = "prodes_amazon"
    ) -> Optional[float]:
        """
        Busca desmatamento usando filtro por UF (mais eficiente que geometria)
        """
        class_name = f"d{year}"
        

        cql_filter = f"uf='{uf}' AND class_name='{class_name}'"
        
        data = await self._wfs_request(
            type_name="prodes-amazon-nb:yearly_deforestation",
            cql_filter=cql_filter,
            property_name="area_km2", 
            max_features=1000
        )
        
        if data and data.get("features"):
            total_area = sum(
                float(f.get("properties", {}).get("area_km2", 0))
                for f in data["features"]
            )
            logger.info(f"✅ Found {len(data['features'])} features via UF filter")
            return total_area
        
        return None

    async def _get_deforestation_by_bbox(
        self,
        bbox: Tuple[float, float, float, float],
        uf: str,
        year: int,
        dataset: str = "prodes_amazon"
    ) -> Optional[float]:
        """
        Estratégia 2: Query por bounding box + UF
        """
        class_name = f"d{year}"
        minx, miny, maxx, maxy = bbox
        
        layer = LAYER_CONFIG[dataset]["deforestation"]
        cql_filter = f"BBOX(geom,{minx},{miny},{maxx},{maxy}) AND uf='{uf}' AND class_name='{class_name}'"
        
        logger.debug(f"Strategy 2: BBOX filter on {layer}")
        
        data = await self._wfs_request(
            type_name=layer,
            cql_filter=cql_filter,
            max_features=2000
        )
        
        if data and data.get("features"):
            total_area = 0.0
            for feat in data["features"]:
                geom_data = feat.get("geometry")
                if geom_data:
                    try:
                        geom = shape(geom_data)
                        total_area += geom.area / 1e6
                    except:
                        pass
            
            logger.info(f"✅ Strategy 2 success: {total_area:.2f} km²")
            return total_area
        
        logger.warning(f"⚠️ Strategy 2 failed")
        return None
    
    async def _aggregate_by_property(
        self,
        property_value: str,
        property_name: str,
        year: int,
        dataset: str = "prodes_amazon"
    ) -> Optional[float]:
        """
        Agregação server-side quando possível
        """
        class_name = f"d{year}"
        
        cql_filter = f"{property_name}='{property_value}' AND class_name='{class_name}'"
        
        data = await self._wfs_request(
            type_name="prodes-amazon-nb:accumulated_deforestation_2007_biome",
            cql_filter=cql_filter,
            max_features=5000
        )
        
        if not data or not data.get("features"):
            return None
        
        total_area = 0.0
        for feat in data["features"]:
            area = feat.get("properties", {}).get("area_km2")
            if area:
                total_area += float(area)
            else:
                geom_data = feat.get("geometry")
                if geom_data:
                    try:
                        geom = shape(geom_data)
                        total_area += geom.area / 1e6
                    except:
                        pass
        
        return total_area

    async def get_state_deforestation(
        self, 
        state_input: str, 
        year: int, 
        dataset: str = "prodes_amazon",
        _fetch_previous: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Busca desmatamento com múltiplas estratégias (fallback automático)
        """
        resolved = resolve_state(state_input)
        if not resolved:
            logger.warning(f"State '{state_input}' not recognized")
            return None
        
        state_name = resolved["name"]
        uf = resolved["uf"]
        
        logger.info(f"🔍 Fetching deforestation: {state_name} ({uf}) - {year}")
        

        cache_key = f"{uf}_{year}_{dataset}"
        if cache_key in self._cache:
            logger.info("📦 Using cached data")
            return self._cache[cache_key]
        
        area_km2 = None
        

        logger.info("Strategy 1: Direct UF filter")
        area_km2 = await self._get_deforestation_by_uf(uf, year, dataset)
        

        if area_km2 is None:
            logger.warning("Strategy 1 failed, trying Strategy 2: BBOX + UF")
            

            states_data = await self._wfs_request(
                type_name="prodes-amazon-nb:states_amazon_biome",
                cql_filter=f"sigla='{uf}'",
                max_features=1
            )
            
            if states_data and states_data.get("features"):
                state_geom = shape(states_data["features"][0]["geometry"])
                bbox = state_geom.bounds
                area_km2 = await self._get_deforestation_by_bbox(bbox, uf, year, dataset)
        

        if area_km2 is None:
            logger.warning("Strategy 2 failed, trying Strategy 3: Property aggregation")
            area_km2 = await self._aggregate_by_property(uf, "uf", year, dataset)
        

        if area_km2 is None:
            logger.error(f"❌ All strategies failed for {uf}/{year}")
            return None
        

        biome = STATE_PRIMARY_BIOME.get(state_name, "Amazônia")
        

        previous_area = 0.0
        prev_year = year - 1
        if _fetch_previous and prev_year >= 2007:
            prev_data = await self.get_state_deforestation(
                state_input, prev_year, dataset, _fetch_previous=False
            )
            if prev_data:
                previous_area = prev_data.get("area_km2", 0.0)
        
        change_km2 = area_km2 - previous_area
        change_percentage = ((area_km2 - previous_area) / previous_area * 100) if previous_area > 0 else 0.0
        
        result = {
            "state": state_name,
            "state_code": uf,
            "year": year,
            "dataset": dataset,
            "area_km2": round(area_km2, 2),
            "percentage_of_total": 0.0,  
            "comparison_previous_year": {
                "year": prev_year,
                "area_km2": round(previous_area, 2) if previous_area > 0 else None,
                "change_km2": round(change_km2, 2),
                "change_percentage": round(change_percentage, 2)
            },
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Cache result
        self._cache[cache_key] = result
        
        return result

    async def get_ranking(
        self, 
        year: int, 
        order: str = "desc", 
        limit: int = 10,
        biome: Optional[str] = None,
        dataset: str = "prodes_amazon"
    ) -> Dict[str, Any]:
        """
        Ranking com queries paralelas otimizadas
        """
        logger.info(f"🏆 Getting ranking for {year}")
        
        # Lista de estados para buscar
        states_to_fetch = list(STATE_MAP.keys())
        
        # Buscar dados em paralelo (limitado por semaphore)
        tasks = [
            self.get_state_deforestation(uf, year, dataset, _fetch_previous=False)
            for uf in states_to_fetch
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtrar resultados válidos
        valid_results = [
            r for r in results 
            if r is not None and not isinstance(r, Exception) and r.get("area_km2", 0) > 0
        ]
        
        logger.info(f"📊 Got {len(valid_results)}/{len(states_to_fetch)} valid results")
        
        if not valid_results:
            logger.error("No valid results for ranking")
            return {
                "year": year,
                "total_brazil_km2": 0.0,
                "order": order,
                "ranking": [],
                "error": "No data available"
            }
        
        # Ordenar
        reverse = (order.lower() == "desc")
        sorted_states = sorted(valid_results, key=lambda x: x["area_km2"], reverse=reverse)
        
        # Calcular total
        total_brazil = sum(r["area_km2"] for r in valid_results)
        
        # Construir ranking
        ranking = []
        for i, item in enumerate(sorted_states[:limit], start=1):
            percentage = (item["area_km2"] / total_brazil * 100) if total_brazil > 0 else 0.0
            ranking.append({
                "position": i,
                "state": item["state"],
                "state_code": item["state_code"],
                "area_km2": item["area_km2"],
                "percentage_of_total": round(percentage, 2)
            })
        
        return {
            "year": year,
            "total_brazil_km2": round(total_brazil, 2),
            "order": order,
            "biome_filter": biome,
            "ranking": ranking,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def close(self):
        await self.client.aclose()