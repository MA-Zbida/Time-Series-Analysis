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

// Debugging: Log the received contact_id to ensure it's being sent properly
error_log("Received contact_id: " . print_r($data, true));

// Ensure data is valid
if (!isset($data['contact_id']) || !is_numeric($data['contact_id'])) {
    die(json_encode(['status' => 'error', 'message' => 'Invalid contact ID.']));
}

$contact_id = $data['contact_id'];

try {
    // Start a transaction to ensure consistency
    $pdo->beginTransaction();

    // Delete from contact_categories table
    $stmt = $pdo->prepare("DELETE FROM contact_categories WHERE contact_id = :contact_id");
    $stmt->execute([':contact_id' => $contact_id]);

    // Delete from contacts table
    $stmt = $pdo->prepare("DELETE FROM contacts WHERE contact_id = :contact_id AND user_id = :user_id");
    $stmt->execute([':contact_id' => $contact_id, ':user_id' => $user_id]);

    // Check if any rows were affected in the contacts table
    if ($stmt->rowCount() > 0) {
        // Commit the transaction
        $pdo->commit();

        echo json_encode(['status' => 'success', 'message' => 'Contact deleted successfully.']);
    } else {
        // Rollback the transaction if no rows were affected
        $pdo->rollBack();

        echo json_encode(['status' => 'error', 'message' => 'Contact not found or not authorized to delete.']);
    }
} catch (PDOException $e) {
    // Rollback the transaction on error
    $pdo->rollBack();
    error_log("Database error: " . $e->getMessage());
    echo json_encode(['status' => 'error', 'message' => 'An error occurred while deleting the contact.']);
}
?>
