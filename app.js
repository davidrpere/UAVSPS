var express = require('express');
var app = express();
var path = require("path");
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var http = require('http').Server(app);
var io = require('socket.io')(http);
var zmq = require('zmq');
var base64ToImage = require('base64-to-image');
var mysql = require('mysql');

var con = mysql.createConnection({
  host: "localhost",
  user: "uavsps",
  password: "uavsps"
});

/***********************************************************************************************************************
 *                                  Configuracion comunicacion con algoritmo genetico
 **********************************************************************************************************************/
var req_algoritmo_genetico = zmq.socket('req');

req_algoritmo_genetico.connect("tcp://localhost:7777");

/***********************************************************************************************************************
 *                                  Configuracion comunicaciones con Dron1.
 **********************************************************************************************************************/
var req_dron1_envio_waypoints = zmq.socket('req');
var sub_dron1_latlng = zmq.socket('sub');
var sub_dron1_orientacion = zmq.socket('sub');
var sub_dron1_foto = zmq.socket('sub');

req_dron1_envio_waypoints.connect("tcp://192.168.43.219:5558");
sub_dron1_latlng.connect("tcp://192.168.43.219:5557");
sub_dron1_orientacion.connect("tcp://192.168.43.219:5560");
sub_dron1_foto.connect('tcp://192.168.43.219:8999');

sub_dron1_latlng.subscribe('');
sub_dron1_orientacion.subscribe('');
sub_dron1_foto.subscribe('');


/***********************************************************************************************************************
 *                                  Configuracion comunicaciones con Dron2.
 **********************************************************************************************************************/
var req_dron2_envio_waypoints = zmq.socket('req');
var sub_dron2_latlng = zmq.socket('sub');
var sub_dron2_orientacion = zmq.socket('sub');
var sub_dron2_foto = zmq.socket('sub');

req_dron2_envio_waypoints.connect("tcp://192.168.43.27:5558");
sub_dron2_latlng.connect("tcp://192.168.43.27:5557");
sub_dron2_orientacion.connect("tcp://192.168.43.27:5560");
sub_dron2_foto.connect('tcp://192.168.43.27:8999');

sub_dron2_latlng.subscribe('');
sub_dron2_orientacion.subscribe('');
sub_dron2_foto.subscribe('');

/***********************************************************************************************************************
 *                      Configuracion de motor de plantillas PUG, rutas, json, urlencoded
 **********************************************************************************************************************/
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');
app.use(logger('dev'));
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')));


/***********************************************************************************************************************
 *                                                  Lógica ExpressJS
 **********************************************************************************************************************/
app.get('/', function (req, res) {
    res.render('dashboard');
});

app.get('/mission', function (req, res) {
    // Recibimos la ruta del algoritmo genetico y enviamos waypoints a los drones.
    req_algoritmo_genetico.on('message', function (data) {
        var arr = JSON.parse(data.toString());

        for (var i = 0; i < arr.length; i++) {
            switch (i){
                case 0:
                    var jsonDron1 = arr[i].waypoints;
                    var waypoints_dron1 = "";

                    for (var j = 0; j < jsonDron1.length; j++) {
                        waypoints_dron1 = waypoints_dron1 + (jsonDron1[j].latitud).toFixed(7) + "," + (jsonDron1[j].longitud).toFixed(7) + " ";

                    }
                    waypoints_dron1 = waypoints_dron1.trim();

                    // Envio waypoints
                    req_dron1_envio_waypoints.send(waypoints_dron1);

                    break;
                case 1:
                    var jsonDron2 = arr[i].waypoints;
                    var waypoints_dron2 = "";

                    for (var j = 0; j < jsonDron1.length; j++) {
                        waypoints_dron2 = waypoints_dron2 + (jsonDron2[j].latitud).toFixed(7) + "," + (jsonDron2[j].longitud).toFixed(7) + " ";

                    }
                    waypoints_dron2 = waypoints_dron2.trim();

                    // Envio waypoints a dron 2
                    req_dron2_envio_waypoints.send(waypoints_dron2);

                    break;
            }
        }

        res.render('mission');

        // Envio ruta a cliente
        io.on('connection', function (socket) {
            socket.emit("ruta", arr);
        });
    });
});


io.on('connection', function (socket) {
    // Obtencion de los parametros y contacto con el algoritmo genetico para obtener la ruta
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

    /*******************************************************************************************************************
     *                           DRON 1 ACK ENVIO WAYPOINTS, TELEMETRIA E IMAGENES
     ******************************************************************************************************************/

    // Obtener la posicion geografica del dron1 y enviarlas al cliente
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

    // Obtener la orientacion del dron1 y enviarlas al cliente
    sub_dron1_orientacion.on('message', function (data) {
        var split = (data.toString()).split();
        var orientacion = split[0].trim();
        var split2 = orientacion.split(' ');

        socket.emit('dron1_orientacion', {
            'orientacion': split2[0]
        });
    });

    // Recibimos imagenes del dron1
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

        base64ToImage("data:image/png;base64," + base64Str, path, optionalObj);

        socket.emit('foto', {
            'url': 'fotos_dron/' + namePhoto + '.png',
            'lat': lat,
            'lng': lng,
            'alt': alt
        });
    });

    req_dron1_envio_waypoints.on('message', function (data) {
        console.log(data.toString());
    });


    /*******************************************************************************************************************
     *                           DRON 2 ACK ENVIO WAYPOINTS, TELEMETRIA E IMAGENES
     ******************************************************************************************************************/

    // Obtener la posicion geografica del dron2 y enviarlas al cliente
    sub_dron2_latlng.on('message', function (data) {
        var split = (data.toString()).split();
        var latlong = split[0].split(' ');
        var lat = latlong[0];
        var lng = latlong[1];

        socket.emit('dron2_posicion', {
            'lat': lat,
            'lng': lng
        });
    });

    // Obtener la orientacion del dron2 y enviarlas al cliente
    sub_dron2_orientacion.on('message', function (data) {
        var split = (data.toString()).split();
        var orientacion = split[0].trim();
        var split2 = orientacion.split(' ');

        socket.emit('dron2_orientacion', {
            'orientacion': split2[0]
        });
    });

    // Recibimos imagenes del dron2
    sub_dron2_foto.on('message', function (data) {
        var jsonFoto = JSON.parse(data.toString());
        var path ='public/fotos_dron/';
        var namePhoto = "img-" + Date.now();
        var optionalObj = {'fileName': namePhoto, 'type':'png'};
        var base64Str = jsonFoto['imagen'];
        var lat = jsonFoto['lat'];
        var lng = jsonFoto['lng'];
        var id_dron = jsonFoto['id_dron'];
        var alt = jsonFoto['alt'];

        base64ToImage("data:image/png;base64," + base64Str, path, optionalObj);

        socket.emit('foto', {
            'url': 'fotos_dron/' + namePhoto + '.png',
            'lat': lat,
            'lng': lng,
            'alt': alt
        });
    });

    req_dron2_envio_waypoints.on('message', function (data) {
        console.log(data.toString());
    });

    var nombreMision;
     var auxIdMision;
     var auxIdDronMision;
     var fotos =[];
     var fecha;
     var alturaRelativa;

  con.connect(function(err) {
   con.query("SELECT Nombre_mision, ID_mision, Fecha, Altitud_vuelo FROM Mision", function (err, rows) {
     if (err) throw err;
     rows.forEach( (row) => {
       console.log("Resultado de la mision n : "+`${row.Nombre_mision}`, `${row.ID_mision}`, `${row.Fecha}`, `${row.Altitud_vuelo}` );
       nombreMision = `${row.Nombre_mision}` ;
       auxIdMision = `${row.ID_mision}`;
       Fecha = `${row.Fecha}`;
       alturaRelativa = `${row.Altitud_vuelo}`;

       con.query("SELECT ID_dron_mision FROM Dron_mision WHERE ID_mision='"+auxIdMision+"'", function (err, rows) {
         if (err) throw err;
         rows.forEach( (row) => {
           console.log("Resultado de la busqueda de ID_dron_mision coincidente con la mision n: "+`${row.ID_dron_mision}` );
           auxIdDronMision = `${row.ID_dron_mision}` ;

           con.query("SELECT Foto FROM Fotos WHERE ID_dron_mision='"+auxIdDronMision+"'", function (err, rows) {
             if (err) throw err;
             for (i = 0; i < rows.length; i++) {
               fotos.push((rows[i].Foto).toString());
             }
             console.log("El resultado de la busqueda de fotos de la mision es "+ fotos);
             socket.emit("historial", {
               'nombre' : nombreMision,
               'fecha' : Fecha,
               'altura' : alturaRelativa,
               'fotos' : fotos});
           });

         });
       });


     });
   });



 });

});


http.listen(3000, function () {
    console.log('listening on *:3000');
});
