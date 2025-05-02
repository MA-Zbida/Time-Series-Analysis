<?php
// Example of database connection (replace with your actual DB connection)
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "contactease";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Log incoming POST data for debugging
error_log(print_r($_POST, true));

// Check if all required data is set
if (isset($_POST['contact_id'], $_POST['first_name'], $_POST['last_name'], $_POST['email'], $_POST['phone_number'], $_POST['category'], $_POST['user_id'])) {
    $contactId = $_POST['contact_id']; // Updated from 'editContactId' to 'contact_id'
    $firstName = $_POST['first_name'];
    $lastName = $_POST['last_name'];
    $email = $_POST['email'];
    $phoneNumber = $_POST['phone_number'];
    $category = $_POST['category'];
    $userId = $_POST['user_id']; // User ID to ensure that only the correct user can update their contacts

    // Prepare the update SQL query
    $sql = "UPDATE contacts 
            SET first_name = ?, last_name = ?, email = ?, phone_number = ?, category = ? 
            WHERE contact_id = ? AND user_id = ?";

    // Prepare statement
    if ($stmt = $conn->prepare($sql)) {
        // Bind parameters
        $stmt->bind_param('ssssssi', $firstName, $lastName, $email, $phoneNumber, $category, $contactId, $userId);

        // Execute the query
        if ($stmt->execute()) {
            echo json_encode(['success' => true]);
        } else {
            echo json_encode(['success' => false, 'error' => 'Failed to update contact.']);
        }

        // Close the statement
        $stmt->close();
    } else {
        echo json_encode(['success' => false, 'error' => 'Invalid query.']);
    }
} else {
    echo json_encode(['success' => false, 'error' => 'Missing required data.']);
}

// Close the connection
$conn->close();
?>