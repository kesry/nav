#!/config/env/python/3.10/python
from init import init
import sqlite3
import os
from queue import Queue
from conf import config


class Pool(object):
    def __init__(self, config):
        self.path = os.path.join(os.getcwd(), config['path'])
        self.poolsize = config['poolsize']
        self.pool = Queue(self.poolsize)
        for i in range(self.poolsize):
            conn = Connection(sqlite3.connect(self.path))
            self.pool.put(conn)

    def getConn(self):
        if (not self.pool.empty()):
            return self.pool.get()
        else:
            raise Exception("数据库连接已满，请扩大连接数后重启服务。")

    def release(self, conn):
        conn.release()
        self.pool.put(conn)

    def execute(self, sql, param=()):
        conn = self.getConn()
        res = conn.execute(sql, param)
        self.release(conn)
        return res


class Connection():
    def __init__(self, conn):
        self.conn = conn
        self.conn.row_factory = self.row_factory
        self.cursor = conn.cursor()
        self.istransaction = False

    def row_factory(self, cursor, row):
        dataline = {}
        for idx, val in enumerate(cursor.description):
            dataline[val[0]] = row[idx]
        return dataline

    def release(self):
        if (self.istransaction):
            print("当前连接正在进行事务，无法释放！")

        if (not self.cursor):
            self.cursor.close()
        if (not self.conn):
            self.conn.commit()
        self.cursor = self.conn.cursor()
        self.istransaction = False

    def executemany(self, sql, param=[()]):
        rows = self.cursor.executemany(sql, param)
        result = self.fetchall()
        self.cursor.close()
        if (not self.istransaction):
            self.conn.commit()
        return {
            "row": rows,
            "data": result
        }

    def execute(self, sql, param=()):
        self.cursor.execute(sql, param)
        rowcount = self.cursor.rowcount
        result = self.cursor.fetchall()
        self.cursor.close()

        if (not self.istransaction):
            self.conn.commit()

        return {
            "row": rowcount,
            "data": result
        }

    def starttransaction(self):
        self.istransaction = True

    def stoptransaction(self):
        self.conn.commit()
        self.istransaction = False


init()
pool = Pool(config=config['db']['sqlite3'])
