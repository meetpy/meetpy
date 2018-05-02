#!/bin/bash

function title {
    echo -e "\n\n\n" $1 "\n--------"
}


title "Add upstream remote"
git remote add upstream git@github.com:pykonik/pykonik.org.git
git fetch upstream

title "Create virtualenv"
virtualenv .pykonik-env
source ./.pykonik-env/bin/activate

title "Run pip install"
# currently there is no dev requirements file,
# but when there is – we should add it here.
pip install -r requirements/base.txt

cd pykonik/

title "Setup basic secrets"
mkdir pykonik/settings/pykonik_secret_variables


cat <<EOF > pykonik/settings/pykonik_secret_variables/base.json
{
    "ADMIN_EMAIL": "foo@example.com",
    "SECRET_KEY": "asdf",
    "ALLOWED_HOSTS": ["*"]
}
EOF

export DJANGO_SETTINGS_MODULE="pykonik.settings.local"

title "Run migrations"
./manage.py migrate

title "Run tests"
./manage.py test

title "Create superuser"
./manage.py createsuperuser

title "Runserver"
./manage.py runserver
