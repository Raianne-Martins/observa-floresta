'use client';

import React, { useEffect, useState } from 'react';
import { deforestationApi } from '@/lib/api';

interface BiomeSelectorProps {
  value: string | null;
  onChange: (biome: string | null) => void;
  includeAll?: boolean;
}

const BIOME_COLORS: Record<string, string> = {
  'Amazônia': 'bg-green-100 text-green-800 border-green-300',
  'Cerrado': 'bg-yellow-100 text-yellow-800 border-yellow-300',
  'Mata Atlântica': 'bg-emerald-100 text-emerald-800 border-emerald-300',
  'Caatinga': 'bg-orange-100 text-orange-800 border-orange-300',
  'Pampa': 'bg-lime-100 text-lime-800 border-lime-300',
  'Pantanal': 'bg-blue-100 text-blue-800 border-blue-300',
};

const BIOME_ICONS: Record<string, string> = {
  'Amazônia': '🌳',
  'Cerrado': '🌾',
  'Mata Atlântica': '🌴',
  'Caatinga': '🌵',
  'Pampa': '🌱',
  'Pantanal': '💧',
};

export function BiomeSelector({ value, onChange, includeAll = true }: BiomeSelectorProps) {
  const [biomes, setBiomes] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchBiomes() {
      try {
        const data = await deforestationApi.getBiomes();
        setBiomes(data.biomes);
      } catch (error) {
        console.error('Error fetching biomes:', error);
      } finally {
        setLoading(false);
      }
    }
    fetchBiomes();
  }, []);

  if (loading) {
    return <div className="text-sm text-gray-500">Carregando biomas...</div>;
  }

  return (
    <div className="flex flex-wrap gap-2">
      {includeAll && (
        <button
          onClick={() => onChange(null)}
          className={`
            px-4 py-2 rounded-lg border-2 font-medium text-sm transition-all
            ${value === null
              ? 'bg-gray-800 text-white border-gray-800'
              : 'bg-white text-gray-600 border-gray-300 hover:border-gray-400'
            }
          `}
        >
          🌍 Todos os Biomas
        </button>
      )}
      
      {biomes.map((biome) => (
        <button
          key={biome}
          onClick={() => onChange(biome)}
          className={`
            px-4 py-2 rounded-lg border-2 font-medium text-sm transition-all
            ${value === biome
              ? BIOME_COLORS[biome] + ' border-current'
              : 'bg-white text-gray-600 border-gray-300 hover:border-gray-400'
            }
          `}
        >
          {BIOME_ICONS[biome]} {biome}
        </button>
      ))}
    </div>
  );
}
