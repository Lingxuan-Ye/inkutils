#!/usr/bin/env bash

shopt -s globstar

rm -rf **/.mypy_cache/ **/__pycache__/

read -p "press any key to exit..." -n 1
