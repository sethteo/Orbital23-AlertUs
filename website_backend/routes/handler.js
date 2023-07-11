const express = require('express');
const router = express.Router();

router.get('/items', (req, res) => {
    const str = [{
        "name": 'me',
        "msg": "my item",
        "username": "sethteo"
    }];
    res.end(JSON.stringify(str));
});

router.post('/additem', (req, res) => {
    res.end('TBA');
});

module.exports = router;