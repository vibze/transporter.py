# -*- coding: utf-8 -*-
import cx_Oracle
import os
from transporter.cargo import Cargo


class Oracle:
    nls_lang = None
    user = None
    pwd = None
    path = 'AMERICAN_AMERICA.CL8ISO8859P5'

    def __init__(self, debug_sql=False):
        os.environ['NLS_LANG'] = self.nls_lang
        self.conn = cx_Oracle.connect(self.user, self.pwd, self.path)
        self.cursor = self.conn.cursor()
        self.debug_sql = debug_sql

    def execute(self, sql, *args):
        if args:
            return self.cursor.execute(sql.decode('utf8'), args[0])

        if self.debug_sql:
            print sql

        self.cursor.execute(sql.decode('utf8'))
        self.conn.commit()
        return self.cursor

    def extract(self, sql):
        self.execute(sql)
        return Cargo(type=Cargo.CURSOR, cursor=self.cursor, statement=sql)

    def count(self, table):
        return self.execute('SELECT COUNT(1) FROM %s' % table).fetchone()[0]
