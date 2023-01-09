#!/usr/bin/env bash

# this script must be executed top level directory of 'inkutils'

# remove dotfile
rm -f ~/{.bashrc,.gitconfig,.inkonfig}

# deploy dotfiles
dir="$( python ./services/locate.py )"  # this creates '~/.inkonfig'
ln "$dir/dotfiles/.bashrc" ~/.bashrc
ln "$dir/dotfiles/.gitconfig" ~/.gitconfig

# create venv
rm -r -f ~/venv/ink/ && python -m venv ~/venv/ink/

# activate venv
source ~/venv/ink/Scripts/activate

# upgrade pip
pip install --upgrade pip

# install site-packages
pip install -r ./requirements.txt

# exit prompt
echo
read -p 'press any key to exit...' -n 1
