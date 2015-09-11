(function($process) {
    "use strict";

    var express     = require('express'),
        app         = express(),
        server      = require('http').createServer(app);

    // Begin Express so the statistics are available from the `localPort`.
    app.use(express.static(__dirname + '/public'));

    app.get('/server/give_me_time',function(req,res){
      res.send((new Date()).toString());
    });

    app.listen(7000);
    console.log('working on 7000');
})(process);
