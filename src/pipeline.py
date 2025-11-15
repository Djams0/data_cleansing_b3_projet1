# src/pipeline.py
"""
Script principal pour exécuter tous les pipelines :
- clients
- ventes (sales)
- catalogues (FR + US)

Usage:
    python src/pipeline.py
"""

import os
from clients_pipeline import clients_clean
from sales_pipeline import sales_clean
from catalog_pipeline import catalog_clean

# Créer dossiers de sortie s'ils n'existent pas
for d in ['./clean','./reports','./logs']:
    os.makedirs(d, exist_ok=True)

def main():
    print("=== Nettoyage clients ===")
    clients_out = clients_clean(input_path="./raw/clients.csv", output_clean="./clean/clients_clean.csv", reports_dir="./reports/")
    print("clients nettoyés:", len(clients_out))

    print("\n=== Nettoyage ventes ===")
    sales_out = sales_clean(input_path="./raw/sales.csv", output_clean="./clean/sales_clean.csv", reports_dir="./reports/", output_refunds="./clean/refunds.csv")
    print("ventes nettoyées:", len(sales_out))

    print("\n=== Nettoyage catalogues ===")
    catalog_out = catalog_clean(input_fr="./raw/catalog_fr.csv", input_us="./raw/catalog_us.csv", mapping="./raw/mapping_categories.csv", output_clean="./clean/catalog_canonique.csv", reports_dir="./reports/")
    print("catalogue canonique lignes:", len(catalog_out))

    print("\n=== FIN du pipeline ===")
    print("Fichiers produits dans ./clean et ./reports")

if __name__ == "__main__":
    main()
