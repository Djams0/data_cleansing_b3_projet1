# Mini Projet 1

## Colonnes du fichier clients_clean.csv

| Colonne            | Type      | Description                     |Contraintes/Correspondances               |
|------------------- | --------- | ------------------------------- | ---------------------------------------- |
| nom                | string    | Nom du client                   | -                                        |
| prenom             | string    | Prénom du client                | -                                        |
| email_clean        | string    | Email nettoyé et validé         | Format valide (xxx@yyy.zz), email non valides → None           |
| pays_clean         | string    | Pays standardisé                | fr, FR, fr, Fr, france -> France ; ch -> Chine ; be -> Belgique |
| telephone_clean    | string    | Téléphone normalisé (+33...)    | Format international                     |
| naissance_clean    | date      | Date au format ISO AAAA-MM-JJ   | -                                        |
| completude         | int       | Score de complétude de la ligne | Somme des colonnes non nulles            |

# Mini Projet 2

# Mini Projet 3

## Colonnes du fichier sales_clean.csv

| Colonne        | Type   | Description                       | Contraintes/Correspondances                |
|--------------- | ------ | --------------------------------- | ------------------------------------------ |
| order_id       | string | Identifiant unique de commande    | -                                          |
| customer_email | string | Email du client nettoyé et validé | Emails invalides supprimés                 |
| order_date_clean| date   | Date normalisée (ISO AAAA-MM-JJ)  | -                                          |
| amount_clean   | float  | Montant nettoyé                   | Montants négatifs séparés dans refunds.csv |
| currency_clean | string | Devise                            | € → EUR                                    |
| channel        | string | Canal de vente                    | -                                          |


## Colonnes du fichier refunds.csv
Même structure que sales_clean.csv mais `amount_clean < 0`.

## Colonnes du fichier daily_revenue.csv

| Colonne       | Type  | Description                        |
| ------------- | ----- | ---------------------------------- |
| order_date    | date  | Date de la commande                |
| daily_revenue | float | Total des ventes positives du jour |
