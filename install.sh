#!/usr/bin/env bash

set -e

pip3 install -r requirements.txt

python3 prepare_service.py

if [ "$(uname)" == "Darwin" ]; then
    launchctl unload check_repos.plist
    launchctl load check_repos.plist
else
    sudo cp check_repos.service /etc/systemd/system

    sudo systemctl stop check_repos.service
    sudo systemctl disable check_repos.service
    sudo systemctl enable check_repos.service
    sudo systemctl daemon-reload
    sudo systemctl start check_repos.service
fi

echo "Service installed and started"