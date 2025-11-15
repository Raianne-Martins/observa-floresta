/**
 * Página inicial do Observa Floresta
 */
'use client';

console.log("API_URL FRONT:", process.env.NEXT_PUBLIC_API_URL);

import { useEffect, useState } from 'react';
import api from '@/lib/api';
import type { HealthCheck } from '@/types';

export default function Home() {
  const [health, setHealth] = useState<HealthCheck | null>(null);
  const [loading, setLoading] = useState(true);

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

  return (
    <main className="min-h-screen bg-linear-to-b from-green-50 to-green-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-green-800 mb-4">
            🌳 Observa Floresta
          </h1>
          <p className="text-xl text-green-600">
            Monitoramento de Desmatamento na Amazônia Legal
          </p>
        </div>

        <div className="max-w-2xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">
            Status do Sistema
          </h2>
          
          {loading ? (
            <div className="text-center py-8">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
              <p className="mt-4 text-gray-600">Carregando...</p>
            </div>
          ) : health ? (
            <div className="space-y-4">
              <div className="flex justify-between items-center p-4 bg-green-50 rounded">
                <span className="font-medium text-gray-700">Status:</span>
                <span className="px-3 py-1 bg-green-500 text-white rounded-full text-sm">
                  {health.status}
                </span>
              </div>
              
              <div className="flex justify-between items-center p-4 bg-gray-50 rounded">
                <span className="font-medium text-gray-700">Modo:</span>
                <span className="text-gray-600">{health.mode}</span>
              </div>
              
              <div className="flex justify-between items-center p-4 bg-gray-50 rounded">
                <span className="font-medium text-gray-700">Ambiente:</span>
                <span className="text-gray-600">{health.environment}</span>
              </div>
              
              <div className="flex justify-between items-center p-4 bg-gray-50 rounded">
                <span className="font-medium text-gray-700">Versão:</span>
                <span className="text-gray-600">{health.version}</span>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-red-600">
              ❌ Erro ao conectar com o backend
            </div>
          )}

          <div className="mt-8 pt-8 border-t border-gray-200">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Próximos Passos
            </h3>
            <ul className="space-y-2 text-gray-600">
              <li>✅ Backend configurado</li>
              <li>✅ Frontend configurado</li>
              <li>⏳ Implementar ações de desmatamento</li>
              <li>⏳ Criar interface de chat</li>
              <li>⏳ Adicionar dashboard de analytics</li>
            </ul>
          </div>
        </div>
      </div>
    </main>
  );
}