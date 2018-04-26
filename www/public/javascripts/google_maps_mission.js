var map;
var markerDron1;
var markerDron2;
var marker_photo;
var positive_marker = [];
var last_photo_positive = false;
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

function clear_map() {
    if(circle) circle.setMap(null);
    if(flightPath) flightPath.setMap(null);
    for (var i = 0; i < marker_flightPath.length; i++) {
        marker_flightPath[i].setMap(null);
    }
    for (var i = 0; i < positive_marker.length; i++) {
        positive_marker[i].setMap(null);
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

function setPhoto(lat, lng, path, positive, color) {
    var latlngset = new google.maps.LatLng(lat, lng);

    if (!last_photo_positive && marker_photo)
        marker_photo.setMap(null);

    if (positive > 0){
        last_photo_positive = true;
        var new_maker = true;

        for (var i = 0; i < positive_marker.length; i++) {
            if (positive_marker[i].getPosition().lat() == latlngset.lat() &&
                positive_marker[i].getPosition().lng() == latlngset.lng()) {
                new_maker = false;
            }
        }

        if (new_maker){
            marker_photo = new google.maps.Marker({
                map: map,
                position: latlngset,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: 10,
                    strokeColor: color,
                    strokeOpacity: 1,
                    strokeWeight: 3,
                    fillOpacity: 1,
                    fillColor: '#4CAF50',
                    fillOpacity: 0.8
                }
            });

            positive_marker.push(marker_photo);

            google.maps.event.addListener(marker_photo, 'click', function () {
                $.magnificPopup.open({
                    type: 'image',
                    items: {
                        src: path
                    }
                });
            });
        }
    }else {
        last_photo_positive = false;

        var aux_positive_marker = [];
        for (var i = 0; i < positive_marker.length; i++) {
            if(positive_marker[i].getPosition().lat() == latlngset.lat() &&
                positive_marker[i].getPosition().lng() == latlngset.lng()){
                positive_marker[i].setMap(null);
            }else {
                aux_positive_marker.push(positive_marker[i]);
            }
        }

        positive_marker = aux_positive_marker;

        marker_photo = new google.maps.Marker({
            map: map,
            position: latlngset,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 10,
                strokeColor: color,
                strokeOpacity: 1,
                strokeWeight: 3,
                fillOpacity: 1,
                fillColor: '#F44336',
                fillOpacity: 0.8
            }
        });

        google.maps.event.addListener(marker_photo, 'click', function () {
            $.magnificPopup.open({
                type: 'image',
                items: {
                    src: path
                }
            });
        });
    }
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
                            src: 'http://192.168.43.219:8000/index.html'
                        }
                    });
                });
            }

            break;

        default:
            break;
    }
}