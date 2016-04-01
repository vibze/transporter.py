import os
import click
from cli_tasks import get_template_path


def create_datastore():
    available_types = ['mysql', 'oracle', 'ssh']

    type_index = click.prompt(
        '\nWhich type datastore do you want to create?\n'
        '1) MySQL\n'
        '2) Oracle\n'
        '3) SSH\n'
        'Enter number',
        type=int
    )

    try:
        ds_type = available_types[type_index-1]
        template_path = get_template_path('%s.py' % ds_type)
    except IndexError:
        return click.echo('Provided number is not in list of available options. Aborting task...')

    datastore_name = click.prompt('Enter a name for the new datastore', type=str)
    target_path = os.path.join(os.getcwd(), 'datastores', '%s.py' % datastore_name)

    if os.path.exists(target_path):
        return click.echo('Datastore with given name already exists in your project. Aborting task...')

    try:
        click.echo('\nCreating new datastore %s of type %s' % (datastore_name, ds_type))

        source_file = open(template_path, 'r')
        target_file = open(target_path, 'w')

        target_file.write(source_file.read().replace('DataStoreNameGoesHere', datastore_name))
        target_file.close()
        source_file.close()
        click.echo('Proceed to configure datastores/%s.py at your project' % datastore_name)
    except OSError as e:
        raise