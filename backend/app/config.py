"""
Configuração centralizada da aplicação
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Settings do Observa Floresta"""
    
    # Application Mode
    USE_AZURE_AGENT: bool = False
    MOCK_DATA: bool = True
    ENVIRONMENT: str = "development"
    
    # Azure OpenAI (para Agent Mode)
    AZURE_OPENAI_ENDPOINT: str = ""
    AZURE_OPENAI_API_KEY: str = ""
    AZURE_OPENAI_DEPLOYMENT_NAME: str = "gpt-4"
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_AI_PROJECT_NAME: str = "observa-floresta"
    
    # External APIs
    INPE_API_BASE_URL: str = "https://terrabrasilis.dpi.inpe.br/api/v1"
    INPE_API_KEY: str = ""
    IBGE_API_BASE_URL: str = "https://servicodados.ibge.gov.br/api/v1"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # Cache
    CACHE_TTL: int = 3600
    ENABLE_CACHE: bool = True
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Retorna lista de origens permitidas para CORS"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    @property
    def is_development(self) -> bool:
        """Verifica se está em ambiente de desenvolvimento"""
        return self.ENVIRONMENT == "development"
    
    @property
    def is_production(self) -> bool:
        """Verifica se está em ambiente de produção"""
        return self.ENVIRONMENT == "production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância global de configuração
settings = Settings()