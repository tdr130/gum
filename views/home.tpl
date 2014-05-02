<html>
	<head>
	</head>
	<body>
%include('logout.tpl', token=token)
		<h2><a href='/home/project/{{new}}'>NewProject</a></h2>
		project
%for project in projects:
    %if project[-1] != 'yes':
		{{project[0]}}<a href='/home/project/{{project[0]}}'>{{project[1]}}</a>
    %end
%end
		<br>
		object
%for object in objects:
    %if object[-1] != 'yes':
		<a href='/home/object/{{object[0]}}'>{{object[1]}}</a>
    %end
%end
		<br>
        <p><a href='/home/rekey'>Setkey</a></p>
        <p><a href='/home/plus'>Upload</a></p>
	</body>
</html>
