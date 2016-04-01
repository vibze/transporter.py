import hashlib
import random
import os
import sys, traceback
from datetime import date, datetime
from transporter import settings
from transporter.interfaces.transporter_csv import CSV


class Table(object):
    def __init__(self, db, name):
        self.db = db
        self.name = name
        self._has_id_column = None

    @property
    def has_id_column(self):
        if self._has_id_column is None:
            self._has_id_column = 'id' in self.columns

        return self._has_id_column

    @property
    def columns(self):
        return [c[0] for c in self.db.execute('select * from %s limit 1' % self.name).description]

    def delete(self, where=None):
        if where is not None:
            where_stmt = 'where ' + where if where else ''
            self.db.execute('DELETE FROM %s %s' % (self.name, where_stmt))
        else:
            self.db.execute('TRUNCATE %s' % self.name)

    def delta(self, cargo):
        temp = '%s_temp_%s' % (self.name, random.randrange(1001, 9999))
        self.db.execute('create temporary table %s like %s' % (temp, self.name))

        self.load_via_infile(cargo, table=temp)
        delta = self.db.execute('select * from %s where id not in (select id from %s)' % (temp, self.name)).fetchall()
        self.db.execute('drop table %s' % temp)

        return delta

    def load(self, data):
        if not data:
            return 0
        count = len(data)
        data = '),('.join([','.join([self.q(column) for column in row]) for row in data])

        statement = 'INSERT INTO %s VALUES(%s)' % (self.name, data.decode('utf8'))
        try:
            self.db.execute(statement)
            return count
        except:
            print 'ERROR: %s' % (statement)
            print traceback.format_exc().splitlines()[-1]
            return 0

    def load_via_infile(self, cargo, chunksize=50000, flags='REPLACE', table=None):
        filepath = os.path.join(settings.TMP_ROOT, hashlib.sha224(cargo.statement).hexdigest()+'.dat')
        csv = CSV()
        rows = 0
        while True:
            chunk = cargo.chunk(chunksize)
            if not chunk:
                break

            rows += len(chunk)
            csv.dump(chunk, filepath)
            self.load_infile(filepath, flags=flags, table=table)

        if os.path.exists(filepath):
            os.unlink(filepath)

        return rows

    def load_infile(self, filepath, cols='', flags='REPLACE', table=None):
        if cols:
            cols = '(%s)' % (','.join(cols))

        if not table:
            table = self.name

        return self.db.execute('''
            LOAD DATA INFILE '%s' %s INTO TABLE %s
            FIELDS ENCLOSED BY '"'
            LINES TERMINATED BY '\r\n'
            %s;''' % (filepath.replace('\\', '/'), flags, table, cols)
        )

    def index_exists(self, name):
        self.db.execute('SHOW INDEX FROM %s WHERE key_name = "%s"' % (self.name, name))
        return len(self.db.cursor.fetchall())

    def add_index(self, col, index):
        if not self.index_exists(index):
            self.db.execute('CREATE INDEX %s ON %s (%s)' % (index, self.name, col))

    def add_column(self, column, type):
        if column not in self.columns:
            self.db.execute('ALTER TABLE %s ADD %s %s' % (self.name, column, type))

    def clear_column(self, column):
        if column in self.columns:
            self.db.execute('UPDATE %s SET %s = NULL' % (self.name, column))

    def table_exists(self):
        self.db.execute('select count(*) from information_schema.tables where table_name = "%s"' % self.name)
        return self.db.cursor.fetchone()[0] > 0

    def drop_column(self, column):
        if column in self.columns:
            self.db.execute('ALTER TABLE %s DROP COLUMN %s' % (self.name, column))

    def add_partition(self, partition):
        self.db.execute('ALTER TABLE %s ADD PARTITION (PARTITION %s)' % (self.name, partition))

    def drop_partition(self, partition):
        try:
            self.db.execute('ALTER TABLE %s DROP PARTITION %s' % (self.name, partition))
        except:
            pass

    def insert_record(self, **kwargs):
        columns = []
        values = []

        for key, value in kwargs.iteritems():
            columns.append(key)
            values.append(value)

        statement = 'INSERT INTO %s (%s) VALUES (%s)' % (self.name, ','.join(columns), ','.join(map(self.db.esc, values)))
        self.db.execute(statement)

        if self.has_id_column:
            r = self.db.execute('SELECT MAX(id) FROM %s' % self.name)
            return r.fetchone()[0]
        else:
            return True

    def rows(self):
        return self.db.execute('SELECT * FROM %s' % self.name)

    def q(self, value):

        if isinstance(value, str):
            value = value.replace("'", '"')
            return "'%s'" % value

        if isinstance(value, unicode):
            value = value.encode('utf8').replace("'", '"')
            return "'%s'" % value

        if isinstance(value, datetime):
            return self.q(value.isoformat(' '))

        if isinstance(value, date):
            return self.q(value.isoformat())

        if value is None:
            return 'NULL'

        return str(value)