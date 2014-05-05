#! /usr/bin/env python
# encoding=utf-8

#from __future__ import unicode_literals

import sqlite3
from hashlib import md5
from base64 import b64encode
from sys import argv

salt = 'chewingum'
filekey = './filekey'

def install(salt, filekey):
    hashs = md5()
    with open(filekey) as keyfile:
        hashs.update(b64encode(keyfile.read()))
        key = hashs.hexdigest()
    auser = sqlite3.connect('./data/auser.db')
    ausers = auser.cursor()
    auser.execute('''
	create table user(
		id,
		salt,
		key,
		cookie
	);
''')
    ausers.execute('insert into user (id, salt, key) values (?,?,?,?)',
	[1, salt, key])
    auser.commit()
    auser.close()

    gum = sqlite3.connect('./data/gum.db')
    gums = gum.cursor()
    gum.executescript('''
	create table project(
		id integer primary key autoincrement,
		upkey not null,
		referer,
		browser,
		server
	);
	create table object(
		upkey not null,
		idsalt,
		name,
		browser,
		server,
		life,
		shellcode,
		shellinfo
	);
	create table info(
		upkey not null,
		id integer primary key autoincrement,
		idsalt,
		serverinfo,
		browserinfo
	);
''')
    gums.execute('insert into project (upkey,referer) values (?,?)',
	['no', '$default'])
    gums.execute('insert into project (upkey) values (?)',
	['yes'])
    gums.execute('insert into object (upkey) values (?)',
	['yes'])
    gums.execute('insert into info (upkey) values (?)',
	['yes'])
    gum.commit()
    gum.close()

if __name__ == '__main__':
    if '-h' in argv or '--help' in argv or len(argv) in (1, 3, 4):
        print '''
usage:
	python config.py install [ salt filekeyPath]

	-h --help
'''
        exit()
    elif 'install' in argv:
        if len(argv) == 5:
            install(argv[2], argv[3])
        else:
            install(salt, filekey)
