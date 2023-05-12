const express = require('express');
const port=2345;
const app = express();

const cors=require('cors');

// allow requests from all origin
app.use(cors({
    origin:'*',
        credentials:true
}));

// Default route
app.get('/',(req,res)=>res.json({'status':'OK','message':'Please use /alldata to get all the data'}));

// Handle /alldata routes
const alldata=require('./controller/alldata');
app.use('/alldata',alldata);

app.listen(port,()=> console.log(`Serving on port ${port}`));