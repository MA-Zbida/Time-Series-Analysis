<?php
session_start();
require 'db_connection.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitize and trim inputs
    $username = filter_var(trim($_POST['username']), FILTER_SANITIZE_STRING);
    $email = filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL);
    $password = $_POST['password'];

    // Validation checks
    $errors = [];

    // Username validation
    if (empty($username)) {
        $errors[] = "Username is required.";
    } elseif (strlen($username) < 3 || strlen($username) > 20) {
        $errors[] = "Username must be between 3 and 20 characters.";
    } elseif (!preg_match("/^[a-zA-Z0-9_]+$/", $username)) {
        $errors[] = "Username can only contain letters, numbers, and underscores.";
    }

    // Email validation
    if (empty($email)) {
        $errors[] = "Email is required.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $errors[] = "Invalid email format.";
    }

    // Password validation
    if (empty($password)) {
        $errors[] = "Password is required.";
    } elseif (strlen($password) < 8) {
        $errors[] = "Password must be at least 8 characters long.";
    } elseif (!preg_match("/^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$/", $password)) {
        $errors[] = "Password must include at least one letter, one number, and one special character.";
    }

    // If there are validation errors
    if (!empty($errors)) {
        $_SESSION['error'] = implode("<br>", $errors);
        $_SESSION['username'] = $username; // Retain username
        $_SESSION['email'] = $email;      // Retain email
        header("Location: signup.php");
        exit;
    }

    try {
        // Check if username or email already exists
        $stmt = $pdo->prepare("SELECT * FROM Users WHERE username = :username OR email = :email");
        $stmt->execute([
            ':username' => $username,
            ':email' => $email
        ]);
        $existingUser = $stmt->fetch();

        if ($existingUser) {
            $_SESSION['error'] = "Username or email already exists. Please choose a different one.";
            $_SESSION['username'] = $username; // Retain username
            $_SESSION['email'] = $email;      // Retain email
            header("Location: signup.php");
            exit;
        }

        // Hash the password
        $hashed_password = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);

        // Insert the new user
        $stmt = $pdo->prepare("INSERT INTO Users (username, email, password) VALUES (:username, :email, :password)");
        $stmt->execute([
            ':username' => $username,
            ':email' => $email,
            ':password' => $hashed_password
        ]);

        $_SESSION['signup_success'] = "Signup successful! You can now log in.";
        header("Location: login.php");
        exit;

    } catch (PDOException $e) {
        error_log("Signup error: " . $e->getMessage());
        $_SESSION['error'] = "An unexpected error occurred. Please try again later.";
        $_SESSION['username'] = $username; // Retain username
        $_SESSION['email'] = $email;      // Retain email
        header("Location: signup.php");
        exit;
    }
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sign Up</title>
    <link rel="stylesheet" href="../css codes/styles.css">
</head>
<body>
    <div class="container">
        <h2>Sign Up</h2>
        <?php
        if (isset($_SESSION['error'])) {
            echo "<div class='error'>" . $_SESSION['error'] . "</div>";
            unset($_SESSION['error']);
        }
        ?>
        <form method="POST" action="signup.php">
            <input 
                type="text" 
                name="username" 
                placeholder="Username" 
                value="<?php echo isset($_SESSION['username']) ? htmlspecialchars($_SESSION['username']) : ''; ?>" 
                required
            >
            <input 
                type="email" 
                name="email" 
                placeholder="Email" 
                value="<?php echo isset($_SESSION['email']) ? htmlspecialchars($_SESSION['email']) : ''; ?>" 
                required
            >
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign Up</button>
        </form>
        <div style="margin-top: 15px" class="links">
            <span>Already have an account?</span>
            <a href="login.php">Log In</a>
        </div>
    </div>
</body>
</html>
