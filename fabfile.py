from fabric.api import run, cd, env, abort
from fabric.context_managers import prefix
from fabric.contrib.console import confirm

env.hosts = ['pywaw@pywaw.org']

env.project_name = 'pywaw'

env.settings = ['staging']

env.hot_settings = []

env.branches = {
    'staging': 'default',
}


def deploy(settings='staging'):
    if settings not in env.settings:
        abort('Invalid settings.')
    if settings in env.hot_settings and not confirm('Do you really want to deploy?'):
        abort('Aborting!')
    with prefix('source ~/apps/{0}_{1}/env/bin/activate'.format(env.project_name, settings)):
        with cd('~/apps/{0}_{1}/repo/'.format(env.project_name, settings)):
            run('hg pull')
            run('hg update --clean {0}'.format(env.branches[settings]))
            run('pip install -q -r requirements/{0}.txt'.format(settings))
            with cd(env.project_name):
                run('./manage.py collectstatic --settings={0}.settings.{1} --noinput'.format(env.project_name, settings))
                run('./manage.py syncdb --settings={0}.settings.{1} --noinput'.format(env.project_name, settings))
                run('./manage.py migrate --settings={0}.settings.{1} --noinput'.format(env.project_name, settings))
            run('appctl restart {0}_{1}'.format(env.project_name, settings))
