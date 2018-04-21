var map;
var markerDron1;

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

function setRoute(route) {
    var flightPlanCoordinates = [];

    for (var i = 0; i < route.length; i++) {
        latlngset = new google.maps.LatLng(route[i].latitud, route[i].longitud);
        flightPlanCoordinates.push(latlngset);

        new google.maps.Marker({
            map: map,
            position: latlngset,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 5,
                strokeColor:"#1976d2"
            }
        });
    }

    var flightPath = new google.maps.Polyline({
        path: flightPlanCoordinates,
        geodesic: true,
        strokeColor: '#1976d2',
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
        'title="Coordenadas: (' + lat + ', ' + lng + ', ' + alt + ')">\n' +
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


function setDronePosition(lat, lng) {
    var latlngset = new google.maps.LatLng(lat, lng);

    if (markerDron1) markerDron1.setMap(null);

    var url_icon = 'images/navigation/drone' + heading + '.png';

    var icon = {
        url: url_icon
    };

    markerDron1 = new google.maps.Marker({
        map: map,
        position: latlngset,
        draggable: false,
        icon: icon
    });
}
