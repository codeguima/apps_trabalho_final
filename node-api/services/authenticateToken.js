// ./services/authenticateToken.js

const jwt = require('jsonwebtoken');

class AuthenticateToken {
    constructor(secretKey) {
        this.secretKey = secretKey;
    }

    generateToken(userId) {
        return jwt.sign({ id: userId }, this.secretKey, { expiresIn: '1h' });
    }

    verifyToken(req, res, next) {
        const token = req.headers['authorization'];

        if (!token) {
            return res.status(401).json({ error: 'Token de autenticação não fornecido' });
        }

        // Remover espaços em branco antes e depois do token usando split
        const trimmedToken = token.split(' ').filter(Boolean)[1];

        jwt.verify(trimmedToken, this.secretKey, (err, decoded) => {
            if (err) {
                return res.status(403).json({ error: 'Token de autenticação inválido' });
            }
            req.userId = decoded.id;
            next();
        });
    }
}

module.exports = AuthenticateToken;
