<?php

$conn = mysqli_connect("database", "username", "password", "table"); #Removed credentials
if(!$conn){
	die("Connection failed: ".mysqli_connect_error()); #Remove error or be prone to injections!!!! Only for testing
}
