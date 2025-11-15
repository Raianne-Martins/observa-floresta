"""
Modelos de Request (Pydantic)
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Literal


class StateDeforestationRequest(BaseModel):
    """Request para consulta de desmatamento por estado"""
    state: str = Field(
        ...,
        description="Nome ou sigla do estado",
        example="Pará"
    )
    year: Optional[int] = Field(
        None,
        description="Ano da consulta (se None, usa ano atual)",
        ge=2020,
        le=2024,
        example=2024
    )
    
    @validator('state')
    def validate_state(cls, v):
        if not v or not v.strip():
            raise ValueError("Estado não pode ser vazio")
        return v.strip()


class ComparisonRequest(BaseModel):
    """Request para comparação temporal"""
    state_or_biome: str = Field(
        ...,
        description="Nome do estado, bioma ou 'Brasil' para agregado",
        example="Amazonas"
    )
    year_start: int = Field(
        ...,
        description="Ano inicial",
        ge=2020,
        le=2024,
        example=2020
    )
    year_end: int = Field(
        ...,
        description="Ano final",
        ge=2020,
        le=2024,
        example=2024
    )
    
    @validator('year_end')
    def validate_years(cls, v, values):
        if 'year_start' in values and v <= values['year_start']:
            raise ValueError("year_end deve ser maior que year_start")
        return v
    
    @validator('state_or_biome')
    def validate_entity(cls, v):
        if not v or not v.strip():
            raise ValueError("Estado/Bioma não pode ser vazio")
        return v.strip()


class RankingRequest(BaseModel):
    """Request para ranking de estados"""
    year: int = Field(
        ...,
        description="Ano da consulta",
        ge=2020,
        le=2024,
        example=2024
    )
    order: Literal["desc", "asc"] = Field(
        "desc",
        description="Ordem (desc = maior para menor, asc = menor para maior)"
    )
    limit: int = Field(
        10,
        description="Número de estados no ranking",
        ge=1,
        le=30
    )
    biome: Optional[str] = Field(
        None,
        description="Filtrar por bioma (opcional)",
        example="Amazônia"
    )


class BiomeComparisonRequest(BaseModel):
    """NOVA: Request para comparação de biomas"""
    year: int = Field(
        ...,
        description="Ano da comparação",
        ge=2020,
        le=2024,
        example=2024
    )