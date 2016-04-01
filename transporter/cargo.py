class Cargo(object):
    CURSOR = 1

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    def chunk(self, chunksize=50000):
        return self.cursor.fetchmany(chunksize)

    @property
    def size(self):
        return self.cursor.rowcount