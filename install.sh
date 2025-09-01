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

# Install Waveshare e-Paper library
echo "Installing Waveshare e-Paper library..."
# Méthode 1: Installation via pip (plus fiable)
pip install waveshare-epd

# Méthode 2: Si la méthode 1 échoue, installation depuis GitHub
if ! python -c "import waveshare_epd" 2>/dev/null; then
    echo "Installing Waveshare e-Paper library from GitHub..."
    cd /tmp
    if [ -d "e-Paper" ]; then
        rm -rf e-Paper
    fi
    git clone https://github.com/waveshare/e-Paper.git
    cd e-Paper/RaspberryPi_JetsonNano/python
    pip install .
    cd "$TARGET_DIR"
fi

# Vérifier l'installation
echo "Verifying Waveshare installation..."
if python -c "import waveshare_epd.epd7in3f; print('Waveshare EPD library installed successfully')"; then
    echo "✅ Waveshare library installed successfully"
else
    echo "❌ Failed to install Waveshare library"
    exit 1
fi

echo "Installing systemd service..."
# Update the service file to use the virtual environment
sed -i "s|ExecStart=.*|ExecStart=$VENV_DIR/bin/python dashboard.py|" frame/frame.service
cp frame/frame.service /etc/systemd/system/frame.service

# Copy the update script to a convenient location
echo "Installing update script..."
cp update.sh /usr/local/bin/frame-update
chmod +x /usr/local/bin/frame-update

systemctl daemon-reload
systemctl enable frame.service
systemctl start frame.service

echo "Installation complete!"
echo "You can update the Frame software at any time by running: sudo frame-update"
