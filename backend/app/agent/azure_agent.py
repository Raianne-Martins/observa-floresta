"""
Azure AI Agent Implementation
Integração real com Azure OpenAI
"""
from typing import Dict, Optional
import logging
import json
from openai import AzureOpenAI

from app.config import settings

logger = logging.getLogger(__name__)


class AzureAgent:
    """
    Agente que usa Azure OpenAI para processar queries
    """
    
    def __init__(self):
        """Inicializa cliente Azure OpenAI"""
        logger.info("Inicializando Azure Agent...")
        
        self.client = AzureOpenAI(
            api_key=settings.AZURE_OPENAI_API_KEY,
            api_version=settings.AZURE_OPENAI_API_VERSION,
            azure_endpoint=settings.AZURE_OPENAI_ENDPOINT
        )
        
        self.deployment = settings.AZURE_OPENAI_DEPLOYMENT_NAME
        logger.info(f"Azure Agent inicializado: {self.deployment}")
    
    def _build_system_prompt(self) -> str:
        """Constrói prompt do sistema"""
        return """Você é o Observa Floresta, um assistente especializado em dados ambientais do Brasil.

Você tem acesso a dados de degradação ambiental de todos os estados brasileiros e biomas.

IMPORTANTE:
- Sempre responda em português brasileiro
- Use dados fornecidos nas ferramentas (tools)
- Seja preciso com números
- Explique tendências quando relevante
- Formate respostas de forma clara

BIOMAS BRASILEIROS:
1. Amazônia
2. Cerrado
3. Mata Atlântica
4. Caatinga
5. Pampa
6. Pantanal

AÇÕES DISPONÍVEIS:
1. get_state_deforestation: Consultar dados de um estado
2. compare_deforestation: Comparar períodos temporais
3. get_states_ranking: Ranking de estados
"""
    
    def _build_tools(self) -> list:
        """Define as ferramentas (tools) disponíveis"""
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_state_deforestation",
                    "description": "Obtém dados de degradação ambiental de um estado brasileiro específico",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "state": {
                                "type": "string",
                                "description": "Nome ou sigla do estado (ex: Pará, PA, São Paulo, SP)"
                            },
                            "year": {
                                "type": "integer",
                                "description": "Ano da consulta (2020-2024). Se não especificado, usa 2024",
                                "minimum": 2020,
                                "maximum": 2024
                            }
                        },
                        "required": ["state"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "compare_deforestation",
                    "description": "Compara degradação ambiental entre dois anos. Pode ser usado para estados, biomas ou Brasil inteiro",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "state_or_biome": {
                                "type": "string",
                                "description": "Estado, bioma ou 'Brasil' (ex: Pará, Cerrado, Brasil)"
                            },
                            "year_start": {
                                "type": "integer",
                                "description": "Ano inicial",
                                "minimum": 2020,
                                "maximum": 2024
                            },
                            "year_end": {
                                "type": "integer",
                                "description": "Ano final",
                                "minimum": 2020,
                                "maximum": 2024
                            }
                        },
                        "required": ["state_or_biome", "year_start", "year_end"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_states_ranking",
                    "description": "Retorna ranking de estados por degradação ambiental",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "year": {
                                "type": "integer",
                                "description": "Ano da consulta",
                                "minimum": 2020,
                                "maximum": 2024
                            },
                            "order": {
                                "type": "string",
                                "enum": ["desc", "asc"],
                                "description": "Ordem: desc (maior para menor) ou asc (menor para maior)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Número de estados no ranking",
                                "minimum": 1,
                                "maximum": 27,
                                "default": 10
                            },
                            "biome": {
                                "type": "string",
                                "description": "Filtrar por bioma (opcional)",
                                "enum": ["Amazônia", "Cerrado", "Mata Atlântica", "Caatinga", "Pampa", "Pantanal"]
                            }
                        },
                        "required": ["year"]
                    }
                }
            }
        ]
    
    async def _execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """Executa uma ferramenta e retorna resultado"""
        from app.services import mock_data_brazil as mock_data
        
        logger.info(f"Executando tool: {tool_name} com args: {arguments}")
        
        try:
            if tool_name == "get_state_deforestation":
                state = arguments.get("state")
                year = arguments.get("year", 2024)
                result = mock_data.get_state_data(state, year)
                
            elif tool_name == "compare_deforestation":
                entity = arguments.get("state_or_biome")
                year_start = arguments.get("year_start")
                year_end = arguments.get("year_end")
                result = mock_data.get_comparison_data(entity, year_start, year_end)
                
            elif tool_name == "get_states_ranking":
                year = arguments.get("year")
                order = arguments.get("order", "desc")
                limit = arguments.get("limit", 10)
                biome = arguments.get("biome")
                result = mock_data.get_ranking_data(year, order, limit, biome)
            
            else:
                raise ValueError(f"Tool desconhecida: {tool_name}")
            
            logger.info(f"Tool {tool_name} executada com sucesso")
            return result
            
        except Exception as e:
            logger.error(f"Erro ao executar tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def process_query(self, user_message: str) -> str:
        """
        Processa uma query do usuário usando Azure OpenAI
        
        Args:
            user_message: Pergunta do usuário
            
        Returns:
            Resposta formatada
        """
        logger.info(f"Processando query: {user_message}")
        
        messages = [
            {"role": "system", "content": self._build_system_prompt()},
            {"role": "user", "content": user_message}
        ]
        
        tools = self._build_tools()
        
        try:
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                temperature=0.7,
                max_tokens=1000
            )
            
            response_message = response.choices[0].message
            
            if response_message.tool_calls:
                messages.append(response_message)
                
                for tool_call in response_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)
                    
                    function_response = await self._execute_tool(
                        function_name,
                        function_args
                    )
                    
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(function_response, ensure_ascii=False)
                    })
                
                second_response = self.client.chat.completions.create(
                    model=self.deployment,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1500
                )
                
                final_message = second_response.choices[0].message.content
                
            else:
                final_message = response_message.content
            
            logger.info("Query processada com sucesso")
            return final_message
            
        except Exception as e:
            logger.error(f"Erro ao processar query: {e}")
            return f"Desculpe, ocorreu um erro ao processar sua pergunta: {str(e)}"
    
    async def get_state_deforestation(self, state: str, year: Optional[int] = None):
        """Wrapper para compatibilidade"""
        from app.services import mock_data_brazil as mock_data
        return mock_data.get_state_data(state, year or 2024)
    
    async def compare_deforestation(self, state_or_biome: str, year_start: int, year_end: int):
        """Wrapper para compatibilidade"""
        from app.services import mock_data_brazil as mock_data
        return mock_data.get_comparison_data(state_or_biome, year_start, year_end)
    
    async def get_states_ranking(self, year: int, order: str = "desc", limit: int = 10, biome: Optional[str] = None):
        """Wrapper para compatibilidade"""
        from app.services import mock_data_brazil as mock_data
        return mock_data.get_ranking_data(year, order, limit, biome)
    
    async def get_biome_comparison(self, year: int):
        """Wrapper para compatibilidade"""
        from app.services import mock_data_brazil as mock_data
        return mock_data.get_biome_comparison(year)
    
    async def get_available_states(self, biome: Optional[str] = None):
        """Wrapper para compatibilidade"""
        from app.services import mock_data_brazil as mock_data
        return mock_data.get_available_states(biome)
    
    async def get_available_years(self):
        """Wrapper para compatibilidade"""
        from app.services import mock_data_brazil as mock_data
        return mock_data.get_available_years()
    
    async def get_available_biomes(self):
        """Wrapper para compatibilidade"""
        from app.services import mock_data_brazil as mock_data
        biomes = mock_data.get_available_biomes()
        from datetime import datetime
        return {
            "biomes": biomes,
            "total": len(biomes),
            "timestamp": datetime.utcnow().isoformat()
        }
