class Job(object):
    WORKING = "WORKING"

    def __init__(self):
        self.status = self.WORKING

    @classmethod
    def run(cls, *args, **kwargs):
        return cls().run(*args, **kwargs)

    def run(self, *args, **kwargs):
        print "Error! Method run for this class must be overriden"
