# src/utils_cleaning.py
"""
Fonctions utilitaires de nettoyage (emails, téléphones, poids, devises, pays, catégories...)
"""

import re
import pandas as pd

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def normalize_email(email):
    """Nettoie et valide une adresse email. Retourne None si invalide."""
    if pd.isna(email):
        return None
    e = str(email).strip().lower()
    e = re.sub(r"\s+", "", e)  # enlever espaces internes
    if EMAIL_REGEX.match(e):
        return e
    return None

def normalize_country(country):
    """Normalise abréviations courantes en noms de pays français simples."""
    if pd.isna(country):
        return None
    c = str(country).strip().lower()
    mapping = {
        'fr':'France', 'france':'France', 'fr.':'France',
        'ch':'Suisse', 'ch.':'Suisse', 'suisse':'Suisse',
        'be':'Belgique', 'belgique':'Belgique',
        'us':'États-Unis', 'usa':'États-Unis', 'united states':'États-Unis',
    }
    return mapping.get(c, c.capitalize())

def normalize_phone_fr(phone):
    """
    Normalise un numéro français:
    - accepte '0642702383', '+33642702383', '06 42 70 23 83', '33642702383'
    - renvoie '+33XXXXXXXXX' ou None
    """
    if pd.isna(phone):
        return None
    s = re.sub(r"\D+", "", str(phone))
    if s.startswith('00') and len(s) > 2:
        s = s[2:]
    if s.startswith('33') and len(s) == 11:
        return '+' + s
    if len(s) == 10 and s.startswith('0'):
        return '+33' + s[1:]
    if len(s) == 9:  # rare: missing leading 0
        return '+33' + s
    return None

def convert_weight_to_kg(value, unit):
    """Convertit value/unit en kilogrammes (float) ou None."""
    try:
        if pd.isna(value) or pd.isna(unit):
            return None
        v = float(str(value).strip())
    except:
        return None
    u = str(unit).strip().lower()
    if u in ['kg','kgs','kilogram','kilogramme','kilogrammes']:
        return v
    if u in ['g','gr','gram','gramme','grammes']:
        return v / 1000.0
    if u in ['lb','lbs','pound','pounds']:
        return v * 0.45359237
    # si unité inconnue : essayer d'inférer selon l'ordre de grandeur
    if v > 1000:  # probablement g
        return v / 1000.0
    return None

def normalize_currency(cur):
    """Standardise les symboles / codes de devise en 'EUR' ou 'USD' ou original upper."""
    if pd.isna(cur):
        return None
    c = str(cur).strip()
    if c in ['€', 'eur', 'EUR', 'Eur']:
        return 'EUR'
    if c in ['$', 'usd', 'USD', 'Usd']:
        return 'USD'
    return c.upper()

def safe_to_datetime(s):
    """Wrapper pour pd.to_datetime avec errors='coerce'."""
    try:
        return pd.to_datetime(s, errors='coerce', dayfirst=False)
    except:
        return pd.NaT
