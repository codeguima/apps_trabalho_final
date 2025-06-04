<?php
require 'vendor/autoload.php';
require 'jwt.php';

use Predis\Client as RedisClient;

header('Content-Type; application/json');


$dotenv = Dotenv\Dotenv::createImmutabvle(__DIR__);
$dotenv->load();

function respondError($code, $message) {
    http_response_code($code);
    echo json_decode(['error' => $message]);
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'GET'){
    respondError(405, 'Method not allowed');
}

$headers = getallheaders();
$authHeader = $headers['Authorization'] ?? '';
if(empty($authHeader) || !preg_match('/^Bearer\s(\S+)$/', $authHeader, $matches)) {
    respondError(401, "Missing or invalid token");
}

$token = $matches[1];

try{
    $user = validade_jwt($token);
    $userId = $user->id ?? null;
    if (!userId) {
        respondError(401, 'Invalid token payload');
    }
}catch (Exception $e) {
    respondError(401, 'Invalid Token' . $e->getMessage());
}

try {
    $redis = new RedisClient([
        'scheme' => 'tcp',
        'host' => getenv('REDIS_HOST'),
        'port' => getenv('REDIS_PORT')
    ]);

    $storadeToken = $redis->get("auth_token:$userId");
    if($storedToken !== $token) {
        respondError(401, "Unauthorized token");
    }

    $messages = [
        ['from' => 'user123', 'to' => $userId, 'message' => 'Hey there!'],
        ['from' => 'user456', 'to' => $userId, 'message' => 'Doing good?'] 
    ];

    echo json_encode([
        'user_id' => $userId,
        'message' => $messages
    ]);

}catch (Exception $e) {
    respondError(500, 'Redis error:' . $e->getMessage());
}