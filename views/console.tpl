<html>
<head>
    <script src='/static/js/jquery-2.0.3.js'></script>
    <script>xdomain = '{{domain}}';</script>
    <script src='/static/js/websocket_console.js'></script>
</head>
<body>
    <form id='send'>
        <input id='command' type='text'>
        <button type='submit'>send</button>
    </form>
    <div id='messages'></div>
</body>
</html>
