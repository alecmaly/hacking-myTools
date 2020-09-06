'use strict';

// simple express server
var express = require('express');
var bodyParser = require('body-parser')

var app = express();

// parse application/json
app.use(bodyParser.json())

app.use('/styles', express.static('./src/styles'));
app.use('/scripts', express.static('./src/scripts'));
app.use('/public', express.static('./src/public'));
app.use('/assets', express.static('./src/assets'));

var webScan = require('./api/webScan')
var util = require('./api/util')

app.use('/api/util', util)
app.use('/api/webScan', webScan)


app.get('/', function(req, res) {
    res.sendfile('./src/index.html');
});

app.listen(5000);