from datetime import datetime
import logging
import os
from peewee import *
from transporter import settings


def global_logger(log_file=None):
    log_file = log_file.replace('{exec_time}', datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.environ["TRANSPORTER_LOGGER"] = '%s' % log_file
    return logger()


def logger(log_file=None):
    log_file = os.environ.get("TRANSPORTER_LOGGER", log_file)

    if log_file:
        log_file = log_file.replace('{exec_time}', datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
        logger_name = 'transporter_job_logger(%s)' % log_file
    else:
        logger_name = 'transporter_job_logger'

    logger = logging.getLogger(logger_name)

    if len(logger.handlers) != 0:
        return logger

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    if log_file:
        log_file_path = os.path.join(settings.LOG_ROOT, log_file)
        fh = logging.FileHandler(log_file_path)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    logger.setLevel(logging.INFO)
    return logger


class JobLog(Model):
    job = CharField()
    status = TextField(default='')
    started_at = DateTimeField()
    ended_at = DateTimeField()

    def __init__(self, job):
        super(JobLog, self).__init__()
        self.log = logger()
        self.job = job

    def start(self, message=None):
        self.started_at = datetime.now()

        if message:
            self.status = message
        else:
            self.status = 'Starting job %s' % self.job

    def put(self, message):
        # TODO: Log output should be appended to status
        self.status += '\n'
        self.status += message

    def end(self, message=None):
        self.ended_at = datetime.now()

        if message:
            self.status += '\n* * *\n'
            self.status += message

        self.save()

    class Meta:
        database = SqliteDatabase(settings.DATABASE, threadlocals=True)
