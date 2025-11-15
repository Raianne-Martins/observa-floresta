'use client';

import React from 'react';
import { cn } from '@/lib/utils';

interface MessageBubbleProps {
  message: string;
  isUser: boolean;
  timestamp?: string;
}

export function MessageBubble({ message, isUser, timestamp }: MessageBubbleProps) {
  return (
    <div className={cn("flex w-full mb-4", isUser ? "justify-end" : "justify-start")}>
      <div className={cn("flex flex-col max-w-[70%]", isUser ? "items-end" : "items-start")}>
        <div
          className={cn(
            "rounded-lg px-4 py-2 shadow-sm",
            isUser
              ? "bg-green-600 text-white"
              : "bg-white border border-gray-200 text-gray-800"
          )}
        >
          <p className="text-sm whitespace-pre-wrap">{message}</p>
        </div>
        {timestamp && (
          <span className="text-xs text-gray-500 mt-1 px-2">
            {new Date(timestamp).toLocaleTimeString('pt-BR', {
              hour: '2-digit',
              minute: '2-digit'
            })}
          </span>
        )}
      </div>
    </div>
  );
}
