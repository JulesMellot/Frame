#!/bin/bash
set -e

TARGET_DIR="/home/pi/Frame"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$TARGET_DIR/venv"

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root (e.g. with sudo)"
    exit 1
fi

# Copy repository to the default location if not already there
if [ "$SCRIPT_DIR" != "$TARGET_DIR" ]; then
    echo "Copying project to $TARGET_DIR"
    mkdir -p "$TARGET_DIR"
    cp -r "$SCRIPT_DIR"/* "$TARGET_DIR/"
fi

cd "$TARGET_DIR"

echo "Installing system dependencies..."
apt-get update
apt-get install -y python3-pip python3-venv python3-pil python3-numpy python3-smbus
apt-get install -y python3-spidev python3-rpi.gpio git

# Enable SPI interface
echo "Enabling SPI interface..."
raspi-config nonint do_spi 0

# Add pi user to required groups
echo "Adding pi user to gpio and spi groups..."
usermod -a -G gpio pi
usermod -a -G spi pi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv "$VENV_DIR"

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip in the virtual environment
pip install --upgrade pip

# Install Python dependencies in the virtual environment
echo "Installing Python dependencies..."
pip install --no-cache-dir -r requirements.txt

# Vérifier l'installation des dépendances critiques
echo "Verifying critical dependencies..."
if python -c "import spidev; import gpiozero; import RPi.GPIO; print('Critical dependencies installed successfully')"; then
    echo "✅ Critical dependencies installed successfully"
else
    echo "❌ Failed to install critical dependencies"
    exit 1
fi

echo "Installing systemd service..."
# Update the service file to use the pi user
sed -i "s|User=.*|User=pi|" frame/frame.service
sed -i "s|Group=.*|Group=pi|" frame/frame.service
cp frame/frame.service /etc/systemd/system/frame.service

# Copy the update script to a convenient location
echo "Installing update script..."
cp update.sh /usr/local/bin/frame-update
chmod +x /usr/local/bin/frame-update

systemctl daemon-reload
systemctl enable frame.service

echo "Installation complete!"
echo "The system needs to be rebooted for GPIO permissions to take effect."
echo "Please run: sudo reboot"
echo "After reboot, start the service with: sudo systemctl start frame.service"
