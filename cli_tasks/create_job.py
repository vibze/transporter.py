import os
import click
from cli_tasks import get_template_path, create_module
from transporter import settings


def create_job():
    job = click.prompt('\nEnter name for the job')

    target_path = create_module('jobs.' + job)

    if os.path.exists(target_path):
        return click.echo('Job %s already exists. Aborting task...' % job)

    try:
        click.echo('\nCreating new jobs %s' % job)

        source_file = open(get_template_path('job.py'), 'r')
        target_file = open(target_path, 'w')

        target_file.write(source_file.read().replace('JobNameGoesHere', job))

        source_file.close()
        target_file.close()

        click.echo('\nProcess to write the job')
    except OSError:
        raise