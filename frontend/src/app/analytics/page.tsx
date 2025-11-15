'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BiomeSelector } from '@/components/common/BiomeSelector';
import { TrendChart } from '@/components/charts/TrendChart';
import { RankingBarChart } from '@/components/charts/RankingBarChart';
import { BiomePieChart } from '@/components/charts/BiomePieChart';
import { deforestationApi } from '@/lib/api';
import { ArrowLeft, Loader2 } from 'lucide-react';

export default function AnalyticsPage() {
  const [selectedBiome, setSelectedBiome] = useState<string | null>(null);
  const [comparisonData, setComparisonData] = useState<any>(null);
  const [rankingData, setRankingData] = useState<any>(null);
  const [biomeData, setBiomeData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const entity = selectedBiome || 'Brasil';
        
        const [comparison, ranking, biomes] = await Promise.all([
          deforestationApi.compareData(entity, 2020, 2024),
          deforestationApi.getRanking(2024, 'desc', 10, selectedBiome || undefined),
          deforestationApi.compareBiomes(2024)
        ]);
        
        setComparisonData(comparison);
        setRankingData(ranking);
        setBiomeData(biomes);
      } catch (error) {
        console.error('Error fetching analytics data:', error);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, [selectedBiome]);

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'decreasing': return '#10b981'; // green
      case 'increasing': return '#ef4444'; // red
      default: return '#eab308'; // yellow
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-b from-green-50 to-green-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-4xl">📊</span>
              <div>
                <h1 className="text-2xl font-bold text-green-800">
                  Analytics - Observa Floresta
                </h1>
                <p className="text-sm text-gray-600">
                  Visualizações e Gráficos Interativos
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <Link href="/">
                <Button variant="outline">
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Voltar
                </Button>
              </Link>
              <Link href="/dashboard">
                <Button variant="outline">
                  Dashboard
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {loading ? (
          <div className="flex items-center justify-center h-96">
            <Loader2 className="h-12 w-12 animate-spin text-green-600" />
          </div>
        ) : (
          <>
            {/* Filtro de Bioma */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Selecione um Bioma para Análise</CardTitle>
                <CardDescription>
                  Escolha um bioma específico ou veja dados do Brasil inteiro
                </CardDescription>
              </CardHeader>
              <CardContent>
                <BiomeSelector
                  value={selectedBiome}
                  onChange={setSelectedBiome}
                  includeAll={true}
                />
              </CardContent>
            </Card>

            {/* Resumo com Tendência */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>
                  {selectedBiome || 'Brasil'} - Resumo (2020-2024)
                </CardTitle>
                <CardDescription>
                  Evolução temporal da degradação ambiental
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-2">Mudança Total</p>
                    <p className={`text-3xl font-bold ${
                      comparisonData.total_change_km2 < 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {comparisonData.total_change_km2 > 0 ? '+' : ''}
                      {comparisonData.total_change_km2.toLocaleString('pt-BR')} km²
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-2">Variação (%)</p>
                    <p className={`text-3xl font-bold ${
                      comparisonData.percentage_change < 0 ? 'text-green-600' : 'text-red-600'
                    }`}>
                      {comparisonData.percentage_change > 0 ? '+' : ''}
                      {comparisonData.percentage_change.toFixed(1)}%
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-2">Tendência</p>
                    <p className="text-3xl font-bold">
                      {comparisonData.trend === 'decreasing' && '📉'}
                      {comparisonData.trend === 'increasing' && '📈'}
                      {comparisonData.trend === 'stable' && '➡️'}
                    </p>
                    <p className="text-sm text-gray-600 mt-1">
                      {comparisonData.trend === 'decreasing' && 'Redução'}
                      {comparisonData.trend === 'increasing' && 'Aumento'}
                      {comparisonData.trend === 'stable' && 'Estável'}
                    </p>
                  </div>
                  
                  <div className="text-center">
                    <p className="text-sm text-gray-600 mb-2">Bioma</p>
                    <p className="text-xl font-bold text-gray-800">
                      {comparisonData.biome}
                    </p>
                  </div>
                </div>

                <TrendChart
                  data={comparisonData.data}
                  title={`Evolução Temporal - ${selectedBiome || 'Brasil'}`}
                  color={getTrendColor(comparisonData.trend)}
                  showArea={true}
                />
              </CardContent>
            </Card>

            {/* Grid com 2 gráficos */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
              {/* Ranking em Barras */}
              <Card>
                <CardHeader>
                  <CardTitle>
                    Ranking de Estados - 2024
                    {selectedBiome && ` (${selectedBiome})`}
                  </CardTitle>
                  <CardDescription>
                    Top 10 estados por área degradada
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <RankingBarChart data={rankingData.ranking} />
                </CardContent>
              </Card>

              {/* Distribuição por Bioma */}
              <Card>
                <CardHeader>
                  <CardTitle>Distribuição por Bioma - 2024</CardTitle>
                  <CardDescription>
                    Participação de cada bioma no total nacional
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <BiomePieChart data={biomeData.biomes} />
                </CardContent>
              </Card>
            </div>

            {/* Detalhamento de Biomas */}
            <Card>
              <CardHeader>
                <CardTitle>Detalhamento por Bioma</CardTitle>
                <CardDescription>
                  Comparação detalhada entre todos os biomas brasileiros
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {biomeData.biomes.map((biome: any, index: number) => (
                    <div
                      key={biome.biome}
                      className="p-4 border-2 border-gray-200 rounded-lg hover:border-green-500 transition-colors cursor-pointer"
                      onClick={() => setSelectedBiome(biome.biome)}
                    >
                      <div className="flex items-center justify-between mb-3">
                        <h4 className="font-semibold text-lg">{biome.biome}</h4>
                        <span className={`
                          w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm
                          ${index === 0 ? 'bg-red-500' : 
                            index === 1 ? 'bg-orange-500' : 
                            index === 2 ? 'bg-yellow-500' : 
                            'bg-gray-400'}
                        `}>
                          {index + 1}
                        </span>
                      </div>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Área:</span>
                          <span className="font-semibold">
                            {biome.area_km2.toLocaleString('pt-BR')} km²
                          </span>
                        </div>
                        
                        <div className="flex justify-between">
                          <span className="text-gray-600">% Total:</span>
                          <span className="font-semibold">
                            {biome.percentage_of_total.toFixed(1)}%
                          </span>
                        </div>
                        
                        <div className="flex justify-between">
                          <span className="text-gray-600">Estados:</span>
                          <span className="font-semibold">
                            {biome.num_states}
                          </span>
                        </div>
                      </div>

                      <div className="w-full bg-gray-200 rounded-full h-2 mt-3">
                        <div
                          className="bg-green-600 h-2 rounded-full transition-all"
                          style={{ width: `${biome.percentage_of_total}%` }}
                        />
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* CTA */}
            <div className="mt-8 text-center">
              <Card className="p-8">
                <h3 className="text-2xl font-bold mb-4">Explore mais com nosso Chat!</h3>
                <p className="text-gray-600 mb-6">
                  Faça perguntas específicas e obtenha análises personalizadas sobre qualquer estado ou bioma.
                </p>
                <Link href="/chat">
                  <Button size="lg">
                    Ir para o Chat Inteligente
                  </Button>
                </Link>
              </Card>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
