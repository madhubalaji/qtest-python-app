# Gestionnaire de Tâches

Une application simple de gestion de tâches avec des interfaces CLI et web.

## Fonctionnalités

- Ajouter, voir, mettre à jour et **supprimer** les tâches
- Marquer les tâches comme terminées
- Rechercher des tâches par mot-clé
- Filtrer les tâches par statut et priorité
- Interface en ligne de commande pour une gestion rapide des tâches
- Interface web construite avec Streamlit pour une expérience utilisateur conviviale
- **Nouvelle fonctionnalité**: Suppression de tâches avec confirmation dans l'interface utilisateur

## Structure du Projet

```
task_manager_project/
├── config/                 # Fichiers de configuration et stockage des tâches
├── docs/                   # Documentation
├── src/                    # Code source
│   ├── models/             # Modèles de données
│   │   └── task.py         # Modèle de tâche
│   ├── services/           # Logique métier
│   │   └── task_service.py # Service de gestion des tâches
│   ├── utils/              # Modules utilitaires
│   │   └── exceptions.py   # Exceptions personnalisées
│   ├── app.py              # Application web Streamlit
│   └── cli.py              # Interface en ligne de commande
└── requirements.txt        # Dépendances du projet
```

## Installation

1. Cloner le dépôt :
   ```
   git clone <repository-url>
   cd task_manager_project
   ```

2. Installer les dépendances :
   ```
   pip install -r requirements.txt
   ```

## Utilisation

### Interface en Ligne de Commande

Exécuter l'application CLI :

```
python -m src.cli
```

Commandes disponibles :

- Ajouter une tâche : `python -m src.cli add "Titre de la tâche" -d "Description de la tâche" -p high`
- Lister les tâches : `python -m src.cli list`
- Lister toutes les tâches y compris les terminées : `python -m src.cli list -a`
- Terminer une tâche : `python -m src.cli complete <task-id>`
- **Supprimer une tâche** : `python -m src.cli delete <task-id>`
- Rechercher des tâches : `python -m src.cli search <keyword>`
- Voir les détails d'une tâche : `python -m src.cli view <task-id>`

### Interface Web

Exécuter l'application web Streamlit :

```
streamlit run src/app.py
```

L'interface web fournit les pages suivantes :
- **Voir les Tâches** : Afficher et gérer toutes les tâches avec possibilité de suppression
- **Ajouter une Tâche** : Créer de nouvelles tâches
- **Rechercher des Tâches** : Trouver des tâches par mot-clé avec option de suppression

## Nouvelles Fonctionnalités de Suppression

### Dans l'Interface Web :

1. **Page "Voir les Tâches"** :
   - Bouton de suppression (🗑️) à côté de chaque tâche
   - Confirmation en deux étapes pour éviter les suppressions accidentelles
   - Messages de succès après suppression

2. **Page "Rechercher des Tâches"** :
   - Bouton "Supprimer la Tâche" dans les détails de chaque tâche
   - Même système de confirmation que dans la page principale
   - Retour automatique à la liste après suppression

### Sécurité :
- **Confirmation obligatoire** : Chaque suppression nécessite une confirmation explicite
- **Gestion d'erreurs** : Messages d'erreur informatifs si la tâche n'existe pas
- **Persistance** : Les suppressions sont immédiatement sauvegardées

## Test de la Fonctionnalité

Pour tester la fonctionnalité de suppression :

```
python test_delete_functionality.py
```

Ce script teste automatiquement :
- Création de tâches
- Suppression de tâches existantes
- Gestion des erreurs pour les tâches inexistantes
- Persistance des données

## Licence

[MIT License](LICENSE)
