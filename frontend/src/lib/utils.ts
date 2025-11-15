import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatNumber(num: number, decimals: number = 1): string {
  return num.toFixed(decimals);
}

export function formatPercentage(num: number, decimals: number = 1): string {
  return `${num >= 0 ? '+' : ''}${num.toFixed(decimals)}%`;
}

export function getTrendColor(trend: 'increasing' | 'decreasing' | 'stable'): string {
  switch (trend) {
    case 'increasing':
      return 'text-red-600';
    case 'decreasing':
      return 'text-green-600';
    case 'stable':
      return 'text-yellow-600';
  }
}

export function getTrendIcon(trend: 'increasing' | 'decreasing' | 'stable'): string {
  switch (trend) {
    case 'increasing':
      return '📈';
    case 'decreasing':
      return '📉';
    case 'stable':
      return '➡️';
  }
}
