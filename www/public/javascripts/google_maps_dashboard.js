var rectangle;
var circle;
var map;
var markerDron1;
var markerDron2;

function initAutocomplete() {
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 19,
        center: {
            lat: 42.1694839,
            lng: -8.683478499999978
        },
        mapTypeId: 'satellite',
        mapTypeControl: false,
        scaleControl: true,
        fullscreenControl: false,
        disableDoubleClickZoom: false,
        gestureHandling: 'auto',
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

    // Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function () {
        searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function () {
        var places = searchBox.getPlaces();

        if (places.length == 0) {
            return;
        }

        // Clear out the old markers.
        markers.forEach(function (marker) {
            marker.setMap(null);
        });
        markers = [];

        // For each place, get name and location.
        var bounds = new google.maps.LatLngBounds();
        places.forEach(function (place) {
            if (!place.geometry) {
                console.log('Returned place contains no geometry');
                return;
            }

            // Create a marker for each place.
            markers.push(new google.maps.Marker({
                map: map,
                title: place.name,
                position: place.geometry.location
            }));

            if (place.geometry.viewport) {
                // Only geocodes have viewport.
                bounds.union(place.geometry.viewport);
            } else {
                bounds.extend(place.geometry.location);
            }
        });
        map.fitBounds(bounds);
    });

}

function get_center_lat() {
    return map.getCenter().lat();
}

function get_center_lng() {
    return map.getCenter().lng();
}

function add_area(tipo_area) {

    // Tipo 0: rectangulo, tipo 1: circulo.
    switch (tipo_area) {
        case 0:
            //Define the LatLng coordinates for the rectangle.
            var jsonMapBounds = map.getBounds().toJSON();
            var jsonMapCenter = map.getCenter().toJSON();
            var north = midpoint_coordinates(jsonMapBounds.north, jsonMapCenter.lng, jsonMapCenter.lat, jsonMapCenter.lng).lat;
            var south = midpoint_coordinates(jsonMapCenter.lat, jsonMapCenter.lng, jsonMapBounds.south, jsonMapCenter.lng).lat;
            var east = midpoint_coordinates(jsonMapCenter.lat, jsonMapCenter.lng, jsonMapCenter.lat, jsonMapBounds.east).lon;
            var west = midpoint_coordinates(jsonMapCenter.lat, jsonMapCenter.lng, jsonMapCenter.lat, jsonMapBounds.west).lon;

            var bounds = {
                north: north,
                south: south,
                east: east,
                west: west
            };

            // Construct the polygon.
            rectangle = new google.maps.Rectangle({
                bounds: bounds,
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.35,
                map: map,
                editable: true,
                draggable: true
            });

            break;

        case 1:
            //Define the LatLng coordinates for the rectangle.
            var jsonMapCenter = map.getCenter().toJSON();
            var jsonMapBounds = map.getBounds().toJSON();

            var radio = midpoint_coordinates(jsonMapBounds.north, jsonMapCenter.lng, jsonMapCenter.lat, jsonMapCenter.lng).lat;


            circle = new google.maps.Circle({
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.35,
                map: map,
                center: jsonMapCenter,
                radius: radio,
                editable: true,
                draggable: true
            });

            break;
    }

}

function remove_area() {
    if (rectangle)
        rectangle.setMap(null);

    if (circle)
        circle.setMap(null);
}

function midpoint_coordinates(lat1, lon1, lat2, lon2) {
    var dLon = (lon2 - lon1) * (Math.PI / 180);

    //convert to rad
    lat1 = lat1 * (Math.PI / 180);
    lat2 = lat2 * (Math.PI / 180);
    lon1 = lon1 * (Math.PI / 180);

    var Bx = Math.cos(lat2) * Math.cos(dLon);
    var By = Math.cos(lat2) * Math.sin(dLon);

    var lat3 = Math.atan2(Math.sin(lat1) + Math.sin(lat2), Math.sqrt((Math.cos(lat1) + Bx) * (Math.cos(lat1) + Bx) + By * By));
    var lon3 = lon1 + Math.atan2(By, Math.cos(lat1) + Bx);

    //Convert to degrees
    lat3 = lat3 * (180 / Math.PI);
    lon3 = lon3 * (180 / Math.PI);

    return {'lat': lat3, 'lon': lon3}
}

function setDronePosition(lat, lng, orientacion, id_dron) {
    var latlng = new google.maps.LatLng(lat, lng);

    switch (id_dron) {
        case 1:
            var icon = {
                url: 'images/navigation_dron1/drone' + orientacion + '.png'
            };

            if (markerDron1) {
                markerDron1.setIcon(icon);
                markerDron1.setPosition(latlng);
            } else {
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
                            src: 'http://192.168.43.219:8000/index.html'
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
            } else {
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
                            src: 'http://192.168.43.92:8000/index.html'
                        }
                    });
                });
            }

            break;
    }
}