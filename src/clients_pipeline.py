# src/clients_pipeline.py
"""
Pipeline de nettoyage pour clients.
Utilise utils_cleaning et utils_kpi.
"""

import pandas as pd
from utils_cleaning import normalize_email, normalize_country, normalize_phone_fr, safe_to_datetime
from utils_kpi import kpi_quality, kpi_dicts_to_dataframe

def clients_clean(input_path="./raw/clients.csv", output_clean="./clean/clients_clean.csv", reports_dir="./reports/"):
    df = pd.read_csv(input_path, dtype=str)
    
    # KPI avant
    kpi_before = kpi_quality(df)

    # Nettoyages
    df['email_clean'] = df.get('email').apply(normalize_email)
    df['pays_clean'] = df.get('pays').apply(normalize_country)
    df['telephone_clean'] = df.get('telephone').apply(normalize_phone_fr)
    if 'naissance' in df.columns:
        df['naissance_clean'] = df['naissance'].apply(safe_to_datetime)

    # Indicateurs / anomalies
    anomalies = df[
        df['email_clean'].isna() & df['telephone_clean'].isna()
    ].copy()
    anomalies.to_csv(f"{reports_dir}anomalies_clients.csv", index=False)

    # Supprimer lignes sans email ni téléphone
    df = df[ df['email_clean'].notna() | df['telephone_clean'].notna() ].copy()

    # Complétude et fusion doublons (garder la ligne la plus complète)
    df['completude'] = df[['email_clean','telephone_clean','pays_clean','naissance_clean']].notna().sum(axis=1)
    df = df.sort_values('completude', ascending=False)
    df = df.drop_duplicates(subset=['nom','prenom','email_clean'], keep='first')

    # Colonnes finales
    out_cols = ['id','nom','prenom','email_clean','telephone_clean','pays_clean','naissance_clean','completude']
    for c in out_cols:
        if c not in df.columns:
            df[c] = None
    df_out = df[out_cols].copy()

    # KPI après
    kpi_after = kpi_quality(df_out)
    kpi_df = kpi_dicts_to_dataframe(kpi_before, kpi_after)
    kpi_df.to_csv(f"{reports_dir}clients_kpi.csv", index=False)

    # Sauvegarde
    df_out.to_csv(output_clean, index=False)
    return df_out
