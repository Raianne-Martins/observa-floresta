/**
 * Utilitário para parse de queries de desmatamento
 * Extrai estados, anos e intenções do texto do usuário
 */

export interface ParsedQuery {
  type: 'state' | 'compare' | 'ranking' | 'biome' | 'unknown';
  state?: string;
  year?: number;
  yearStart?: number;
  yearEnd?: number;
  limit?: number;
  order?: 'asc' | 'desc';
  biome?: string;
}

// Mapa de estados (sigla → nome)
const STATE_MAP: Record<string, string> = {
  AC: 'Acre',
  AL: 'Alagoas',
  AP: 'Amapá',
  AM: 'Amazonas',
  BA: 'Bahia',
  CE: 'Ceará',
  DF: 'Distrito Federal',
  ES: 'Espírito Santo',
  GO: 'Goiás',
  MA: 'Maranhão',
  MT: 'Mato Grosso',
  MS: 'Mato Grosso do Sul',
  MG: 'Minas Gerais',
  PA: 'Pará',
  PB: 'Paraíba',
  PR: 'Paraná',
  PE: 'Pernambuco',
  PI: 'Piauí',
  RJ: 'Rio de Janeiro',
  RN: 'Rio Grande do Norte',
  RS: 'Rio Grande do Sul',
  RO: 'Rondônia',
  RR: 'Roraima',
  SC: 'Santa Catarina',
  SP: 'São Paulo',
  SE: 'Sergipe',
  TO: 'Tocantins',
};

// Mapa reverso (nome → sigla) sem acentos também
const STATE_PATTERNS = [
  { pattern: /\b(ac|acre)\b/i, code: 'AC' },
  { pattern: /\b(al|alagoas)\b/i, code: 'AL' },
  { pattern: /\b(ap|amapá|amapa)\b/i, code: 'AP' },
  { pattern: /\b(am|amazonas)\b/i, code: 'AM' },
  { pattern: /\b(ba|bahia)\b/i, code: 'BA' },
  { pattern: /\b(ce|ceará|ceara)\b/i, code: 'CE' },
  { pattern: /\b(df|distrito federal)\b/i, code: 'DF' },
  { pattern: /\b(es|espírito santo|espirito santo)\b/i, code: 'ES' },
  { pattern: /\b(go|goiás|goias)\b/i, code: 'GO' },
  { pattern: /\b(ma|maranhão|maranhao)\b/i, code: 'MA' },
  { pattern: /\b(mt|mato grosso)\b/i, code: 'MT' },
  { pattern: /\b(ms|mato grosso do sul)\b/i, code: 'MS' },
  { pattern: /\b(mg|minas gerais)\b/i, code: 'MG' },
  { pattern: /\b(pa|pará|para)\b/i, code: 'PA' },
  { pattern: /\b(pb|paraíba|paraiba)\b/i, code: 'PB' },
  { pattern: /\b(pr|paraná|parana)\b/i, code: 'PR' },
  { pattern: /\b(pe|pernambuco)\b/i, code: 'PE' },
  { pattern: /\b(pi|piauí|piaui)\b/i, code: 'PI' },
  { pattern: /\b(rj|rio de janeiro)\b/i, code: 'RJ' },
  { pattern: /\b(rn|rio grande do norte)\b/i, code: 'RN' },
  { pattern: /\b(rs|rio grande do sul)\b/i, code: 'RS' },
  { pattern: /\b(ro|rondônia|rondonia)\b/i, code: 'RO' },
  { pattern: /\b(rr|roraima)\b/i, code: 'RR' },
  { pattern: /\b(sc|santa catarina)\b/i, code: 'SC' },
  { pattern: /\b(sp|são paulo|sao paulo)\b/i, code: 'SP' },
  { pattern: /\b(se|sergipe)\b/i, code: 'SE' },
  { pattern: /\b(to|tocantins)\b/i, code: 'TO' },
];

// Biomas brasileiros

/**
 * Extrai estado do texto
 */
export function extractState(text: string): string | undefined {
  const normalized = text.toLowerCase();

  for (const { pattern, code } of STATE_PATTERNS) {
    if (pattern.test(normalized)) {
      return code;
    }
  }

  return undefined;
}

/**
 * Extrai ano único do texto (para consultas simples)
 */
export function extractYear(text: string): number | undefined {
  // Procurar ano de 4 dígitos (2000-2099)
  const match = text.match(/\b(20\d{2})\b/);
  if (match) {
    return parseInt(match[1]);
  }

  // Procurar ano parcial e completar com ano atual
  const partialMatch = text.match(/\b(20\d{0,1})\b/);
  if (partialMatch) {
    const partial = partialMatch[1];
    const currentYear = new Date().getFullYear();

    // Se digitou "202", usar ano atual
    if (partial.length < 4) {
      return currentYear;
    }
  }

  return undefined;
}

/**
 * Extrai intervalo de anos (para comparações)
 */
export function extractYearRange(text: string): {
  yearStart?: number;
  yearEnd?: number;
} {
  // Padrões: "entre 2020 e 2024", "de 2020 a 2024", "2020-2024", "2020 2024"
  const patterns = [
    /entre\s+(\d{4})\s+e\s+(\d{4})/i,
    /de\s+(\d{4})\s+a(?:té)?\s+(\d{4})/i,
    /(\d{4})\s*[-–]\s*(\d{4})/,
    /(\d{4})\s+(?:a|e)\s+(\d{4})/i,
  ];

  for (const pattern of patterns) {
    const match = text.match(pattern);
    if (match) {
      return {
        yearStart: parseInt(match[1]),
        yearEnd: parseInt(match[2]),
      };
    }
  }

  return {};
}

/**
 * Extrai bioma do texto
 */
export function extractBiome(text: string): string | undefined {
  const normalized = text.toLowerCase();

  const biomePatterns = [
    { pattern: /\b(amazônia|amazonia)\b/i, name: 'Amazônia' },
    { pattern: /\b(cerrado)\b/i, name: 'Cerrado' },
    { pattern: /\b(mata atlântica|mata atlantica)\b/i, name: 'Mata Atlântica' },
    { pattern: /\b(caatinga)\b/i, name: 'Caatinga' },
    { pattern: /\b(pampa)\b/i, name: 'Pampa' },
    { pattern: /\b(pantanal)\b/i, name: 'Pantanal' },
  ];

  for (const { pattern, name } of biomePatterns) {
    if (pattern.test(normalized)) {
      return name;
    }
  }

  return undefined;
}

/**
 * Extrai limite de resultados
 */
export function extractLimit(text: string): number | undefined {
  const match = text.match(/(\d+)\s+estados?/i);
  if (match) {
    return parseInt(match[1]);
  }

  // Padrões como "top 5", "5 primeiros"
  const topMatch = text.match(/top\s+(\d+)/i);
  if (topMatch) {
    return parseInt(topMatch[1]);
  }

  return undefined;
}

/**
 * Detecta tipo de query
 */
export function detectQueryType(text: string): ParsedQuery['type'] {
  const lower = text.toLowerCase();

  // Ranking
  if (
    lower.includes('ranking') ||
    lower.includes('top') ||
    lower.includes('quais') ||
    lower.includes('estados que mais') ||
    lower.includes('estados que menos')
  ) {
    return 'ranking';
  }

  // Comparação
  if (
    lower.includes('compar') ||
    lower.includes('entre') ||
    lower.includes('de ') ||
    lower.includes('evolu')
  ) {
    return 'compare';
  }

  // Bioma
  if (lower.includes('bioma')) {
    return 'biome';
  }

  // Consulta simples de estado
  if (
    lower.includes('desmatamento') ||
    lower.includes('área') ||
    lower.includes('quanto') ||
    lower.includes('qual')
  ) {
    return 'state';
  }

  return 'unknown';
}

/**
 * Parser principal - analisa query completa
 */
export function parseQuery(text: string): ParsedQuery {
  const type = detectQueryType(text);
  const state = extractState(text);
  const year = extractYear(text);
  const { yearStart, yearEnd } = extractYearRange(text);
  const limit = extractLimit(text);
  const biome = extractBiome(text);

  // Detectar ordem (crescente/decrescente)
  const lower = text.toLowerCase();
  const order: 'asc' | 'desc' =
    lower.includes('menos') || lower.includes('menor') ? 'asc' : 'desc';

  return {
    type,
    state,
    year: year || new Date().getFullYear(), // Fallback para ano atual
    yearStart,
    yearEnd,
    limit: limit || 5,
    order,
    biome,
  };
}

/**
 * Valida se a query tem informações suficientes
 */
export function validateQuery(parsed: ParsedQuery): {
  valid: boolean;
  error?: string;
} {
  switch (parsed.type) {
    case 'state':
      if (!parsed.state) {
        return {
          valid: false,
          error:
            'Não consegui identificar o estado. Por favor, especifique um estado brasileiro.',
        };
      }
      break;

    case 'compare':
      if (!parsed.state && !parsed.biome) {
        return {
          valid: false,
          error: 'Não consegui identificar o estado ou bioma para comparar.',
        };
      }
      if (!parsed.yearStart || !parsed.yearEnd) {
        return {
          valid: false,
          error:
            'Não consegui identificar o intervalo de anos. Use: "Compare PA entre 2020 e 2024"',
        };
      }
      if (parsed.yearEnd <= parsed.yearStart) {
        return {
          valid: false,
          error: 'O ano final deve ser maior que o ano inicial.',
        };
      }
      break;

    case 'ranking':
      // Ranking sempre válido (usa defaults)
      break;

    case 'unknown':
      return {
        valid: false,
        error:
          'Não entendi sua pergunta. Tente: "Desmatamento no Pará em 2024" ou "Ranking 2024"',
      };
  }

  return { valid: true };
}

/**
 * Formata nome do estado (sigla → nome completo)
 */
export function formatStateName(code: string): string {
  return STATE_MAP[code.toUpperCase()] || code;
}