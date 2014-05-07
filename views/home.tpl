%rebase('base.tpl', token=token, title=title)
<div id='main'>
    <div class='header'>
        <h1>{{title}}</h1>
        <h2>Unll~</h2>
    </div>

    <div class='content'>
        <h2 id='projects' class='content-subhead'>Projects</h2>
        <p>
%for project in projects:
    %if project[-1] != 'yes':
            <a class='pure-button' href='/home/project/{{project[0]}}'>{{project[1]}}</a>
    %end
%end
        </p>
    </div>
    <div class='content'>
        <h2 id='objects' class='content-subhead'>Objects</h2>
        <p>
%for object in objects:
    %if object[-1] != 'yes':
            <a class='pure-button' href='/home/object/{{object[0]}}'>{{object[1]}}</a>
    %end
%end
        </p>
    </div>
</div>
