CFGURL="/ipc.sh?"
function do_action(url)
{
    $.ajax({
        url: url,
        dataType: 'json',
        success: function(data){
            console.log('success');
            console.log(data);
            console.log(url);
            timer = setTimeout('fill_stuff()', 200);
        },
        error: function(  jqXHR, textStatus,  errorThrown ) {
            console.log(errorThrown);
        }
    });
}

function get_btn_str(text, url)
{
    url = "'" + url + "'";
    var str = "<button type=\"button\" onclick=\"do_action("+url+")\" class=\"btn btn-danger\">"+text+"</button>";
    return str;
}


function plot_item(id_no, list)
{
    console.log(list.tput);
    $.plot("#placeholder"+id_no, [  list.tput ]);
    if (list.running) {
        setTimeout(function() { plot_item_json(id_no)}, 1000);
    }
}

function plot_item_json(id_no)
{
    $.ajax({
        url: '/get_parsed?id_no=' + id_no,
        dataType: 'json',
        success: function(data) {
            plot_item(id_no, data);
        },
        error: function( data ) {
            console.log(data);
        }
    });
}


function list_tcp_listeners(data) {
    var htmlstring = '';
    htmlstring += ' \
    <table class="table table-striped table-bordered"> \
        <tr> \
            <th>Port</th> \
            <th></th> \
        </tr> \
    ';
    data.tcp_listeners.forEach(function(p) {
        htmlstring += "<tr><td>" + p.port + "</td> <td>" + get_btn_str("Stop",CFGURL + "cmd=tcp_listener_kill&port="+p.port) + "</td></tr>";
    });
    htmlstring +=' </table> ';
    $("#tcplisteners").empty();
    $("#tcplisteners").append(htmlstring);
}

function list_udp_listeners(data) {
    var htmlstring = '';
    htmlstring += ' \
    <table class="table table-striped table-bordered"> \
        <tr> \
            <th>Port</th> \
            <th></th> \
        </tr> \
    ';
    data.udp_listeners.forEach(function(p) {
        htmlstring += "<tr><td>" + p.port + "</td> <td>" + get_btn_str("Stop",CFGURL + "cmd=udp_listener_kill&port="+p.port) + "</td></tr>";
    });
    htmlstring +=' </table> ';
    $("#udplisteners").empty();
    $("#udplisteners").append(htmlstring);
}

function list_tcp_connections(data) {
    var htmlstring = '';
    htmlstring += ' \
    <table class="table table-striped table-bordered"> \
        <tr> \
            <th>Destination</th> \
            <th>Port</th> \
            <th>Pairs</th> \
            <th></th> \
        </tr> \
    ';
    data.tcp_connections.forEach(function(p) {
        htmlstring += "<tr>";
        htmlstring += "<td>" + p.dest + "</td>";
        htmlstring += "<td>" + p.port + "</td>";
        htmlstring += "<td>" + p.pair + "</td>";
        htmlstring += "<td>" + get_btn_str("Stop",CFGURL + "cmd=tcp_connection_kill&port="+p.port+"&dest="+p.dest) + "</td>";
        htmlstring += "</tr>";
    });
    htmlstring +=' </table> ';
    $("#tcpconnections").empty();
    $("#tcpconnections").append(htmlstring);
}

function list_udp_connections(data) {
    var htmlstring = '';
    htmlstring += ' \
    <table class="table table-striped table-bordered"> \
        <tr> \
            <th>Destination</th> \
            <th>Port</th> \
            <th>Bandwidth (Mbit/s)</th> \
            <th></th> \
        </tr> \
    ';
    data.udp_connections.forEach(function(p) {
        htmlstring += "<tr>";
        htmlstring += "<td>" + p.dest + "</td>";
        htmlstring += "<td>" + p.port + "</td>";
        htmlstring += "<td>" + p.bw + "</td>";
        htmlstring += "<td>" + get_btn_str("Stop",CFGURL + "cmd=udp_connection_kill&port="+p.port+"&dest="+p.dest) + "</td>";
        htmlstring += "</tr>";
    });
    htmlstring +=' </table> ';
    $("#udpconnections").empty();
    $("#udpconnections").append(htmlstring);
}


function get_tcp_listeners () {
    $.ajax({
        url: CFGURL + 'cmd=tcp_listener_list',
        dataType: 'json',
        success: list_tcp_listeners,
        error: function( data ) {
            console.log(data);
        }
    });
}

function get_udp_connections () {
    $.ajax({
        url: CFGURL + 'cmd=udp_connection_list',
        dataType: 'json',
        success: list_udp_connections,
        error: function( data ) {
            console.log(data);
        }
    });
}

function get_tcp_connections () {
    $.ajax({
        url: CFGURL + 'cmd=tcp_connection_list',
        dataType: 'json',
        success: list_tcp_connections,
        error: function( data ) {
            console.log(data);
        }
    });
}


function get_udp_listeners () {
    $.ajax({
        url: CFGURL + 'cmd=udp_listener_list',
        dataType: 'json',
        success: list_udp_listeners,
        error: function( data ) {
            console.log(data);
        }
    });
}

function fill_stuff () {
    get_tcp_listeners();
    get_udp_listeners();
    get_tcp_connections();
    get_udp_connections();
    timer = setTimeout('fill_stuff()', 5000);
}

function start_listener() {
    var get_str = "";
    var url = CFGURL;
    var type = $("#lprotocol_type").val();
    if (type == "tcp_listen" || "udp_listen") {
        var portno = ($("#lportno").val());
        get_str += "cmd=" + type;
        get_str += "&port=" + portno;
        url += get_str;
    }

    $.ajax({
        url: url,
        dataType: 'json',
        success: function(data){
            if (data.err == "success") {
                alert("Sucess");
            }
            else {
                alert('Error string: "' + data.err + '"');
            }
            console.log(data);
            console.log(url);
        },
        error: function(  jqXHR, textStatus,  errorThrown ) {
            console.log(errorThrown);
        }
    });
}

function start_traffic() {
    var get_str = "";
    var url = CFGURL;
    var type = $("#protocol_type").val();
    if (type == "tcp_connect") {
        var portno = ($("#portno").val());
        var dur = ($("#duration").val());
        var dest = ($("#destination").val());
        var pair = ($("#optional").val());
        get_str += "cmd=" + type;
        get_str += "&port=" + portno;
        get_str += "&dur=" + dur;
        get_str += "&dest=" + dest;
        get_str += "&pair=" + pair;
        url += get_str;
    }
    else if (type == "udp_connect") {
        var portno = ($("#portno").val());
        var dur = ($("#duration").val());
        var dest = ($("#destination").val());
        var bw = ($("#optional").val());
        get_str += "cmd=" + type;
        get_str += "&port=" + portno;
        get_str += "&dur=" + dur;
        get_str += "&dest=" + dest;
        get_str += "&bw=" + bw;
        url += get_str;
    }

    $.ajax({
        url: url,
        dataType: 'json',
        success: function(data){
            if (data.err == "success") {
                alert("Sucess");
            }
            else {
                alert('Error string: "' + data.err + '"');
            }
            console.log('success');
            console.log(data);
            console.log(url);
        },
        error: function(  jqXHR, textStatus,  errorThrown ) {
            console.log(errorThrown);
        }
    });
}

function setopttext() {
    var type = $("#protocol_type").val();
    if (type == "tcp_connect") {
        $("#optiontext").text("Pairs");
    }
    else if (type == "udp_connect") {
        $("#optiontext").text("Bandwidth (Mbit/s)");
    }
}

///////
var pattern = /\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b/;
x = 46;
//$('#destination').keypress(function (e) {
$('.ipaddr').keypress(function (e) {
    if (e.which != 8 && e.which != 0 && e.which != x && (e.which < 48 || e.which > 57)) {
        console.log(e.which);
        return false;
    }
}).keyup(function () {
    var this1 = $(this);
    if (!pattern.test(this1.val())) {
        //$('#destination').css({'background-color' : '#EE1111'});
        this1.css({'background-color' : '#EE1111'});
        while (this1.val().indexOf("..") !== -1) {
            this1.val(this1.val().replace('..', '.'));
        }
        x = 46;
    } else {
        x = 0;
        var lastChar = this1.val().substr(this1.val().length - 1);
        if (lastChar == '.') {
            this1.val(this1.val().slice(0, -1));
        }
        var ip = this1.val().split('.');
        if (ip.length == 4) {
            //$('#destination').css({'background-color' : '#11EE11'});
            this1.css({'background-color' : '#11EE11'});
        }
    }
});

$('.portno').keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        console.log(e.which);
        return false;
    }
}).keyup(function () {
    var this1 = $(this);
    var portno = parseInt(this1.val());
    if (portno >= 65536) {
        this1.css({'background-color' : '#EE1111'});
    } else {
        this1.css({'background-color' : '#11EE11'});
    }
});


$('.numeric').keypress(function (e) {
    if (e.which != 8 && e.which != 0 && (e.which < 48 || e.which > 57)) {
        console.log(e.which);
        return false;
    }
});
