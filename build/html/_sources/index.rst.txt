==================================
Prévision de l'Économie Marocaine
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

Architecture Centrale et Composants
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

Détails de l'Implémentation Technique
-------------------------------------

**Pipeline de Traitement des Données**

Le projet maintient la cohérence temporelle grâce à des données mensuelles complétées par des zéros, garantissant que :
- Toutes les séries temporelles ont une granularité uniforme
- Les points de données manquants sont gérés systématiquement
- Les modèles saisonniers et les comportements cycliques sont préservés

**Architecture de l'Interface Utilisateur**

L'interface basée sur Streamlit fournit :
- **Visualisation en Temps Réel** : Graphiques et diagrammes interactifs pour explorer les prévisions
- **Intégration de Chronologie d'Événements** : Représentation visuelle de la façon dont les événements sont corrélés aux changements économiques
- **Analyse de Scénarios** : Les utilisateurs peuvent simuler l'impact d'événements hypothétiques
- **Analyse Comparative** : Comparaison côte à côte de différents scénarios de prévision

**Entraînement et Validation des Modèles**

Le système emploie des méthodologies d'entraînement sophistiquées :
- **Validation Croisée** : La validation croisée des séries temporelles assure la robustesse du modèle
- **Entraînement Conscient des Événements** : Les modèles sont entraînés à reconnaître les modèles avant, pendant et après des événements significatifs
- **Prévision Multi-Horizon** : Différents horizons de prédiction (court, moyen, long terme) sont supportés

Caractéristiques Avancées
-------------------------

**Apprentissage Adaptatif**

Le système est conçu pour s'améliorer continuellement grâce à :
- **Réentraînement des Modèles** : Mises à jour programmées tous les deux ans pour incorporer de nouveaux modèles de données
- **Apprentissage d'Événements** : Le système apprend de nouveaux événements et leurs impacts réels sur l'économie
- **Surveillance des Performances** : Évaluation continue de la précision des prévisions et des performances du modèle

**Quantification de l'Incertitude**
- **Intervalles de Confiance** : Toutes les prévisions incluent des bornes d'incertitude
- **Probabilités de Scénarios** : Plusieurs scénarios sont fournis avec des probabilités associées
- **Évaluation des Risques** : Les risques potentiels à la baisse et à la hausse sont quantifiés

**Capacités d'Intégration**
- **Points de Terminaison API** : Le système peut être intégré avec des flux de données économiques externes
- **Fonctionnalité d'Exportation** : Les prévisions et analyses peuvent être exportées dans plusieurs formats
- **Fonctionnalités Collaboratives** : Plusieurs utilisateurs peuvent partager des scénarios et analyses

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

Intégration NLP Détaillée
-------------------------

**Interface IA Conversationnelle**

Le composant chatbot permet aux utilisateurs de :
- Transformer le prompt en une fichier ou on peut modifier les données extraites comme la date, le peak, la description...
- Interroger les données économiques en utilisant le langage naturel
- Explorer les scénarios de prévision à travers le dialogue
- Recevoir des insights personnalisés basés sur des intérêts spécifiques

**Traitement Automatisé d'Événements**

Les algorithmes NLP automatiquement :
- Extraient les événements pertinents des sources d'actualités et documents politiques
- Catégorisent les événements par type et impact économique potentiel
- Génèrent des courbes d'influence d'événements pour la modélisation
- Mettent à jour les bases de données d'événements avec de nouveaux développements

**Génération Intelligente de Rapports**

Le système produit :
- Des résumés en langage naturel des résultats de prévision
- Des explications de la confiance et de l'incertitude du modèle
- Une interprétation contextuelle des tendances économiques
- Des alertes automatisées pour les changements significatifs de prévision

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
    streamlit run interface/app.py

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   index2
   index3