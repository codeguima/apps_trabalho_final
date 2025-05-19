<?php
require_once __DIR__.'/../controllers/AuthController.php';

$authController = new AuthController();

$requestUri = parse_url($_SERVER['REQUEST_URI'], PHP_URL_PATH);
$requestMethod = $_SERVER['REQUEST_METHOD'];

header('Content-Type: application/json');

switch ($requestUri) {
    case '/api/register':
        if ($requestMethod === 'POST') {
            $data = json_decode(file_get_contents('php://input'), true);
            echo json_encode($authController->register($data));
        } else {
            http_response_code(405);
            echo json_encode(['error' => 'Method Not Allowed']);
        }
        break;
        
    case '/api/login':
        if ($requestMethod === 'POST') {
            $data = json_decode(file_get_contents('php://input'), true);
            echo json_encode($authController->login($data));
        } else {
            http_response_code(405);
            echo json_encode(['error' => 'Method Not Allowed']);
        }
        break;
        
    default:
        http_response_code(404);
        echo json_encode(['error' => 'Not Found']);
        break;
}