const express = require('express');
const router = express.Router();
const Post = require('../models/Post');

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
        title: req.body.title,
        director: req.body.director,
        actor: req.body.actor,
        actress: req.body.actress
    });

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