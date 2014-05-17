%rebase('base.tpl', token=token, title=title)
<div id='main'>
    <div class='header'>
        <h1>{{title}}</h1>
%if title != 'Object':
        <h2>Unll~</h2>
%else:
        <h2><a href='/home/console#{{idsalt}}'>Console</a></h2>
        <h3>Last time: {{life}}</h3>
%end
    </div>

    <form class='pure-form' action='/home/{{idsalt}}/{{'useing' if title == 'Object' else 'setting'}}' method='POST'>
        <input type='hidden' name='token' value='{{token}}'>
        <div class='content'>
            <h2>{{title}} Name</h2>
            <input name='name' value='{{name}}'>
        </div>

        <div class='content'>
            <h2 class='content-subhead'>Server Code</h2>
            <textarea name='server' id='serv'>{{server}}</textarea>
        </div>
        <div class='content'>
            <h2 class='content-subhead'>Browser Code</h2>
            <textarea name='browser' id='brows'>{{browser}}</textarea>
        </div>
        <input class='pure-button pure-button-primary' type='submit' value='Save'>
    </form>
%include('delete.tpl', token=token, title=title, id=id)
%if title == 'Object':
    <div class='content'>
        <h2 class='content-subhead'>Object info</h2>
        <p>
    %for info in infos:
            <a class='pure-button' href='/home/{{info[0]}}/info'>{{info[0]}}</a>
    %end
        </p>
    </div>
%end
</div>
