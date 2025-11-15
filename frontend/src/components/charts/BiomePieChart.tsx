'use client';

import React from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface BiomeData {
  biome: string;
  area_km2: number;
  percentage_of_total: number;
  num_states: number;
}

interface BiomePieChartProps {
  data: BiomeData[];
  title?: string;
}

const BIOME_COLORS: Record<string, string> = {
  'Amazônia': '#10b981',
  'Cerrado': '#eab308',
  'Mata Atlântica': '#059669',
  'Caatinga': '#f97316',
  'Pampa': '#84cc16',
  'Pantanal': '#06b6d4',
};

export function BiomePieChart({ data, title = "Distribuição por Bioma" }: BiomePieChartProps) {
  const chartData = data.map(item => ({
    name: item.biome,
    value: Math.round(item.area_km2),
    percentage: item.percentage_of_total.toFixed(1)
  }));

  const renderLabel = (entry: any) => {
    return `${entry.name}: ${entry.percentage}%`;
  };

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={400}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={true}
            label={renderLabel}
            outerRadius={120}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={BIOME_COLORS[entry.name] || '#94a3b8'} 
              />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '12px'
            }}
            formatter={(value: any, name: any, props: any) => [
              `${value.toLocaleString('pt-BR')} km² (${props.payload.percentage}%)`,
              name
            ]}
          />
          <Legend 
            verticalAlign="bottom" 
            height={36}
            formatter={(value) => value}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}