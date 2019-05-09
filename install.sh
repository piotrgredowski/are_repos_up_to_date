#!/usr/bin/env bash

set -e

pip3 install -r requirements.txt

python3 prepare_service.py

sudo cp check_repos.service /etc/systemd/system

sudo systemctl stop check_repos.service
sudo systemctl disable check_repos.service
sudo systemctl enable check_repos.service
sudo systemctl daemon-reload
sudo systemctl start check_repos.service

echo "Service installed and started"