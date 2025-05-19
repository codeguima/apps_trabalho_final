const authService = require('../services/auth.service');

class AuthMiddleware {
  async verifyToken(req, res, next) {
    const token = req.headers.authorization?.split(' ')[1];
    
    if (!token) {
      return res.status(401).json({ error: 'No token provided' });
    }

    try {
      const decoded = authService.verifyToken(token);
      req.user = { userId: decoded.userId };
      next();
    } catch (error) {
      return res.status(401).json({ error: 'Invalid token' });
    }
  }
}

module.exports = new AuthMiddleware();