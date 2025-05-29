<?php
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

function validate_jwt(string $jwt): object
{
    $secret ='secreto123';

    try {
        return JWT::decode($jwt, new Key($secret, 'HS256'));
    } catch (Exception $e) {
        http_response_code(401);
        echo json_encode(['error' => 'Token inválido', 'details' => $e->getMessage()]);
        exit;
    }
}
