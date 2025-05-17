#!/usr/bin/env bash
echo "updating pip"
pip install --root-user-action ignore -U pip setuptools wheel
echo "installing reqs"
pip install --root-user-action ignore -U -r requirements.txt
echo "running check"
python -u -m updater
echo "sleeping"
sleep 300
exit 0
