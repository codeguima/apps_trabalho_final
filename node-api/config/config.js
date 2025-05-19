module.exports = {
  jwt: {
    secret: process.env.JWT_SECRET || 'sua_chave_secreta',
    expiresIn: '1h'
  },
  mysql: {
    host: process.env.MYSQL_HOST || 'localhost',
    user: process.env.MYSQL_USER || 'root',
    password: process.env.MYSQL_PASSWORD || 'password',
    database: process.env.MYSQL_DB || 'message_system'
  },
  rabbitmq: {
    url: process.env.RABBITMQ_URL || 'amqp://localhost'
  }
};