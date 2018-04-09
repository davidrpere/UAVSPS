var express = require('express');
var app = express();
var http = require('http').Server(app);
var io = require('socket.io')(http);
var path = require("path");
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var zmq = require('zmq');

//Router
var dashboardRouter = require('./routes/dashboard');

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'pug');

app.use(logger('dev'));
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));
app.use('*', dashboardRouter);


io.on('connection', function (socket) {
    socket.on('start_mission', function (data) {
        console.log("Connecting to genetic_algoritm...");
        var requester = zmq.socket('req');

        requester.connect("tcp://localhost:5555");

        requester.send(JSON.stringify(data));

        requester.on("message", function(reply) {
            console.log(reply.toString());
            requester.close();
        });
    });
});

http.listen(3000, function(){
    console.log('listening on *:3000');
});

module.exports = app;