var express = require('express');
var app = express();
var zmq = require('zeromq');
var http = require('http');
var server = http.createServer(app);
var io  = require('socket.io').listen(server)
var path = require("path");

var dashboard = require('./routes/dashboard')(io,__dirname);

app.set('views', path.join(__dirname, 'views'));
app.use('/', dashboard);
app.use('/dashboard', dashboard);

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

module.exports = app;
