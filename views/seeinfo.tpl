%from base64 import b64decode
<html>
	<head></head>
	<body>
%include('logout.tpl', token=token)
%include('delete.tpl', states=states, id=ids, token=token)
		<a href='/home/object/{{idsalt}}'><h1>object</h1></a>
		<br><b>Sever info:</b><br>
%for http in serverinfo:
		<p>{{http}}:{{b64decode(serverinfo[http])}}</p>
%end
		<br><br>
		<b>Browser info:</b><br>
%for script in browserinfo:
		<p>{{script}}:{{b64decode(browserinfo[script])}}</p>
%end
	</body>
</html>
