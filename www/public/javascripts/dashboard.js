var rectPoly;
var mapa;
var params;

var btnContinue = new Vue({
    el: '#btnContinue',
    methods: {
        getData: function() {
            if (!$("#nombre_mision").val()) {
                alert_name_mision.seen = true
            } else {
                params = $("form").serializeArray()
                $('#modalCenter').modal('toggle')
                btnSetMission.seen = false
                btnArea.seen = true
            }
        }
    }
})

var btnClose = new Vue({
    el: "#btnClose",
    methods: {
        hide_alert_name_mision: function() {
            alert_name_mision.seen = false
        }
    }
})

var btnSetMission = new Vue({
    el: "#btnSetMission",
    data: {
        seen: true
    }
})

var btnArea = new Vue({
    el: "#btnArea",
    data: {
        seen: false
    },
    methods: {
        add_area: function() {
            add_area();
        },
        remove_area: function() {
            remove_area();
        },
        start_mission: function() {
            var coordinates = getCoordinates()

            console.log(coordinates);
            console.log(params)

            var socket = io();
            socket.emit('empezar_mision', { my: 'data1'});
        }
    }
})

var name_mission = new Vue({
    el: "#nombre_mision",
    methods: {
        hide_alert_name_mision: function() {
            alert_name_mision.seen = false
        }
    }
})

var alert_name_mision = new Vue({
    el: '#alert_name_mision',
    data: {
        seen: false
    }
})

/**
 * Google Maps
 */
function initMap() {
    /*var map;
    // Try HTML5 geolocation.
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };

        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 18,
          center: {
            lat: 42.1694839,
            lng: -8.683478499999978
          },
          mapTypeId: 'satellite',
          mapTypeControl: false,
          scaleControl: true,
          fullscreenControl: false
        });

        map.setCenter(pos);
      }, function() {
        map = new google.maps.Map(document.getElementById('map'), {
          zoom: 18,
          center: {
            lat: 42.1694839,
            lng: -8.683478499999978
          },
          mapTypeId: 'satellite',
          mapTypeControl: false,
          scaleControl: true,
          fullscreenControl: false
        });
      });
    } else {
      // Browser doesn't support Geolocation
      map = new google.maps.Map(document.getElementById('map'), {
        zoom: 18,
        center: {
          lat: 42.1694839,
          lng: -8.683478499999978
        },
        mapTypeId: 'satellite',
        mapTypeControl: false,
        scaleControl: true,
        fullscreenControl: false
      });
    }*/
    mapa = new google.maps.Map(document.getElementById('map'), {
        zoom: 16,
        center: {
            lat: 42.1694839,
            lng: -8.683478499999978
        },
        mapTypeId: 'satellite',
        mapTypeControl: false,
        scaleControl: true,
        fullscreenControl: false,
        heading: 90,
        tilt: 45
    });
}

function add_area() {
    //Define the LatLng coordinates for the rectangle.
    var bounds = {
        north: 42.1694839,
        south: 42.1634839,
        east: -8.683478499999978,
        west: -8.689478499999978
    };

    // Construct the polygon.
    var rectangle = new google.maps.Rectangle({
        bounds: bounds,
        strokeColor: '#FF0000',
        strokeOpacity: 0.8,
        strokeWeight: 2,
        fillColor: '#FF0000',
        fillOpacity: 0.35,
        map: mapa,
        editable: true,
        draggable: true
    });

    rectPoly = createPolygonFromRectangle(rectangle);
}

function remove_area() {
    rectPoly.setMap(null)
}

function createPolygonFromRectangle(rectangle) {
    var map = rectangle.getMap();

    var coords = [{
        lat: rectangle.getBounds().getNorthEast().lat(),
        lng: rectangle.getBounds().getNorthEast().lng()
    },
        {
            lat: rectangle.getBounds().getNorthEast().lat(),
            lng: rectangle.getBounds().getSouthWest().lng()
        },
        {
            lat: rectangle.getBounds().getSouthWest().lat(),
            lng: rectangle.getBounds().getSouthWest().lng()
        },
        {
            lat: rectangle.getBounds().getSouthWest().lat(),
            lng: rectangle.getBounds().getNorthEast().lng()
        }
    ];

    // Construct the polygon.
    var rectPoly = new google.maps.Polygon({
        path: coords,
        editable: true,
        draggable: true
    });
    var properties = ["strokeColor", "strokeOpacity", "strokeWeight", "fillOpacity", "fillColor"];
    //inherit rectangle properties
    var options = {};
    properties.forEach(function(property) {
        if (rectangle.hasOwnProperty(property)) {
            options[property] = rectangle[property];
        }
    });
    rectPoly.setOptions(options);

    rectangle.setMap(null);
    rectPoly.setMap(map);
    return rectPoly;
}

function getCoordinates() {
    var contentString;
    var vertices = rectPoly.getPath();

    // Iterate over the vertices.
    for (var i = 0; i < vertices.getLength(); i++) {
        var xy = vertices.getAt(i);
        contentString += '<br>' + 'Coordinate ' + i + ':<br>' + xy.lat() + ',' +
            xy.lng();
    }
    return contentString;

}
