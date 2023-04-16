<?php
session_start();

/* haiku time */

$host = "Once again, you search"; /* Host name */
$user = "For passwords, only to fail"; /* User */
$password = "Please, friend, try harder"; /* Password */

$con = mysqli_connect($host, $user, $password, $dbname);
// Check connection
if (!$con) {
  die("Failed to connect to database: " . mysqli_connect_error());
}