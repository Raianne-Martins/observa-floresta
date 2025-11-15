'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { TrendChart } from '@/components/charts/TrendChart';

interface ChartMessageProps {
  data: Array<{
    year: number;
    area_km2: number;
  }>;
  title: string;
  trend: 'increasing' | 'decreasing' | 'stable';
}

export function ChartMessage({ data, title, trend }: ChartMessageProps) {
  const getTrendColor = () => {
    switch (trend) {
      case 'decreasing': return '#10b981';
      case 'increasing': return '#ef4444';
      default: return '#eab308';
    }
  };

  return (
    <Card className="p-4 my-2 max-w-2xl">
      <TrendChart
        data={data}
        title={title}
        color={getTrendColor()}
        showArea={true}
      />
    </Card>
  );
}