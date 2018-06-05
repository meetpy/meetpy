#!/bin/bash

function title {
    echo -e "\n\n\n" $1 "\n--------"
}


title "Add upstream remote"
git remote add upstream git@github.com:pykonik/pykonik.org.git
git fetch upstream

title "Create virtualenv"
virtualenv -p python3 .meetpy-env
source ./.meetpy-env/bin/activate

title "Run pip install"
# currently there is no dev requirements file,
# but when there is – we should add it here.
pip install -r requirements/base.txt

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
./manage.py migrate

title "Run tests"
pytest

title "Create superuser"
./manage.py createsuperuser

title "Runserver"
./manage.py runserver
