<?php

namespace App;

use App\JwtService;
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
            $redisPassword = $_ENV['REDIS_PASSWORD'] ?? null; // Permite senha opcional

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

        // Função de erro
        $respondError = function ($code, $message) {
            http_response_code($code);
            echo json_encode(['error' => $message]);
            exit;
        };

        // Validar token JWT
        $headers = getallheaders();
        $authHeader = $headers['Authorization'] ?? '';
        if (empty($authHeader) || !preg_match('/^Bearer\s(\S+)$/', $authHeader, $matches)) {
            $respondError(401, "Missing or invalid token");
        }

        $token = $matches[1];

        try {
            $redisClient = self::getRedisClient();
            $redisKey = "user:token:" . $token;

            if (!$redisClient->exists($redisKey)) {
                $respondError(401, "Token expirado ou inválido");
            }

            $userId = $redisClient->get($redisKey);

            // Buscar todas as chaves que o usuário está envolvido
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
            $respondError(500, 'Redis error: ' . $e->getMessage());
        }
    }
}
