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

### Windows
If you use Windows operation system open command line then checkout the repository on github.com/meetpy/meetpy
and clone the link to your terminal and create at the same time new folder. It should look like this (for example):
git@github.com:meetpy/meetpy.git meetpy2
Open your code editor (for example PyCharm) and open the folder which you created.
Open the terminal in your code editor and run following commands:
1) virtualenv .meetpy-env
2) .meetpy-env\Scripts\activate
Next in file requirements\base.txt delete Pillow
and then find and change all ImageField in meetups\models.py and misc\models.py for FileField
Next run in terminal:
1) pip install -r requirements/base.txt
2) cd meetpy
3) set DJANGO_SETTINGS_MODULE=meetpy.settings.local
4) set PYTHON_PATH=.
Next in command line (not in code editor!) go into your folder with manage.py file and run:
1) python manage.py migrate
2) python manage.py createsuperuser
3) write some login (e-mail is blank) and password
4) python manage.py runserver

### Docker
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
