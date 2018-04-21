var area_map_bool = false;
var h;
var socket = io();

var row_map = new Vue({
    el: "#row_map",
    data: {
        seen: true
    }
});

var load = new Vue({
    el: "#load",
    data: {
        seen: false
    }
});

var btn_float = new Vue({
    el: '#btn-float',
    data:{
        seen: true
    },
    methods: {
        start_mission: function () {
            var params = $('form').serializeArray();
            var center_lat = get_center_lat();
            var center_lng = get_center_lng();

            var ne = rectangle.getBounds().getNorthEast();
            var so = rectangle.getBounds().getSouthWest();

            socket.emit('start_mission', {
                'nombre_mision': params[0].value,
                'tipo_mision': params[1].value,
                'numero_drones': params[2].value,
                'solapamiento': params[3].value,
                'altura_vuelo': params[4].value,
                'norte_este': ne,
                'sur_oeste': so
            });

            row_map.seen = false;
            btn_float.seen = false;
            load.seen = true;


            localStorage.setItem("center_lat", center_lat);
            localStorage.setItem("center_lng", center_lng);
        },
        remove_area: function () {
            if (area_map_bool == true) {
                remove_area();
                area_map_bool = false;
            }
        },
        add_area: function () {
            if (area_map_bool == false) {
                add_area();
                area_map_bool = true;
            }
        }
    }
});

$(document).ready(function () {
    $('.sidenav').sidenav();
    $('.fixed-action-btn').floatingActionButton();
    $('.modal').modal();
    $('select').formSelect();
});

$(window).resize(function () {
    h = $(window).height()
    var offsetTop = 60; // Calculate the top offset

    $('#map').css('height', (h - offsetTop));
}).resize();