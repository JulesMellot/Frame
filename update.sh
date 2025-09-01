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
else
    echo "Updates available. Updating..."
    # Mettre à jour le code
    git pull origin main
fi

# Vérifier et installer les dépendances système si nécessaire
echo "Checking system dependencies..."
apt-get update
apt-get install -y python3-pip python3-venv python3-pil python3-numpy python3-smbus
apt-get install -y python3-spidev python3-rpi.gpio

# Activer l'interface SPI si nécessaire
echo "Enabling SPI interface..."
raspi-config nonint do_spi 0

# Add pi user to required groups (if not already done)
echo "Adding pi user to gpio and spi groups..."
usermod -a -G gpio pi
usermod -a -G spi pi

# Mettre à jour les dépendances dans l'environnement virtuel
echo "Updating dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade -r requirements.txt

# Vérifier l'installation des dépendances critiques
echo "Verifying critical dependencies..."
if python -c "import spidev; import gpiozero; import RPi.GPIO; print('Critical dependencies installed successfully')"; then
    echo "✅ Critical dependencies installed successfully"
else
    echo "❌ Failed to install critical dependencies"
    exit 1
fi

# Redémarrer le service
echo "Update complete!"
echo "Please restart the service with: sudo systemctl restart frame.service"
echo "Or reboot the system for GPIO permission changes to take full effect: sudo reboot"