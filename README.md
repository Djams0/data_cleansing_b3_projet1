# Projet : Qualité et Nettoyage des Données — Repo Git

Ce document sert de **README principal** et contient :

* structure recommandée du dépôt Git
* fichiers et modèles de code (extraits)
* instructions d'exécution
* dictionnaire de données (template)
* journal de transformation (template)
* guide pour le tableau de bord KPI

> **But du dépôt** : fournir un processus reproductible pour nettoyer et contrôler la qualité de trois jeux de données : *clients*, *produits*, *ventes*. Livrables : code, raw/, clean/, reports/, README.md, dictionnaire, journal, dashboard.

---

## Arborescence recommandée (à committer)

```
data-quality-project/
├── data/
│   ├── raw/
│   │   ├── clients.csv
│   │   ├── produits.csv
│   │   └── ventes.csv
│   ├── clean/
│   │   ├── clients_clean.csv
│   │   ├── produits_clean.csv
│   │   └── ventes_clean.csv
│   └── reports/
│       ├── kpi_quality_before_after.csv
│       └── daily_revenue.csv
├── src/
│   ├── pipeline.py
│   ├── utils_cleaning.py
│   ├── clients_pipeline.py
│   ├── produits_pipeline.py
│   └── ventes_pipeline.py
├── docs/
│   ├── data_dictionary.md
│   └── transformation_log.md
├── dashboards/
│   └── kpi_dashboard.pbix (Power BI) or notebooks for matplotlib
├── requirements.txt
└── README.md
```

---


## Rédaction du rendu à remettre (checklist)

* [ ] `src/` : code propre, functions réutilisables
* [ ] `data/raw/` : jeux d'origine (CSV)
* [ ] `data/clean/` : sorties nettoyées
* [ ] `data/reports/` : KPI et rapports
* [ ] `docs/data_dictionary.md` complété
* [ ] `docs/transformation_log.md` complété
* [ ] `README.md` (mode d'emploi) — ce document
* [ ] Optionnel : notebooks et dashboard

---

## Commandes d'exécution rapides

```bash
# créer venv
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
pip install -r requirements.txt

# lancer le pipeline principal
python src/pipeline.py

# lancer pipeline clients séparément
python src/clients_pipeline.py
```