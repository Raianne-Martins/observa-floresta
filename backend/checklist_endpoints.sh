# Criar checklist de verificação

echo "========================================"
echo "  CHECKLIST DE ENDPOINTS"
echo "========================================"
echo ""

BASE="http://localhost:8000/api"

# Função para testar endpoint
test_endpoint() {
    local method=$1
    local url=$2
    local name=$3
    
    echo -n "[$method] $name ... "
    
    if [ "$method" = "GET" ]; then
        status=$(curl -s -o /dev/null -w "%{http_code}" "$url")
    else
        status=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$url" -H "Content-Type: application/json" -d '{}')
    fi
    
    if [ "$status" -eq 200 ] || [ "$status" -eq 400