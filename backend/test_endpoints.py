"""
Teste dos endpoints da API
Usando requests para simular chamadas HTTP
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_section(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def print_response(response, show_full=False):
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if show_full:
            print(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            # Mostrar apenas campos principais
            if isinstance(data, dict):
                for key, value in data.items():
                    if key not in ['timestamp', 'data_source']:
                        if isinstance(value, (list, dict)) and len(str(value)) > 100:
                            print(f"{key}: (dados omitidos)")
                        else:
                            print(f"{key}: {value}")
    else:
        print(f"Erro: {response.text}")
    print()

def test_endpoints():
    print_section("🧪 TESTE DOS ENDPOINTS - OBSERVA FLORESTA")
    
    # Verificar se servidor está rodando
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print("✅ Backend rodando!")
        print(f"   Modo: {response.json().get('mode')}")
        print(f"   Mock Data: {response.json().get('mock_data')}")
    except Exception as e:
        print(f"❌ Backend não está rodando! Execute: uvicorn app.main:app --reload")
        return
    
    # Teste 1: Endpoint de info
    print_section("1️⃣ Teste: GET /deforestation (info)")
    try:
        response = requests.get(f"{BASE_URL}/deforestation")
        print_response(response, show_full=True)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 2: Estados disponíveis
    print_section("2️⃣ Teste: GET /deforestation/states")
    try:
        response = requests.get(f"{BASE_URL}/deforestation/states")
        print_response(response)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 3: Anos disponíveis
    print_section("3️⃣ Teste: GET /deforestation/years")
    try:
        response = requests.get(f"{BASE_URL}/deforestation/years")
        print_response(response)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 4: Ação 1 - POST
    print_section("4️⃣ Teste: POST /deforestation/state (Pará, 2024)")
    try:
        payload = {
            "state": "Pará",
            "year": 2024
        }
        response = requests.post(
            f"{BASE_URL}/deforestation/state",
            json=payload
        )
        print_response(response)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 5: Ação 1 - GET
    print_section("5️⃣ Teste: GET /deforestation/state/MT?year=2024")
    try:
        response = requests.get(
            f"{BASE_URL}/deforestation/state/MT",
            params={"year": 2024}
        )
        print_response(response)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 6: Ação 2 - POST
    print_section("6️⃣ Teste: POST /deforestation/compare (Amazonas, 2020-2024)")
    try:
        payload = {
            "state": "Amazonas",
            "year_start": 2020,
            "year_end": 2024
        }
        response = requests.post(
            f"{BASE_URL}/deforestation/compare",
            json=payload
        )
        print_response(response)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 7: Ação 2 - GET (Brasil)
    print_section("7️⃣ Teste: GET /deforestation/compare/Brasil")
    try:
        response = requests.get(
            f"{BASE_URL}/deforestation/compare/Brasil",
            params={"year_start": 2020, "year_end": 2024}
        )
        print_response(response)
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 8: Ação 3 - POST
    print_section("8️⃣ Teste: POST /deforestation/ranking (2024, top 5)")
    try:
        payload = {
            "year": 2024,
            "order": "desc",
            "limit": 5
        }
        response = requests.post(
            f"{BASE_URL}/deforestation/ranking",
            json=payload
        )
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Ano: {data['year']}")
        print(f"Total Brasil: {data['total_brazil_km2']} km²")
        print("\nTop 5 Estados:")
        for item in data['ranking']:
            print(f"  {item['position']}º {item['state']:<15} {item['area_km2']:>8.1f} km²")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 9: Ação 3 - GET
    print_section("9️⃣ Teste: GET /deforestation/ranking/2024 (menor para maior)")
    try:
        response = requests.get(
            f"{BASE_URL}/deforestation/ranking/2024",
            params={"order": "asc", "limit": 3}
        )
        data = response.json()
        print(f"Status: {response.status_code}")
        print("\nTop 3 Estados com MENOR desmatamento:")
        for item in data['ranking']:
            print(f"  {item['position']}º {item['state']:<15} {item['area_km2']:>8.1f} km²")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    # Teste 10: Validação de erros
    print_section("🔟 Teste: Validação de erros (estado inválido)")
    try:
        response = requests.get(f"{BASE_URL}/deforestation/state/XYZ")
        print(f"Status: {response.status_code} (esperado: 400)")
        if response.status_code == 400:
            print(f"✅ Erro capturado corretamente: {response.json()['detail']}")
        print()
    except Exception as e:
        print(f"❌ Erro: {e}\n")
    
    print_section("✅ TESTES CONCLUÍDOS!")
    print("📊 Acesse a documentação interativa em: http://localhost:8000/docs")
    print()

if __name__ == "__main__":
    test_endpoints()