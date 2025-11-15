"""
Modelos de Response (Pydantic)
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class ComparisonPreviousYear(BaseModel):
    """Comparação com ano anterior"""
    year: int
    area_km2: Optional[float]
    change_km2: float
    change_percentage: float


class StateDeforestationResponse(BaseModel):
    """Response de consulta por estado"""
    state: str
    state_code: str
    year: int
    area_km2: float
    percentage_of_total: float
    biome: str
    comparison_previous_year: ComparisonPreviousYear
    data_source: str
    timestamp: str


class DataPoint(BaseModel):
    """Ponto de dados temporal"""
    year: int
    area_km2: float


class ComparisonResponse(BaseModel):
    """Response de comparação temporal"""
    state: str
    state_code: str
    biome: str
    year_start: int
    year_end: int
    data: List[DataPoint]
    total_change_km2: float
    percentage_change: float
    trend: Literal["increasing", "decreasing", "stable"]
    data_source: str
    timestamp: str


class RankingItem(BaseModel):
    """Item do ranking"""
    position: int
    state: str
    state_code: str
    area_km2: float
    percentage_of_total: float
    biome: str


class RankingResponse(BaseModel):
    """Response de ranking"""
    year: int
    total_brazil_km2: float
    order: str
    ranking: List[RankingItem]
    data_source: str
    timestamp: str


class StateInfo(BaseModel):
    """Informações de um estado"""
    name: str
    code: str
    biome: str


class StatesListResponse(BaseModel):
    """Response de lista de estados"""
    states: List[StateInfo]
    total: int
    timestamp: str


class YearsListResponse(BaseModel):
    """Response de lista de anos"""
    years: List[int]
    total: int
    timestamp: str


class ErrorResponse(BaseModel):
    """Response de erro"""
    detail: str
    status_code: int
    timestamp: str


class BiomeData(BaseModel):
    """Dados de um bioma"""
    biome: str
    area_km2: float
    percentage_of_total: float
    num_states: int


class BiomeComparisonResponse(BaseModel):
    """NOVA: Response de comparação de biomas"""
    year: int
    total_brazil_km2: float
    biomes: List[BiomeData]
    data_source: str
    timestamp: str


class BiomesListResponse(BaseModel):
    """NOVA: Response de lista de biomas"""
    biomes: List[str]
    total: int
    timestamp: str
