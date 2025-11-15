"""
Models do Observa Floresta
"""
from app.models.requests import (
    StateDeforestationRequest,
    ComparisonRequest,
    RankingRequest
)
from app.models.responses import (
    StateDeforestationResponse,
    ComparisonResponse,
    RankingResponse,
    StatesListResponse,
    YearsListResponse,
    ErrorResponse
)

__all__ = [
    # Requests
    "StateDeforestationRequest",
    "ComparisonRequest",
    "RankingRequest",
    # Responses
    "StateDeforestationResponse",
    "ComparisonResponse",
    "RankingResponse",
    "StatesListResponse",
    "YearsListResponse",
    "ErrorResponse"
]
