<?php

require_once("database/config.php");

$email = $password = $login_err = "";

if($_SERVER["REQUEST_METHOD"] == "POST"){
    if(empty(trim($_POST["email"]))){
        $login_err = "Please enter email.";
    } else{
        $email = trim($_POST["email"]);
    }
    
    if(empty(trim($_POST["password"]))){
        $login_err = "Please enter your password.";
    } else{
        $password = trim($_POST["password"]);
    }
    
    if(empty($login_err)){
        $param_email = $_POST['email'];
        $password = $_POST['password'];
        $param_password = password_hash($password, PASSWORD_DEFAULT);

        $query = "INSERT INTO users (email, password) VALUES ('$param_email', '$param_password')";
        if (mysqli_query($con, $query)){
            
        }else{
            echo mysqli_error($con);
        }
        
    }
}


?>

<html>
    <head>
        <style type="text/css">
        .full-page-div {
            height: 80%;
            width: 80%;
            position: absolute;
            margin-left: 50%;
            top: 15%;
            transform: translate(-50%, 0%);
        }
        .login-banner {
            text-align: center;
            color: white;
            font-size: 30;
            font-family: Helvetica;
            font-weight: bold;
            margin-bottom: 4%;
        }
        .login-form-div {
            margin-left: 50%;
            transform: translateX(-50%);
            width: 80%;
            height: 70%;
            display: flex;
            justify-content: start;
            flex-direction: column;
        }
        .input {
            margin-left: 50%;
            transform: translateX(-50%);
            width: 72%;
            height: 8%;
            border-width: 0;
            border-bottom-width: 1;
            border-bottom-color: white;
            font-size: 20;
            background-color: rgb(11, 11, 69);
            color: white;
        }
        .login-button {
            margin-left: 50%;
            border-radius: 30px;
            border-color: white;
            border-width: 1;
            transform: translateX(-50%);
            margin-top: 4%;
            width: 72%;
            height: 8%;
            background-color: rgb(11, 11, 69);
            color: white;
        }
        .login-err-text {
            text-align: center;
            font-family: Helvetica;
            font-size: 15;
            color: white;
        }
        </style>
    </head>
    <body style='background-color: rgb(11, 11, 69);'>
        <div class='full-page-div'>
            <p class='login-banner'>Signup</p>
            <div>
                <p class='login-err-text'><?php echo $login_err ?></p>
                <form class='login-form-div' action='signup.php' method='post'>
                    <input class='input' type='text' name='email' placeholder='Email'>
                    <br>
                    <input class='input' type='password' name='password' placeholder='Password'>
                    <br>
                    <button class='login-button'>Signup</button>
                </form>
            </div>
        </div>
    </body>
</html>
