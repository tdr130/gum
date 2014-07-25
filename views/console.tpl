%rebase('base.tpl', token=token, title=title)
<script src='/static/js/jquery-2.0.3.js'></script>
<script>xdomain = '{{domain}}';</script>
<script src='/static/js/websocket_console.js'></script>
<div id='main'>
    <div class='header'>
        <h1>{{title}}</h1>
        <h2>In fact, landscaping can..</h2>
    </div>
    <div id='messages'></div>
    <div class='content'>
        <h2 class='content-subhead'>Command</h2>
        <form id='send'>
            <input id='command' type='text'>
            <button type='submit'>send</button>
        </form>
    </div>
</div>
