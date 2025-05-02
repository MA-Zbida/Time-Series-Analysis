<?php
// Start session
session_start();

// Require database connection
require 'db_connection.php';

// Initialize variables
$identifier = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $identifier = trim($_POST['identifier']);
    $password = $_POST['password'];

    // Check if inputs are empty
    if (empty($identifier) || empty($password)) {
        $_SESSION['error'] = "Username/Email and Password are required.";
        $_SESSION['identifier'] = $identifier; // Retain identifier
        header("Location: login.php");
        exit;
    }

    try {
        // Query user by username or email
        $stmt = $pdo->prepare("SELECT * FROM users WHERE username = :identifier OR email = :identifier");
        $stmt->execute([':identifier' => $identifier]);
        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($user && password_verify($password, $user['password'])) {
            // Successful login
            session_regenerate_id(true);
            $_SESSION['user_id'] = $user['user_id'];
            $_SESSION['username'] = $user['username'];

            // Generate a secure token for the session
            $token = bin2hex(random_bytes(64)); // Generate a random secure token

            // Store the token in the remember_tokens table
            $stmt = $pdo->prepare("INSERT INTO remember_tokens (user_id, token) VALUES (:user_id, :token)");
            $stmt->execute([':user_id' => $user['user_id'], ':token' => $token]);

            // Set the token as a cookie to remember the user
            setcookie('auth_token', $token, time() + 3600 * 24 * 30, '/', null, true, true); // Expires in 30 days

            header("Location: ../html codes/homepage.html");
            exit;
        } else {
            $_SESSION['error'] = "Invalid username/email or password.";
            $_SESSION['identifier'] = $identifier; // Retain identifier
        }
    } catch (PDOException $e) {
        error_log("Database error: " . $e->getMessage());
        $_SESSION['error'] = "A system error occurred. Please try again later.";
        $_SESSION['identifier'] = $identifier; // Retain identifier
    }

    header("Location: login.php");
    exit;
}
?>

<!-- HTML Form remains unchanged -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="../css codes/styles.css">
</head>
<body>
    <div class="container">
        <h2>Login</h2>
        <?php
        if (isset($_SESSION['error'])) {
            echo "<div class='error'>" . htmlspecialchars($_SESSION['error']) . "</div>";
            unset($_SESSION['error']);
        }
        ?>
        <form method="POST" action="login.php">
            <input 
                type="text" 
                name="identifier" 
                placeholder="Username or Email" 
                value="<?php echo isset($_SESSION['identifier']) ? htmlspecialchars($_SESSION['identifier']) : ''; ?>" 
                required
            >
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div style="margin-top: 15px" class="links">
            <span>Don't have an Account?</span>
            <a href="signup.php">Sign Up</a>
        </div>
    </div>
</body>
</html>
