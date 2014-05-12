<html>
    <head>
%include('static.tpl')
    </head>
	<body>
        <h3>{{uri}}</h3>
	    <form class="pure-form" action='{{uri}}' method='POST' enctype='multipart/form-data'>
		    <fieldset>
                <legend>Key</legend>
$if uri == '/home/rekey':
                <input type='hidden' name='token' value='{{token}}'>
%end
			    <input type='file' name='filekey'>
			    <input for='URL' type='text' name='urlkey'>
		        <input class='pure-button pure-button-primary' type='submit' value='Yes'>
            </fieldset>
        </form>
    </body>
</html>

