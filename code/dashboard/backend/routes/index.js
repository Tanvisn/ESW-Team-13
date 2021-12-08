var express = require('express');
var router = express.Router();

var SomeModel = require('../model.js')
var last

/* GET home page. */
router.get('/', function(req, res) {
  	//fetch all student data
    SomeModel.find({}, function(err, users) {
      var userMap = [];
  
      users.forEach(function(user) {
        userMap.push([user['x'], user['y'], user['t']])
      });
      console.log("Sent Data to frontend\n")
      console.log(userMap)
      res.status(200).send(userMap);  
    });
});

router.post('/', function(req, res, next) {

  console.log("hello");
  console.log(req.body['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']);

  om2m_string = (req.body['m2m:sgn']['m2m:nev']['m2m:rep']['m2m:cin']['con']);
  raw_data = om2m_string.split(" ");

  console.log(raw_data[0], raw_data[1], raw_data[2] );
  console.log("Recieved Data from om2m\n");


  const data = new SomeModel({ x: Number(raw_data[0]), y : Number(raw_data[1]), t : Number(raw_data[2])});
  data.save();
  

  res.status(200).send('Done');
});


module.exports = router;
