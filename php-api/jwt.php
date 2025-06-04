<?php
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

function validade_jwt($token) {
    $secret = getenv('JWT_SECRET');
    return JWT::decode($toeken,new Key($SECRET, 'hs256'));
    
}