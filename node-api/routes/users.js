//./routes/users.js

const express = require('express');
const router = express.Router();
const db = require('../models'); // Importa o modelo de usuário

const AuthenticateToken = require('../services/authenticateToken');
const secretKey = 'SUA_CHAVE_SECRETA'; // Chave secreta do token JWT
const authenticateToken = new AuthenticateToken(secretKey);

const UserController = require('../controllers/userController');
const UserService = require('../services/userService');
const userService = new UserService(db.User, authenticateToken);
const userController = new UserController(userService);

//--------------------------------------------------------------------------------------------------//
router.get('/', authenticateToken.verifyToken.bind(authenticateToken),(req, res, next) => {
  res.send('Módulo de usuários está rodando');
});

router.post('/new', (req, res, next) => {
  userController.create(req, res).catch(next);
});

router.post('/login', (req, res, next) => {
  userController.login(req, res).catch(next);
});

// Rota de atualização
router.put('/update/:id', authenticateToken.verifyToken.bind(authenticateToken),(req, res, next) => {
  userController.update(req, res).catch(next);
});

router.get('/findall', authenticateToken.verifyToken.bind(authenticateToken), (req, res, next) => {
  userController.findAll(req, res).catch(next);
})

router.get('/findbyId/:id', authenticateToken.verifyToken.bind(authenticateToken), (req, res, next) => {
  userController.findbyId(req, res).catch(next);
});

router.delete('/delete/:id', authenticateToken.verifyToken.bind(authenticateToken), (req, res, next) => {
  userController.delete(req, res).catch(next);
});

//--------------------------------------------------------------------------------------------------//

module.exports = router;
