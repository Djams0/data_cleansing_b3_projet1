# Importation des bibliothèques
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
    clients_clean["email"] = clients_clean["email"].apply(standariser_email)
    clients_clean["pays"] = clients_clean["pays"].apply(standariser_pays)
    clients_clean["telephone"] = clients_clean["telephone"].apply(standariser_telephone)

    # Vérifier et convertir les dates (AAAA-MM-JJ)
    if "naissance" in clients_clean.columns:
        clients_clean['naissance'] = pd.to_datetime(
            clients_clean['naissance'], errors='coerce'
        )
    
    # Supprimer les clients sans email ou sans téléphone
    clients_clean = clients_clean.dropna(subset=['email','telephone'])

    # Supprimer les doublons en gardant les clients les plus complets
    clients_clean['completude'] = clients_clean[['email','telephone','pays','naissance']].notna().sum(axis=1)
    clients_clean = clients_clean.sort_values('completude',ascending=False)
    clients_clean = clients_clean.drop_duplicates(subset=['nom','prenom','email'])
    
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
    sales_clean["order_date"] = sales_clean["order_date"].apply(standariser_date)
    # Vérifier que les montants sont positifs
    sales_clean["amount"] = sales_clean["amount"].apply(standariser_amount)
    sales_clean['currency'] = sales_clean['currency'].replace({'€':'EUR'}).fillna('EUR')
    
    # Supprimer les doublons (order_id + email client) en gardant les plus grosses ventes
    sales_clean = sales_clean.sort_values('amount', ascending=False).drop_duplicates(subset=['order_id','customer_email'])
    
    # Supprimer les ventes sans date ou sans email
    sales_clean = sales_clean.dropna(subset=['order_date','customer_email'])
    
    # Séparer les remboursements et ventes
    remboursement = sales_clean[sales_clean["amount"] < 0].copy()
    sales_clean = sales_clean[sales_clean["amount"] >= 0].copy()
   
    # Calculer le chiffre d'affaires total par jour
    CA = (sales_clean.dropna(subset=['order_date','customer_email'])
    .groupby(pd.Grouper(key='order_date', freq='D'))
    ['amount'].sum().reset_index(name='daily_revenue'))

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