# Importation des bibliothèques
import pandas as pd
import re

# Fonction pour uniformiser les dates au format ISO (AAAA-MM-JJ)
def standariser_date(dates):
    # Convertit la valeur en datetime, remplace les valeurs invalides par NaT
    dt = pd.to_datetime(dates, errors='coerce')
    return dt

# Fonction pour vérifier et convertir les montants
def standariser_amount(amount):
    # Convertit en numérique, remplace les valeurs invalides par NaN
    return pd.to_numeric(amount,errors='coerce')

