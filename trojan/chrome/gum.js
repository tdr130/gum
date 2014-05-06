gum = function(){
	var u = {
		'version':'1140501',
		'domain':'{{domain}}',
	    'backinfo':{}
    };

	u.e = function(code){try{return eval(code)}catch(e){return ''}};

	u.jquery = function(){
		if(u.e('$().jquery')){return 1}else{return 0};
	};

	u.id = function(id){
		if(u.jquery()){
			return $('#'+id);
		}else{
			return document.getElementById(id);
		};
	};

	u.name = function(name){
		return document.getElementsByTagName(name);
	};

    u.html = function(){
            return u.name('html')[0]
                    ||document.write('<html>')
                    ||u.name('html')[0];
    };

	u.rdm = function(){return Math.random()*1e5};

    u.bind = function(e, name, foo){
        if(u.jquery()){
            $(e).bind(name, foo);
        }else{
            (e.addEventListener)?(
                e.addEventListener(name, foo, false)):(
                e.attachEvent('on'+name, foo));
        };
    };

    u.kill = function(dom){
            if(u.jquery()){
                    $(dom).remove();
            }else{
                    dom.parentElement.removeChild(dom);
            };
    };

    u.addom = function(html, doming, hide, callback){
        (!doming)&&(doming = u.html());
        var temp = document.createElement('span');
        temp.innerHTML = html;
        var dom = temp.children[0];
        (hide)&&(dom.style.display = 'none');
        callback&&u.bind(dom, 'load', callback);
        doming.appendChild(dom);
        return dom;
    };

	u.script = function(url, callback){
		if(u.jquery()){
			$.getScript(url, callback);
		}else{
            url += '?_=' + u.rdm();
			document.documentElement.appendChild(
                script = document.createElement('script')).src=url;
            callback&&u.bind(script, 'load', callback);
            u.kill(script);
		};
	};

	u.ajax = function(url, datas, headers, callback){
        var xhr;
        datas?(type = 'POST'):(type = 'GET');
		if(u.jquery()){
			xhr = $.ajax({
                type:type,
                url:url,
                data:datas,
                headers:headers,
                success:callback
            });
			return xhr;
		}else{
			(window.XMLHttpRequest)?(
                xhr = new XMLHttpRequest()):(
                xhr = new ActiveXObject('Microsoft.XMLHTTP'));
			xhr.open(type, url, false);
			(type=='POST')&&(
                xhr.setRequestHeader('content-type',
                                     'application/x-www-form-urlencoded'));
            if(headers){
                for(var header in headers){
                    xhr.setRequestHeader(header, headers[header]);
                };
            };
            callback&&(xhr.onreadystatechange = function(){
                (this.readyState == 4 && (
                    (this.status >= 200 && this.status <= 300)
                        || this.status == 304)
                )&&callback.apply(this, arguments);
            });
			xhr.send(datas);
			return xhr;
		};
	};

	u.post = function(url, data, o, callback){
		var form = u.addom("<form method='POST'>", u.html(), true);
		form.action = url;
		for(var name in data){
			var input = document.createElement('input');
			input.name = name;
			input.value = data[name];
			form.appendChild(input);
		};
		if(!o){
			var iframe = u.addom('<iframe sandbox name=_'+u.rdm()+'_>', u.html(), true);
			form.target = iframe.name;
		};
        callback&&u.bind(form, 'submit', callback);
		form.submit();
		(!o)&&(u.kill(form))&(setTimeout(function(){
            u.kill(iframe);
        }, 3*1000));
	};

	return u;
}();

{{!script}}
