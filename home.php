<?php

require_once("database/config.php");

if(!isset($_SESSION["session"]) || $_SESSION["session"] === false){
    header("location: login.php");
    exit;
}

$global_from_date = $global_to_date = $global_case_num = $global_county = $global_address = "";

if($_SERVER["REQUEST_METHOD"] == "POST"){
	$global_from_date = $_POST['from_date'];
	$global_to_date = $_POST['to_date'];
	$global_case_num = $_POST['case_num'];
	$global_county = $_POST['county'];
	$global_address = $_POST['address'];
}

$filter_style = "recent"

?>



<html>
	<head>
		<style type="text/css">
			
			* {box-sizing: border-box;}

			p, h1 { margin: 0; }

			body { 
				margin: 0;
				font-family: Arial, Helvetica, sans-serif;
			}

			.header {
				overflow: hidden;
				background-color: #f1f1f1;
				height: 14%;
				text-align: center;
			}

			.header a {
				float: left;
				color: black;
				text-align: center;
				padding: 20px;
				text-decoration: none;
				font-size: 18px; 
				line-height: 25px;
				border-radius: 4px;
			}

			.logo {
				position: relative;
				object-fit: contain;
				float: left;
				width: 10%;
				height: 80%;
				top: 50%;
				transform: translateY(-50%);
			}

			.header-right {
				position: relative;
				float: right;
				top: 50%;
				transform: translateY(-50%);
				width: 90%;
				display: flex;
				flex-direction: row;
				padding-left: 4%;
				justify-content: left;
			}

			.body-content {
				width: 100%;
				height: 86%;
				float: left;
				clear: none; 
			}

			.foreclosure-archive-header {
				width: 100%;
				height: 12%;
				justify-content: center;
				border-bottom: 1px solid black;
				display: flex;
				flex-direction: column;
			}

			.foreclosure-archive-header-text {
				position: relative;
				text-align: center;
				#transform: translateY(-50%);
			}

			.foreclosure-archive-body {
				height: 88%;
				width: 100%;
				display: flex;
				flex-direction: column;
				overflow: hidden;
			}

			.foreclosure-archive-filter {
				position: relative;
				width: 100%;
				max-height: 0%;
				float: left;
				overflow: auto;
				#border-bottom: 1px solid black;
			}

			.foreclosure-archive-results {
				position: relative;
				max-width: 100%;
				max-height: 100%;
				height: 100%;
				float: right;
				overflow: auto;
			}

			.filter-results-header {
				position: relative;
				top: 2.5%;
				text-align: center;
			}

			.search-results-header {
				position: relative;
				top: 2.5%;
				text-align: center;
				white-space: nowrap;
			}

			.filter-form {
				width: 100%;
				display: flex;
				flex-direction: column;
			}

			.filter-form-submit {
				margin-top: 3%;
				width: 60%;
				margin-left: 50%;
				transform: translateX(-50%);
			}

			.filter-form-date-selectors {
				display: flex;
				flex-direction: row;
				justify-content: center;
				margin-top: 3%;
			}

			.filter-form-enddate-selector {
				float: left;
				width: 100%;
			}
			.filter-form-startdate-selector {
				float: right;
				width: 100%;
			}
			.filter-form-button {
				width: 80%;
				margin-left: 50%;
				transform: translateX(-50%);
			}
			.filter-form-button-label {
				text-align: center;
				margin-top: 3%;
			}

			.filter-form-enddate-selector-div {
				display: flex;
				flex-direction: column;
				margin-right: 5%;
				text-align: center;
			}

			.filter-form-startdate-selector-div {
				display: flex;
				flex-direction: column;
				text-align: center;
			}

			.search-results-contents {
				position: relative;
				top: 5%;
			}
			
			.filter-popup-button {
				position: relative;
				margin-left: 50%;
				transform: translateX(-50%);
				width: 10%;
			}
			.table-row {
				white-space:nowrap;
				width:100%;
				#border: 1px solid black;
			}
			tr:nth-child(even) td {
				background: lightgrey;
			}
			th {
				position: -webkit-sticky;
				position: sticky;
				top: 0;
				background: lightgrey;
				text-align: left;
				font-weight: normal;
				font-size: 1.1rem;
				color: black;
				position: relative;
			}


		</style>
	</head>
	<body>
		<div class="header">
			<img class='logo' src='/images/contenderproperties-logo-bw.png'>
			<div class="header-right">
				<a href="home.php">Home</a>
				<a href="record.php">Test</a>
				<a href="archive.php">Archive</a>
				<a href="signup.php">Create Account</a>
				<a href="logout.php">Logout</a>
			</div>
		</div> 
		<div class='body-content'>
			<div class='foreclosure-archive-header'>
				<h1 class='foreclosure-archive-header-text'>Foreclosure Archive</h1>
				<button onclick="toggleFilterPage()" class='filter-popup-button'>Advanced Search</button>
			</div>
			<div class='foreclosure-archive-body'>
				<div class='foreclosure-archive-filter'>
					<h1 class='filter-results-header'>Filter</h1>
					<form action='home.php' method='post'>
						<div class='filter-form'>
							<div class='filter-form-date-selectors'>
								<div class='filter-form-enddate-selector-div'>
									<label>From</label>
									<input class='filter-form-enddate-selector' type='date' id='from_date' name='from_date'>
								</div>
								<div class='filter-form-startdate-selector-div'>
									<label>To</label>
									<input class='filter-form-startdate-selector' type='date' id='to_date' name='to_date'>
								</div>
							</div>
							<label class='filter-form-button-label'>Case Number</label>
							<input class='filter-form-button' type='text' id='case_num' name='case_num' placeholder='SP/CSV/CSD #'>
							<label class='filter-form-button-label'>County</label>
							<input class='filter-form-button' type='text' id='county' name='county' placeholder='County'>
							<label class='filter-form-button-label'>Address</label>
							<input class='filter-form-button' type='text' id='address' name='address' placeholder='Address'>
							<button class='filter-form-submit'>filter</button>
						</div>
					</form>	
				</div>
				<div class='foreclosure-archive-results'>
					<h1 class='search-results-header'>Results</h1>
					<div class='search-results-contents'>
						<table style='width:100%;'>
							<thead>
								<tr class='table-row' style='border: 1px solid black;'>
									<th><div style='border: 1px solid black;'>Date</div></th>
									<th><div style='border: 1px solid black;'>Case Number</div></th>
									<th><div style='border: 1px solid black;'>County</div></th>
									<th><div style='border: 1px solid black;'>Address</div></th>
									<th><div style='border: 1px solid black;'>Phone Number</div></th>
									<th><div style='border: 1px solid black;'>Trailer</div></th>
									<th><div style='border: 1px solid black;'>Listing Link</div></th>
								</tr>
							</thead>
							<tbody>

						<?php
						
							// $file = fopen("./foreclosures/output.csv","r+");

							// $row = 0;
							// $csvArray = array();
							
							// while(($data = fgetcsv($file, 0, ",")) !== FALSE){
							// 	$num = count($data);
							// 	for($c = 0; $c < $num; $c++){
							// 		$csvArray[$row][] = $data[$c];
							// 	}
							// 	$row++;
							// }
							
							// $csvData = array_splice($csvArray, 1);

							// $count = 0;
							// $date_array = array();
							// foreach($csvData as $key){
							// 	$date_array[$count] = $key[0];
							// 	$count++;
							// }


							// if($filter_style == "recent"){
							// 	rsort($date_array);
							// 	foreach($date_array as $item){
							// 		#echo $item;
							// 	}
							// }elseif($filter_style == "oldest"){
							// 	sort($date_array);
							// 	foreach($date_array as $item){
							// 		#echo $item;
							// 	}
							// }elseif($filter_style == "county_az"){

							// }elseif($filter_style == "county_za"){

							// }

							$query = "SELECT * FROM foreclosure_listing ORDER BY date_of_sale DESC";
							$res = mysqli_query($con, $query);
							if(is_object($res)){
								for($x = 0; $x < $res->num_rows; $x++){
									$row = $res->fetch_assoc();
									echo "<tr class='table-row' style='border: 1px solid black;'>";
									$date = $row['date_of_sale'];
									echo "<td><div style='border: 1px solid black;'>$date</div></td>";
									$case_num = $row['case_num'];
									echo "<td><div style='border: 1px solid black;'>$case_num</div></td>";
									$county = $row['county'];
									echo "<td><div style='border: 1px solid black;'>$county</div></td>";
									$address = $row['address'];
									echo "<td><div style='border: 1px solid black;'>$address</div></td>";
									$phone = $row['phone'];
									echo "<td><div style='border: 1px solid black;'>$phone</div></td>";
									$trailer = $row['trailer'];
									echo "<td><div style='border: 1px solid black;'>$trailer</div></td>";
									$link = $row['link'];
									echo "<td><div style='border: 1px solid black;'><a href='$link'>Listing Link</a></div></td>";
									echo "</tr>";
								}
							}

							// $file = fopen("./foreclosures/output.csv","r+");

							// $count = 0;
							
							
							// while(($data = fgetcsv($file, 0, ",")) !== FALSE){
							// 	if ($count == 0){
							// 		$count = 1;
							// 		continue;
							// 	}
							// 	if($global_address == "" && $global_case_num == "" && $global_county == "" && $global_from_date == "" && $global_to_date == ""){
							// 		echo "<tr class='table-row' style='border: 1px solid black;'>";
							// 		$date = $data[0];
							// 		echo "<td><div style='border: 1px solid black;'>$date</div></td>";
							// 		$case_num = $data[1];
							// 		echo "<td><div style='border: 1px solid black;'>$case_num</div></td>";
							// 		$county = $data[2];
							// 		echo "<td><div style='border: 1px solid black;'>$county</div></td>";
							// 		$address = $data[3];
							// 		echo "<td><div style='border: 1px solid black;'>$address</div></td>";
							// 		$phone = $data[4];
							// 		echo "<td><div style='border: 1px solid black;'>$phone</div></td>";
							// 		$trailer = $data[5];
							// 		echo "<td><div style='border: 1px solid black;'>$trailer</div></td>";
							// 		$link = $data[6];
							// 		echo "<td><div style='border: 1px solid black;'><a href='$link'>Listing Link</a></div></td>";
							// 		echo "</tr>";
							// 		continue;
							// 	}
							// 	if($global_address != "" && str_contains($data[3], $global_address)){
									
							// 		echo "<tr class='table-row' style='border: 1px solid black;'>";
							// 		$date = $data[0];
							// 		echo "<td><div style='border: 1px solid black;'>$date</div></td>";
							// 		$case_num = $data[1];
							// 		echo "<td><div style='border: 1px solid black;'>$case_num</div></td>";
							// 		$county = $data[2];
							// 		echo "<td><div style='border: 1px solid black;'>$county</div></td>";
							// 		$address = $data[3];
							// 		echo "<td><div style='border: 1px solid black;'>$address</div></td>";
							// 		$phone = $data[4];
							// 		echo "<td><div style='border: 1px solid black;'>$phone</div></td>";
							// 		$trailer = $data[5];
							// 		echo "<td><div style='border: 1px solid black;'>$trailer</div></td>";
							// 		$link = $data[6];
							// 		echo "<td><div style='border: 1px solid black;'><a href='$link'>Listing Link</a></div></td>";
							// 		echo "</tr>";
							// 		continue;
							// 	}
							// 	if($global_case_num != "" && str_contains($data[1], $global_case_num)){
							// 		echo 2;
							// 		echo "<tr class='table-row' style='border: 1px solid black;'>";
							// 		$date = $data[0];
							// 		echo "<td><div style='border: 1px solid black;'>$date</div></td>";
							// 		$case_num = $data[1];
							// 		echo "<td><div style='border: 1px solid black;'>$case_num</div></td>";
							// 		$county = $data[2];
							// 		echo "<td><div style='border: 1px solid black;'>$county</div></td>";
							// 		$address = $data[3];
							// 		echo "<td><div style='border: 1px solid black;'>$address</div></td>";
							// 		$phone = $data[4];
							// 		echo "<td><div style='border: 1px solid black;'>$phone</div></td>";
							// 		$trailer = $data[5];
							// 		echo "<td><div style='border: 1px solid black;'>$trailer</div></td>";
							// 		$link = $data[6];
							// 		echo "<td><div style='border: 1px solid black;'><a href='$link'>Listing Link</a></div></td>";
							// 		echo "</tr>";
							// 		continue;
							// 	}
							// 	if($global_county != "" && str_contains($data[2], $global_county)){
							// 		echo 3;
							// 		echo "<tr class='table-row' style='border: 1px solid black;'>";
							// 		$date = $data[0];
							// 		echo "<td><div style='border: 1px solid black;'>$date</div></td>";
							// 		$case_num = $data[1];
							// 		echo "<td><div style='border: 1px solid black;'>$case_num</div></td>";
							// 		$county = $data[2];
							// 		echo "<td><div style='border: 1px solid black;'>$county</div></td>";
							// 		$address = $data[3];
							// 		echo "<td><div style='border: 1px solid black;'>$address</div></td>";
							// 		$phone = $data[4];
							// 		echo "<td><div style='border: 1px solid black;'>$phone</div></td>";
							// 		$trailer = $data[5];
							// 		echo "<td><div style='border: 1px solid black;'>$trailer</div></td>";
							// 		$link = $data[6];
							// 		echo "<td><div style='border: 1px solid black;'><a href='$link'>Listing Link</a></div></td>";
							// 		echo "</tr>";
							// 		continue;
							// 	}
							// }
							
							
							#echo type($data[0]);
							// 	echo $data;
							// endwhile;

						?>

							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
		<script src='/js/home.js'></script>
	</body>
</html>
