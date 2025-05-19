const express = require('express');
const bodyParser = require('body-parser');
const sequelize = require('./config/database');
const apiRoutes = require('./routes/api');

const app = express();

// Middlewares
app.use(bodyParser.json());

// Rotas
app.use('/api', apiRoutes);

// Sincronizar banco de dados e iniciar servidor
sequelize.sync()
  .then(() => {
    app.listen(3000, () => {
      console.log('Server running on port 3000');
    });
  })
  .catch(err => {
    console.error('Database sync error:', err);
  });

module.exports = app;