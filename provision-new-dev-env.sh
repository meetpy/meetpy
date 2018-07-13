#!/bin/bash

function title {
    echo -e "\n\n\n" $1 "\n--------"
}


title "Add upstream remote"
git remote add upstream git@github.com:pykonik/pykonik.org.git
git fetch upstream

title "Create virtualenv via pipenv"
pipenv --python 3.7

title "Run pip install"
pipenv install --dev

cd meetpy/

title "Setup basic secrets"
mkdir -p meetpy/settings/meetpy_secret_variables


SECRETS_FILE="meetpy/settings/meetpy_secret_variables/base.json"
[[ -e $SECRETS_FILE ]] || cat <<EOF > $SECRETS_FILE
{
    "ADMIN_EMAIL": "foo@example.com",
    "SECRET_KEY": "asdf",
    "ALLOWED_HOSTS": ["*"]
}
EOF

export DJANGO_SETTINGS_MODULE="meetpy.settings.local"

title "Run migrations"
pipenv run ./manage.py migrate

title "Run tests"
pipenv run pytest

title "Create superuser"
pipenv run ./manage.py createsuperuser

title "Runserver"
pipenv run ./manage.py runserver
