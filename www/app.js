var express = require('express');
var app = express();
var path = require("path");
var server = require('http').Server(app);
var io = require('socket.io')(server);
var cookieParser = require('cookie-parser');
var logger = require('morgan');

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
app.use('/', dashboardRouter);

server.listen(3000);

io.on('connection', function (socket) {
    socket.on('empezar_mision', function (data) {
        console.log(data);
    });
});

module.exports = app;