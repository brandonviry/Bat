#!/bin/bash

echo "Battery Monitor - Démarrage"
echo "============================"

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé"
    echo "Veuillez installer Python 3 depuis https://python.org"
    exit 1
fi

# Créer un environnement virtuel si il n'existe pas
if [ ! -d "venv" ]; then
    echo "Création de l'environnement virtuel..."
    python3 -m venv venv
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances
echo "Installation des dépendances..."
pip install -r requirements.txt

# Démarrer l'application
echo "Démarrage de Battery Monitor..."
echo "Appuyez sur Ctrl+C pour arrêter"
echo ""
python main.py

# Désactiver l'environnement virtuel
deactivate
