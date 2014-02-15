<html>
	<head>
%#		<script src='/js/jquery-2.0.3.js'></script>
	</head>
	<body>
%include logout token = token
%include delete token = token, states = 'object' if state else 'project', id = idsalt if state else id
		<h1>{{id}}</h1>
%if state:
		<h2><a href='/home/console#{{idsalt}}'>console</a></h2>
		lifetime : {{life}}
%end
		<form name='setting' action='/home/{{idsalt if state else id}}/{{'useing' if state else 'setting'}}' method='POST'>
			<input type='hidden' name='token' value='{{token}}'>
		<h2>{{'object name' if state else 'project domain or url'}}</h2>
			<input name='{{'name' if state else 'referer'}}' type='text' value='{{name}}'>
		<h2>code</h2>
			<p>server</p><textarea name='server' cols='80' rows='10'>{{server}}</textarea>
			<br>
			<p>browser</p><textarea name='browser' cols='80' rows='10'>{{browser}}</textarea>
			<br><br>
			<input type='submit' value='Start'>
		</form>
%if state:
		info
    %for ids in infos:
		<a href='/home/{{ids[0]}}/info'>{{ids[0]}}</a>
    %end
%end
	</body>
</html>
