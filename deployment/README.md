# Installation

## Riak
Either install via the [installation instructions](http://docs.basho.com/riak/kv/2.2.3/setup/installing/)
or [in a docker container](http://basho.com/posts/technical/running-riak-in-docker/).

`docker run --name=riak -d -p 8087:8087 -p 8098:8098 basho/riak-kv`

## RLand
| | |
| --- | --- |
| Set up a new user to run rland under	| `useradd -m rland`
| Login to the rland user		| `sudo -iu rland`
| Deploy the rland files		| via git clone, file upload, etc.

## Python
| | |
| --- | --- |
| Create the python virtualenv		| `python -m venv venv`
| Go in the rland folder		| `cd rland`
| Install the python dependencies	| `pip install -r requirements.txt`

## Node
| | |
| --- | --- |
| Install nvm	| `curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash`
| Install nodejs via nvm	| `nvm install lts/carbon`
| Activate nvm nodejs		| `nvm use lts/carbon`
| Go into the ember folder	| `cd ember-proj`
| Install ember-cli		| `npm install -g ember-cli`
| Install bower			| `npm install -g bower`
| Install rland dependencies	| `npm install`
| Install rland’s bower dependencies	| `bower install`
| Build rland’s ember project	| `ember build`

## System configuration
Sample configuration for deployment with nginx and systemd services are
provided (`riak.service` and `rland.service`).  This systemd unit for riak
starts riak via docker; in a direct installation of riak an appropriate init
script or systemd service should already be provided by riak itself.

The port number in `rland.nginx.conf` should match the one that `serve2.py` is
run with.

`update-run.sh` performs a full re-deployment by updating a git checkout, building the
ember project, and starting the tornado server.
