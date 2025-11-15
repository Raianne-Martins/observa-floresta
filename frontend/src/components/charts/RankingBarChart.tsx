'use client';

import React from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  Cell
} from 'recharts';

interface RankingItem {
  position: number;
  state: string;
  state_code: string;
  area_km2: number;
  percentage_of_total: number;
  biome: string;
}

interface RankingBarChartProps {
  data: RankingItem[];
  title?: string;
}

const COLORS = [
  '#ef4444', // red-500
  '#f97316', // orange-500
  '#eab308', // yellow-500
  '#84cc16', // lime-500
  '#22c55e', // green-500
  '#14b8a6', // teal-500
  '#06b6d4', // cyan-500
  '#3b82f6', // blue-500
  '#8b5cf6', // violet-500
  '#ec4899', // pink-500
];

export function RankingBarChart({ data, title = "Ranking de Estados" }: RankingBarChartProps) {
  const chartData = data.map((item, index) => ({
    estado: item.state_code,
    'Área (km²)': Math.round(item.area_km2),
    nome: item.state,
    bioma: item.biome
  }));

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={chartData} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            type="number"
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            tickFormatter={(value) => `${(value / 1000).toFixed(1)}k`}
          />
          <YAxis 
            type="category"
            dataKey="estado"
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            width={50}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '12px'
            }}
            formatter={(value: any, name: any, props: any) => [
              `${value.toLocaleString('pt-BR')} km²`,
              props.payload.nome
            ]}
            labelFormatter={(label, payload) => {
              if (payload && payload[0]) {
                return `${payload[0].payload.nome} (${label}) - ${payload[0].payload.bioma}`;
              }
              return label;
            }}
          />
          <Legend />
          <Bar dataKey="Área (km²)" radius={[0, 8, 8, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}