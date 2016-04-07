import imp
import importlib
from inflection import camelize
from datetime import datetime
import os
from transporter import settings


class JobFile(object):
    def __init__(self, project_path):
        self.path = os.path.join(settings.JOBS_ROOT, project_path)
        self.project_path = project_path

        self.ref = 'jobs.' + project_path.replace(os.sep, '.')[:-3]
        self.module = self.import_module()
        self.doc = self.module.__doc__

        if hasattr(self.module, 'run'):
            self.type = 'function'
        else:
            job_class_name = camelize(self.module.__name__.split('_')[-1])  # Try to find camelized module title class
            if hasattr(self.module, job_class_name):
                job_class = getattr(self.module, job_class_name)
                self.type = 'class'

    def import_module(self):
        import_id = self.ref.replace('.', '_')
        return imp.load_source(import_id, self.path)

    @property
    def contents(self):
        f = open(self.path)
        return f.read()


class LogFile(object):
    def __init__(self, project_path):
        self.path = os.path.join(settings.LOGS_ROOT, project_path)
        self.project_path = project_path

        data_string = self.path.split(os.sep)[-1][:-4]  # Get just the log file name without extension
        self.job_ref = data_string.split('_')[0]
        self.time = datetime.strptime(data_string.split('_')[1], '%Y-%m-%d-%H-%M-%S')

    @property
    def contents(self):
        f = open(self.path)
        return f.read()

class Manager(object):
    def all_jobs(self):
        jobs = []
        for root, dirs, files in os.walk(settings.JOBS_ROOT):
            for f in files:
                if f != '__init__.py' and f.endswith('.py'):
                    filepath = os.path.join(root, f).replace(settings.JOBS_ROOT, '')[1:]
                    jobs.append(JobFile(filepath))

        return jobs

    def all_logs(self):
        logs = []
        for root, dirs, files in os.walk(settings.LOGS_ROOT):
            for f in files:
                if f.endswith('.log'):
                    filepath = os.path.join(root, f).replace(settings.LOGS_ROOT, '')[1:]
                    try:
                        logs.append(LogFile(filepath))
                    except ValueError:
                        pass

        return logs

    # TODO: Implement
    # run_job
    # list_logs
    # delete_log(path)
    # stop_job(id)
