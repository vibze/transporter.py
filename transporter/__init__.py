from datetime import datetime
import importlib
import logging
import os
from job import Job


class Settings(object):
    configured = False

    def __getattribute__(self, item):
        try:
            attribute = object.__getattribute__(self, item)
        except AttributeError:
            self.configure()
            attribute = object.__getattribute__(self, item)

        return attribute

    def configure(self):
        self.SETTINGS_MODULE = os.environ.get("TRANSPORTER_SETTINGS_MODULE")
        self.PROJECT_ROOT = os.getcwd()
        self.JOBS_ROOT = os.path.join(self.PROJECT_ROOT, 'jobs')
        self.LOGS_ROOT = os.path.join(self.PROJECT_ROOT, 'logs')
        self.LOG_FILE = None
        self.LOGGER = None

        self.MONITOR_LOGIN = 'admin'
        self.MONITOR_PASSWORD = 'password'

        self.YELL_JOBS_RUN = False

        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)
            for setting in dir(mod):
                if setting.isupper():
                    setting_value = getattr(mod, setting)
                    setattr(self, setting, setting_value)

            self.configured = True
        except AttributeError:
            raise RuntimeError("Settings not found: %s" % self.SETTINGS_MODULE)


class Logger(object):
    initialized = False

    def __init__(self):
        self.logger = None

    def info(self, *args, **kwargs):
        if self.logger is None:
            self.initialize()

        self.logger.info(*args, **kwargs)

    def error(self, *args, **kwargs):
        if self.logger is None:
            self.initialize()

        self.logger.error(*args, **kwargs)

    def exception(self, *args, **kwargs):
        if self.logger is None:
            self.initialize()

        self.logger.exception(*args, **kwargs)

    def initialize(self):
        log_file = os.environ.get("TRANSPORTER_JOB_NAME", None)

        if log_file is None:
            raise "Transporter job not set"

        log_file += '_%s.log' % datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        logger = logging.getLogger('transporter_job_logger')

        if len(logger.handlers) == 0:
            formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
            sh = logging.StreamHandler()
            sh.setFormatter(formatter)
            logger.addHandler(sh)

            log_file_path = os.path.join(settings.LOG_ROOT, log_file)
            fh = logging.FileHandler(log_file_path)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

        logger.setLevel(logging.INFO)
        self.logger = logger

settings = Settings()
log = Logger()

from transporter.classes.manager import Manager
manager = Manager()