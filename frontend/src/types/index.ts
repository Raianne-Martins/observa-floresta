/**
 * Tipos TypeScript do Observa Floresta
 */

export interface HealthCheck {
  status: string;
  timestamp: string;
  environment: string;
  mode: string;
  mock_data: boolean;
  version: string;
}

export interface DeforestationData {
  state: string;
  year: number;
  area_km2: number;
  percentage: number;
  biome: string;
}

export interface ComparisonData {
  state: string;
  year_start: number;
  year_end: number;
  data: Array<{
    year: number;
    area_km2: number;
  }>;
  total_change_km2: number;
  percentage_change: number;
  trend: 'increasing' | 'decreasing' | 'stable';
}

export interface RankingData {
  year: number;
  ranking: Array<{
    position: number;
    state: string;
    area_km2: number;
    percentage_total: number;
  }>;
}

export interface ApiError {
  detail: string;
  status_code: number;
}