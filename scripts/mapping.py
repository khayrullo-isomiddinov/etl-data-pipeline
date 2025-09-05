


import re


_ALIASES = {
    "united states": "US", "usa": "US", "us": "US", "u.s.": "US", "u.s.a.": "US",
    "united kingdom": "GB", "uk": "GB", "great britain": "GB", "england": "GB",
    "germany": "DE", "deutschland": "DE",
    "hungary": "HU", "magyarorszag": "HU", "magyarország": "HU",
    "netherlands": "NL", "holland": "NL",
    "france": "FR",
    "spain": "ES", "españa": "ES", "espana": "ES",
    "italy": "IT", "italia": "IT",
    "czech republic": "CZ", "czechia": "CZ",
    "poland": "PL",
    "austria": "AT",
    "sweden": "SE",
    "norway": "NO",
    "denmark": "DK",
    "switzerland": "CH",
    "portugal": "PT",
    "ireland": "IE",
    "belgium": "BE",
    "romania": "RO",
    "bulgaria": "BG",
    "greece": "GR",
    "turkey": "TR", "türkiye": "TR", "turkiye": "TR",
    "russia": "RU", "russian federation": "RU",
    "ukraine": "UA",
    "belarus": "BY",
    "estonia": "EE", "latvia": "LV", "lithuania": "LT",
    "slovakia": "SK", "slovenia": "SI", "croatia": "HR", "serbia": "RS",
    "georgia": "GE",
    "azerbaijan": "AZ",
    "armenia": "AM",
    "kazakhstan": "KZ", "uzbekistan": "UZ", "kyrgyzstan": "KG", "tajikistan": "TJ", "turkmenistan": "TM",
    "china": "CN",
    "japan": "JP",
    "south korea": "KR", "republic of korea": "KR", "korea, republic of": "KR",
    "india": "IN",
    "pakistan": "PK",
    "bangladesh": "BD",
    "united arab emirates": "AE", "uae": "AE",
    "saudi arabia": "SA",
    "qatar": "QA",
    "kuwait": "KW",
    "bahrain": "BH",
    "oman": "OM",
    "egypt": "EG",
    "morocco": "MA",
    "tunisia": "TN",
    "algeria": "DZ",
    "south africa": "ZA",
    "australia": "AU",
    "new zealand": "NZ",
    "canada": "CA",
    "mexico": "MX",
    "brazil": "BR",
    "argentina": "AR",
    "chile": "CL",
    "peru": "PE",
    "colombia": "CO",
    "cote d'ivoire": "CI", "côte d’ivoire": "CI", "ivory coast": "CI",
    "hong kong": "HK", "singapore": "SG",
}


_ALPHA2 = set(_ALIASES.values())

def _norm(s: str) -> str:
    s = s.strip().lower()
    s = re.sub(r"[.\u2019’]", "'", s)   
    s = re.sub(r"[^a-z0-9+'\s,]", " ", s)  
    s = re.sub(r"\s+", " ", s)
    return s

def to_country_code(value: str) -> str | None:
    """
    Returns ISO alpha-2 (e.g., 'DE') or None if unknown.
    Accepts country names, common aliases, or already-a-code.
    """
    if not value:
        return None
    v = value.strip()
    
    if len(v) == 2 and v.isalpha():
        return v.upper()
    key = _norm(v)
    
    if key in _ALIASES:
        return _ALIASES[key]
    
    if "," in key:
        first = key.split(",", 1)[0].strip()
        if first in _ALIASES:
            return _ALIASES[first]
    
    if len(key) == 2 and key.isalpha():
        guess = key.upper()
        return guess if guess in _ALPHA2 else None
    return None
