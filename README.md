# 🌳 Observa Floresta

Sistema de monitoramento de desmatamento nos biomas brasileiros utilizando Azure AI Foundry e análise de dados ambientais.

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte do **Azure Frontier Girls 2025**.

O Observa Floresta é um agente inteligente que permite consultar, comparar e analisar dados de desmatamento dos estados da Amazônia Legal, utilizando dados públicos do INPE, IBGE e MapBiomas.

## 🏗️ Arquitetura

O projeto utiliza uma arquitetura híbrida:

- **Agent Mode**: Utiliza Azure AI Foundry para processamento de linguagem natural
- **Direct Mode**: Lógica implementada diretamente no backend (para desenvolvimento e economia de custos)

### Stack Tecnológica

**Backend:**
- Python 3.12.x
- FastAPI
- Azure AI Foundry SDK
- Pandas (análise de dados)

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- Recharts (visualizações)

## 🚀 Como Executar

### Pré-requisitos

- Python 3.12.x
- Node.js 18+
- Conta Azure (para modo Agent)

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
cp .env.example .env
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Testes
```bash
cd backend
python test_endpoints.py
```

## 📊 Funcionalidades

### 3 Ações Principais

1. **Consulta por Estado**: Dados de desmatamento de um estado específico
2. **Comparação Temporal**: Análise de tendências ao longo dos anos
3. **Ranking de Estados**: Estados mais/menos desmatados

## 🎓 Decisões Técnicas

### 📊 Sobre os Dados

#### Fontes de Dados

Os dados utilizados neste projeto são **baseados em fontes oficiais**:
- **INPE** (Instituto Nacional de Pesquisas Espaciais) - TerraBrasilis
- **IBGE** (Instituto Brasileiro de Geografia e Estatística)
- **MapBiomas** - Plataforma de dados ambientais

#### Implementação Atual

Para fins de **demonstração e desenvolvimento**, o sistema utiliza dados mockados que:

✅ **Refletem tendências reais** observadas nos últimos anos  
✅ **Mantêm proporções realistas** entre estados e biomas  
✅ **Seguem padrões históricos** de 2020-2024  
✅ **São consistentes** com relatórios oficiais publicados

## 📸 Screenshots


![Figura 1. Azure AI Foundry - Projeto criado](..\Screenshots\criar_projeto.png)
<br>
![Figura 2. Agente deployado](..\Screenshots\agente_criado.png)
<br>
![Figura 3. Página de credenciais](..\Screenshots\credenciais_criadas.png)
<br>
![Figura 4. Playground](..\Screenshots\playground_agents.png)
<br>
![Figura 5. Terminal com Azure Agent Mode](..\Screenshots\azure_agent_terminal.png)
<br>
![Video 1. Swagger com resposta do agent](..\Screenshots\aswagger.mp4)
<br>
![Figura 6. Chat com agent](..\Screenshots\aswagger.mp4)
<br>

## 📝 Licença

MIT

## 👩‍💻 Autora

Raianne Martins

---

**Status**: 🚧 Em desenvolvimento
```

---
