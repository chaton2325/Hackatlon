# Gestionnaire d'Établissements

Une application web Flask pour gérer une liste d'établissements, avec espace administrateur pour validation.

## Fonctionnalités

- Page d'accueil avec deux boutons (Ajouter / Consulter)
- Formulaire d'ajout d'établissement
- Liste des établissements validés
- Dashboard administrateur pour gérer les établissements
- Base de données JSON simple

## Installation

1. Installez les dépendances:
   ```
   pip install -r requirements.txt
   ```

## Exécution

1. Lancez l'application:
   ```
   python app.py
   ```

2. Accédez à l'application dans votre navigateur:
   - **URL:** http://127.0.0.1:5000/
   
3. Accès administrateur:
   - **URL:** http://127.0.0.1:5000/admin/login
   - **Identifiants par défaut:** 
     - Nom d'utilisateur: admin
     - Mot de passe: admin123 