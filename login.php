<?php

require_once("database/config.php");

if(isset($_SESSION["session"]) && $_SESSION["session"] === true){
    header("location: home_page.php");
    exit;
}

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

        $query = "SELECT * FROM users WHERE email = '$param_email'";
        $result = mysqli_query($con, $query);
        if (is_object($result)) {
            if ($result->num_rows === 1) {
                $row = $result->fetch_assoc();
                if(password_verify($password, $row['password'])){
                    session_start();    
                    $_SESSION["session"] = true;
                    $_SESSION["user_id"] = $row['user_id'];
                    $_SESSION["email"] = $row['email'];
                    $_SESSION["role"] = $row['role'];
                    header("location: home.php");
                }
		        $_SESSION['last_email'] = trim($_POST["email"]);
                $login_err = "Invalid password";
            }else{
                $login_err = "Invalid email";
            }
        }else{
                $login_err = "Problem occured in database";
        }
        mysqli_close($con);
    }
}


?>

<html>
    <head>
        <script src="./js/test.js"></script>
        
        <style type="text/css">
        .full-page-div {
            height: 50%;
            width: 57.6%;
            position: absolute;
            margin-left: 50%;
            top: 37%;
            transform: translate(-50%, 0%);
            overflow: auto;
            border-width: 10;
            border-color: black;
            overflow: hidden;
        }
        .login-banner {
            margin-top: 4%;
            text-align: center;
            color: black;#white;
            font-size: 30;
            font-family: Helvetica;
            font-weight: bold;
            margin-bottom: 4%;
        }
        .login-form-div {
            margin-left: 50%;
            transform: translateX(-50%);
            width: 100%;
            height: 100%;
            display: flex;
            justify-content: start;
            flex-direction: column;
        }
        .input {
            margin-left: 50%;
            transform: translateX(-50%);
            width: 100%;
            height: 10%;
            border-width: 0;
            border-bottom-width: 1;
            border-bottom-color: black;#white;
            border-radius: 0;
            font-size: 20;
            background-color: white;#rgb(11, 11, 69);
            color: black;#white;
        }
        .login-button {
            margin-left: 50%;
            border-radius: 30px;
            border-color: black;#white;
            border-width: 1;
            transform: translateX(-50%);
            margin-top: 6%;
            width: 100%;
            height: 10%;
            background-color: white;#rgb(11, 11, 69);
            color: black;#white;
            cursor:pointer;
        }
        .login-err-text {
            text-align: center;
            font-family: Helvetica;
            font-size: 15;
            color: black;#white;
        }
        .palmtree-image {
            position: absolute;
            margin-left: 50%;
            transform: translate(-55%, -125%);
            height: 30%;
            width: 40%;
            object-fit: contain;
        }
        .company-logo {
            position: absolute;
            margin-left: 50%;
            top: 15%;
            transform: translate(-50%, -20%);
            height: 25%;
            width: 32%;
            object-fit: contain;
        }
        </style>
    </head>
    <body style='background-color: white;'>
    <img class='company-logo' src='/images/contenderproperties-logo-bw.png'>
        <div class='full-page-div'>
            <p class='login-banner'>Login</p>
            <div>
                <p class='login-err-text'><?php echo $login_err ?></p>
                <script></script>
                <form class='login-form-div' action='login.php' method='post'>
                    <input class='input' type='text' name='email' placeholder='Email'>
                    <br>
                    <input class='input' type='password' name='password' placeholder='Password'>
                    <br>
                    <button class='login-button'>Login</button>
                </form>
            </div>
            <!-- <img class='palmtree-image' src='/images/palmtree-watermark.png'> -->
        </div>
    </body>
</html>
