<?php
/* Attempt MySQL server connection. Assuming you are running MySQL
server with default setting (user 'root' with no password) */
$mysqli = new mysqli("192.168.7.95", "jagpal78", "686Shanghai", "dashboard");
 
// Check connection
if($mysqli === false){
    die("ERROR: Could not connect. " . $mysqli->connect_error);
}

// Print host information
$sql = "SELECT * FROM run";
$result = $mysqli->query($sql);
$return_arr = array();
if ($result->num_rows > 0) {
    // output data of each row
    while($row = $result->fetch_assoc()) {
          $row_array['day'] = $row['day'];
		  $row_array['miles'] = $row['miles'];
		  array_push($return_arr,$row_array);
    }
} else
    echo json_encode($return_arr);
echo json_encode($return_arr);
$mysqli->close();
?>