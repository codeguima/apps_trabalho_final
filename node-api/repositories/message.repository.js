class MessageRepository {
  constructor(model) {
    this.model = model;
  }

  async create(data) {
    return await this.model.create(data);
  }

  async getById(id) {
    return await this.model.findByPk(id);
  }

  async getConversation(user1, user2) {
    return await this.model.findAll({
      where: {
        [this.model.sequelize.Op.or]: [
          { sender_id: user1, receiver_id: user2 },
          { sender_id: user2, receiver_id: user1 }
        ]
      },
      order: [['created_at', 'ASC']]
    });
  }
}

module.exports = MessageRepository;