const fs = require('fs');

var cache_file = './src/cache.json'

function ReadConfigProp(key) {
  let rawdata = fs.readFileSync(cache_file);
  let cache = JSON.parse(rawdata);
  return cache[key]
}

function SetConfigProp(key, value) {
  let rawdata = fs.readFileSync(cache_file);
  let cache = JSON.parse(rawdata);

  cache[key] = value

  let data = JSON.stringify(cache);
  fs.writeFileSync(cache_file, data);

  return cache[key]
}


function ExecuteCommand(value) {
  let rawdata = fs.readFileSync(cache_file);
  let cache = JSON.parse(rawdata);

  cache[key] = value

  let data = JSON.stringify(cache);
  fs.writeFileSync(cache_file, data);

  return cache[key]
}

module.exports = { ReadConfigProp, SetConfigProp }