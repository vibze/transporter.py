'''

class Task(object):

    logger = get_logger()

    def __init__(self, **params):
        self.params = params

    def execute(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        self.logger.info('Running %s job.' % self.__module__)

        timer = Timer()
        try:
            self.execute(*args, **kwargs)
            self.logger.info('Done in %s' % timer)
        except Exception as e:
            self.logger.info('Error (after %s): %s' % (timer, e))

    def run_day(self, period):
        p = datetime.strptime(str(period), '%Y%m%d')

        self.logger.info('Running %s job for period %s' % (self.__module__, p.strftime('%d/%m/%Y')))

        timer = Timer()
        try:
            self.execute(p)
            self.logger.info('Done in %s' % timer)
        except Exception as e:
            self.logger.info('Error (after %s): %s' % (timer, e))

    def run_week(self, period):
        p = datetime.strptime(str(period), '%Y%m%d')
        d1 = p.replace(hour=00, minute=00, second=00) - timedelta(days=p.weekday())
        d2 = d1 + timedelta(days=7)

        self.logger.info('Running %s job for period range %s - %s' %
                         (self.__module__, d1.strftime('%d/%m/%Y'), d2.strftime('%d/%m/%Y')))

        timer = Timer()
        try:
            self.execute(d1, d2)
            self.logger.info('Done in %s' % timer)
        except Exception as e:
            self.logger.info('Error (after %s): %s' % (timer, e))

    def run_range(self, date_from, date_to):
        d1 = datetime.strptime(str(date_from), '%Y%m%d')
        d2 = datetime.strptime(str(date_to), '%Y%m%d')

        self.logger.info('Running %s job for period range %s - %s' %
                         (self.__module__, d1.strftime('%d/%m/%Y'), d2.strftime('%d/%m/%Y')))

        timer = Timer()
        try:
            self.execute(d1, d2)
            self.logger.info('Done in %s' % timer)
        except Exception as e:
            self.logger.info('Error (after %s): %s' % (timer, e))


    def run_all_time(self):
        self.logger.info('Running %s job for all periods' % self.__module__)
        timer = Timer()
        try:
            self.execute(datetime.strptime('1980-01-01', '%Y-%m-%d'), datetime.strptime('2050-01-01', '%Y-%m-%d'))
            self.logger.info('Done in %s' % timer)
        except Exception as e:
            self.logger.info('Error (after %s): %s' % (timer, e))

    def migrate_data(self, src_table_name, src_columns, dst_table_name, dst_columns, src_table_select_where=''):
        db = DB(**config.dwh_db)

        src_table = db.table(src_table_name)
        dst_table = db.table(dst_table_name)

        if isinstance(src_columns, str):
            src_columns = src_columns.replace(' ', '')
            src_columns = string.split(src_columns, ',')

        if isinstance(dst_columns, str):
            dst_columns = dst_columns.replace(' ', '')
            dst_columns = string.split(dst_columns, ',')

        aliases = []
        for dst_column in dst_columns:
            aliases.append(dst_column.replace('`', ''))

        if len(src_columns) == len(dst_columns):
            columns = []
            i = 0
            for src_column in src_columns:
                columns.append(src_column + ' as ' + aliases[i])
                i += 1

        rows = src_table.select(columns=columns, distinct=True, where=src_table_select_where, order=src_columns[0]+' ASC').all(as_dict=True)
        if rows:
            dst_table.upsert(rows)

        print 'Done (inserted to ' + dst_table_name + ')'

    def days_of_period_range(self, d1, d2):
        days = [d1]
        while d1 <= d2:
            d1 += timedelta(days=1)
            days.append(d1)
        return days

    def months_of_period_range(self, d1, d2):
        months = []
        current_m = d1.month
        current_y = d1.year
        while True:
            if current_m > 12:
                current_m = 1
                current_y += 1
            months.append(datetime(current_y, current_m, 1))
            current_m += 1
            if current_m > d2.month and current_y >= d2.year:
                break
        return months
'''