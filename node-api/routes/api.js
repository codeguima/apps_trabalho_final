const express = require('express');
const router = express.Router();
const authController = require('../controllers/auth.controller');
const messageController = require('../controllers/messages.controller');
const authMiddleware = require('../middlewares/auth.middleware');

// Rotas públicas
router.post('/register', authController.register);
router.post('/login', authController.login);

// Rotas protegidas
router.use(authMiddleware.verifyToken);
router.post('/messages', messageController.sendMessage);
router.get('/conversation/:userId', messageController.getConversation);

module.exports = router;