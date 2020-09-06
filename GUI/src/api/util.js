var express = require('express')
var router = express.Router()
const fs = require('fs');
const { exec } = require("child_process");

var util = require('./_helperFunctions')


// working directory
router.get('/working_dir', function (req, res) {
  var dir = util.ReadConfigProp('working_dir')
  res.send(dir)
})

// working directory
router.post('/working_dir', function (req, res) {
  var path = req.body.path
  
  if (path == null)
    res.send('missing parameter: Path') 

  try {
    util.SetConfigProp('working_dir', path)
    res.send('Directory set to: ' + path)
  } catch {
    res.send('failed')
  }
})


// cmd
router.post('/execute_cmd', function (req, res, next) {
  const cmd = req.body.cmd
  if (!cmd) {
    res.send('Missing parameter: cmd')
  }

  exec(cmd, (error, stdout, stderr) => {
    if (error) {
      res.status(400).send(error.message);
      return;
    }
    if (stderr) {
      res.status(400).send(stderr);
      return;
    }
    res.send(stdout)
  });

})


router.get('/stream', function (req, res, next) {

  res.writeHead(200, {
    'Content-Type': 'text/plain',
    'Transfer-Encoding': 'chunked'
  })

  // set default chunks to 10
  var chunks = req.params.chunks || 10

  // max out chunks at 100
  if (chunks > 100) chunks = 100

  var count = 1

  while (count <= chunks) {
    res.write(JSON.stringify({
      type: "stream",
      chunk: count++
    })+'\n')
  };

  res.end()
  next()
});




module.exports = router