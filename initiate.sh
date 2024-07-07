#!/usr/bin/env bash
pip install -r requirements.txt
while [$? -eq 0]
do
  python -m updater
  sleep 300
done
