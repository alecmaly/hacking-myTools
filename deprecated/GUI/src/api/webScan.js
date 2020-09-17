var express = require('express')
var router = express.Router()

const { exec } = require("child_process");

var util = require('./_helperFunctions')


// define the home page route
router.get('/', function (req, res) {
  res.send('Please specify a POST command. { url: "", cookies: ""}')
})

router.post('/extract_comments', function (req, res) {
    const url = req.body.url
    const cookies = req.body.cookies || ''

    if (url == null)
        res.send('need url')

    const working_dir = util.ReadConfigProp('working_dir')
    
    exec(`mkdir ${working_dir}/scans`)
    exec(`mkdir ${working_dir}/scans/scraped_comments`)
    exec(`python3 /opt/myTools/tools/extract_comments.py -u "${url}" -c "${cookies}" > ${working_dir}/scans/scraped_comments/tmp &`, (error, stdout, stderr) => {
        if (error) {
            console.log(`error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.log(`stderr: ${stderr}`);
            return;
        }
        console.log(`stdout: ${stdout}`);
    });

    res.send('success')
})

module.exports = router