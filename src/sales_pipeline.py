# src/sales_pipeline.py
"""
Pipeline de nettoyage pour ventes.
"""

import pandas as pd
from utils_cleaning import normalize_email, normalize_currency, safe_to_datetime
from utils_kpi import kpi_quality, kpi_dicts_to_dataframe
import numpy as np

def standartize_amount(val):
    if pd.isna(val):
        return np.nan
    try:
        return float(str(val).replace(',','').strip())
    except:
        return np.nan

def sales_clean(input_path="./raw/sales.csv", output_clean="./clean/sales_clean.csv", reports_dir="./reports/", output_refunds="./clean/refunds.csv"):
    df = pd.read_csv(input_path, dtype=str)

    # KPI avant
    kpi_before = kpi_quality(df)

    # Normalisations
    df['order_date_clean'] = df.get('order_date').apply(safe_to_datetime)
    df['amount_clean'] = df.get('amount').apply(standartize_amount)
    df['currency_clean'] = df.get('currency').apply(normalize_currency)
    df['customer_email_clean'] = df.get('customer_email').apply(normalize_email)

    # Anomalies : lignes sans email ou sans date ou sans montant
    anomalies = df[ df['customer_email_clean'].isna() | df['order_date_clean'].isna() | df['amount_clean'].isna() ].copy()
    anomalies.to_csv(f"{reports_dir}anomalies_sales.csv", index=False)

    # Supprimer ventes sans email ou sans montant valide
    df = df[ df['customer_email_clean'].notna() & df['amount_clean'].notna() ].copy()

    # Dedup : garder la ligne avec le montant le plus élevé
    df = df.sort_values('amount_clean', ascending=False)
    df = df.drop_duplicates(subset=['order_id','customer_email_clean'], keep='first')

    # Séparer remboursements
    refunds = df[ df['amount_clean'] < 0 ].copy()
    sales = df[ df['amount_clean'] >= 0 ].copy()

    # Calcul CA journalier (par date)
    sales = sales.dropna(subset=['order_date_clean'])
    sales['order_date_only'] = sales['order_date_clean'].dt.date
    daily_revenue = sales.groupby('order_date_only')['amount_clean'].sum().reset_index(name='daily_revenue')

    # Colonnes finales
    sales_out = sales[['order_id','order_date_clean','customer_email_clean','amount_clean','currency_clean','channel']].copy()
    sales_out.rename(columns={'customer_email_clean':'customer_email'}, inplace=True)

    # KPI après
    kpi_after = kpi_quality(sales_out)
    kpi_df = kpi_dicts_to_dataframe(kpi_before, kpi_after)
    kpi_df.to_csv(f"{reports_dir}sales_kpi.csv", index=False)
    daily_revenue.to_csv(f"{reports_dir}ventes_kpi_journalier.csv", index=False)

    # Sauvegarde
    sales_out.to_csv(output_clean, index=False)
    refunds.to_csv(output_refunds, index=False)

    return sales_out
