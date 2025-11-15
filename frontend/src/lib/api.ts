/**
 * Cliente API para comunicação com o backend
 * Agora com suporte a TODOS os biomas brasileiros
 */
import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface StateDeforestationData {
  state: string;
  state_code: string;
  year: number;
  area_km2: number;
  percentage_of_total: number;
  biome: string;
  comparison_previous_year: {
    year: number;
    area_km2: number | null;
    change_km2: number;
    change_percentage: number;
  };
  data_source: string;
  timestamp: string;
}

export interface ComparisonData {
  state: string;
  state_code: string;
  biome: string;
  year_start: number;
  year_end: number;
  data: Array<{
    year: number;
    area_km2: number;
  }>;
  total_change_km2: number;
  percentage_change: number;
  trend: 'increasing' | 'decreasing' | 'stable';
  data_source: string;
  timestamp: string;
}

export interface RankingData {
  year: number;
  total_brazil_km2: number;
  order: string;
  biome_filter: string | null;
  ranking: Array<{
    position: number;
    state: string;
    state_code: string;
    area_km2: number;
    percentage_of_total: number;
    biome: string;
  }>;
  data_source: string;
  timestamp: string;
}

export interface BiomeData {
  biome: string;
  area_km2: number;
  percentage_of_total: number;
  num_states: number;
}

export interface BiomeComparisonData {
  year: number;
  total_brazil_km2: number;
  biomes: BiomeData[];
  data_source: string;
  timestamp: string;
}

// Funções de API
export const deforestationApi = {
  // Ação 1: Consultar por estado
  getStateData: async (state: string, year?: number): Promise<StateDeforestationData> => {
    const params = year ? { year } : {};
    const response = await api.get(`/api/deforestation/state/${state}`, { params });
    return response.data;
  },

  // Ação 2: Comparação temporal (estado, bioma ou Brasil)
  compareData: async (
    stateOrBiome: string,
    yearStart: number,
    yearEnd: number
  ): Promise<ComparisonData> => {
    const response = await api.get(`/api/deforestation/compare/${stateOrBiome}`, {
      params: { year_start: yearStart, year_end: yearEnd }
    });
    return response.data;
  },

  // Ação 3: Ranking (com filtro de bioma)
  getRanking: async (
    year: number,
    order: 'desc' | 'asc' = 'desc',
    limit: number = 10,
    biome?: string
  ): Promise<RankingData> => {
    const params: any = { order, limit };
    if (biome) params.biome = biome;
    
    const response = await api.get(`/api/deforestation/ranking/${year}`, { params });
    return response.data;
  },

  // NOVO: Comparar biomas
  compareBiomes: async (year: number): Promise<BiomeComparisonData> => {
    const response = await api.get(`/api/deforestation/biomes/compare/${year}`);
    return response.data;
  },

  // Auxiliares
  getStates: async (biome?: string) => {
    const params = biome ? { biome } : {};
    const response = await api.get('/api/deforestation/states', { params });
    return response.data;
  },

  getYears: async () => {
    const response = await api.get('/api/deforestation/years');
    return response.data;
  },

  getBiomes: async () => {
    const response = await api.get('/api/deforestation/biomes');
    return response.data;
  },
};

export default api;
