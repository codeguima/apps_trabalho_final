<?php

require_once dirname(__DIR__) . '/vendor/autoload.php';

use Dotenv\Dotenv;
use App\GetMessages;

$dotenv = Dotenv::createImmutable(dirname(__DIR__));
$dotenv->load();

$scriptName = $_SERVER['SCRIPT_NAME'];
$requestUri = $_SERVER['REQUEST_URI'];

if ($requestUri === '/get-messages') {
  $getMessages = new GetMessages();
  $getMessages->handle();
  exit;
}

http_response_code(404);
echo json_encode(['error' => 'Route not found']);
