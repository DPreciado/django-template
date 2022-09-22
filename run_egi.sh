#!/bin/bash
source venv/bin/activate
python3 -W ignore manage.py runsslserver 0.0.0.0:3000 --certificate /etc/letsencrypt/live/egi.systems/fullchain.pem  --key /etc/letsencrypt/live/egi.systems/privkey.pem
