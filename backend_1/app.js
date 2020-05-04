const express = require('express');
const app = express();
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const request = require('request-promise');
const cors = require('cors');
require('dotenv/config');

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

const postsRoute = require('./routes/posts');
app.use('/posts',postsRoute);

//Routes
app.get('/',(req,res) => {
    res.send("This is SDGP Coursework");
});


//DB Connect
mongoose.connect(process.env.MONGODB_URL ,
    { useNewUrlParser: true, useUnifiedTopology: true }, 
    () => console.log('Connected to DB'));

mongoose.connection.on('connected', () => {
    console.log('Mongoose is connected!!!');
});

app.get('/postdatatoFlask', async function (req, res) {
  var data = { // this variable contains the data you want to send
    actor1 : "Akshay Kumar",
    actor2 : "Amithab Bachan",
    actor3 : "Kamal Haasan",
    director : "Shankar",
    year : 2020,
    budget : 55,
    faceno : 2,
    duration : 127,
    color : "color",
    c_rating : "r",
    genre : "action",
    language : "english",
    score : 8,
    aspect_ratio: 2.3
  }

  var options = {
      method: 'POST',
      uri: 'http://127.0.0.1:5000/',
      body: data,
      json: true // Automatically stringifies the body to JSON
  };
  
  var returndata;
  var sendrequest = await request(options)
  .then(function (parsedBody) {
      console.log(parsedBody); // parsedBody contains the data sent back from the Flask server
      returndata = parsedBody;
      
       // do something with this data, here I'm assigning it to a variable.
  })
  .catch(function (err) {
      console.log(err);
  });
  
  res.send(returndata);
});


//server
app.listen(4000);