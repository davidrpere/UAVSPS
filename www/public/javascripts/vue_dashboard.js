var area_map_bool = false;
var h;
var socket = io();

socket.on('waypoints', function (data) {
    console.log(data.img)
    setMarkers(data.lat, data.lng, data.img)
});

var btn_float = new Vue({
    el: '#btn-float',
    data: {
        seen: true
    },
    methods: {
        start_mission: function () {
            var params = $('form').serializeArray();
            var center_lat = get_center_lat();
            var center_lng = get_center_lng();

            var array_coordJSON = [];
            var MVCArray = rectPoly.getPath();
            MVCArray.forEach(function (element) {
                array_coordJSON.push(element.toJSON());
            });

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


            mission_map(center_lat, center_lng);
            btn_float_stop.seen = true;
            btn_float.seen = false;

            localStorage.setItem("in_mission", "1");
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

var btn_float_stop = new Vue({
    el: "#btn-floating-stop",
    data: {
        seen: false
    },
    methods: {
        stop_mission: function () {
            swal({
                title: "¿Finalizar misión?",
                icon: "warning",
                buttons: {
                    cancel: "Cancelar",
                    confirm: "Finalizar misión"
                },
                dangerMode: true,
            }).then((willDelete) => {
                if (willDelete) {
                    pac_input.seen = true;
                    console.log("ordenando a todos los drones vuelta a casa");
                    localStorage.setItem("in_mission", "0");
                    btn_float_stop.seen = false;
                    btn_float.seen = true;
                    initAutocomplete();
                }
            });

        }
    }
});

var pac_input = new Vue({
    el: "#pac-input",
    data: {
        seen: true
    }
});


$(document).ready(function () {
    if(localStorage.in_mission == "1"){
        mission_map(parseFloat(localStorage.center_lat), parseFloat(localStorage.center_lng));
        btn_float_stop.seen = true;
        btn_float.seen = false;
        pac_input.seen = false;
    }
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



