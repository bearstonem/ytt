#!/bin/bash

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
fi

# Install system dependencies
case $OS in
    "Ubuntu"|"Debian GNU/Linux")
        sudo apt-get update
        sudo apt-get install -y ffmpeg python3-pip
        sudo pip3 install --upgrade yt-dlp
        ;;
    "Fedora")
        sudo dnf install -y ffmpeg python3-pip
        sudo pip3 install --upgrade yt-dlp
        ;;
    *)
        echo "Unsupported OS. Please install ffmpeg and yt-dlp manually."
        exit 1
        ;;
esac

# Install Poetry if not already installed
if ! command -v poetry &> /dev/null; then
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install project dependencies
poetry install 

# Install service based on OS
if [ "$(uname)" == "Linux" ]; then
    echo "Installing Linux service..."
    sudo ./install_service_linux.sh
else
    echo "Installing Windows service..."
    ./install_service.bat
fi

echo "Setup complete!"