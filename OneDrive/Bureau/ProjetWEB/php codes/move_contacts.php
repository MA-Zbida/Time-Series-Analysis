<?php
// Include your DB connection
require_once 'db_connection.php';

// Check if user is logged in and has a valid user_id
session_start();
$user_id = isset($_SESSION['user_id']) ? $_SESSION['user_id'] : null;

if ($_SERVER['REQUEST_METHOD'] == 'POST' && $user_id) {
    // Get the new category and contact IDs from the POST data
    $category_name = trim($_POST['category_name']);
    $contact_ids = json_decode($_POST['contact_ids'], true);  // Decode the JSON string of contact IDs

    // Check if category name and contact IDs are valid
    if (empty($category_name) || empty($contact_ids)) {
        echo json_encode(['success' => false, 'error' => 'Invalid category or contact IDs.']);
        exit;
    }

    // Prepare the SQL query to update the category for the selected contacts
    try {
        // Build the placeholders for the contact IDs
        $placeholders = implode(',', array_fill(0, count($contact_ids), '?'));
        
        // Prepare the query with positional placeholders
        $stmt = $pdo->prepare("UPDATE contacts SET category = ? WHERE user_id = ? AND contact_id IN ($placeholders)");
        
        // Bind the parameters
        $stmt->bindValue(1, $category_name, PDO::PARAM_STR);  // Bind category_name
        $stmt->bindValue(2, $user_id, PDO::PARAM_INT);  // Bind user_id

        // Bind the contact IDs dynamically
        foreach ($contact_ids as $index => $contact_id) {
            $stmt->bindValue($index + 3, $contact_id, PDO::PARAM_INT);  // Start binding from the 3rd position
        }

        // Execute the query
        $stmt->execute();

        // If the update was successful, return success
        echo json_encode(['success' => true]);
    } catch (PDOException $e) {
        echo json_encode(['success' => false, 'error' => 'Database error: ' . $e->getMessage()]);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'User not logged in or invalid request.']);
}
?>
