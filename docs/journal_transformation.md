# Mini Projet 1

### 1. Nettoyage des emails
- Règle appliquée : standardisation des emails:
  - Suppression des espaces avant/après
  - Conversion en minuscules
  - Validation du format xxx@yyy.zz
- Volume : 2503 emails invalides.
- Exceptions : emails invalides remplacés par None.

### 2. Standardisation des pays
- Règle appliquée : standardisation avec dictionnaire de correspondance (fr -> France, bl -> Belgique, etc.).
- Volume : 33452 pays modifiés.
- Exceptions : aucune.

### 3. Standardisation des téléphones
- Règle appliquée : standardisation des numéros:
  - Suppression des caractères non numériques
  - Conversion vers format international (+33...)
- Volume : 4907 numéros invalides.
- Exceptions : Numéros invalides remplacés par None.

### 4.Conversion des dates de naissance
- Règle appliquée : conversion avec pd.to_datetime en format ISO (naissance_clean).
- Volume : 0 dates invalides.
- Exceptions : aucune.

### 5. Suppression des doublons
- Règle appliquée : suppression des doublons basés sur nom + prénom + email_clean
- Volume : 0 doublons supprimés.
- Exceptions : aucune.

# Mini Projet 2

# Mini Projet 3

### 1. Conversion des dates
- Règle appliquée : conversion avec pd.to_datetime en format ISO (order_date_clean).
- Volume : 0 dates invalides.
- Exceptions : aucune.

### 2. Vérification et conversion des montants
- Règle appliquée : conversion de amount en numérique (amount_clean) avec pd.to_numeric.
- Volume : 186875 montants positif.
- Exceptions : aucune.

### 3. Séparation des remboursements
- Règle appliquée : toutes les lignes avec amount_clean < 0 sont séparées dans refunds.csv.
- Volume : 3154 montants négatifs.
- Exceptions : aucune.

### 4. Calcul du chiffre d’affaires quotidien
- Règle appliquée : agrégation par order_date_clean et pour calculer le CA total par jour (daily_revenue.csv).
- Volume : 31 jours de chiffre d’affaires calculés par jour.
- Exceptions : aucune.

### 5. Suppression des doublons
- Règle appliquée : suppression des doublons order_id et customer_email.
- Volume : 0 doublons supprimés.
- Exceptions : aucune.

