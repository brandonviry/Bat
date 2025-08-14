# Battery Monitor - Surveillance Professionnelle de Batterie

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Version](https://img.shields.io/badge/version-1.0.0-brightgreen.svg)](main.py)

Un système de surveillance de batterie professionnel et modulaire pour ordinateurs portables, développé en Python avec une architecture moderne et extensible.

> 🔄 **Projet Refactorisé** : Ce projet a été complètement restructuré d'un script simple vers une architecture modulaire professionnelle avec l'aide de l'IA pour accélérer le développement et améliorer la qualité du code.

## 🚀 Fonctionnalités

- **Surveillance en temps réel** : Monitoring continu de l'état de la batterie
- **Notifications intelligentes** : Alertes pour batterie faible, pleine, et changements d'état de charge
- **Configuration flexible** : Paramètres configurables via arguments CLI ou variables d'environnement
- **Logging avancé** : Système de logs complet avec niveaux configurables
- **Architecture modulaire** : Code organisé en modules réutilisables
- **Gestion d'erreurs robuste** : Gestion appropriée des exceptions et états d'erreur
- **Tests unitaires** : Suite de tests pour assurer la qualité du code
- **Cross-platform** : Compatible Windows, macOS, et Linux

## 📦 Installation

### Installation rapide

```bash
# Cloner le repository
git clone https://github.com/brandonviry/Bat.git
cd Bat

# Méthode 1: Script automatique (recommandé)
# Windows
start.bat

# Linux/macOS
chmod +x start.sh
./start.sh

# Méthode 2: Installation manuelle
pip install -r requirements.txt
python main.py
```

### Installation pour le développement

```bash
# Installation en mode développement avec outils de dev
pip install -e .[dev]

# Ou installation des dépendances de test uniquement
pip install -e .[test]

# Installation depuis setup.py
python setup.py install
```

## 🎯 Utilisation

### Démarrage rapide

```bash
# Windows - Double-cliquez sur start.bat ou :
start.bat

# Linux/macOS
chmod +x start.sh
./start.sh

# Ou directement avec Python
python main.py
```

### Utilisation basique

```bash
# Lancer avec la configuration par défaut
python main.py

# Afficher l'aide complète
python main.py --help

# Afficher la version
python main.py --version
```

### Options de configuration avancées

```bash
# Personnaliser les seuils de batterie
python main.py --low-threshold 15 --full-threshold 85

# Modifier l'intervalle de vérification (en secondes)
python main.py --interval 30

# Désactiver les notifications système
python main.py --no-notifications

# Activer les logs détaillés avec fichier
python main.py --log-level DEBUG --log-file battery.log

# Configuration personnalisée complète
python main.py --low-threshold 10 --full-threshold 90 --interval 15 --app-name "Mon Monitor" --log-level INFO
```

### Configuration par variables d'environnement

```bash
# Copier le fichier d'exemple
cp config.example.env .env

# Éditer le fichier .env selon vos besoins
# Puis définir les variables :
export BAT_LOW_THRESHOLD=15
export BAT_FULL_THRESHOLD=85
export BAT_CHECK_INTERVAL=30
export BAT_LOG_LEVEL=DEBUG
export BAT_LOG_FILE=battery.log

# Lancer l'application
python main.py
```

## ⚙️ Configuration

### Variables d'environnement supportées

| Variable | Description | Défaut |
|----------|-------------|---------|
| `BAT_LOW_THRESHOLD` | Seuil batterie faible (%) | 20 |
| `BAT_FULL_THRESHOLD` | Seuil batterie pleine (%) | 80 |
| `BAT_CHECK_INTERVAL` | Intervalle de vérification (secondes) | 60 |
| `BAT_APP_NAME` | Nom de l'application | Battery Monitor |
| `BAT_ENABLE_NOTIFICATIONS` | Activer les notifications | true |
| `BAT_LOG_LEVEL` | Niveau de log | INFO |
| `BAT_LOG_FILE` | Fichier de log | None |

### Arguments en ligne de commande

```
--low-threshold PERCENT     Seuil de batterie faible
--full-threshold PERCENT    Seuil de batterie pleine
--interval SECONDS          Intervalle de vérification
--app-name NAME            Nom de l'application
--no-notifications         Désactiver les notifications
--log-level LEVEL          Niveau de logging (DEBUG, INFO, WARNING, ERROR)
--log-file FILE            Fichier de log
--version                  Afficher la version
```

## 🏗️ Architecture

Le projet suit une architecture modulaire avec séparation claire des responsabilités :

```
Bat/
├── src/                          # Code source modulaire
│   ├── __init__.py              # Package principal (v1.0.0)
│   ├── config.py                # Gestion de la configuration
│   ├── battery_status.py        # Monitoring de la batterie avec psutil
│   ├── notifications.py         # Système de notifications multi-plateforme
│   └── monitor.py               # Service principal de surveillance
├── tests/                       # Suite de tests
│   ├── __init__.py
│   └── test_config.py          # Tests unitaires de configuration
├── main.py                      # Point d'entrée principal avec CLI
├── requirements.txt             # Dépendances Python
├── setup.py                     # Configuration d'installation
├── README.md                    # Documentation complète
├── LICENSE                      # Licence MIT
├── .gitignore                   # Fichiers à ignorer
├── config.example.env           # Exemple de configuration
├── start.bat                    # Script de démarrage Windows
├── start.sh                     # Script de démarrage Linux/macOS
└── bat.py                       # Version originale (legacy)
```

### Composants principaux

- **BatteryConfig** : Gestion centralisée de la configuration avec validation
- **BatteryStatusMonitor** : Interface avec psutil pour récupérer l'état de la batterie
- **BatteryInfo** : Dataclass pour les informations de batterie (pourcentage, état de charge, temps restant)
- **NotificationManager** : Gestion des notifications avec providers pluggables
- **PlyerNotificationProvider** : Notifications système cross-platform
- **LogNotificationProvider** : Provider de notifications via logs
- **BatteryMonitorService** : Service principal orchestrant la surveillance
- **BatteryMonitorApp** : Application wrapper avec gestion du logging et CLI

### Patterns de conception utilisés

- **Strategy Pattern** : Pour les providers de notifications
- **Factory Pattern** : Pour la création de configurations
- **Observer Pattern** : Pour la surveillance de la batterie
- **Dependency Injection** : Pour l'injection des dépendances

## 🧪 Tests

```bash
# Lancer les tests
pytest

# Tests avec couverture
pytest --cov=src

# Tests en mode verbose
pytest -v
```

## 🔧 Développement

### Prérequis

- Python 3.8+
- pip

### Setup de développement

```bash
# Cloner le projet
git clone https://github.com/brandonviry/Bat.git
cd Bat

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows

# Installer en mode développement
pip install -e .[dev]

# Lancer les tests
pytest
```

### Standards de code

Le projet utilise :
- **Black** pour le formatage du code
- **Flake8** pour le linting
- **MyPy** pour la vérification de types
- **Pytest** pour les tests

```bash
# Formater le code
black src/ tests/

# Vérifier le style
flake8 src/ tests/

# Vérifier les types
mypy src/
```

## 📋 Dépendances

### Dépendances principales

- **psutil** (≥5.9.0) : Accès aux informations système
- **plyer** (≥2.1.0) : Notifications cross-platform

### Dépendances de développement

- **pytest** : Framework de tests
- **pytest-cov** : Couverture de code
- **black** : Formatage de code
- **flake8** : Linting
- **mypy** : Vérification de types

## 🤝 Contribution

Les contributions sont les bienvenues ! Voici comment contribuer :

1. Fork le projet
2. Créer une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Commiter vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pousser vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Guidelines de contribution

- Suivre les standards de code du projet
- Ajouter des tests pour les nouvelles fonctionnalités
- Mettre à jour la documentation si nécessaire
- S'assurer que tous les tests passent

## 📝 Changelog

### Version 1.0.0 (2025-01-14)

**🔄 Refactorisation Complète**
- ✨ Architecture modulaire professionnelle (de 100 à 500+ lignes)
- ✨ Configuration flexible (CLI + variables d'environnement)
- ✨ Système de logging avancé avec niveaux configurables
- ✨ Notifications intelligentes avec prévention des doublons
- ✨ Gestion d'erreurs robuste avec exceptions personnalisées
- ✨ Tests unitaires avec pytest
- ✨ Documentation complète avec exemples
- ✨ Scripts de démarrage multi-plateforme
- ✨ Support des dataclasses pour les informations de batterie
- ✨ Pattern Strategy pour les notifications
- ✨ Validation de configuration avec messages d'erreur clairs
- ✨ Logging structuré avec timestamps
- ✨ Support du temps de batterie restant
- ✨ Interface CLI professionnelle avec argparse

**🛠️ Améliorations Techniques**
- 🔧 Séparation claire des responsabilités
- 🔧 Code réutilisable et extensible
- 🔧 Gestion gracieuse des interruptions (Ctrl+C)
- 🔧 Threading sécurisé avec Event
- 🔧 Configuration par défaut sensée
- 🔧 Support multi-plateforme (Windows, Linux, macOS)

### Version 0.1.0 (Original)
- 📦 Script monolithique de base
- 📦 Surveillance simple de batterie
- 📦 Notifications basiques

## 📄 Licence

Ce projet est sous Aucune licence.

## 👨‍💻 Auteur

**VIRY Brandon**

- GitHub: [@brandonviry](https://github.com/brandonviry)


## 🔮 Roadmap

### Version 1.1.0 (Prochaine)
- [ ] Interface graphique (GUI) avec tkinter/PyQt
- [ ] Historique et graphiques de batterie
- [ ] Notifications par email/SMS
- [ ] Configuration via fichier JSON/YAML

### Version 1.2.0 (Future)
- [ ] API REST pour monitoring distant
- [ ] Dashboard web avec Flask/FastAPI
- [ ] Support de multiples batteries
- [ ] Intégration avec des services de monitoring (Prometheus, Grafana)

### Version 2.0.0 (Long terme)
- [ ] Mode économie d'énergie automatique
- [ ] Intelligence artificielle pour prédiction de batterie
- [ ] Application mobile compagnon
- [ ] Synchronisation cloud
- [ ] Plugins et extensions

### Améliorations continues
- [ ] Plus de tests unitaires et d'intégration
- [ ] Documentation API avec Sphinx
- [ ] CI/CD avec GitHub Actions
- [ ] Package PyPI officiel
- [ ] Docker container

---

⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile !
