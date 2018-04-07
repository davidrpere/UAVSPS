var app = require('express');
var router = app.Router();

/* GET home page. */
router.get('/', function(req, res) {
    res.render('dashboard');
});

module.exports = router;