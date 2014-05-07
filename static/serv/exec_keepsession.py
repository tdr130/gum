#! /usr/bin/env python
# encoding=utf-8
#   quininer - 140502
#	exec_keepsession - keep temp sessionid or cookie
#		null
#
'''
gum_keepsession = {
	'url':referer,
	'session':cookie,
	'data':{'a':'b'},
	'frequency':300,
	'endate':'2013-12-12 15:17:00'
}
with open('./static/serv/exec_keepsession.py') as files: exec files.read()
'''
def load():
    from os import system
    from urllib import urlencode

    system('python ./exec_keepsession.py {url} {session} {data} {frequency} {endate}'.format(
	    url = b64encode(gum_keepsession['url']),
	    session = b64encode(gum_keepsession['session']),
	    data = b64encode(urlencode(gum_keepsession['data'])),
	    frequency = b64encode(gum_keepsession['frequency']),
	    endate = b64encode(gum_keepsession['endate'])
    ))

def main():
    import httplib
    from sys import argv
    from base64 import b64decode
    from urlparse import urlparse
    from time import time, strptime, mktime, sleep
    from httplib import HTTPConnection as httpconn

    endtime = int(mktime(strptime(b64decode(argv[5]), '%Y-%m-%d %H:%M:%S')))
    urls = urlparse(b64decode(argv[1]))
    data = b64decode(argv[3])
    session = b64decode(argv[2])
    frequency = b64decode(argv[4])
    while time() < endtime:
        keeping = httpconn(urls.netloc)
        keeping.request('HEAD', urls.path, data, {'Cookie':session})
        keeping.close()
        sleep(frequency)

if __name__ == '__main__':
    main()
else:
    load()
