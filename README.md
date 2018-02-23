# RLand

## Installing (details being worked out)
* Ubuntu 16.04 is the best option
* Riak has instructions for Ubuntu 16.04
* ember.js needs a newer node.js version than Ubuntu has (use something like `nvm` to install a node.js version)
* python3 and tornado, and other python libraries required. virtualenv recommended. `pip3 install -r requirements.txt`

## Running
In the `ember-proj` folder:
`ember build -w`

In the `server` folder:
`python3 serve2.py`

## Resetting the Database contents
In the `server` folder:
`python3 reset_db.py`

## Testing
In the `server` folder:
`python3 -m unittest`
