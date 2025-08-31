#!/bin/bash
set -e

TARGET_DIR="/home/pi/Frame"
VENV_DIR="$TARGET_DIR/venv"
BACKUP_DIR="$TARGET_DIR/backup"

# Vérifier si le script est exécuté en tant que root
if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root (e.g. with sudo)"
    exit 1
fi

# Créer un répertoire de sauvegarde
echo "Creating backup..."
mkdir -p "$BACKUP_DIR"
cp "$TARGET_DIR/.env" "$BACKUP_DIR/" 2>/dev/null || echo "No .env file to backup"

# Sauvegarder la configuration du service si elle existe
cp /etc/systemd/system/frame.service "$BACKUP_DIR/" 2>/dev/null || echo "No service file to backup"

echo "Fetching latest changes from repository..."
cd "$TARGET_DIR"

# Récupérer les derniers changements
git fetch origin

# Vérifier s'il y a des mises à jour
LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    echo "Already up to date."
    exit 0
fi

echo "Updates available. Updating..."

# Mettre à jour le code
git pull origin main

# Mettre à jour les dépendances dans l'environnement virtuel
echo "Updating dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade -r requirements.txt

# Redémarrer le service
echo "Restarting service..."
systemctl restart frame.service

echo "Update complete!"