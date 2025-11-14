import pandas as pd
import numpy as np
import re

#emails
def standariser_email(email):

    if not isinstance(email, str):
        return None

    email = email.strip().lower()

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return None
    return email

#pays
def standariser_pays(pays):

    if not isinstance(pays, str):
        return None

    pays = pays.strip().lower()

    pays_map = {
    "france": "France",
    "fr": "France",
    "allemagne": "Allemagne",
    "germany": "Allemagne",
    "etats-unis": "États-Unis",
    "usa": "États-Unis",
    "united states": "États-Unis",
    "royaume-uni": "Royaume-Uni",
    "uk": "Royaume-Uni",
    "united kingdom": "Royaume-Uni",
    "ch": "Chine",
    "be": "Belgique"
    }
    return pays_map.get(pays, pays.capitalize())

#téléphones
def standariser_telephone(telephone):

    if not isinstance(telephone, str):
        return None

    telephone_clean = re.sub(r'\D', '', telephone)

    if len(telephone_clean) in [9,10] and telephone_clean.startswith('0'):
        telephone_clean = '33' + telephone_clean[1:]
    elif len(telephone_clean) == 11 and telephone_clean.startswith('33'):
        pass
    else:
        return None
    return f"+{telephone_clean}"

#kpi
def kpi_quality(df):

    quality_metrics = {}

    # Calcul du taux de complétude par colonne
    completeness_by_column = (df.isnull().sum() / len(df) * 100).round(2)
    quality_metrics['completeness_per_column'] = completeness_by_column.to_dict()

    # Calcul du taux de complétude global
    total_missing = df.isnull().sum().sum()
    total_cells = df.size
    global_completeness_rate = (1 - (total_missing / total_cells)) * 100
    quality_metrics['global_completeness_rate'] = round(global_completeness_rate, 2)

    # Calcul du taux de doublons
    num_duplicates = df.duplicated().sum()
    duplicate_rate = (num_duplicates / len(df) * 100).round(2)
    quality_metrics['duplicate_rate'] = duplicate_rate
    return quality_metrics
