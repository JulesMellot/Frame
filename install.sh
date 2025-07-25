#!/bin/bash
set -e

TARGET_DIR="/home/pi/Frame"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

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

echo "Installing dependencies..."
apt-get update
apt-get install -y python3-pip git
pip3 install --no-cache-dir Pillow requests plexapi flask waveshare-epd

echo "Installing systemd service..."
cp OnFrame/frame.service /etc/systemd/system/frame.service
systemctl daemon-reload
systemctl enable frame.service
systemctl start frame.service

echo "Installation complete!"
