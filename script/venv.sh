#!/usr/bin/env bash

if [[ $# -eq 0 ]]; then
    source ~/venv/ink/Scripts/activate
elif [[ "$1" != "-m" ]]; then
    source ~/venv/"$1"/Scripts/activate
else
    python -m venv ${@:2}
fi
