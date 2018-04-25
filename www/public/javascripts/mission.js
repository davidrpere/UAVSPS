var h;
var socket = io();

socket.on('posicion', function (data) {
    setDronePosition(data.lat, data.lng, data.orientacion, data.id_dron);
});

socket.on('foto', function (data) {
    setPhoto(data.lat, data.lng, data.url);
});

socket.on('ruta_mon_busqueda', function (route) {
    clear_routes();

    for (var i = 0; i < route.length; i++) {
        switch (i){
            case 0:
                setRouteMonBusqueda(route[i].waypoints, "#3F51B5");
                break;

            case 1:
                setRouteMonBusqueda(route[i].waypoints, "#FF9800");
                break;

            default:
                break;
        }
    }
});

socket.on('ruta_vigilancia', function (route) {
    clear_routes();

    var radio = route.radio;
    var centro_lat = route.centro_lat;
    var centro_lng = route.centro_lng;
    var id_dron = route.id_dron;

    switch (id_dron){
        case 1:
            setRouteVigilancia(radio, centro_lat, centro_lng, "#3F51B5");
            break;
        case 2:
            setRouteVigilancia(radio, centro_lat, centro_lng, "#FF9800");
            break;

        default:
            break;
    }
});

$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.fixed-action-btn').floatingActionButton();
    $('.modal').modal();
    $('select').formSelect();
    $('.simple-ajax-popup').magnificPopup({
        type: 'ajax'
    });
});

$(window).resize(function () {
    h = $(window).height();
    var offsetTop = 60; // Calculate the top offset

    $('#map').css('height', (h - offsetTop));
}).resize();