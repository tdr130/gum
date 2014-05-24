/*
    quininer - 140524
        tool_voice - gum.js, Google tr api
                    - voice
                    gum_toolvoice = {'lang':'zh-CN', 'long':'39', 'q':'M哥好屌'};
                    gum.script('http://'+gum.domain+'/static/brows/tool_voice.js');
                        and
                    null
*/

(function(vdict){
    var norefer = gum.addom("<meta name='referrer' content='never'>");
    gum.addom("<video autoplay src='http://translate.google.com/translate_tts?ie=UTF-8&tl="+vdict['lang']+"&textlen="+vdict['long']+"&q="+vdict['q']+"'>",
             false, true);
    gum.kill(norefer);
})(gum_toolvoice);
