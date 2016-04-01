from datetime import datetime
import sys
from transporter.job_record import JobLog


def transporter_job(func):
    def inner(*args, **kwargs):
        log = JobLog('%s.%s' % (sys.modules[func.__module__], func.__name__))
        log.start = datetime.now()
        result = func(*args, **kwargs)
        log.end = datetime.now()
        log.save()
        return result

    return inner