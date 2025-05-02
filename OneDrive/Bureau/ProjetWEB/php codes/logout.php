<?php
// Start the session
session_start();

// Destroy all session data
session_unset();
session_destroy();

// Remove the auth_token cookie by setting it to expire in the past
setcookie('auth_token', '', time() - 3600, '/', null, true, true); // Expire the cookie by setting a past time

// Redirect to the login page after logout
header("Location: login.php");
exit();
?>
