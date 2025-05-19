<?php
require_once __DIR__.'/../config/jwt.php';

class Token {
    private static $secret;
    
    public static function init() {
        $config = include(__DIR__.'/../config/jwt.php');
        self::$secret = $config['secret'];
    }

    public static function generate($userId) {
        $header = json_encode(['typ' => 'JWT', 'alg' => 'HS256']);
        $payload = json_encode([
            'user_id' => $userId,
            'iat' => time(),
            'exp' => time() + 3600
        ]);
        
        $base64Header = base64_encode($header);
        $base64Payload = base64_encode($payload);
        
        $signature = hash_hmac('sha256', "$base64Header.$base64Payload", self::$secret, true);
        $base64Signature = base64_encode($signature);
        
        return "$base64Header.$base64Payload.$base64Signature";
    }

    public static function validate($token) {
        $parts = explode('.', $token);
        if (count($parts) !== 3) return false;
        
        list($base64Header, $base64Payload, $base64Signature) = $parts;
        
        $signature = base64_decode($base64Signature);
        $expectedSignature = hash_hmac('sha256', "$base64Header.$base64Payload", self::$secret, true);
        
        if (!hash_equals($signature, $expectedSignature)) return false;
        
        $payload = json_decode(base64_decode($base64Payload));
        
        if ($payload->exp < time()) return false;
        
        return $payload;
    }
}

Token::init();