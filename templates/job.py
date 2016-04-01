from transporter.job_record import logger
from transporter.decorators import transporter_job
from transporter.utils import Timer


# Configure your data sources here
# source = SomeDB()
# target = MyDB()
log = logger('JobNameGoesHere_{exec_time}.log')


@transporter_job
def run():
    """
    JobNameGoesHere

    About this job...
    """
    # Simple job example:
    # log.info('Selecting a user data from table users')
    #
    # cargo = source.execute('SELECT * FROM users WHERE MONTH(date_from) = MONTH(NOW())')
    # target.load(cargo)
    #
    # log.info('Loaded %s rows' % cargo.size)