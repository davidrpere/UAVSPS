module.exports = function (io, root_path) {
    var express = require('express');
    var router = express.Router();
    var path = require("path");

    /* GET home page. */
    router.get('*', function(req, res) {
        res.sendFile(path.join(root_path, 'views/dashboard.html'));
    });

    return router
}
