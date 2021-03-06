<html>
    <head>
        <meta charset='utf-8'>
        <title>{{title}} - Gum</title>
%include('static.tpl')
    </head>
    <body>
%include('logout.tpl', token=token)
        <div id='layout'>
            <a href='#menu' id='menuLink' class='menu-link'>
                <span></span>
            </a>
            <div id='menu'>
                <div class='pure-menu pure-menu-open'>
                    <a class='pure-menu-heading' href='#'>GUM</a>
                    <ul>
%liclass = "class='menu-item-divided pure-menu-selected'"
                        <li>
                            <a href='{{'#main' if title == 'Home' else '/home'}}'>Home</a>
                        </li>
                        <li {{! liclass if title == 'Project' else ''}}>
                            <a href='{{'#' if title == 'Home' else '/home#'}}projects'>Projects</a>
                        </li>
                        <li {{! liclass if title in ('Object', 'Seeinfo') else ''}}>
                            <a href='{{'#' if title == 'Home' else '/home#'}}objects'>Objects</a>
                        </li>
                        <li {{! liclass if title == 'Console' else ''}}>
                            <a href='/home/console'>Console</a>
                        </li>
                        <li><a href='/home/rekey'>Setkey</a></li>
                        <li {{! liclass if title == 'Plugins' else ''}}>
                            <a href='/home/plus'>Plugins</a>
                        </li>
                        <li><a href='#' onclick='logout()'>Logout</a></li>
                    </ul>
                </div>
            </div>

            {{!base}}

        </div>
        <script src='/static/js/ui.js'></script>
    </body>
</html>
