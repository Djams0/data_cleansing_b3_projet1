# src/utils_kpi.py
"""
Fonctions pour calculer et sauvegarder KPI de qualité.
"""

import pandas as pd
import numpy as np

def kpi_quality(df):
    """
    Retourne un dict de KPI :
    - global_completeness_rate (pour toutes les cellules)
    - completeness_per_column (dict)
    - duplicate_rate (en %)
    - num_rows
    """
    n = len(df)
    total_cells = df.size
    total_missing = df.isnull().sum().sum()
    global_completeness_rate = round((1 - (total_missing / total_cells)) * 100, 2) if total_cells > 0 else None
    completeness_by_column = ((1 - df.isnull().sum() / n) * 100).round(2).to_dict() if n > 0 else {}
    num_duplicates = df.duplicated().sum()
    duplicate_rate = round(num_duplicates / n * 100, 2) if n > 0 else None
    return {
        'num_rows': n,
        'global_completeness_rate': global_completeness_rate,
        'completeness_per_column': completeness_by_column,
        'num_duplicates': int(num_duplicates),
        'duplicate_rate_pct': duplicate_rate
    }

def kpi_dicts_to_dataframe(before_dict, after_dict):
    """
    Convertit deux dicts KPI en DataFrame lisible (Avant/Apres).
    """
    rows = []
    rows.append({'stage':'Avant','num_rows': before_dict.get('num_rows'), 'global_completeness_rate': before_dict.get('global_completeness_rate'), 'num_duplicates': before_dict.get('num_duplicates'), 'duplicate_rate_pct': before_dict.get('duplicate_rate_pct')})
    rows.append({'stage':'Apres','num_rows': after_dict.get('num_rows'), 'global_completeness_rate': after_dict.get('global_completeness_rate'), 'num_duplicates': after_dict.get('num_duplicates'), 'duplicate_rate_pct': after_dict.get('duplicate_rate_pct')})
    return pd.DataFrame(rows)
