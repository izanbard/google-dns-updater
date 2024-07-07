#!/usr/bin/env bash
pip install -r requirements.txt
while :
do
  python -m updater
  sleep 300
done
