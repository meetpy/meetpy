## Meetpy
[![Build Status](https://travis-ci.org/meetpy/meetpy.svg?branch=master)](https://travis-ci.org/meetpy/meetpy)

Meetpy website - this is a shared website along polish Python meetup groups.

For example:
http://pywaw.org/
http://pykonik.org
https://www.pythonlodz.org/


## Local install and setup
For linux:
Before the next step, be sure the following OS libraries are installed.
 - g++
 - libjpeg-dev
 - zlib-dev
 - python-dev

You can run `provision-new-dev-envirionment.sh` on your dev environment – it will create
everything necessary (using virutalenv) for basic development.

Alternatively you can use Docker and Docker Compose:
`docker-compose up` it will setup a container with meetpy Django app
(available at http://localhost:8080), a Postgres database with a PhpPgAdmin
interface (available at http://localhost:8082) and a mock of SMTP service
(available at http://localhost:8081).

For more info read the script, or ask us on slack.

https://pykonik.slack.com/ or https://join-slack.pykonik.org/

For docker:
 - docker-compose -f docker-compose-dev.yml up


## Contributing

1. Make a fork of `https://github.com/meetpy/meetpy`
2. Make changes in your fork (ideally on a feature/bugfix branch)
3. Make sure your branch is based on latest `upstream/master` (`git fetch
   upstream`) (`provision-new-dev-envirionment.sh` adds `meetpy/meetpy` as `upstream`)
4. Push your changes.
5. Create a pull request to meetpy/meetpy, targeting master.
