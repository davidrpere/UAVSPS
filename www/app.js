var express = require('express');
var app = express();
var path = require("path");
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var zmq = require('zmq');
var base64ToImage = require('base64-to-image');
process.setMaxListeners(0);

// Conectar con los modulos.
var req_algoritmo_genetico = zmq.socket('req');
var req_dron1 = zmq.socket('req');
var sub_dron1_latlng = zmq.socket('sub');
var sub_dron1_orientacion = zmq.socket('sub');

// RASP SARA
var sub_dron1_foto = zmq.socket('sub');
sub_dron1_foto.connect('tcp://192.168.43.219:8999');
sub_dron1_foto.subscribe('');

// Establecer conexiones
req_algoritmo_genetico.connect("tcp://localhost:7777");
req_dron1.connect("tcp://192.168.43.219:5558");
sub_dron1_latlng.connect("tcp://192.168.43.219:5557");
sub_dron1_orientacion.connect("tcp://192.168.43.219:5560");

// Suscripcion a topics
sub_dron1_latlng.subscribe('');
sub_dron1_orientacion.subscribe('');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')));

//Express
app.get('/', function (req, res) {
    res.render('dashboard');
});


app.get('/mission', function (req, res) {
    // Recibimos la ruta del algoritmo genetico y enviamos waypoints a los drones.
    req_algoritmo_genetico.on('message', function (data) {
        var arr = JSON.parse(data.toString());

        var jsonDron1 = arr[0].waypoints;
        var waypoints_dron1 = "";

        for (var i = 0; i < jsonDron1.length; i++) {
            waypoints_dron1 = waypoints_dron1 + (jsonDron1[i].latitud).toFixed(7) + "," + (jsonDron1[i].longitud).toFixed(7) + " ";

        }
        waypoints_dron1 = waypoints_dron1.trim();


        //Envio waypoints
        req_dron1.send(waypoints_dron1);
        res.render('mission');

        //Envio ruta a cliente
        io.on('connection', function (socket) {
            socket.emit("ruta", jsonDron1);
        });
    });
});


req_dron1.on('message', function (data) {
    console.log(data.toString());
});

//Obtencion de los parametros y contacto con el algoritmo genetico para obtener la ruta
io.on('connection', function (socket) {
    socket.on('start_mission', function (data) {
        var numero_drones = data['numero_drones'];
        var posiciones_base = [];

        for (var i = 0; i < numero_drones; i++) {
            posiciones_base.push([0, 0])
        }

        var jsonData = {
            'norte_este': data['norte_este'],
            'norte_oeste': data['norte_oeste'],
            'sur_este': data['sur_este'],
            'sur_oeste': data['sur_oeste'],
            'altura_vuelo': data['altura_vuelo'],
            'fraccion_solape': data['solapamiento'] / 100,
            'posiciones_base': posiciones_base
        };

        req_algoritmo_genetico.send(JSON.stringify(jsonData));
    });


});


// Obtener la posicion geografica de los drones y enviarlas al cliente
io.on('connection', function (socket) {
    sub_dron1_latlng.on('message', function (data) {
        var split = (data.toString()).split();
        var latlong = split[0].split(' ');
        var lat = latlong[0];
        var lng = latlong[1];

        socket.emit('dron1_posicion', {
            'lat': lat,
            'lng': lng
        });
    });
});

// Obtener la orientacion de los drones y enviarlas al cliente
io.on('connection', function (socket) {
    sub_dron1_orientacion.on('message', function (data) {
        var split = (data.toString()).split();
        var orientacion = split[0].trim();
        var split2 = orientacion.split(' ');

        socket.emit('dron1_orientacion', {
            'orientacion': split2[0]
        });
    });
});

io.on('connection', function (socket) {
    sub_dron1_foto.on('message', function (data) {
        var jsonFoto = JSON.parse(data.toString());
        var path ='public/fotos_dron/';
        var namePhoto = "img-" + Date.now();
        var optionalObj = {'fileName': namePhoto, 'type':'png'};
        var base64Str = jsonFoto['imagen'];
        var lat = jsonFoto['lat'];
        var lng = jsonFoto['lng'];
        var id_dron = jsonFoto['id_dron'];
        var alt = jsonFoto['alt'];

        console.log("lat: " + parseFloat(lat));
        console.log("lng: " + parseFloat(lng));
        console.log("id_dron: " + id_dron);
        console.log("alt: " + parseFloat(alt));

        base64ToImage("data:image/png;base64," + base64Str, path, optionalObj);

        socket.emit('foto', {
            'url': 'fotos_dron/' + namePhoto + '.png',
            'lat': lat,
            'lng': lng,
            'alt': alt
        });
    });
});

http.listen(3000, function () {
    console.log('listening on *:3000');
});