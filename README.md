# Plateforme d'Analyse des Données de Santé Mentale

Application web universitaire développée avec Streamlit pour importer, explorer, nettoyer, visualiser et exporter des données de santé mentale.

## Présentation

La plateforme permet d'analyser des datasets psychologiques et comportementaux contenant, par exemple, des variables comme l'âge, le genre, le niveau de stress, l'anxiété, la dépression, le sommeil, les heures de travail ou le traitement médical.

L'application est entièrement en français et pensée pour une présentation universitaire : interface moderne, cartes KPI, graphiques interactifs, gestion d'erreurs, historique des traitements et exports.

## Architecture

```text
mental-health-analytics-platform/
|-- app.py
|-- pages/
|   |-- accueil.py
|   |-- importation.py
|   |-- analyse.py
|   |-- preprocessing.py
|   |-- visualisations.py
|   |-- exportation.py
|   `-- apropos.py
|-- utils/
|   |-- data_loader.py
|   |-- statistiques.py
|   |-- preprocessing_utils.py
|   |-- visualisation_utils.py
|   |-- export_utils.py
|   `-- helpers.py
|-- data/
|   `-- exemple_sante_mentale.csv
|-- exports/
|-- assets/
|   `-- logo.svg
|-- requirements.txt
`-- README.md
```

## Technologies utilisées

- Python 3.12
- Streamlit
- Pandas
- NumPy
- Plotly
- Matplotlib
- OpenPyXL
- Statsmodels
- Kaleido

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

## Fonctionnalités

- Importation de fichiers CSV.
- Aperçu du dataset, dimensions, types, mémoire utilisée et doublons.
- Cartes KPI : patients, âge moyen, stress moyen, anxiété, dépression, lignes et colonnes.
- Statistiques : moyenne, médiane, mode, variance, écart-type, minimum, maximum et quartiles.
- Analyse des valeurs manquantes avec tableau et graphique.
- Analyse des doublons.
- Corrélations avec heatmap Plotly.
- Distributions : histogrammes, boxplots, densité, barres et diagrammes circulaires.
- Analyses spécifiques santé mentale :
  - répartition du stress ;
  - répartition de l'anxiété ;
  - répartition de la dépression ;
  - impact du sommeil sur le stress ;
  - impact des heures de travail sur le stress ;
  - comparaison par genre ;
  - analyse par tranche d'âge.
- Prétraitement :
  - suppression ou imputation des valeurs manquantes ;
  - suppression des doublons ;
  - détection et suppression des valeurs aberrantes par IQR ;
  - normalisation Min-Max ;
  - standardisation Z-Score ;
  - encodage One-Hot ;
  - renommage et changement de type ;
  - sélection de variables ;
  - recherche, filtres et tri.
- Comparaison dataset original / dataset nettoyé.
- Historique des traitements.
- Score de qualité du dataset et recommandations de nettoyage.
- Exports CSV, Excel, statistiques et rapport Markdown.
- Export HTML et PNG des graphiques lorsque Kaleido est disponible.

## Guide utilisateur

1. Ouvrir l'application avec `streamlit run app.py`.
2. Aller dans la page **Importation**.
3. Charger un fichier CSV de santé mentale.
4. Consulter les indicateurs de qualité et l'aperçu du dataset.
5. Utiliser **Analyse** pour explorer les tendances, corrélations et distributions.
6. Utiliser **Prétraitement** pour nettoyer les données.
7. Créer des graphiques personnalisés dans **Visualisations**.
8. Télécharger les résultats depuis **Exportation**.

## Gestion des erreurs

L'application utilise des validations et des blocs `try/except` pour éviter l'arrêt brutal de l'interface :

- vérification du format CSV ;
- gestion des encodages ;
- colonnes inexistantes ignorées automatiquement ;
- messages utilisateur explicites ;
- export PNG désactivé proprement si Kaleido n'est pas disponible.

## Captures d'écran

Section réservée aux captures d'écran de l'application pendant la soutenance.

## Préparation pour GitHub

Le dépôt contient uniquement les fichiers nécessaires à l'exécution et à la présentation du projet. Les fichiers temporaires, caches Python, environnements virtuels, exports générés et paramètres locaux sont exclus avec `.gitignore`.

## Perspectives d'amélioration

- Ajouter un modèle prédictif du risque de stress élevé.
- Ajouter une authentification utilisateur.
- Enregistrer les exports dans une base de données.
- Ajouter un rapport PDF automatique.
- Ajouter des tests unitaires sur les fonctions de nettoyage.
