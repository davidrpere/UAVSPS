var rectangle;

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

      //map.setCenter(pos);
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
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 18,
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

  //Define the LatLng coordinates for the rectangle.
  var bounds = {
    north: 42.1694839,
    south: 42.1734839,
    east: -8.683478499999978,
    west: -8.689478499999978
  };

  // Construct the polygon.
  rectangle = new google.maps.Rectangle({
    bounds: bounds,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35,
    editable: true,
    draggable: true
  });
  rectangle.setMap(map);
}

function sendCoords() {
  var bounds = rectangle.getBounds();
  var northEast = bounds.getNorthEast();
  var southWest = bounds.getSouthWest();
  var northWest = new google.maps.LatLng(northEast.lat(), southWest.lng());
  var southEast = new google.maps.LatLng(southWest.lat(), northEast.lng());

  console.log("northWest (lat/long): " + northWest);
  console.log("northEast (lat/long): " + northEast);
  console.log("southWest (lat/long): " + southWest);
  console.log("southEast (lat/long): " + southEast);
}
