#!/usr/bin/env bash

## create venv
python -m venv ../venv

## activate venv
source ../venv/Scripts/activate

## upgrade pip
pip install --upgrade pip

## install site-packages
pip install -r ./requirements.txt

echo
read -p 'press any key to exit...' -n 1
