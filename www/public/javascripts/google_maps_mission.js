var map;
var markerDron1;
var markerDron2;
var flightPath;
var circle;
var marker_flightPath = [];

function mission_map() {
    var lat = parseFloat(localStorage.getItem('center_lat'));
    var lng = parseFloat(localStorage.getItem('center_lng'));

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 19,
        center: {
            lat: lat,
            lng: lng
        },
        mapTypeId: 'satellite',
        mapTypeControl: false,
        scaleControl: true,
        fullscreenControl: false,
        gestureHandling: 'auto',
        disableDoubleClickZoom: false,
        zoomControl: true,
        tilt: 0,
        zoomControlOptions: {
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        streetViewControl: false,
        rotateControl: false
    });
}

function clear_routes() {
    if(circle) circle.setMap(null);
    if(flightPath) flightPath.setMap(null);
    for (var i = 0; i < marker_flightPath.length; i++) {
        marker_flightPath[i].setMap(null);
    }
}

function setRouteMonBusqueda(route, color) {
    var flightPlanCoordinates = [];

    for (var i = 0; i < route.length; i++) {
        latlngset = new google.maps.LatLng(route[i].latitud, route[i].longitud);
        flightPlanCoordinates.push(latlngset);

        var marker = new google.maps.Marker({
            map: map,
            position: latlngset,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 3,
                strokeColor: color,
                fillColor: color,
                fillOpacity: 1.0
            }
        });

        marker_flightPath.push(marker);
    }

    flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: color,
        strokeOpacity: 1.0,
        strokeWeight: 3
    });

    flightPath.setMap(map);
}

function setRouteVigilancia(radio, centro_lat, centro_lng, color) {
    var latlngset = new google.maps.LatLng(centro_lat, centro_lng);
    radio = parseInt(radio) / 100

    circle = new google.maps.Circle({
        strokeColor: color,
        strokeOpacity: 1,
        strokeWeight: 3,
        fillOpacity: 0.0,
        center: latlngset,
        radius: radio
    });

    circle.setMap(map);
}

function setPhoto(lat, lng, path) {
    var latlngset = new google.maps.LatLng(lat, lng);

    var marker = new google.maps.Marker({
        map: map,
        position: latlngset,
        icon: '/images/pin.png'
    });


    google.maps.event.addListener(marker, 'click', function () {
        $.magnificPopup.open({
            type: 'image',
            items: {
                src: path
            }
        });
    });
}


function setDronePosition(lat, lng, orientacion, id_dron) {
    var latlng = new google.maps.LatLng(lat, lng);

    switch (id_dron){
        case 1:
            var icon = {
                url: 'images/navigation_dron1/drone' + orientacion + '.png'
            };

            if (markerDron1) {
                markerDron1.setIcon(icon);
                markerDron1.setPosition(latlng);
            }else{
                markerDron1 = new google.maps.Marker({
                    map: map,
                    position: latlng,
                    draggable: false,
                    icon: icon
                });

                google.maps.event.addListener(markerDron1, 'click', function () {
                    $.magnificPopup.open({
                        type: 'iframe',
                        items: {
                            src: 'http://192.168.43.92:8000/index.html'
                        }
                    });
                });
            }

            break;

        case 2:
            var icon = {
                url: 'images/navigation_dron2/drone' + orientacion + '.png'
            };

            if (markerDron2) {
                markerDron2.setIcon(icon);
                markerDron2.setPosition(latlng);
            }else{
                markerDron2 = new google.maps.Marker({
                    map: map,
                    position: latlng,
                    draggable: false,
                    icon: icon
                });

                google.maps.event.addListener(markerDron2, 'click', function () {
                    $.magnificPopup.open({
                        type: 'iframe',
                        items: {
                            src: 'http://192.168.43.244:8000/index.html'
                        }
                    });
                });
            }

            break;

        default:
            break;
    }
}