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

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSend(input.trim());
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
          className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50"
        >
          Pará 2024
        </button>
        <button
          onClick={() => onSend("Compare Amazonas entre 2020 e 2024")}
          disabled={disabled}
          className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50"
        >
          Comparar Amazonas
        </button>
        <button
          onClick={() => onSend("Quais os 5 estados que mais desmataram em 2024?")}
          disabled={disabled}
          className="text-xs px-3 py-1 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-700 disabled:opacity-50"
        >
          Top 5 estados
        </button>
      </div>
    </div>
  );
}
