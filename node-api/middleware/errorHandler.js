
//middleware/errorHandler.js

function errorHandler(err, req, res, next) {
    console.error(err.stack);
    res.status(500).send('Ops, algo deu errado!!');
  }
  
  module.exports = errorHandler;
  