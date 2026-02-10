#!/bin/bash

set -e

echo "Stopping bot service..."
sudo systemctl stop discordbot

echo "Updating code from GitHub..."
cd /home/ubuntu/nido_tuzni_kutak_bot
git pull

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing/updating dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "Starting bot service..."
sudo systemctl start discordbot

echo "Bot status:"
sudo systemctl status discordbot --no-pager
