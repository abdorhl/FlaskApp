# Application Flask Sécurisée avec Pipeline CI/CD

Ce projet implémente une application web Flask avec un pipeline CI/CD sécurisé utilisant Jenkins, Ansible et Git.

## Prérequis

- Python 3.9+
- Jenkins
- Ansible
- Git
- Docker (pour les tests OWASP ZAP)
- Serveur Ubuntu (pour le déploiement)

## Configuration de l'environnement de développement

1. Cloner le dépôt :
```bash
git clone <votre-repo>
cd <votre-repo>
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows : venv\Scripts\activate
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration de Jenkins

1. Installer les plugins Jenkins requis :
   - Git plugin
   - Ansible plugin
   - Pipeline plugin
   - HTML Publisher plugin

2. Configurer les credentials dans Jenkins :
   - Credentials Git
   - Credentials SSH pour Ansible

3. Créer un nouveau pipeline dans Jenkins pointant vers votre dépôt Git

## Configuration d'Ansible

1. Modifier le fichier `ansible/inventory.ini` avec vos informations serveur
2. Vérifier les configurations dans `ansible/deploy.yml`

## Tests de sécurité

Le pipeline inclut plusieurs niveaux de tests de sécurité :
- Analyse statique avec Bandit
- Tests unitaires avec pytest
- Scan de vulnérabilités avec OWASP ZAP

## Déploiement

Le déploiement est automatisé via Ansible et inclut :
- Configuration du pare-feu
- Installation et configuration de Nginx
- Configuration SSL/TLS
- Démarrage sécurisé de l'application avec Gunicorn

## Sécurité

L'application implémente plusieurs mesures de sécurité :
- HTTPS forcé
- En-têtes de sécurité
- Configuration sécurisée des cookies
- Pare-feu configuré
- Isolation des processus
