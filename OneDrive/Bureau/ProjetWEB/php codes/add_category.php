<?php
// Include your DB connection
require_once 'db_connection.php';

// Check if user is logged in and has a valid user_id
session_start();
$user_id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : null;

if ($_SERVER['REQUEST_METHOD'] == 'POST' && $user_id) {
    // Get category name from the POST data
    $category_name = trim($_POST['category_name']);

    // First, check if the category already exists for this user
    $checkStmt = $pdo->prepare("SELECT COUNT(*) FROM categories WHERE user_id = :user_id AND category_name = :category_name");
    $checkStmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
    $checkStmt->bindParam(':category_name', $category_name, PDO::PARAM_STR);
    $checkStmt->execute();
    
    // If category exists, return an error
    if ($checkStmt->fetchColumn() > 0) {
        echo json_encode(['success' => false, 'error' => 'This category already exists. Please choose a different name.']);
        exit; // Exit here so no further code executes
    }

    // Prepare a statement to insert the new category
    $stmt = $pdo->prepare("INSERT INTO categories (user_id, category_name) VALUES (:user_id, :category_name)");
    $stmt->bindParam(':user_id', $user_id, PDO::PARAM_INT);
    $stmt->bindParam(':category_name', $category_name, PDO::PARAM_STR);

    // Try to insert the category into the database
    try {
        $stmt->execute();
        echo json_encode(['success' => true]);
    } catch (PDOException $e) {
        echo json_encode(['success' => false, 'error' => $e->getMessage()]);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'User not logged in or invalid request.']);
}
?>
