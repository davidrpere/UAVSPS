var express = require('express');
var app = express();
var router = express.Router();

app.use('/', router);

router.get('/', function(req, res){
  res.sendFile(__dirname + '/dashboard.html');
});

router.get('/dashboard.html', function(req, res){
  res.sendFile(__dirname + '/dashboard.html');
});

router.get('/map.html', function(req, res){
  res.sendFile(__dirname + '/map.html');
});

app.use('*', function(req, res){
  res.send('Error 404: Not Found!');
});

app.listen(3000, function(){
  console.log("Server running at Port 3000");
});
