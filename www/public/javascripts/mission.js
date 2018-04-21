var h;
var socket = io();
var heading = 0;

socket.on('dron1_posicion', function (data) {
    setDronePosition(data.lat, data.lng);
});

socket.on('dron1_orientacion', function (data) {
    heading = data.orientacion;
});

socket.on('foto', function (data) {
    setPhoto(data.lat, data.lng, data.url, data.alt);
});

socket.on('ruta', function (route) {
    setRoute(route);
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