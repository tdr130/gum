%rebase('base.tpl', token=token, title=title)
%from base64 import b64decode
<div id='main'>
    <div class='header'>
        <h1>{{title}}</h1>
        <h2><a href='/home/object/{{idsalt}}'>Object</a></h2>
    </div>

    <div class='content'>
        <h2 class='content-subhead'>Server info</h2>
%for info in serverinfo:
    %if info.split('_')[0] == 'png':
        {{info}}:<img src='data:image/png;base64,{{serverinfo[info]}}'><br>
    %else:
        {{info}}:<pre><code>{{b64decode(serverinfo[info])}}</code></pre><br>
    %end
%end
    </div>
    <div class='content'>
        <h2 class='content-subhead'>Browser info</h2>
%for info in browserinfo:
    %if info.split('_')[0] == 'png':
        {{info}}:<img src='data:image/png;base64,{{browserinfo[info]}}'><br>
    %else:
        {{info}}:<pre><code>{{b64decode(browserinfo[info])}}</code></pre>
    %end
%end
    </div>
%include('delete.tpl', token=token, title=title, id=ids)
</div>
