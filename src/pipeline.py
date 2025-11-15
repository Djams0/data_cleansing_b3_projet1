# Importation des bibliothèques et fonctions
import pandas as pd
from clients_pipeline import *
from sales_pipeline import *

# Fonctions pour les clients
def clients_clean():
    # Charger le fichier clients
    clients_clean = pd.read_csv("./raw/clients.csv", dtype={"telephone": str})
    
    # Calculer le KPI avant nettoyage
    kpi_avant = kpi_quality(clients_clean)
    
    # Standardiser email, pays et téléphone
    clients_clean["email_clean"] = clients_clean["email"].apply(standariser_email)
    clients_clean["pays_clean"] = clients_clean["pays"].apply(standariser_pays)
    clients_clean["telephone_clean"] = clients_clean["telephone"].apply(standariser_telephone)

    print("Emails invalides :", clients_clean["email"].isna().sum())
    print("Pays modifiés :", (clients_clean["pays"].str.lower() != clients_clean["pays_clean"].str.lower()).sum())
    print("Numéros invalides :", clients_clean["telephone"].isna().sum())

    # Vérifier et convertir les dates (AAAA-MM-JJ)
    if "naissance" in clients_clean.columns:
        clients_clean['naissance_clean'] = pd.to_datetime(
            clients_clean['naissance'], errors='coerce'
        )
    
    print("Dates invalides :", clients_clean['naissance'].isna().sum())

    # Supprimer les clients sans email et sans téléphone
    clients_clean = clients_clean[clients_clean['email_clean'].notna() | clients_clean['telephone_clean'].notna()]

    # Supprimer les doublons en gardant les clients les plus complets
    clients_clean['completude'] = clients_clean[['email_clean','telephone_clean','pays_clean','naissance']].notna().sum(axis=1)
    clients_clean = clients_clean.sort_values('completude',ascending=False)
    clients_clean = clients_clean.drop_duplicates(subset=['nom','prenom','email_clean'])
   
    # Supprimer les colonnes originales
    clients_clean = clients_clean[[
    "id", "nom", "prenom",
    "email_clean", "telephone_clean",
    "pays_clean", "naissance_clean", 
    "completude"
    ]]

    # Calculer le KPI après nettoyage
    kpi_apres = kpi_quality(clients_clean)
   
    # Sauvegarder le KPI dans un fichier CSV
    clients_kpi = pd.DataFrame([kpi_avant, kpi_apres], index=['Avant', 'Apres'])
    clients_kpi.to_csv('./reports/kpi_qualite.csv')

    # Sauvegarder le fichier clients nettoyé
    clients_clean.to_csv("./clean/clients_clean.csv", index=False)
    return clients_clean

# Fonctions pour les ventes et remboursements
def sales_clean():
    # Charger le fichier ventes
    sales_clean = pd.read_csv("./raw/sales.csv")

    # Calculer le KPI avant nettoyage
    kpi_avant = kpi_quality(sales_clean) 

    # Standardiser order_dates, amount et devise
    # Mettre les dates au format ISO
    sales_clean["order_date_clean"] = sales_clean["order_date"].apply(standariser_date)
    # Vérifier que les montants sont positifs
    sales_clean["amount_clean"] = sales_clean["amount"].apply(standariser_amount)
    sales_clean['currency_clean'] = sales_clean['currency'].replace({'€':'EUR'})

    print("Devise en € :", (sales_clean['currency'] == '€').sum())
    print("Dates invalides :", sales_clean["order_date"].isna().sum())
  
    # Supprimer les doublons (order_id + email client) en gardant les plus grosses ventes
    sales_clean = sales_clean.sort_values('amount_clean', ascending=False).drop_duplicates(subset=['order_id','customer_email'])

    # Supprimer les ventes sans email
    sales_clean = sales_clean.dropna(subset=['customer_email'])

    # Séparer les remboursements et ventes
    remboursement = sales_clean[sales_clean["amount_clean"] < 0].copy()
    sales_clean = sales_clean[sales_clean["amount_clean"] >= 0].copy()

    print("Montants positif :", len(sales_clean))
    print("Montants négatif :", len(remboursement))
     
    # Calculer le chiffre d'affaires total par jour
    CA = (sales_clean.dropna(subset=['order_date_clean','amount_clean'])
    .groupby(pd.Grouper(key='order_date_clean', freq='D'))
    ['amount_clean'].sum().reset_index(name='daily_revenue'))

    print("Nombre de jours avec CA :", CA.shape[0])

    # Supprimer les colonnes originales
    sales_clean = sales_clean[[
     "order_id","order_date_clean","customer_email",
     "amount_clean","currency_clean","channel"
    ]]
    
    # Calculer le KPI après nettoyage
    kpi_apres = kpi_quality(sales_clean)

    # Sauvegarder le KPI des ventes et le chiffre d'affaires dans un fichier CSV
    sales_kpi = pd.DataFrame([kpi_avant, kpi_apres], index=['Avant', 'Apres'])
    sales_kpi.to_csv("./reports/sales_kpi.csv", index=False)
    CA.to_csv("./reports/daily_revenue.csv", index=False)
    
    # Sauvegarder les fichiers nettoyés 
    sales_clean.to_csv("./clean/sales_clean.csv", index=False)
    remboursement.to_csv("./clean/refunds.csv", index=False)

    return sales_clean

# Exécution des fonctions
df_clean = clients_clean()
df_clean = sales_clean()