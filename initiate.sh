#!/usr/bin/env bash
pip install -U pip
pip install -r requirements.txt
#while :
#do
#  python -m updater
#  sleep 300
#done
for i in $(seq 1 288);
do
	echo $i
	python -m updater
	sleep 300
done
