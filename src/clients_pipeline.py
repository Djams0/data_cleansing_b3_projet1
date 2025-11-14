# Importation des bibliothèques
import pandas as pd
import numpy as np
import re

# Fonction pour nettoyer les emails
def standariser_email(email):

    # Vérifie si la variable est une chaîne de caractères
    if not isinstance(email, str):
        return None
    
    # Supprime les espaces avant/après et met tous les caractères en minuscules
    email = email.strip().lower()
    
    # Vérifie si l'email est au bon format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return None
    return email

# Fonction pour uniformiser les pays
def standariser_pays(pays):

    # Vérifie si la variable est une chaîne de caractères
    if not isinstance(pays, str):
        return None
    
    # Supprime les espaces avant/après et met tous les caractères en minuscules
    pays = pays.strip().lower()

    # Dictionnaire de correspondance pour les variations courantes
    pays_map = {
    "france": "France",
    "fr": "France",
    "allemagne": "Allemagne",
    "germany": "Allemagne",
    "etats-unis": "États-Unis",
    "usa": "États-Unis",
    "united states": "États-Unis",
    "royaume-uni": "Royaume-Uni",
    "uk": "Royaume-Uni",
    "united kingdom": "Royaume-Uni",
    "ch": "Chine",
    "be": "Belgique"
    }
    return pays_map.get(pays, pays.capitalize())

# Fonction pour mettre les numéros de téléphone en format international
def standariser_telephone(telephone):

    # Vérifie si la variable est une chaîne de caractères
    if not isinstance(telephone, str):
        return None

    # Supprime tous les caractères non numériques
    telephone_clean = re.sub(r'\D', '', telephone)
    
    # Vérifie la longueur standard d'un numéro français et retourne None
    # pour numéro non reconnaissable ou invalide
    if len(telephone_clean) in [9,10] and telephone_clean.startswith('0'):
        telephone_clean = '33' + telephone_clean[1:]
    elif len(telephone_clean) == 11 and telephone_clean.startswith('33'):
        pass
    else:
        return None
    return f"+{telephone_clean}"

# Fonction pour calculer les KPI
def kpi_quality(df):

    quality_metrics = {}

    # Calcul du taux de complétude par colonne
    completeness_by_column = (df.isnull().sum() / len(df) * 100).round(2)
    quality_metrics['completude_par_colonne'] = completeness_by_column.to_dict()

    # Calcul du taux de complétude global
    total_missing = df.isnull().sum().sum()
    total_cells = df.size
    global_completeness_rate = (1 - (total_missing / total_cells)) * 100
    quality_metrics['taux_completude_global'] = round(global_completeness_rate, 2)

    # Calcul du taux de doublons
    num_duplicates = df.duplicated().sum()
    duplicate_rate = (num_duplicates / len(df) * 100).round(2)
    quality_metrics['taux_doublons'] = duplicate_rate
    return quality_metrics
