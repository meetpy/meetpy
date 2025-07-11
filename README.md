## Meetpy

[![Build Status](https://github.com/meetpy/meetpy/actions/workflows/ci.yml/badge.svg?branch=master)](https://github.com/meetpy/meetpy/actions/workflows/ci.yml)

Meetpy website - this is a shared website along polish Python meetup groups.

For example:

 - http://pywaw.org/
 - http://pykonik.org
 - https://www.pythonlodz.org/

## Local install and setup

### Manual installation on linux

Before the next step, be sure the following OS libraries are installed:

 - g++
 - libjpeg-dev
 - zlib-dev
 - python-dev

You can run `provision-new-dev-env.sh` on your dev environment – it will create
everything necessary (using virtualenv) for basic development.


### Docker

Alternatively you can use Docker and Docker Compose.
They will setup a container with meetpy Django app
(available at http://localhost:18000), a Postgres database with a PhpPgAdmin
interface (available at http://localhost:8082) and a mock of SMTP service
(available at http://localhost:8081).

For docker:
 - `docker compose -f compose.yaml up`
 - `docker compose -f compose.yaml exec meetpy python manage.py migrate`

*NOTE*

Tested on:

 - Docker versions 28.1.1
 - Docker Compose version v2.35.1

Consult https://docs.docker.com/install/ and https://docs.docker.com/compose/install/ for
instructions how to install docker.

For more info read the `provision-new-dev-env.sh`, `compose.yaml` or ask us on discord:

https://discord.pykonik.org

## Contributing

1. Make a fork of `https://github.com/meetpy/meetpy`
2. Make changes in your fork (ideally on a feature/bugfix branch)
3. Make sure your branch is based on latest `upstream/master` (`git fetch
   upstream`) (`provision-new-dev-envirionment.sh` adds `meetpy/meetpy` as `upstream`)
4. Push your changes.
5. Create a pull request to meetpy/meetpy, targeting master.

# New group

1. Copy `meetpy.settings.group_constants.constants.default.yaml` to `meetpy.settings.group_constants.constants.<meetup_name>.yaml`
2. Fill in the data for your group.
3. In case you need different templates, create `templates/<group_name>` directory and put any templates you'd like.
4. Execute with `MEETUP_NAME=<group_name> command`