.. raw:: html

   <div style="display: flex; align-items: center; margin-bottom: 20px;">
     <img src="build/html/_static/images/image.png" alt="Logo" width="80" style="margin-right: 20px;">
     <h1 style="margin: 0;">Prévision de l'Économie Marocaine</h1>
   </div>

==================================

.. image:: https://img.shields.io/badge/Statut-Actif-green
   :alt: Statut Actif

.. image:: https://img.shields.io/badge/Python-3.8%2B-blue
   :alt: Version Python

.. image:: https://img.shields.io/badge/Framework-Streamlit-red
   :alt: Framework Streamlit

Analyse Avancée de Séries Temporelles avec Influence d'Événements et Intégration NLP
==================================================================================

Ce projet représente une approche de pointe pour la prévision économique, spécifiquement conçue pour l'économie marocaine. Il combine une modélisation sophistiquée de séries temporelles avec une analyse événementielle et un traitement du langage naturel pour fournir des prédictions économiques complètes et interprétables.

Vue d'Ensemble du Projet
------------------------

Le projet de Prévision de l'Économie Marocaine représente un système d'analyse de séries temporelles avancé conçu pour prédire les indicateurs économiques clés du Maroc. Ce qui distingue ce projet des modèles de prévision économique traditionnels, c'est son intégration sophistiquée d'analyses événementielles et de capacités de traitement du langage naturel, créant un écosystème de prévision complet qui tient compte à la fois des données économiques quantitatives et des impacts qualitatifs des événements.

.. figure:: _static/images/pipeline.png
   :alt: Piepeline d'interface
   :width: 100%
   
   **Figure 1:** Pipeline de l'interface
----------------------------------

**1. Système de Prévision Multi-Modèles**

Le projet emploie une approche modulaire avec des modèles de réseaux de neurones spécialisés, chacun adapté à des catégories spécifiques d'indicateurs économiques :

- **eco1_model.keras & eco2_model.keras** : Gèrent les indicateurs économiques généraux tels que les composants du PIB, les taux d'inflation et les mesures fiscales
- **prod_model.keras** : Se concentre sur les métriques liées à la production, y compris la production industrielle, les indices manufacturiers et la productivité sectorielle
- **rate_model.keras** : Se spécialise dans les indicateurs basés sur les taux tels que les taux d'intérêt, les taux de change et les courbes de rendement
- **demo_model.keras** : Traite les indicateurs démographiques incluant la croissance démographique, les statistiques d'emploi et la participation à la main-d'œuvre
- **consum_model.keras** : Analyse les modèles de consommation, les ventes au détail et les métriques de comportement des consommateurs

Chaque modèle est associé à son normalisateur dédié (stocké dans saved_scalers/) pour assurer une normalisation appropriée des données et un prétraitement cohérent across different indicator types.

**2. Cadre de Prévision Conscient des Événements**

La force unique du système réside dans sa capacité à incorporer des événements significatifs dans le processus de prévision :

- **Intégration d'Événements** : Les jours fériés majeurs, les crises économiques, les réformes politiques et les chocs externes sont encodés comme caractéristiques
- **Cartographie Temporelle** : Les événements sont mappés à leurs dates d'occurrence et leur influence est modélisée dans le temps
- **Courbes d'Impact** : Le module `curves.py` traite les modèles d'influence des événements, permettant au modèle de comprendre comment différents types d'événements affectent les indicateurs économiques sur diverses horizons temporels

**3. Intégration du Traitement du Langage Naturel**

Le composant NLP, implémenté à travers la fonctionnalité de chatbot, sert plusieurs objectifs :

Interface de Requête Conversationnelle
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Les utilisateurs peuvent poser des questions sur les tendances économiques en langage naturel
- Le système interprète les requêtes et fournit des prévisions et explications pertinentes
- Les concepts économiques complexes sont expliqués dans un langage accessible

Interprétation Intelligente des Données
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Les algorithmes NLP analysent les descriptions textuelles d'événements et catégorisent automatiquement leur impact économique potentiel
- Les articles de presse, annonces politiques et rapports économiques peuvent être traités pour extraire les événements pertinents
- L'analyse de sentiment des nouvelles économiques aide à pondérer l'impact des événements sur les modèles de prévision

Génération Automatique de Rapports
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- Le système génère des explications en langage naturel des résultats de prévision
- Les tendances et modèles sont automatiquement décrits dans un format lisible par l'homme
- La quantification de l'incertitude est communiquée à travers un langage clair et compréhensible


Indicateurs Économiques Clés Prévus
-----------------------------------

Le système fournit des prévisions pour les indicateurs économiques critiques du Maroc :

- **IDE (Indice de Développement des Investissements)** : Suivi des flux d'investissement et des modèles de développement
- **REER (Taux de Change Effectif Réel)** : Compréhension de la compétitivité monétaire
- **Métriques d'Emploi** : Dynamiques du marché du travail et tendances du chômage
- **Volumes Commerciaux** : Modèles d'importation/exportation et prévisions de balance commerciale
- **Indicateurs Sectoriels** : Performance des secteurs agriculture, manufacturier et services
- **Indicateurs Monétaires** : Masse monétaire, croissance du crédit et métriques du secteur bancaire

Structure du Projet
-------------------

::

    interface/
    ├── data/
    │   └── Morocco.csv              # Jeu de données économiques mensuelles (complété par zéros)
    ├── saved_models/                # Modèles de prévision entraînés
    │   ├── eco1_model.keras         # Indicateurs économiques généraux (ensemble 1)
    │   ├── eco2_model.keras         # Indicateurs économiques généraux (ensemble 2)
    │   ├── prod_model.keras         # Métriques de production et industrielles
    │   ├── rate_model.keras         # Taux d'intérêt et taux financiers
    │   ├── demo_model.keras         # Données démographiques et d'emploi
    │   └── consum_model.keras       # Indicateurs de consommation et de vente au détail
    ├── saved_scalers/               # Normalisateurs de prétraitement pour la cohérence des modèles
    │   ├── eco_scaler1.pkl          # Normalisateur pour eco1_model
    │   ├── eco_scaler2.pkl          # Normalisateur pour eco2_model
    │   ├── prod_scaler.pkl          # Normalisateur pour prod_model
    │   ├── rate_scaler.pkl          # Normalisateur pour rate_model
    │   ├── demo_scaler.pkl          # Normalisateur pour demo_model
    │   └── consum_scaler.pkl        # Normalisateur pour consum_model
    ├── ui/                          # Composants de l'interface utilisateur
    │   ├── chatbot.py               # Interface conversationnelle alimentée par NLP
    │   ├── indicator_list.py        # Définitions complètes des indicateurs
    │   ├── indicators.py            # Traitement et analyse des indicateurs
    │   ├── overview.py              # Vue d'ensemble et résumé du tableau de bord
    │   ├── sidebar.py               # Intégration d'événements et contrôles
    │   ├── simulation.py            # Prévision et simulation de scénarios
    │   └── styles.py                # Style et thématisation de l'interface utilisateur
    ├── curves.py                    # Modélisation des courbes d'influence d'événements
    ├── custom_functions.py          # Custom Functions utilisées pour entraîner les models
    ├── model.py                     # Configuration des modèles et moteur de prévision
    ├── data.py                      # Traitement et gestion des données
    └── app.py                       # Application Streamlit principale

Assistant IA - Chatbot de Création d'Événements
==============================================

Aperçu Général
---------------

L'Assistant IA est un chatbot intelligent conçu pour extraire et créer des événements à partir de descriptions en langage naturel. Il utilise un traitement de texte avancé et la reconnaissance de motifs pour analyser automatiquement les informations d'événements et les convertir en données structurées pour l'analyse et la visualisation.

Fonctionnalités
---------------

 **Traitement du Langage Naturel**
   Le chatbot peut comprendre et traiter les descriptions d'événements écrites en français naturel, en extrayant automatiquement les informations clés.

 **Extraction Intelligente de Dates**
   Prend en charge plusieurs formats de dates et expressions :
   
   - Formats standard : ``JJ/MM/AAAA``, ``AAAA-MM-JJ``
   - Mois français : "15 janvier 2030", "mars 2028"
   - Expressions relatives : "début 2030", "deuxième trimestre 2027"
   - Dates contextuelles : "en 2029", "pour 2030"

 **Catégorisation Automatique**
   Les événements sont automatiquement classés en 8 catégories principales :
   
   -  Infrastructure & Transport
   -  Énergie & Environnement
   -  Industrie & Manufacturing
   -  Agriculture & Agroalimentaire
   -  Tourisme & Culture
   -  Santé & Éducation
   -  Digital & Technologies
   -  Économie & Finance

 **Analyse d'Impact**
   Le système détermine automatiquement :
   
   - **Sentiment** : Impact positif (Good) ou négatif (Bad)
   - **Intensité** : Valeur de pic d'impact de -1.0 à 1.0
   - **Durée** : Durée de l'événement en mois
   - **Type de Courbe** : Distribution d'impact linéaire, exponentielle ou gaussienne

 **Reconnaissance Géographique**
   Identifie automatiquement les villes marocaines mentionnées dans les descriptions d'événements et les associe à l'événement.

Modes de Saisie
----------------

Mode Langage Naturel
~~~~~~~~~~~~~~~~~~~~

Les utilisateurs peuvent décrire les événements en français naturel. L'IA extrait automatiquement toutes les informations pertinentes.

**Exemples de saisie :**

.. code-block:: text

   "Inauguration d'une nouvelle usine automobile à Casablanca en mars 2028"
   "Crise économique majeure prévue pour le deuxième trimestre 2027"
   "Ouverture d'un grand complexe touristique à Agadir fin 2029"
   "Lancement du projet de modernisation des ports en 2030"

**Processus d'extraction :**

1. **Analyse du Texte** : Le système analyse le texte d'entrée pour les mots-clés et motifs
2. **Extraction d'Informations** : Les dates, lieux, catégories et indicateurs d'impact sont identifiés
3. **Sortie Structurée** : Toutes les informations sont converties en format d'événement structuré
4. **Validation** : Les utilisateurs peuvent réviser et modifier les informations extraites avant l'ajout

Mode Formulaire Structuré
~~~~~~~~~~~~~~~~~~~~~~~~~

Pour les utilisateurs qui préfèrent la saisie manuelle, un formulaire structuré est disponible avec les champs suivants :

- **Nom de l'Événement** : Nom descriptif de l'événement
- **Date de l'Événement** : Sélecteur de date calendaire
- **Type d'Impact** : Sélection Bon/Mauvais
- **Catégorie** : Menu déroulant avec 8 catégories prédéfinies
- **Impact de Pic** : Curseur de -1.0 à 1.0
- **Durée** : Saisie numérique en mois
- **Courbe d'Impact** : Sélection Linéaire/Exponentielle/Gaussienne
- **Description** : Description en texte libre

Composants Principaux
---------------------

Classe EventExtractor
~~~~~~~~~~~~~~~~~~~~~

Le moteur de traitement principal qui gère toutes les tâches de traitement du langage naturel.

**Méthodes Clés :**

``extract_date(text: str) -> Optional[str]``
   Extrait les informations de date du texte en utilisant plusieurs motifs regex pour divers formats de date français.

``extract_category(text: str) -> str``
   Détermine la catégorie d'événement basée sur la correspondance de mots-clés avec des dictionnaires de catégories prédéfinis.

``extract_sentiment(text: str) -> str``
   Analyse le sentiment du texte pour déterminer si l'événement a un impact positif ou négatif.

``extract_peak_intensity(text: str, event_type: str) -> float``
   Calcule l'intensité de l'impact de l'événement basée sur les mots-clés d'intensité et le type d'événement.

``extract_duration(text: str) -> int``
   Estime la durée de l'événement en mois à partir de mentions explicites ou d'inférence basée sur des mots-clés.

``extract_curve_type(text: str) -> str``
   Détermine le type de courbe d'impact (Linéaire, Exponentielle, Gaussienne) basé sur des mots-clés descriptifs.

``extract_location(text: str) -> List[str]``
   Identifie les villes marocaines mentionnées dans le texte en utilisant une base de données de villes complète.

``parse_event(text: str) -> Dict``
   Méthode principale qui orchestre toutes les fonctions d'extraction pour créer un objet événement complet.

Reconnaissance de Motifs
~~~~~~~~~~~~~~~~~~~~~~~

Le système utilise une reconnaissance de motifs sophistiquée pour :

**Motifs de Date :**

.. code-block:: python

   # Formats de date standard
   r'(\d{1,2}[/-]\d{1,2}[/-]\d{4})'  # JJ/MM/AAAA
   r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})'  # AAAA/MM/JJ
   
   # Motifs de mois français
   r'(\d{1,2})\s+(janvier|février|mars|...)\s+(\d{4})'
   
   # Expressions de temps relatives
   r'(début|milieu|fin)\s+(\d{4})'
   r'(premier|deuxième|troisième|quatrième)\s+trimestre\s+(\d{4})'

**Mots-clés de Catégorie :**
Chaque catégorie contient 15-20 mots-clés pertinents pour une classification précise.

**Analyse de Sentiment :**
Utilise des dictionnaires de mots-clés positifs et négatifs pour déterminer le type d'impact de l'événement.

Interface Utilisateur
----------------------

L'interface du chatbot fournit :

Section de Saisie
~~~~~~~~~~~~~~~~~

- **Sélection de Mode** : Boutons radio pour choisir entre Langage Naturel et Formulaire Structuré
- **Zone de Texte** : Grand champ de saisie pour les descriptions d'événements
- **Aide Extensible** : Section pliable avec exemples et conseils

Section d'Analyse
~~~~~~~~~~~~~~~~~

- **Bouton Analyser** : Traite le texte de saisie et extrait les informations
- **Affichage des Résultats** : Montre toutes les informations extraites dans un format structuré
- **Validation** : Permet aux utilisateurs de réviser avant d'ajouter à la liste d'événements

Gestion des Événements
~~~~~~~~~~~~~~~~~~~~~~

- **Tableau des Événements Actuels** : Affiche tous les événements ajoutés dans un tableau formaté
- **Compteur d'Événements** : Montre le nombre total d'événements
- **Fonction de Suppression** : Option pour supprimer tous les événements
- **Statistiques Résumées** : Aperçu des événements positifs vs négatifs

Format de Sortie
-----------------

Chaque événement traité génère un dictionnaire structuré avec les champs suivants :

.. code-block:: python

   {
       "Date": "2028-03-01",                    # Format de date ISO
       "Event": "Nouvelle Usine Automobile",    # Nom d'événement généré
       "Type": "Good",                          # Classification Bon/Mauvais
       "Peak": 0.75,                           # Intensité d'impact (-1.0 à 1.0)
       "Duration": 24,                         # Durée en mois
       "Curve": "Linear",                      # Type de courbe d'impact
       "Description": "Description complète de l'événement", # Texte original ou résumé
       "Category": "🏭 Industrie & Manufacturing", # Catégorie auto-assignée
       "Locations": ["Casablanca"]             # Localisations extraites
   }

Exemples d'Utilisation
-----------------------

Création d'Événement de Base
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Sélectionner le mode "Langage Naturel"
2. Entrer la description d'événement : *"Ouverture d'un nouveau port à Tanger en juin 2029"*
3. Cliquer sur "Analyser l'Événement"
4. Réviser les informations extraites
5. Cliquer sur "Ajouter aux Événements"

Le système extraira :
- Date : 2029-06-01
- Catégorie : Infrastructure & Transport
- Type : Good (en raison du mot-clé "ouverture")
- Localisation : Tanger

Analyse d'Événement Complexe
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Pour des événements plus complexes avec plusieurs aspects :

.. code-block:: text

   "Lancement d'un projet majeur de développement d'énergies renouvelables 
   dans la région de Ouarzazate, prévu pour le premier trimestre 2030, 
   avec un impact économique significatif sur toute la région du sud"

Le système identifiera :
- Plusieurs mots-clés de la catégorie énergie
- Spécification de date trimestrielle  
- Localisation géographique
- Indicateurs d'intensité d'impact
- Implications de portée régionale

Intégration
-----------

Gestion de l'État de Session
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Le chatbot s'intègre avec l'état de session de Streamlit pour maintenir :

- ``events_data`` : Liste de tous les événements créés
- ``event_extractor`` : Instance EventExtractor initialisée
- ``current_extracted_event`` : Stockage temporaire pour les résultats d'analyse

Flux de Données
~~~~~~~~~~~~~~~

1. **Saisie Utilisateur** → Texte en langage naturel ou formulaire structuré
2. **Traitement** → EventExtractor analyse et extrait les informations  
3. **Validation** → L'utilisateur révise les données extraites
4. **Stockage** → Événement ajouté à l'état de session
5. **Affichage** → Liste d'événements mise à jour affichée à l'utilisateur

Bonnes Pratiques
-----------------

Pour des résultats optimaux lors de l'utilisation du mode langage naturel :

Directives de Saisie
~~~~~~~~~~~~~~~~~~~~

- **Être Spécifique** : Inclure dates, localisations et descriptions d'impact
- **Utiliser des Mots-clés** : Incorporer du vocabulaire sectoriel pertinent
- **Mentionner l'Échelle** : Inclure des mots comme "majeur", "important", "léger" pour l'intensité
- **Ajouter du Contexte** : Fournir des informations de fond pour une meilleure catégorisation

Exemples de Bonnes Saisies
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    "Inauguration d'une centrale solaire de 200MW à Ouarzazate en septembre 2028, 
       avec un impact économique majeur sur la région"
   
    "Fermeture définitive de l'usine textile de Casablanca prévue pour fin 2027, 
       entraînant une crise de l'emploi local"

Exemples de Mauvaises Saisies
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: text

    "Quelque chose va se passer"  # Trop vague
    "Nouveau projet"              # Détails manquants
    "Impact économique"           # Aucune description d'événement

Limitations
-----------

Limitations actuelles du système de chatbot :

- **Langue** : Principalement optimisé pour les saisies en français
- **Géographie** : Reconnaissance de localisation limitée aux villes marocaines
- **Contexte** : Ne peut accéder aux sources de données externes pour validation
- **Complexité** : Les descriptions multi-événements très complexes peuvent nécessiter une analyse manuelle

Améliorations Futures
--------------------

Améliorations prévues incluses :

- **Support Multi-langues** : Traitement des langues anglaise et arabe
- **Intégration de Données Externes** : Validation en temps réel contre les sources d'actualités
- **NER Amélioré** : Reconnaissance d'entités nommées améliorée pour les organisations et projets
- **Notation de Sentiment** : Analyse de sentiment plus nuancée avec scores de confiance
- **Fonctionnalité d'Export** : Export direct vers divers formats (CSV, JSON, Excel)

Référence API
--------------

La fonctionnalité du chatbot est accessible via ces fonctions principales :

``render_chatbot_tab()``
   Point d'entrée principal qui rend l'interface complète du chatbot.

``render_natural_language_input()``
   Gère l'interface de traitement du langage naturel et les interactions utilisateur.

``render_structured_form_input()``
   Fournit l'interface de formulaire de création d'événement manuel.

``render_current_events()``
   Affiche la liste d'événements actuelle et les contrôles de gestion.

``get_events_summary()``
   Retourne une chaîne de résumé des événements actuels pour l'affichage du statut.

Pour des exemples d'implémentation détaillés et des modèles d'utilisation avancés, référez-vous à la documentation du code source et aux commentaires en ligne.

Comment Commencer
-----------------

Installation
~~~~~~~~~~~~

.. code-block:: bash

    # Cloner le dépôt
    git clone https://github.com/MA-Zbida/Time-Series-Analysis.git
    cd Time-Series-Analysis

Lancer l'Application
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Démarrer l'application Streamlit
    streamlit run Interface/app.py

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index2
   index3
