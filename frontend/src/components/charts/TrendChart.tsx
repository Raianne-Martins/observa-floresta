'use client';

import React from 'react';
import {
  LineChart,
  Line,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface TrendChartProps {
  data: Array<{
    year: number;
    area_km2: number;
  }>;
  title?: string;
  color?: string;
  showArea?: boolean;
}

export function TrendChart({ 
  data, 
  title = "Tendência Temporal",
  color = "#16a34a",
  showArea = false 
}: TrendChartProps) {
  const chartData = data.map(d => ({
    ano: d.year.toString(),
    'Área (km²)': Math.round(d.area_km2)
  }));

  const ChartComponent = showArea ? AreaChart : LineChart;
  const DataComponent = showArea ? Area : Line;

  return (
    <div className="w-full">
      {title && (
        <h3 className="text-lg font-semibold text-gray-800 mb-4">{title}</h3>
      )}
      <ResponsiveContainer width="100%" height={300}>
        <ChartComponent data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="ano" 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            tickFormatter={(value) => `${(value / 1000).toFixed(1)}k`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: 'white',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '8px'
            }}
            formatter={(value: any) => [
              `${value.toLocaleString('pt-BR')} km²`,
              'Área'
            ]}
          />
          <Legend />
          <DataComponent
            type="monotone"
            dataKey="Área (km²)"
            stroke={color}
            fill={showArea ? `${color}33` : undefined}
            strokeWidth={3}
            dot={{ fill: color, r: 4 }}
            activeDot={{ r: 6 }}
          />
        </ChartComponent>
      </ResponsiveContainer>
    </div>
  );
}
