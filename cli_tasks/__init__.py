import os


def get_template_path(target):
    package_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return os.path.join(package_path, 'templates', target)


def create_module(dot_path):
    from transporter import settings
    full_path = os.path.join(settings.PROJECT_ROOT, os.path.join(*dot_path.split('.'))) + '.py'

    if os.path.exists(full_path):
        return full_path

    dirs = [settings.PROJECT_ROOT]
    for segment in dot_path.split('.')[:-1]:
        dirs.append(segment)
        path = os.path.join(*dirs)

        if not os.path.exists(path):
            os.mkdir(path)

        init_file = os.path.join(path, '__init__.py')
        if not os.path.exists(init_file):
            touch(init_file)

    return full_path


def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()