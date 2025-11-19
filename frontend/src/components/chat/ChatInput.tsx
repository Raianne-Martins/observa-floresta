'use client';

import React, { useState, KeyboardEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
}

export function ChatInput({ onSend, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');

  /**
   * Normaliza input antes de enviar
   * - Completa anos parciais (ex: "202" → "2024")
   * - Normaliza estados (ex: "Para" → "Pará")
   */
  const normalizeInput = (text: string): string => {
    let normalized = text.trim();
    
    const currentYear = new Date().getFullYear();
    normalized = normalized.replace(/\b(20\d{0,2})\b/g, (match) => {
      return match.length < 4 ? currentYear.toString() : match;
    });
    

    if (/^par$/i.test(normalized)) {
      normalized = 'PA';
    }
    

    const stateNormalizations: Record<string, string> = {
      'para': 'Pará',
      'Para': 'Pará',
      'PARA': 'PA',       
      'parana': 'Paraná',
      'Parana': 'Paraná',
      'paraiba': 'Paraíba',
      'Paraiba': 'Paraíba',
      'ceara': 'Ceará',
      'Ceara': 'Ceará',
      'goias': 'Goiás',
      'Goias': 'Goiás',
      'maranhao': 'Maranhão',
      'Maranhao': 'Maranhão',
      'piaui': 'Piauí',
      'Piaui': 'Piauí',
      'rondonia': 'Rondônia',
      'Rondonia': 'Rondônia',
      'amapa': 'Amapá',
      'Amapa': 'Amapá',
    };
    
    // Aplicar normalizações (match de palavras completas)
    Object.entries(stateNormalizations).forEach(([wrong, correct]) => {
      const regex = new RegExp(`\\b${wrong}\\b`, 'gi');
      normalized = normalized.replace(regex, correct);
    });
    
    return normalized;
  };

  const handleSend = () => {
    if (input.trim() && !disabled) {
      const normalized = normalizeInput(input);
      onSend(normalized);
      setInput('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <div className="flex gap-2 items-end">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Digite sua pergunta sobre desmatamento..."
          disabled={disabled}
          rows={2}
          className="flex-1 resize-none rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
        />
        <Button
          onClick={handleSend}
          disabled={disabled || !input.trim()}
          size="lg"
          className="h-[72px]"
        >
          <Send className="h-5 w-5" />
        </Button>
      </div>
      
      <div className="mt-2 flex flex-wrap gap-2">
        <button
          onClick={() => onSend("Qual o desmatamento no Pará em 2024?")}
          disabled={disabled}
          className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50 transition-colors"
        >
          🌳 Pará 2024
        </button>
        <button
          onClick={() => onSend("Compare Amazonas entre 2020 e 2024")}
          disabled={disabled}
          className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50 transition-colors"
        >
          📊 Comparar Amazonas
        </button>
        <button
          onClick={() => onSend("Quais os 5 estados que mais desmataram em 2024?")}
          disabled={disabled}
          className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50 transition-colors"
        >
          🏆 Top 5 estados
        </button>
        <button
          onClick={() => onSend("Ranking da Amazônia em 2024")}
          disabled={disabled}
          className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50 transition-colors"
        >
          🌲 Ranking Amazônia
        </button>
      </div>
      
      <div className="mt-3 text-xs text-gray-500 text-center">
        💡 Dica: Você pode digitar apenas &quot;PA 2024&quot; ou &quot;Pará 202&quot; - eu completo pra você!
      </div>
    </div>
  );
}