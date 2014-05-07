<html>
    <head>
%include('static.tpl')
    </head>
    <body>
%if error=='404':
        <h1>404, Page Not Found</h1>
        <p>It looks like you've tried to access nil...</p>
%else:
    %if error=='500':
        <h1>500, Internal Server Error</h1>
        <p>Learning includes mistakes...</p>
    %else:
        %if error=='405':
        <h1>405, Method Not Allow</h1>
        <p>get or post?...</p>
        %end
    %end
%end
        <p>for {{ctime}}</p>
    </body>
</html>
