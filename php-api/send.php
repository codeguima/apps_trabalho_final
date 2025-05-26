<?php
require 'vendor/autoload.php';
require 'jwt.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

header('Content-Type: application/json');

// Autenticação JWT
$authHeader = $_SERVER['HTTP_AUTHORIZATION'] ?? '';
if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
    http_response_code(401);
    echo json_encode(['error' => 'Token não fornecido']);
    exit;
}
$jwt = str_replace('Bearer ', '', $authHeader);
$user = validate_jwt($jwt);

$body = json_decode(file_get_contents('php://input'), true);

if (!isset($body['message']) || !isset($body['user_id_received'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Campos obrigatórios: message, user_id_received']);
    exit;
}

$connection = new AMQPStreamConnection(
    'rabbitmq',
    5672,
    'guest',
    'guest'
);
$channel = $connection->channel();
$channel->queue_declare('messages', false, false, false, false);

$msg = new AMQPMessage(json_encode([
    'message' => $body['message'],
    'user_id_send' => $user->id,
    'user_id_received' => $body['user_id_received']
]));
$channel->basic_publish($msg, '', 'messages');

echo json_encode(['status' => 'Mensagem enviada']);
