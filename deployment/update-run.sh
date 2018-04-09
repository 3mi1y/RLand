#!/bin/sh

rland_dir=$HOME/rland

source "$HOME/.nvm/nvm.sh"
source "$HOME"/venv/bin/activate

cd "$rland_dir"
git pull

cd "$rland_dir"/ember-proj
npm install
bower install
ember build

cd "$rland_dir"/server
python serve2.py --port=8080
