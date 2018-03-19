var http = require("http");
var url = require('url');
var fs = require('fs');
var count = 0;

var server = http.createServer(function(request, response){
  var path = url.parse(request.url).pathname;

  switch(path){
    case '/':
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write('<h1>Hey, have you heard about our <a href="/signup.html">signup page</a></h1>');
    response.end();
    break;

    default:
    response.writeHead(404);
    response.write("opps this doesn't exist - 404");
    response.end();
    break;
  }
});
server.listen(8000);

// define interactions with client
var io = require('socket.io').listen(server);
io.sockets.on('connection', function(socket){
    //send data to client
    setInterval(function(){
        count = count + 1;
        if (count == 5) {
          socket.emit('stream', {'title': "Valor contador: " + count , 'seen' : false});
        }else{
          socket.emit('stream', {'title': "Valor contador: " + count , 'seen' : true});
        }
    }, 1000);

});
