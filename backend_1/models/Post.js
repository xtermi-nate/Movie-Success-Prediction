const mongoose = require('mongoose');

const PostSchema = mongoose.Schema({
    actor1: String,
    actor2: String,
    actor3: String,
    director: String,
    year: Number,
    budget: Number,
    faceno: Number,
    duration: Number,
    color: String,
    c_rating: String,
    genre: String,
    language: String,
    score: Number,
    aspect_ratio: Number

});

module.exports = mongoose.model('Posts' , PostSchema);