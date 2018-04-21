var map;
var markerDron1;
var markerDron2;

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
        streetViewControl: true,
        streetViewControlOptions: {
            position: google.maps.ControlPosition.LEFT_BOTTOM
        },
        rotateControl: false
    });
}

function setRoute(route, color) {
    var flightPlanCoordinates = [];

    for (var i = 0; i < route.length; i++) {
        latlngset = new google.maps.LatLng(route[i].latitud, route[i].longitud);
        flightPlanCoordinates.push(latlngset);

        new google.maps.Marker({
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
    }

    var flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: color,
        strokeOpacity: 1.0,
        strokeWeight: 2
    });

    flightPath.setMap(map);
}

function setPhoto(lat, lng, path, alt) {
    latlngset = new google.maps.LatLng(lat, lng);

    var marker = new google.maps.Marker({
        map: map,
        position: latlngset,
        icon: '/images/pin.png'
    });


    var content = '<a class="image-popup-vertical-fit" href="' + path + '" ' +
        'title="Coordenadas: (' + lat + ', ' + lng + '), altura: ' + alt + '.">\n' +
        '\t<img src="' + path + '" width="200"></a>';

    var infowindow = new google.maps.InfoWindow();

    google.maps.event.addListener(marker, 'click', (function (marker, content, infowindow) {
        return function () {
            infowindow.setContent(content);
            infowindow.open(map, marker);
        };
    })(marker, content, infowindow));

    google.maps.event.addListener(infowindow, 'domready', function () {
        $('.image-popup-vertical-fit').magnificPopup({
            type: 'image',
            closeOnContentClick: true,
            mainClass: 'mfp-img-mobile',
            image: {
                verticalFit: true
            }

        });
    });
}


function setDronePosition(lat, lng, id_dron) {
    var latlngset = new google.maps.LatLng(lat, lng);

    switch (id_dron){
        case 1:
            if (markerDron1) markerDron1.setMap(null);

            var url_icon = 'images/navigation_dron1/drone' + heading_dron1 + '.png';

            var icon = {
                url: url_icon
            };

            markerDron1 = new google.maps.Marker({
                map: map,
                position: latlngset,
                draggable: false,
                icon: icon
            });
            break;

        case 2:
            if (markerDron2) markerDron2.setMap(null);

            var url_icon = 'images/navigation_dron2/drone' + heading_dron2 + '.png';

            var icon = {
                url: url_icon
            };

            markerDron2 = new google.maps.Marker({
                map: map,
                position: latlngset,
                draggable: false,
                icon: icon
            });

            break;
    }
}