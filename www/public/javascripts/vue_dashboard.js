var area_map_bool = false;
var h;

var btn_float = new Vue({
    el: '#btn-float',
    data: {
        seen: true
    },
    methods: {
        start_mission: function () {
            var params = $('form').serializeArray();

            var array_coordJSON = [];
            var MVCArray = rectPoly.getPath();
            MVCArray.forEach(function (element) {
                array_coordJSON.push(element.toJSON());
            });

            var socket = io();
            socket.emit('start_mission', {
                'nombre_mision': params[0].value,
                'tipo_mision': params[1].value,
                'numero_drones': params[2].value,
                'solapamiento': params[3].value,
                'altura_vuelo': params[4].value,
                'norte_este': array_coordJSON[0],
                'norte_oeste': array_coordJSON[1],
                'sur_este': array_coordJSON[3],
                'sur_oeste': array_coordJSON[2]
            });

            mission_map(get_center_lat(), get_center_lng());
            btn_float_stop.seen = true;
            btn_float.seen = false;
        },
        remove_area: function () {
            if(area_map_bool == true){
                remove_area();
                area_map_bool = false;
            }
        },
        add_area: function () {
            if(area_map_bool == false){
                add_area();
                area_map_bool = true;
            }
        }
    }
});

var btn_float_stop = new Vue({
    el: "#btn-floating-stop",
    data: {
        seen: false
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
    $('#btn-float').css('height', (h - 50));
}).resize();



