'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { BiomeSelector } from '@/components/common/BiomeSelector';
import { deforestationApi } from '@/lib/api';
import { ArrowLeft, Loader2} from 'lucide-react';

export default function DashboardPage() {
  const [rankingData, setRankingData] = useState<any>(null);
  const [biomeComparison, setBiomeComparison] = useState<any>(null);
  const [selectedBiome, setSelectedBiome] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      try {
        const [ranking, biomes] = await Promise.all([
          deforestationApi.getRanking(2024, 'desc', 10, selectedBiome || undefined),
          deforestationApi.compareBiomes(2024)
        ]);
        setRankingData(ranking);
        setBiomeComparison(biomes);
      } catch (error) {
        console.error('Error fetching data:', error);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, [selectedBiome]);

  return (
    <div className="min-h-screen bg-linear-to-b from-green-50 to-green-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-4xl">🌳</span>
              <div>
                <h1 className="text-2xl font-bold text-green-800">
                  Dashboard - Observa Floresta
                </h1>
                <p className="text-sm text-gray-600">
                  Visualização de Dados - Todos os Biomas Brasileiros
                </p>
              </div>
            </div>
            <Link href="/">
              <Button variant="outline">
                <ArrowLeft className="mr-2 h-4 w-4" />
                Voltar
              </Button>
            </Link>
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
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Total Brasil (2024)</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-green-600">
                    {rankingData?.total_brazil_km2.toLocaleString('pt-BR')} km²
                  </p>
                  <p className="text-sm text-gray-600 mt-2">
                    Área total degradada
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Estados</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-blue-600">27</p>
                  <p className="text-sm text-gray-600 mt-2">
                    Todos os estados
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Biomas</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-purple-600">6</p>
                  <p className="text-sm text-gray-600 mt-2">
                    Biomas monitorados
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="text-lg">Período</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-3xl font-bold text-orange-600">
                    2020-2024
                  </p>
                  <p className="text-sm text-gray-600 mt-2">
                    5 anos de dados
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Biome Comparison */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Comparação de Biomas (2024)</CardTitle>
                <CardDescription>
                  Distribuição da degradação entre os biomas brasileiros
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {biomeComparison?.biomes.map((biome: any, index: number) => (
                    <div
                      key={biome.biome}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex items-center gap-4 flex-1">
                        <div className={`
                          w-10 h-10 rounded-full flex items-center justify-center font-bold text-white text-sm
                          ${index === 0 ? 'bg-red-500' : 
                            index === 1 ? 'bg-orange-500' : 
                            index === 2 ? 'bg-yellow-500' : 
                            'bg-gray-400'}
                        `}>
                          {index + 1}º
                        </div>
                        <div className="flex-1">
                          <div className="flex items-center gap-2">
                            <p className="font-semibold text-lg">{biome.biome}</p>
                            <span className="text-sm text-gray-500">
                              ({biome.num_states} estado{biome.num_states > 1 ? 's' : ''})
                            </span>
                          </div>
                          <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                            <div
                              className="bg-green-600 h-2 rounded-full transition-all"
                              style={{ width: `${biome.percentage_of_total}%` }}
                            />
                          </div>
                        </div>
                      </div>
                      <div className="text-right ml-4">
                        <p className="font-bold text-xl text-gray-800">
                          {biome.area_km2.toLocaleString('pt-BR')} km²
                        </p>
                        <p className="text-sm text-gray-600">
                          {biome.percentage_of_total.toFixed(1)}% do total
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Biome Filter */}
            <Card className="mb-8">
              <CardHeader>
                <CardTitle>Filtrar por Bioma</CardTitle>
                <CardDescription>
                  Selecione um bioma para ver apenas seus estados no ranking
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

            {/* Ranking Table */}
            <Card>
              <CardHeader>
                <CardTitle>
                  Ranking de Estados (2024)
                  {selectedBiome && ` - ${selectedBiome}`}
                </CardTitle>
                <CardDescription>
                  {selectedBiome
                    ? `Estados do bioma ${selectedBiome} ordenados por área degradada`
                    : 'Todos os estados ordenados por área degradada'
                  }
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {rankingData?.ranking.map((item: any) => (
                    <div
                      key={item.position}
                      className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex items-center gap-4">
                        <div className={`
                          w-10 h-10 rounded-full flex items-center justify-center font-bold text-white
                          ${item.position === 1 ? 'bg-red-500' : 
                            item.position === 2 ? 'bg-orange-500' : 
                            item.position === 3 ? 'bg-yellow-500' : 
                            'bg-gray-400'}
                        `}>
                          {item.position}º
                        </div>
                        <div>
                          <p className="font-semibold text-lg">{item.state}</p>
                          <p className="text-sm text-gray-600">
                            {item.state_code} • {item.biome}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="font-bold text-xl text-gray-800">
                          {item.area_km2.toLocaleString('pt-BR')} km²
                        </p>
                        <p className="text-sm text-gray-600">
                          {item.percentage_of_total.toFixed(1)}% do total
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* CTA to Chat */}
            <div className="mt-8 text-center">
              <Card className="p-8">
                <h3 className="text-2xl font-bold mb-4">Quer explorar mais?</h3>
                <p className="text-gray-600 mb-6">
                  Use nosso chat para fazer perguntas específicas sobre qualquer bioma ou estado!
                </p>
                <Link href="/chat">
                  <Button size="lg">
                    Ir para o Chat
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
