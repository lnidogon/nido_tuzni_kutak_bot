#!/bin/bash

set -e

bash stop.sh

echo "Updating code from GitHub..."
cd /home/ubuntu/nido_tuzni_kutak_bot
git pull

bash start.sh
