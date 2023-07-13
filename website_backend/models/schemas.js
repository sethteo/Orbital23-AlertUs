const { Int32 } = require('bson');
const mongoose = require('mongoose');
const Schema = mongoose.Schema;

const userSchema = new Schema({
    tele_id: {type:Int32, required:true},
    name: {type:String, required:true},
    items: {type:Array},
    slots: {type:Int32},
})

const itemSchema = new Schema({
    item_url: {type: String},
    item_name: {type: String},
    price: {type:Array}
})

const Users = mongoose.model('users', userSchema, 'users');
const Items = mongoose.model('items', itemSchema, 'items');
const mySchemas = {'Users':Users, 'Items':Items};

module.exports = mySchemas;