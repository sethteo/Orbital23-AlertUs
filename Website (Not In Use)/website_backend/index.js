const express = require('express');
const bodyParser = require('body-parser');
const routesHandler = require('./routes/handler.js');
const mongoose = require('mongoose');
require('dotenv/config.js');

const app = express();
app.use(bodyParser.urlencoded({extended:false}));
app.use(bodyParser.json());
app.use('/', routesHandler);

mongoose.connect(process.env.DB_URL, {useUnifiedTopology:true})
.then(()=>{
    console.log('DB Connected');
})
.catch((err)=>{
    console.log(err);
});

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});