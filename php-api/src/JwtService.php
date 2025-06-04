<?php

namespace App;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;

class JwtService {
    public static function decodePayload(string $token) {
        return JWT::jsonDecode(JWT::urlsafeB64Decode(explode('.', $token)[1]));
    }
}
