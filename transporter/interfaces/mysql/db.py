# -*- coding: utf-8 -*-
from _mysql import ProgrammingError
import pymysql
from transporter.cargo import Cargo
from transporter.interfaces.mysql.table import Table


class MySQL:
    host = None
    user = None
    pwd = None
    db = None
    charset = 'utf8mb4'
    print_sql = False

    def __init__(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.pwd,
            db=self.db,
            charset=self.charset,
            autocommit=True)
        self.cursor = self.conn.cursor()

    def execute(self, sql, *args):
        if self.print_sql:
            print sql

        try:
            if args:
                return self.cursor.execute(sql, args)

            self.cursor.execute(sql)
        except:
            print sql
            raise

        return self.cursor

    def extract(self, sql):
        self.execute(sql)
        return Cargo(type=Cargo.CURSOR, cursor=self.cursor, statement=sql)

    def table(self, name):
        return Table(db=self, name=name)

    def q(self, input):
        if input is None:
            return 'NULL'

        if type(input) is str or type(input) is unicode:
            return "'%s'" % input

        return str(input)

    def esc(self, input):
        return self.conn.escape(input)

    def commit(self):
        self.conn.commit()