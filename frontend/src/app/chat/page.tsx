'use client';

import React, { useState, useRef, useEffect } from 'react';
import { MessageBubble } from '@/components/chat/MessageBubble';
import { ChatInput } from '@/components/chat/ChatInput';
import { QuickActions } from '@/components/chat/QuickActions';
import { Card } from '@/components/ui/card';
import { deforestationApi } from '@/lib/api';
import { Link, Loader2 } from 'lucide-react';

interface Message {
  id: string;
  content: string;
  isUser: boolean;
  timestamp: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const processedPendingQuery = useRef(false);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    if (typeof window !== 'undefined' && !processedPendingQuery.current) {
      const pendingQuery = localStorage.getItem('pendingQuery');
      if (pendingQuery) {
        processedPendingQuery.current = true;
        localStorage.removeItem('pendingQuery');
        // Pequeno delay para a UI carregar
        setTimeout(() => {
          processQuery(pendingQuery);
        }, 500);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const addMessage = (content: string, isUser: boolean) => {
    const newMessage: Message = {
      id: Date.now().toString(),
      content,
      isUser,
      timestamp: new Date().toISOString(),
    };
    setMessages((prev) => [...prev, newMessage]);
  };

  const processQuery = async (query: string) => {
    addMessage(query, true);
    setIsLoading(true);

    try {
      const lowerQuery = query.toLowerCase();

      // Ação 1: Consulta por estado
      if (lowerQuery.includes('desmatamento') && (lowerQuery.includes('em') || lowerQuery.includes('no'))) {
        const stateMatch = query.match(/(?:em|no|na)\s+(\w+)/i);
        const yearMatch = query.match(/(\d{4})/);

        if (stateMatch) {
          const state = stateMatch[1];
          const year = yearMatch ? parseInt(yearMatch[1]) : undefined;

          const data = await deforestationApi.getStateData(state, year);

          const response = `📊 **Desmatamento em ${data.state} (${data.year})**

🌳 Área desmatada: **${data.area_km2.toLocaleString('pt-BR')} km²**
📈 Percentual do total: **${data.percentage_of_total.toFixed(1)}%**
🏞️ Bioma: ${data.biome}

**Comparação com ${data.comparison_previous_year.year}:**
${data.comparison_previous_year.change_km2 < 0 ? '📉' : '📈'} ${data.comparison_previous_year.change_percentage > 0 ? '+' : ''}${data.comparison_previous_year.change_percentage.toFixed(1)}% (${data.comparison_previous_year.change_km2 > 0 ? '+' : ''}${data.comparison_previous_year.change_km2.toFixed(1)} km²)`;

          addMessage(response, false);
        }
      }


      else if (lowerQuery.includes('bioma') ||
        lowerQuery.match(/amazônia|cerrado|mata atlântica|caatinga|pampa|pantanal/i)) {

        // Comparação de biomas
        if (lowerQuery.includes('compar') || lowerQuery.includes('todos')) {
          const yearMatch = query.match(/(\d{4})/);
          const year = yearMatch ? parseInt(yearMatch[1]) : 2024;

          const data = await deforestationApi.compareBiomes(year);

          const response = `🌍 **Comparação de Biomas (${data.year})**

📊 Total Brasil: **${data.total_brazil_km2.toLocaleString('pt-BR')} km²**

**Ranking por bioma:**

${data.biomes.map((b, idx) =>
            `${idx + 1}º ${b.biome}
   └─ ${b.area_km2.toLocaleString('pt-BR')} km² (${b.percentage_of_total.toFixed(1)}% do total)
   └─ ${b.num_states} estado${b.num_states > 1 ? 's' : ''} afetado${b.num_states > 1 ? 's' : ''}`
          ).join('\n\n')}`;

          addMessage(response, false);
        }
        // Ranking de um bioma específico
        else if (lowerQuery.includes('ranking') || lowerQuery.includes('estados')) {
          const biomeMatch = query.match(/(amazônia|cerrado|mata atlântica|caatinga|pampa|pantanal)/i);
          const yearMatch = query.match(/(\d{4})/);

          if (biomeMatch) {
            const biome = biomeMatch[1];
            const year = yearMatch ? parseInt(yearMatch[1]) : 2024;

            const data = await deforestationApi.getRanking(year, 'desc', 10, biome);

            const response = `🏆 **Ranking - ${biome} (${year})**

${data.ranking.map(item =>
              `${item.position}º ${item.state} (${item.state_code})
   └─ ${item.area_km2.toLocaleString('pt-BR')} km²`
            ).join('\n\n')}`;

            addMessage(response, false);
          }
        }
      }

      // Ação 2: Comparação temporal
      else if (lowerQuery.includes('compare') || lowerQuery.includes('compar') || lowerQuery.includes('entre')) {
        const stateMatch =
          query.match(/(?:compare|compar)[a-z]*\s+(\w+)/i) ||
          query.match(/(\w+)\s+entre/i);
        const yearsMatch = query.match(/(\d{4})\s+(?:e|a|até)\s+(\d{4})/);

        if (stateMatch && yearsMatch) {
          const state = stateMatch[1];
          const yearStart = parseInt(yearsMatch[1]);
          const yearEnd = parseInt(yearsMatch[2]);

          const data = await deforestationApi.compareData(state, yearStart, yearEnd);

          const trendEmoji =
            data.trend === 'decreasing'
              ? '📉'
              : data.trend === 'increasing'
                ? '📈'
                : '➡️';

          const trendText =
            data.trend === 'decreasing'
              ? 'REDUÇÃO'
              : data.trend === 'increasing'
                ? 'AUMENTO'
                : 'ESTÁVEL';

          const response = `📊 **Comparação: ${data.state} (${data.year_start}-${data.year_end})**

${trendEmoji} **Tendência: ${trendText}**

📉 Mudança total: ${data.total_change_km2 > 0 ? '+' : ''}${data.total_change_km2.toFixed(1)} km²
📊 Variação percentual: ${data.percentage_change > 0 ? '+' : ''}${data.percentage_change.toFixed(1)}%

**Dados por ano:**
${data.data.map((d) => `${d.year}: ${d.area_km2.toFixed(1)} km²`).join('\n')}

🏞️ Bioma: ${data.biome}`;

          addMessage(response, false);
        }
      }

      // Ação 3: Ranking
      else if (lowerQuery.includes('ranking') || lowerQuery.includes('top') || lowerQuery.includes('quais')) {
        const yearMatch = query.match(/(\d{4})/);
        const limitMatch = query.match(/(\d+)\s+estados?/i);

        const year = yearMatch ? parseInt(yearMatch[1]) : 2024;
        const limit = limitMatch ? parseInt(limitMatch[1]) : 5;
        const order =
          lowerQuery.includes('menos') || lowerQuery.includes('menor') ? 'asc' : 'desc';

        const data = await deforestationApi.getRanking(year, order, limit);

        const response = `🏆 **Ranking de Desmatamento (${data.year})**

📊 Total Brasil: **${data.total_brazil_km2.toLocaleString('pt-BR')} km²**

${order === 'desc' ? '**Estados que MAIS desmataram:**' : '**Estados que MENOS desmataram:**'}

${data.ranking
            .map(
              (item, idx) =>
                `${idx + 1}º ${item.state} (${item.state_code})
   └─ ${item.area_km2.toLocaleString('pt-BR')} km² (${item.percentage_of_total.toFixed(1)}% do total)`
            )
            .join('\n\n')}`;

        addMessage(response, false);
      }

      // Caso não reconheça o comando
      else {
        addMessage(
          '❓ Desculpe, não entendi sua pergunta. Tente perguntar sobre:\n\n' +
          '• "Qual o desmatamento no [Estado] em [Ano]?"\n' +
          '• "Compare [Estado] entre [Ano] e [Ano]"\n' +
          '• "Quais os 5 estados que mais desmataram em [Ano]?"',
          false
        );
      }
    } catch (error) {
      console.error('Error processing query:', error);
      addMessage(
        '❌ Ocorreu um erro ao processar sua consulta. Por favor, tente novamente ou reformule a pergunta.',
        false
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-b from-green-50 to-green-100">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-4xl">🌳</span>
              <div>
                <h1 className="text-2xl font-bold text-green-800">Observa Floresta</h1>
                <p className="text-sm text-gray-600">
                  Monitoramento de Desmatamento na Amazônia Legal
                </p>
              </div>
            </div>

            <div className="flex gap-2">
              <Link href="/" className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900">
                Início
              </Link>

              <a
                href="/dashboard"
                className="px-4 py-2 text-sm text-gray-600 hover:text-gray-900"
              >
                Dashboard
              </a>
            </div>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Welcome Message */}
        {messages.length === 0 && (
          <div className="mb-8">
            <Card className="p-8 text-center">
              <span className="text-6xl mb-4 block">🌳</span>
              <h2 className="text-3xl font-bold text-gray-800 mb-4">
                Olá! Sou o Observa Floresta
              </h2>
              <p className="text-gray-600 mb-8 max-w-2xl mx-auto">
                Estou aqui para te ajudar a entender os dados de desmatamento na Amazônia Legal.
                Pergunte-me sobre estados específicos, compare períodos ou veja rankings!
              </p>
              <QuickActions onActionClick={processQuery} />
            </Card>
          </div>
        )}

        {/* Chat Messages */}
        <Card className="h-[600px] flex flex-col">
          <div className="flex-1 overflow-y-auto p-6">
            {messages.map((message) => (
              <MessageBubble
                key={message.id}
                message={message.content}
                isUser={message.isUser}
                timestamp={message.timestamp}
              />
            ))}

            {isLoading && (
              <div className="flex items-center justify-start mb-4">
                <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-green-600" />
                  <span className="text-sm text-gray-600">Consultando dados...</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <ChatInput onSend={processQuery} disabled={isLoading} />
        </Card>

        {/* Info Footer */}
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>
            💡 Dica: Use linguagem natural! Exemplos: &quot;Qual o desmatamento em RO?&quot;
            ou &quot;Compare PA entre 2020 e 2024&quot;
          </p>
        </div>
      </div>
    </div>
  );
}

