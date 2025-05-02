<?php
// Start the session
session_start();
require 'db_connection.php';  // Include the database connection

// Check if the user is logged in using the session or cookie
if (!isset($_SESSION['user_id']) && !isset($_COOKIE['auth_token'])) {
    die(json_encode(['status' => 'error', 'message' => 'Unauthorized access. Please log in.']));
}

$user_id = $_SESSION['user_id'] ?? null;  // Get the user_id from the session if available
$token = $_COOKIE['auth_token'] ?? null;  // Get the auth_token from the cookie if available

// Validate token if the user is not already logged in via session
if (!$user_id && $token) {
    $stmt = $pdo->prepare("SELECT user_id FROM remember_tokens WHERE token = :token");
    $stmt->execute([':token' => $token]);
    $tokenData = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($tokenData) {
        $user_id = $tokenData['user_id'];
        $_SESSION['user_id'] = $user_id;  // Store user_id in the session
    }
}

// If no valid user_id is found, access is denied
if (!$user_id) {
    die(json_encode(['status' => 'error', 'message' => 'Unauthorized access. Please log in.']));
}

// Fetch contacts from the database
try {
    $stmt = $pdo->prepare("SELECT contact_id, first_name, last_name, phone_number, email, category FROM contacts WHERE user_id = :user_id");
    $stmt->execute([':user_id' => $user_id]);
    $contacts = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Prepare the response in the format the frontend expects
    $response = array_map(function($contact) {
        return [
            'id' => $contact['contact_id'],
            'name' => $contact['first_name'] . ' ' . $contact['last_name'],
            'category' => $contact['category'],
            'initial' => strtoupper(substr($contact['first_name'], 0, 1) . substr($contact['last_name'], 0, 1)),
            'email' => $contact['email'],
            'phone' => $contact['phone_number']
        ];
    }, $contacts);

    // Return the contacts as a JSON response
    echo json_encode(['status' => 'success', 'contacts' => $response]);

} catch (PDOException $e) {
    error_log("Database error: " . $e->getMessage());
    echo json_encode(['status' => 'error', 'message' => 'A database error occurred. Please try again later.']);
}
?>
