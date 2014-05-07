<html>
    <head>
%include('static.tpl')
    </head>
	<body>
	    <form class="pure-form pure-form" action='{{uri}}' method='POST' enctype='multipart/form-data'>
		    <fieldset>
                <legend>Key</legend>
			    <input type='file' name='filekey'>
			    <input for='URL' type='text' name='urlkey'>
		        <input class='pure-button pure-button-primary' type='submit' value='Yes'>
            </fieldset>
        </form>
    </body>
</html>

