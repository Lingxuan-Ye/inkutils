#!/usr/bin/env bash

## create symbolic link for dotfiles
ln -s ~/inkutils/dotfiles/.bashrc ~/.bashrc
ln -s ~/inkutils/dotfiles/.gitconfig ~/.gitconfig

## create venv
rm -r -f ~/venv/ink/ && python -m venv ~/venv/ink/

## activate venv
source ~/venv/ink/Scripts/activate

## upgrade pip
pip install --upgrade pip

## install site-packages
pip install -r ./requirements.txt

# exit prompt
echo
read -p 'press any key to exit...' -n 1
