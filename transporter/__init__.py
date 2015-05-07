import importlib
import os


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
        self.LOG_FILE = None

        self.MONITOR_LOGIN = 'admin'
        self.MONITOR_PASSWORD = 'password'

        try:
            mod = importlib.import_module(self.SETTINGS_MODULE)
            for setting in dir(mod):
                if setting.isupper():
                    setting_value = getattr(mod, setting)
                    setattr(self, setting, setting_value)

            self.configured = True
        except AttributeError:
            raise RuntimeError("Settings not found: %s" % self.SETTINGS_MODULE)


settings = Settings()

from job_record import JobLog as Log