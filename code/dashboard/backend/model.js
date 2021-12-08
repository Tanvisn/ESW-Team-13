const { Timestamp, Int32 } = require('bson');
var mongoose = require('mongoose')

// Define schema
var Schema = mongoose.Schema;

var SomeModelSchema = new Schema({
  x: Number,
  y: Number,
  t: Number,
  dir: Number,
  sr: Number
});

// Compile model from schema
module.exports = mongoose.model('SomeModel', SomeModelSchema );
