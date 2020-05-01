const express = require('express');
const app = express();
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const cors = require('cors');
require('dotenv/config');

app.use(cors());
app.use(bodyParser.json());

const postsRoute = require('./routes/posts');
app.use('/posts',postsRoute);


//Routes
app.get('/',(req,res) => {
    res.send("We are on hell");
});

//DB Connect
mongoose.connect(process.env.MONGODB_URL ,
    { useNewUrlParser: true, useUnifiedTopology: true }, 
    () => console.log('Connected to DB'));

mongoose.connection.on('connected', () => {
    console.log('Mongoose is connected!!!');
});

var spawn = require('child_process').spawn,
    py    = spawn('python', ['recommender.py']),
    nameMovie = ["Sarkar"]
    dataString = '';

py.stdout.on('data', function(nameMovie){
  dataString += nameMovie.toString();
});

py.stdout.on('end', function(){
  console.log('Movie Name = ',dataString);
});
py.stdin.write(JSON.stringify(nameMovie));
py.stdin.end();

//server
app.listen(4000);