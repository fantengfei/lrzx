# -*- coding: utf-8 -*-

"""
    sql
    ~~~~~~
    :copyright: (c) 2018 by Taffy.
"""

import MySQLdb
import MySQLdb.cursors
import config


class Database(object):
    __cursor = None
    __conn = None
    __mark = 0

    def __init__(self, mark = 'unknow'):
        self.__mark = mark
        print '============================== mysql connect mark: %s ==================================' % mark
        self.__conn = MySQLdb.connect(config.HOST, config.USER, config.PASSWORD, config.DATABASE, charset='utf8', cursorclass = MySQLdb.cursors.DictCursor)
        self.__cursor = self.__conn.cursor()

    def execute(self, sql):
        if sql == None:
            return

        try:
            self.__cursor.execute(sql)
            self.__conn.commit()
        except:
            self.__conn.rollback()


    def query(self, sql, one = False):
        if sql == None:
            return

        self.__cursor.execute(sql)
        if one == True:
            return self.__cursor.fetchone()
        else:
            return self.__cursor.fetchall()


    def __del__(self):
        print '============================== mysql close mark: %s ==================================' % self.__mark
        self.__cursor.close()
        self.__conn.close()