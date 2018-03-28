# RLand

## Dependencies Overview
RLand is built using ember.js (node.js) for the client application,
tornado (python) for the application server, and riak for the database.
Each of these components has other dependencies that must be installed on
the development/deployment machine.

### Riak
Riak provides [installation instructions](http://docs.basho.com/riak/kv/2.2.3/setup/installing/)
for several operating systems, including several Ubuntu LTS releases and
RHEL/CentOS. Building from source is time-consuming and prone to failure, as
Riak uses an old version of Erland with custom patches. Installing from
a third-party repository or running via docker is recommended.

### Ember.js
Ember.js requires at least version 4.5 of node.js, which is not in
Ubuntu's repositories as of the 16.04 LTS release. [`nvm`](https://github.com/creationix/nvm/)
is recommended for installing a private copy of any version of node.js
if the target platform does not support a recent enough version.

### Python
The RLand server code is written in Python 3 using the Tornado framework
and other dependences. A [python virtualenv](https://docs.python.org/3/library/venv.html)
is recommended to isolate these dependences from the rest of the system.

## Installation
* Recommended Operating System: Ubuntu 16.04
* Install Riak according to the official installation guide or via docker
* Install node.js via `nvm`. RLand is currently tested on the 'carbon'
  LTS branch.
  * Activate the nvm-installed node.js, and use `npm -g` to install
    `ember-cli` and `bower`
  * In the `ember-proj` folder: `npm install; bower install`
* Install python 3. Create a python virtualenv and activate it.
  * RLand dependencies can be installed by running `pip install -r requirements.txt`

## Developing and Running
In the `ember-proj` folder: `ember build`. `ember build -w` can be used
to automatically rebuild the ember project as files are written to.

In the `server` folder: `python3 serve2.py`

### Resetting the Database contents
In the `server` folder: `python3 reset_db.py`

### Running Tests
In the `server` folder: `python3 -m unittest`
