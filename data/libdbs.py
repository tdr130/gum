#!/usr/bin/env python
# encoding: utf-8

import sqlite3

class sqlitei:
    '''Encapsulation sql.'''
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.cs = self.db.cursor()

    def commit(self):
        self.db.commit()

    def select(self, table, column, dump=None):
        '''Select
        table str, column list, dump dict.'''
        columns = ','.join(column)
        sql = 'select ' + columns + ' from ' + table
        dumps = []
        if dump:
            dumpname = dump.keys()[0]
            sql += ' where ' + dumpname + '=?'
            dumps.append(dump[dumpname])
        return self.cs.execute(sql, dumps)

    def update(self, table, column, dump):
        '''Update
        table str, column dict, dump dict.'''
        columns = []
        columnx = ''
        for c in column:
            columnx += c + '=?,'
            columns.append(column[c])
        dumpname = dump.keys()[0]
        sql = 'update ' + table + ' set '+ columnx[:-1] + ' where ' + dumpname + '=?'
        columns.append(dump[dumpname])
        return self.cs.execute(sql, columns)

    def insert(self, table, column, dump):
        '''Insert
        table str, column list, dump list'''
        dumps = ('?,'*len(dump))[:-1]
        columns = ','.join(column)
        sql = 'insert into ' + table + ' (' + columns + ') values (' +dumps + ')'
        return self.cs.execute(sql, dump)

    def delete(self, table, dump):
        '''Delete
        table str, dump dict'''
        dumpname = dump.keys()[0]
        sql = 'delete from ' + table + ' where ' + dumpname + '=?'
        return self.cs.execute(sql, [dump[dumpname]])
