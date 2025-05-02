<?php
// db_connection.php

// Database configuration
$servername = "localhost"; // Usually 'localhost' for local development
$username = "root"; // Replace with your actual database username
$password = ""; // Replace with your actual database password
$dbname = "contactease"; // Ensure this database exists

try {
    // Data Source Name (DSN)
    $dsn = "mysql:host=$servername;dbname=$dbname;charset=utf8mb4";
    
    // Create a PDO instance
    $pdo = new PDO($dsn, $username, $password, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION, // Enable exceptions for errors
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC, // Set default fetch mode to associative array
    ]);

} catch (PDOException $e) {
    // Handle connection errors gracefully
    die("Database connection failed: " . $e->getMessage());
}
?>
