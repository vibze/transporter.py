from datetime import datetime
import inspect
import logging
from peewee import *
from sqlalchemy import Column, Integer, String, DateTime
from transporter import settings

def logger():
    logger = logging.getLogger('Transporter Job Logger')
    if len(logger.handlers) != 0:
        return logger

    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    if settings.LOG_FILE:
        fh = logging.FileHandler(settings.LOG_FILE)
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
