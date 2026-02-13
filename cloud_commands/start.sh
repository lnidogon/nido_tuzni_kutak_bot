#!/bin/bash

set -e

echo "Activating venv..."
source venv/bin/activate

echo "Updating dependencies..."
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
fi

echo "Starting the Gori-Bot..."
sudo systemctl start discordbot

echo "Bot status:"
sudo systemctl status discordbot --no-pager