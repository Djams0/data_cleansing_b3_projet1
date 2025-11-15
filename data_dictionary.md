# 📘 Dictionnaire de Données – Projet de Nettoyage

Ce dictionnaire décrit **toutes les colonnes finales produites dans `clean/`**, ainsi que leur type, leur origine et les règles de transformation appliquées.

---

# 1. Clients — `clean/clients_clean.csv`

| Colonne            | Type      | Description | Transformation appliquée | Exemple |
|-------------------|-----------|-------------|---------------------------|---------|
| id                | string    | Identifiant unique client | Copié depuis raw/clients.csv | 1 |
| nom               | string    | Nom du client | Copié, strip() | Dupont |
| prenom            | string    | Prénom du client | Copié, strip() | Jean |
| email_clean       | string    | Adresse email normalisée et validée | lowercase, suppression espaces, regex email, invalid → NaN | jean@mail.com |
| telephone_clean   | string    | Téléphone normalisé au format international | suppression caractères non numériques, conversion en +33 | +33642702383 |
| pays_clean        | string    | Pays normalisé | mapping (fr→France, ch→Suisse…) | France |
| naissance_clean   | datetime  | Date de naissance validée | `pd.to_datetime`, invalid → NaT | 1955-05-11 |
| completude        | int       | Score de complétude (0–4) | somme des colonnes non nulles | 4 |

---

# 2. Ventes — `clean/sales_clean.csv`

| Colonne            | Type      | Description | Transformation | Exemple |
|-------------------|-----------|-------------|----------------|---------|
| order_id          | string    | Identifiant de commande | Copié | O0000123 |
| order_date_clean  | datetime  | Date de commande normalisée | `pd.to_datetime()`, invalid → NaT | 2025-01-03 |
| customer_email    | string    | Email client normalisé | regex email | user1@mail.com |
| amount_clean      | float     | Montant numérique validé | conversion float, invalid → NaN | 2926.69 |
| currency_clean    | string    | Devise normalisée | €→EUR, $→USD | USD |
| channel           | string    | Canal d’achat | Copié | mobile |

### Fichiers séparés :
- `clean/refunds.csv` → remboursements (`amount_clean < 0`)

---

# 3. Catalogue — `clean/catalog_canonique.csv`

| Colonne        | Type   | Description | Transformation | Exemple |
|----------------|--------|-------------|----------------|---------|
| sku            | string | Identifiant produit unique | Copié | FR000123 |
| name           | string | Nom du produit | Copié | Webcam HD |
| category       | string | Catégorie standardisée | mapping depuis mapping_categories.csv | Vidéo |
| weight_kg      | float  | Poids converti en kilogrammes | g→kg, lb→kg, kg→kg | 1.300 |
| price          | float  | Prix brut | Converti en float | 1177.01 |
| currency_clean | string | Devise normalisée | €→EUR, $→USD | EUR |
| completude     | int    | Score de complétude | somme des champs non-nuls | 5 |

---

# 4. KPI — Rapports dans `reports/`

### Exemples de fichiers :
- `clients_kpi.csv`
- `sales_kpi.csv`
- `catalog_kpi.csv`
- `ventes_kpi_journalier.csv`

Ces fichiers contiennent les indicateurs suivants :
- taux de complétude global
- complétude par colonne
- nombre de doublons
- duplicate_rate
- nombre de lignes
- CA journalier (pour sales)

---

# 📝 Notes
- Tous les champs invalides (email, dates, unités inconnues) sont convertis en `NaN`/`NaT`.
- Aucun fichier brut n’est modifié.
- La logique de normalisation est décrite en détail dans `transformation_log.md`.
