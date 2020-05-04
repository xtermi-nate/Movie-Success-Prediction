const express = require('express');
const router = express.Router();
const Post = require('../models/Post');
const movies = require('../models/movies');
const axios = require("axios").default;

//Get All Movie data
router.get('/', async (req,res) => {
    try{
        const posts = await Post.find();
        res.json(posts);
        
    }catch(err){
        res.json({message:err});
    }


});


//Add Movie data
router.post('/', async (req,res) => {
    const post = new Post({
        actor1: req.body.actor1,
        actor2: req.body.actor2,
        actor3: req.body.actor3,
        director: req.body.director,
        year: req.body.year,
        budget: req.body.budget,
        faceno: req.body.faceno,
        duration: req.body.duration,
        color: req.body.color,
        c_rating: req.body.c_rating,
        genre: req.body.genre,
        language: req.body.language,
        score: req.body.score,
        aspect_ratio: req.body.aspect_ratio
    });

    //Save data in the database
    try{
        const savedPost = await post.save()
        res.json(savedPost);}
        catch(err){
            res.json({message :err});
        }

    
});

//Search Movie data
router.get('/:postTitle', async (req,res) => {
    try{
        const post = await Post.findOne(req.params.postTitle);
        res.json(post);
    }catch(err){
        res.json({message :err});
    }
});




module.exports = router;