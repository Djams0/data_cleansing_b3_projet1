# Projet : Qualité et Nettoyage des Données — Repo Git

Ce dépôt fournit un **processus reproductible pour nettoyer et contrôler la qualité** de trois jeux de données : *clients*, *produits*, *ventes*.  

Il contient le code Python, les jeux de données bruts, les sorties nettoyées, les KPI et rapports, ainsi que la documentation complète (dictionnaire des données et journal de transformation).

---

## Objectifs du projet

1. **Nettoyage des données** : identifier et corriger les anomalies, doublons et valeurs manquantes.  
2. **Création de jeux de données canoniques** pour analyses ultérieures.  
3. **Calcul et export des KPI** pour le suivi des ventes, clients et catalogue produits.  
4. **Documentation complète** : dictionnaire des données et journal des transformations appliquées.

---

## Arborescence du dépôt

```

data_cleansing_b3_projet1/
│── clean/
│   ├── clients_clean.csv
│   ├── catalog_canonique.csv
│   ├── refunds.csv
│   └── sales_clean.csv
├── raw/
│   ├── catalog_fr.csv
│   ├── catalog_us.csv
│   ├── clients.csv
│   ├── mapping_categories.csv
│   └── sales.csv
├── reports/
│   ├── anomalies_catalog.csv
│   ├── anomalies_clients.csv
│   ├── anomalies_sales.csv
│   ├── catalog_kpi.csv
│   ├── clients_kpi.csv
│   ├── ventes_kpi_journalier.csv
│   └── sales_kpi.csv
├── src/
│   ├── pipeline.py
│   ├── clients_pipeline.py
│   ├── catalog_pipeline.py
│   ├── utils_cleaning.py
│   ├── utils_kpi.py
│   └── sales_pipeline.py
├── data_dictionary.md
├── transformation_log.md
├── requirements.txt
└── README.md

````

---

## Prérequis

- Python 3.10+  
- pip installé  
- Windows, Mac ou Linux

---

## Installation

```bash
# créer un environnement virtuel
python -m venv .venv
# activer l'environnement
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate     # Windows
# installer les dépendances
pip install -r requirements.txt
````

---

## Exécution du pipeline

Le pipeline principal nettoie les données et génère les rapports :

```bash
python src/pipeline.py
```

**Options :**

* Chaque module (`clients_pipeline.py`, `catalog_pipeline.py`, `sales_pipeline.py`) peut être exécuté individuellement pour tester une partie du pipeline.

---

## Tests automatisés

```bash
pytest -v tests/
```
ou
```bash
C:\Python313\python.exe -m pytest -v
```

* `test_cleaning.py` : vérifie la qualité et l’intégrité des données nettoyées
* `test_kpi.py` : vérifie le calcul correct des KPI

---

## Livrables attendus

1. `clean/` : jeux de données nettoyés
2. `reports/` : anomalies et KPI
3. `data_dictionary.md` : dictionnaire des colonnes et types
4. `transformation_log.md` : journal des modifications appliquées
5. `src/` : code Python réutilisable

---


## Auteur

* menbres du groupe : **NDIAYE Mansour Djamil** & **ABDILLAHI ABDI Mariam Marwo**
* Email : [[mansourdjamil14@gmail.com](mailto:mansourdjamil14@gmail.com)]
* Projet réalisé dans le cadre de : **B3 — Data Quality & Cleaning**

