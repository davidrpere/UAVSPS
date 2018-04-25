var area_map_bool = false;
var h;
var socket = io();
var tipo_mision_dash = -1;

socket.on('posicion', function (data) {
    setDronePosition(data.lat, data.lng, data.orientacion, data.id_dron);
});

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
    data: {
        seen: true
    },
    methods: {
        remove_area: function () {
            if (area_map_bool == true) {
                remove_area();
                $("#mission_type").attr("class", "btn-floating deep-purple darken-2");
                $("#mission_type").attr("href", "javascript:void(0);");
                area_map_bool = false;
            }
        },
        add_rectangle: function () {
            if (area_map_bool == false) {
                add_area(0);
                area_map_bool = true;
                tipo_mision_dash = 0;

                $("#mission_type").attr("class", "btn-floating deep-purple darken-2 modal-trigger");
                $("#mission_type").attr("href", "#modal_params_mon_search");
            }
        },
        add_circle: function () {
            if (area_map_bool == false) {
                add_area(1);
                area_map_bool = true;
                tipo_mision_dash = 1;

                $("#mission_type").attr("class", "btn-floating deep-purple darken-2 modal-trigger");
                $("#mission_type").attr("href", "#modal_params_vigilance");
            }
        },
        save_params: function () {
            switch (tipo_mision_dash){
                case 0:
                    var ne = rectangle.getBounds().getNorthEast();
                    var so = rectangle.getBounds().getSouthWest();

                    $("#norte_este_lat").attr("value", ne.lat());
                    $("#norte_este_lng").attr("value", ne.lng());
                    $("#sur_oeste_lat").attr("value", so.lat());
                    $("#sur_oeste_lng").attr("value", so.lng());

                    break;

                case 1:
                    var centro_lat = circle.getCenter().lat();
                    var centro_lng = circle.getCenter().lng();
                    var radio = Math.round(circle.getRadius() * 100);


                    $("#radio").attr("value", radio);
                    $("#centro_lat").attr("value", centro_lat);
                    $("#centro_lng").attr("value", centro_lng);

                    break;

                default:
                    break;
            }

            localStorage.setItem("center_lat", get_center_lat());
            localStorage.setItem("center_lng", get_center_lng());
        }
    }
});

$(document).ready(function () {
    $('.sidenav').sidenav();

    $('.fixed-action-btn').floatingActionButton();

    $('.modal').modal();

    $('select').formSelect();

    $("select[required]").css({
        display: "inline",
        height: 0,
        padding: 0,
        width: 0
    });
});

$(window).resize(function () {
    h = $(window).height()
    var offsetTop = 60; // Calculate the top offset

    $('#map').css('height', (h - offsetTop));
}).resize();