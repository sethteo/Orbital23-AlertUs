const express = require('express');
const router = express.Router();
const Schemas = require('../models/schemas');

router.get('/items', async(req, res) => {
    const users = Schemas.Users;
    
    const userItems = await users.find({}, (err, itemData) => {
        if (err) throw err;
        if (itemData) {
            res.end(JSON.stringify(itemdata));
        } else {
            res.end();
        }
    })
});

router.post('/additem', (req, res) => {
    res.end('TBA');
});

module.exports = router;