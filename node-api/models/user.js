// ./models/user.js
const Sequelize = require('sequelize');

module.exports= (sequelize) => {
    const User = sequelize.define('User',{
        id:{
            type: Sequelize.INTEGER,
            primaryKey:true,
            autoIncrement: true
        },
        name:{
            type: Sequelize.STRING,
            allowNull:false
        },
        lastname:{
            type: Sequelize.STRING,
            allowNull:false
        },
        email:{
            type: Sequelize.STRING,
            unique:true
        },
        password:{
            type:Sequelize.STRING,
            allowNull:false
        },
        status: {
            type: Sequelize.BOOLEAN,
            allowNull: false
        },
    }, {
        indexes: [
          {
            fields: ['status']
          }
        ]
      });

    return User;
};