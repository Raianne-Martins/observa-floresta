# 🌳 Observa Floresta

Sistema de monitoramento de desmatamento na Amazônia Legal utilizando Azure AI Foundry e análise de dados ambientais.

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
venv\Scripts\activate.bat  #no powershell
pip install -r requirements.txt
cp .env.example .env
# Editar .env conforme necessário
uvicorn app.main:app --reload
#ou
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Editar .env.local conforme necessário
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

(Em desenvolvimento - será detalhado conforme implementação)

## 📸 Screenshots

(Serão adicionados durante o desenvolvimento)

## 📝 Licença

MIT

## 👩‍💻 Autora

Raianne Martins

---

**Status**: 🚧 Em desenvolvimento
```

---
