#!/usr/bin/env bash
pip install -U pip
pip install --root-user-action ignore -U -r requirements.txt
python -u -m updater
sleep 300
exit 0
