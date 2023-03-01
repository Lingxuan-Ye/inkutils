#!/usr/bin/env bash

# this script must be executed top level directory of 'inkutils'

python ./services/deploy.py

# exit prompt
echo
read -p 'Press any key to exit...' -n 1
