const mongoose = require('mongoose');

const PostSchema = mongoose.Schema({
    title: String,
    director: String,
    actor: String,
    actress: String
});

module.exports = mongoose.model('Posts' , PostSchema);