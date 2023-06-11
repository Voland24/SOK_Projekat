function searchf() {
    var sp = document.getElementById("search").value;
    if (sp == "") {
        return;
    }
    var search_param = escape(sp.replaceAll("/", "|"));
    window.location.href = "http://127.0.0.1:" + window.location.port + '/search/' + search_param;
}

function filterf() {
    var fp = document.getElementById("filter").value;
    if (fp == "") {
        return;
    }
    var filter_param = escape(fp.replaceAll("/", "|"));
    window.location.href = "http://127.0.0.1:" + window.location.port + '/filter/' + filter_param;
}

function complete_graphf() {
    window.location.href = "http://127.0.0.1:" + window.location.port + '/complete_graph' ;
}