<?php
// Enable error reporting for debugging
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

// Database connection
$conn = new mysqli('localhost', 'root', '', 'contactease');

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Query to fetch categories
$sql = "SELECT DISTINCT CONCAT(UPPER(LEFT(category_name, 1)), LOWER(SUBSTRING(category_name, 2))) AS category_name FROM categories";
$result = $conn->query($sql);

if ($result->num_rows > 0) {
    $categories = [];
    while ($row = $result->fetch_assoc()) {
        $categories[] = $row['category_name'];
    }
    echo json_encode(['success' => true, 'categories' => $categories]);
} else {
    echo json_encode(['success' => false, 'error' => 'No categories found.']);
}

// Close connection
$conn->close();
?>
