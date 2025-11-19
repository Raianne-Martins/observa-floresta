import re
import unicodedata
from typing import Optional, Tuple


STATE_MAP = {
    "AC": "Acre", "AL": "Alagoas", "AP": "Amapá", "AM": "Amazonas",
    "BA": "Bahia", "CE": "Ceará", "DF": "Distrito Federal", "ES": "Espírito Santo",
    "GO": "Goiás", "MA": "Maranhão", "MT": "Mato Grosso", "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais", "PA": "Pará", "PB": "Paraíba", "PR": "Paraná",
    "PE": "Pernambuco", "PI": "Piauí", "RJ": "Rio de Janeiro", "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul", "RO": "Rondônia", "RR": "Roraima", "SC": "Santa Catarina",
    "SP": "São Paulo", "SE": "Sergipe", "TO": "Tocantins",
}

def _normalize_for_key(s: str) -> str:
    s = s.strip().upper()
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^A-Z0-9]", "", s)
    return s

STATE_NAME_TO_CODE = { _normalize_for_key(name): code for code, name in STATE_MAP.items() }

def resolve_state(user_input: str):
    """Resolve input de usuário para estado"""
    raw = user_input.strip()
    if len(raw) == 2 and raw.isalpha():
        code = raw.upper()
        if code in STATE_MAP:
            return {"name": STATE_MAP[code], "uf": code}
    key_norm = _normalize_for_key(raw)
    if key_norm in STATE_NAME_TO_CODE:
        code = STATE_NAME_TO_CODE[key_norm]
        return {"name": STATE_MAP[code], "uf": code}
    matches = [code for name_norm, code in STATE_NAME_TO_CODE.items() if name_norm.startswith(key_norm)]
    if len(matches) == 1:
        code = matches[0]
        return {"name": STATE_MAP[code], "uf": code}
    return None


def sanitize_state_or_biome(raw: str) -> str:
    if not raw:
        return ""
    cleaned = re.sub(r"\b(entre|de|comparar|em)\b", "", raw, flags=re.IGNORECASE)
    cleaned = cleaned.strip()

    resolved = resolve_state(cleaned)
    if resolved:
        return resolved["name"]

    normalized = cleaned.capitalize()
    if normalized in [
        "Amazônia", "Cerrado", "Caatinga", "Mata Atlantica",
        "Pantanal", "Pampa", "Brasil", "Brazil"
    ]:
        return normalized

    return cleaned

def parse_user_text(raw: str) -> Optional[dict]:
    """
    Extrai estado/bioma e ano(s) de uma frase natural do usuário.
    Exemplo:
    - "Quero os dados do desmatamento Pará 2024"
    - "Quero SP 2020-2024"
    """
    if not raw:
        return None

    text = raw.strip()

    years = re.findall(r"\b\d{4}\b", text)
    year_start, year_end = None, None
    if len(years) == 1:
        year_start = int(years[0])
        year_end = year_start
    elif len(years) >= 2:
        year_start = int(years[0])
        year_end = int(years[1])

    text_no_years = re.sub(r"\b\d{4}\b", "", text)
    text_no_years = text_no_years.strip()

    resolved = resolve_state(text_no_years)
    if resolved:
        return {
            "type": "state",
            "name": resolved["name"],
            "uf": resolved["uf"],
            "year_start": year_start,
            "year_end": year_end
        }

  
    normalized = text_no_years.capitalize()
    if normalized in ["Amazônia", "Cerrado", "Caatinga", "Mata Atlantica", "Pantanal", "Pampa", "Brasil", "Brazil"]:
        return {
            "type": "biome" if normalized != "Brasil" else "country",
            "name": normalized,
            "year_start": year_start,
            "year_end": year_end
        }

    return None

