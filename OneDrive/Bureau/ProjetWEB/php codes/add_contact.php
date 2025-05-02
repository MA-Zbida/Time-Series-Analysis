<?php
// Start session
session_start();
require 'db_connection.php';  // Include the database connection

// Ensure the user is logged in
if (!isset($_SESSION['user_id']) && !isset($_COOKIE['auth_token'])) {
    die(json_encode(['status' => 'error', 'message' => 'Unauthorized access. Please log in.']));
}

$user_id = $_SESSION['user_id'] ?? null;
$token = $_COOKIE['auth_token'] ?? null;

// Validate token if necessary
if (!$user_id && $token) {
    $stmt = $pdo->prepare("SELECT user_id FROM remember_tokens WHERE token = :token");
    $stmt->execute([':token' => $token]);
    $tokenData = $stmt->fetch(PDO::FETCH_ASSOC);
    if ($tokenData) {
        $user_id = $tokenData['user_id'];
        $_SESSION['user_id'] = $user_id;
    }
}

// If no valid user_id is found, access is denied
if (!$user_id) {
    die(json_encode(['status' => 'error', 'message' => 'Unauthorized access. Please log in.']));
}

// Get contact data from the request
$fullName = $_POST['fullName'];
$email = $_POST['email'];
$phone = $_POST['phone'];
$categoryName = $_POST['category'];

try {
    // Start transaction
    $pdo->beginTransaction();

    // Insert the new contact into the database
    $stmt = $pdo->prepare("INSERT INTO contacts (user_id, first_name, last_name, phone_number, email, category, initial) 
                                VALUES (:user_id, :first_name, :last_name, :phone_number, :email, :category, :initial)");
    $nameParts = explode(' ', $fullName);
    $firstName = $nameParts[0];
    $lastName = isset($nameParts[1]) ? $nameParts[1] : '';

    // Generate initial from the first name and last name
    $initial = strtoupper(substr($firstName, 0, 1)) . strtoupper(substr($lastName, 0, 1));

    $stmt->execute([
        ':user_id' => $user_id,
        ':first_name' => $firstName,
        ':last_name' => $lastName,
        ':phone_number' => $phone,
        ':email' => $email,
        ':category' => $categoryName,
        ':initial' => $initial
    ]);

    // Get the ID of the inserted contact
    $contact_id = $pdo->lastInsertId();

    // Check if the category exists in `categories`
    $stmt = $pdo->prepare("SELECT category_id FROM categories WHERE user_id = :user_id AND category_name = :category_name");
    $stmt->execute([':user_id' => $user_id, ':category_name' => $categoryName]);
    $category = $stmt->fetch(PDO::FETCH_ASSOC);

    if (!$category) {
        // Insert the category if it doesn't exist
        $stmt = $pdo->prepare("INSERT INTO categories (user_id, category_name) VALUES (:user_id, :category_name)");
        $stmt->execute([':user_id' => $user_id, ':category_name' => $categoryName]);
        $category_id = $pdo->lastInsertId();
    } else {
        $category_id = $category['category_id'];
    }

    // Link the contact with the category in `contact_categories`
    $stmt = $pdo->prepare("INSERT INTO contact_categories (contact_id, category_id) VALUES (:contact_id, :category_id)");
    $stmt->execute([':contact_id' => $contact_id, ':category_id' => $category_id]);

    // Commit transaction
    $pdo->commit();

    // Return success with the contact ID
    echo json_encode(['status' => 'success', 'contact_id' => $contact_id]);
} catch (PDOException $e) {
    // Rollback transaction on error
    $pdo->rollBack();
    error_log("Database error: " . $e->getMessage());
    echo json_encode(['status' => 'error', 'message' => 'Error adding contact. Please try again later.']);
}
?>
