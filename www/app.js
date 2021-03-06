var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var path = require("path");
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var zmq = require('zmq');
var req_genetic_algorithm = zmq.socket('req')


//Router
var dashboardRouter = require('./routes/dashboard');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use(express.static(path.join(__dirname, 'public')));

//Express router
app.use('/', dashboardRouter);

//Establish connection in port 5555 using ZMQ with the genetic algorithm code.
req_genetic_algorithm.connect("tcp://localhost:5555");

req_genetic_algorithm.on("message", function (reply) {
    console.log(reply.toString());
});


var locations = [
    [42.17042007861182, -8.68519511376951],
    [42.17042007861182, -8.681761886230447],
    [42.16854769367686, -8.68519511376951],
    [42.16854769367686, -8.681761886230447]
];
var x = 0;

io.on('connection', function (socket) {
    socket.on('start_mission', function (data) {
        console.log("Connecting to genetic_algoritm...");
        //req_genetic_algorithm.send(JSON.stringify(data));

        for (var i = 0; i < 5; i++) {
            setTimeout(function () {
                if(x < 4){
                    socket.emit('waypoints', {"lat": locations[x][0], "lng": locations[x][1], "img": "/images/prueba.jpg"});
                }
                else{
                    console.log("entra");
                    socket.emit('waypoints', {"lat": 42.17042007861182, "lng": -8.68519511376951, "img": "/images/prueba2.jpg"});
                }

                x = x + 1;
            }, i * 5000)
        }
    });
});


http.listen(3000, function () {
    console.log('listening on *:3000');
});

module.exports = app;