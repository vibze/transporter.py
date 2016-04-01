import os
from time import time
from transporter import settings


class Timer:
    def __init__(self):
        self.reset()

    def __str__(self):
        return self.readable_time(time() - self.start)

    def readable_time(self, secs):
        t = ''
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        if hours > 0: t+= '%ih '%hours
        if mins > 0: t+= '%im '%mins
        if secs > 0: t+= '%is '%secs
        return t.strip()

    def sec(self):
        return time() - self.start

    def reset(self):
        self.start = time()


def open_file(path, mode='r'):
    return open(os.path.join(settings.PROJECT_ROOT, path), mode)

def file_url(path):
    return 'file:///' + os.path.join(settings.PROJECT_ROOT, path)