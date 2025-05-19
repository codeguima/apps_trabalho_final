const MessageRepository = require('../repositories/message.repository');
const messageModel = require('../models/message.model');
const rabbitmqService = require('./rabbitmq.service');

const messageRepository = new MessageRepository(messageModel);

class MessageService {
  async sendMessage(senderId, receiverId, content) {
    const message = await messageRepository.create({
      sender_id: senderId,
      receiver_id: receiverId,
      content
    });

    await rabbitmqService.publish('new_message', {
      messageId: message.id,
      receiverId
    });

    return message;
  }

  async getConversation(user1, user2) {
    return await messageRepository.getConversation(user1, user2);
  }
}

module.exports = new MessageService();