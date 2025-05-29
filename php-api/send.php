<?php
require 'vendor/autoload.php';
require 'jwt.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

header('Content-Type: application/json');

// Função para resposta de erro e saída
function respondError($code, $message) {
    http_response_code($code);
    echo json_encode(['error' => $message]);
    exit;
}

// Obter e validar o header Authorization
$headers = getallheaders();
$authHeader = $headers['Authorization'] ?? '';

if (!$authHeader || !str_starts_with($authHeader, 'Bearer ')) {
    respondError(401, 'Token não fornecido ou formato inválido');
}

$token = trim(str_replace('Bearer ', '', $authHeader));

// Validar JWT
$user = validate_jwt($token);

// Obter e validar o corpo da requisição
$body = json_decode(file_get_contents('php://input'), true);
if (!is_array($body)) {
    respondError(400, 'Corpo da requisição inválido');
}

if (empty($body['message']) || empty($body['user_id_received'])) {
    respondError(400, 'Campos obrigatórios: message, user_id_received');
}

// Conectar ao RabbitMQ
try {
    $connection = new AMQPStreamConnection('rabbitmq', 5672, 'guest', 'guest');
    $channel = $connection->channel();
    $channel->queue_declare('messages', false, true, false, false);

    // Criar e publicar a mensagem
    $msg = new AMQPMessage(json_encode([
        'message' => $body['message'],
        'user_id_send' => $user->id,
        'user_id_received' => $body['user_id_received']
    ]));

    $channel->basic_publish($msg, '', 'messages');

    // Fechar conexão
    $channel->close();
    $connection->close();

    // Resposta de sucesso
    echo json_encode(['status' => 'Mensagem enviada']);
} catch (Exception $e) {
    respondError(500, 'Erro ao enviar mensagem: ' . $e->getMessage());
}
