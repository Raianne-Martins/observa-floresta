'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { MessageSquare, BarChart3, Leaf, TrendingDown, TrendingUp } from 'lucide-react';

interface HealthCheck {
  status: string;
  timestamp: string;
  environment: string;
  mode: string;
  mock_data: boolean;
  version: string;
}

export default function Home() {
  const [health, setHealth] = useState<HealthCheck | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    async function fetchHealth() {
      try {
        const response = await api.get<HealthCheck>('/api/health');
        setHealth(response.data);
      } catch (error) {
        console.error('Erro ao buscar health:', error);
      } finally {
        setLoading(false);
      }
    }

    fetchHealth();
  }, []);

  // Funções para navegação dos cards
  const handleCardClick = (action: string) => {
    // Salvar query no localStorage para o chat processar
    if (typeof window !== 'undefined') {
      localStorage.setItem('pendingQuery', action);
      router.push('/chat');
    }
  };

  return (
    <main className="min-h-screen bg-linear-to-b from-green-50 to-green-100">
      {/* Hero Section */}
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <span className="text-8xl">🌳</span>
          </div>
          <h1 className="text-6xl font-bold text-green-800 mb-4">
            Observa Floresta
          </h1>
          <p className="text-2xl text-green-600 mb-8">
            Monitoramento de Desmatamento na Amazônia Legal
          </p>
          <div className="flex gap-4 justify-center">
            <Link href="/chat">
              <Button size="lg" className="text-lg">
                <MessageSquare className="mr-2 h-5 w-5" />
                Iniciar Chat
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="outline" className="text-lg">
                <BarChart3 className="mr-2 h-5 w-5" />
                Ver Dashboard
              </Button>
            </Link>
            <Link href="/analytics">
              <Button size="lg" variant="outline" className="text-lg">
                <TrendingUp className="mr-2 h-5 w-5" />
                Ver Analytics
              </Button>
            </Link>
          </div>
        </div>

        {/* Features - AGORA CLICÁVEIS */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-16">
          <Card
            className="hover:shadow-lg transition-all cursor-pointer hover:scale-105"
            onClick={() => handleCardClick('Qual o desmatamento no Pará em 2024?')}
          >
            <CardHeader>
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
                <Leaf className="h-6 w-6 text-blue-600" />
              </div>
              <CardTitle>Dados em Tempo Real</CardTitle>
              <CardDescription>
                Acesse dados atualizados de desmatamento dos estados da Amazônia Legal
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-blue-600 font-medium">
                👉 Clique para consultar um estado
              </p>
            </CardContent>
          </Card>

          <Card
            className="hover:shadow-lg transition-all cursor-pointer hover:scale-105"
            onClick={() => handleCardClick('Compare Amazonas entre 2020 e 2024')}
          >
            <CardHeader>
              <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
                <TrendingDown className="h-6 w-6 text-purple-600" />
              </div>
              <CardTitle>Análise Temporal</CardTitle>
              <CardDescription>
                Compare a evolução do desmatamento ao longo dos anos e identifique tendências
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-purple-600 font-medium">
                👉 Clique para comparar períodos
              </p>
            </CardContent>
          </Card>

          <Card
            className="hover:shadow-lg transition-all cursor-pointer hover:scale-105"
            onClick={() => router.push('/dashboard')}
          >
            <CardHeader>
              <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center mb-4">
                <BarChart3 className="h-6 w-6 text-orange-600" />
              </div>
              <CardTitle>Rankings e Estatísticas</CardTitle>
              <CardDescription>
                Visualize rankings de estados e estatísticas consolidadas do desmatamento
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-orange-600 font-medium">
                👉 Clique para ver o dashboard
              </p>
            </CardContent>
          </Card>
        </div>

        {/* System Status */}
        <Card className="max-w-2xl mx-auto">
          <CardHeader>
            <CardTitle>Status do Sistema</CardTitle>
          </CardHeader>
          <CardContent>
            {loading ? (
              <div className="text-center py-8">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
                <p className="mt-4 text-gray-600">Verificando conexão...</p>
              </div>
            ) : health ? (
              <div className="space-y-4">
                <div className="flex justify-between items-center p-4 bg-green-50 rounded-lg">
                  <span className="font-medium text-gray-700">Status:</span>
                  <span className="px-3 py-1 bg-green-500 text-white rounded-full text-sm font-medium">
                    ✅ {health.status}
                  </span>
                </div>

                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="font-medium text-gray-700">Modo:</span>
                  <span className="text-gray-600">{health.mode}</span>
                </div>

                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="font-medium text-gray-700">Ambiente:</span>
                  <span className="text-gray-600">{health.environment}</span>
                </div>

                <div className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                  <span className="font-medium text-gray-700">Versão:</span>
                  <span className="text-gray-600">{health.version}</span>
                </div>
              </div>
            ) : (
              <div className="text-center py-8 text-red-600">
                ❌ Erro ao conectar com o backend
                <p className="text-sm text-gray-600 mt-2">
                  Certifique-se de que o backend está rodando em http://localhost:8000
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* About */}
        <div className="mt-16 text-center max-w-3xl mx-auto">
          <h2 className="text-3xl font-bold text-gray-800 mb-4">
            Sobre o Projeto
          </h2>
          <p className="text-gray-600 leading-relaxed">
            O <strong>Observa Floresta</strong> é um sistema inteligente de monitoramento
            de desmatamento na Amazônia Legal, desenvolvido como parte do{' '}
            <strong>Azure Frontier Girls - Build Your First Copilot Challenge</strong>.
            Utilizando dados públicos do INPE, IBGE e MapBiomas, oferecemos uma interface
            intuitiva para consultar, comparar e analisar dados de desmatamento dos 9 estados
            da Amazônia Legal.
          </p>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 mt-16">
        <div className="container mx-auto px-4 py-8 text-center text-gray-600">
          <p>🌳 Observa Floresta - Azure Frontier Girls Challenge 2024</p>
          <p className="text-sm mt-2">
            Dados: INPE • IBGE • MapBiomas | Tecnologias: Next.js • FastAPI • Azure AI Foundry
          </p>
        </div>
      </footer>
    </main>
  );
}
