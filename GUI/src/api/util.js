var express = require('express')
var router = express.Router()
const fs = require('fs');
const { spawn, exec } = require("child_process");

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


router.post('/stream_cmd', function (req, res, next) {
  const cmd = req.body.cmd
  if (!cmd)
    res.status(400).send('invalid paramater: cmd')


  res.writeHead(200, {
    'Content-Type': 'text/plain',
    'Transfer-Encoding': 'chunked'
  })
  

  // set default chunks to 10
  var chunks = req.params.chunks || 10

  // max out chunks at 100
  if (chunks > 100) chunks = 100


  // execute command
  let executing_cmd = spawn('sh', ['-c', cmd]);

  executing_cmd.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
    res.write(data)
  });

  executing_cmd.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
    res.write(data)
  });

  executing_cmd.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    res.write('\n\nExitted with code status: ' + code.toString())
    res.end()
  });

  executing_cmd.on('error', (err) => {
    console.error('Failed to start subprocess.');
    console.error(err)
    res.write('Internal error, malformed command')
  });


  next()
});


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