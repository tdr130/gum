$(document).ready(function(){
    if(!window.WebSocket){
        if(window.MozWebSocket){
            window.WebSocket = window.MozWebSocket;
        }else{
            $('#messages').append("<li>Your browser doesn't support WebSockets.</li>");
        };
    };
    ws = new window.WebSocket('ws://'+xdomain+'/home/connect?idsalt='+document.location.hash.split('#')[1]);
    ws.onopen = function(){
        $('#messages').append('<li>Connected to success.</li>');
    };
    ws.onmessage = function(info){
        $('#messages').append('<br>:' + info.data);
    };
    $('#send').submit(function(){
        ws.send($('#command').val());
        $('#messages').append('<br>'+$('#command').val().replace(/</g, '&lt;').replace(/>/g, '&gt;'))
        $('#command').val('').focus();
        return false;
    });
});
