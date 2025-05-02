<?php
session_start(); // Start the session to access the logged-in user's data

// Database connection parameters
$host = "localhost";
$user = "root";
$password = "";
$database = "contactease";

// Connect to the database
$conn = new mysqli($host, $user, $password, $database);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Ensure the user is logged in and has a valid user_id in the session
if (!isset($_SESSION['user_id']) || intval($_SESSION['user_id']) <= 0) {
    die(json_encode(["error" => "User not logged in or invalid user_id"]));
}

$user_id = intval($_SESSION['user_id']); // Get the logged-in user's ID

// SQL query to fetch distinct category names for the logged-in user
$sql = "SELECT DISTINCT CONCAT(UPPER(LEFT(category_name, 1)), LOWER(SUBSTRING(category_name, 2))) AS category_name
        FROM categories
        WHERE user_id = ?";

// Prepare the SQL statement
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $user_id); // Bind user_id as an integer
$stmt->execute();

$result = $stmt->get_result();

// Prepare an array to store the categories
$categories = [];

if ($result->num_rows > 0) {
    // Fetch rows and add to the array
    while ($row = $result->fetch_assoc()) {
        $categories[] = $row['category_name'];
    }
} else {
    // No categories found for the user
    echo json_encode(['success' => false, 'error' => 'No categories found.']);
    exit;
}

// Close the database connection
$stmt->close();
$conn->close();

// Return the categories as a JSON response
header('Content-Type: application/json');
echo json_encode(['success' => true, 'categories' => $categories]);
?>
