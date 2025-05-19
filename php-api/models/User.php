<?php
require_once __DIR__.'/../config/database.php';

class User {
    private $conn;
    public $id;
    public $name;
    public $email;
    public $password;
    public $created_at;

    public function __construct() {
        $dbConfig = include(__DIR__.'/../config/database.php')['mysql'];
        $this->conn = new PDO(
            "mysql:host={$dbConfig['host']};dbname={$dbConfig['database']}",
            $dbConfig['username'],
            $dbConfig['password']
        );
    }

    public static function findByEmail($email) {
        $instance = new self();
        $stmt = $instance->conn->prepare("SELECT * FROM users WHERE email = :email");
        $stmt->bindParam(':email', $email);
        $stmt->execute();
        return $stmt->fetchObject(__CLASS__);
    }

    public function save() {
        $stmt = $this->conn->prepare("
            INSERT INTO users (name, email, password) 
            VALUES (:name, :email, :password)
        ");
        $stmt->bindParam(':name', $this->name);
        $stmt->bindParam(':email', $this->email);
        $stmt->bindParam(':password', $this->password);
        return $stmt->execute();
    }
}