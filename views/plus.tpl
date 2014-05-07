%rebase('base.tpl', token=token, title=title)
<div id='main'>
    <div class='header'>
        <h1>{{title}}</h1>
        <h2>Unfinished...</h2>
    </div>

    <div class='content'>
        <h2 class='content-subhead'>Upload</h2>
        <form action='/home/plus/up' method='POST' enctype='multipart/form-data'>
            Path:<input type='text' name='path' value='./static'>
            File:<input type='file' name='plus'>
            <input type='hidden' name='token' value='{{token}}'>
            <input type='submit' class='pure-button pure-button-primary' value='Upload'>
    </div>
</div>
