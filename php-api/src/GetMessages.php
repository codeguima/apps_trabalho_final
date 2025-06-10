<?php

namespace App;

use Predis\Client as RedisClient;
use Exception;

class GetMessages
{
    private static ?RedisClient $redis = null;

    private static function getRedisClient(): RedisClient
    {
        if (self::$redis === null) {
            $redisHost = $_ENV['REDIS_HOST'] ?? '127.0.0.1';
            $redisPort = $_ENV['REDIS_PORT'] ?? 6379;
            $redisPassword = $_ENV['REDIS_PASSWORD'] ?? null;

            $connectionParams = [
                'scheme' => 'tcp',
                'host'   => $redisHost,
                'port'   => $redisPort,
            ];

            if (!empty($redisPassword)) {
                $connectionParams['password'] = $redisPassword;
            }

            self::$redis = new RedisClient($connectionParams);
        }

        return self::$redis;
    }

    public function handle()
    {
        header('Content-Type: application/json');

        $respondError = function ($code, $message) {
            http_response_code($code);
            echo json_encode(['error' => $message]);
            exit;
        };

        // Validar token via endpoint /me
        $headers = getallheaders();
        $authHeader = $headers['Authorization'] ?? '';
        if (empty($authHeader) || !preg_match('/^Bearer\s(\S+)$/', $authHeader, $matches)) {
            $respondError(401, "Missing or invalid token");
        }

        $token = $matches[0]; // "Bearer <token>"
        $apiUrl = $_ENV['API_NODE_URL'] ?? null;
        if (!$apiUrl) {
            $respondError(500, "API_NODE_URL não configurada");
        }

        try {
            $ch = curl_init();
            curl_setopt_array($ch, [
                CURLOPT_URL => rtrim($apiUrl, '/') . '/me',
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_HTTPHEADER => [
                    "Authorization: $token",
                    "Accept: application/json"
                ],
                CURLOPT_TIMEOUT => 5,
            ]);

            $response = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

            if (curl_errno($ch)) {
                throw new Exception(curl_error($ch));
            }

            curl_close($ch);

            if ($httpCode !== 200) {
                $respondError(401, "Token inválido ou expirado");
            }

            $userData = json_decode($response, true);
            $userId = $userData['id'] ?? null;

            if (!$userId) {
                $respondError(401, "Usuário inválido");
            }

            $redisClient = self::getRedisClient();
            $allKeys = $redisClient->keys("messages:from:*:to:*");

            $userMessages = [];

            foreach ($allKeys as $key) {
                if (preg_match('/^messages:from:(.*):to:(.*)$/', $key, $parts)) {
                    $from = $parts[1];
                    $to = $parts[2];

                    if ((string)$from === (string)$userId || (string)$to === (string)$userId) {
                        $messages = $redisClient->lrange($key, 0, -1);
                        foreach ($messages as $msg) {
                            $userMessages[] = [
                                'from' => $from,
                                'to' => $to,
                                'message' => $msg,
                            ];
                        }
                    }
                }
            }

            echo json_encode([
                'user_id' => $userId,
                'messages' => $userMessages,
            ]);
        } catch (Exception $e) {
            $respondError(500, 'Erro: ' . $e->getMessage());
        }
    }
}
