# 1. Application d'analyse et prédiction du risque d'AVC chez différentes catégories de patients

Ce projet est une application web complète développée en Python (Flask), permettant de :

- Gérer une base de données de patients ayant eu un AVC (Accident Vasculaire Cérébral)
- Analyser et nettoyer un dataset public (données santé AVC) téléchargé depuis la plateforme Kaggle
- Visualiser les informations concernant les patients sous forme de tableau interactif
- Explorer les données grâce à des graphiques interactifs (âge, genre, glucose, IMC, etc.)
- Filtrer les patients selon plusieurs critères (genre, âge, type de travail, résidence)
- Exporter les résultats filtrés en CSV et PDF
- Ajouter, modifier ou supprimer des patients
- Connecter et insérer les données dans une base PostgreSQL (gestion via pgAdmin)
- Introduire une modélisation prédictive (Machine Learning) pour estimer le risque d’AVC

L'application web est développée avec Flask et connectée à PostgreSQL.  
L'analyse exploratoire et les visualisations sont réalisées dans un notebook Jupyter.  
Le design est modernisé avec Bootstrap pour une interface claire et responsive.

# 2. Objectif

L'objectif principal de ce projet est avant tout l'analyse d'un dataset médical 
Analyser un dataset médical (AVC - Accidents Vasculaires Cérébraux) intitulé **healthcare-dataset-stroke-data.csv** et créer une **application web** qui a pour but de :
- Analyse les données issues du Dataset téléchargé sous Jupyter (Nettoyage, Visualisation)
- Stockage des données dans une base PostgreSQL
- Interface web avec Flask (Ajout, Filtrage, Export CSV/PDF)
- Visualisations avec Seaborn et Matplotlib

# 3. Structure du projet

stroke-project/
│
├── app_flask/ # Application Flask (fichiers Python et templates HTML)
│ ├── projet.py # Fichier principal Flask (routes, logique web)
│ ├── templates/ # Fichiers HTML (index, ajout, modification)
│ │ ├── index.html
│ │ ├── add_patient.html
│ │ └── edit_patient.html
│
├── Data/ # Données sources (healthcare-dataset-stroke-data.csv)
│
├── notebooks/ # Notebook Jupyter (nettoyage, visualisation, ML)
│ └── Untitled7.ipynb
│
├── screenshoots/ # Captures d'écran pour illustrer l'application et les visualisations
│ ├── index.png
│ ├── Ajout_patient.png
│ ├── Edit.png
│ ├── AVC-genre-age.PNG
│ ├── Tabagisme.png
│ ├── type-de-travail.png
│ ├── relationGlucoseIMCAVG.PNG
│ └── MatriceDeConfusion.png
│
├── requirements.txt # Liste des dépendances Python
└── README.md # Documentation du projet (ce fichier)
# 4. Technologies utilisées

- **Python** 
- **Flask** — Framework web léger pour le backend
- **PostgreSQL** — Base de données relationnelle
- **pgAdmin** — Interface graphique pour gérer PostgreSQL
- **Pandas** — Nettoyage et manipulation des données
- **Seaborn & Matplotlib** — Visualisations statistiques et exploratoires
- **Scikit-learn** — Modélisation prédictive (classification du risque d'AVC)
- **FPDF** — Génération de rapports PDF
- **Jupyter Notebook** — Analyse exploratoire et prototypage
- **HTML & Jinja2** — Templates dynamiques pour l'interface web
- **Bootstrap** — Stylisation et design responsive
- **Kaggle** — Source du dataset utilisé

# 5. Installation et exécution

## Prérequis

- Python 3.13.2
- PostgreSQL installé et configuré (via pgAdmin)
- Dataset téléchargé depuis Kaggle (`healthcare-dataset-stroke-data.csv`)

## Installation


# Cloner le dépôt
git clone https://github.com/Massilia2001/ProjectAvc.git
cd stroke-project

# Installer les dépendances
pip install -r requirements.txt

# Configuration de la base PostgreSQL

    Créer une base stroke_db via pgAdmin

    Créer la table patients avec la structure définie dans le notebook ou dans le code Flask

# Lancer l'application Flask
python app_flask/projet.py

# Notebook

Pour explorer les visualisations et effectuer l'analyse exploratoire :

    Ouvrir le fichier notebooks/Untitled7.ipynb

    Exécuter toutes les cellules dans Jupyter
# 6. Aperçu et captures d'écran

Voici quelques captures d'écran de l'application pour illustrer son interface et ses fonctionnalités :

## Interface principale (tableau des patients)

![Tableau des patients](screenshoots/index.png)

## Formulaire d'ajout d'un patient

![Ajout patient](screenshoots/Ajout_patient.png)

## Formulaire de modification d'un patient

![Modification patient](screenshoots/Edit.png)

##  Notebook (Les visualisations)


Voici quelques exemples de visualisations générées dans le notebook :

### Distribution des AVC par genre et Boxplot de l'âge selon AVC

![Genre AVC et Âge AVC](screenshoots/AVC-genre-age.PNG)

### Statut tabagique et AVC

![Tabac AVC](screenshoots/Tabagisme.png)

### Type de travail et AVC

![Travail AVC](screenshoots/type-de-travail.png)

### Relation glucose/IMC/AVC

![Glucose IMC AVC](screenshoots/relationGlucoseIMCAVG.PNG)

### Matrice de confusion

![Matrice de confusion](screenshoots/MatriceDeConfusion.png)

 **D'autres visualisations et analyses détaillées sont disponibles dans le notebook complet (`notebooks/Untitled7.ipynb`).**


 # 7. Auteur & Contexte

Ce projet a été réalisé dans le cadre du module **"Outils libres pour le développement logiciel"**, Master 1 Informatique.

-  **Auteur** : Massilia Oumaza
-  **Formation** : Master 1 Informatique parcours Big Data et fouille de données
-  **Université** :  IED_ Université Paris 8
-  **Date** : 01 juillet 2025



