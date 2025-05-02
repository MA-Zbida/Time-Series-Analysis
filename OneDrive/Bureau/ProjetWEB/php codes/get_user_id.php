<?php
session_start();
require 'db_connection.php';

header('Content-Type: application/json');

// Check if the user is logged in and return user_id
if (isset($_SESSION['user_id'])) {
    echo json_encode(['user_id' => $_SESSION['user_id']]);
} else {
    echo json_encode(['error' => 'User not logged in']);
}
