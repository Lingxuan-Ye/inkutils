#!/usr/bin/env bash

shopt -s globstar
rm -rf **/.mypy_cache
rm -rf **/__pycache__
read -p "press any key to exit..." -n 1
