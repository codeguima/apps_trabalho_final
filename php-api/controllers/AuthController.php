<?php
require_once __DIR__.'/../models/User.php';
require_once __DIR__.'/../models/Token.php';

class AuthController {
    private $redis;
    
    public function __construct() {
        $this->redis = new Redis();
        $this->redis->connect('127.0.0.1', 6379);
    }
    
    public function register($request) {
        $user = new User();
        $user->name = $request['name'];
        $user->email = $request['email'];
        $user->password = password_hash($request['password'], PASSWORD_BCRYPT);
        
        if ($user->save()) {
            return ['status' => 'success', 'message' => 'User registered'];
        }
        
        return ['status' => 'error', 'message' => 'Registration failed'];
    }
    
    public function login($request) {
        $user = User::findByEmail($request['email']);
        
        if ($user && password_verify($request['password'], $user->password)) {
            $token = Token::generate($user->id);
            $this->redis->set("user_token:$user->id", $token, 3600);
            
            return [
                'status' => 'success',
                'token' => $token,
                'user' => [
                    'id' => $user->id,
                    'name' => $user->name,
                    'email' => $user->email
                ]
            ];
        }
        
        return ['status' => 'error', 'message' => 'Invalid credentials'];
    }
    
    public function validateToken($token) {
        $decoded = Token::validate($token);
        if (!$decoded) return false;
        
        $storedToken = $this->redis->get("user_token:{$decoded->user_id}");
        return $storedToken === $token;
    }
}