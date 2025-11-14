import pandas as pd
from clients_pipeline import *
from sales_pipeline import *

# fonctions clients
def clients_clean():
    #charger le fichier
    clients_clean = pd.read_csv("./raw/clients.csv", dtype={"telephone": str})
    
    #kpi avant
    kpi_avant = kpi_quality(clients_clean)
    
    #standariser
    clients_clean["email"] = clients_clean["email"].apply(standariser_email)
    clients_clean["pays"] = clients_clean["pays"].apply(standariser_pays)
    clients_clean["telephone"] = clients_clean["telephone"].apply(standariser_telephone)

    #date
    if "naissance" in clients_clean.columns:
        clients_clean['naissance'] = pd.to_datetime(
            clients_clean['naissance'], errors='coerce'
        )
    
    #supprimer les commandes sans date et sans email
    clients_clean = clients_clean.dropna(subset=['email','telephone'])

    #supprimer les doublons
    clients_clean['completude'] = clients_clean[['email','telephone','pays','naissance']].notna().sum(axis=1)
    clients_clean = clients_clean.sort_values('completude',ascending=False)
    clients_clean = clients_clean.drop_duplicates(subset=['nom','prenom','email'])
    
    #kpi apres
    kpi_apres = kpi_quality(clients_clean)
    
    #Sauvegarde du kpi
    clients_kpi = pd.DataFrame([kpi_avant, kpi_apres], index=['Avant', 'Apres'])
    clients_kpi.to_csv('./reports/kpi_qualite.csv')

    #Sauvegarde du fichier clean
    clients_clean.to_csv("./clean/clients_clean.csv", index=False)
    return clients_clean

# fonctiosn sales et refunds
def sales_clean():

    #charger le fichier
    sales_clean = pd.read_csv("./raw/sales.csv")

    #kpi avant
    kpi_avant = kpi_quality(sales_clean) 

    #date au format ISO
    sales_clean["order_date"] = sales_clean["order_date"].apply(normaliser_date)

    #montant positifs
    sales_clean["amount"] = sales_clean["amount"].apply(normaliser_amount)
    print((sales_clean['amount'] > 0).sum())

    # Standardiser devise
    sales_clean['currency'] = sales_clean['currency'].replace({'€':'EUR'}).fillna('EUR')
    
    #separations
    remboursement = sales_clean[sales_clean["amount"] < 0].copy()
    sales_clean = sales_clean[sales_clean["amount"] >= 0].copy()

    #supprimer les doublons
    sales_clean = sales_clean.sort_values('amount', ascending=False).drop_duplicates(subset=['order_id','customer_email'])
    
    #supprimer les commandes sans date et sans email
    sales_clean = sales_clean.dropna(subset=['order_date','customer_email'])

    #kpi apres
    kpi_apres = kpi_quality(sales_clean)

    #Sauvegarde du kpi
    sales_kpi = pd.DataFrame([kpi_avant, kpi_apres], index=['Avant', 'Apres'])
    sales_kpi.to_csv("./reports/sales_kpi.csv", index=False)
    
    #Sauvegarde du fichier clean et remboursement
    sales_clean.to_csv("./clean/sales_clean.csv", index=False)
    remboursement.to_csv("./clean/refunds.csv", index=False)

    return sales_clean

df_clean = clients_clean()
df_clean = sales_clean()