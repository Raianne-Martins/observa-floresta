'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { BarChart3, TrendingDown, Trophy } from 'lucide-react';

interface QuickActionsProps {
  onActionClick: (query: string) => void;
}

export function QuickActions({ onActionClick }: QuickActionsProps) {
  const actions = [
    {
      icon: BarChart3,
      title: "Consultar Estado",
      description: "Dados de desmatamento por estado",
      query: "Qual o desmatamento no Pará em 2024?",
      color: "bg-blue-50 text-blue-600"
    },
    {
      icon: TrendingDown,
      title: "Comparar Períodos",
      description: "Evolução temporal do desmatamento",
      query: "Compare Mato Grosso entre 2020 e 2024",
      color: "bg-purple-50 text-purple-600"
    },
    {
      icon: Trophy,
      title: "Ranking de Estados",
      description: "Estados mais/menos desmatados",
      query: "Quais os 5 estados que mais desmataram em 2024?",
      color: "bg-orange-50 text-orange-600"
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {actions.map((action, index) => (
        <Card
          key={index}
          className="cursor-pointer hover:shadow-md transition-shadow"
          onClick={() => onActionClick(action.query)}
        >
          <div className="p-6">
            <div className={`w-12 h-12 rounded-lg ${action.color} flex items-center justify-center mb-4`}>
              <action.icon className="h-6 w-6" />
            </div>
            <h3 className="font-semibold text-lg mb-2">{action.title}</h3>
            <p className="text-sm text-gray-600">{action.description}</p>
          </div>
        </Card>
      ))}
    </div>
  );
}
