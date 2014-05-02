<html>
    <body>
        <form action='/home/plus/up' method='POST' enctype='multipart/form-data'>
            Path:<input type='text' name='path' value='./static/'>
            File:<input type='file' name='plus'>
            <input type='hidden' name='token' value='{{token}}'>
            <input type='submit' value='upload'>
        </form>
    </body>
</html>
