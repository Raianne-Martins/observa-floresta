"""
Script para testar DirectService e verificar se está usando API real ou mock
"""
import asyncio
import logging
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def test_direct_service():
    """Testa DirectService com logs detalhados"""
    
    print("\n" + "="*70)
    print("🧪 TESTE DO DIRECT SERVICE")
    print("="*70)
    
    from app.services.direct_service import DirectService
    from app.config import settings
    

    print("\n📋 CONFIGURAÇÃO ATUAL:")
    print(f"   USE_MOCK_DATA: {settings.USE_MOCK_DATA}")
    print(f"   USE_AGENT: {settings.USE_AGENT}")
    print(f"   INPE_BASE_URL: {settings.INPE_BASE_URL}")
    

    print("\n🔧 Inicializando DirectService...")
    service = DirectService()
    
    try:
        print("\n" + "="*70)
        print("📊 TESTE 1: Ranking de Estados 2024")
        print("="*70)
        
        result = await service.get_states_ranking(
            year=2024,
            order='desc',
            limit=5
        )
        
        print(f"\n✅ Resultado recebido:")
        print(f"   Fonte: {result.get('data_source', 'desconhecida')}")
        print(f"   Total de estados: {len(result.get('data', []))}")
        
        if result.get('data'):
            print(f"\n   Top 3:")
            for i, state in enumerate(result['data'][:3], 1):
                print(f"      {i}. {state}")
        

        print("\n" + "="*70)
        print("📈 TESTE 2: Comparação Amazonas 2020-2024")
        print("="*70)
        
        result = await service.compare_deforestation(
            state_or_biome='Amazonas',
            year_start=2020,
            year_end=2024
        )
        
        print(f"\n✅ Resultado recebido:")
        print(f"   Fonte: {result.get('data_source', 'desconhecida')}")
        print(f"   Estado: {result.get('state', 'N/A')}")
        print(f"   Período: {result.get('period', 'N/A')}")
        
        if 'yearly_data' in result:
            print(f"\n   Dados anuais:")
            for year, value in sorted(result['yearly_data'].items()):
                print(f"      {year}: {value} km²")
        
        print("\n" + "="*70)
        print("🌳 TESTE 3: Desmatamento São Paulo 2024")
        print("="*70)
        
        result = await service.get_state_deforestation(
            state='SP',
            year=2024
        )
        
        print(f"\n✅ Resultado recebido:")
        print(f"   Fonte: {result.get('data_source', 'desconhecida')}")
        print(f"   Estado: {result.get('state', 'N/A')}")
        print(f"   Ano: {result.get('year', 'N/A')}")
        print(f"   Desmatamento: {result.get('deforestation_km2', 'N/A')} km²")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n🔌 Fechando serviço...")
        await service.close()
    
    print("\n" + "="*70)
    print("✅ TESTES CONCLUÍDOS")
    print("="*70)
    
    print("\n🔍 DIAGNÓSTICO:")
    if settings.USE_MOCK_DATA:
        print("   ⚠️  USE_MOCK_DATA=true")
        print("   💡 Para usar API real, configure USE_MOCK_DATA=false no .env")
    else:
        print("   ✅ USE_MOCK_DATA=false (correto)")
        print("   💡 Se ainda assim está usando mock, verifique:")
        print("      1. SmartService está respeitando a configuração?")
        print("      2. INPEClient está fazendo chamadas reais?")
        print("      3. API do INPE está acessível?")
        print("\n   🧪 Teste direto da API:")
        print("      curl 'http://terrabrasilis.dpi.inpe.br/api/v1/deforestation?year_start=2024&year_end=2024'")


async def test_api_directly():
    """Testa API INPE diretamente"""
    
    print("\n" + "="*70)
    print("🌐 TESTE DIRETO DA API INPE")
    print("="*70)
    
    import aiohttp
    from app.config import settings
    
    url = f"{settings.INPE_BASE_URL}/deforestation"
    params = {
        'year_start': 2024,
        'year_end': 2024
    }
    
    print(f"\n📡 Testando: {url}")
    print(f"   Params: {params}")
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as response:
                print(f"\n   Status: {response.status}")
                print(f"   URL completa: {response.url}")
                
                if response.status == 200:
                    data = await response.json()
                    
                    if isinstance(data, list):
                        print(f"   ✅ Dados recebidos: {len(data)} registros")
                        
                        if data:
                            print(f"\n   📋 Amostra do primeiro registro:")
                            first = data[0]
                            for key, value in list(first.items())[:5]:
                                print(f"      {key}: {value}")
                    else:
                        print(f"   ℹ️  Tipo de resposta: {type(data)}")
                        print(f"   Chaves: {list(data.keys()) if isinstance(data, dict) else 'N/A'}")
                else:
                    text = await response.text()
                    print(f"   ❌ Erro: {text[:200]}")
    
    except asyncio.TimeoutError:
        print(f"   ⏱️  Timeout - API não respondeu em 10 segundos")
    except Exception as e:
        print(f"   ❌ Erro: {e}")


if __name__ == "__main__":
    print("\n🚀 Iniciando testes...\n")
    

    asyncio.run(test_api_directly())
    asyncio.run(test_direct_service())
    
    print("\n✅ Todos os testes concluídos!\n")