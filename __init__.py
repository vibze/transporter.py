from datetime import datetime
import sys


def job(func):
    def inner(*args, **kwargs):
        log = JobLog()
        log.start = datetime.now()
        result = func(*args, **kwargs)
        log.job = '%s.%s' % (sys.modules[func.__module__], func.__name__)
        log.end = datetime.now()
        log.save()
        return result

    return inner