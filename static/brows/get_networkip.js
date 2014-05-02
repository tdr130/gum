/*
    quininer[http://net.ipcalf.com/] - 140502
    get_networkip - gum.js
        - networkip probe
        and
            gum.script('http://' + gum.domain + '/static/brows/get_networkip.js');
        and
            null

*/

var RTCPeerConnection = /*window.RTCPeerConnection ||*/ window.webkitRTCPeerConnection || window.mozRTCPeerConnection;

if (RTCPeerConnection) (function () {
    function addgum_networkip(info){
        gum.backinfo['networkip'] = info;
    };

    var rtc = new RTCPeerConnection({iceServers:[]});
    if (window.mozRTCPeerConnection) {
        rtc.createDataChannel('', {reliable:false});
    };

    rtc.onicecandidate = function (evt) {
        if (evt.candidate) grepSDP(evt.candidate.candidate);
    };
    rtc.createOffer(function (offerDesc) {
        grepSDP(offerDesc.sdp);
        rtc.setLocalDescription(offerDesc);
    }, function (e) { console.warn("offer failed", e); });

    var addrs = Object.create(null);
    addrs["0.0.0.0"] = false;
    function updateDisplay(newAddr) {
        if (newAddr in addrs) return;
        else addrs[newAddr] = true;
        var displayAddrs = Object.keys(addrs).filter(function (k) { return addrs[k]; });
        addgum_networkip(displayAddrs.join(" or perhaps "));
    }

    function grepSDP(sdp) {
        var hosts = [];
        sdp.split('\r\n').forEach(function (line) {
            if (~line.indexOf("a=candidate")) {
                var parts = line.split(' '),
                    addr = parts[4],
                    type = parts[7];
                if (type === 'host') updateDisplay(addr);
            } else if (~line.indexOf("c=")) {
                var parts = line.split(' '),
                    addr = parts[2];
                updateDisplay(addr);
            }
        });
    }
})(); else {
    addgum_networkip('browser error');
}
