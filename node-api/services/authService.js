const jwt = require('jsonwebtoken');
const config = require('../config/config');
const UserRepository = require('../repositories/user.repository');
const userModel = require('../models/user.model');

const userRepository = new UserRepository(userModel);

class AuthService {
  async register(userData) {
    const user = await userRepository.create(userData);
    return this.generateToken(user.id);
  }

  async login(email, password) {
    const user = await userRepository.findByEmail(email);
    if (!user || user.password !== password) {
      throw new Error('Invalid credentials');
    }
    return this.generateToken(user.id);
  }

  generateToken(userId) {
    return jwt.sign({ userId }, config.jwt.secret, {
      expiresIn: config.jwt.expiresIn
    });
  }

  verifyToken(token) {
    return jwt.verify(token, config.jwt.secret);
  }
}

module.exports = new AuthService();