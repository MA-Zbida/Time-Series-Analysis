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

// Get the JSON input from the request body
$input = file_get_contents('php://input');
$data = json_decode($input, true);

// Debugging: Log the received contacts data
error_log("Received contacts data: " . print_r($data, true));

// Ensure data is valid
if (!isset($data['contacts']) || !is_array($data['contacts'])) {
    die(json_encode(['status' => 'error', 'message' => 'Invalid contact data.']));
}

$contacts = $data['contacts'];
$successCount = 0;
$failedCount = 0;

try {
    // Start a transaction
    $pdo->beginTransaction();

    foreach ($contacts as $contact) {
        $nameParts = explode(' ', $contact['name']);
        $firstName = $nameParts[0];
        $lastName = isset($nameParts[1]) ? $nameParts[1] : '';

        // Generate initials
        $initial = strtoupper(substr($firstName, 0, 1)) . strtoupper(substr($lastName, 0, 1));

        // Insert the category if it does not exist
        $stmt = $pdo->prepare("SELECT category_id FROM categories WHERE user_id = :user_id AND LOWER(category_name) = LOWER(:category_name)");
        $stmt->execute([
            ':user_id' => $user_id,
            ':category_name' => $contact['category']
        ]);
        $category = $stmt->fetch(PDO::FETCH_ASSOC);

        if (!$category) {
            $stmt = $pdo->prepare("INSERT INTO categories (user_id, category_name) VALUES (:user_id, :category_name)");
            $stmt->execute([
                ':user_id' => $user_id,
                ':category_name' => $contact['category']
            ]);
            $category_id = $pdo->lastInsertId();
        } else {
            $category_id = $category['category_id'];
        }

        // Insert the contact
        $stmt = $pdo->prepare("INSERT INTO contacts (user_id, first_name, last_name, phone_number, email, category, initial) 
                                        VALUES (:user_id, :first_name, :last_name, :phone_number, :email, :category, :initial)");
        $stmt->execute([
            ':user_id' => $user_id,
            ':first_name' => $firstName,
            ':last_name' => $lastName,
            ':phone_number' => $contact['phone'],
            ':email' => $contact['email'],
            ':category' => $contact['category'],
            ':initial' => $initial
        ]);

        // Get the inserted contact ID
        $contact_id = $pdo->lastInsertId();

        // Insert into contact_categories
        $stmt = $pdo->prepare("INSERT INTO contact_categories (contact_id, category_id) VALUES (:contact_id, :category_id)");
        $stmt->execute([
            ':contact_id' => $contact_id,
            ':category_id' => $category_id
        ]);

        $successCount++;
    }

    // Commit the transaction
    $pdo->commit();

    // Debugging: Log successful commit
    error_log("Transaction committed successfully.");

    echo json_encode([
        'status' => 'success',
        'message' => "Successfully imported $successCount contacts."
    ]);
} catch (PDOException $e) {
    // If something goes wrong, rollback the transaction
    $pdo->rollBack();
    error_log("Database error: " . $e->getMessage());
    echo json_encode(['status' => 'error', 'message' => 'An error occurred while importing contacts. Please try again later.']);
}
?>
