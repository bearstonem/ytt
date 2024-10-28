#!/bin/bash

# Check for root privileges
if [ "$EUID" -ne 0 ]; then 
    echo "Please run as root or with sudo"
    exit 1
fi

# Set up directories and permissions
SERVICE_USER="ytservice"
INSTALL_DIR="/opt/youtube-transcriber"
LOG_DIR="/var/log/youtube-transcriber"

# Create service user if it doesn't exist
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/false "$SERVICE_USER"
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$LOG_DIR"

# Copy application files
cp server.py "$INSTALL_DIR/"
cp service.py "$INSTALL_DIR/"
cp .env "$INSTALL_DIR/"

# Set permissions
chown -R "$SERVICE_USER:$SERVICE_USER" "$INSTALL_DIR"
chown -R "$SERVICE_USER:$SERVICE_USER" "$LOG_DIR"
chmod 750 "$INSTALL_DIR"
chmod 750 "$LOG_DIR"

# Install systemd service
cp youtube-transcriber.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable youtube-transcriber
systemctl start youtube-transcriber

echo "Service installation complete!"
echo "Check service status with: systemctl status youtube-transcriber"
echo "View logs with: journalctl -u youtube-transcriber" 