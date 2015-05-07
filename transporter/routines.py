from datetime import datetime


def run_day(job):
    def routine():
        p = datetime.strptime(str(period), '%Y%m%d')

        return func(*args)

    return routine


    self.logger.info('Running %s job for period %s' % (self.__module__, p.strftime('%d/%m/%Y')))

    timer = Timer()
    try:
        self.execute(p)
        self.logger.info('Done in %s' % timer)
    except Exception as e:
        self.logger.info('Error (after %s): %s' % (timer, e))
