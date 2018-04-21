var h;
var socket = io();
var heading_dron1 = 0;
var heading_dron2 = 0;

socket.on('dron1_posicion', function (data) {
    setDronePosition(data.lat, data.lng, 1);
});

socket.on('dron1_orientacion', function (data) {
    heading_dron1 = data.orientacion;
});

socket.on('dron2_posicion', function (data) {
    setDronePosition(data.lat, data.lng, 2);
});

socket.on('dron2_orientacion', function (data) {
    heading_dron2 = data.orientacion;
});

socket.on('foto', function (data) {
    setPhoto(data.lat, data.lng, data.url, data.alt);
});

socket.on('ruta', function (route) {
    for (var i = 0; i < route.length; i++) {
        switch (i){
            case 0:
                console.log(route[i].waypoints);
                setRoute(route[i].waypoints, "#3F51B5");
                break;

            case 1:
                console.log(route[i].waypoints);
                setRoute(route[i].waypoints, "#FF9800");
                break;
        }
    }
});

$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.modal').modal();
});

$(window).resize(function () {
    h = $(window).height();
    var offsetTop = 60; // Calculate the top offset

    $('#map').css('height', (h - offsetTop));
}).resize();