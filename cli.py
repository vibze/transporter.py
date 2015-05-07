import importlib
import shutil
import sys

import os
import click


SETTINGS_ENV_VARIABLE = "TRANSPORTER_SETTINGS_MODULE"


@click.group()
def cli():
    sys.path.insert(1, os.getcwd())


@cli.command()
@click.argument('name', nargs=1)
def new(name):
    package_path = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(package_path, 'new_project_template')
    working_path = os.path.join(os.getcwd(), name)

    try:
        click.echo('Creating new project structure %s' % name)
        shutil.copytree(template_path, working_path)
    except OSError as e:
        raise


@cli.command()
@click.option('--settings', default='config')
@click.argument('job', required=True)
@click.argument('params', nargs=-1)
def run(settings, params, job):
    os.environ[SETTINGS_ENV_VARIABLE] = settings

    job = importlib.import_module(job)
    kwargs = dict(param.split('=') for param in params)

    job.run(**kwargs)


@cli.command()
@click.option('--settings', default='settings')
@click.argument('host', nargs=1, default='0.0.0.0:5000')
def monitor(settings, host):
    from transporter.web import app

    os.environ[SETTINGS_ENV_VARIABLE] = settings
    click.echo(" * Transporter monitor starting...")

    ip, port = host.split(':')
    app.run(ip, port=int(port))