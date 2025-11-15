# src/catalog_pipeline.py
"""
Pipeline de nettoyage pour catalogues FR + US, fusion en catalog_canonique.csv
"""

import pandas as pd
from utils_cleaning import convert_weight_to_kg, normalize_currency
from utils_kpi import kpi_quality, kpi_dicts_to_dataframe

def catalog_clean(input_fr="./raw/catalog_fr.csv", input_us="./raw/catalog_us.csv", mapping="./raw/mapping_categories.csv", output_clean="./clean/catalog_canonique.csv", reports_dir="./reports/"):
    # Lire fichiers
    df_fr = pd.read_csv(input_fr, dtype=str)
    df_us = pd.read_csv(input_us, dtype=str)
    mapping = pd.read_csv(mapping) if mapping is not None else pd.DataFrame(columns=['source_category','target_category'])
    map_dict = dict(zip(mapping['source_category'].astype(str), mapping['target_category'].astype(str)))

    # KPI avant (concatené)
    kpi_before = kpi_quality(pd.concat([df_fr, df_us], ignore_index=True))

    # Standardisations FR
    for df in [df_fr, df_us]:
        # poids -> float
        df['weight_kg'] = df.apply(lambda r: convert_weight_to_kg(r.get('weight'), r.get('weight_unit')), axis=1)
        # currency
        df['currency_clean'] = df.get('currency').apply(normalize_currency)
        # categories mapping
        df['category_clean'] = df.get('category').map(map_dict).fillna(df.get('category').astype(str).str.capitalize())

    # Fusion
    df = pd.concat([df_fr, df_us], ignore_index=True)

    # Détection anomalies
    anomalies = df[ df['weight_kg'].isna() | df['currency_clean'].isna() ].copy()
    anomalies.to_csv(f"{reports_dir}anomalies_catalog.csv", index=False)

    # Supprimer lignes sans SKU ou sans name
    if 'sku' in df.columns:
        df = df[ df['sku'].notna() ]
    df = df[ df['name'].notna() ]

    # Complétude et déduplication : garder ligne la plus complète par sku
    df['completude'] = df[['name','weight_kg','price','currency_clean','category_clean']].notna().sum(axis=1)
    df = df.sort_values('completude', ascending=False)
    df = df.drop_duplicates(subset=['sku'], keep='first')

    # Colonnes finales
    out_cols = ['sku','name','category_clean','weight_kg','price','currency_clean','completude']
    for c in out_cols:
        if c not in df.columns:
            df[c] = None
    df_out = df[out_cols].copy()
    df_out.rename(columns={'category_clean':'category'}, inplace=True)

    # KPI après
    kpi_after = kpi_quality(df_out)
    kpi_df = kpi_dicts_to_dataframe(kpi_before, kpi_after)
    kpi_df.to_csv(f"{reports_dir}catalog_kpi.csv", index=False)

    # Sauvegarde
    df_out.to_csv(output_clean, index=False)
    return df_out
