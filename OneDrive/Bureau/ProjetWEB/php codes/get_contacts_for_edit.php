<?php
// Start the session to access logged-in user data
session_start();

// Database connection settings
$host = 'localhost';
$dbname = 'contactease';
$username = 'root';
$password = ''; // Your database password

// Create connection
$conn = new mysqli($host, $username, $password, $dbname);

// Check for connection errors
if ($conn->connect_error) {
    die('Connection failed: ' . $conn->connect_error);
}

// Check if user is logged in and get the user_id from session
if (isset($_SESSION['user_id'])) {
    $userId = $_SESSION['user_id']; // Assuming the user_id is stored in the session

    // Get the contact ID from the request
    if (isset($_GET['id'])) {
        $contactId = $_GET['id']; // The contact ID passed from the client

        // Prepare SQL query to get the contact for the specified user
        $sql = "SELECT * FROM contacts WHERE contact_id = ? AND user_id = ?";
        $stmt = $conn->prepare($sql);
        $stmt->bind_param("ii", $contactId, $userId);
        
        // Execute query
        if ($stmt->execute()) {
            $result = $stmt->get_result();
            
            if ($result->num_rows > 0) {
                $contact = $result->fetch_assoc();
                
                // Logging response for debugging
                error_log("Contact fetched: " . print_r($contact, true));
                
                echo json_encode([
                    'success' => true,
                    'contact' => [
                        'id' => $contact['contact_id'], 
                        'first_name' => $contact['first_name'],
                        'last_name' => $contact['last_name'],
                        'email' => $contact['email'],
                        'phone_number' => $contact['phone_number'],
                        'category' => $contact['category']
                    ]
                ]);
            } else {
                echo json_encode([
                    'success' => false,
                    'error' => 'Contact not found or does not belong to the current user'
                ]);
            }
        } else {
            echo json_encode([
                'success' => false,
                'error' => 'Failed to execute query'
            ]);
        }
    } else {
        echo json_encode([
            'success' => false,
            'error' => 'No contact ID provided'
        ]);
    }
} else {
    echo json_encode([
        'success' => false,
        'error' => 'User not logged in'
    ]);
}

// Close the database connection
$conn->close();
?>
