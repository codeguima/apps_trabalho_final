const messageService = require('../services/message.service');
const authMiddleware = require('../middlewares/auth.middleware');

class MessageController {
  async sendMessage(req, res) {
    try {
      const { receiverId, content } = req.body;
      const senderId = req.user.userId;
      
      const message = await messageService.sendMessage(senderId, receiverId, content);
      res.status(201).json(message);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }

  async getConversation(req, res) {
    try {
      const { userId } = req.params;
      const currentUserId = req.user.userId;
      
      const messages = await messageService.getConversation(currentUserId, userId);
      res.json(messages);
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  }
}

module.exports = new MessageController();