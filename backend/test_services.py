"""
Script de teste dos services
"""
import asyncio
from app.services.direct_service import DirectService


async def test_services():
    service = DirectService()
    
    print("\n" + "=" * 60)
    print("🧪 Testando Services do Observa Floresta")
    print("=" * 60)
    
    # Teste 1: Dados por estado
    print("\n1️⃣ Teste: get_state_deforestation")
    print("-" * 60)
    try:
        result = await service.get_state_deforestation("Pará", 2024)
        print(f"✅ Estado: {result['state']} ({result['state_code']})")
        print(f"✅ Área: {result['area_km2']} km²")
        print(f"✅ Percentual do total: {result['percentage_of_total']}%")
        print(f"✅ Bioma: {result['biome']}")
        print(f"✅ Mudança vs 2023: {result['comparison_previous_year']['change_percentage']}%")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 2: Comparação temporal
    print("\n2️⃣ Teste: compare_deforestation")
    print("-" * 60)
    try:
        result = await service.compare_deforestation("Amazonas", 2020, 2024)
        print(f"✅ Estado: {result['state']} ({result['state_code']})")
        print(f"✅ Período: {result['year_start']} - {result['year_end']}")
        print(f"✅ Mudança total: {result['total_change_km2']} km² ({result['percentage_change']:.1f}%)")
        print(f"✅ Tendência: {result['trend']}")
        print(f"✅ Pontos de dados: {len(result['data'])}")
        print("   Anos:", [d['year'] for d in result['data']])
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 3: Ranking
    print("\n3️⃣ Teste: get_states_ranking")
    print("-" * 60)
    try:
        result = await service.get_states_ranking(2024, "desc", 5)
        print(f"✅ Ano: {result['year']}")
        print(f"✅ Total Brasil: {result['total_brazil_km2']} km²")
        print(f"✅ Top 5 estados que mais desmataram:")
        for item in result['ranking']:
            print(f"   {item['position']}º {item['state']:<15} {item['area_km2']:>8.1f} km² ({item['percentage_of_total']:>5.1f}%)")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 4: Estados disponíveis
    print("\n4️⃣ Teste: get_available_states")
    print("-" * 60)
    try:
        result = await service.get_available_states()
        print(f"✅ Total de estados: {result['total']}")
        print("✅ Estados da Amazônia Legal:")
        for state in result['states'][:5]:  # Mostrar só os 5 primeiros
            print(f"   - {state['name']} ({state['code']}) - {state['biome']}")
        print(f"   ... e mais {result['total'] - 5} estados")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 5: Anos disponíveis
    print("\n5️⃣ Teste: get_available_years")
    print("-" * 60)
    try:
        result = await service.get_available_years()
        print(f"✅ Total de anos: {result['total']}")
        print(f"✅ Anos disponíveis: {result['years']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 6: Teste com siglas
    print("\n6️⃣ Teste: Usando siglas de estado")
    print("-" * 60)
    try:
        result = await service.get_state_deforestation("MT", 2024)
        print(f"✅ MT reconhecido como: {result['state']}")
        print(f"✅ Área: {result['area_km2']} km²")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 7: Teste com Brasil
    print("\n7️⃣ Teste: Comparação para Brasil (agregado)")
    print("-" * 60)
    try:
        result = await service.compare_deforestation("Brasil", 2020, 2024)
        print(f"✅ Brasil: {result['state']}")
        print(f"✅ Mudança total: {result['total_change_km2']} km²")
        print(f"✅ Tendência: {result['trend']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Todos os testes concluídos!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    asyncio.run(test_services())
