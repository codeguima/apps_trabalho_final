const amqp = require('amqplib');
const config = require('../config/config');

class RabbitMQService {
  constructor() {
    this.connection = null;
    this.channel = null;
  }

  async connect() {
    this.connection = await amqp.connect(config.rabbitmq.url);
    this.channel = await this.connection.createChannel();
    await this.channel.assertQueue('messages_queue');
    console.log('Connected to RabbitMQ');
  }

  async publish(event, data) {
    if (!this.channel) await this.connect();
    
    await this.channel.sendToQueue(
      'messages_queue',
      Buffer.from(JSON.stringify({ event, data }))
    );
  }

  async consume(callback) {
    if (!this.channel) await this.connect();
    
    await this.channel.consume('messages_queue', (msg) => {
      if (msg) {
        const content = JSON.parse(msg.content.toString());
        callback(content);
        this.channel.ack(msg);
      }
    });
  }
}

module.exports = new RabbitMQService();