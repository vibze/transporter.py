import importlib
import shutil
import sys

import os
import click
from inflection import camelize
from transporter import log


SETTINGS_ENV_VARIABLE = "TRANSPORTER_SETTINGS_MODULE"
JOB_ENV_VARIABLE = "TRANSPORTER_JOB_NAME"


@click.group()
def cli():
    sys.path.insert(1, os.getcwd())


@cli.command()
@click.option('--settings', default='config')
@click.argument('name', nargs=1)
def create_project(settings, name):
    from cli_tasks import get_template_path
    template_path = get_template_path('new_project_template')
    working_path = os.path.join(os.getcwd(), name)

    try:
        click.echo('Creating new project structure %s' % name)
        shutil.copytree(template_path, working_path)
    except OSError as e:
        raise


@cli.command()
@click.option('--settings', default='config')
@click.argument('task', nargs=1, default='job')
def new(settings, task):
    """ New job/datastore, you will be prompted. """
    os.environ[SETTINGS_ENV_VARIABLE] = settings

    from cli_tasks.create_datastore import create_datastore
    from cli_tasks.create_job import create_job

    if task == 'datastore':
        create_datastore()

    if task == 'job':
        create_job()


@cli.command()
@click.option('--settings', default='config')
@click.argument('job_name', required=True)
@click.argument('params', nargs=-1)
def run(settings, params, job_name):
    """ Run a job (example: run jobs.do_this) """
    os.environ[SETTINGS_ENV_VARIABLE] = settings
    os.environ[JOB_ENV_VARIABLE] = job_name

    job = importlib.import_module(job_name)
    kwargs = dict(param.split('=') for param in params)

    try:
        from transporter import settings as s
        from transporter import log
        if s.YELL_JOBS_RUN:
            log.info('Running job %s' % job)
        if hasattr(job, 'run'):
            job.run(**kwargs)
        else:
            job_class_name = camelize(job.__name__.split('.')[-1])  # Try to find camelized module title class
            if hasattr(job, job_class_name):
                job_class = getattr(job, job_class_name)
                job_class().run(**kwargs)

    except Exception as e:
        log.exception(e)


@cli.command()
@click.option('--settings', default='config')
@click.argument('host', nargs=1, default='0.0.0.0:5000')
def server(settings, host):
    """ Run transporter server """
    from transporter.server import app

    os.environ[SETTINGS_ENV_VARIABLE] = settings
    click.echo(" * Transporter monitor starting...")

    ip, port = host.split(':')
    app.debug = True
    app.run(ip, port=int(port))
