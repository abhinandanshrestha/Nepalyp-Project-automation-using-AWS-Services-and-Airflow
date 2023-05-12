const express = require('express');
const router=express.Router();

// Create a PostgreSQl connection pool
const client= require('./dbconnection');

//define the data route
router.get('/',(req,res)=>{
    client.query('Select * from companytable')
    .then((result)=>{
        res.json(result.rows);
    })
    .catch((err)=>{
        console.log(err);
        res.status(500).send('Error executing query');
    })
});

module.exports=router;


