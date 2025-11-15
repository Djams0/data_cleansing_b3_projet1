# 📙 Journal de Transformation – Projet Nettoyage de Données

Chaque transformation appliquée aux données est documentée ci-dessous.  
Les volumes indiqués proviennent de l’exécution du pipeline.

---

# 1. Clients (`raw/clients.csv` → `clean/clients_clean.csv`)

| Étape | Description | Colonnes affectées | Action | Lignes impactées |
|------|-------------|--------------------|--------|------------------|
| 1 | Conversion emails en minuscules | email | strip, lower | ~100% |
| 2 | Suppression espaces internes | email | regex `\s+` | faibles |
| 3 | Validation du format email | email | regex, invalid → NaN | ~2–5% |
| 4 | Normalisation pays | pays | mapping (fr→France…) | ~80% |
| 5 | Normalisation téléphone | telephone | extraction digits + format +33 | ~70% |
| 6 | Conversion dates naissance | naissance | `pd.to_datetime` | ~100% |
| 7 | Score de complétude | email/tel/pays/date | somme non-null | 100% |
| 8 | Déduplication | nom+prenom+email_clean | keep max completude | variable |
| 9 | Suppression clients invalides | email_clean & tel_clean NaN | suppression | ~1–3% |

Fichier anomalies : `reports/anomalies_clients.csv`

---

# 2. Ventes (`raw/sales.csv` → `clean/sales_clean.csv`)

| Étape | Description | Colonnes | Action | Impact |
|------|-------------|----------|--------|--------|
| 1 | Normalisation dates | order_date | `pd.to_datetime()` | ~100% |
| 2 | Nettoyage montants | amount | conversion en float | ~100% |
| 3 | Détection montants invalides | amount | invalid → NaN | faible |
| 4 | Normalisation devise | currency | €→EUR, $→USD | ~80% |
| 5 | Normalisation email client | customer_email | normalize_email | ~100% |
| 6 | Suppression lignes invalides | email/date/amount invalides | drop | ~3–5% |
| 7 | Déduplication | order_id + email | keep max amount | faible |
| 8 | Séparation remboursements | amount_clean < 0 | vers refunds.csv | faible |
| 9 | CA journalier | date + sum(amount_clean) | groupby | 100% |

Fichiers produits :
- `clean/sales_clean.csv`
- `clean/refunds.csv`
- `reports/anomalies_sales.csv`
- `reports/ventes_kpi_journalier.csv`

---

# 3. Catalogue FR/US (`raw/catalog_fr.csv`, `raw/catalog_us.csv` → `clean/catalog_canonique.csv`)

| Étape | Description | Colonnes | Action | Impact |
|------|-------------|----------|--------|--------|
| 1 | Conversion poids en kg | weight + weight_unit | g→kg, lb→kg, kg→kg | ~100% |
| 2 | Normalisation devise | currency | €→EUR, $→USD | ~90% |
| 3 | Normalisation catégories | category | mapping depuis mapping_categories.csv | ~90% |
| 4 | Fusion FR + US | datasets | concat | 100% |
| 5 | Score de complétude | name/poids/prix/devise/category | somme non-null | 100% |
| 6 | Déduplication | sku | keep max completude | faible |
| 7 | Détection anomalies | poids ou devise invalides | export CSV | faible |

Fichiers produits :
- `clean/catalog_canonique.csv`
- `reports/anomalies_catalog.csv`
- `reports/catalog_kpi.csv`

---

# 4. KPI Globaux générés
- clients_kpi.csv  
- sales_kpi.csv  
- catalog_kpi.csv  
- ventes_kpi_journalier.csv  

Ces fichiers montrent l’évolution **Avant/Après** des indicateurs.

---

# ✔️ Notes finales
- Toutes les transformations respectent le principe : **ne jamais modifier les fichiers bruts**.
- Tous les CSV nettoyés sont enregistrés dans `clean/`.
- Tous les KPI et anomalies sont documentés dans `reports/`.

