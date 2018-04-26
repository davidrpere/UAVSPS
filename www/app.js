var express = require('express'),
    app = express(),
    http = require('http'),
    server = http.createServer(app),
    path = require("path"),
    io = require('socket.io')({transports  : ['websocket']}).listen(server),
    zmq  = require('zmq'),
    cookieParser = require('cookie-parser'),
    logger = require('morgan'),
    bodyParser = require('body-parser'),
    base64ToImage = require('base64-to-image');

/***********************************************************************************************************************
 * Variables globales del sistema.
 **********************************************************************************************************************/
var tipoMision = -1,
    heading_dron1 = 0,
    heading_dron2 = 0,
    dron1_activo = true,
    dron2_activo = true;

/***********************************************************************************************************************
 * Configuración comunicacion con módulo OpenCV.
 **********************************************************************************************************************/
var opencv = zmq.socket('req');

opencv.connect("tcp://localhost:6666");

/***********************************************************************************************************************
 * Configuración comunicacion con módulo algoritmo genético.
 **********************************************************************************************************************/
var req_algoritmo_genetico = zmq.socket('req');

req_algoritmo_genetico.connect("tcp://localhost:7777");

/***********************************************************************************************************************
 * Configuración publicador fin de misión.
 **********************************************************************************************************************/
var pub_fin_mision = zmq.socket('pub');
pub_fin_mision.bind('tcp://*:8888');


/***********************************************************************************************************************
 * Configuración comunicaciones con Dron1.
 **********************************************************************************************************************/
var req_dron1_envio_waypoints = zmq.socket('req'),
    sub_dron1_latlng = zmq.socket('sub'),
    sub_dron1_orientacion = zmq.socket('sub'),
    sub_dron1_foto = zmq.socket('sub');

/* CODIGO PARA USO DEL DRON
req_dron1_envio_waypoints.connect("tcp://192.168.43.92:5558");
sub_dron1_latlng.connect("tcp://192.168.43.92:5557");
sub_dron1_orientacion.connect("tcp://192.168.43.92:5560");
sub_dron1_foto.connect('tcp://192.168.43.92:8999');
sub_dron1_latlng.subscribe('');
sub_dron1_orientacion.subscribe('');
sub_dron1_foto.subscribe('');
*/

req_dron1_envio_waypoints.connect("tcp://localhost:5558");
sub_dron1_latlng.connect("tcp://localhost:5557");
sub_dron1_orientacion.connect("tcp://localhost:5560");
sub_dron1_foto.connect('tcp://localhost:8999');

sub_dron1_latlng.subscribe('');
sub_dron1_orientacion.subscribe('');
sub_dron1_foto.subscribe('');


/***********************************************************************************************************************
 * Configuración comunicaciones con Dron2.
 **********************************************************************************************************************/
var req_dron2_envio_waypoints = zmq.socket('req'),
    sub_dron2_latlng = zmq.socket('sub'),
    sub_dron2_orientacion = zmq.socket('sub'),
    sub_dron2_foto = zmq.socket('sub');

/* CODIGO PARA USO DEL DRON
req_dron2_envio_waypoints.connect("tcp://192.168.43.219:5558");
sub_dron2_latlng.connect("tcp://192.168.43.219:5557");
sub_dron2_orientacion.connect("tcp://192.168.43.219:5560");
sub_dron2_foto.connect('tcp://192.168.43.219:8999');
sub_dron2_latlng.subscribe('');
sub_dron2_orientacion.subscribe('');
sub_dron2_foto.subscribe('');
*/

req_dron2_envio_waypoints.connect("tcp://localhost:6558");
sub_dron2_latlng.connect("tcp://localhost:6557");
sub_dron2_orientacion.connect("tcp://localhost:6560");
sub_dron2_foto.connect('tcp://localhost:8999');

sub_dron2_latlng.subscribe('');
sub_dron2_orientacion.subscribe('');
sub_dron2_foto.subscribe('');


/***********************************************************************************************************************
 * Configuración de motor de plantillas PUG, rutas, json, urlencoded.
 **********************************************************************************************************************/
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');
app.use(logger('dev'));
app.use(cookieParser());
app.use(express.json());
app.use(bodyParser.json() );
app.use(bodyParser.urlencoded({extended: true }));
app.use(express.urlencoded({extended: false }));
app.use(express.static(path.join(__dirname, 'public')));


/***********************************************************************************************************************
 * Lógica ExpressJS.
 **********************************************************************************************************************/
app.get('/', function (req, res) {
    res.render('dashboard');
});

app.post('/mision', function (req, res) {
    tipoMision = parseInt(req.body.tipo_mision);

    // Tipo 0: Monitorización, tipo 1: búsqueda de personas, tipo 2: vigilancia.
    switch (tipoMision){
        case 0:
        case 1:
            var numero_drones = parseInt(req.body.numero_drones);
            var posiciones_base = [];

            for (var i = 0; i < numero_drones; i++) {
                posiciones_base.push([0, 0])
            }

            var jsonData = {
                'norte_este': {
                    'lat': req.body.norte_este_lat,
                    'lng': req.body.norte_este_lng
                },
                'sur_oeste': {
                    'lat': req.body.sur_oeste_lat,
                    'lng': req.body.sur_oeste_lng
                },
                'altura_vuelo': req.body.altura_vuelo,
                'fraccion_solape': parseInt(req.body.solapamiento_img) / 100,
                'posiciones_base': posiciones_base
            };

            req_algoritmo_genetico.send(JSON.stringify(jsonData));

            break;
        case 2:
            var radio = req.body.radio;
            var centro_lat = req.body.centro_lat;
            var centro_lng = req.body.centro_lng;

            console.log("v " + centro_lat+","+centro_lng+" " + radio);

            if(dron1_activo){
                req_dron1_envio_waypoints.send("v " + centro_lat+","+centro_lng+" " + radio);

                io.on('connection', function (socket) {
                    socket.emit("ruta_vigilancia", {
                        "radio": radio,
                        "centro_lat": centro_lat,
                        "centro_lng": centro_lng,
                        "id_dron": 1
                    });
                });
            } else{
                if (dron2_activo){
                    req_dron2_envio_waypoints.send("v " + centro_lat+","+centro_lng+" " + radio);

                    io.on('connection', function (socket) {
                        socket.emit("ruta_vigilancia", {
                            "radio": radio,
                            "centro_lat": centro_lat,
                            "centro_lng": centro_lng,
                            "id_dron": 2
                        });
                    });
                }
            }

            break;
    }

    res.render('mission');
});

/***********************************************************************************************************************
 * Conexiones frontend - backend + resto de servicios.
 **********************************************************************************************************************/

io.on('connection', function (socket) {
    /*******************************************************************************************************************
     * Recibimos la ruta del algoritmo genetico y enviamos waypoints a los drones.
     ******************************************************************************************************************/
    req_algoritmo_genetico.on('message', function (data) {
        var arr = JSON.parse(data.toString());

        for (var i = 0; i < arr.length; i++) {
            switch (i) {
                case 0:
                    var jsonDron1 = arr[i].waypoints;
                    var waypoints_dron1 = "";

                    for (var j = 0; j < jsonDron1.length; j++) {
                        waypoints_dron1 = waypoints_dron1 + (jsonDron1[j].latitud).toFixed(7) + ","
                            + (jsonDron1[j].longitud).toFixed(7) + " ";

                    }
                    waypoints_dron1 = waypoints_dron1.trim();

                    // Envio waypoints a dron 1, si no esta activo, se lo enviamos al dron 2, si este no esta activo,
                    // no se envian los waypoints
                    if(dron1_activo){
                        req_dron1_envio_waypoints.send(waypoints_dron1);
                    } else{
                        if (dron2_activo) {
                            req_dron2_envio_waypoints.send(waypoints_dron1);
                        }
                    }

                    break;
                case 1:
                    var jsonDron2 = arr[i].waypoints;
                    var waypoints_dron2 = "m ";

                    for (var j = 0; j < jsonDron1.length; j++) {
                        waypoints_dron2 = waypoints_dron2 + (jsonDron2[j].latitud).toFixed(7) + ","
                            + (jsonDron2[j].longitud).toFixed(7) + " ";

                    }
                    waypoints_dron2 = waypoints_dron2.trim();

                    // Envio waypoints a dron 2
                    if(dron2_activo)
                        req_dron2_envio_waypoints.send(waypoints_dron2);

                    break;
            }
        }

        socket.emit("ruta_mon_busqueda", arr);
    });

    /*******************************************************************************************************************
     * Recibimos respuesta OpenCV y enviamos la foto al cliente
     ******************************************************************************************************************/
    opencv.on('message', function (data) {
        var jsonOpenCV = JSON.parse(data.toString());
        var positivo = jsonOpenCV['positivo'];
        var id_dron = jsonOpenCV['id_dron'];

        console.log("Respuesta del modulo OpenCV => " + "[id_dron: " + id_dron + ", positivo: " + positivo);

        socket.emit('foto', {
            'url': 'fotos_dron/' + namePhoto + '.png',
            'lat': lat,
            'lng': lng,
            'alt': alt,
            'id_dron': parseInt(id_dron),
            'positivo': parseInt(positivo)
        });
    });

    /*******************************************************************************************************************
     * DRON 1: Recibimos la posicion geografica y la orientación y enviarlas al cliente.
     ******************************************************************************************************************/
    sub_dron1_latlng.on('message', function (data) {
        var split = (data.toString()).split();
        var latlong = split[0].split(' ');
        var lat = latlong[0];
        var lng = latlong[1];
        dron1_activo = true;

        socket.emit('posicion', {
            'id_dron': 1,
            'lat': lat,
            'lng': lng,
            'orientacion': heading_dron1
        });
    });

    /*******************************************************************************************************************
     * DRON 1: Recibimos la orientacion.
     ******************************************************************************************************************/
    sub_dron1_orientacion.on('message', function (data) {
        /* CODIGO PARA USO DEL DRON
        var split = (data.toString()).split();
        var orientacion = split[0].trim();
        var split2 = orientacion.split(' ');

        heading_dron1 = parseInt(split2[0]);
        */

        heading_dron1 = data.toString().trim();
    });

    /*******************************************************************************************************************
     * DRON 1: Recibimos imagenes.
     ******************************************************************************************************************/
    sub_dron1_foto.on('message', function (data) {
        var jsonFoto = JSON.parse(data.toString());
        var path = 'public/fotos_dron/';
        var namePhoto = "img-" + Date.now();
        var optionalObj = {'fileName': namePhoto, 'type': 'png'};
        var base64Str = jsonFoto['imagen'];
        var lat = jsonFoto['lat'];
        var lng = jsonFoto['lng'];
        var id_dron = jsonFoto['id_dron'];
        var alt = jsonFoto['alt'];

        base64ToImage("data:image/png;base64," + base64Str, path, optionalObj);

        // Tipo 0: Monitorización, tipo 1: búsqueda de personas, tipo 2: vigilancia.
        switch (tipoMision){
            case 1:
            case 2:
                var ruta = '/Users/rubenperezvaz/UAVSPS/www/public/fotos_dron/' + namePhoto + '.png';
                opencv.send(JSON.stringify({'ruta': ruta, 'id_dron': 1}));

                break;
            default:
                break;
        }
    });


    req_dron1_envio_waypoints.on('message', function (data) {
        console.log(data.toString());
    });


    /*******************************************************************************************************************
     * DRON 2: Recibimos la posicion geografica y la orientación y enviarlas al cliente.
     ******************************************************************************************************************/
    sub_dron2_latlng.on('message', function (data) {
        var split = (data.toString()).split();
        var latlong = split[0].split(' ');
        var lat = latlong[0];
        var lng = latlong[1];

        dron2_activo = true;

        socket.emit('posicion', {
            'id_dron': 2,
            'lat': lat,
            'lng': lng,
            'orientacion': heading_dron2
        });
    });


    /*******************************************************************************************************************
     * DRON 2: Recibimos la orientacion
     ******************************************************************************************************************/
    sub_dron2_orientacion.on('message', function (data) {
        /*CODIGO PARA USO DEL DRON
        var split = (data.toString()).split();
        var orientacion = split[0].trim();
        var split2 = orientacion.split(' ');

        heading_dron2 = parseInt(split2[0]);
        */

        heading_dron2 = data.toString().trim();
    });


    /*******************************************************************************************************************
     * DRON 2: Recibimos imagenes.
     ******************************************************************************************************************/
    sub_dron2_foto.on('message', function (data) {
        var jsonFoto = JSON.parse(data.toString());
        var path = 'public/fotos_dron/';
        var namePhoto = "img-" + Date.now();
        var optionalObj = {'fileName': namePhoto, 'type': 'png'};
        var base64Str = jsonFoto['imagen'];
        var lat = jsonFoto['lat'];
        var lng = jsonFoto['lng'];
        var id_dron = jsonFoto['id_dron'];
        var alt = jsonFoto['alt'];

        base64ToImage("data:image/png;base64," + base64Str, path, optionalObj);

        // Tipo 0: Monitorización, tipo 1: búsqueda de personas, tipo 2: vigilancia.
        switch (tipoMision){
            case 1:
            case 2:
                var ruta = '/Users/rubenperezvaz/UAVSPS/www/public/fotos_dron/' + namePhoto + '.png'
                opencv.send(JSON.stringify({'ruta': ruta, 'id_dron': 2}));

                break;
            default:
                break;
        }
    });

    // Consultar con DAVID.
    req_dron2_envio_waypoints.on('message', function (data) {
        console.log(data.toString());
    });

    /*******************************************************************************************************************
     * Aviso fin de misión.
     ******************************************************************************************************************/
    socket.on("finalizar_mision", function (data) {
        console.log(data.mensaje);
        pub_fin_mision.send(JSON.stringify({'mensaje': data.mensaje}));
    });

});

server.listen(3000, function () {
    console.log('Express server listening on port 3000');
});

module.exports = app;