#!/bin/bash
sudo apt -y install python3.9
sudo apt -y install python3-pip
pip3 install --upgrade pip
pip3 install virtualenv
$HOME/.local/bin/virtualenv -p /usr/bin/python3.9 venv
. venv/bin/activate
pip3 install -r requirements.txt
kill $(ps -ef | grep /app/app.py | grep -v grep | awk '{print $2}') || true
nohup python3 app/app.py > log.txt 2>&1 &