//app.js

const express = require('express');
const dotenv = require('dotenv');

dotenv.config();

const indexRouter = require('./routes/index');
const usersRouter = require('./routes/users');

const { applyMigrations } = require('./config/database');
const errorHandler = require('./middleware/errorHandler');

const app = express();


app.use(express.json());


app.use('/', indexRouter);
app.use('/users', usersRouter);



// Middleware de tratamento de erros
app.use(errorHandler);

// Sincronização com o banco de dados
applyMigrations();

const port = process.env.PORT || 3000;
app.listen(port, () => {
  console.log(`Servidor rodando na porta ${port}`);
});

module.exports = app;
